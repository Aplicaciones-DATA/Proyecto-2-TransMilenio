# Plan de trabajo — Proyecto 2 TransMilenio

## Pregunta que sí podemos responder ahora

**¿En qué estaciones troncales y horas se registran más entradas durante los días disponibles?** Se responde con las validaciones diarias. La unidad es la validación, no el pasajero único. El notebook `02_demanda_observada_estaciones.ipynb` procesa los ZIP por bloques y genera una tabla por fecha, hora y estación.

## Preguntas para la siguiente etapa

1. **¿Cuántos viajes se programan por ruta, estación y franja en una fecha concreta?** Requiere `calendar.txt`, `calendar_dates.txt` y `stop_times.txt` de una versión GTFS compatible con esa fecha.
2. **¿Dónde coinciden alta demanda registrada y menor oferta programada?** Ya hay un cruce piloto para el 16 y el 18 de noviembre, con cerca del 88 % de las validaciones comparables en cada día. Falta auditar las estaciones no emparejadas y ampliar fechas. Es una señal de presión sobre la oferta, **no ocupación real**.
3. **¿Cómo cambian los patrones entre días y franjas?** Requiere suficientes días comparables y verificar que cada ZIP cubra el día completo.
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
- [ ] Crear y verificar tabla de correspondencia de estaciones; registrar las no emparejadas.
- [x] Integrar oferta programada y demanda observada solo en filas con fechas y estaciones comparables; resultados piloto e informe en `reports/informe_alejandro_cruce_fechas.md`.
- [ ] Solo si se adopta el piloto GPS: revisar cobertura, sesgos y límites de las capturas `.pb` antes de añadir indicadores operativos.
- [ ] Si se usa contexto socioeconómico, elegir fuente, año y geografía adecuados; documentar que es información agregada y no de pasajeros individuales.
- [ ] Construir dashboard con pregunta, fuentes, filtros, indicadores válidos y advertencias.
- [ ] Redactar conclusiones y recomendaciones acordes con lo que muestran los datos, sin afirmar causalidad.
- [ ] Preparar presentación de máximo 10 minutos y ensayar la explicación de fuentes, limpieza y cruces.
- [ ] Verificar con Bloque Neón/profesor la fecha y el mecanismo oficial de entrega; publicar los enlaces finales a tiempo.

Los datos crudos permanecen fuera de Git según `.gitignore`; cada integrante necesita acceso local a las fuentes o a una copia compartida autorizada.
