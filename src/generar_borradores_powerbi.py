"""Genera figuras de revisión para construir después el tablero en Power BI.

Las figuras usan solo datos agregados del proyecto. No sustituyen un .pbix.
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import FuncFormatter, MaxNLocator
import pandas as pd


PROYECTO = Path(__file__).resolve().parent.parent
DATOS = PROYECTO / "datos" / "procesados" / "powerbi_borrador_estacion_hora.csv"
LOCALIDADES = PROYECTO.parent / "fuentes_compartidas" / "socioeconomicos" / "limites_localidades_bogota.json"
SALIDA = PROYECTO / "outputs" / "borradores_powerbi"

ETIQUETAS = {
    "2026-11-14": "Sábado 14",
    "2026-11-15": "Domingo 15",
    "2026-11-16": "Lunes 16 · servicio dominical",
    "2026-11-18": "Miércoles 18",
}
COLORES = {
    "2026-11-14": "#e69f00",
    "2026-11-15": "#d55e00",
    "2026-11-16": "#6c757d",
    "2026-11-18": "#0072b2",
}


def formato_miles(valor, _):
    return f"{valor:,.0f}".replace(",", ".")


def estilo_horario(eje):
    eje.set_xlim(3, 23)
    eje.set_xticks(range(3, 24, 2))
    eje.grid(axis="y", alpha=0.25)
    eje.yaxis.set_major_formatter(FuncFormatter(formato_miles))
    eje.axvspan(6, 9, color="#f2c94c", alpha=0.12)
    eje.axvspan(17, 20, color="#f2c94c", alpha=0.12)
    eje.set_xlabel("Hora de Bogotá")


def demanda_por_hora(datos):
    fig, eje = plt.subplots(figsize=(12, 5.6))
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.20, top=0.90)
    for fecha in ETIQUETAS:
        serie = datos[datos["fecha"] == fecha].groupby("hora")["validaciones"].sum()
        eje.plot(serie.index, serie.values, marker="o", markersize=3, linewidth=2,
                 color=COLORES[fecha], label=ETIQUETAS[fecha])
    estilo_horario(eje)
    eje.set_ylabel("Entradas registradas")
    eje.set_title("¿Cuándo se registraron más entradas? · Días disponibles")
    eje.legend(ncol=2, frameon=False)
    fig.text(0.08, 0.04,
             "Amarillo: franjas pico provisionales (06–08 y 17–19). El lunes 16 se separa porque el GTFS activa servicio dominical.",
             fontsize=9, color="#4b5563")
    fig.savefig(SALIDA / "01_entradas_por_hora.png", dpi=180)
    plt.close(fig)


def oferta_y_demanda(datos):
    comparables = datos[datos["comparable"]].copy()
    fig, ejes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.14, top=0.92, hspace=0.16)
    for fecha in ("2026-11-16", "2026-11-18"):
        por_hora = comparables[comparables["fecha"] == fecha].groupby("hora")[
            ["validaciones", "pasos_programados"]
        ].sum()
        ejes[0].plot(por_hora.index, por_hora["validaciones"], marker="o", markersize=3,
                     linewidth=2, color=COLORES[fecha], label=ETIQUETAS[fecha])
        ejes[1].plot(por_hora.index, por_hora["pasos_programados"], marker="o", markersize=3,
                     linewidth=2, color=COLORES[fecha], label=ETIQUETAS[fecha])
    for eje in ejes:
        estilo_horario(eje)
    ejes[0].set_xlabel("")
    ejes[0].set_ylabel("Entradas comparables")
    ejes[1].set_ylabel("Pasos programados comparables")
    ejes[0].set_title("Oferta y demanda por hora · Dos escalas separadas")
    ejes[0].legend(ncol=2, frameon=False)
    fig.text(0.09, 0.04,
             "Cada línea usa solo estación-hora con entrada y paso programado comparables. El GTFS del fin de semana sigue pendiente.",
             fontsize=9, color="#4b5563")
    fig.savefig(SALIDA / "02_oferta_y_demanda_por_hora.png", dpi=180)
    plt.close(fig)


def relacion_pico_valle(datos):
    comparables = datos[datos["comparable"] & datos["franja"].ne("Otras horas")]
    resumen = comparables.groupby(["fecha", "franja"])[["validaciones", "pasos_programados"]].sum()
    fig, eje = plt.subplots(figsize=(10, 5.4))
    fig.subplots_adjust(left=0.09, right=0.97, bottom=0.26, top=0.90)
    posiciones = [0, 1, 3, 4]
    fechas = ["2026-11-16", "2026-11-16", "2026-11-18", "2026-11-18"]
    franjas = ["Pico (provisional)", "Valle (provisional)"] * 2
    colores = ["#d55e00", "#0072b2"] * 2
    for posicion, fecha, franja, color in zip(posiciones, fechas, franjas, colores):
        fila = resumen.loc[(fecha, franja)]
        razon = fila["validaciones"] / fila["pasos_programados"]
        eje.bar(posicion, razon, width=0.8, color=color)
        eje.text(posicion, razon, f"{razon:.1f}", ha="center", va="bottom", fontsize=10)
    eje.set_xticks(posiciones, ["Pico", "Valle", "Pico", "Valle"])
    eje.set_ylabel("Entradas por paso programado")
    eje.set_title("Relación entre entradas y oferta programada · Pico frente a valle")
    eje.grid(axis="y", alpha=0.2)
    eje.set_axisbelow(True)
    fig.text(0.30, 0.14, "Lunes 16 · servicio dominical", ha="center", fontsize=10)
    fig.text(0.75, 0.14, "Miércoles 18", ha="center", fontsize=10)
    fig.text(0.09, 0.04,
             "Razón = suma de entradas / suma de pasos, solo filas comparables. Fin de semana: oferta aún sin emparejar.",
             fontsize=9, color="#4b5563")
    fig.savefig(SALIDA / "03_relacion_pico_valle.png", dpi=180)
    plt.close(fig)


def mapa_demanda(datos):
    con_ubicacion = datos.dropna(subset=["latitud", "longitud"]).copy()
    estaciones = con_ubicacion.groupby(
        ["estacion_gtfs", "nombre_estacion", "latitud", "longitud"], as_index=False
    )["validaciones"].sum()
    total = datos["validaciones"].sum()
    cobertura = 100 * con_ubicacion["validaciones"].sum() / total

    geometria = json.loads(LOCALIDADES.read_text(encoding="utf-8"))
    fig, eje = plt.subplots(figsize=(10, 7.2))
    fig.subplots_adjust(left=0.10, right=0.89, bottom=0.14, top=0.90)
    for localidad in geometria["features"]:
        for anillo in localidad["geometry"]["rings"]:
            xs, ys = zip(*anillo)
            eje.plot(xs, ys, color="#aeb8c2", linewidth=0.5, zorder=1)
    puntos = eje.scatter(
        estaciones["longitud"], estaciones["latitud"], c=estaciones["validaciones"],
        cmap="YlOrRd", norm=LogNorm(), s=23, edgecolors="#293241", linewidths=0.2, zorder=2,
    )
    barra = fig.colorbar(puntos, ax=eje, shrink=0.82)
    barra.set_label("Entradas registradas por estación · escala logarítmica")
    eje.set_aspect(1.0 / 0.9968)
    eje.set_xlim(-74.30, -73.97)
    eje.set_ylim(4.50, 4.85)
    eje.set_xlabel("Longitud")
    eje.set_ylabel("Latitud")
    eje.set_title("¿Dónde se concentran las entradas? · Área urbana con estaciones")
    fig.text(0.10, 0.04,
             f"Suma del 14, 15, 16 y 18 de noviembre. El mapa cubre {cobertura:.1f}% de las entradas; las demás no tienen coordenada vinculada.",
             fontsize=9, color="#4b5563")
    fig.savefig(SALIDA / "04_mapa_concentracion_entradas.png", dpi=180)
    plt.close(fig)


def estaciones_destacadas(datos):
    estaciones = datos.groupby(["estacion_gtfs", "nombre_estacion"], as_index=False)["validaciones"].sum()
    mayores = estaciones.nlargest(12, "validaciones").sort_values("validaciones")
    fig, eje = plt.subplots(figsize=(10, 6.2), layout="constrained")
    eje.barh(mayores["nombre_estacion"], mayores["validaciones"], color="#0072b2")
    eje.xaxis.set_major_formatter(FuncFormatter(formato_miles))
    eje.set_xlabel("Entradas registradas · cuatro días disponibles")
    eje.set_title("Estaciones con más entradas registradas")
    eje.grid(axis="x", alpha=0.2)
    eje.set_axisbelow(True)
    fig.savefig(SALIDA / "05_estaciones_destacadas.png", dpi=180)
    plt.close(fig)


def comparar_tipos_de_dia(datos):
    """Compara entradas por hora observada sin confundir días con cantidad de registros."""
    por_hora = datos.groupby(["fecha", "tipo_dia", "hora", "franja"], as_index=False)[
        "validaciones"
    ].sum()
    por_hora = por_hora[por_hora["franja"].ne("Otras horas")]
    promedio = por_hora.groupby(["tipo_dia", "franja"])["validaciones"].mean()
    tipos = ["Fin de semana", "Lunes con servicio dominical", "Día hábil"]
    etiquetas = ["Fin de semana\n(2 días)", "Lunes especial\n(1 día)", "Día hábil\n(1 día)"]
    colores = ["#e69f00", "#6c757d", "#0072b2"]
    franjas = ["Pico (provisional)", "Valle (provisional)"]
    fig, eje = plt.subplots(figsize=(10, 5.8))
    fig.subplots_adjust(left=0.10, right=0.97, bottom=0.25, top=0.90)
    for posicion, (tipo, etiqueta, color) in enumerate(zip(tipos, etiquetas, colores)):
        valores = [promedio.loc[(tipo, franja)] for franja in franjas]
        ubicaciones = [grupo + (posicion - 1) * 0.25 for grupo in (0, 1)]
        eje.bar(ubicaciones, valores, width=0.23, label=etiqueta, color=color)
    eje.set_xticks([0, 1], ["Pico", "Valle"])
    eje.set_ylabel("Entradas promedio por hora observada")
    eje.yaxis.set_major_formatter(FuncFormatter(formato_miles))
    eje.set_title("Demanda en pico y valle · Días disponibles")
    eje.legend(ncol=3, frameon=False, loc="upper right")
    eje.grid(axis="y", alpha=0.2)
    eje.set_axisbelow(True)
    fig.text(0.10, 0.04,
             "Promedio horario de cada grupo de días. No compara oferta: faltan GTFS emparejados de sábado y domingo.",
             fontsize=9, color="#4b5563")
    fig.savefig(SALIDA / "06_demanda_pico_valle_por_tipo_dia.png", dpi=180)
    plt.close(fig)


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    datos = pd.read_csv(DATOS, dtype={"estacion_gtfs": str})
    if datos.duplicated(["fecha", "hora", "estacion_gtfs"]).any():
        raise ValueError("La tabla de origen repite fecha-hora-estación.")
    demanda_por_hora(datos)
    oferta_y_demanda(datos)
    relacion_pico_valle(datos)
    mapa_demanda(datos)
    estaciones_destacadas(datos)
    comparar_tipos_de_dia(datos)
    for archivo in sorted(SALIDA.glob("*.png")):
        print(archivo.name, archivo.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
