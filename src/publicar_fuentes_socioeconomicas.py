"""Sube fuentes oficiales a la carpeta privada de Drive del proyecto.

El archivo OAuth y el token permanecen en el PC, fuera de este repositorio.
El script no publica los datos en GitHub ni cambia los originales.
"""

import hashlib
import json
import os
from pathlib import Path

from googleapiclient.http import MediaFileUpload

from recolectar_a_drive import (
    buscar_o_crear_carpeta,
    credenciales_drive,
    servicio_drive,
)


PROYECTO = Path(__file__).resolve().parent.parent
FUENTES = PROYECTO.parent / "fuentes_compartidas" / "socioeconomicos"
CONFIGURACION = PROYECTO / "config" / "captura_local.json"
CARPETA_PRIVADA = Path(os.environ["LOCALAPPDATA"]) / "Proyecto2TransMilenio"

# El tamaño esperado permite detectar una descarga incompleta antes de subirla.
ARCHIVOS = [
    ("em2021.csv", 1254896789, "CC BY 4.0"),
    ("diccionario_em2021.ods", 100117, "CC BY 4.0"),
    ("variables_adicionales_em2021.csv", 105740264, "CC BY 4.0"),
    ("diccionario_variables_adicionales_em2021.ods", 12822, "CC BY 4.0"),
    ("geometria_upz_indicador_espacio_publico.zip", 867343, "CC BY-SA 4.0"),
    ("proyecciones_poblacion_upz_2005_2035.ods", 1954607, "CC BY 4.0"),
    ("limites_localidades_bogota.json", 2363493, "CC BY 4.0"),
]


def huellas(archivo):
    """Calcula las huellas de seguridad sin cargar todo el archivo en memoria."""
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()
    with archivo.open("rb") as origen:
        for bloque in iter(lambda: origen.read(8 * 1024 * 1024), b""):
            sha256.update(bloque)
            md5.update(bloque)
    return sha256.hexdigest(), md5.hexdigest()


def archivo_en_drive(servicio, carpeta, nombre):
    """Busca una copia con ese nombre en la carpeta compartida."""
    nombre_seguro = nombre.replace("'", "\\'")
    consulta = (
        f"name = '{nombre_seguro}' and '{carpeta}' in parents and trashed = false"
    )
    resultado = servicio.files().list(
        q=consulta, fields="files(id,name,size,md5Checksum,webViewLink)", pageSize=10
    ).execute()
    encontrados = resultado.get("files", [])
    if len(encontrados) > 1:
        raise RuntimeError(f"Hay varias copias de {nombre} en Drive: revisar primero.")
    return encontrados[0] if encontrados else None


def subir_y_verificar(servicio, carpeta, nombre, tamano, licencia):
    origen = FUENTES / nombre
    if not origen.is_file():
        raise FileNotFoundError(origen)
    if origen.stat().st_size != tamano:
        raise ValueError(f"El tamaño de {nombre} no coincide con el portal oficial.")

    sha256, md5 = huellas(origen)
    anterior = archivo_en_drive(servicio, carpeta, nombre)
    if anterior:
        if anterior.get("md5Checksum") != md5 or int(anterior["size"]) != tamano:
            raise RuntimeError(f"Ya existe {nombre} con contenido diferente en Drive.")
        print("Ya estaba verificado:", nombre, flush=True)
        return anterior

    descripcion = (
        f"Fuente: Datos Abiertos Bogotá; licencia: {licencia}; "
        f"SHA-256 local: {sha256}; bytes: {tamano}. "
        "Consultar docs/fuentes_socioeconomicas.md para URL y limitaciones."
    )
    medio = MediaFileUpload(
        str(origen), mimetype="application/octet-stream",
        chunksize=16 * 1024 * 1024, resumable=True
    )
    solicitud = servicio.files().create(
        body={"name": nombre, "parents": [carpeta], "description": descripcion},
        media_body=medio,
        fields="id,name,size,md5Checksum,webViewLink",
    )
    respuesta = None
    while respuesta is None:
        progreso, respuesta = solicitud.next_chunk(num_retries=5)
        if progreso:
            print(nombre, round(progreso.progress() * 100), "%", flush=True)

    if int(respuesta["size"]) != tamano or respuesta.get("md5Checksum") != md5:
        raise RuntimeError(f"Drive recibió {nombre}, pero la verificación no coincide.")
    print("Verificado en Drive:", nombre, respuesta.get("webViewLink"), flush=True)
    return respuesta


def main():
    configuracion = json.loads(CONFIGURACION.read_text(encoding="utf-8"))
    credenciales = credenciales_drive(
        CARPETA_PRIVADA / "oauth_client.json",
        CARPETA_PRIVADA / "drive_token.json",
    )
    servicio = servicio_drive(credenciales, configuracion["correo_esperado"])
    carpeta = buscar_o_crear_carpeta(
        servicio, "fuentes_socioeconomicas", configuracion["carpeta_drive_id"]
    )
    print("Carpeta compartida:", f"https://drive.google.com/drive/folders/{carpeta}")
    for nombre, tamano, licencia in ARCHIVOS:
        subir_y_verificar(servicio, carpeta, nombre, tamano, licencia)


if __name__ == "__main__":
    main()
