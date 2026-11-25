# Tablero Power BI: borrador funcional del 24 de noviembre

Archivo local: `outputs/TransMilenio_borrador_2026-11-24.pbix`. Es un borrador **guardado en el PC**, no un tablero publicado ni una entrega. `outputs/` está excluido de Git; para abrirlo en otro equipo habrá que compartir el `.pbix` y los CSV derivados, y ajustar sus rutas de origen. Este documento reemplaza el estado antiguo descrito en `borrador_tablero_powerbi.md`.

## Pregunta y unidad de comparación

**¿Cómo varían las entradas registradas frente a los pasos de bus programados entre las franjas pico y valle, los días hábiles y fines de semana, y las estaciones troncales de los días comparables? ¿Qué contexto territorial muestran las localidades donde se encuentran esas estaciones?** La pregunta sobre confiabilidad/puntualidad real de la propuesta original sigue sin resolverse con este indicador y debe acordarse con el profesor si se cambia formalmente el alcance. [Propuesta Proyecto 2, `README.md`; cálculo local en `src/comparar_validaciones_gtfs.py`]

Una fila de la tabla principal es **estación GTFS + fecha + hora**. `validaciones` cuenta entradas registradas, no personas únicas. `pasos_programados` cuenta llegadas en `stop_times.txt` para servicios activos ese día; no son buses observados, cupos, ocupación ni puntualidad. La razón se calcula siempre como **suma de validaciones comparables / suma de pasos programados de esas mismas filas**. `comparable` exige mismo día, estación y hora y un denominador mayor que cero. Los nulos no se convierten en cero. [Scripts `src/comparar_validaciones_gtfs.py` y `src/preparar_borrador_powerbi.py`; GTFS y validaciones del inventario local]

Franjas de análisis **provisionales**: pico 06:00–08:59 y 17:00–19:59; valle 09:00–16:59; las demás se muestran aparte. No se afirma que esta sea la definición oficial de TransMilenio. El 16/11 se presenta como lunes con servicio dominical, no como día hábil común. [Regla explícita en `src/preparar_borrador_powerbi.py`; `calendar_dates.txt` del GTFS del 16/11]

## Fuentes y periodo cargados

- [Validaciones troncales oficiales](https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html): 14, 15, 16 y 18–23 de noviembre de 2026. Sus ZIP originales permanecen en `../registros_diarios/AAAA-MM-DD/` y se leen solo con fecha, estación y sistema. El 24/11 no estaba publicado en el portal al consultar el 24/11 hacia las 20:00; las capturas GPS de ese día **no sustituyen** validaciones. [Portal oficial; `src/comparar_validaciones_gtfs.py`]
- GTFS diario: 16 y 18–23 de noviembre en las mismas carpetas diarias. Para 14 y 15 no hay GTFS emparejado en la tabla, por lo cual sí contribuyen a gráficos de demanda, pero no a la razón ni a la oferta. [ZIP originales e inventario `docs/registro_descargas.md`]
- Tabla de Alejandro `../data_casi_lista/Comparacion_TransMilenio_2026-11-18_con_localidades.csv`: se usa para asignar **estación → localidad**, no para reemplazar los pasos del cálculo previo. En 1.117 de 2.931 claves comunes del 18/11 los pasos difieren; suman 248.283 en el archivo de Alejandro frente a 235.072 en la versión previa. Debe aclararse la regla de conteo antes de fijar una cifra definitiva. [Auditoría en `src/integrar_localidades_powerbi.py`]
- [Encuesta Multipropósito 2021](https://datosabiertos.bogota.gov.co/dataset/encuesta-multiproposito-2021-sdp/resource/b3fd892e-b9f9-4f34-ac22-6cc50612eac9): indicadores agregados por localidad de residentes de 2021 (pobreza monetaria y respuestas sobre uso de TransMilenio para trabajo/estudio). **No** describen a las personas que entraron por cada estación en 2026. [Script `src/preparar_contexto_localidad.py`; `docs/fuentes_socioeconomicas.md`]

## Tablas derivadas y controles

1. `powerbi_borrador_estacion_hora.csv`: 26.060 claves únicas de nueve fechas, sin entradas negativas; 23.539 filas con coordenadas.
2. `powerbi_tabla_integrada_provisional.csv`: conserva las 26.060 filas y los conteos, añade localidad para 133 de 151 estaciones. No se sustituyeron los pasos discrepantes de Alejandro.
3. `powerbi_contexto_localidad_em2021.csv` y `powerbi_mapa_contexto_localidad.csv`: agregados territoriales; el mapa usa puntos representativos de las estaciones de cada localidad, **no** polígonos de residencia.
4. `powerbi_relacion_localidad.csv`: 19 localidades con estaciones mapeadas en 18–23/11; 18 tienen una razón comparable y Usme queda sin razón. La dispersión omite esa localidad por falta de denominador, no porque su valor sea cero.
5. `powerbi_ranking_estaciones.csv`: 132 estaciones con seis fechas comparables. La primera es Portal 20 de Julio, con 26,47 entradas por paso programado en el periodo; es una señal descriptiva, no evidencia de peor servicio. La cobertura de validaciones dentro de esas 132 estaciones es 99,92 %, **no** cobertura del sistema completo.

La auditoría detallada de las 18 estaciones sin localidad y de Cabecera Usme está en `docs/auditoria_cobertura_estaciones_2026-11-24.md`. El mapa de contexto muestra 18 localidades, no las 19 de la tabla territorial; Usme registra 253.175 entradas en el periodo comparable, pero no tiene pasos emparejados ni coordenadas en la tabla principal. No interpretamos esos vacíos como ceros.

Las tablas se regeneran, en orden, con `src/comparar_validaciones_gtfs.py` para cada fecha, `src/preparar_borrador_powerbi.py`, `src/integrar_localidades_powerbi.py`, `src/preparar_contexto_localidad.py`, `src/preparar_mapa_contexto_powerbi.py`, `src/preparar_relacion_territorial_powerbi.py` y `src/preparar_ranking_estaciones_powerbi.py`. Se requieren los ZIP originales en las rutas indicadas; no se alteran. Tras regenerarlas, usar **Actualizar** en Power BI Desktop y verificar los resultados. [Scripts citados]

## Ocho páginas actuales del `.pbix`

1. Dos curvas horarias: entradas promedio por día y pasos programados promedio por día, separados porque tienen unidades distintas. **No son todavía un par con el mismo periodo:** la curva de entradas incorpora las nueve fechas cargadas (14, 15, 16 y 18–23), mientras la de pasos solo puede mostrar los siete días con GTFS (16 y 18–23). La serie «Lunes con servicio dominical» muestra que el 16 está presente. Para responder la pregunta principal con curvas comparables, falta filtrar ambas a 18–23 o rotular explícitamente esta diferencia. La página 4 también requiere verificar su filtro temporal antes de compararla directamente con el cociente de la página 5.
2. Mapa de concentración de entradas por estación con coordenadas GTFS.
3. Mapa contextual por localidad: pobreza monetaria de residentes de EM2021 y tooltips de uso de TransMilenio para trabajo/estudio. Un punto representa estaciones de la localidad, no el domicilio de usuarios.
4. Barras de entradas promedio por hora para pico/valle y tipo de día. El promedio horario evita confundir franjas de distinta duración.
5. Barras de entradas por paso programado para pico/valle y tipo de día, solo filas comparables.
6. Dispersión territorial: pobreza monetaria de residentes (eje X), entradas por paso en estaciones de la localidad (eje Y), tamaño por número de estaciones. Periodo operativo fijo 18–23/11; encuesta de 2021. No implica causalidad.
7. Top 10 de estaciones por entradas por paso programado del 18–23/11, filtrado sobre las 132 estaciones comparables.
8. Método y límites: define entradas, pasos programados, razón, franjas provisionales, alcance territorial de EM2021 y la discrepancia abierta con Alejandro. Esta nota ya es visible dentro del tablero.

Las ocho páginas tienen nombres descriptivos. El archivo se guardó de nuevo a las 21:35 (hora de Bogotá). Aún faltan filtros interactivos, tarjetas KPI finales y una revisión conjunta de cifras con Alejandro. Las fuentes y las limitaciones deben acompañar la demostración oral y la presentación, no depender únicamente de este documento.

La auditoría automatizada `tests/validar_tablas_powerbi.py` comprobó 26.060 claves estación-fecha-hora únicas, 151 estaciones, 133 con localidad, 23.539 filas geocodificadas y 87,62 % de cobertura de entradas en el periodo comparable **18–23/11**. Este porcentaje no incluye el 14 y el 15, que carecen de GTFS emparejado. La prueba no sustituye la revisión visual ni resuelve el denominador discrepante. [Tablas derivadas; prueba citada]

## Antes de entregar

- Resolver con Alejandro la diferencia en `pasos_programados` y documentar cuál definición queda. Al recalcular el 18/11 con versiones GTFS posteriores, los horarios del 20–22 se parecen mucho más a su tabla (93,07 % de coincidencias) que los del propio 18 (56,54 %), pero sigue sin probarse qué ZIP utilizó. Hasta aclararlo, todas las razones son **provisionales**. Ver `tests/comparar_versiones_gtfs_18.py` y `reports/hallazgos_preliminares_2026-11-24.md`.
- Si el portal publica validaciones del 24/11, descargarlas, verificar integridad y procesarlas con el GTFS del mismo día. Las capturas GTFS-RT del 24/11 ya están en Drive, pero no aportan conteos de entrada.
- La auditoría de las 18 estaciones sin localidad quedó documentada en `docs/auditoria_cobertura_estaciones_2026-11-24.md`. Sigue pendiente revisar la causa de todos los registros sin oferta comparable; no afirmar cobertura universal de Bogotá.
- Revisar manualmente una estación-hora y los totales en Power BI; las notas metodológicas ya están visibles. Priorizar que las dos curvas de la página 1 usen 18–23/11 o tengan un aviso de periodos distintos. Agregar filtros de fecha/franja/localidad y tarjetas KPI acordadas si el tiempo y la conciliación del denominador lo permiten.
- Preparar la presentación de máximo 10 minutos, ensayar, compartir un archivo abrible por Alejandro y verificar el mecanismo oficial de entrega antes de publicar. La fecha oficial anotada en la memoria académica es 24/11/2026 23:59; el equipo se puso como meta operativa las 23:00. [Bloque Neón, `src-bloque-neon-data-proyecto-2-2026-11-23`; indicación del usuario]
