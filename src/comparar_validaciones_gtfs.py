"""Compara entradas registradas con pasos programados en la misma estación y hora.

Ejecutar desde cualquier carpeta:
    python src/comparar_validaciones_gtfs.py 2026-11-18

Por defecto usa los archivos del 18 de noviembre, guardados junto al repositorio.
No modifica los ZIP originales. Los resultados quedan en datos/procesados/.
"""

from datetime import date, timedelta
from pathlib import Path
from sys import argv
from zipfile import ZipFile

import pandas as pd


CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
FECHA = date(2026, 11, 18)
if __name__ == "__main__" and len(argv) > 1:
    FECHA = date.fromisoformat(argv[1])
CARPETA_DIA = CARPETA_PROYECTO.parent / "registros_diarios" / FECHA.isoformat()
ARCHIVO_VALIDACIONES = CARPETA_DIA / (
    "validacionTroncal" + FECHA.strftime("%Y%m%d") + ".zip"
)
CARPETA_SALIDA = CARPETA_PROYECTO / "datos" / "procesados"


def servicios_del_dia(archivo_gtfs, dia):
    """Busca el horario semanal y aplica las excepciones de la fecha."""
    numero_fecha = int(dia.strftime("%Y%m%d"))
    columna_dia = dia.strftime("%A").lower()

    calendario = pd.read_csv(archivo_gtfs.open("calendar.txt"))
    excepciones = pd.read_csv(archivo_gtfs.open("calendar_dates.txt"))

    regulares = calendario[
        (calendario["start_date"] <= numero_fecha)
        & (calendario["end_date"] >= numero_fecha)
        & (calendario[columna_dia] == 1)
    ]
    servicios = set(regulares["service_id"].astype(str))

    excepciones_dia = excepciones[excepciones["date"] == numero_fecha]
    for _, fila in excepciones_dia.iterrows():
        codigo = str(fila["service_id"])
        if fila["exception_type"] == 1:
            servicios.add(codigo)
        elif fila["exception_type"] == 2:
            servicios.discard(codigo)

    return servicios


def leer_validaciones(archivo_zip, dia):
    """Lee por bloques, sin cargar números de tarjeta ni saldos."""
    columnas = ["Fecha_Transaccion", "Estacion_Parada", "Sistema"]
    partes = []
    total_filas = 0
    filas_del_dia = 0

    for bloque in pd.read_csv(
        archivo_zip,
        compression="zip",
        encoding="utf-8",
        usecols=columnas,
        chunksize=100000,
    ):
        total_filas += len(bloque)
        bloque["Fecha_Transaccion"] = pd.to_datetime(
            bloque["Fecha_Transaccion"], errors="coerce"
        )
        bloque = bloque[
            (bloque["Sistema"] == "TRONCAL")
            & (bloque["Fecha_Transaccion"].dt.date == dia)
        ].copy()
        filas_del_dia += len(bloque)

        # El código entre paréntesis es más estable que el nombre de la estación.
        bloque["estacion_gtfs"] = (
            bloque["Estacion_Parada"]
            .str.extract(r"[(]([0-9]+)[)]")[0]
            .str.lstrip("0")
            .replace("", "0")
        )
        bloque["hora"] = bloque["Fecha_Transaccion"].dt.hour
        parte = bloque.groupby(
            ["hora", "estacion_gtfs", "Estacion_Parada"], dropna=False
        ).size().reset_index(name="validaciones")
        partes.append(parte)

    resumen = pd.concat(partes, ignore_index=True)
    resumen = resumen.groupby(
        ["hora", "estacion_gtfs", "Estacion_Parada"], dropna=False, as_index=False
    )["validaciones"].sum()
    resumen.insert(0, "fecha", dia.isoformat())
    print("Filas del ZIP:", total_filas)
    print("Validaciones troncales de la fecha:", filas_del_dia)
    return resumen


def leer_estaciones(archivo_gtfs):
    """Relaciona cada plataforma de GTFS con su estación principal."""
    paradas = pd.read_csv(
        archivo_gtfs.open("stops.txt"),
        dtype={"stop_id": str, "parent_station": str, "location_type": str},
    )
    paradas["estacion_gtfs"] = paradas["parent_station"]
    estaciones_principales = paradas["location_type"] == "1"
    paradas.loc[estaciones_principales, "estacion_gtfs"] = paradas["stop_id"]
    return paradas[["stop_id", "estacion_gtfs"]]


def viajes_troncales(archivo_gtfs, dia):
    """Selecciona solo los viajes de la agencia troncal activos ese día."""
    servicios = servicios_del_dia(archivo_gtfs, dia)
    rutas = pd.read_csv(
        archivo_gtfs.open("routes.txt"),
        dtype={"route_id": str, "agency_id": str},
    )
    viajes = pd.read_csv(
        archivo_gtfs.open("trips.txt"),
        usecols=["trip_id", "route_id", "service_id"],
        dtype={"trip_id": str, "route_id": str, "service_id": str},
    )
    rutas_troncales = set(rutas.loc[rutas["agency_id"] == "1", "route_id"])
    activos = viajes[
        viajes["route_id"].isin(rutas_troncales)
        & viajes["service_id"].isin(servicios)
    ]
    print(dia, "servicios activos:", sorted(servicios), "viajes troncales:", len(activos))
    return set(activos["trip_id"])


def leer_pasos_programados(archivo_gtfs, dia):
    """Cuenta llegadas programadas por estación y hora, leyendo por partes."""
    paradas = leer_estaciones(archivo_gtfs)
    codigos = paradas.set_index("stop_id")["estacion_gtfs"]
    partes = []

    # Un horario como 24:30 del día anterior corresponde a las 00:30 de hoy.
    for fecha_servicio in [dia - timedelta(days=1), dia]:
        viajes_activos = viajes_troncales(archivo_gtfs, fecha_servicio)
        with archivo_gtfs.open("stop_times.txt") as archivo_horarios:
            bloques = pd.read_csv(
                archivo_horarios,
                usecols=["trip_id", "stop_id", "arrival_time"],
                dtype={"trip_id": str, "stop_id": str, "arrival_time": str},
                chunksize=100000,
            )
            for bloque in bloques:
                bloque = bloque[bloque["trip_id"].isin(viajes_activos)].copy()
                if bloque.empty:
                    continue

                bloque["estacion_gtfs"] = bloque["stop_id"].map(codigos)
                bloque = bloque.dropna(subset=["estacion_gtfs", "arrival_time"])
                horas_gtfs = pd.to_numeric(
                    bloque["arrival_time"].str.split(":").str[0], errors="coerce"
                )
                dia_extra = horas_gtfs // 24
                bloque["hora"] = horas_gtfs % 24
                diferencia_dias = (dia - fecha_servicio).days
                bloque = bloque[dia_extra == diferencia_dias]
                if bloque.empty:
                    continue

                parte = bloque.groupby(["hora", "estacion_gtfs"]).size()
                partes.append(parte.reset_index(name="pasos_programados"))

    if not partes:
        raise ValueError("No se encontraron pasos programados para esta fecha.")
    resumen = pd.concat(partes, ignore_index=True)
    resumen = resumen.groupby(
        ["hora", "estacion_gtfs"], as_index=False
    )["pasos_programados"].sum()
    resumen["hora"] = resumen["hora"].astype(int)
    resumen.insert(0, "fecha", dia.isoformat())
    return resumen


def main():
    archivos_gtfs = list(CARPETA_DIA.glob("GTFS*.zip"))
    if len(archivos_gtfs) != 1 or not ARCHIVO_VALIDACIONES.exists():
        raise FileNotFoundError(
            "Debe haber un GTFS y el ZIP de validaciones de la misma fecha en "
            + str(CARPETA_DIA)
        )
    archivo_gtfs = archivos_gtfs[0]

    with ZipFile(archivo_gtfs) as gtfs:
        validaciones = leer_validaciones(ARCHIVO_VALIDACIONES, FECHA)
        pasos = leer_pasos_programados(gtfs, FECHA)
        estaciones = leer_estaciones(gtfs)
        estaciones_validas = set(estaciones["estacion_gtfs"].dropna())

    # Dos nombres distintos pueden compartir código de estación. Se suman antes
    # de unirlos con los pasos, para no contar dos veces el mismo denominador.
    etiquetas = validaciones.sort_values(
        "validaciones", ascending=False
    ).drop_duplicates("estacion_gtfs")[["estacion_gtfs", "Estacion_Parada"]]
    validaciones = validaciones.groupby(
        ["fecha", "hora", "estacion_gtfs"], dropna=False, as_index=False
    )["validaciones"].sum()
    validaciones = validaciones.merge(
        etiquetas, on="estacion_gtfs", how="left", validate="many_to_one"
    )

    validaciones["estacion_en_gtfs"] = validaciones["estacion_gtfs"].isin(
        estaciones_validas
    )
    comparacion = validaciones.merge(
        pasos, on=["fecha", "hora", "estacion_gtfs"], how="left", validate="many_to_one"
    )
    comparacion["comparable"] = (
        comparacion["estacion_en_gtfs"]
        & comparacion["pasos_programados"].gt(0)
    )
    comparacion["validaciones_por_paso"] = (
        comparacion["validaciones"] / comparacion["pasos_programados"]
    ).where(comparacion["comparable"])

    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)
    archivo_detalle = CARPETA_SALIDA / (
        "comparacion_estacion_hora_" + FECHA.isoformat() + ".csv"
    )
    archivo_resumen = CARPETA_SALIDA / (
        "resumen_comparacion_" + FECHA.isoformat() + ".csv"
    )
    comparacion.to_csv(archivo_detalle, index=False)

    resumen = comparacion[comparacion["comparable"]].groupby(
        ["fecha", "estacion_gtfs", "Estacion_Parada"], as_index=False
    )[["validaciones", "pasos_programados"]].sum()
    resumen["validaciones_por_paso"] = (
        resumen["validaciones"] / resumen["pasos_programados"]
    )
    resumen.to_csv(archivo_resumen, index=False)

    total = comparacion["validaciones"].sum()
    comparables = comparacion.loc[comparacion["comparable"], "validaciones"].sum()
    print("Filas estación-hora observadas:", len(comparacion))
    print("Filas comparables:", int(comparacion["comparable"].sum()))
    print("Validaciones comparables:", int(comparables), "de", int(total))
    print("Cobertura de validaciones:", round(100 * comparables / total, 2), "%")
    print("Estaciones comparables:", resumen["estacion_gtfs"].nunique())
    print("Detalle:", archivo_detalle)
    print("Resumen:", archivo_resumen)


if __name__ == "__main__":
    main()
