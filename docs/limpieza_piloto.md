# Limpieza y análisis exploratorio del piloto

Esta bitácora sigue el orden de las sesiones de DATA-1002 sobre estructura tabular, procesamiento, calidad, EDA y reproducibilidad. Los ZIP originales se conservan intactos.

| Paso | Decisión y control |
|---|---|
| Comprender | Una fila de validaciones crudas es un acceso registrado. Una fila de horarios por parada es un evento programado de un viaje en una parada. Una fila del resultado representa fecha civil, hora y estación. |
| Diagnosticar | Se verifican el tamaño, las columnas, los tipos, los faltantes y las repeticiones. El notebook muestra los controles y las auditorías registran la cantidad de filas afectadas. |
| Seleccionar y filtrar | Se agrupan validaciones por fecha de transacción. Se excluyen de la base principal los tres códigos denominados Corral o Bicicletero. La copia de control los conserva. En los horarios se filtran viajes troncales vigentes para cada fecha de servicio. |
| Transformar | Se conservan los códigos como texto de cinco dígitos y se normaliza el identificador de estación. Los horarios de plataformas se asignan a su estación principal. Las horas GTFS desde 24:00 se trasladan al día civil correspondiente. |
| Duplicados y faltantes | Se distingue entre validaciones repetidas y duplicados idénticos detectables entre ZIP. Los faltantes de localidad, oferta o indicador se conservan y se auditan. Se evita imputar oferta con cero. |
| Integrar y validar | Validaciones y catálogo se unen por código. La localidad se asigna por ubicación y se enlaza al cuadro del DANE por nombre normalizado. Se comprueba cardinalidad muchos a uno, totales y unicidad por fecha, hora y estación. |
| Explorar | Se revisan la distribución por hora, el ranking de estaciones y el volumen por localidad. Las localidades solo incluyen estaciones con ubicación asignada. Los picos se conservan como observaciones. |

## Archivos y procedencia

| Insumo local | Fuente y unidad |
|---|---|
| `datos/raw/validaciones/validacionTroncalAAAAMMDD.zip` | [Validaciones troncales](https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html). Una fila por validación de acceso. Disponibles para este cálculo: 15 y 16 de noviembre. |
| `datos/raw/gtfs/GTFS_AAAAMMDD.zip` | [GTFS diario](https://gtfs.transmilenio.gov.co/). Se usan los ZIP internos de las fechas 18–23. Cada uno aporta el calendario, los viajes, las estaciones y los horarios programados. |
| `datos/raw/territorio/estaciones.geojson` | [Catálogo oficial de estaciones](https://datosabiertos.bogota.gov.co/dataset/estaciones-troncales-de-transmilenio1). Una ubicación y código por punto de la capa. [Descarga GeoJSON](https://datosabiertos-transmilenio.hub.arcgis.com/api/download/v1/items/5365d814bbdd4062a59234eea7d70db7/geojson?layers=2). |
| `datos/raw/territorio/localidades_wgs.geojson` | [Límites de localidades](https://datosabiertos.bogota.gov.co/dataset/localidad-bogota-d-c). [Consulta oficial en EPSG:4326](https://serviciosgis.catastrobogota.gov.co/arcgis/rest/services/ordenamientoterritorial/localidad/MapServer/0/query?where=1%3D1&outFields=LocNombre%2CLocCodigo&outSR=4326&f=geojson). |
| `datos/raw/territorio/pobreza.xlsx` | [Encuesta Multipropósito 2025, anexo de pobreza](https://www.dane.gov.co/files/operaciones/EM/anex-EM-pobreza-2025.xlsx), cuadro 216A. Población urbana estimada e incidencia de pobreza monetaria por localidad. |

El manifiesto `datos/demo/inventario_insumos.csv` registra nombres, tamaños y huellas SHA-256. El directorio `datos/demo/` contiene resultados agregados y la capa pública de límites de localidades, atribuida a SDP/IDECA (CC BY 4.0). Los ZIP y las transacciones individuales quedan en el espacio de datos del equipo.

## Pregunta del proyecto

> ¿En qué estaciones y franjas horarias se concentran más validaciones respecto a los pasos programados y, donde haya suficientes posiciones GPS, qué tan cerca coincide el paso estimado de los buses con el horario previsto?

## Evidencia según la rúbrica

| Criterio | Cómo mostrarlo |
|---|---|
| C1 · Problema, 1,0 | Abrir con la pregunta del proyecto. Explicar qué muestran los dos días con validaciones y qué hace falta para contrastarlos con la oferta y el GPS. |
| C2 · Fuentes y preparación, 0,8 | Mostrar la unión de validaciones, estaciones, localidades y encuesta. Explicar la llave, los filtros, los faltantes y el control de totales. |
| C3 · Dashboard, 0,5 | Cambiar de domingo a festivo y explicar el cambio de hora pico. Mostrar Portal Norte en el ranking y en el mapa. |
| C4 · Recomendaciones, 0,5 | Proponer revisar Portal Norte y obtener un día con datos de entradas y oferta coincidentes antes de recomendar cambios de servicio. |
| C5 · Comunicación, 0,7 | Contar problema, evidencia, hallazgo y acción dentro de 10 minutos. Un ensayo de 8 minutos deja margen. |

El 16 fue festivo. La comparación no caracteriza días laborables comunes. Una validación registra un acceso y una parada del GTFS refleja el horario. La encuesta describe residentes de las localidades. El cruce de entradas y oferta requiere fecha, hora y código en común. Los ZIP del 22 y el 23 amplían la oferta, pero no añaden validaciones ni capturas GPS.
