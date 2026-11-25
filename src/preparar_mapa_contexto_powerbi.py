"""Prepara un punto por localidad para el mapa de contexto del tablero.

El punto se calcula con las coordenadas promedio de las estaciones troncales
observadas en cada localidad. No representa el domicilio de los encuestados.
La Encuesta Multipropósito de 2021 describe residentes, no pasajeros de 2026.
"""

from pathlib import Path

import pandas as pd


PROYECTO = Path(__file__).resolve().parent.parent
PROCESADOS = PROYECTO / "datos" / "procesados"
ESTACIONES = PROCESADOS / "powerbi_tabla_integrada_provisional.csv"
CONTEXTO = PROCESADOS / "powerbi_contexto_localidad_em2021.csv"
SALIDA = PROCESADOS / "powerbi_mapa_contexto_localidad.csv"


def main():
    datos = pd.read_csv(
        ESTACIONES,
        dtype={"estacion_gtfs": str, "codigo_localidad": str},
        decimal=",",
    )
    encuesta = pd.read_csv(CONTEXTO, dtype={"codigo_localidad": str}, decimal=",")

    # Cada estación cuenta una sola vez, aunque aparezca en muchos días y horas.
    estaciones = datos[
        ["estacion_gtfs", "codigo_localidad", "latitud", "longitud"]
    ].drop_duplicates()
    estaciones = estaciones.dropna(subset=["codigo_localidad", "latitud", "longitud"])
    if estaciones["estacion_gtfs"].duplicated().any():
        raise ValueError("Una estación aparece con distintas coordenadas o localidades.")

    puntos = estaciones.groupby("codigo_localidad", as_index=False).agg(
        latitud=("latitud", "mean"),
        longitud=("longitud", "mean"),
        estaciones_representadas=("estacion_gtfs", "count"),
    )
    mapa = puntos.merge(encuesta, on="codigo_localidad", how="left", validate="one_to_one")
    if mapa["localidad"].isna().any():
        raise ValueError("Falta contexto de encuesta para una localidad con estaciones.")
    if not mapa["latitud"].between(3.5, 5.0).all():
        raise ValueError("Hay latitudes fuera del área esperada para Bogotá.")
    if not mapa["longitud"].between(-75.0, -73.0).all():
        raise ValueError("Hay longitudes fuera del área esperada para Bogotá.")

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    mapa.to_csv(SALIDA, index=False, encoding="utf-8-sig", decimal=",")
    print("Localidades con estaciones y contexto:", len(mapa))
    print("Estaciones representadas:", int(mapa["estaciones_representadas"].sum()))
    print("Archivo:", SALIDA)


if __name__ == "__main__":
    main()
