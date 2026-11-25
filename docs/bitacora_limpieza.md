# Bitácora de preparación e integración

| Paso | Decisión | Resultado verificado |
| --- | --- | --- |
| Selección de validaciones | Trabajamos con accesos troncales de cada fecha. Leemos fecha, sistema y estación. | 9.205.097 validaciones del 18 al 23 de noviembre de 2026. |
| Preparar el GTFS | Seleccionamos rutas y viajes troncales activos según calendario y excepciones. Los horarios de servicios que pasan de medianoche se asignan a su fecha civil. | Pasos agrupados por fecha, hora y estación. |
| Cruzar entradas y programación | Normalizamos el código, agrupamos variantes de nombre bajo el mismo código y usamos fecha, hora y estación. Clasificamos como comparables las filas con estación identificada y pasos positivos. | 17.503 filas. Se cruzaron 8.065.892 validaciones, el 87,62 %. Quedaron 1.139.205 validaciones sin un paso comparable. |
| Ubicar estaciones | Usamos coordenadas GTFS y polígonos oficiales de Bogotá. Revisamos los puntos de las estaciones comparables en los GTFS del 18 al 23 y obtuvimos las mismas coordenadas. | 128 de 132 estaciones comparables asignadas. San Mateo, Terreros, León XIII y La Despensa quedaron sin coincidencia con los polígonos de Bogotá. |
| Añadir la Encuesta Multipropósito 2021 | Empatamos nombres normalizados de localidad con su código oficial. Aplicamos una unión de muchas filas por estación y hora a una localidad. Conservamos los porcentajes publicados y sus universos. | Se preservaron las 17.503 filas y sus totales. Las estaciones comparables con localidad cubren 7.640.382 validaciones, repartidas en 18 localidades. |
| Separar franjas | Exploramos pico de 06:00–08:59 y 16:00–18:59, valle de 09:00–15:59 y otras horas. Aplicamos los mismos rangos a ambos tipos de día. | Rangos propuestos para confirmar antes de presentar. La razón se calcula con sumas de filas comparables. |
