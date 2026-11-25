"""Prueba si la discrepancia del 18/11 depende de la versión GTFS usada.

Solo lee archivos originales y tablas derivadas; no modifica los resultados.
"""

from datetime import date
from pathlib import Path
from sys import path as rutas_python
from zipfile import ZipFile

import pandas as pd


PROYECTO = Path(__file__).resolve().parent.parent
rutas_python.insert(0, str(PROYECTO))
from src.comparar_validaciones_gtfs import leer_pasos_programados  # noqa: E402


DIA = date(2026, 11, 18)
REGISTROS = PROYECTO.parent / "registros_diarios"
ARCHIVO_ALEJANDRO = (
    PROYECTO.parent
    / "data_casi_lista"
    / "Comparacion_TransMilenio_2026-11-18_con_localidades.csv"
)


def comparar(gtfs_fecha, alejandro):
    archivos = list((REGISTROS / gtfs_fecha).glob("GTFS*.zip"))
    if len(archivos) != 1:
        raise FileNotFoundError("Se esperaba un único ZIP GTFS en " + gtfs_fecha)
    archivo = archivos[0]
    with ZipFile(archivo) as gtfs:
        calculado = leer_pasos_programados(gtfs, DIA)
    comparacion = alejandro.merge(
        calculado,
        on=["fecha", "hora", "estacion_gtfs"],
        how="left",
        suffixes=("_alejandro", "_calculado"),
        validate="one_to_one",
    )
    ambos = comparacion["pasos_programados_alejandro"].notna() & comparacion[
        "pasos_programados_calculado"
    ].notna()
    iguales = (
        comparacion.loc[ambos, "pasos_programados_alejandro"]
        == comparacion.loc[ambos, "pasos_programados_calculado"]
    )
    print(
        gtfs_fecha,
        "claves con ambos conteos:", int(ambos.sum()),
        "coincidencias:", int(iguales.sum()),
        "porcentaje:", round(100 * iguales.mean(), 2),
        "pasos calculados:", int(comparacion.loc[ambos, "pasos_programados_calculado"].sum()),
        "pasos Alejandro en esas claves:", int(comparacion.loc[ambos, "pasos_programados_alejandro"].sum()),
    )


def main():
    alejandro = pd.read_csv(
        ARCHIVO_ALEJANDRO,
        dtype={"estacion_gtfs": str},
        usecols=["fecha", "hora", "estacion_gtfs", "pasos_programados"],
    )
    for gtfs_fecha in [
        "2026-11-18",
        "2026-11-19",
        "2026-11-20",
        "2026-11-21",
        "2026-11-22",
        "2026-11-23",
    ]:
        comparar(gtfs_fecha, alejandro)


if __name__ == "__main__":
    main()
