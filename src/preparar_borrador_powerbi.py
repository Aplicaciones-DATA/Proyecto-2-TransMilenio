"""Prepara una tabla ligera para el primer borrador en Power BI.

Incluye entradas del 14 al 16 y del 18 al 23 de noviembre.
Del 18 al 23 y el 16 tienen GTFS comparable de su fecha; el 14 y 15 no.
El cruce del 18 proviene de la versión corregida por Alejandro; 19–23
coinciden con los cruces anteriores. No mezcla resultados de versiones.
No modifica los ZIP originales ni publica datos personales.
"""

from datetime import date
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from comparar_validaciones_gtfs import leer_validaciones


PROYECTO = Path(__file__).resolve().parent.parent
DIAS = PROYECTO.parent / "registros_diarios"
SALIDA = PROYECTO / "datos" / "procesados" / "powerbi_borrador_estacion_hora.csv"
FECHAS = [date(2026, 11, dia) for dia in (14, 15, 16, 18, 19, 20, 21, 22, 23)]
FECHAS_CON_SERVICIO_ESPECIAL = {date(2026, 11, 16)}
COMPARACION_CORREGIDA_18 = (
    PROYECTO.parent
    / "data_casi_lista"
    / "Comparacion_TransMilenio_2026-11-18_con_localidades.csv"
)


def cargar_entradas_sin_gtfs(dia):
    archivo = DIAS / dia.isoformat() / ("validacionTroncal" + dia.strftime("%Y%m%d") + ".zip")
    if not archivo.exists():
        raise FileNotFoundError(archivo)
    entradas = leer_validaciones(archivo, dia)
    # Una estación puede tener dos nombres; conservamos el de mayor frecuencia.
    nombres = entradas.sort_values("validaciones", ascending=False)
    nombres = nombres.drop_duplicates("estacion_gtfs")[["estacion_gtfs", "Estacion_Parada"]]
    entradas = entradas.groupby(["fecha", "hora", "estacion_gtfs"], dropna=False, as_index=False)["validaciones"].sum()
    entradas = entradas.merge(nombres, on="estacion_gtfs", how="left", validate="many_to_one")
    entradas["pasos_programados"] = pd.NA
    entradas["comparable"] = False
    entradas["estado_oferta"] = "GTFS del día pendiente"
    return entradas


def cargar_comparacion(dia):
    if dia == date(2026, 11, 18):
        archivo = COMPARACION_CORREGIDA_18
    else:
        archivo = PROYECTO / "datos" / "procesados" / ("comparacion_estacion_hora_" + dia.isoformat() + ".csv")
    if not archivo.exists():
        raise FileNotFoundError(archivo)
    datos = pd.read_csv(archivo, dtype={"estacion_gtfs": str})
    # Las coordenadas se agregan una sola vez desde los GTFS de todos los días.
    datos = datos.drop(columns=["latitud", "longitud"], errors="ignore")
    datos["comparable"] = datos["comparable"].astype(str).str.lower() == "true"
    datos["estado_oferta"] = "Comparable"
    datos.loc[~datos["comparable"], "estado_oferta"] = "Sin paso comparable"
    return datos


def cargar_coordenadas():
    archivos = [
        DIAS / "2026-11-16" / "GTFS_descargado_2026-11-16.zip",
        DIAS / "2026-11-18" / "GTFS (1).zip",
        DIAS / "2026-11-19" / "GTFS_20261119.zip",
        DIAS / "2026-11-20" / "GTFS_20261120.zip",
        DIAS / "2026-11-21" / "GTFS_20261121.zip",
        DIAS / "2026-11-22" / "GTFS_20261122.zip",
        DIAS / "2026-11-23" / "GTFS_20261123.zip",
    ]
    partes = []
    for archivo in archivos:
        with ZipFile(archivo) as gtfs:
            paradas = pd.read_csv(gtfs.open("stops.txt"), dtype={"stop_id": str, "location_type": str})
        estaciones = paradas[paradas["location_type"] == "1"].copy()
        estaciones["estacion_gtfs"] = estaciones["stop_id"].str.lstrip("0").replace("", "0")
        partes.append(estaciones[["estacion_gtfs", "stop_lat", "stop_lon"]])
    coordenadas = pd.concat(partes, ignore_index=True)
    coordenadas = coordenadas.drop_duplicates("estacion_gtfs")
    return coordenadas.rename(columns={"stop_lat": "latitud", "stop_lon": "longitud"})


def clasificar_franja(hora):
    # Misma regla provisional del análisis corregido de Alejandro.
    if 6 <= hora < 9 or 16 <= hora < 19:
        return "Pico (provisional)"
    if 9 <= hora < 16:
        return "Valle (provisional)"
    return "Otras horas"


def clasificar_tipo_dia(fecha):
    dia = date.fromisoformat(fecha)
    # El calendar_dates.txt del GTFS del 16 activa servicio dominical ese lunes.
    if dia in FECHAS_CON_SERVICIO_ESPECIAL:
        return "Lunes con servicio dominical"
    if dia.weekday() >= 5:
        return "Fin de semana"
    return "Día hábil"


def main():
    partes = []
    for dia in FECHAS:
        if dia == date(2026, 11, 18):
            comparacion = COMPARACION_CORREGIDA_18
        else:
            comparacion = PROYECTO / "datos" / "procesados" / (
                "comparacion_estacion_hora_" + dia.isoformat() + ".csv"
            )
        if not comparacion.exists():
            if dia in (date(2026, 11, 14), date(2026, 11, 15)):
                partes.append(cargar_entradas_sin_gtfs(dia))
            else:
                raise FileNotFoundError(comparacion)
        else:
            partes.append(cargar_comparacion(dia))

    datos = pd.concat(partes, ignore_index=True)
    datos["estacion_gtfs"] = datos["estacion_gtfs"].astype("string")
    datos["tipo_dia"] = datos["fecha"].apply(clasificar_tipo_dia)
    datos["franja"] = datos["hora"].apply(clasificar_franja)
    datos["nombre_estacion"] = datos["Estacion_Parada"].str.replace(r"^\s*\(\d+\)\s*", "", regex=True)
    datos = datos.merge(cargar_coordenadas(), on="estacion_gtfs", how="left", validate="many_to_one")
    columnas = [
        "fecha", "hora", "tipo_dia", "franja", "estacion_gtfs", "nombre_estacion",
        "validaciones", "pasos_programados", "comparable", "estado_oferta", "latitud", "longitud",
    ]
    datos = datos[columnas].sort_values(["fecha", "hora", "estacion_gtfs"])
    if datos.duplicated(["fecha", "hora", "estacion_gtfs"]).any():
        raise ValueError("Hay más de una fila por fecha, hora y estación.")
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    datos.to_csv(SALIDA, index=False, encoding="utf-8-sig")
    print("Archivo:", SALIDA)
    print("Filas:", len(datos))
    print("Fechas:", datos["fecha"].value_counts().sort_index().to_dict())
    print("Filas con coordenadas:", int(datos["latitud"].notna().sum()))
    print("Validaciones por tipo de día:", datos.groupby("tipo_dia")["validaciones"].sum().to_dict())
    print("Los días sin GTFS quedan sin pasos, nunca como cero.")


if __name__ == "__main__":
    main()
