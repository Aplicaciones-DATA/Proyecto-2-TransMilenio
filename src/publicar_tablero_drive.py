"""Sube al Drive compartido un paquete verificado del borrador de Power BI.

Uso: python src/publicar_tablero_drive.py outputs/Paquete_tablero_AAAAMMDD_HHMMSS.zip
La autorización OAuth queda en el PC; no se guarda ni se publica en el repositorio.
"""

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from googleapiclient.http import MediaFileUpload

from empaquetar_tablero import ARCHIVOS
from recolectar_a_drive import credenciales_drive, servicio_drive


PROYECTO = Path(__file__).resolve().parent.parent
CONFIGURACION = PROYECTO / "config" / "captura_local.json"
CARPETA_PRIVADA = Path.home() / "AppData" / "Local" / "Proyecto2TransMilenio"


def huella_md5(ruta):
    resumen = hashlib.md5()
    with ruta.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            resumen.update(bloque)
    return resumen.hexdigest()


def comprobar_paquete(ruta):
    ruta = ruta.resolve()
    if ruta.parent != (PROYECTO / "outputs").resolve():
        raise ValueError("El paquete debe estar en outputs/ de este proyecto.")
    if not ruta.name.startswith("Paquete_tablero_") or ruta.suffix.lower() != ".zip":
        raise ValueError("Se esperaba un ZIP generado por empaquetar_tablero.py.")
    with ZipFile(ruta) as paquete:
        if paquete.testzip() is not None or paquete.namelist() != ARCHIVOS:
            raise ValueError("Contenido incompleto, inesperado o dañado en el ZIP.")
    return ruta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paquete", type=Path)
    args = parser.parse_args()
    paquete = comprobar_paquete(args.paquete)
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
        raise ValueError("El ID configurado no corresponde a una carpeta de Drive.")
    if not any(
        permiso.get("emailAddress", "").lower() == "s.rojasm23@uniandes.edu.co"
        for permiso in carpeta.get("permissions", [])
    ):
        raise RuntimeError("No se confirmó el acceso de Alejandro a la carpeta compartida.")
    print("Carpeta verificada:", carpeta["name"], carpeta["webViewLink"], flush=True)

    nombre_seguro = paquete.name.replace("'", "\\'")
    consulta = f"name = '{nombre_seguro}' and '{carpeta_id}' in parents and trashed = false"
    encontrados = servicio.files().list(
        q=consulta,
        fields="files(id,name,size,md5Checksum,webViewLink,parents)",
        pageSize=10,
    ).execute().get("files", [])
    if len(encontrados) > 1:
        raise RuntimeError("Hay varios paquetes con el mismo nombre: revisar Drive.")
    md5_local = huella_md5(paquete)
    tamano = paquete.stat().st_size
    if encontrados:
        archivo = encontrados[0]
        if archivo.get("md5Checksum") != md5_local or int(archivo["size"]) != tamano:
            raise RuntimeError("Ya existe un archivo con ese nombre y distinto contenido.")
        print("Ya estaba subido y verificado:", archivo["webViewLink"], flush=True)
        return

    medio = MediaFileUpload(str(paquete), mimetype="application/zip", resumable=True)
    creado = servicio.files().create(
        body={"name": paquete.name, "parents": [carpeta_id]},
        media_body=medio,
        fields="id,name,size,md5Checksum,webViewLink,parents",
    ).execute()
    leido = servicio.files().get(
        fileId=creado["id"],
        fields="id,name,size,md5Checksum,webViewLink,parents",
    ).execute()
    if (
        leido["name"] != paquete.name
        or int(leido["size"]) != tamano
        or leido.get("md5Checksum") != md5_local
        or carpeta_id not in leido.get("parents", [])
    ):
        raise RuntimeError("La verificación de tamaño, contenido o carpeta en Drive falló.")
    print("Paquete subido y verificado:", leido["webViewLink"], flush=True)


if __name__ == "__main__":
    main()
