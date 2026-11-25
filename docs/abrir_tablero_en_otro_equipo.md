# Abrir el tablero actualizado de Power BI en otro computador

Esta es una **copia de trabajo posterior a la entrega oficial**, no una nueva entrega. El periodo comparable del análisis principal es el **19–23 de noviembre de 2026**. El 18 se excluyó por una discrepancia no conciliada en los pasos programados; el 24 no se incluyó porque sus validaciones oficiales no estaban disponibles al último chequeo.

## Archivos que acompañan al `.pbix`

El [paquete actualizado en Drive](https://drive.google.com/file/d/1JJ2RuE9qTF57AE5q8ZbDaqOlNWgkDA-o/view?usp=drivesdk) se llama `Paquete_tablero_20261125_023452.zip`. Reúne el tablero y las seis tablas derivadas que utiliza. Esta guía y el análisis de gráficos están en el repositorio de GitHub, no dentro del ZIP:

- `TransMilenio_19-23_noviembre_2026.pbix`
- `powerbi_borrador_estacion_hora.csv`
- `powerbi_tabla_integrada_provisional.csv`
- `powerbi_contexto_localidad_em2021.csv`
- `powerbi_mapa_contexto_localidad.csv`
- `powerbi_relacion_localidad.csv`
- `powerbi_ranking_estaciones.csv`

Las seis tablas son agregadas o de contexto territorial; **no** se incluyen capturas `.pb`, ZIP originales ni credenciales. No compartir este paquete como versión definitiva sin revisar las cifras y la licencia/forma de entrega acordada.

## Pasos para Alejandro

1. Extrae el ZIP completo en una carpeta de tu PC, conservando sus subcarpetas `outputs/` y `datos/procesados/`. Abre `outputs/TransMilenio_19-23_noviembre_2026.pbix` con Power BI Desktop. Deberías poder ver el tablero guardado sin actualizar.
2. Para recalcular desde los CSV, en Power BI Desktop entra a **Inicio → Transformar datos → Configuración de origen de datos**. Cambia cada ruta de archivo que apunte al PC de Emanuel por el CSV del mismo nombre en tu carpeta extraída. Los decimales de los CSV usan **coma**; si Power BI los reconoce como texto, configura el tipo numérico con la región **Español (Colombia)**. Luego pulsa **Actualizar**.
3. Comprueba que el corte sea **19–23/11**, que la razón principal muestre **5,97** y la cobertura **87,61 %**. Si alguna tabla no carga, revisa la ruta y no sustituyas un archivo por otro de nombre parecido.
4. Antes de usar una cifra en la sustentación, lee `docs/resultados.md` y `docs/analisis_graficos_19_23_2026.docx`. El indicador es entradas registradas por paso **programado**, no ocupación ni llegada efectiva de buses.

La prueba reproducible `tests/validar_tablas_powerbi.py` verifica claves y totales de las tablas derivadas si también clonas el repositorio y conservas los CSV en `datos/procesados/`.
