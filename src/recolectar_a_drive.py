"""Captura GTFS/GTFS-RT en franjas y guarda los bytes directamente en Drive.

No escribe archivos de datos en el disco local. Requiere autorización OAuth
de la cuenta personal antes de su primer uso real.
"""

import argparse
import ctypes
import gzip
import hashlib
import io
import json
import os
import time
import zipfile
from datetime import date, datetime
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


ZONA = ZoneInfo("America/Bogota")
PERMISO_DRIVE = ["https://www.googleapis.com/auth/drive"]


def leer_configuracion(ruta):
    configuracion = json.loads(Path(ruta).read_text(encoding="utf-8"))
    franjas = configuracion.get("franjas", [])
    fuentes = configuracion.get("fuentes", {})
    if not configuracion.get("correo_esperado") or not configuracion.get("carpeta_drive_id"):
        raise ValueError("Faltan correo_esperado o carpeta_drive_id en la configuración privada.")
    if not franjas:
        raise ValueError("Faltan las franjas horarias: defínelas antes de iniciar la captura.")
    for nombre in ("positions", "tripupdates", "alerts", "gtfs"):
        url = fuentes.get(nombre, "")
        if not url.startswith("https://"):
            raise ValueError(f"Falta una URL HTTPS verificada para {nombre}.")
    franjas_revisadas = []
    for franja in franjas:
        inicio, fin = separar_franja(franja)
        if inicio >= fin:
            raise ValueError(f"La franja debe terminar después de empezar: {franja}")
        for anterior in franjas_revisadas:
            inicio_anterior, fin_anterior = separar_franja(anterior)
            if inicio < fin_anterior and fin > inicio_anterior:
                raise ValueError("Las franjas habituales no pueden solaparse.")
        franjas_revisadas.append(franja)
    if not configuracion.get("fecha_inicio") or not configuracion.get("fecha_fin"):
        raise ValueError("Faltan fecha_inicio y fecha_fin para limitar los días de captura.")
    inicio = date.fromisoformat(configuracion["fecha_inicio"])
    fin = date.fromisoformat(configuracion["fecha_fin"])
    if inicio > fin:
        raise ValueError("fecha_fin debe ser igual o posterior a fecha_inicio.")
    adicionales_por_fecha = configuracion.get("franjas_adicionales_por_fecha", {})
    if not isinstance(adicionales_por_fecha, dict):
        raise ValueError("franjas_adicionales_por_fecha debe ser un objeto por fecha.")
    for fecha_texto, adicionales in adicionales_por_fecha.items():
        dia = date.fromisoformat(fecha_texto)
        if not inicio <= dia <= fin or not isinstance(adicionales, list):
            raise ValueError("Cada fecha adicional debe estar en la prueba y contener una lista de franjas.")
        franjas_del_dia = franjas.copy()
        for franja in adicionales:
            hora_inicio, hora_fin = separar_franja(franja)
            if hora_inicio >= hora_fin:
                raise ValueError(f"La franja debe terminar después de empezar: {franja}")
            for existente in franjas_del_dia:
                inicio_existente, fin_existente = separar_franja(existente)
                if hora_inicio < fin_existente and hora_fin > inicio_existente:
                    raise ValueError("Las franjas adicionales no pueden solaparse con otra franja.")
            franjas_del_dia.append(franja)
    return configuracion


def separar_franja(franja):
    inicio, fin = franja.split("-")
    return datetime.strptime(inicio, "%H:%M").time(), datetime.strptime(fin, "%H:%M").time()


def fecha_permitida(configuracion, dia):
    """Impide capturas fuera del intervalo acordado, aunque se ejecute el programa."""
    inicio = date.fromisoformat(configuracion["fecha_inicio"])
    fin = date.fromisoformat(configuracion["fecha_fin"])
    return inicio <= dia <= fin


def franjas_para_fecha(configuracion, dia):
    """Combina las franjas habituales con las adicionales de ese día, si existen."""
    adicionales = configuracion.get("franjas_adicionales_por_fecha", {})
    return configuracion["franjas"] + adicionales.get(dia.isoformat(), [])


def preparar_token_para_cliente(datos_token, datos_cliente):
    """Actualiza el secreto del mismo cliente OAuth sin cambiar de cuenta ni permisos."""
    if datos_token.get("client_id") != datos_cliente.get("client_id"):
        raise RuntimeError("El token guardado pertenece a otro cliente OAuth.")
    if not datos_cliente.get("client_secret"):
        raise ValueError("Al archivo OAuth del cliente le falta client_secret.")
    actualizado = datos_token.copy()
    actualizado["client_secret"] = datos_cliente["client_secret"]
    return actualizado


def credenciales_drive(ruta_cliente, ruta_token, autorizar=False):
    from google.auth.transport.requests import Request as GoogleRequest
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    datos_cliente = json.loads(Path(ruta_cliente).read_text(encoding="utf-8")).get("installed", {})
    if not datos_cliente.get("client_id") or not datos_cliente.get("client_secret"):
        raise ValueError("El JSON OAuth de escritorio está incompleto.")
    token = Path(ruta_token)
    credenciales = None
    if token.exists():
        datos_token = json.loads(token.read_text(encoding="utf-8"))
        datos_actualizados = preparar_token_para_cliente(datos_token, datos_cliente)
        secreto_rotado = datos_actualizados["client_secret"] != datos_token.get("client_secret")
        credenciales = Credentials.from_authorized_user_info(datos_actualizados, PERMISO_DRIVE)
        # Comprobar ante Google el secreto nuevo, aunque el token anterior aún no venza.
        if secreto_rotado or credenciales.expired:
            if not credenciales.refresh_token:
                raise RuntimeError("El token no permite renovar la sesión; autoriza Drive otra vez.")
            credenciales.refresh(GoogleRequest())
    if not credenciales or not credenciales.valid:
        if not autorizar:
            raise RuntimeError("Falta autorizar Drive. No se abrirá el navegador sin --autorizar.")
        flujo = InstalledAppFlow.from_client_secrets_file(
            str(ruta_cliente), PERMISO_DRIVE, autogenerate_code_verifier=True
        )
        credenciales = flujo.run_local_server(
            port=0,
            authorization_prompt_message="",
            success_message="Autorización terminada. Puedes cerrar esta pestaña.",
            timeout_seconds=900,
        )
    return credenciales


def servicio_drive(credenciales, correo_esperado):
    from googleapiclient.discovery import build

    servicio = build("drive", "v3", credentials=credenciales)
    cuenta = servicio.about().get(fields="user(emailAddress)").execute()["user"]["emailAddress"]
    if cuenta.lower() != correo_esperado.lower():
        raise RuntimeError(f"Cuenta incorrecta: {cuenta}. No se subió ningún archivo.")
    print("Cuenta de Drive comprobada:", cuenta, flush=True)
    return servicio


def buscar_o_crear_carpeta(servicio, nombre, padre):
    nombre_seguro = nombre.replace("'", "\\'")
    filtro = f"name = '{nombre_seguro}' and '{padre}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    respuesta = servicio.files().list(q=filtro, fields="files(id,name,createdTime)", pageSize=10).execute()
    carpetas = respuesta.get("files", [])
    if len(carpetas) > 1:
        ocupadas = []
        for carpeta in carpetas:
            hijos = servicio.files().list(
                q=f"'{carpeta['id']}' in parents and trashed = false",
                fields="files(id)", pageSize=1,
            ).execute().get("files", [])
            if hijos:
                ocupadas.append(carpeta)
        if len(ocupadas) > 1:
            raise RuntimeError(f"Hay varias carpetas con archivos llamadas {nombre}; requieren revisión manual.")
        candidatas = ocupadas or carpetas
        elegida = min(candidatas, key=lambda carpeta: (carpeta.get("createdTime", ""), carpeta["id"]))
        print(f"Aviso: hay {len(carpetas)} carpetas llamadas {nombre}; se usará {elegida['id']} sin borrar las demás.", flush=True)
        return elegida["id"]
    if carpetas:
        return carpetas[0]["id"]
    creada = servicio.files().create(body={"name": nombre, "mimeType": "application/vnd.google-apps.folder", "parents": [padre]}, fields="id").execute()
    return creada["id"]


def archivo_existe(servicio, nombre, carpeta):
    nombre_seguro = nombre.replace("'", "\\'")
    filtro = f"name = '{nombre_seguro}' and '{carpeta}' in parents and trashed = false"
    respuesta = servicio.files().list(q=filtro, fields="files(id)", pageSize=1).execute()
    return bool(respuesta.get("files"))


def descargar_bytes(url, tipo):
    solicitud = Request(url, headers={"User-Agent": "Proyecto2TransMilenio/1.0"})
    with urlopen(solicitud, timeout=20) as respuesta:
        contenido = respuesta.read()
        formato = respuesta.headers.get("Content-Type", "").lower()
    inicio = contenido[:100].lstrip().lower()
    if not contenido or any(x in formato for x in ("text/html", "application/json")) or inicio.startswith((b"<!doctype html", b"<html", b"{")):
        raise ValueError(f"{tipo}: respuesta vacía o página de mantenimiento, no datos.")
    if tipo == "gtfs":
        validar_gtfs_zip(contenido)
    if tipo != "gtfs" and not contenido.startswith(b"\x0a\x0d\x0a\x03"):
        raise ValueError(f"{tipo}: la respuesta no parece ser un feed GTFS-Realtime.")
    return contenido


def validar_gtfs_zip(contenido):
    """Evita subir un ZIP incompleto o sin las tablas básicas del proyecto."""
    tablas_necesarias = {"agency.txt", "routes.txt", "trips.txt", "stops.txt", "stop_times.txt"}
    try:
        with zipfile.ZipFile(io.BytesIO(contenido)) as archivo:
            faltantes = tablas_necesarias - set(archivo.namelist())
            if faltantes:
                raise ValueError("Al GTFS le faltan tablas: " + ", ".join(sorted(faltantes)))
            archivo_danado = archivo.testzip()
            if archivo_danado:
                raise ValueError("El GTFS contiene un archivo dañado: " + archivo_danado)
    except zipfile.BadZipFile as error:
        raise ValueError("El GTFS diario es un ZIP incompleto o dañado.") from error


def comprimir_pb(contenido):
    """Comprime sin pérdida una captura Protobuf antes de subirla a Drive."""
    return gzip.compress(contenido, compresslevel=6, mtime=0)


def subir_bytes(servicio, carpeta, nombre, contenido, fuente, instante, sha_original=None):
    from googleapiclient.http import MediaIoBaseUpload

    if archivo_existe(servicio, nombre, carpeta):
        print("Ya existe, se omite:", nombre, flush=True)
        return
    resumen = hashlib.sha256(contenido).hexdigest()
    descripcion = f"Fuente: {fuente}; captura: {instante.isoformat()}; bytes: {len(contenido)}; SHA-256: {resumen}"
    if sha_original:
        descripcion += f"; SHA-256 del PB original: {sha_original}"
    tipo_mime = "application/zip" if nombre.endswith(".zip") else "application/gzip"
    medio = MediaIoBaseUpload(io.BytesIO(contenido), mimetype=tipo_mime, resumable=True)
    creado = servicio.files().create(body={"name": nombre, "parents": [carpeta], "description": descripcion}, media_body=medio, fields="id,name,size").execute()
    if int(creado.get("size", -1)) != len(contenido):
        raise RuntimeError(f"El tamaño subido de {nombre} no coincide con el descargado.")
    print("Subido:", nombre, len(contenido), "bytes", flush=True)


def capturar_una_vez(servicio, configuracion, carpetas, suspendidas):
    for nombre in ("positions", "tripupdates", "alerts"):
        if time.monotonic() < suspendidas.get(nombre, 0):
            continue
        instante = datetime.now(ZONA)
        nombre_archivo = f"{nombre}_{instante.strftime('%Y%m%dT%H%M%S%z')}.pb.gz"
        try:
            contenido = descargar_bytes(configuracion["fuentes"][nombre], nombre)
            sha_original = hashlib.sha256(contenido).hexdigest()
            comprimido = comprimir_pb(contenido)
            subir_bytes(servicio, carpetas["tiempo_real"], nombre_archivo, comprimido,
                        configuracion["fuentes"][nombre], instante, sha_original)
        except (HTTPError, ValueError) as error:
            print(f"Fallo en {nombre}: {error}", flush=True)
            # Un mantenimiento o límite de solicitudes no se consulta cada 26 s.
            suspendidas[nombre] = time.monotonic() + 600
        except Exception as error:
            print(f"Fallo en {nombre}: {error}", flush=True)


def recolectar_dia(servicio, configuracion, franja_objetivo=None):
    hoy = datetime.now(ZONA).date()
    franjas_hoy = franjas_para_fecha(configuracion, hoy)
    if franja_objetivo and franja_objetivo not in franjas_hoy:
        raise ValueError(f"La franja {franja_objetivo} no está en la configuración.")
    cada = configuracion.get("cada_segundos", 26)
    if cada != 26:
        raise ValueError("Este proyecto acordó una captura cada 26 segundos.")
    if not fecha_permitida(configuracion, hoy):
        print("Hoy está fuera de las fechas autorizadas; no se capturará nada.", flush=True)
        return
    franjas_elegidas = [franja_objetivo] if franja_objetivo else franjas_hoy
    franjas_pendientes = []
    for franja in franjas_elegidas:
        _, hora_fin = separar_franja(franja)
        if datetime.now(ZONA) >= datetime.combine(hoy, hora_fin, tzinfo=ZONA):
            print("Franja pasada, se omite:", franja, flush=True)
        else:
            franjas_pendientes.append(franja)
    if not franjas_pendientes:
        return
    fecha = hoy.isoformat()
    carpeta_gtfs = buscar_o_crear_carpeta(servicio, "GTFS_diario", configuracion["carpeta_drive_id"])
    carpeta_rt = buscar_o_crear_carpeta(servicio, "capturas_tiempo_real", configuracion["carpeta_drive_id"])
    carpetas = {
        "gtfs": buscar_o_crear_carpeta(servicio, fecha, carpeta_gtfs),
        "tiempo_real": buscar_o_crear_carpeta(servicio, fecha, carpeta_rt),
    }

    suspendidas = {}
    for franja in franjas_pendientes:
        hora_inicio, hora_fin = separar_franja(franja)
        inicio = datetime.combine(hoy, hora_inicio, tzinfo=ZONA)
        fin = datetime.combine(hoy, hora_fin, tzinfo=ZONA)
        if datetime.now(ZONA) >= fin:
            print("Franja pasada mientras se preparaba, se omite:", franja, flush=True)
            continue
        espera = (inicio - datetime.now(ZONA)).total_seconds()
        if espera > 0:
            print("Esperando hasta", inicio.isoformat(), flush=True)
            time.sleep(espera)
        print("Iniciando franja", franja, flush=True)
        siguiente = time.monotonic()
        while datetime.now(ZONA) < fin:
            capturar_una_vez(servicio, configuracion, carpetas, suspendidas)
            siguiente += 26
            demora = siguiente - time.monotonic()
            if demora > 0:
                time.sleep(demora)
            else:
                print("Advertencia: una captura tardó más de 26 s; no se solapan solicitudes.", flush=True)
                siguiente = time.monotonic()

    # El ZIP grande se procesa después para no retrasar las posiciones en tiempo real.
    nombre_gtfs = f"GTFS_{hoy.strftime('%Y%m%d')}.zip"
    if not archivo_existe(servicio, nombre_gtfs, carpetas["gtfs"]):
        try:
            instante = datetime.now(ZONA)
            contenido = descargar_bytes(configuracion["fuentes"]["gtfs"], "gtfs")
            subir_bytes(servicio, carpetas["gtfs"], nombre_gtfs, contenido, configuracion["fuentes"]["gtfs"], instante)
        except Exception as error:
            print("Fallo en GTFS diario:", error, flush=True)


def leer_archivo_drive(servicio, id_archivo):
    """Devuelve un archivo de Drive en memoria, útil para analizarlo en VS Code."""
    return servicio.files().get_media(fileId=id_archivo).execute()


def impedir_suspension_mientras_captura():
    """En Windows, mantiene despierto el equipo solo durante esta ejecución."""
    if os.name != "nt":
        return None
    funcion = ctypes.WinDLL("kernel32", use_last_error=True).SetThreadExecutionState
    funcion.argtypes = [ctypes.c_uint]
    funcion.restype = ctypes.c_uint
    # ES_CONTINUOUS | ES_SYSTEM_REQUIRED: no cambia el plan de energía del PC.
    if funcion(0x80000001) == 0:
        raise OSError(ctypes.get_last_error(), "Windows no pudo impedir la suspensión")
    return funcion


def restaurar_suspension(funcion):
    """Retira la petición de mantener despierto el equipo al terminar."""
    if funcion is not None and funcion(0x80000000) == 0:
        print("Advertencia: Windows no confirmó la restauración de suspensión.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="JSON con franjas y URLs verificadas")
    parser.add_argument("--oauth-cliente", default=os.environ.get("GTFS_OAUTH_CLIENT"), help="Archivo OAuth fuera del repositorio")
    parser.add_argument("--autorizar", action="store_true", help="Permitir abrir Google para autorizar la primera vez")
    parser.add_argument("--solo-autorizar", action="store_true", help="Comprobar la cuenta de Drive sin descargar ni subir datos")
    parser.add_argument("--franja", help="Capturar solo una de las franjas de la configuración")
    args = parser.parse_args()
    configuracion = leer_configuracion(args.config)
    if not args.oauth_cliente:
        raise RuntimeError("Falta --oauth-cliente o GTFS_OAUTH_CLIENT. No guardes ese archivo en Git.")
    carpeta_privada = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Proyecto2TransMilenio"
    token = carpeta_privada / "drive_token.json"
    credenciales = credenciales_drive(args.oauth_cliente, token, autorizar=args.autorizar)
    servicio = servicio_drive(credenciales, configuracion["correo_esperado"])
    # Solo conservar el permiso después de comprobar la cuenta correcta.
    token.parent.mkdir(parents=True, exist_ok=True)
    token.write_text(credenciales.to_json(), encoding="utf-8")
    if args.solo_autorizar:
        print("Conexión verificada. No se capturaron ni subieron archivos.", flush=True)
        return
    solicitud_suspension = impedir_suspension_mientras_captura()
    try:
        recolectar_dia(servicio, configuracion, args.franja)
    finally:
        restaurar_suspension(solicitud_suspension)


if __name__ == "__main__":
    main()
