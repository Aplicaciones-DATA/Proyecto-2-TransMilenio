"""Resume las estaciones comparables para un ranking provisional del tablero.

Una entrada es una validación registrada y un paso es una llegada programada
en GTFS. Su cociente no mide ocupación ni puntualidad real del servicio.
"""

from pathlib import Path

import pandas as pd


PROYECTO = Path(__file__).resolve().parent.parent
ENTRADA = PROYECTO / "datos" / "procesados" / "powerbi_tabla_integrada_provisional.csv"
SALIDA = PROYECTO / "datos" / "procesados" / "powerbi_ranking_estaciones.csv"


def main():
    datos = pd.read_csv(ENTRADA, dtype={"estacion_gtfs": str}, decimal=",")
    datos = datos[datos["fecha"].between("2026-11-18", "2026-11-23")].copy()
    if datos.duplicated(["fecha", "hora", "estacion_gtfs"]).any():
        raise ValueError("Hay claves estación-fecha-hora repetidas.")

    # Verificar que la correspondencia geográfica no cambie entre días.
    localidades = datos.groupby("estacion_gtfs")["codigo_localidad"].nunique()
    if localidades.gt(1).any():
        raise ValueError("Una estación aparece en más de una localidad.")

    observadas = datos.groupby("estacion_gtfs", as_index=False).agg(
        validaciones_observadas=("validaciones", "sum"),
    )
    comparables = datos[datos["comparable"] & datos["pasos_programados"].gt(0)]
    resumen = comparables.groupby("estacion_gtfs", as_index=False).agg(
        validaciones_comparables=("validaciones", "sum"),
        pasos_programados=("pasos_programados", "sum"),
        dias_comparables=("fecha", "nunique"),
    )
    resumen = resumen.merge(observadas, on="estacion_gtfs", validate="one_to_one")
    resumen["validaciones_por_paso"] = (
        resumen["validaciones_comparables"] / resumen["pasos_programados"]
    )
    resumen["cobertura_validaciones_pct"] = (
        100 * resumen["validaciones_comparables"] / resumen["validaciones_observadas"]
    )

    # Los nombres son etiquetas. La llave del cruce es el código GTFS.
    etiquetas = datos.sort_values("validaciones", ascending=False)
    etiquetas = etiquetas.drop_duplicates("estacion_gtfs")[
        ["estacion_gtfs", "nombre_estacion", "localidad"]
    ]
    resumen = resumen.merge(etiquetas, on="estacion_gtfs", validate="one_to_one")
    if not resumen["dias_comparables"].eq(6).all():
        raise ValueError("No todas las estaciones comparables cubren los seis días.")
    if resumen["validaciones_por_paso"].isna().any():
        raise ValueError("Hay razones vacías dentro de las estaciones comparables.")

    resumen = resumen.sort_values("validaciones_por_paso", ascending=False)
    resumen.insert(0, "puesto", range(1, len(resumen) + 1))
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    resumen.to_csv(SALIDA, index=False, encoding="utf-8-sig", decimal=",")
    print("Salida:", SALIDA)
    print("Estaciones comparables:", len(resumen))
    print("Cobertura total de validaciones:", round(
        100 * resumen["validaciones_comparables"].sum()
        / resumen["validaciones_observadas"].sum(), 2,
    ), "%")
    print(resumen.head(10)[
        ["puesto", "nombre_estacion", "validaciones_por_paso", "localidad"]
    ].to_string(index=False))


if __name__ == "__main__":
    main()
