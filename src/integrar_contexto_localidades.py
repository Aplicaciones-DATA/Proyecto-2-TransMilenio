"""Integra el cruce diario con localidades y resultados publicados de la EM 2021."""

from argparse import ArgumentParser
from pathlib import Path
from unicodedata import normalize
from zipfile import ZipFile
import json

from matplotlib.path import Path as PolygonPath
import numpy as np
from openpyxl import load_workbook
import pandas as pd


def clave_localidad(nombre):
    sin_tildes = normalize("NFKD", nombre.casefold()).encode("ascii", "ignore").decode()
    clave = "".join(c for c in sin_tildes if c.isalnum())
    return "candelaria" if clave == "lacandelaria" else clave


def cuadro_em(libro, hoja, fila_inicio, columna_universo, columna_pct, indicador):
    filas = list(libro[hoja].iter_rows(
        min_row=fila_inicio, max_row=fila_inicio + 18,
        max_col=columna_pct + 1, values_only=True,
    ))
    encabezado = [r for r in filas if isinstance(r[0], str) and r[0].strip()]
    if len(encabezado) != 19:
        raise ValueError(f"{hoja} debe contener 19 localidades urbanas.")
    tabla = pd.DataFrame([
        (clave_localidad(r[0]), r[columna_universo - 1], r[columna_pct - 1], r[columna_pct])
        for r in encabezado
    ], columns=["clave_localidad", f"{indicador}_universo_expandido", f"{indicador}_pct", f"{indicador}_cve_pct"])
    if tabla["clave_localidad"].duplicated().any() or not tabla[f"{indicador}_pct"].between(0, 100).all():
        raise ValueError(f"Revisar localidades o porcentajes en {hoja}.")
    return tabla


def contexto_encuesta(hogares, personas, catalogo):
    libro_hogares = load_workbook(hogares, read_only=True, data_only=True)
    libro_personas = load_workbook(personas, read_only=True, data_only=True)
    try:
        demografia = cuadro_em(libro_hogares, "Cuadro 211A", 16, 2, 9, "ingresos_insuficientes")
        trabajo = cuadro_em(libro_personas, "Cuadro 321A", 17, 2, 23, "trabajo_mas_de_60_min")
        estudio = cuadro_em(libro_personas, "Cuadro 312A", 17, 6, 27, "estudio_mas_de_40_min")
    finally:
        libro_hogares.close()
        libro_personas.close()
    salida = demografia.merge(trabajo, on="clave_localidad", validate="one_to_one")
    salida = salida.merge(estudio, on="clave_localidad", validate="one_to_one")
    salida = salida.merge(catalogo, on="clave_localidad", how="left", validate="one_to_one")
    if len(salida) != 19 or salida["codigo_localidad"].isna().any():
        raise ValueError("No coincidieron las 19 localidades urbanas con la capa oficial.")
    columnas = ["codigo_localidad", "localidad", "anio_encuesta"]
    salida = salida.assign(anio_encuesta=2021).drop(columns="clave_localidad")
    return salida[columnas + [col for col in salida if col not in columnas]].sort_values("codigo_localidad")


def dimension_estaciones(gtfs_path, features):
    with ZipFile(gtfs_path) as gtfs:
        estaciones = pd.read_csv(gtfs.open("stops.txt"), dtype={"stop_id": "string", "location_type": "string"})
    estaciones = estaciones.loc[estaciones["location_type"].eq("1"),
                                ["stop_id", "stop_name", "stop_lon", "stop_lat"]].copy()
    estaciones = estaciones.rename(columns={"stop_id": "estacion_gtfs", "stop_name": "nombre_estacion_gtfs",
                                          "stop_lon": "longitud", "stop_lat": "latitud"})
    if estaciones["estacion_gtfs"].duplicated().any():
        raise ValueError("El GTFS tiene códigos de estación repetidos.")
    puntos = estaciones[["longitud", "latitud"]].to_numpy()
    coincidencias = {}
    for feature in features:
        geometria = feature["geometry"]
        poligonos = [geometria["coordinates"]] if geometria["type"] == "Polygon" else geometria["coordinates"]
        dentro = np.zeros(len(puntos), dtype=bool)
        for exterior, *huecos in poligonos:
            cubre = PolygonPath(exterior).contains_points(puntos)
            for hueco in huecos:
                cubre &= ~PolygonPath(hueco).contains_points(puntos)
            dentro |= cubre
        coincidencias[feature["properties"]["LOCCODIGO"]] = dentro
    matr = pd.DataFrame(coincidencias, index=estaciones.index)
    n = matr.sum(axis=1)
    estaciones["codigo_localidad"] = matr.idxmax(axis=1).where(n.eq(1))
    estaciones["asignacion_localidad"] = np.select(
        [n.eq(1), n.gt(1)], ["asignada", "ambigua"], default="sin coincidencia en Bogotá"
    )
    return estaciones


def resumir(datos, niveles):
    tabla = datos.groupby(niveles, as_index=False, dropna=False).agg(
        filas=("comparable", "size"),
        filas_comparables=("comparable", "sum"),
        validaciones=("validaciones", "sum"),
        validaciones_comparables=("validaciones_comparables", "sum"),
        pasos_programados_comparables=("pasos_programados_comparables", "sum"),
    )
    tabla["cobertura_pct"] = 100 * tabla["validaciones_comparables"].div(tabla["validaciones"].where(tabla["validaciones"].gt(0)))
    tabla["validaciones_por_paso"] = tabla["validaciones_comparables"].div(
        tabla["pasos_programados_comparables"].where(tabla["pasos_programados_comparables"].gt(0))
    )
    return tabla


def main():
    parser = ArgumentParser(description=__doc__)
    for nombre in ["procesados", "gtfs", "localidades", "hogares", "personas", "salida"]:
        parser.add_argument(f"--{nombre}", type=Path, required=True)
    parser.add_argument("--pico", type=int, nargs="+", default=[6, 7, 8, 16, 17, 18])
    parser.add_argument("--valle", type=int, nargs="+", default=[9, 10, 11, 12, 13, 14, 15])
    args = parser.parse_args()
    if set(args.pico) & set(args.valle) or not set(args.pico + args.valle) <= set(range(24)):
        parser.error("Las horas de pico y valle deben ser disjuntas y estar entre 0 y 23.")
    rutas = sorted(args.procesados.glob("comparacion_estacion_hora_????-??-??.csv"))
    if not rutas:
        parser.error("Primero genere los cruces diarios en la carpeta de procesados.")
    datos = pd.concat([pd.read_csv(p, dtype={"estacion_gtfs": "string"}) for p in rutas], ignore_index=True)
    llave = ["fecha", "hora", "estacion_gtfs"]
    if datos.duplicated(llave).any():
        raise ValueError("Se repiten combinaciones de fecha, hora y estación.")
    datos["comparable"] = datos["comparable"].eq(True)
    if not (datos.loc[datos["comparable"], "pasos_programados"] > 0).all():
        raise ValueError("Hay filas comparables sin pasos programados positivos.")
    dias = pd.to_datetime(datos["fecha"]).dt.dayofweek
    datos["tipo_dia"] = np.where(dias.lt(5), "entre semana", "fin de semana")
    datos["franja"] = np.select(
        [datos["hora"].isin(args.pico), datos["hora"].isin(args.valle)],
        ["pico", "valle"], default="otras horas",
    )
    datos["validaciones_comparables"] = datos["validaciones"].where(datos["comparable"], 0)
    datos["pasos_programados_comparables"] = datos["pasos_programados"].where(datos["comparable"], 0).astype("int64")

    features = json.loads(args.localidades.read_text(encoding="utf-8"))["features"]
    catalogo = pd.DataFrame([
        (f["properties"]["LOCCODIGO"], f["properties"]["LOCNOMBRE"], clave_localidad(f["properties"]["LOCNOMBRE"]))
        for f in features
    ], columns=["codigo_localidad", "localidad", "clave_localidad"])
    dim = dimension_estaciones(args.gtfs, features)
    contexto = contexto_encuesta(args.hogares, args.personas, catalogo)
    base = datos.merge(dim, on="estacion_gtfs", how="left", validate="many_to_one")
    base = base.merge(catalogo.drop(columns="clave_localidad"), on="codigo_localidad", how="left", validate="many_to_one")
    base["asignacion_localidad"] = base["asignacion_localidad"].fillna("sin código de estación en GTFS")
    if len(base) != len(datos) or base["validaciones"].sum() != datos["validaciones"].sum():
        raise ValueError("El cruce territorial alteró el número de filas o validaciones.")
    territorial = resumir(base, ["codigo_localidad", "localidad"])
    territorial = territorial.merge(contexto.drop(columns="localidad"), on="codigo_localidad", how="left", validate="one_to_one")
    if territorial["validaciones_comparables"].sum() != base["validaciones_comparables"].sum():
        raise ValueError("La suma territorial no coincide con la base.")

    args.salida.mkdir(parents=True, exist_ok=True)
    salidas = {
        "estacion_hora_localidad.csv": base,
        "contexto_localidades_em2021.csv": contexto,
        "resumen_localidad.csv": territorial,
        "resumen_franjas.csv": resumir(base, ["tipo_dia", "franja"]),
        "cobertura_diaria.csv": resumir(base, ["fecha"]),
        "resumen_estacion_franja.csv": resumir(
            base.loc[base["comparable"]], ["estacion_gtfs", "nombre_estacion_gtfs", "codigo_localidad", "localidad", "tipo_dia", "franja"]),
    }
    for nombre, contenido in salidas.items():
        contenido.to_csv(args.salida / nombre, index=False, encoding="utf-8-sig", float_format="%.6f")
    print(f"Filas preservadas: {len(base)}. Localidades con EM: {len(contexto)}.")
    print(f"Estaciones comparables con localidad: {base.loc[base.comparable & base.codigo_localidad.notna(), 'estacion_gtfs'].nunique()}"
          f" de {base.loc[base.comparable, 'estacion_gtfs'].nunique()}.")


if __name__ == "__main__":
    main()
