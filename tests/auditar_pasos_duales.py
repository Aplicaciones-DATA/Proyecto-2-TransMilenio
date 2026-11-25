"""Comprueba si los servicios duales explican la diferencia de pasos del 18/11.

No modifica fuentes ni resultados. Ejecutar con el Python del proyecto:
    python tests/auditar_pasos_duales.py
"""

from datetime import date, timedelta
from pathlib import Path
from sys import path
from zipfile import ZipFile

import pandas as pd


PROYECTO = Path(__file__).resolve().parent.parent
path.insert(0, str(PROYECTO / "src"))
from comparar_validaciones_gtfs import leer_estaciones, servicios_del_dia  # noqa: E402


DIA = date(2026, 11, 18)
GTFS = PROYECTO.parent / "registros_diarios" / DIA.isoformat() / "GTFS (1).zip"
PREVIO = PROYECTO / "datos" / "procesados" / "comparacion_estacion_hora_2026-11-18.csv"
ALEJANDRO = (
    PROYECTO.parent
    / "data_casi_lista"
    / "Comparacion_TransMilenio_2026-11-18_con_localidades.csv"
)


def contar_duales(archivo_gtfs):
    rutas = pd.read_csv(archivo_gtfs.open("routes.txt"), dtype=str)
    viajes = pd.read_csv(
        archivo_gtfs.open("trips.txt"),
        usecols=["trip_id", "route_id", "service_id"],
        dtype=str,
    )
    paradas = leer_estaciones(archivo_gtfs)
    estacion_por_parada = paradas.set_index("stop_id")["estacion_gtfs"]
    rutas_duales = set(rutas.loc[rutas["agency_id"] == "6", "route_id"])
    partes = []

    for fecha_servicio in [DIA - timedelta(days=1), DIA]:
        servicios = servicios_del_dia(archivo_gtfs, fecha_servicio)
        viajes_duales = set(
            viajes.loc[
                viajes["route_id"].isin(rutas_duales)
                & viajes["service_id"].isin(servicios),
                "trip_id",
            ]
        )
        with archivo_gtfs.open("stop_times.txt") as horarios:
            for bloque in pd.read_csv(
                horarios,
                usecols=["trip_id", "stop_id", "arrival_time"],
                dtype=str,
                chunksize=100000,
            ):
                bloque = bloque[bloque["trip_id"].isin(viajes_duales)].copy()
                if bloque.empty:
                    continue
                bloque["estacion_gtfs"] = bloque["stop_id"].map(estacion_por_parada)
                bloque = bloque.dropna(subset=["estacion_gtfs", "arrival_time"])
                hora_gtfs = pd.to_numeric(
                    bloque["arrival_time"].str.split(":").str[0], errors="coerce"
                )
                diferencia_dias = (DIA - fecha_servicio).days
                bloque = bloque[hora_gtfs // 24 == diferencia_dias].copy()
                if bloque.empty:
                    continue
                bloque["hora"] = (hora_gtfs.loc[bloque.index] % 24).astype(int)
                partes.append(
                    bloque.groupby(["hora", "estacion_gtfs"])
                    .size()
                    .reset_index(name="pasos_duales")
                )

    duales = pd.concat(partes, ignore_index=True)
    return duales.groupby(["hora", "estacion_gtfs"], as_index=False)[
        "pasos_duales"
    ].sum()


def main():
    previo = pd.read_csv(PREVIO, dtype={"estacion_gtfs": str})
    alejandro = pd.read_csv(ALEJANDRO, dtype={"estacion_gtfs": str})
    with ZipFile(GTFS) as gtfs:
        duales = contar_duales(gtfs)

    claves = ["fecha", "hora", "estacion_gtfs"]
    cotejo = previo[claves + ["pasos_programados"]].merge(
        alejandro[claves + ["pasos_programados"]],
        on=claves,
        suffixes=("_previo", "_alejandro"),
        validate="one_to_one",
    )
    cotejo = cotejo.merge(
        duales, on=["hora", "estacion_gtfs"], how="left", validate="many_to_one"
    )
    cotejo["prediccion_con_duales"] = (
        cotejo["pasos_programados_previo"].fillna(0)
        + cotejo["pasos_duales"].fillna(0)
    )
    ambos = cotejo["pasos_programados_alejandro"].notna()
    coincidencias = (
        cotejo.loc[ambos, "prediccion_con_duales"]
        == cotejo.loc[ambos, "pasos_programados_alejandro"]
    )
    print("Claves comparadas:", len(cotejo))
    print("Pasos duales totales en las claves:", int(cotejo["pasos_duales"].sum()))
    print("Filas de Alejandro con pasos:", int(ambos.sum()))
    print("Filas que coinciden al añadir duales:", int(coincidencias.sum()))
    print("Filas que aún no coinciden:", int((~coincidencias).sum()))
    print(
        cotejo.loc[ambos & cotejo["prediccion_con_duales"].ne(cotejo["pasos_programados_alejandro"]),
                   ["hora", "estacion_gtfs", "pasos_programados_previo", "pasos_duales", "pasos_programados_alejandro"]]
        .head(12)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
