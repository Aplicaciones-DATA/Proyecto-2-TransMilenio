# Plan de trabajo — Proyecto 2 TransMilenio

## Decisión vigente para el corte del 19 al 23 de noviembre

El equipo cerró su pregunta analítica: **¿cómo varían las entradas registradas frente a los pasos programados entre pico y valle, días hábiles y fines de semana y estaciones de los días comparables, y qué contexto muestran las localidades de esas estaciones?** La elección de la pregunta es una decisión del equipo; no figura como pendiente de aprobación previa del profesor. El objetivo sigue siendo descriptivo. [Decisión directa del usuario el 25/11/2026; pregunta y unidad en `docs/resultados.md`]

Para la nueva versión se **excluye el 18/11/2026** de numeradores, denominadores, gráficos y conclusiones. Sí hay un GTFS local del 18, pero su cálculo produce 235.072 pasos frente a 248.283 del CSV corregido de Alejandro. Como la versión exacta y la regla que generan este último valor no están conciliadas, se marca ese día como **no apto para la comparación final**, sin borrarlo ni decir que no se recolectó. El periodo vigente es **19–23/11/2026**, con tres días hábiles y dos de fin de semana. [Auditoría `docs/auditoria_datos_tablero_2026-11-25.md`; decisión directa del usuario el 25/11/2026]

Los controles filtrados dan **7.252.722 entradas**, **6.353.794 entradas comparables**, **1.063.752 pasos comparables**, **5,97 entradas por paso programado** y **87,61 % de cobertura**. Entre semana, pico/valle es **7,91/6,20**; en fin de semana, **5,62/5,78**. Véase [resultados vigentes](resultados.md). El PBIX de cinco días se refrescó y sus indicadores, títulos y mapas se revisaron localmente. [Datos `datos/procesados/powerbi_tabla_integrada_provisional.csv` y `datos/analisis/` filtrados a 19–23/11; cálculo y revisión local]

### Próximos controles de esta versión

- [x] Cerrar la pregunta analítica y excluir el 18 por discrepancia no conciliada; conservar el incidente documentado.
- [x] Filtrar y comprobar agregados de los cinco días, sin alterar los ZIP originales.
- [x] Refrescar la copia de Power BI y comprobar el periodo, los indicadores principales, títulos y mapas del corte 19–23/11; distinguirla de la versión ya entregada.
- [x] Preparar y revisar visualmente el Word de análisis de gráficos para el corte de cinco días; queda pendiente la discusión de sus conclusiones con el equipo.
- [x] Compartir en Drive el [PBIX actualizado y seis CSV derivados](https://drive.google.com/file/d/1JJ2RuE9qTF57AE5q8ZbDaqOlNWgkDA-o/view?usp=drivesdk) sin publicar los datos crudos en GitHub.
- [ ] Preparar y ensayar con Alejandro la presentación ejecutiva de máximo diez minutos, basada en cifras ya verificadas. El envío oficial anterior no prueba que este nuevo corte se haya entregado.

## Archivo histórico del estado al 25/11/2026, 00:38 (Bogotá)

El texto y el checklist que siguen documentan el **corte anterior 18–23/11** y las acciones de entonces. Se conservan por trazabilidad. Para decisiones, cifras y productos nuevos debe usarse la sección vigente de arriba y `docs/resultados.md`; no reutilizar automáticamente los valores, el PBIX ni las conclusiones históricas de seis días.

La pregunta funcional acordada por el equipo es: **¿cómo varían las entradas registradas frente a los pasos programados entre pico/valle, días hábiles/fines de semana y estaciones de los días comparables, y qué contexto muestran las localidades de esas estaciones?** Esta es una comparación descriptiva de oferta programada y demanda registrada, no de confiabilidad real. El cambio formal de la pregunta original sigue por confirmar con el profesor. [Propuesta original; indicación del usuario; `docs/tablero_powerbi_2026-11-24.md`]

Se integraron los cruces del **18–23/11**, con el 18 corregido de Alejandro. La tabla exploratoria conserva 26.060 claves de nueve fechas; la integrada para comparar oferta y demanda contiene **17.503 filas de seis fechas**. La prueba automatizada pasó. Las ocho páginas del `.pbix` se exportaron a PDF y se revisaron visualmente; el archivo se guardó de nuevo a las 23:13 tras aclarar los nombres y agregaciones territoriales. A las **23:42:44** se guardó y verificó otra corrección: la página «Método y límites» ahora dice pico 06–08 y 16–18, valle 09–15, y presenta como pendiente la versión exacta del GTFS del 18. El mapa sigue mostrando una advertencia de Power BI sobre la futura retirada de ese tipo de visual. Se compartió en Drive un [paquete corregido](https://drive.google.com/file/d/1uATsLaI8TT9PX5-JWtruiwCs9yBfE2IM/view?usp=drivesdk) con **solo el `.pbix` y seis CSV derivados**; los anteriores quedan como versiones históricas. El [PBIX individual](https://drive.google.com/file/d/19VzJ5pWkxH7cgR9f6f4pnA8jUefL7r7m/view?usp=drivesdk) tiene permiso editor directo para Alejandro; su permiso sobre la carpeta sigue siendo lector y Power BI Desktop no permite coedición simultánea. El 24/11 tiene GTFS y capturas GTFS-RT en Drive, pero sus validaciones oficiales no figuraban en el portal al último chequeo; no se añaden al cociente. La cobertura de entradas comparables es **87,62 %**. [Datos `datos/analisis/cobertura_diaria.csv`; `tests/validar_tablas_powerbi.py`; inspección visual local; `docs/tablero_powerbi_2026-11-24.md`; portal oficial]

**Estado posterior a la entrega:** Alejandro envió la actividad en Bloque Neón el 24/11/2026 a las 23:58 (recibo 5080470, antes del cierre de 23:59). El envío mostró un ZIP de 255,91 KB y enlaces al repositorio, al PBIX y a las diapositivas; no se ha confirmado que ese ZIP incluya los seis CSV del paquete compartido. Se preparó una copia local posterior a la entrega, `outputs/TransMilenio_postentrega_2026-11-25_filtros.pbix`, con filtros de fecha y tipo de día, y una página de indicadores; esta copia no forma parte de la entrega oficial. Siguen pendientes la procedencia exacta del denominador GTFS del 18, la discusión de conclusiones con el equipo y la confirmación formal de la pregunta con el profesor. [Recibo de Bloque Neón 5080470; copia local del PBIX; auditoría local]

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
- [x] Crear agregados de Power BI por estación-hora, localidad y ranking; refrescar y guardar el `.pbix` local de ocho páginas. Se inspeccionaron las ocho páginas exportadas a PDF; los ajustes territoriales se guardaron a las 23:13 y la leyenda metodológica se corrigió y verificó en el `.pbix` guardado a las 23:42:44. Ver `docs/tablero_powerbi_2026-11-24.md`.
- [x] Verificar en Power BI que ambas curvas de la primera página se calculan con `powerbi_tabla_integrada_provisional` y las mismas fechas 18–23/11. La curva de entradas usa todas las validaciones de esa tabla, incluidas las que no tienen paso comparable; la razón de entradas por paso usa solo filas comparables. No tienen exactamente la misma población.
- [x] Ejecutar controles automatizados de claves, cobertura y sumas en `tests/validar_tablas_powerbi.py`; redactar borrador de hallazgos en `reports/hallazgos_preliminares_2026-11-24.md`.
- [x] Preparar paquete corregido con `src/empaquetar_tablero.py`: **solo `.pbix` y seis CSV derivados**. El [ZIP de las 23:43](https://drive.google.com/file/d/1uATsLaI8TT9PX5-JWtruiwCs9yBfE2IM/view?usp=drivesdk) se compartió en Drive y se comprobaron su tamaño, MD5 y carpeta. El [PBIX individual](https://drive.google.com/file/d/19VzJ5pWkxH7cgR9f6f4pnA8jUefL7r7m/view?usp=drivesdk) se verificó y se otorgó permiso editor directo a `s.rojasm23@uniandes.edu.co`. Los paquetes anteriores son históricos y no deben usarse para presentar esta versión.
- [ ] Documentar la procedencia del denominador GTFS del 18/11. El archivo corregido de Alejandro suma 248.283 pasos frente a 235.072 del cálculo anterior; las tablas Power BI ya usan su versión. Una prueba encontró 93,07 % de coincidencias al usar GTFS del 20–22, pero falta confirmar qué archivo usó.
- [ ] Solo si se adopta el piloto GPS: revisar cobertura, sesgos y límites de las capturas `.pb` antes de añadir indicadores operativos.
- [x] Elegir Encuesta Multipropósito 2021 por localidad, agregarla y documentar que describe residentes, no pasajeros individuales. Falta revisar la interpretación final de sus comparaciones.
- [x] Probar filtros interactivos y añadir KPI en una copia local posterior a la entrega: `outputs/TransMilenio_postentrega_2026-11-25_filtros.pbix`. Las páginas «Entradas y oferta» e «Indicadores» filtran por fecha y tipo de día. Se verificó que los filtros cambian las curvas y los indicadores y que la vista completa se puede restaurar. La nueva página muestra entradas totales (9.205.097), pasos programados (1.312.035), entradas comparables (8.065.892), entradas por paso comparable (6,15) y cobertura de entradas (87,62 %). Es una mejora local no incluida en el envío oficial; los dos mapas conservan la advertencia de retirada futura del visual actual.
- [x] Redactar un borrador de conclusiones y recomendaciones descriptivas en `reports/conclusiones_provisionales_2026-11-24.md`, sin afirmar causalidad. Falta discusión y aprobación del equipo antes de llamarlas definitivas.
- [ ] Revisar con el equipo el borrador editable de ocho diapositivas y ensayar la explicación de fuentes, limpieza y cruces; guion en `reports/guion_presentacion_2026-11-24.md`. La presentación se compartió en Drive con Alejandro y su enlace figura en el envío oficial; no hay confirmación de ensayo ni de revisión final por el equipo.
- [x] Verificar en Bloque Neón fecha y mecanismo: actividad `Group 7: Proyecto 2`, vence 24/11/2026 a las 23:59, admite archivos y exige pulsar **Enviar** después de cargarlos. A las 23:18 figuraba **No enviado** y con 0 archivos. [Observación directa en Bloque Neón, `db=485930`, 24/11/2026]
- [x] Verificar el envío oficial por Alejandro en Bloque Neón: recibido el 24/11/2026 a las 23:58 con ID 5080470, antes del cierre de las 23:59. El recibo muestra un ZIP de 255,91 KB y enlaces al repositorio, PBIX y diapositivas. No se ha confirmado que el ZIP oficial incluya los seis CSV del paquete compartido. La calificación sigue pendiente.

Los datos crudos permanecen fuera de Git según `.gitignore`; cada integrante necesita acceso local a las fuentes o a una copia compartida autorizada.
