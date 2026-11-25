# Contexto e instrucciones para Claude sobre la presentación del Proyecto 2

Actúa como asistente de diseño y revisión de una presentación ejecutiva para un proyecto universitario de Aplicaciones en Ciencia de Datos. Trabaja en español claro, con un lenguaje que entienda una persona sin conocimientos técnicos. La presentación debe poder exponerse en **máximo diez minutos**. No conviertas las diapositivas en un informe: el análisis detallado irá en un documento Word separado. Tu tarea es seleccionar la evidencia visual más importante, ordenar la historia y dejar notas del presentador que ayuden a Emanuel y Alejandro a explicarla.

## Antes de producir material

**Advertencia académica importante:** el enunciado oficial `C:\Users\c.collazost\Downloads\Proyecto_2___DATA1002 (1).pdf` prohíbe expresamente el uso de IA generativa en cualquier producto del proyecto, incluidos código, repositorio, dashboard y presentación. Señala esta restricción al equipo antes de preparar algo para entregar. No sugieras ocultar el uso de IA ni presentes un material generado como si fuera inequívocamente permitido por el curso. El equipo debe aclarar la situación con el profesor y asumir la decisión sobre el uso de este borrador. Mientras tanto, tu trabajo puede servir como material interno de revisión.

No afirmes que el profesor aprobó el cambio de pregunta, que el dashboard posterior al envío ya se entregó o que existe una calificación. La pregunta funcional fue escogida por el equipo; Emanuel confirmó que no necesita autorización previa para elegirla. La entrega grupal anterior sí quedó registrada en Bloque Neón el 24 de noviembre de 2026 a las 23:58, pero la versión mejorada del tablero es posterior.

## Proyecto y pregunta elegida

El caso estudia la relación descriptiva entre **entradas registradas a estaciones troncales de TransMilenio** y **pasos de bus programados**. La pregunta acordada es:

> ¿Cómo varían las entradas registradas frente a los pasos de bus programados entre las franjas pico y valle, los días hábiles y fines de semana, y las estaciones troncales de los días comparables? ¿Qué contexto territorial muestran las localidades donde se encuentran esas estaciones?

Queremos mostrar **qué** se observó, **cuándo** se observó, **dónde** se concentró y qué relación descriptiva aparece entre demanda registrada, oferta programada y contexto territorial. El valor práctico es identificar estaciones y franjas que merecen una revisión operativa más detallada. No estamos midiendo cumplimiento real de horarios, ocupación de buses, hacinamiento ni pasajeros únicos.

La propuesta inicial del equipo hablaba de confiabilidad real, puntualidad y efecto racimo. Las fuentes verificadas no sostienen esas afirmaciones. El tablero actual responde una pregunta acotada de demanda registrada frente a oferta **programada**. El histórico GPS es un piloto aparte; no mezcles sus capturas con el indicador central ni lo presentes como prueba de llegadas reales.

## Alcance correcto de esta versión

Por decisión de Emanuel, **excluye por completo el 18 de noviembre de 2026 de las comparaciones, gráficos, KPI y conclusiones**. El análisis que debe aparecer en esta presentación cubre **del 19 al 23 de noviembre de 2026**, con **tres días hábiles y dos de fin de semana**. El motivo no es que no exista un ZIP GTFS del 18: sí existe. El problema es que el conteo corregido usado en el tablero previo (248.283 pasos) no se ha podido reproducir con el GTFS local y la regla documentada (235.072 pasos). Hay 13.211 pasos de diferencia. Etiqueta esto como una **discrepancia de procedencia y cálculo no resuelta** y explica que por prudencia ese día se excluyó. No borres los originales ni digas que se perdió la recolección.

Las franjas de trabajo, no oficiales de TransMilenio, son **pico 06:00–08:59 y 16:00–18:59**; **valle 09:00–15:59**. Las demás horas son una categoría aparte. No cambies estas ventanas sin recalcular todo.

## Fuentes, integración y unidades

1. **Validaciones troncales oficiales de TransMilenio**, descargadas por día del portal `https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html`. Una validación es una entrada registrada, no una persona única ni necesariamente un viaje completo.
2. **GTFS estático diario de TransMilenio**, obtenido del portal `https://gtfs.transmilenio.gov.co/`. `stop_times.txt`, `trips.txt` y las reglas de calendario permiten contar pasos **programados** por estación, fecha y hora. Un paso programado no es un bus observado, un asiento disponible ni una prueba de puntualidad.
3. **Encuesta Multipropósito 2021**, del DANE y la Secretaría Distrital de Planeación. Se agrega por localidad y sirve como contexto de los **residentes en 2021**. No sabemos si esas personas son quienes validaron en las estaciones en 2026. La localidad de la estación tampoco demuestra la localidad de residencia del pasajero.
4. **Geografía de localidades y coordenadas de estaciones** para ubicar el contexto territorial. La correspondencia espacial es parcial; ausencia del mapa no significa cero entradas.

La unidad de la tabla principal es **una estación en una fecha y una hora**. Se unen validaciones y pasos por esas tres claves. Una fila es comparable si existe un paso programado positivo en esa misma combinación. La razón correcta es **suma de validaciones de filas comparables dividida por suma de pasos programados de esas mismas filas**. No promedies razones individuales, no dividas una curva general de entradas entre otra de pasos si incluyen poblaciones distintas, no sustituyas faltantes por cero y no lo llames porcentaje ni ocupación.

Hay dos tablas socioeconómicas distintas. `datos\analisis\contexto_localidades_em2021.csv` presenta indicadores de ingresos insuficientes y tiempos de viaje a trabajo o estudio tomados de cuadros publicados por DANE; `datos\procesados\powerbi_contexto_localidad_em2021.csv` alimenta el mapa del PBIX con indicadores de pobreza monetaria y uso declarado de TransMilenio. **No mezcles indicadores ni denominadores de una tabla con la otra.** En cada visual social indica el indicador exacto, su universo, la fuente y el año.

## Cifras de control del corte del 19 al 23 de noviembre

Estas cifras se calcularon filtrando por fecha la tabla integrada local y deben cotejarse de nuevo contra los CSV definitivos y contra Power BI una vez actualizado el PBIX. **Si el tablero muestra las cifras antiguas del 18 al 23, no está listo para usarse como versión final.**

| Indicador | Valor del 19 al 23 | Lectura correcta |
| --- | ---: | --- |
| Entradas registradas | 7.252.722 | Conteo de validaciones, no de pasajeros únicos. |
| Entradas comparables | 6.353.794 | Entradas en estación–fecha–hora con paso programado positivo. |
| Pasos programados en filas comparables | 1.063.752 | Denominador del indicador; no es toda la oferta de la red. |
| Entradas por paso programado comparable | 5,97 | Cociente 6.353.794 / 1.063.752. No es ocupación. |
| Cobertura de entradas para la razón | 87,61 % | Porcentaje de entradas que entró en la comparación. |

En días hábiles del corte, el cociente en pico es **7,91** (2.418.244 entradas comparables / 305.862 pasos) y en valle **6,20** (1.521.184 / 245.239). En los dos días de fin de semana, pico es **5,62** (644.499 / 114.613) y valle **5,78** (778.154 / 134.549). Describe estas diferencias como observaciones de los cinco días, **no como tendencia estable de todo Bogotá o de todos los fines de semana**. Al excluir el 18, los cuatro días hábiles anteriores pasan a ser tres: evita reutilizar textos o promedios de la versión de seis días.

Como verificación adicional, los mayores totales de entradas registrados en el corte incluyen Portal Norte (283.353), Portal Américas (268.751) y Portal Suba (225.693). Son volúmenes, no tasas de servicio ni prueba de saturación. La tabla filtrada conserva 151 estaciones; 135 tienen coordenadas y 133 tienen localidad. Las estaciones con coordenadas representan 6.428.527 entradas (88,64 % del total) y las que tienen localidad 6.319.643 (87,13 %). Coteja esos controles con el tablero actualizado. Cabecera Usme requiere una nota de cobertura si sigue fuera de la razón o del mapa. Recalcula el ranking y todas las etiquetas espaciales para este corte; no copies posiciones ni porcentajes del tablero de seis días.

## Archivos y revisión previa

Repositorio de trabajo local: `C:\Users\c.collazost\Desktop\DATA\PROYS\PROY FINAL\Proyecto-2-TransMilenio`.

La **copia de trabajo recalculada** está en `C:\Users\c.collazost\Desktop\DATA\PROYS\PROY FINAL\DATOS - Muestra 0.1\TransMilenio_19-23_noviembre_2026.pbix`. Se refrescó en Power BI Desktop con los seis CSV recalculados del 19–23; también hay copias de esos CSV junto al PBIX, en la subcarpeta `Datos_PowerBI_19_23`. Se comprobaron las tarjetas **5,97** entradas por paso y **87,61 %** de cobertura, además de los mapas y la comparación pico/valle. El archivo tiene nueve páginas: Entradas y oferta, Mapa de entradas, Mapa social, Pico y valle, Entradas por paso, Contexto territorial, Estaciones, Método y límites, e Indicadores. Se corrigieron los dos títulos que todavía decían 18–23 y el texto de Método y límites. Antes de convertirlo en pieza definitiva, revisa las nueve páginas y prueba los filtros. Al abrirlo en otro equipo, puede ser necesario cambiar las rutas de origen de los seis CSV y volver a pulsar **Actualizar**. El PBIX histórico del repositorio en `outputs\TransMilenio_postentrega_2026-11-25_filtros.pbix` **no** es esta versión y conserva el corte anterior.

Consulta `docs\resultados.md`, `docs\plan_trabajo.md`, `docs\fuentes.md`, `docs\fuentes_socioeconomicas.md` y `docs\bitacora_limpieza.md` para explicar solo decisiones documentadas. El análisis narrativo está en `docs\analisis_graficos_19_23_2026.docx` y también junto al PBIX en `DATOS - Muestra 0.1`; úsalo para las notas del presentador. Si sus números no coinciden con el PBIX tras abrirlo, detén las afirmaciones numéricas y señala exactamente el conflicto. Las seis imágenes antiguas en `outputs\borradores_powerbi\` pertenecen a un corte histórico diferente: **no las reutilices** como gráficos del 19–23.

## Presentación ejecutiva solicitada

Prepara un borrador editable con **aproximadamente ocho diapositivas** y notas del presentador. El tiempo total sugerido es de nueve minutos y medio; deja margen para transiciones. Los títulos deben decir la idea principal con palabras sencillas, no solo el tipo de gráfico. Usa pocos números por lámina, unidades visibles y fuente/periodo legibles. No llenes las láminas con párrafos del Word. Mantén el mismo significado de colores entre láminas y no utilices un solo color como única forma de distinguir series.

1. **Portada y respuesta en una frase, 45 segundos.** Título del proyecto, nombres completos y códigos estudiantiles tal como los confirme el equipo, curso y periodo 19–23/11. Frase de apertura: en estos cinco días, la relación entre entradas registradas y pasos programados fue mayor en las horas pico de los días hábiles que en valle. No atribuyas una causa.
2. **Problema, decisión y pregunta, 60 segundos.** Explica por qué importa observar en qué lugares y horas se concentran las entradas frente a la programación: ayuda a priorizar una revisión. Muestra la pregunta elegida en una versión legible. Aclara que es una exploración descriptiva, no una auditoría de puntualidad.
3. **Fuentes y método, 75 segundos.** Diagrama simple: validaciones + GTFS, unidos por estación, fecha y hora; encuesta de 2021 agregada por localidad para contexto. Explica unidad de análisis, reglas pico/valle y exclusión del 18 por discrepancia no reproducible. Resume las decisiones documentadas sobre inconsistencias, faltantes, duplicados y filas sin correspondencia; no atribuyas al equipo una limpieza que no conste en código o bitácora. Menciona que los originales no se alteran y que los datos personales no se muestran.
4. **Cobertura y significado de los KPI, 60 segundos.** Presenta las cinco cifras de control en una jerarquía clara, sin sugerir que «5,97» sean personas dentro de cada bus. La frase oral debe explicar: «de cada cien entradas registradas, unas 88 pudieron compararse con al menos un paso programado en la misma estación y hora». El resto es dato no comparable, no cero buses.
5. **Cuándo cambia la relación, 90 segundos.** Usa el gráfico de pico/valle y hábil/fin de semana, con los cuatro cocientes correctos (7,91; 6,20; 5,62; 5,78). Si incluyes curvas por hora de entradas y pasos, mantenlas con ejes/unidades separados. Destaca que el contraste pico–valle observado es marcado entre semana, no igual en fin de semana. Da fechas y número de días.
6. **Dónde se registran más entradas, 75 segundos.** Mapa de estaciones con escala de entradas y, si conviene, un ranking breve. Destaca Portal Norte, Portal Américas y Portal Suba por volumen del corte 19–23. Diferencia volumen total de razón por paso; no llames «peor servicio» a un punto oscuro o alto. Añade una nota visible de cobertura de coordenadas, recalculada para este corte.
7. **Contexto territorial, 75 segundos.** Mapa social y, solo si es legible, dispersión por localidad. Explica qué indicador social exacto muestra cada visual y su universo. Puedes contrastar zonas, pero no afirmar que los usuarios de cierta estación tienen las características de los residentes de esa localidad. No proclames asociación estadística si no la verificaste con el corte final; una coincidencia visual puede ser solo contextual.
8. **Conclusiones, limitaciones y acciones, 90 segundos.** Dos o tres conclusiones ligadas a gráficos vistos, dos límites decisivos (pasos programados no reales; cobertura espacial/temporal parcial y exclusión del 18) y recomendaciones concretas proporcionadas al alcance: revisar en campo o con datos operativos las estaciones/franjas destacadas, obtener un histórico GPS validado si se quisiera estudiar puntualidad, y ampliar/conciliar días antes de generalizar. No recomendar modificar rutas ni afirmar déficit de buses solo por el cociente.

Las duraciones son orientativas; el total debe mantenerse **por debajo de diez minutos**. Si una diapositiva necesita más explicación, recorta texto y prioriza la respuesta a la pregunta principal.

## Qué debes entregar al equipo para revisar

- Un archivo de diapositivas **editable**, claramente marcado como borrador hasta que Emanuel y Alejandro lo revisen.
- Notas del presentador con una explicación oral natural de cada gráfico y una referencia al apartado correspondiente del Word.
- Una lista breve de todas las cifras utilizadas, con la tabla y fórmula de donde salen. Verifica que ninguna dependa del 18.
- Una lista de inconsistencias que todavía impidan cerrar el material, especialmente diferencia entre CSV y PBIX, cobertura geográfica sin actualizar, indicador socioeconómico ambiguo o enlaces rotos.

**No inventes cifras, mapas, conclusiones, nombres completos, códigos estudiantiles, causalidad ni calificaciones.** Si falta una gráfica exportada del PBIX actualizado, márcala como pendiente y solicita la exportación; no reemplaces con una imagen del corte anterior. El Word puede ser detallado, pero la presentación debe contar una historia breve y precisa que responda la pregunta escogida y alcance los criterios de la rúbrica del profesor.
