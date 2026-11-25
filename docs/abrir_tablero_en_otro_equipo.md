# Abrir el borrador de Power BI en otro computador

Este es un **borrador local**, no una publicación ni la entrega del proyecto. Los cocientes de entradas por paso son provisionales hasta conciliar con Alejandro el conteo GTFS del 18 de noviembre. El periodo comparable del análisis principal es el **18–23 de noviembre de 2026**; el 24 no se incluyó porque aún no estaban publicadas sus validaciones oficiales al último chequeo.

## Archivos que acompañan al `.pbix`

El paquete local más reciente se llama `outputs/Paquete_tablero_*.zip`. Lo crea `python src/empaquetar_tablero.py` y reúne el tablero, las seis tablas derivadas que utiliza, esta guía, la auditoría de cobertura y el guion de presentación:

- `TransMilenio_borrador_2026-11-24.pbix`
- `powerbi_borrador_estacion_hora.csv`
- `powerbi_tabla_integrada_provisional.csv`
- `powerbi_contexto_localidad_em2021.csv`
- `powerbi_mapa_contexto_localidad.csv`
- `powerbi_relacion_localidad.csv`
- `powerbi_ranking_estaciones.csv`

Las seis tablas son agregadas o de contexto territorial; **no** se incluyen capturas `.pb`, ZIP originales ni credenciales. No compartir este paquete como versión definitiva sin revisar las cifras y la licencia/forma de entrega acordada.

## Pasos para Alejandro

1. Extrae el ZIP completo en una carpeta de tu PC, conservando sus subcarpetas `outputs/`, `datos/procesados/`, `docs/` y `reports/`. Abre `outputs/TransMilenio_borrador_2026-11-24.pbix` con Power BI Desktop. Deberías poder ver las ocho páginas guardadas sin actualizar.
2. Para recalcular desde los CSV, en Power BI Desktop entra a **Inicio → Transformar datos → Configuración de origen de datos**. Cambia cada ruta de archivo que apunte al PC de Emanuel por el CSV del mismo nombre en tu carpeta extraída. Los decimales de los CSV usan **coma**; si Power BI los reconoce como texto, configura el tipo numérico con la región **Español (Colombia)**. Luego pulsa **Actualizar**.
3. Comprueba que siguen apareciendo las ocho páginas, 151 estaciones en la tabla base y 132 estaciones en el ranking de seis días. Si alguna tabla no carga, revisa la ruta y no sustituyas un archivo por otro de nombre parecido.
4. Antes de usar una cifra en la sustentación, compara el denominador de pasos del 18/11 con la versión GTFS y la regla de conteo que utilizaste. El documento `docs/tablero_powerbi_2026-11-24.md` resume la discrepancia; `docs/auditoria_cobertura_estaciones_2026-11-24.md` explica las exclusiones del mapa y de la razón.

La prueba reproducible `tests/validar_tablas_powerbi.py` verifica claves y totales de las tablas derivadas si también clonas el repositorio y conservas los CSV en `datos/procesados/`.
