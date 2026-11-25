# Plan de trabajo — Proyecto 2 TransMilenio

## Estado operativo al 24/11/2026, 23:18 (Bogotá)

La pregunta funcional acordada por el equipo es: **¿cómo varían las entradas registradas frente a los pasos programados entre pico/valle, días hábiles/fines de semana y estaciones de los días comparables, y qué contexto muestran las localidades de esas estaciones?** Esta es una comparación descriptiva de oferta programada y demanda registrada, no de confiabilidad real. El cambio formal de la pregunta original sigue por confirmar con el profesor. [Propuesta original; indicación del usuario; `docs/tablero_powerbi_2026-11-24.md`]

Se integraron los cruces del **18–23/11**, con el 18 corregido de Alejandro. La tabla exploratoria conserva 26.060 claves de nueve fechas; la integrada para comparar oferta y demanda contiene **17.503 filas de seis fechas**. La prueba automatizada pasó. Las ocho páginas del `.pbix` se exportaron a PDF y se revisaron visualmente; el archivo se guardó de nuevo a las 23:13 tras aclarar los nombres y agregaciones de los gráficos territoriales. El mapa sigue mostrando una advertencia de Power BI sobre la futura retirada de ese tipo de visual. Se compartió en Drive un paquete nuevo con **solo el `.pbix` y seis CSV derivados**; los anteriores quedan como versiones históricas. El 24/11 tiene GTFS y capturas GTFS-RT en Drive, pero sus validaciones oficiales no figuraban en el portal al último chequeo; no se añaden al cociente. La cobertura de entradas comparables es **87,62 %**. [Datos `datos/analisis/cobertura_diaria.csv`; `tests/validar_tablas_powerbi.py`; inspección visual local; `docs/tablero_powerbi_2026-11-24.md`; portal oficial]

**Prioridad antes de entregar:** (1) probar filtros interactivos y añadir KPI acordados si alcanza el tiempo; (2) revisar hallazgos y ensayar la presentación de máximo 10 minutos; (3) documentar con Alejandro la versión GTFS del 18 y verificar enlaces y mecanismo oficial de entrega. Enviar la entrega requiere autorización inmediata del estudiante. La meta interna de 23:00 ya pasó; Bloque Neón indica 23:59. [Auditoría local; `src-bloque-neon-data-proyecto-2-2026-11-23`]

## Pregunta que sí podemos responder ahora

**¿En qué estaciones troncales y horas se registran más entradas durante los días disponibles?** Esta primera subpregunta se responde con las validaciones diarias. La unidad es la validación, no el pasajero único. La comparación posterior con oferta programada usa solo los días emparejados, como indica la sección anterior. El notebook `02_demanda_observada_estaciones.ipynb` procesa los ZIP por bloques y genera una tabla por fecha, hora y estación.

## Preguntas para la siguiente etapa

1. **¿Cuántos viajes se programan por ruta, estación y franja en una fecha concreta?** Requiere `calendar.txt`, `calendar_dates.txt` y `stop_times.txt` de una versión GTFS compatible con esa fecha.
2. **¿Dónde coinciden alta demanda registrada y menor oferta programada?** Ya hay cruces para el 16 y el 18–23 de noviembre. Sigue pendiente auditar las estaciones no emparejadas y conciliar dos formas de contar pasos. Es una señal de relación entre entradas y oferta programada, **no ocupación real**.
3. **¿Cómo cambian los patrones entre días y franjas?** El borrador compara pico/valle y días hábiles/fines de semana sobre las fechas disponibles; antes de generalizar se debe revisar cobertura y que cada ZIP cubra el día completo.
4. **Piloto opcional: ¿qué buses aparecen en las capturas y qué rutas reportan?** Requiere decodificar `positions.pb`, guardar varias capturas con fecha y hora, medir cobertura y revisar si sus identificadores coinciden con el GTFS. No bloquea el cruce principal ni equivale todavía a medir puntualidad.

La pregunta de la propuesta sobre **confiabilidad real y efecto racimo** queda pendiente de validación con el profesor: las validaciones de pasajeros no indican cuándo pasó cada bus. No se inferirá racismo ni afectación de un grupo a partir de promedios por zona.

## Checklist para terminar

- [x] Repositorio, estructura y fuentes iniciales documentadas.
- [x] Explorar rutas y viajes publicados en el GTFS (`notebook 01`).
- [x] Organizar cuatro tablas GTFS necesarias en `datos/raw/gtfs` local.
- [x] Preparar notebook de validaciones reales por estación y hora (`notebook 02`).
- [x] Ejecutar el código del notebook 02 con los tres ZIP disponibles y revisar cobertura y faltantes. Los ZIP del 13, 14 y 15 de noviembre contienen 1.898.914, 1.245.040 y 620.221 filas; cada uno se prolonga unas horas después de medianoche. Las gráficas quedan pendientes de verificar en un entorno con Matplotlib.
- [ ] Confirmar con el profesor la pregunta final y el alcance de la comparación oferta-demanda.
- [x] Obtener GTFS y validaciones oficiales para el 16 y el 18 de noviembre, guardados por fecha sin alterar originales.
- [x] Procesar `calendar.txt`, `calendar_dates.txt` y `stop_times.txt` por partes para oferta por fecha, estación y hora en esos dos días.
- [x] Auditar la correspondencia de estaciones: 133 de 151 tienen localidad asignada; las otras 18 están identificadas y clasificadas en `docs/auditoria_cobertura_estaciones_2026-11-24.md`. Se incorporó el conteo corregido de Alejandro para el 18 sin modificar el CSV original. Aún no se han resuelto las ausencias de origen.
- [x] Integrar oferta programada y demanda observada solo en filas con fechas y estaciones comparables; resultados piloto e informe en `reports/informe_alejandro_cruce_fechas.md`.
- [x] Descargar y verificar GTFS y validaciones del 19–23/11; generar los cinco cruces diarios por estación-hora, sin alterar los ZIP.
- [x] Crear agregados de Power BI por estación-hora, localidad y ranking; refrescar y guardar el `.pbix` local de ocho páginas. Se inspeccionaron las ocho páginas exportadas a PDF y se guardaron los ajustes del mapa y la dispersión territorial a las 23:13. Ver `docs/tablero_powerbi_2026-11-24.md`.
- [x] Verificar en Power BI que ambas curvas de la primera página se calculan con `powerbi_tabla_integrada_provisional` y las mismas fechas 18–23/11. La curva de entradas usa todas las validaciones de esa tabla, incluidas las que no tienen paso comparable; la razón de entradas por paso usa solo filas comparables. No tienen exactamente la misma población.
- [x] Ejecutar controles automatizados de claves, cobertura y sumas en `tests/validar_tablas_powerbi.py`; redactar borrador de hallazgos en `reports/hallazgos_preliminares_2026-11-24.md`.
- [x] Preparar paquete actualizado con `src/empaquetar_tablero.py`: **solo `.pbix` y seis CSV derivados**. Se compartió en Drive con Alejandro y se comprobaron su tamaño, MD5 y carpeta. Los paquetes anteriores quedan aparte y no deben usarse para presentar esta versión.
- [ ] Documentar la procedencia del denominador GTFS del 18/11. El archivo corregido de Alejandro suma 248.283 pasos frente a 235.072 del cálculo anterior; las tablas Power BI ya usan su versión. Una prueba encontró 93,07 % de coincidencias al usar GTFS del 20–22, pero falta confirmar qué archivo usó.
- [ ] Solo si se adopta el piloto GPS: revisar cobertura, sesgos y límites de las capturas `.pb` antes de añadir indicadores operativos.
- [x] Elegir Encuesta Multipropósito 2021 por localidad, agregarla y documentar que describe residentes, no pasajeros individuales. Falta revisar la interpretación final de sus comparaciones.
- [ ] Terminar dashboard: ya contiene pregunta, visualizaciones, una página de advertencias y los datos corregidos del 18–23. La exportación permitió revisar las ocho páginas y se verificó que las medidas de ambas curvas usan la misma tabla de seis fechas. La curva de entradas incluye registros sin paso comparable, a diferencia de la razón de la página 5. Faltan probar filtros interactivos y añadir KPI finales. Los dos mapas renderizan con advertencia de retirada futura del visual actual.
- [x] Redactar un borrador de conclusiones y recomendaciones descriptivas en `reports/conclusiones_provisionales_2026-11-24.md`, sin afirmar causalidad. Falta discusión y aprobación del equipo antes de llamarlas definitivas.
- [ ] Revisar con el equipo el borrador local editable de ocho diapositivas y ensayar la explicación de fuentes, limpieza y cruces; guion en `reports/guion_presentacion_2026-11-24.md`. La presentación no está publicada ni entregada.
- [x] Verificar en Bloque Neón fecha y mecanismo: actividad `Group 7: Proyecto 2`, vence 24/11/2026 a las 23:59, admite archivos y exige pulsar **Enviar** después de cargarlos. A las 23:18 figuraba **No enviado** y con 0 archivos. [Observación directa en Bloque Neón, `db=485930`, 24/11/2026]
- [ ] Publicar los materiales finales autorizados, revisar la entrega con el equipo y enviarla en Bloque Neón antes del cierre. La actividad sigue pendiente hasta ver un comprobante de envío.

Los datos crudos permanecen fuera de Git según `.gitignore`; cada integrante necesita acceso local a las fuentes o a una copia compartida autorizada.
