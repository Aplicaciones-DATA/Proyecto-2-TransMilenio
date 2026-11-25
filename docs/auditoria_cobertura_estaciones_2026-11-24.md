# Auditoría de cobertura de estaciones y localidades

Fecha de revisión: 24/11/2026. Esta nota describe los archivos derivados locales; no reemplaza los datos crudos ni resuelve la discrepancia de pasos programados con Alejandro.

## Poblaciones que muestra cada visual

- La tabla principal `datos/procesados/powerbi_tabla_integrada_provisional.csv` reúne 151 estaciones y nueve fechas (14, 15, 16 y 18–23 de noviembre). Tiene 26.060 claves estación-fecha-hora; 23.539 filas incluyen coordenadas. No todas las estaciones o filas aparecen en los mapas.
- El análisis de entradas frente a oferta se restringe al 18–23 de noviembre y a las mismas claves estación-fecha-hora con pasos programados mayores que cero. En ese periodo, 8.065.892 de 9.205.097 entradas quedan emparejadas (87,62 %). No se debe presentar la razón como resultado de toda la red.
- Las otras 1.139.205 entradas (12,38 %) están en 2.185 filas etiquetadas `Sin paso comparable` dentro del 18–23/11. Esto significa que la tabla no encontró un paso GTFS positivo para esa estación y hora con la regla actual; **no demuestra que no pasaran buses**. Las filas comparables son 15.318 de 17.503.
- El ranking incluye 132 estaciones con seis fechas comparables, no las 151 de la tabla principal.
- La tabla territorial incluye 19 localidades con estaciones asignadas, pero solo 18 tienen una razón calculable. El mapa de contexto tiene coordenadas para 18 localidades, no 19.

## Cabecera Usme: ausencia de denominador y de coordenadas

La estación 9000, Cabecera Usme, suma 253.175 entradas del 18–23 de noviembre. Sus 188 filas de la tabla principal (nueve fechas) no tienen coordenadas; tampoco hay pasos programados comparables en el periodo analítico. Por eso su razón queda vacía y Usme no aparece en el mapa de contexto. Este vacío **no equivale a cero entradas, cero oferta ni ausencia de demanda**. Si se presenta el mapa, se debe mencionar explícitamente la exclusión.

Otras estaciones con bastantes entradas sin paso comparable son Corral Portal Dorado (151.993), Marly - Calle 57 (98.164), Ampliacion San Mateo (93.459), Temporal Avenida 39 (91.049), Temporal Flores (84.125), Temporal Calle 57 (71.998) y Temporal AV Jimenez - Inter Electricas (61.017). Es un orden de revisión de correspondencias, no una clasificación de déficit real de buses.

## Estaciones sin localidad asignada

El cruce con la tabla de Alejandro asignó localidad a 133 de 151 estaciones. Las 18 restantes conservan el valor vacío y se agrupan según el campo `estado_localidad` de la tabla derivada; estas etiquetas describen el resultado del cruce, no prueban su causa de fondo.

| Estado en la tabla | Estaciones |
| --- | --- |
| Código ausente en capa oficial (13) | 15001 Tibanica - Primavera; 15002 Los Laureles; 15003 Islandia; 2305 Bicicletero Portal Norte; 50003 Corral Molinos; 50008 Corral Portal Dorado; 57503 Ampliacion San Mateo; 9125 Temporal Calle 57; 9127 Temporal Flores; 9128 Temporal AV Jimenez - Inter Electricas; 9129 Temporal Calle 22; 9130 Temporal Avenida 39; 9131 Marly - Calle 57. |
| Fuera de los polígonos de localidades de Bogotá (4) | 7503 SAN MATEO - C.C. UNISUR; 7504 TERREROS; 7505 LEON XIII; 7506 DESPENSA. |
| Sin correspondencia en catálogo (1) | 8100 Portal Tunal Cable. |

Las 13 estaciones del primer grupo y Portal Tunal Cable tampoco tienen latitud/longitud en la tabla principal. Las cuatro estaciones fuera de los polígonos sí tienen coordenadas. No debe afirmarse que *toda* ausencia de localidad se deba a falta de GPS.

## Qué decir al presentar

«La comparación oferta-demanda y el ranking solo usan estaciones y horarios con datos emparejados. El mapa muestra únicamente puntos con coordenadas. Usme tiene entradas registradas, pero no una razón calculable ni un punto de mapa con estos archivos. Por tanto, las diferencias visibles son descriptivas de la muestra, no un diagnóstico completo de Bogotá».

## Procedencia y reproducción

Fuentes locales: `datos/procesados/powerbi_tabla_integrada_provisional.csv`, `datos/procesados/powerbi_borrador_estacion_hora.csv`, `datos/procesados/powerbi_relacion_localidad.csv`, `datos/procesados/powerbi_mapa_contexto_localidad.csv`, `datos/procesados/powerbi_ranking_estaciones.csv` y `../data_casi_lista/Comparacion_TransMilenio_2026-11-18_con_localidades.csv`. Transformaciones: `src/integrar_localidades_powerbi.py`, `src/preparar_relacion_territorial_powerbi.py`, `src/preparar_mapa_contexto_powerbi.py` y `src/preparar_ranking_estaciones_powerbi.py`. Verificación de totales y claves: `tests/validar_tablas_powerbi.py`.
