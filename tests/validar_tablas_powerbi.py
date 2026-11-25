"""Comprueba las tablas que alimentan el borrador de Power BI.

No modifica datos. Ejecutar: python tests/validar_tablas_powerbi.py
"""

from pathlib import Path

import pandas as pd


PROYECTO = Path(__file__).resolve().parent.parent
PROCESADOS = PROYECTO / "datos" / "procesados"
TABLA = PROCESADOS / "powerbi_tabla_integrada_provisional.csv"
RANKING = PROCESADOS / "powerbi_ranking_estaciones.csv"
RELACION_LOCALIDAD = PROCESADOS / "powerbi_relacion_localidad.csv"
MAPA_LOCALIDAD = PROCESADOS / "powerbi_mapa_contexto_localidad.csv"
FECHAS_CON_GTFS = [
    "2026-11-16",
    "2026-11-18",
    "2026-11-19",
    "2026-11-20",
    "2026-11-21",
    "2026-11-22",
    "2026-11-23",
]


def main():
    datos = pd.read_csv(TABLA, decimal=",", dtype={"estacion_gtfs": str})
    claves = ["fecha", "hora", "estacion_gtfs"]

    assert not datos.duplicated(claves).any(), "Hay estación-hora duplicadas."
    assert datos["validaciones"].notna().all(), "Hay entradas sin conteo."
    assert datos["validaciones"].ge(0).all(), "Hay entradas negativas."
    assert datos.loc[datos["comparable"], "pasos_programados"].gt(0).all()
    assert datos["hora"].between(0, 23).all(), "Hay una hora fuera de rango."

    for fecha in FECHAS_CON_GTFS:
        origen = pd.read_csv(
            PROCESADOS / f"comparacion_estacion_hora_{fecha}.csv",
            dtype={"estacion_gtfs": str},
        )
        seleccionado = datos[datos["fecha"] == fecha]
        assert len(seleccionado) == len(origen), f"Cambió el número de filas {fecha}."
        assert seleccionado["validaciones"].sum() == origen["validaciones"].sum(), (
            f"Cambió el total de entradas {fecha}."
        )
        assert seleccionado["pasos_programados"].sum() == origen[
            "pasos_programados"
        ].sum(), f"Cambió el total de pasos {fecha}."

    sin_gtfs = datos[datos["fecha"].isin(["2026-11-14", "2026-11-15"])]
    assert sin_gtfs["pasos_programados"].isna().all()
    assert not sin_gtfs["comparable"].any()

    ranking = pd.read_csv(RANKING, decimal=",", dtype={"estacion_gtfs": str})
    assert not ranking["estacion_gtfs"].duplicated().any()
    assert ranking["validaciones_por_paso"].gt(0).all()

    relacion_localidad = pd.read_csv(
        RELACION_LOCALIDAD, decimal=",", dtype={"codigo_localidad": str}
    )
    mapa_localidad = pd.read_csv(
        MAPA_LOCALIDAD, decimal=",", dtype={"codigo_localidad": str}
    )
    assert not relacion_localidad["codigo_localidad"].duplicated().any()
    assert not mapa_localidad["codigo_localidad"].duplicated().any()
    assert set(mapa_localidad["codigo_localidad"]).issubset(
        set(relacion_localidad["codigo_localidad"])
    ), "El mapa contiene una localidad ajena a la tabla territorial."
    sin_denominador = relacion_localidad["pasos_programados"].isna()
    assert relacion_localidad.loc[sin_denominador, "validaciones_por_paso"].isna().all(), (
        "Se calculó una razón sin pasos programados."
    )

    comparables = datos[datos["comparable"]]
    print("FECHAS:", ", ".join(sorted(datos["fecha"].unique())))
    print("FILAS:", len(datos), "CLAVES ÚNICAS:", len(datos[claves].drop_duplicates()))
    print("ESTACIONES:", datos["estacion_gtfs"].nunique())
    print("ESTACIONES CON LOCALIDAD:", datos.loc[datos["localidad"].notna(), "estacion_gtfs"].nunique())
    print("FILAS CON COORDENADAS:", datos[["latitud", "longitud"]].notna().all(axis=1).sum())
    print("ENTRADAS TOTALES:", int(datos["validaciones"].sum()))
    print("ENTRADAS COMPARABLES:", int(comparables["validaciones"].sum()))
    print("PASOS COMPARABLES:", int(comparables["pasos_programados"].sum()))
    print("COBERTURA NUEVE FECHAS (%; 14/15 SIN GTFS):", round(100 * comparables["validaciones"].sum() / datos["validaciones"].sum(), 2))
    print("RANKING DE SEIS DÍAS:", len(ranking), "estaciones")
    print("LOCALIDADES EN TABLA TERRITORIAL:", len(relacion_localidad))
    print("LOCALIDADES CON COORDENADAS EN MAPA:", len(mapa_localidad))
    print("LOCALIDADES SIN RAZÓN:", int(sin_denominador.sum()))
    print("CONTROLES: CORRECTOS")

    periodo = datos[datos["fecha"].between("2026-11-18", "2026-11-23")]
    sin_paso = periodo[~periodo["comparable"]]
    print("\nCOBERTURA 18–23/11 (%):", round(100 * periodo.loc[periodo["comparable"], "validaciones"].sum() / periodo["validaciones"].sum(), 2))
    print("ENTRADAS SIN PASO COMPARABLE 18–23/11:", int(sin_paso["validaciones"].sum()))
    print("FILAS SIN PASO COMPARABLE 18–23/11:", len(sin_paso))

    comparables = comparables[comparables["fecha"].between("2026-11-18", "2026-11-23")]
    resumen = comparables.groupby(["tipo_dia", "franja"], as_index=False)[
        ["validaciones", "pasos_programados"]
    ].sum()
    resumen["entradas_por_paso"] = resumen["validaciones"] / resumen["pasos_programados"]
    print("\nRAZÓN 18–23/11, SOLO FILAS COMPARABLES:")
    print(resumen.to_string(index=False))


if __name__ == "__main__":
    main()
