# Bitácora de preparación e integración

Los datos originales se conservan sin cambios. Esta bitácora distingue el primer borrador de Power BI de la integración corregida de Alejandro. Las tablas del tablero se reconstruyeron con el cruce corregido del 18 y se refrescó el `.pbix` a las 22:40; aun así, el primer borrador queda documentado como antecedente, no como resultado vigente.

## Primer borrador de Power BI

| Fecha | Fuente | Paso | Motivo | Filas antes | Filas después | Sin correspondencia | Responsable |
|---|---|---|---|---:|---:|---:|---|
| 2026-11-24 | ZIP oficiales de validaciones y GTFS diarios 16, 18–23/11 | Extraer fecha, hora y código de estación; sumar entradas y contar `stop_times` activos por estación-hora | Comparar misma unidad temporal y espacial sin exponer tarjeta/saldos | Transacciones y horarios individuales (volumen variable por día) | Un CSV agregado por fecha, estación y hora | 12–13 % de validaciones por día 19–23 no tuvieron paso emparejado; medir por fecha | Equipo; script `src/comparar_validaciones_gtfs.py` |
| 2026-11-24 | Tablas agregadas de validaciones y GTFS, 14–16 y 18–23/11 | Unir sin transformar faltantes en ceros; clasificar pico/valle y tipo de día; añadir coordenadas GTFS | Borrador homogéneo para Power BI | 26.060 filas de estación-hora concatenadas | 26.060 claves únicas | 2.521 filas sin coordenada; 14–15/11 sin GTFS del día | Script `src/preparar_borrador_powerbi.py` |
| 2026-11-24 | CSV de Alejandro del 18/11 y tabla principal | Usar correspondencia `estacion_gtfs` → localidad; conservar numeradores y denominadores previos | Añadir contexto territorial sin mezclar dos cálculos discordantes | 26.060 | 26.060 | 18 de 151 estaciones sin localidad asignada; 1.117 de 2.931 claves comunes tienen pasos distintos entre versiones | Script `src/integrar_localidades_powerbi.py` |
| 2026-11-24 | Encuesta Multipropósito 2021 agregada y tabla principal | Resumir por localidad para 18–23/11 | Explorar contexto de residentes sin inferir identidad de pasajeros | 20 localidades en contexto; 26.060 filas estación-hora en tabla principal | 19 localidades con estaciones mapeadas; 18 con razón comparable | Usme sin denominador comparable; 1 localidad sin estación mapeada en el resumen | Script `src/preparar_relacion_territorial_powerbi.py` |
| 2026-11-24 | Tabla principal 18–23/11 | Resumir por estación, limitar ranking a las que tienen seis fechas comparables | Evitar clasificar estaciones sin denominador | 151 estaciones identificadas | 132 estaciones comparables en seis fechas | 19 sin seis fechas comparables; no se interpretan como cero | Script `src/preparar_ranking_estaciones_powerbi.py` |

Antes y después de cada unión, verificar cardinalidad, duplicaciones y registros sin correspondencia. Explicar cualquier exclusión que pueda reducir la cobertura de una troncal o zona.

**Advertencia histórica:** el primer borrador usaba un conteo previo del 18 y pico 06–08/17–19, valle 09–16. La integración corregida usa pico 06–08/16–18 y valle 09–15. Las filas sin coordenada y las estaciones sin localidad no se interpretan como ceros: solo quedan fuera de visualizaciones que necesitan esos campos. [Scripts citados]

## Actualización del tablero a las 22:40

Se incorporó el CSV detallado corregido de Alejandro para el 18/11 sin modificarlo; los cruces locales del 19–23 mantenían los mismos totales de pasos. La tabla integrada de Power BI quedó limitada a **17.503 filas de 18–23/11**; la exploratoria conserva **26.060 filas de nueve fechas**. El 18 corregido aporta **248.283 pasos comparables** y el periodo completo **1.312.035**. Las seis tablas derivadas pasaron la prueba `tests/validar_tablas_powerbi.py` y el `.pbix` se actualizó y guardó. Falta revisar cada página visualmente, confirmar las franjas con el equipo y documentar la versión exacta de GTFS utilizada en el 18. [CSV detallado local de Alejandro; `datos/analisis/cobertura_diaria.csv`; tablas regeneradas; prueba citada]

## Integración corregida del 18–23

| Paso | Decisión | Resultado verificado |
| --- | --- | --- |
| Selección de validaciones | Trabajamos con accesos troncales de cada fecha. Leemos fecha, sistema y estación. | 9.205.097 validaciones del 18 al 23 de noviembre de 2026. |
| Preparar el GTFS | Seleccionamos rutas y viajes troncales activos según calendario y excepciones. Los horarios de servicios que pasan de medianoche se asignan a su fecha civil. | Pasos agrupados por fecha, hora y estación. |
| Cruzar entradas y programación | Normalizamos el código, agrupamos variantes de nombre bajo el mismo código y usamos fecha, hora y estación. Clasificamos como comparables las filas con estación identificada y pasos positivos. | 17.503 filas. Se cruzaron 8.065.892 validaciones, el 87,62 %. Quedaron 1.139.205 validaciones sin un paso comparable. |
| Ubicar estaciones | Usamos coordenadas GTFS y polígonos oficiales de Bogotá. Revisamos los puntos de las estaciones comparables en los GTFS del 18 al 23 y obtuvimos las mismas coordenadas. | 128 de 132 estaciones comparables asignadas. San Mateo, Terreros, León XIII y La Despensa quedaron sin coincidencia con los polígonos de Bogotá. |
| Añadir la Encuesta Multipropósito 2021 | Empatamos nombres normalizados de localidad con su código oficial. Aplicamos una unión de muchas filas por estación y hora a una localidad. Conservamos los porcentajes publicados y sus universos. | Se preservaron las 17.503 filas y sus totales. Las estaciones comparables con localidad cubren 7.640.382 validaciones, repartidas en 18 localidades. |
| Separar franjas | Exploramos pico de 06:00–08:59 y 16:00–18:59, valle de 09:00–15:59 y otras horas. Aplicamos los mismos rangos a ambos tipos de día. | Rangos propuestos para confirmar antes de presentar. La razón se calcula con sumas de filas comparables. |
