# Auditoría de datos del tablero — 25 de noviembre de 2026

## Alcance y unidad de análisis

El tablero descriptivo compara **entradas registradas** con **pasos de bus programados** entre el **18 y el 23 de noviembre de 2026**. Cada fila de `datos/procesados/powerbi_tabla_integrada_provisional.csv` representa una combinación única de **fecha, hora y estación GTFS** que tiene validaciones. Un paso programado procede del horario GTFS; no confirma que el bus haya circulado ni llegado puntual. Una validación tampoco identifica a una persona única.

La tabla parte de las validaciones y les une el horario por fecha, hora y estación. Por eso el total de pasos que aparece aquí corresponde a las filas de validaciones con horario emparejado; **no es un censo de todos los pasos programados en la red**, incluidos lugares u horas sin una fila de validaciones. La razón `entradas por paso` se calcula como la suma de entradas de filas comparables dividida por la suma de pasos de esas mismas filas, no como el promedio de las razones por estación.

## Comprobaciones sobre los archivos actuales

Se ejecutó `tests/validar_tablas_powerbi.py` sin modificar los insumos. La prueba comparó la tabla integrada con los seis cruces diarios, los resúmenes de Alejandro y las tablas territoriales. Además, se hicieron lecturas de solo consulta para cuantificar las filas sin coordenadas o localidad y cotejar las dos versiones del 18.

| Comprobación | Resultado | Qué significa |
| --- | ---: | --- |
| Fechas incluidas | 18–23/11/2026 | Cuatro días hábiles y dos de fin de semana. |
| Filas y claves fecha–hora–estación | 17.503; 17.503 únicas | No hay duplicados en la unidad de análisis del tablero. |
| Estaciones identificadas | 151 | Universo de estaciones con una fila de validación en la tabla. |
| Entradas registradas | 9.205.097 | Total observado en esas filas; no personas únicas. |
| Entradas con paso comparable | 8.065.892 (87,62 % del total) | Coinciden en fecha, hora y estación con al menos un paso programado. |
| Entradas sin paso comparable | 1.139.205 (12,38 %) | No deben interpretarse como cero buses ni como falla del servicio. |
| Pasos programados en filas comparables | 1.312.035 | Denominador del indicador global; no incluye toda la programación de la red. |
| Entradas por paso comparable | 6,15 | Cociente de 8.065.892 / 1.312.035, redondeado a dos decimales. |

Las horas están entre 0 y 23 y no se encontraron entradas ni pasos negativos en la tabla revisada. La prueba automatizada terminó con `CONTROLES: CORRECTOS`, pero ese resultado verifica **coherencia entre archivos derivados**, no demuestra por sí solo que cada conteo se reproduzca desde el ZIP GTFS original.

## Cobertura espacial de los mapas

| Cobertura | Filas | Entradas | Proporción relevante |
| --- | ---: | ---: | ---: |
| Con coordenadas | 15.803 de 17.503 | 8.160.699 de 9.205.097 | 88,65 % de todas las entradas. |
| Con localidad asignada | 15.573 de 17.503 | 8.024.256 de 9.205.097 | 87,17 % de todas las entradas. |
| Comparables con localidad | — | 7.640.382 de 8.065.892 | 94,72 % de las entradas comparables. |

Hay **1.700 filas sin coordenadas** y **1.930 sin localidad**. De las 151 estaciones identificadas, 133 tienen localidad; las demás requieren consultar la [auditoría de correspondencia](auditoria_cobertura_estaciones_2026-11-24.md). Los mapas y la comparación territorial muestran solamente la parte georreferenciada o asignada: un punto ausente **no** representa demanda cero. La Encuesta Multipropósito describe residentes de cada localidad en 2021, no a los pasajeros que validaron en 2026.

## Discrepancia del 18 de noviembre

La tabla histórica `datos/procesados/comparacion_estacion_hora_2026-11-18.csv` y el archivo corregido de Alejandro `../data_casi_lista/Comparacion_TransMilenio_2026-11-18_con_localidades.csv` tienen **las mismas 2.931 claves** y **1.952.375 validaciones**, con **2.570 filas comparables**. Sin embargo, suman respectivamente **235.072** y **248.283** pasos programados: diferencia de **13.211** pasos. Hay **1.117 claves** con un conteo de pasos diferente. El SHA-256 del CSV corregido revisado es `45081570B0A645800638B8D3BE8B6491FB20037A6B6F0E004B2B43EDDD93DB0A`.

El código `src/preparar_borrador_powerbi.py` selecciona expresamente el CSV corregido de Alejandro para el 18; por eso el tablero y los resúmenes actuales usan **248.283**, no 235.072. La prueba `tests/comparar_versiones_gtfs_18.py` documenta que los GTFS diarios locales examinados no reproducen exactamente el conteo corregido. **Falta el ZIP GTFS exacto y/o la regla de conteo con que Alejandro obtuvo su CSV.** Hasta recibirlos, el resultado se puede cotejar entre archivos derivados, pero su procedencia no queda cerrada. No se debe sobrescribir ni borrar silenciosamente ninguna de las dos versiones.

## Dos contextos socioeconómicos distintos

`datos/analisis/contexto_localidades_em2021.csv`, integrado por Alejandro desde cuadros publicados de la Encuesta Multipropósito, tiene **19 localidades urbanas únicas**, sin nulos en sus columnas. Sus indicadores son ingresos insuficientes y viajes largos al trabajo o al estudio, con universos diferentes. En cambio, `datos/procesados/powerbi_contexto_localidad_em2021.csv` tiene **20 códigos únicos** y alimenta el mapa territorial del PBIX con pobreza monetaria y uso declarado de TransMilenio para trabajo o estudio. Ninguno de esos indicadores debe atribuirse al otro archivo: si se presentan ambos, cada visual necesita su nombre, fuente, año y denominador propios. No se infiere causalidad ni identidad de pasajeros a partir de esas asociaciones por localidad.

## Originales y fecha pendiente

`datos/raw/` contiene solo `.gitkeep` **a propósito**. Los ZIP diarios de validaciones y GTFS permanecen intactos fuera del repositorio público, en `../registros_diarios/AAAA-MM-DD/`, y las capturas de GTFS-Realtime se comparten por Drive. Esto evita cargar archivos voluminosos y publicar filas originales que contienen campos sensibles. El inventario de fechas, tamaños y huellas está en [registro_descargas.md](registro_descargas.md); [fuentes.md](fuentes.md) contiene los enlaces oficiales. La reproducción en otro equipo requiere obtener los originales autorizados, no asumir que están en GitHub.

Al revisar el [portal oficial de validaciones troncales](https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html) el 25/11, el ZIP más reciente listado era el del **23/11**. El 24 no se incorporó al indicador aunque exista su GTFS: para compararlo se necesitan las validaciones oficiales de esa misma fecha. Las posiciones GPS tampoco sustituyen las entradas registradas.

## Decisiones para cerrar el tablero

1. Mantener el periodo comparable 18–23/11 hasta que haya un nuevo par diario verificado de GTFS y validaciones.
2. Etiquetar en los mapas la cobertura espacial y conservar las ausencias como desconocidas, no como ceros.
3. Explicar en el tablero que la razón usa solo entradas y pasos de filas comparables.
4. Solicitar a Alejandro el ZIP GTFS, su SHA-256 y la regla que generó los 248.283 pasos del 18; registrar la reconciliación antes de presentar ese denominador como plenamente reproducible.
5. Elegir o distinguir explícitamente los dos conjuntos de indicadores socioeconómicos, sin mezclar sus denominadores ni describir a residentes como pasajeros.

Esta auditoría no modifica los ZIP originales, los CSV ni el archivo PBIX. Es una verificación de calidad para su uso descriptivo, no una conclusión sobre el desempeño real de TransMilenio.
