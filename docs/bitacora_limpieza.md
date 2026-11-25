# Bitácora de preparación e integración

Los datos originales se conservan sin cambios. Registrar aquí cada limpieza, transformación y unión, incluyendo su efecto sobre la cantidad de registros y las zonas representadas.

| Fecha | Fuente | Paso | Motivo | Filas antes | Filas después | Sin correspondencia | Responsable |
|---|---|---|---|---:|---:|---:|---|
| 2026-11-24 | ZIP oficiales de validaciones y GTFS diarios 16, 18–23/11 | Extraer fecha, hora y código de estación; sumar entradas y contar `stop_times` activos por estación-hora | Comparar misma unidad temporal y espacial sin exponer tarjeta/saldos | Transacciones y horarios individuales (volumen variable por día) | Un CSV agregado por fecha, estación y hora | 12–13 % de validaciones por día 19–23 no tuvieron paso emparejado; medir por fecha | Equipo; script `src/comparar_validaciones_gtfs.py` |
| 2026-11-24 | Tablas agregadas de validaciones y GTFS, 14–16 y 18–23/11 | Unir sin transformar faltantes en ceros; clasificar pico/valle y tipo de día; añadir coordenadas GTFS | Borrador homogéneo para Power BI | 26.060 filas de estación-hora concatenadas | 26.060 claves únicas | 2.521 filas sin coordenada; 14–15/11 sin GTFS del día | Script `src/preparar_borrador_powerbi.py` |
| 2026-11-24 | CSV de Alejandro del 18/11 y tabla principal | Usar correspondencia `estacion_gtfs` → localidad; conservar numeradores y denominadores previos | Añadir contexto territorial sin mezclar dos cálculos discordantes | 26.060 | 26.060 | 18 de 151 estaciones sin localidad asignada; 1.117 de 2.931 claves comunes tienen pasos distintos entre versiones | Script `src/integrar_localidades_powerbi.py` |
| 2026-11-24 | Encuesta Multipropósito 2021 agregada y tabla principal | Resumir por localidad para 18–23/11 | Explorar contexto de residentes sin inferir identidad de pasajeros | 20 localidades en contexto; 26.060 filas estación-hora en tabla principal | 19 localidades con estaciones mapeadas; 18 con razón comparable | Usme sin denominador comparable; 1 localidad sin estación mapeada en el resumen | Script `src/preparar_relacion_territorial_powerbi.py` |
| 2026-11-24 | Tabla principal 18–23/11 | Resumir por estación, limitar ranking a las que tienen seis fechas comparables | Evitar clasificar estaciones sin denominador | 151 estaciones identificadas | 132 estaciones comparables en seis fechas | 19 sin seis fechas comparables; no se interpretan como cero | Script `src/preparar_ranking_estaciones_powerbi.py` |

Antes y después de cada unión, verificar cardinalidad, duplicaciones y registros sin correspondencia. Explicar cualquier exclusión que pueda reducir la cobertura de una troncal o zona.

**Advertencia:** `pasos_programados` aún requiere conciliación con la versión de Alejandro. Las cifras derivadas son provisionales. Las filas sin coordenada y las estaciones sin localidad no se eliminan de la tabla principal; solo quedan fuera de las visualizaciones que necesitan esos campos. [Scripts citados]
