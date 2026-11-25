"""Sube una copia PBIX nueva al Drive compartido, sin reemplazar archivos.

Uso: python src/publicar_pbix_drive.py outputs/archivo.pbix
La credencial de Drive permanece en este PC y fuera del repositorio.
"""

import argparse
import hashlib
import json
from pathlib import Path

from googleapiclient.http import MediaFileUpload

from recolectar_a_drive import credenciales_drive, servicio_drive


PROYECTO = Path(__file__).resolve().parent.parent
CONFIGURACION = PROYECTO / "config" / "captura_local.json"
CARPETA_PRIVADA = Path.home() / "AppData" / "Local" / "Proyecto2TransMilenio"


def md5_archivo(ruta):
    resumen = hashlib.md5()
    with ruta.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            resumen.update(bloque)
    return resumen.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archivo", type=Path)
    args = parser.parse_args()
    ruta = args.archivo.resolve()
    if ruta.parent != (PROYECTO / "outputs").resolve() or ruta.suffix.lower() != ".pbix":
        raise ValueError("Solo se permite un PBIX de outputs/ de este proyecto.")
    if not ruta.is_file():
        raise FileNotFoundError(ruta)

    configuracion = json.loads(CONFIGURACION.read_text(encoding="utf-8"))
    credenciales = credenciales_drive(
        CARPETA_PRIVADA / "oauth_client.json",
        CARPETA_PRIVADA / "drive_token.json",
    )
    servicio = servicio_drive(credenciales, configuracion["correo_esperado"])
    carpeta_id = configuracion["carpeta_drive_id"]
    carpeta = servicio.files().get(
        fileId=carpeta_id,
        fields="id,name,mimeType,webViewLink,permissions(emailAddress,role)",
    ).execute()
    if carpeta["mimeType"] != "application/vnd.google-apps.folder":
        raise ValueError("La carpeta configurada no es una carpeta de Drive.")
    if not any(
        permiso.get("emailAddress", "").lower() == "s.rojasm23@uniandes.edu.co"
        for permiso in carpeta.get("permissions", [])
    ):
        raise RuntimeError("No se confirmó el acceso de Alejandro a la carpeta.")

    nombre_seguro = ruta.name.replace("'", "\\'")
    consulta = f"name = '{nombre_seguro}' and '{carpeta_id}' in parents and trashed = false"
    encontrados = servicio.files().list(
        q=consulta, fields="files(id,name,size,md5Checksum,webViewLink,parents)", pageSize=10,
    ).execute().get("files", [])
    if len(encontrados) > 1:
        raise RuntimeError("Hay varios archivos con el mismo nombre en Drive.")
    md5_local = md5_archivo(ruta)
    tamano_local = ruta.stat().st_size
    if encontrados:
        existente = encontrados[0]
        if existente.get("md5Checksum") != md5_local or int(existente["size"]) != tamano_local:
            raise RuntimeError("El nombre ya existe en Drive, pero con otro contenido.")
        print("La copia ya estaba subida y verificada:", existente["webViewLink"])
        return

    medio = MediaFileUpload(str(ruta), mimetype="application/octet-stream", resumable=True)
    creado = servicio.files().create(
        body={"name": ruta.name, "parents": [carpeta_id]},
        media_body=medio, fields="id",
    ).execute()
    leido = servicio.files().get(
        fileId=creado["id"], fields="id,name,size,md5Checksum,webViewLink,parents",
    ).execute()
    if (
        leido["name"] != ruta.name
        or int(leido["size"]) != tamano_local
        or leido.get("md5Checksum") != md5_local
        or carpeta_id not in leido.get("parents", [])
    ):
        raise RuntimeError("Falló la comprobación de contenido o carpeta en Drive.")
    print("Nueva copia subida y verificada:", leido["webViewLink"])


if __name__ == "__main__":
    main()
