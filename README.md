# Proyecto 2 — Entradas y oferta programada de TransMilenio

Proyecto de **Aplicaciones en Ciencia de Datos (DATA-1002)**, Universidad de los Andes. La propuesta está fechada el **11 de noviembre de 2026** y señala que el tema y la fuente principal fueron aprobados por el profesor; esa aprobación se consigna aquí como información de la propuesta, no como una verificación independiente. Profesores mencionados: **Nicolás Mejía Martínez** y **Nicolás Felipe Suárez Ariza**.

**Equipo:** Chiudacchang Collazos y Alejandro Rojas. La distribución de tareas se coordina entre ambos.

**Estado al 24/11/2026:** hay un [borrador funcional en Power BI Desktop](docs/tablero_powerbi_2026-11-24.md) con ocho páginas, tablas reproducibles y datos comparables del 16 y 18–23 de noviembre. El archivo `.pbix` está guardado localmente en `outputs/` y **no está publicado ni entregado**. Los ZIP originales no se suben al repositorio. El conteo de pasos de Alejandro y el cálculo previo discrepan en algunas claves; por ello las razones del tablero son provisionales hasta acordar la regla. Las validaciones oficiales del 24/11 todavía no estaban disponibles en el portal al último chequeo del 24/11 hacia las 22:02. [Inventario local y `src/integrar_localidades_powerbi.py`; [portal oficial](https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html)]

## Acceso al histórico de datos

El repositorio permite encontrar el histórico, pero los archivos grandes se almacenan en la **carpeta compartida del proyecto en Google Drive**:

- [Abrir todos los datos del proyecto](https://drive.google.com/drive/folders/1ZOasXuot0GN8eZCVPzYohVKkKF73UT4z)
- [GTFS diario](https://drive.google.com/drive/folders/1hMytx7v1RhFU9_6_hH5dFCz4cq79T0ZN): archivos de oferta programada.
- [Capturas de tiempo real](https://drive.google.com/drive/folders/121V5T0E_hdcwRwBGJb0WFIQGq5BnJxo7): posiciones, actualizaciones de viajes y alertas guardadas por el recolector.

Cada sección se organiza en subcarpetas `AAAA-MM-DD`. Las nuevas capturas aparecen allí tras cada carga correcta del programa; no hace falta actualizar este enlace. Para abrirlas, inicia sesión en Drive con la cuenta a la que se dio acceso. **El enlace es visible públicamente en GitHub, pero los archivos de Drive solo son accesibles para las personas autorizadas**. El permiso de lectura permite consultar y descargar todo el histórico sin modificarlo.

Los archivos `.pb.gz` son capturas Protobuf comprimidas sin pérdida. El repositorio conserva el código y la documentación; no duplica aquí todos los `.pb.gz` ni los ZIP diarios por su volumen. Esta carpeta de Drive contiene el GTFS y las capturas del piloto; las validaciones descargadas por separado todavía no forman parte de ella.

## Resumen y propósito

La **propuesta original** buscaba evaluar la confiabilidad del servicio y relacionarla con el contexto social. El alcance funcional actual es más acotado: describir dónde y cuándo se registran entradas frente a los **pasos de bus programados**, comparando franjas pico/valle y tipos de día. Añadimos contexto agregado por localidad de la Encuesta Multipropósito 2021 sin atribuirlo a pasajeros específicos. El tablero sirve para orientar preguntas operativas posteriores; no demuestra retrasos, ocupación ni efecto racimo. [Propuesta original; `docs/tablero_powerbi_2026-11-24.md`]

TransMilenio transporta diariamente a muchas personas en Bogotá. Las demoras, los intervalos irregulares y los buses que llegan en grupo pueden causar pérdidas de tiempo, llegadas tarde y hacinamiento. Las consecuencias pueden ser más graves para quienes tienen pocas alternativas de transporte, incluidos hogares de menores ingresos que viven lejos de sus lugares de trabajo o estudio. La decisión que se busca apoyar es **dónde reforzar primero el servicio**, basándose en evidencia y no solo en intuición. La propuesta considera oportuno el trabajo por la disponibilidad de datos abiertos de operación.

## Pregunta analítica vigente para el tablero

> ¿Cómo varían las entradas registradas frente a los pasos de bus programados entre horas pico y valle, días hábiles y fines de semana, y estaciones troncales de los días comparables? ¿Qué contexto territorial muestran las localidades donde se encuentran esas estaciones?

Esta formulación es **exploratoria** y debe validarse con el profesor si reemplaza formalmente la pregunta aprobada. La relación `entradas / pasos programados` no es ocupación de buses ni una medida de puntualidad. [Cálculo y límites en `docs/tablero_powerbi_2026-11-24.md`]

## Pregunta de la propuesta original (pendiente de contraste)

> ¿Qué troncales y zonas de Bogotá reciben el servicio menos confiable de TransMilenio, y qué población depende de ellas?

Preguntas de apoyo:

1. ¿Cuánto se aleja la operación real de la programada en cada troncal?
2. ¿Dónde aparece con mayor frecuencia el **efecto racimo** (varios buses juntos y después un intervalo largo sin servicio)?
3. ¿Coinciden las zonas con peor servicio con las de menores ingresos o mayor dependencia del transporte público?

### Historia del cambio de alcance

La pregunta anterior pertenece a la propuesta original. En el primer examen todavía no había un histórico verificado de paso real de buses ni una correspondencia completa entre los `trip_id` de posiciones y del GTFS. Después se inició un piloto de recolección; su cobertura y calidad aún deben comprobarse. Por eso el equipo trabaja primero con entradas observadas y oferta **programada**, no con un supuesto indicador de confiabilidad real.

La primera comparación funcional usa GTFS estático diario, validaciones de entrada por estación y hora, correspondencia estación-localidad y agregados sociodemográficos por localidad. La comparación es una señal descriptiva de relación entre entradas y oferta **programada**, no una medida de puntualidad, ocupación real o discriminación. El [notebook inicial](notebooks/01_exploracion_oferta_programada.ipynb) explora rutas y viajes; el [documento del tablero](docs/tablero_powerbi_2026-11-24.md) explica los datos ya integrados. Para abrir el borrador en otro equipo, usa la [guía de traslado](docs/abrir_tablero_en_otro_equipo.md); el `.pbix` y los CSV derivados no están publicados en GitHub.

Las descargas locales y sus huellas se documentan en [el registro de descargas](docs/registro_descargas.md). Los archivos diarios y las capturas `.pb` no se publican en este repositorio.

## Fuentes utilizadas en la versión funcional

| Fuente | Qué aporta | Unión usada | Límite |
|---|---|---|---|
| [Validaciones troncales oficiales](https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html) | Entradas registradas por fecha, hora y estación | Código de estación extraído y hora | No identifica pasajeros únicos ni bus abordado; el 24/11 aún no estaba publicado al último chequeo. |
| GTFS estático diario de TransMilenio | Llegadas **programadas** y coordenadas de estaciones | Fecha de servicio, estación y hora | No demuestra qué bus pasó realmente; 14–15/11 sin GTFS emparejado. |
| [Encuesta Multipropósito 2021](https://datosabiertos.bogota.gov.co/dataset/encuesta-multiproposito-2021-sdp/resource/b3fd892e-b9f9-4f34-ac22-6cc50612eac9) | Pobreza monetaria y respuestas de uso de TransMilenio para trabajo y estudio **de residentes** | Agregado por localidad de la estación | Es de 2021 y no permite describir individualmente a los pasajeros de 2026. |
| Tabla de estación-localidad de Alejandro | Código de localidad asignado a 133 de 151 estaciones | `estacion_gtfs` | Su cálculo de pasos difiere del previo; solo se usa su correspondencia territorial. |

La propuesta original priorizaba históricos de operación y un cruce por UPZ. La integración funcional usa localidad porque la encuesta tiene UPZ agrupadas y el mapa aún no valida una unión directa a las 112 UPZ. El piloto de capturas GTFS-Realtime permanece como línea separada para estudiar posiciones de buses cuando se comprueben cobertura e identificadores. [Fuentes y limitaciones en `docs/fuentes_socioeconomicas.md` y `docs/tablero_powerbi_2026-11-24.md`]

Los originales se almacenan fuera de Git y su procedencia se documenta en [docs/fuentes.md](docs/fuentes.md), [docs/fuentes_socioeconomicas.md](docs/fuentes_socioeconomicas.md) y [docs/registro_descargas.md](docs/registro_descargas.md). La [auditoría de cobertura](docs/auditoria_cobertura_estaciones_2026-11-24.md) identifica las 18 estaciones sin localidad, 1.139.205 entradas sin paso comparable y la exclusión de Usme del mapa; aún falta resolver la discrepancia de pasos.

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

1. **Entender el problema:** precisar población afectada, decisión y pregunta analítica.
2. **Comprender las fuentes:** revisar unidad de análisis, periodo, cobertura, calidad, variables, limitaciones y llaves.
3. **Preparar e integrar:** limpiar faltantes e inconsistencias, normalizar nombres de estaciones y rutas, construir variables y unir fuentes. Se revisarán cardinalidad, registros sin correspondencia y duplicaciones. Los datos crudos no se modificarán; cada decisión quedará en [docs/bitacora_limpieza.md](docs/bitacora_limpieza.md).
4. **Explorar y analizar:** calcular estadísticas descriptivas, agregar, comparar troncales y zonas y visualizar.
5. **Construir y comunicar:** presentar pregunta, indicadores, hallazgos, límites y recomendaciones en el dashboard.

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
| Alejandro Rojas | Tabla de comparación del 18/11 con asignación de localidad por estación; su criterio de conteo de pasos debe conciliarse con el previo. |
| Ambos | Validar la pregunta con el profesor, revisar hallazgos, preparar presentación y entrega. |

La tabla registra lo que se encontró, no asigna responsabilidad exclusiva ni afirma que el proyecto esté terminado.

## Criterios éticos y límites de interpretación

- **Equidad:** poco uso no implica poca necesidad; podría ser consecuencia de un mal servicio. No usar ese dato de forma automática para reducir la oferta.
- **Cobertura desigual:** si faltan registros en algunas zonas, medir y reportar la cobertura antes de compararlas.
- **Personas detrás de los datos:** trabajar con agregados por ruta, troncal y zona; no evaluar conductores ni vehículos individuales.
- **Alcance de las conclusiones:** describir solo los periodos y lugares cubiertos, sin generalizar más allá. Mostrar esta limitación en el dashboard.
- **Procedencia y licencias:** usar fuentes oficiales con licencia identificada y citar cada una en el repositorio.

## Riesgos y alternativas

| Riesgo | Plan B propuesto |
|---|---|
| Los históricos no tienen detalle por bus. | Calcular indicadores agregados por ruta y troncal con lo disponible. |
| Las fuentes de operación real y GTFS usan identificadores distintos. | Intentar nombres normalizados de estaciones o coordenadas; validar la correspondencia. |
| No es viable unir la fuente socioeconómica por UPZ. | Trabajar por localidad o estudiar la Encuesta de Movilidad 2023 como alternativa. |
| La carga supera la capacidad de dos personas. | Completar primero el núcleo mínimo: tres fuentes integradas, indicadores principales y dashboard. |

## Plan de trabajo

1. **Fuentes:** descargar las tres bases, revisar campos, cobertura y licencias; definir llaves.
2. **Preparación e integración:** limpiar, normalizar, unir, comprobar cardinalidad y calcular primeros indicadores.
3. **Análisis y dashboard:** explorar, comparar troncales y zonas y construir una primera versión.
4. **Comunicación:** formular recomendaciones, ajustar el dashboard, preparar y ensayar la presentación.

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

Esta estructura sigue el esquema de reproducibilidad y organización tipo Cookiecutter enseñado en clase: datos crudos separados de los procesados, notebooks secuenciales, código reutilizable, resultados, reportes y dependencias. Las carpetas vacías contienen `.gitkeep` para que Git pueda conservarlas. Los datos crudos y procesados se excluyen del repositorio público **hasta verificar su licencia y pertinencia**; los archivos originales siempre se conservan sin modificaciones.

## Referencias indicadas en la propuesta

- Alcaldía de Bogotá (2026), «Datos abiertos en tiempo real: TransMilenio conecta la operación del sistema con la tecnología de Bogotá» (`bogota.gov.co`).
- Datos Abiertos Bogotá, sección TransMilenio (`datosabiertos.bogota.gov.co/organization/transmilenio`).
- TransMilenio S. A., «GTFS Estáticos 2025-11-25» (`datosabiertos-transmilenio.hub.arcgis.com`).
- Secretaría Distrital de Planeación, Encuesta Multipropósito 2021 (`datosabiertos.bogota.gov.co`).
- Datos Abiertos Bogotá, límites de Unidades de Planeamiento Zonal (`datosabiertos.bogota.gov.co`).
- Universidad de los Andes (2026), «Proyecto 2: Profundización e Impacto», DATA-1002.

Estas referencias se trasladan de la propuesta; los enlaces precisos, la versión descargada y las licencias están **pendientes de verificación** en `docs/fuentes.md`.
