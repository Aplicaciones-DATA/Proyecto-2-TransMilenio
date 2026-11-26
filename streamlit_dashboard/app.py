from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


DATA = Path(__file__).resolve().parent / "data"
COUNTS = ["validaciones", "validaciones_comparables", "pasos_programados_comparables"]
PERIODS = ["Pico mañana", "Valle", "Pico tarde", "Otras horas"]
DAYS = ["entre semana", "fin de semana"]
COLORS = ["#126477", "#ad4a1e"]


def spanish(value, decimals=0):
    return f"{value:,.{decimals}f}".translate(str.maketrans(",.", ".,"))


@st.cache_data
def load_data():
    entries = pd.read_csv(
        DATA / "estacion_hora.csv",
        dtype={"estacion_gtfs": str, "codigo_localidad": str},
    )
    entries["franja"] = pd.cut(
        entries["hora"], bins=[-1, 5, 8, 15, 18, 23],
        labels=["Otras horas", *PERIODS[:3], "Otras horas"], ordered=False,
    )
    context = pd.read_csv(DATA / "contexto_localidades.csv", dtype={"codigo_localidad": str})
    return entries, context


def aggregate(data, by):
    table = data.groupby(by, as_index=False, observed=True)[COUNTS].sum()
    table["razon"] = table[COUNTS[1]].div(table[COUNTS[2]].where(table[COUNTS[2]].gt(0)))
    return table


def counts_line(data, column, label):
    return alt.Chart(data).mark_line(point=True).encode(
        x=alt.X("hora:Q", title="Hora de Bogotá", scale=alt.Scale(domain=[0, 23])),
        y=alt.Y(f"{column}:Q", title=label),
        color=alt.Color("tipo_dia:N", title="Tipo de día",
                        scale=alt.Scale(domain=DAYS, range=COLORS)),
        tooltip=["hora:Q", "tipo_dia:N", alt.Tooltip(f"{column}:Q", title=label, format=",.0f")],
    ).properties(height=240)


def main():
    st.set_page_config(page_title="Entradas y pasos de TransMilenio", layout="wide")
    st.title("Entradas y pasos programados de TransMilenio")
    st.caption("Bogotá · 19–23 de noviembre de 2026")
    base, context = load_data()

    date_choices = sorted(base["fecha"].unique())
    selected = st.sidebar.multiselect("Fechas", date_choices, default=date_choices)
    day = st.sidebar.selectbox("Tipo de día", ["Todos", *DAYS])
    data = base[base["fecha"].isin(selected)]
    if day != "Todos":
        data = data[data["tipo_dia"].eq(day)]
    if data.empty:
        st.info("Selecciona fechas que correspondan al tipo de día elegido.")
        return

    entries, paired, steps = data[COUNTS].sum()
    first, second, third = st.columns(3)
    first.metric("Entradas registradas", spanish(entries))
    second.metric("Entradas por paso", spanish(paired / steps, 2) if steps else "—")
    third.metric("Cobertura del cruce", f"{spanish(100 * paired / entries, 2)} %")
    st.caption(f"{spanish(paired)} entradas comparables y {spanish(steps)} pasos programados comparables.")

    hours, stations, territory = st.tabs(["Franjas y horas", "Estaciones", "Contexto territorial"])

    with hours:
        st.subheader("Entradas por paso según la franja")
        st.caption("Pico mañana 06:00–08:59 · Valle 09:00–15:59 · Pico tarde 16:00–18:59")
        ratios = aggregate(data, ["tipo_dia", "franja"])
        chart = alt.Chart(ratios).mark_bar().encode(
            x=alt.X("franja:N", title="Franja", sort=PERIODS),
            xOffset="tipo_dia:N",
            y=alt.Y("razon:Q", title="Entradas por paso"),
            color=alt.Color("tipo_dia:N", title="Tipo de día",
                            scale=alt.Scale(domain=DAYS, range=COLORS)),
            tooltip=["tipo_dia:N", "franja:N",
                     alt.Tooltip("razon:Q", title="Entradas por paso", format=".2f")],
        ).properties(height=295)
        st.altair_chart(chart)
        st.subheader("Promedio por día observado según la hora")
        day_counts = data.groupby("tipo_dia")["fecha"].nunique()
        hourly = aggregate(data, ["tipo_dia", "hora"])
        for column in COUNTS[1:]:
            hourly[column] = hourly[column].div(hourly["tipo_dia"].map(day_counts))
        left, right = st.columns(2)
        left.altair_chart(counts_line(hourly, COUNTS[1], "Entradas comparables"))
        right.altair_chart(counts_line(hourly, COUNTS[2], "Pasos programados comparables"))

    with stations:
        st.subheader("Estaciones con más entradas")
        top = aggregate(data, ["estacion_gtfs", "nombre_estacion_gtfs"]).nlargest(10, COUNTS[0])
        st.altair_chart(alt.Chart(top).mark_bar(color=COLORS[0]).encode(
            y=alt.Y("nombre_estacion_gtfs:N", sort="-x", title="Estación"),
            x=alt.X("validaciones:Q", title="Entradas registradas"),
            tooltip=[alt.Tooltip("nombre_estacion_gtfs:N", title="Estación"),
                     alt.Tooltip("validaciones:Q", title="Entradas", format=",.0f")],
        ).properties(height=320))
        st.subheader("Distribución espacial de las entradas")
        located = data.dropna(subset=["latitud", "longitud"])
        points = aggregate(located, ["estacion_gtfs", "nombre_estacion_gtfs", "latitud", "longitud"])
        st.caption(f"{located['estacion_gtfs'].nunique()} estaciones con coordenadas · "
                   f"{spanish(100 * located[COUNTS[0]].sum() / entries, 2)} % de las entradas.")
        st.altair_chart(alt.Chart(points).mark_circle(opacity=0.65, color=COLORS[0]).encode(
            x=alt.X("longitud:Q", title="Longitud", scale=alt.Scale(zero=False)),
            y=alt.Y("latitud:Q", title="Latitud", scale=alt.Scale(zero=False)),
            size=alt.Size("validaciones:Q", title="Entradas"),
            tooltip=[alt.Tooltip("nombre_estacion_gtfs:N", title="Estación"),
                     alt.Tooltip("validaciones:Q", title="Entradas", format=",.0f")],
        ).properties(height=360))

    with territory:
        st.subheader("Entradas por paso e ingresos insuficientes")
        regional = aggregate(data.dropna(subset=["codigo_localidad"]), ["codigo_localidad"])
        joined = regional.merge(context, on="codigo_localidad", validate="one_to_one")
        st.altair_chart(alt.Chart(joined).mark_circle(color=COLORS[1], size=115).encode(
            x=alt.X("ingresos_insuficientes_pct:Q", title="Hogares con ingresos insuficientes · EM 2021 (%)"),
            y=alt.Y("razon:Q", title="Entradas por paso programado"),
            tooltip=["localidad:N", alt.Tooltip("ingresos_insuficientes_pct:Q",
                      title="Ingresos insuficientes (%)", format=".2f"),
                     alt.Tooltip("razon:Q", title="Entradas por paso", format=".2f")],
        ).properties(height=390))
        st.caption("La encuesta describe hogares residentes en 2021. La operación corresponde a las estaciones ubicadas en cada localidad en 2026. La comparación es descriptiva.")

    with st.expander("Fuentes, definición y alcance"):
        st.markdown(
            "El indicador divide las **entradas comparables** entre los **pasos programados** "
            "de esas mismas filas. La llave del cruce es fecha, hora y estación, y requiere un paso positivo. "
            "La cobertura expresa qué proporción de las entradas cumple ese criterio. "
            "Los pasos representan la programación del GTFS. La ocupación y las llegadas reales "
            "requieren otras mediciones. El 18 de noviembre se excluyó por una discrepancia de conteo.\n\n"
            "Fuentes: validaciones de TransMilenio, horarios GTFS y Encuesta Multipropósito 2021. "
            "[Repositorio y método](https://github.com/Aplicaciones-DATA/Proyecto-2-TransMilenio)."
        )


if __name__ == "__main__":
    main()
