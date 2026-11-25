# Proyecto 2 — Confiabilidad del servicio de TransMilenio

Hicimos este proyecto para **Aplicaciones en Ciencia de Datos (DATA-1002)** en la Universidad de los Andes, con el profesor **Nicolás Mejía Martínez**. Nuestra propuesta es del **11 de noviembre de 2026**.

Somos Chiudacchang Collazos Trujillo y Sergio Rojas.

## Acceso al histórico de datos

Guardamos los archivos grandes en la carpeta compartida de Google Drive. Desde aquí se puede abrir el histórico del proyecto.

- [Abrir todos los datos del proyecto](https://drive.google.com/drive/folders/1ZOasXuot0GN8eZCVPzYohVKkKF73UT4z)
- [GTFS diario](https://drive.google.com/drive/folders/1hMytx7v1RhFU9_6_hH5dFCz4cq79T0ZN): archivos de oferta programada.
- [Capturas de tiempo real](https://drive.google.com/drive/folders/121V5T0E_hdcwRwBGJb0WFIQGq5BnJxo7): posiciones, actualizaciones de viajes y alertas guardadas por el recolector.

Organizamos los archivos por fecha en carpetas `AAAA-MM-DD`. Cada vez que el recolector termina una carga, las capturas quedan en la carpeta del día. Para consultar o descargar los archivos hace falta tener acceso al Drive compartido.

En Drive dejamos el GTFS y las capturas del piloto en formato `.pb.gz`. Descargamos las validaciones por separado. En el repositorio dejamos el código y la documentación para mantener liviana la descarga.

## Resumen y propósito

Comparamos las entradas registradas en TransMilenio con los pasos de bus que figuran en el horario. Queremos mostrar en el dashboard en qué estaciones y horas se registran más validaciones por paso programado, para saber dónde vale la pena mirar con más detalle. Desde la propuesta pensamos el tablero para analizar el servicio. Para consultar rutas y horarios, los pasajeros ya cuentan con Google Maps, Moovit y la aplicación oficial.

Nos interesa el tema porque las demoras y los intervalos irregulares afectan la rutina de quienes dependen de TransMilenio para llegar al trabajo o al estudio, sobre todo si viven lejos y tienen pocas alternativas de transporte. Con los datos abiertos buscamos aportar evidencia para decidir dónde revisar primero el servicio.

## Preguntas del proyecto

> **Pregunta principal.** ¿En qué estaciones y horas se registran más entradas frente a los buses que deberían pasar según el horario, y cómo cambia esto entre horas pico y horas de menor afluencia?

> **Pregunta de contexto.** ¿Qué características sociales y de movilidad tienen las localidades donde se ubican esas estaciones?

Para la primera pregunta contamos todas las entradas registradas, cualquiera que sea el motivo del viaje. Con «buses que deberían pasar» nos referimos a los pasos programados en el GTFS. Antes de comparar pico y valle, vamos a fijar los rangos y a asignar las observaciones según la hora.

Para la segunda usamos la [Encuesta Multipropósito 2021](https://datosabiertos.bogota.gov.co/dataset/encuesta-multiproposito-2021-sdp) como contexto de las localidades. Nos interesan los ingresos, las condiciones de los hogares y la movilidad. Si presentamos desplazamientos al trabajo y al estudio, mostramos cada grupo por separado y dejamos claros la población, los pesos y el denominador. Las cifras de la encuesta describen a los residentes de las localidades.

Verificamos la unión por localidad. Para explorar pico y valle usamos unos rangos iniciales que el equipo debe confirmar antes de la entrega. Empezamos un piloto con capturas en tiempo real y seguimos revisando su cobertura. Anotamos los archivos que descargamos y sus huellas en [el registro de descargas](docs/registro_descargas.md).

### Preguntas de la propuesta inicial

> ¿Qué troncales y zonas de Bogotá reciben el servicio menos confiable de TransMilenio, y qué población depende de ellas?

En la propuesta también nos preguntamos lo siguiente.

1. ¿Cuánto se aleja la operación real de la programada en cada troncal?
2. ¿Dónde aparece con mayor frecuencia el **efecto racimo** (varios buses juntos y después un intervalo largo sin servicio)?
3. ¿Coinciden las zonas con peor servicio con las de menores ingresos o mayor dependencia del transporte público?

## Fuentes de datos

| Fuente | Qué responde y contenido esperado | Integración prevista | Límite actual |
|---|---|---|---|
| [Validaciones troncales de TransMilenio](https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html) | Entradas registradas | Fecha, estación y hora | El cruce verificado cubre del 18 al 23 de noviembre de 2026. |
| GTFS estático de TransMilenio | **Qué debía pasar:** rutas, paradas con coordenadas y frecuencias programadas | Ruta, viaje y parada | Puede no recoger cambios recientes por obras. |
| Encuesta Multipropósito 2021 de la Secretaría Distrital de Planeación y límites de localidades | Ingresos, condiciones de los hogares y movilidad | Estaciones asignadas a localidad para agregar contexto territorial | La encuesta es de 2021 y describe a los residentes de las localidades. |

Conservamos las capturas GTFS-Realtime del piloto en Drive. Describimos las fuentes y sus límites en [docs/fuentes.md](docs/fuentes.md).

## Indicadores para el dashboard

| Indicador | Pregunta sencilla |
|---|---|
| Validaciones | ¿Cuántas entradas se registraron por estación y hora? |
| Pasos programados | ¿Cuántos pasos de bus están programados según el GTFS? |
| Validaciones por paso programado | ¿Cuántas entradas se registraron por paso programado en las filas comparables? |
| Cobertura del cruce | ¿Qué proporción de las validaciones pudo cruzarse con la programación? |

## Metodología

1. Definimos la pregunta y qué decisión queremos apoyar.
2. Revisamos qué mide cada fuente, qué fechas cubre y cómo podemos cruzarla con las demás.
3. Preparamos las bases y comprobamos cuántas filas coinciden. Registramos las decisiones en la [bitácora de limpieza](docs/bitacora_limpieza.md).
4. Comparamos los resultados por estación y hora para preparar las visualizaciones.
5. En el dashboard queremos presentar los hallazgos junto con sus límites.

### Cruce verificado

Agrupamos los registros por fecha, estación y hora. Para calcular el indicador usamos las filas en las que encontramos la estación en el GTFS y había pasos programados. Si agrupamos varias estaciones u horas, dividimos el total de validaciones comparables por el total de pasos programados de esas mismas filas.

Del **18 al 23 de noviembre de 2026** pudimos cruzar **8.065.892 de 9.205.097 validaciones (87,62 %)**. Ubicamos **128 de las 132 estaciones comparables** dentro de Bogotá y cruzamos esas localidades con los indicadores de la Encuesta Multipropósito 2021. Para el **24 de noviembre** tenemos los pasos programados y todavía nos falta incorporar las validaciones.

Para repetir el cruce, guardamos los dos ZIP de cada fecha en `registros_diarios/AAAA-MM-DD/`, al lado del repositorio. Con las dependencias instaladas, ejecutamos este comando en PowerShell desde la raíz del proyecto. El ejemplo usa los archivos del 18 y guarda el resultado en `datos/procesados/`.

```powershell
py .\src\comparar_validaciones_gtfs.py 2026-11-18
```

### Resultados del análisis

- Entre semana obtuvimos **8,13 validaciones por paso programado** en las franjas de pico propuestas y **6,28** en valle.
- En ese pico entre semana, **Portal 20 de Julio** registró **81.894 validaciones y 2.357 pasos programados** en las filas comparables, una relación de **34,75**. Es un punto para revisar con observaciones de campo.
- Usamos el contexto de la Encuesta Multipropósito 2021 para comparar las localidades por separado. La encuesta describe a los residentes y el cruce operativo cuenta entradas de estaciones.

En [resultados y reproducción](docs/resultados.md) dejamos las franjas, las fuentes, el comando de integración y el recorrido sugerido para la demostración. Los [resúmenes agregados](datos/analisis/) permiten revisar las cifras.

## Entregables previstos

| Entregable | Contenido |
|---|---|
| **Repositorio público** | Código completo, organización reproducible, procedencia y licencia de cada fuente. |
| **Dashboard operativo** | Pregunta, indicadores, comparaciones, hallazgos y al menos una limitación importante. Debe alimentarse de datos integrados y estar accesible durante la sustentación. |
| **Presentación ejecutiva (máximo 10 minutos)** | Problema, relevancia, pregunta, fuentes, integración, preparación, demostración del dashboard, hallazgos, conclusiones y recomendaciones. |
| **Sustentación** | Explicar de dónde salen los datos, cómo se unieron y qué decisiones de limpieza se tomaron. La propuesta la sitúa en la primera clase de la última semana del semestre. |

Según la propuesta, debemos enviar los enlaces del repositorio, la presentación y el dashboard antes de la medianoche del día anterior a la sustentación. Nos queda por confirmar la fecha oficial.

## Equipo y trabajo propuesto

| Integrante | Responsabilidad principal propuesta |
|---|---|
| Sergio Rojas | Preparar la base de datos y actualizar el repositorio. |
| Chiudacchang Collazos Trujillo | Preparar el dashboard. |
| Ambos | Exploración, implicaciones éticas, recomendaciones y presentación ejecutiva. |

Así nos repartimos el trabajo por ahora.

## Criterios éticos y límites de interpretación

- Si vemos pocas validaciones en una estación, revisamos la cobertura y la oferta antes de sacar conclusiones sobre la necesidad de servicio. Esa cifra por sí sola no basta para recomendar una reducción de la oferta.
- Trabajamos con agregados por estación y hora para cuidar la privacidad de los registros y mantener el análisis centrado en el servicio.
- Limitamos las conclusiones a las fechas y estaciones que pudimos comparar. Para hablar de puntualidad u ocupación necesitaríamos otros datos.
- Citamos las fuentes y registramos sus licencias en el repositorio.

## Riesgos y alternativas

| Riesgo | Plan B propuesto |
|---|---|
| Los históricos no tienen detalle por bus. | Calcular indicadores agregados por ruta y troncal con lo disponible. |
| Las fuentes de operación real y GTFS usan identificadores distintos. | Intentar nombres normalizados de estaciones o coordenadas; validar la correspondencia. |
| No es viable unir la fuente socioeconómica por UPZ. | Trabajar por localidad o estudiar la Encuesta de Movilidad 2023 como alternativa. |
| La carga supera la capacidad de dos personas. | Completar primero el núcleo mínimo: tres fuentes integradas, indicadores principales y dashboard. |

## Plan de trabajo

1. Revisar las fuentes y dejar claras las fechas, licencias y llaves de unión.
2. Revisar el cruce de localidad y agregar fechas cuando tengamos los insumos completos.
3. Confirmar las franjas de pico y valle y actualizar el dashboard.
4. Elegir los hallazgos que vamos a mostrar y ensayar la presentación.

## Organización del repositorio

```text
.
├── README.md                 # Propósito, metodología, alcance y estado
├── .gitignore                # Entornos, cachés y datos no autorizados para publicación
├── requirements.txt          # Dependencias Python, por fijar al empezar el código
├── datos/
│   ├── raw/                  # Copias inmutables de fuentes, si su licencia permite publicarlas
│   └── procesados/           # Resultados derivados y documentados
├── notebooks/                # Exploración y análisis reproducible
├── src/                      # Funciones o scripts reutilizables
├── outputs/                  # Tablas, figuras y archivos generados
├── reports/                  # Presentación y materiales de comunicación
└── docs/
    ├── fuentes.md            # Procedencia, cobertura, licencia y llaves
    └── bitacora_limpieza.md  # Decisiones y efectos de preparación
```

Separamos los datos crudos de los procesados y dejamos el código, los notebooks y la documentación en sus propias carpetas. Usamos `.gitkeep` para que Git conserve las carpetas vacías. Guardamos los originales tal como los descargamos y revisamos la licencia antes de publicar datos.

## Referencias indicadas en la propuesta

- Alcaldía de Bogotá (2026), «Datos abiertos en tiempo real: TransMilenio conecta la operación del sistema con la tecnología de Bogotá» (`bogota.gov.co`).
- Datos Abiertos Bogotá, sección TransMilenio (`datosabiertos.bogota.gov.co/organization/transmilenio`).
- TransMilenio S. A., «GTFS Estáticos 2025-11-25» (`datosabiertos-transmilenio.hub.arcgis.com`).
- Secretaría Distrital de Planeación, Encuesta Multipropósito 2021 (`datosabiertos.bogota.gov.co`).
- Datos Abiertos Bogotá, límites de Unidades de Planeamiento Zonal (`datosabiertos.bogota.gov.co`).
- Universidad de los Andes (2026), «Proyecto 2: Profundización e Impacto», DATA-1002.

Conservamos las referencias de la propuesta y anotamos en `docs/fuentes.md` qué enlaces, versiones y licencias hemos podido verificar.
