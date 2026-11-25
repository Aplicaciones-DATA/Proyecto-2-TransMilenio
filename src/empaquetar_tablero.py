"""Prepara un ZIP local para abrir el borrador de Power BI en otro equipo.

Uso: python src/empaquetar_tablero.py
No sube nada a Internet ni incluye datos crudos o credenciales.
"""

from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


PROYECTO = Path(__file__).resolve().parent.parent
ARCHIVOS = [
    "outputs/TransMilenio_borrador_2026-11-24.pbix",
    "datos/procesados/powerbi_borrador_estacion_hora.csv",
    "datos/procesados/powerbi_tabla_integrada_provisional.csv",
    "datos/procesados/powerbi_contexto_localidad_em2021.csv",
    "datos/procesados/powerbi_mapa_contexto_localidad.csv",
    "datos/procesados/powerbi_relacion_localidad.csv",
    "datos/procesados/powerbi_ranking_estaciones.csv",
    "docs/abrir_tablero_en_otro_equipo.md",
    "docs/tablero_powerbi_2026-11-24.md",
    "docs/auditoria_cobertura_estaciones_2026-11-24.md",
    "reports/guion_presentacion_2026-11-24.md",
    "reports/conclusiones_provisionales_2026-11-24.md",
]


def main():
    for nombre in ARCHIVOS:
        if not (PROYECTO / nombre).is_file():
            raise FileNotFoundError(f"Falta el archivo: {nombre}")

    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    salida = PROYECTO / "outputs" / f"Paquete_tablero_{fecha}.zip"
    with ZipFile(salida, "x", ZIP_DEFLATED) as paquete:
        for nombre in ARCHIVOS:
            paquete.write(PROYECTO / nombre, arcname=nombre)

    with ZipFile(salida) as paquete:
        if paquete.testzip() is not None:
            raise ValueError("El ZIP no pasó la prueba de integridad.")
        if paquete.namelist() != ARCHIVOS:
            raise ValueError("El contenido del ZIP no coincide con la lista aprobada.")

    print(f"Paquete local creado: {salida}")
    print(f"Archivos incluidos: {len(ARCHIVOS)}")
    print(f"Tamaño: {salida.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
