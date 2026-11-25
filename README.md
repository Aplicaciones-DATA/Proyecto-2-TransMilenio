# Proyecto 2 — Entradas y oferta programada de TransMilenio

Hicimos este proyecto para **Aplicaciones en Ciencia de Datos (DATA-1002)** en la Universidad de los Andes, con el profesor **Nicolás Mejía Martínez**. Nuestra propuesta es del **11 de noviembre de 2026**.

**Equipo:** Chiudacchang Collazos Trujillo y Alejandro Rojas.

**Estado al 24/11/2026:** Alejandro publicó la integración corregida de los días 18–23 en [resultados y reproducción](docs/resultados.md) y [resúmenes agregados](datos/analisis/). Hay un [borrador de ocho páginas en Power BI](docs/tablero_powerbi_2026-11-24.md) y un [paquete en el Drive compartido](https://drive.google.com/file/d/1NON8xecYhW7OjgmT4lut-XOqgE-7sOsr/view?usp=drivesdk), pero el `.pbix` aún usa el cálculo previo del 18 y franjas distintas: **sus cifras no deben presentarse como resultados finales** hasta actualizarlo. Los ZIP originales no están en GitHub. La actividad aún no se había enviado en Bloque Neón al último chequeo.

## Acceso al histórico de datos

Guardamos los archivos grandes en la carpeta compartida de Google Drive. Desde aquí se puede abrir el histórico del proyecto.

- [Abrir todos los datos del proyecto](https://drive.google.com/drive/folders/1ZOasXuot0GN8eZCVPzYohVKkKF73UT4z)
- [GTFS diario](https://drive.google.com/drive/folders/1hMytx7v1RhFU9_6_hH5dFCz4cq79T0ZN): archivos de oferta programada.
- [Capturas de tiempo real](https://drive.google.com/drive/folders/121V5T0E_hdcwRwBGJb0WFIQGq5BnJxo7): posiciones, actualizaciones de viajes y alertas guardadas por el recolector.

Organizamos los archivos por fecha en carpetas `AAAA-MM-DD`. Cada vez que el recolector termina una carga, las capturas quedan en la carpeta del día. Para consultar o descargar los archivos hace falta tener acceso al Drive compartido.

En Drive dejamos el GTFS y las capturas del piloto en formato `.pb.gz`. Descargamos las validaciones por separado. En el repositorio dejamos el código y la documentación para mantener liviana la descarga.

## Resumen y propósito

La **propuesta original** buscaba evaluar la confiabilidad del servicio. El alcance funcional es más acotado: comparar entradas registradas con **pasos de bus programados**, por estación, franja y tipo de día. El contexto de la Encuesta Multipropósito 2021 se agrega por localidad; no describe a los pasajeros individuales. Esto orienta dónde investigar el servicio, pero no demuestra retrasos, ocupación ni efecto racimo.

Nos interesa el tema porque las demoras y los intervalos irregulares afectan la rutina de quienes dependen de TransMilenio para llegar al trabajo o al estudio, sobre todo si viven lejos y tienen pocas alternativas de transporte. Con los datos abiertos buscamos aportar evidencia para decidir dónde revisar primero el servicio.

## Preguntas del proyecto

> **Pregunta principal.** ¿En qué estaciones y horas se registran más entradas frente a los buses que deberían pasar según el horario, y cómo cambia esto entre horas pico y horas de menor afluencia?

> **Pregunta de contexto.** ¿Qué características sociales y de movilidad tienen las localidades donde se ubican esas estaciones?

Para la primera pregunta contamos todas las entradas registradas, cualquiera que sea el motivo del viaje. Con «buses que deberían pasar» nos referimos a los pasos programados en el GTFS. Antes de comparar pico y valle, vamos a fijar los rangos y a asignar las observaciones según la hora.

Para la segunda usamos la [Encuesta Multipropósito 2021](https://datosabiertos.bogota.gov.co/dataset/encuesta-multiproposito-2021-sdp) como contexto de las localidades. Nos interesan los ingresos, las condiciones de los hogares y la movilidad. Si presentamos desplazamientos al trabajo y al estudio, mostramos cada grupo por separado y dejamos claros la población, los pesos y el denominador. Las cifras de la encuesta describen a los residentes de las localidades.

Verificamos la unión por localidad. En el análisis corregido se propusieron pico 06:00–08:59 y 16:00–18:59, valle 09:00–15:59 y otras horas; el equipo debe confirmar estos rangos. La relación `entradas / pasos programados` no mide ocupación ni puntualidad. El piloto de tiempo real sigue por separado. Las descargas y huellas constan en [el registro](docs/registro_descargas.md).

### Preguntas de la propuesta inicial

> ¿Qué troncales y zonas de Bogotá reciben el servicio menos confiable de TransMilenio, y qué población depende de ellas?

En la propuesta también nos preguntamos lo siguiente.

1. ¿Cuánto se aleja la operación real de la programada en cada troncal?
2. ¿Dónde aparece con mayor frecuencia el **efecto racimo** (varios buses juntos y después un intervalo largo sin servicio)?
3. ¿Coinciden las zonas con peor servicio con las de menores ingresos o mayor dependencia del transporte público?

### Historia del cambio de alcance

La pregunta anterior pertenece a la propuesta original. En el primer examen todavía no había un histórico verificado de paso real de buses ni una correspondencia completa entre los `trip_id` de posiciones y del GTFS. Después se inició un piloto de recolección; su cobertura y calidad aún deben comprobarse. Por eso el equipo trabaja primero con entradas observadas y oferta **programada**, no con un supuesto indicador de confiabilidad real.

La primera comparación funcional usa GTFS estático diario, validaciones por estación y hora, correspondencia estación-localidad y agregados sociodemográficos por localidad. Es una señal descriptiva de oferta **programada**, no una medida de puntualidad, ocupación real o discriminación. El [notebook inicial](notebooks/01_exploracion_oferta_programada.ipynb) explora rutas y viajes; el [documento del tablero](docs/tablero_powerbi_2026-11-24.md) explica el borrador. Para abrirlo en otro equipo, usa la [guía de traslado](docs/abrir_tablero_en_otro_equipo.md).

Las descargas locales y sus huellas se documentan en [el registro de descargas](docs/registro_descargas.md). Los archivos diarios y las capturas `.pb` no se publican en este repositorio.

## Fuentes de datos

| Fuente | Qué aporta | Unión usada | Límite |
|---|---|---|---|
| [Validaciones troncales de TransMilenio](https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html) | Entradas registradas | Fecha, estación y hora | El cruce verificado cubre del 18 al 23 de noviembre de 2026. |
| GTFS estático de TransMilenio | **Qué debía pasar:** rutas, paradas con coordenadas y frecuencias programadas | Ruta, viaje y parada | Puede no recoger cambios recientes por obras. |
| Encuesta Multipropósito 2021 de la Secretaría Distrital de Planeación y límites de localidades | Ingresos, condiciones de los hogares y movilidad | Estaciones asignadas a localidad para agregar contexto territorial | La encuesta es de 2021 y describe a los residentes de las localidades. |

Conservamos las capturas GTFS-Realtime del piloto en Drive. Describimos las fuentes y sus límites en [docs/fuentes.md](docs/fuentes.md).

Los originales están fuera de Git. La [auditoría de cobertura](docs/auditoria_cobertura_estaciones_2026-11-24.md) explica las estaciones sin localidad y las entradas sin paso comparable; las cifras del tablero previo deben recalcularse con la corrección del 18.

## Indicadores del tablero actual y límites

| Indicador | Qué muestra |
|---|---|
| Validaciones registradas | Cuántas entradas hay por fecha, hora y estación; no personas únicas. |
| Pasos programados | Cuántas llegadas figuran en el GTFS; no llegadas reales. |
| Entradas por paso programado | Suma de entradas comparables dividida por suma de pasos de esas mismas filas. No es ocupación ni puntualidad. |
| Cobertura de comparación | Proporción de validaciones que cuentan con paso programado emparejado; varía por fecha y estación. |
| Contexto territorial | Indicadores de residentes de la localidad donde se ubica la estación, no perfil de pasajeros. |

Cumplimiento real, regularidad, efecto racimo y velocidad son preguntas de la **propuesta original**, pendientes de un histórico de posiciones y un emparejamiento verificado con los viajes. No aparecen como hechos calculados en el tablero actual. [Propuesta original; `docs/tablero_powerbi_2026-11-24.md`]

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

Bloque Neón fue revisado de nuevo el 24/11 hacia las 22:25: la actividad **Group 7: Proyecto 2** cierra el **24/11/2026 a las 23:59**, seguía como **No enviado** y pedía cargar archivos y después pulsar **Enviar**. El equipo se fijó las 23:00 como meta interna. Este repositorio, por sí solo, no constituye la entrega. [Observación directa en la actividad de Bloque Neón, `db=485930`; memoria académica: `src-bloque-neon-data-proyecto-2-2026-11-23`]

## Equipo y trabajo actual

| Integrante | Aporte documentado |
|---|---|
| Chiudacchang Collazos | Recolección y cruce inicial; borrador de Power BI, auditoría y documentación. |
| Alejandro Rojas | Base corregida del 18/11, integración de contexto territorial, resúmenes y documentación de resultados. |
| Ambos | Exploración, implicaciones éticas, recomendaciones y presentación ejecutiva. |

La tabla registra los aportes observados; no afirma que el proyecto esté terminado.

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
