"""Resume la Encuesta Multipropósito 2021 por localidad para Power BI.

La encuesta describe residentes, no a quienes ingresaron en una estación.
Solo se exportan resultados agregados; los registros personales permanecen
en la fuente local y no se copian al repositorio ni al tablero.
"""

from pathlib import Path

import pandas as pd


PROYECTO = Path(__file__).resolve().parent.parent
FUENTES = PROYECTO.parent / "fuentes_compartidas" / "socioeconomicos"
SALIDA = PROYECTO / "datos" / "procesados" / "powerbi_contexto_localidad_em2021.csv"


def porcentaje_ponderado(grupo, variable, respuesta_si, respuesta_no):
    # El denominador incluye solo a quienes contestaron sí o no esa pregunta.
    respondieron = grupo[variable].isin([respuesta_si, respuesta_no])
    peso_total = grupo.loc[respondieron, "FEX_C"].sum()
    if peso_total <= 0:
        return None, 0
    peso_si = grupo.loc[grupo[variable] == respuesta_si, "FEX_C"].sum()
    return round(100 * peso_si / peso_total, 2), int(respondieron.sum())


def main():
    encuesta = pd.read_csv(
        FUENTES / "em2021.csv",
        encoding="latin1",
        usecols=[
            "DIRECTORIO_PER", "COD_LOCALIDAD", "NOMBRE_LOCALIDAD", "FEX_C",
            "NPCKP45A", "NPCHP18AA",
        ],
        low_memory=False,
    )
    adicionales = pd.read_csv(
        FUENTES / "variables_adicionales_em2021.csv",
        usecols=["directorio_per", "N_pobre_monetario"],
    )
    if encuesta["DIRECTORIO_PER"].duplicated().any():
        raise ValueError("La encuesta tiene identificadores de persona repetidos.")
    if adicionales["directorio_per"].duplicated().any():
        raise ValueError("Las variables adicionales tienen identificadores repetidos.")

    personas = encuesta.merge(
        adicionales,
        left_on="DIRECTORIO_PER",
        right_on="directorio_per",
        how="left",
        validate="one_to_one",
        indicator=True,
    )
    if not personas["_merge"].eq("both").all():
        raise ValueError("La variable adicional no cubre todas las personas de la encuesta.")
    personas = personas[personas["COD_LOCALIDAD"].notna() & personas["FEX_C"].gt(0)].copy()
    personas["codigo_localidad"] = personas["COD_LOCALIDAD"].astype(int).astype(str).str.zfill(2)

    filas = []
    for codigo, grupo in personas.groupby("codigo_localidad"):
        nombres = grupo["NOMBRE_LOCALIDAD"].dropna().unique()
        if len(nombres) != 1:
            raise ValueError(f"Nombres de localidad ambiguos para {codigo}.")
        trabajo, n_trabajo = porcentaje_ponderado(grupo, "NPCKP45A", 1, 2)
        estudio, n_estudio = porcentaje_ponderado(grupo, "NPCHP18AA", 1, 2)
        pobreza, n_pobreza = porcentaje_ponderado(grupo, "N_pobre_monetario", 1, 0)
        filas.append({
            "codigo_localidad": codigo,
            "localidad": nombres[0],
            "encuestados_con_localidad": len(grupo),
            "respondieron_transmilenio_trabajo": n_trabajo,
            "uso_tm_trabajo_pct_respondientes": trabajo,
            "respondieron_transmilenio_estudio": n_estudio,
            "uso_tm_estudio_pct_respondientes": estudio,
            "con_dato_pobreza_monetaria": n_pobreza,
            "pobreza_monetaria_pct_residentes": pobreza,
        })

    contexto = pd.DataFrame(filas).sort_values("codigo_localidad")
    if contexto["codigo_localidad"].duplicated().any():
        raise ValueError("La salida tiene una localidad duplicada.")
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    # Evita que Power BI en español confunda los decimales con miles.
    contexto.to_csv(SALIDA, index=False, encoding="utf-8-sig", decimal=",")
    print("Salida:", SALIDA)
    print("Localidades:", len(contexto))
    print("Personas con localidad y factor válido:", len(personas))
    print("Mínimo de respuestas a trabajo:", contexto["respondieron_transmilenio_trabajo"].min())
    print("Mínimo de respuestas a estudio:", contexto["respondieron_transmilenio_estudio"].min())
    print(contexto[["codigo_localidad", "localidad", "encuestados_con_localidad"]].to_string(index=False))


if __name__ == "__main__":
    main()
