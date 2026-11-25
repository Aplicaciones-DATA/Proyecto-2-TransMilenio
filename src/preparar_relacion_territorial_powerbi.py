"""Crea una tabla agregada para explorar demanda, oferta y contexto local.

La localidad indica dónde está la estación, no dónde vive quien validó.
La encuesta de 2021 describe residentes y no permite identificar pasajeros.
"""

from pathlib import Path

import pandas as pd


PROYECTO = Path(__file__).resolve().parent.parent
ENTRADAS = PROYECTO / "datos" / "procesados" / "powerbi_tabla_integrada_provisional.csv"
ENCUESTA = PROYECTO / "datos" / "procesados" / "powerbi_contexto_localidad_em2021.csv"
SALIDA = PROYECTO / "datos" / "procesados" / "powerbi_relacion_localidad.csv"


def main():
    datos = pd.read_csv(
        ENTRADAS,
        dtype={"estacion_gtfs": str, "codigo_localidad": str},
        decimal=",",
    )
    contexto = pd.read_csv(ENCUESTA, dtype={"codigo_localidad": str}, decimal=",")

    # Usar seis fechas consecutivas con validaciones y GTFS de cada día.
    datos = datos[datos["fecha"].between("2026-11-18", "2026-11-23")].copy()
    datos = datos[datos["codigo_localidad"].notna()].copy()
    if datos.duplicated(["fecha", "hora", "estacion_gtfs"]).any():
        raise ValueError("Hay más de una fila por estación, fecha y hora.")

    observadas = datos.groupby("codigo_localidad", as_index=False).agg(
        validaciones_observadas=("validaciones", "sum"),
        filas_observadas=("validaciones", "size"),
        estaciones=("estacion_gtfs", "nunique"),
        dias=("fecha", "nunique"),
    )
    observadas["validaciones_promedio_estacion_hora"] = (
        observadas["validaciones_observadas"] / observadas["filas_observadas"]
    )

    # Solo las filas con un paso programado válido forman el denominador.
    comparables = datos[datos["comparable"] & datos["pasos_programados"].gt(0)]
    comparables = comparables.groupby("codigo_localidad", as_index=False).agg(
        validaciones_comparables=("validaciones", "sum"),
        pasos_programados=("pasos_programados", "sum"),
        filas_comparables=("validaciones", "size"),
    )
    resumen = observadas.merge(comparables, on="codigo_localidad", how="left", validate="one_to_one")
    resumen["validaciones_por_paso"] = (
        resumen["validaciones_comparables"] / resumen["pasos_programados"]
    )
    resumen["cobertura_validaciones_pct"] = (
        100 * resumen["validaciones_comparables"] / resumen["validaciones_observadas"]
    )

    # Los indicadores sociales se mantienen como contexto de la localidad.
    columnas_encuesta = [
        "codigo_localidad", "localidad", "pobreza_monetaria_pct_residentes",
        "uso_tm_trabajo_pct_respondientes", "uso_tm_estudio_pct_respondientes",
        "encuestados_con_localidad", "respondieron_transmilenio_trabajo",
        "respondieron_transmilenio_estudio",
    ]
    resumen = resumen.merge(
        contexto[columnas_encuesta], on="codigo_localidad", how="left", validate="one_to_one",
    )
    if resumen["localidad"].isna().any():
        raise ValueError("Hay localidades sin contexto de la Encuesta Multipropósito.")
    if resumen["dias"].max() > 6:
        raise ValueError("El periodo del resumen no debe superar seis días.")

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    resumen.to_csv(SALIDA, index=False, encoding="utf-8-sig", decimal=",")
    print("Salida:", SALIDA)
    print("Localidades:", len(resumen))
    print("Estaciones con localidad:", datos["estacion_gtfs"].nunique())
    print("Días:", sorted(datos["fecha"].unique()))
    print("Validaciones observadas:", int(resumen["validaciones_observadas"].sum()))
    print("Cobertura total:", round(100 * resumen["validaciones_comparables"].sum() / resumen["validaciones_observadas"].sum(), 2), "%")


if __name__ == "__main__":
    main()
