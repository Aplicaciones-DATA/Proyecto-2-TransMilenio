# Borrador de presentación, 8–10 minutos

Este guion acompaña el borrador de Power BI. Los números de pasos y sus cocientes son **provisionales** hasta conciliar la diferencia con el archivo de Alejandro. No usar palabras como “hacinamiento”, “puntualidad”, “pasajeros únicos” o “peor servicio” para interpretar estas razones. [Auditoría `reports/hallazgos_preliminares_2026-11-24.md`]

## 1. Problema y pregunta (1 minuto)

**En pantalla:** ¿Cuándo y dónde se registran más entradas frente a los pasos de bus programados? ¿Cómo cambia la comparación entre pico, valle, días hábiles y fin de semana? ¿Qué contexto muestran las localidades de esas estaciones?

**Decir:** Este primer diagnóstico ayuda a ubicar estaciones y momentos para investigar, pero no mide si un bus llegó a tiempo. El cambio de la pregunta original sobre confiabilidad real debe acordarse con el profesor. [Propuesta original; `docs/tablero_powerbi_2026-11-24.md`]

## 2. Fuentes y método (1,5 minutos)

**En pantalla:** Validaciones troncales oficiales + GTFS diario del 18 al 23 de noviembre de 2026. Encuesta Multipropósito 2021 solo como contexto por localidad.

**Decir:** Agrupamos entradas y horarios por fecha, hora y estación. Conservamos únicamente pares con un número positivo de pasos para el indicador `entradas por paso = suma de entradas comparables / suma de pasos de esas mismas filas`. No convertimos faltantes en cero. Cuatro días hábiles y dos de fin de semana entran en la comparación principal. [Scripts `src/comparar_validaciones_gtfs.py`, `src/preparar_borrador_powerbi.py`; `tests/validar_tablas_powerbi.py`]

## 3. Cobertura y magnitud (1 minuto)

**En pantalla:** 151 estaciones; 9,21 millones de entradas; 87,62 % de esas entradas con estación-hora comparable; 6,21 entradas por paso en las filas comparables, valor provisional.

**Decir:** La cobertura indica cuánta demanda registrada entró en el cociente. El 12,38 % restante (1.139.205 entradas) no tiene paso comparable con nuestra regla; no equivale a cero buses. Ni 6,21 ni el mapa representan cupos ocupados; un paso es un evento del horario. Si se muestra la página 1 de Power BI, advertir que sus dos curvas aún tienen periodos diferentes (nueve fechas de entradas frente a siete con GTFS). Para comparar directamente oferta y demanda, usar las páginas de pico/valle calculadas sobre 18–23/11. [Tabla integrada; `tests/validar_tablas_powerbi.py`; `docs/tablero_powerbi_2026-11-24.md`]

## 4. Pico, valle y tipo de día (1,5 minutos)

**En pantalla:** Página 5 de Power BI. Días hábiles: pico 7,38 y valle 6,83. Fin de semana: pico 5,39 y valle 5,76. Cocientes provisionales.

**Decir:** En estos cuatro días hábiles el valor de pico supera el de valle. En sábado y domingo ocurre lo contrario. Nuestras ventanas horarias son provisionales y visibles en la metodología; son pocas fechas, por lo que no extendemos la observación a todo el año. [Tabla integrada; `tests/validar_tablas_powerbi.py`]

## 5. Dónde se concentra la demanda (1 minuto)

**En pantalla:** Página 2 con mapa de estaciones y página 7 con ranking comparable. Mencionar como ejemplos de volumen total Portal Norte, Portal Américas y Portal Suba.

**Decir:** El mapa responde dónde se registraron entradas. El ranking de razón responde otra pregunta: cuántas entradas corresponden a cada paso programado, solo entre 132 estaciones presentes en las seis fechas comparables. No llamar a estas estaciones “las de peor servicio”. [Tabla integrada; `src/preparar_ranking_estaciones_powerbi.py`]

## 6. Contexto territorial y límites (1,5 minutos)

**En pantalla:** Páginas 3 y 6 de Power BI. Un mapa operativo y otro de contexto local; dispersión agregada por localidad.

**Decir:** La Encuesta Multipropósito describe residentes de 2021. Las entradas son de 2026 y se registran en una estación que puede no estar cerca de la vivienda del usuario. La comparación territorial es descriptiva, no identifica viajeros ni demuestra una causa. Hay localidad asignada a 133 de 151 estaciones. El mapa contextual muestra 18 localidades: Usme queda fuera por falta de coordenadas, aunque Cabecera Usme sí registra 253.175 entradas en el periodo. [CSV de Alejandro; EM2021; `src/preparar_relacion_territorial_powerbi.py`; `docs/auditoria_cobertura_estaciones_2026-11-24.md`]

## 7. Conclusión y siguiente comprobación (1 minuto)

**En pantalla:** Los horarios del periodo permiten detectar franjas y estaciones que merecen examen operativo. Confirmar la regla de conteo del GTFS y ampliar días cuando se publiquen validaciones.

**Decir:** El principal resultado sólido es el patrón de entradas observadas por hora y estación. La comparación con pasos ya funciona, pero la diferencia entre dos cálculos del denominador impide cerrar ese indicador como definitivo. Las posiciones GPS del piloto permitirían estudiar servicio real en otra fase, tras validar identificadores y cobertura. [Auditorías `reports/hallazgos_preliminares_2026-11-24.md`; `docs/plan_trabajo.md`]

## Antes de sustentar

- Sustituir “página 1/2/…” por los títulos finales del `.pbix` cuando estén cerrados.
- Abrir el `.pbix` en el PC de la presentación, comprobar rutas de CSV y ensayar con Alejandro el cambio de páginas.
- Si se incorpora el 24/11, recalcular las cifras de este guion y la presentación; no añadir el día por el solo hecho de tener GTFS/GPS.
- Mostrar la fuente y el periodo al menos en la diapositiva de método o junto al gráfico. [Checklist `docs/plan_trabajo.md`]
