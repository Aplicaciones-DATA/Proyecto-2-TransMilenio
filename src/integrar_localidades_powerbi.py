"""Añade localidades al borrador del tablero sin cambiar las medidas originales.

El archivo de Alejandro sirve aquí como tabla de correspondencia estación-localidad.
Sus pasos programados se auditan, pero no reemplazan los del cruce previo porque
los dos cálculos no coinciden. Los archivos de entrada se conservan intactos.
"""

from pathlib import Path

import pandas as pd


PROYECTO = Path(__file__).resolve().parent.parent
ORIGINAL = PROYECTO / "datos" / "procesados" / "powerbi_borrador_estacion_hora.csv"
ALEJANDRO = (
    PROYECTO.parent
    / "data_casi_lista"
    / "Comparacion_TransMilenio_2026-11-18_con_localidades.csv"
)
SALIDA = PROYECTO / "datos" / "procesados" / "powerbi_tabla_integrada_provisional.csv"


def preparar_correspondencia(datos_alejandro):
    columnas = ["estacion_gtfs", "codigo_localidad", "localidad", "estado_localidad"]
    correspondencia = datos_alejandro[columnas].drop_duplicates()
    if correspondencia["estacion_gtfs"].duplicated().any():
        raise ValueError("Una estación tiene más de una asignación de localidad.")
    return correspondencia


def revisar_pasos(datos_originales, datos_alejandro):
    """Cuenta discrepancias sobre las mismas claves, sin modificar ningún dato."""
    previo = datos_originales[datos_originales["fecha"] == "2026-11-18"]
    anterior = previo[["fecha", "hora", "estacion_gtfs", "pasos_programados"]]
    nuevo = datos_alejandro[["fecha", "hora", "estacion_gtfs", "pasos_programados"]]
    cotejo = anterior.merge(
        nuevo,
        on=["fecha", "hora", "estacion_gtfs"],
        how="outer",
        suffixes=("_previo", "_alejandro"),
        validate="one_to_one",
        indicator=True,
    )
    if not cotejo["_merge"].eq("both").all():
        raise ValueError("Las claves de estación-hora del 18 de noviembre no coinciden.")
    diferentes = (
        cotejo["pasos_programados_previo"].ne(cotejo["pasos_programados_alejandro"])
        & cotejo["pasos_programados_previo"].notna()
        & cotejo["pasos_programados_alejandro"].notna()
    )
    print("Pasos distintos entre las dos versiones:", int(diferentes.sum()))
    print("Pasos en versión previa:", int(cotejo["pasos_programados_previo"].sum()))
    print("Pasos en versión de Alejandro:", int(cotejo["pasos_programados_alejandro"].sum()))


def main():
    datos = pd.read_csv(ORIGINAL, dtype={"estacion_gtfs": str})
    alejandro = pd.read_csv(
        ALEJANDRO,
        dtype={"estacion_gtfs": str, "codigo_localidad": str},
    )
    if datos.duplicated(["fecha", "hora", "estacion_gtfs"]).any():
        raise ValueError("La tabla previa tiene claves repetidas.")
    if alejandro.duplicated(["fecha", "hora", "estacion_gtfs"]).any():
        raise ValueError("La tabla de Alejandro tiene claves repetidas.")

    revisar_pasos(datos, alejandro)
    correspondencia = preparar_correspondencia(alejandro)
    integrado = datos.merge(
        correspondencia,
        on="estacion_gtfs",
        how="left",
        validate="many_to_one",
        indicator=True,
    )
    if not integrado["_merge"].eq("both").all():
        raise ValueError("Quedaron estaciones sin correspondencia en el archivo de Alejandro.")
    integrado = integrado.drop(columns="_merge")
    if len(integrado) != len(datos):
        raise ValueError("La unión cambió el número de filas.")
    for columna in ["validaciones", "pasos_programados"]:
        if not integrado[columna].equals(datos[columna]):
            raise ValueError(f"La unión modificó la columna {columna}.")

    # Son conteos enteros. El tipo Int64 permite conservar los vacíos sin
    # exportar valores como "12.0", que Power BI puede leer como texto.
    integrado["pasos_programados"] = integrado["pasos_programados"].astype("Int64")
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    # Power BI en español interpreta la coma como separador decimal.
    # Pandas entrecomilla esos valores para conservar el CSV separado por comas.
    integrado.to_csv(SALIDA, index=False, encoding="utf-8-sig", decimal=",")
    print("Salida:", SALIDA)
    print("Filas conservadas:", len(integrado))
    print("Estaciones:", integrado["estacion_gtfs"].nunique())
    print("Estaciones con localidad:", integrado.loc[integrado["codigo_localidad"].notna(), "estacion_gtfs"].nunique())
    print("Estados:", integrado["estado_localidad"].value_counts().to_dict())


if __name__ == "__main__":
    main()
