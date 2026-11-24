"""Genera los agregados de entradas, oferta programada y contexto territorial."""
import argparse
from datetime import date, timedelta
import json
import hashlib
from pathlib import Path
import re
import unicodedata
from zipfile import ZipFile

from matplotlib.path import Path as PolygonPath
from openpyxl import load_workbook
import pandas as pd

KEY = ["fecha", "hora", "codigo_estacion"]
DIAS = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")
WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


def codigo(values):
    return values.astype("string").str.strip().str.zfill(5)


def tipo_dia(day):
    if day.weekday() >= 5:
        return "Fin de semana"
    if day == date(2026, 11, 16):
        return "Festivo"
    return "Laborable"


def agrega_dia(frame):
    days = pd.to_datetime(frame["fecha"]).dt.date
    return frame.assign(dia_semana=days.map(lambda d: DIAS[d.weekday()]),
                        tipo_dia=days.map(tipo_dia))


def escribir(frame, path):
    frame.to_csv(path, index=False, encoding="utf-8-sig")


def fecha_del_archivo(path):
    return pd.to_datetime(re.search(r"(\d{8})$", path.stem).group(1), format="%Y%m%d").date()


def limpiar_entradas(paths):
    dates = {fecha_del_archivo(path).isoformat() for path in paths}
    parts, audits, aliases = [], [], []
    for path in paths:
        stats = dict(archivo=path.name, filas=0, fecha_invalida=0,
                     fuera_de_fechas=0, estacion_invalida=0, filas_validas=0)
        file_parts = []
        with ZipFile(path) as archive:
            members = [n for n in archive.namelist() if n.lower().endswith(".csv")]
            if len(members) != 1:
                raise ValueError(f"Se esperaba un CSV en {path.name}")
            with archive.open(members[0]) as source:
                for raw in pd.read_csv(source, chunksize=65_000, dtype=str, keep_default_na=False):
                    timestamp = pd.to_datetime(raw["Fecha_Transaccion"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
                    day = timestamp.dt.strftime("%Y-%m-%d")
                    label = raw["Estacion_Parada"].str.extract(r"^\s*\(([0-9]{1,5})\)\s*(\S.*?)\s*$")
                    eligible = day.isin(dates)
                    valid = eligible & label[0].notna()
                    stats["filas"] += len(raw)
                    stats["fecha_invalida"] += int(timestamp.isna().sum())
                    stats["fuera_de_fechas"] += int((timestamp.notna() & ~eligible).sum())
                    stats["estacion_invalida"] += int((eligible & ~valid).sum())
                    stats["filas_validas"] += int(valid.sum())
                    base = pd.DataFrame({"fecha": day[valid], "hora": timestamp[valid].dt.hour,
                                         "codigo_estacion": codigo(label.loc[valid, 0])})
                    file_parts.append(base.assign(huella=pd.util.hash_pandas_object(raw.loc[valid, sorted(raw.columns)], index=False)))
                    alias = base.assign(nombre=label.loc[valid, 1])
                    aliases.append(alias.groupby(["codigo_estacion","nombre"]).size().rename("filas"))
        block = pd.concat(file_parts, ignore_index=True)
        block["ocurrencia"] = block.groupby("huella", sort=False).cumcount()
        stats["repeticiones_identicas_dentro_del_zip_conservadas"] = int(block.ocurrencia.ne(0).sum())
        audits.append(stats)
        parts.append(block)
    combined = pd.concat(parts, ignore_index=True)
    clean = combined.drop_duplicates(["huella", "ocurrencia"])
    summary = clean.groupby(KEY, as_index=False).size().rename(columns={"size": "entradas_registradas"})
    names = pd.concat(aliases).groupby(level=[0,1]).sum().reset_index()
    most_common = names.sort_values(["filas","nombre"], ascending=[False,True]).drop_duplicates("codigo_estacion")
    summary = summary.merge(most_common[["codigo_estacion","nombre"]], on="codigo_estacion", validate="many_to_one")
    puntos_especiales = summary.nombre.str.contains(r"^(?:corral|bicicletero)\b", case=False)
    summary["tipo_punto"] = puntos_especiales.map({True: "Punto especial", False: "Estación o código por verificar"})
    audit = pd.DataFrame(audits)
    assert len(clean) == summary.entradas_registradas.sum()
    assert (audit.filas == audit[["fecha_invalida","fuera_de_fechas","estacion_invalida","filas_validas"]].sum(axis=1)).all()
    return agrega_dia(summary), audit, len(combined)-len(clean), names


def servicios_vigentes(day, calendar, exceptions):
    stamp = day.strftime("%Y%m%d")
    active = set(calendar.loc[(calendar[WEEKDAYS[day.weekday()]] == "1")
                 & (calendar.start_date <= stamp) & (calendar.end_date >= stamp), "service_id"])
    for row in exceptions.loc[exceptions.date == stamp].itertuples():
        if row.exception_type == "1":
            active.add(row.service_id)
        elif row.exception_type == "2":
            active.discard(row.service_id)
    return active


def limpiar_oferta(paths):
    parts, audits, station_lists = [], [], []
    for path in paths:
        service_day = fecha_del_archivo(path)
        with ZipFile(path) as archive:
            def read(name):
                with archive.open(name + ".txt") as source:
                    return pd.read_csv(source, dtype=str, keep_default_na=False)

            active = servicios_vigentes(service_day, read("calendar"), read("calendar_dates"))
            routes = set(read("routes").query('agency_id == "1"').route_id)
            all_trips = read("trips")
            trips = all_trips.loc[all_trips.route_id.isin(routes) & all_trips.service_id.isin(active)]
            assert trips.trip_id.is_unique
            assert set(trips.trip_id).isdisjoint(read("frequencies").trip_id), "Hay viajes troncales por frecuencia sin expandir"
            stops = read("stops")
            stations = stops.loc[stops.location_type.eq("1"), ["stop_id","stop_name"]].copy()
            stations["codigo_estacion"] = codigo(stations.stop_id)
            station_lists.append(stations.rename(columns={"stop_name":"nombre_gtfs"}))
            parent_mapping = stops.set_index("stop_id").parent_station.to_dict()
            station_id = stops.stop_id.map(lambda stop: parent_mapping[stop] or stop)
            regulation = set(stops.loc[stops.stop_name.str.contains("regulaci", case=False), "stop_id"])
            mapping = dict(zip(stops.stop_id, station_id.where(station_id.isin(stations.stop_id))))
            counts = dict(archivo=path.name, fecha_servicio=service_day.isoformat(),
                          viajes_troncales_activos=len(trips), candidatos=0, regulacion=0,
                          sin_estacion_padre=0, hora_invalida=0, filas_aptas=0)
            file_parts = []
            with archive.open("stop_times.txt") as source:
                for data in pd.read_csv(source, usecols=["trip_id","stop_id","stop_sequence","arrival_time"], chunksize=300_000, dtype=str, keep_default_na=False):
                    data = data.loc[data.trip_id.isin(trips.trip_id)].copy()
                    counts["candidatos"] += len(data)
                    excluded = data.stop_id.isin(regulation)
                    counts["regulacion"] += int(excluded.sum())
                    data = data.loc[~excluded].copy()
                    parent = data.stop_id.map(mapping)
                    counts["sin_estacion_padre"] += int(parent.isna().sum())
                    data = data.loc[parent.notna()].copy()
                    hours = pd.to_numeric(data.arrival_time.str.extract(r"^(\d{2,}):[0-5]\d:[0-5]\d$")[0])
                    counts["hora_invalida"] += int(hours.isna().sum())
                    valid = hours.notna()
                    counts["filas_aptas"] += int(valid.sum())
                    file_parts.append(data.loc[valid, ["trip_id","stop_sequence","arrival_time"]].assign(
                        codigo_estacion=codigo(parent[valid]), hora_servicio=hours[valid].astype(int)))
            frame = pd.concat(file_parts, ignore_index=True).drop_duplicates()
            if frame.duplicated(["trip_id", "stop_sequence"]).any():
                raise ValueError(f"Horarios contradictorios para un mismo viaje y secuencia en {path.name}")
            counts["duplicados_exactos"] = counts["filas_aptas"] - len(frame)
            counts["eventos_programados"] = len(frame)
            assert counts["candidatos"] == sum(counts[field] for field in ["regulacion","sin_estacion_padre","hora_invalida","filas_aptas"])
            audits.append(counts)
            frame["fecha"] = (pd.Timestamp(service_day) + pd.to_timedelta(frame.hora_servicio // 24, unit="D")).dt.strftime("%Y-%m-%d")
            frame["hora"] = frame.hora_servicio % 24
            frame["fecha_servicio"] = service_day.isoformat()
            parts.append(frame.groupby(KEY + ["fecha_servicio"], as_index=False).size().rename(columns={"size":"eventos"}))
            print("Oferta:", counts, flush=True)
    event_table = pd.concat(parts, ignore_index=True)
    covered = {fecha_del_archivo(path).isoformat() for path in paths}
    result = (event_table.groupby(KEY, as_index=False)
              .agg(paradas_programadas=("eventos","sum")))
    day = pd.to_datetime(result.fecha).dt.date
    result["cobertura_fecha_servicio"] = [
        "Se cuenta solo arrastre desde el día anterior" if d.isoformat() not in covered else
        "Sin GTFS del día anterior para verificar arrastre" if (d - timedelta(days=1)).isoformat() not in covered else
        "GTFS del día y del día anterior disponibles" for d in day]
    gtfs_stations = pd.concat(station_lists).drop_duplicates("codigo_estacion", keep="last")
    return agrega_dia(result), pd.DataFrame(audits), gtfs_stations


def normalizar(name):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower())


def territorio(folder, stations):
    shapes = json.loads((folder / "localidades_wgs.geojson").read_text())["features"]
    areas = []
    for feature in shapes:
        geometry = feature["geometry"]
        coords = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
        areas.append((feature["properties"], [[PolygonPath(ring) for ring in rings] for rings in coords]))
    wb = load_workbook(folder / "pobreza.xlsx", read_only=True, data_only=True)
    try:
        dane = {normalizar(row[0]): (round(row[1]), row[7]) for row in
                wb["Cuadro 216A"].iter_rows(min_row=17,max_row=35,values_only=True)}
    finally:
        wb.close()
    assert len(dane) == 19
    dane["candelaria"] = dane["lacandelaria"]
    official = json.loads((folder / "estaciones.geojson").read_text())["features"]
    records = []
    for feature in official:
        lon, lat = feature["geometry"]["coordinates"][:2]
        point = lon, lat
        assigned = [meta for meta, polygons in areas if any(polygon[0].contains_point(point)
                    and not any(hole.contains_point(point) for hole in polygon[1:]) for polygon in polygons)]
        meta = assigned[0] if len(assigned) == 1 else {}
        loc = meta.get("LOCNOMBRE")
        population, poverty = dane.get(normalizar(loc or ""), (None, None))
        props = feature["properties"]
        records.append({"codigo_estacion": str(props["num_est"]).zfill(5), "nombre_capa_oficial": props["nom_est"],
                        "longitud": lon, "latitud": lat, "codigo_localidad": meta.get("LOCCODIGO"),
                        "localidad": loc, "poblacion_urbana_estimada_2025": population,
                        "pobreza_monetaria_pct_2025": poverty,
                        "estado_territorio": ("Completo" if population is not None else
                                             "Límite ambiguo" if len(assigned)>1 else
                                             "Sin localidad asignada" if not assigned else "Sin indicador DANE")})
    context = stations.merge(pd.DataFrame(records), on="codigo_estacion", how="outer", validate="one_to_one")
    context["estado_territorio"] = context.estado_territorio.fillna("Código ausente en capa oficial")
    context["poblacion_urbana_estimada_2025"] = context.poblacion_urbana_estimada_2025.astype("Int64")
    return context.sort_values("codigo_estacion")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("validaciones","gtfs","territorio","salida"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    args.salida.mkdir(parents=True, exist_ok=True)
    validation_files = sorted(args.validaciones.glob("validacionTroncal*.zip"))
    gtfs_files = sorted(args.gtfs.glob("GTFS_*.zip"))
    if not validation_files or not gtfs_files:
        raise SystemExit("Se requieren ZIP de validaciones y GTFS. Consulte LEEME.md.")
    entries, validation_audit, duplicate_count, aliases = limpiar_entradas(validation_files)
    offer, gtfs_audit, gtfs_stations = limpiar_oferta(gtfs_files)
    stations = (entries[["codigo_estacion","nombre"]].drop_duplicates()
                .merge(gtfs_stations[["codigo_estacion","nombre_gtfs"]], on="codigo_estacion", how="outer", validate="one_to_one"))
    context = territorio(args.territorio, stations)
    dashboard = entries.loc[entries.tipo_punto.ne("Punto especial")].merge(
        context.drop(columns="nombre"), on="codigo_estacion", how="left", validate="many_to_one")
    covered = set(gtfs_audit.fecha_servicio)
    comparable = offer.loc[offer.fecha.isin(covered), KEY + ["paradas_programadas"]]
    dashboard = dashboard.merge(comparable, on=KEY, how="left", validate="one_to_one")
    dashboard["paradas_programadas"] = dashboard.paradas_programadas.astype("Int64")
    dashboard["entradas_por_parada_programada"] = dashboard.entradas_registradas / dashboard.paradas_programadas.where(dashboard.paradas_programadas.gt(0))
    dashboard["estado_oferta"] = dashboard.fecha.map(lambda d: "Sin GTFS de esa fecha" if d not in covered else "Sin coincidencia estación-hora")
    dashboard.loc[dashboard.paradas_programadas.notna(), "estado_oferta"] = "Oferta programada disponible"
    outputs = {
        "entradas_estacion_hora.csv": entries, "oferta_programada_estacion_hora.csv": offer,
        "estaciones_localidad_poblacion.csv": context, "base_dashboard.csv": dashboard,
        "auditoria_validaciones.csv": validation_audit, "auditoria_gtfs.csv": gtfs_audit,
        "variantes_nombres_validaciones.csv": aliases[aliases.duplicated("codigo_estacion", keep=False)]
    }
    inputs = [*validation_files, *gtfs_files, *(args.territorio / name for name in
              ("estaciones.geojson", "localidades_wgs.geojson", "pobreza.xlsx"))]
    inventory = []
    for path in inputs:
        with path.open("rb") as contents:
            digest = hashlib.file_digest(contents, "sha256").hexdigest()
        inventory.append({"archivo": path.name, "bytes": path.stat().st_size, "sha256": digest})
    outputs["inventario_insumos.csv"] = pd.DataFrame(inventory)
    outputs["auditoria_cruce_fecha.csv"] = pd.DataFrame([
        {"fecha": d, "validaciones": d in set(entries.fecha), "gtfs_de_fecha_servicio": d in covered,
         "pares_con_oferta": int((dashboard.fecha.eq(d) & dashboard.paradas_programadas.notna()).sum())}
        for d in sorted(set(entries.fecha) | covered)
    ])
    outputs["auditoria_faltantes_base.csv"] = pd.DataFrame({
        "columna": dashboard.columns, "faltantes": dashboard.isna().sum().to_numpy(),
        "porcentaje": (100 * dashboard.isna().mean()).round(2).to_numpy()
    })
    for name, frame in outputs.items():
        escribir(frame, args.salida / name)
    print("Duplicados idénticos entre ZIP retirados:", duplicate_count, flush=True)
    print("Validaciones por fecha:", entries.groupby("fecha").entradas_registradas.sum().to_dict(), flush=True)
    print("Entradas por estado territorial:", dashboard.groupby("estado_territorio").entradas_registradas.sum().to_dict(), flush=True)
    print("Validaciones en puntos especiales por fecha:", entries.loc[entries.tipo_punto.eq("Punto especial")].groupby("fecha").entradas_registradas.sum().to_dict(), flush=True)
    print("Pares estación-hora con oferta:", int(dashboard.paradas_programadas.notna().sum()), flush=True)
    print("Filas por archivo:", {name:len(frame) for name,frame in outputs.items()}, flush=True)


if __name__ == "__main__":
    main()
