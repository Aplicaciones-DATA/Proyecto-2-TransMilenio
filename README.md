# Proyecto 2 — Confiabilidad del servicio de TransMilenio

Proyecto de **Aplicaciones en Ciencia de Datos (DATA-1002)**, Universidad de los Andes. La propuesta está fechada el **11 de noviembre de 2026** y señala que el tema y la fuente principal fueron aprobados por el profesor; esa aprobación se consigna aquí como información de la propuesta, no como una verificación independiente. Profesores mencionados: **Nicolás Mejía Martínez** y **Nicolás Felipe Suárez Ariza**.

**Equipo:** Emanuel [apellido por completar] y [nombre del segundo integrante por completar]. Los nombres y la distribución definitiva deben confirmarse antes de publicar información personal.

## Resumen y propósito

El proyecto asesora al comité directivo de TransMilenio para identificar qué troncales y zonas de Bogotá reciben un servicio menos confiable y qué población depende de ellas. Compara lo que ocurrió con lo programado, relaciona los indicadores con el perfil de los hogares y comunica los resultados en un **dashboard** para priorizar flota, control operativo o infraestructura. No se pretende crear una aplicación para pasajeros; la propuesta señala que Google Maps, Moovit y la aplicación oficial ya cumplen esa función.

TransMilenio transporta diariamente a muchas personas en Bogotá. Las demoras, los intervalos irregulares y los buses que llegan en grupo pueden causar pérdidas de tiempo, llegadas tarde y hacinamiento. Las consecuencias pueden ser más graves para quienes tienen pocas alternativas de transporte, incluidos hogares de menores ingresos que viven lejos de sus lugares de trabajo o estudio. La decisión que se busca apoyar es **dónde reforzar primero el servicio**, basándose en evidencia y no solo en intuición. La propuesta considera oportuno el trabajo por la disponibilidad de datos abiertos de operación.

## Pregunta analítica

> ¿Qué troncales y zonas de Bogotá reciben el servicio menos confiable de TransMilenio, y qué población depende de ellas?

Preguntas de apoyo:

1. ¿Cuánto se aleja la operación real de la programada en cada troncal?
2. ¿Dónde aparece con mayor frecuencia el **efecto racimo** (varios buses juntos y después un intervalo largo sin servicio)?
3. ¿Coinciden las zonas con peor servicio con las de menores ingresos o mayor dependencia del transporte público?

## Fuentes de datos previstas

| Fuente | Qué responde y contenido esperado | Integración prevista | Límite actual |
|---|---|---|---|
| Históricos de operación de TransMilenio en Datos Abiertos Bogotá | **Qué pasó:** registros de la operación real | Ruta, estación o troncal y fecha | La cobertura y el detalle dependen de lo publicado. |
| GTFS estático de TransMilenio | **Qué debía pasar:** rutas, paradas con coordenadas y frecuencias programadas | Ruta, viaje y parada | Puede no recoger cambios recientes por obras. |
| Encuesta Multipropósito 2021 de la Secretaría Distrital de Planeación y límites de UPZ | **A quién le pasa:** estrato, ingreso y características de los hogares por zona | Coordenadas de paradas asignadas a UPZ o localidad | La encuesta es de 2021 y se basa en una muestra. |

La propuesta prioriza los **históricos de Datos Abiertos Bogotá** y descarta construir una recolección propia en tiempo real: el tiempo disponible no alcanza y no se encontró un acceso público activo al feed en tiempo real. La integración propuesta compara operación real y programada por ruta, estación o troncal; después ubica las paradas en su UPZ mediante coordenadas y añade el perfil socioeconómico de esa zona.

**Pendiente antes de fijar la integración:** descargar las tres fuentes, comprobar campos, unidades de análisis, periodos, cobertura, llaves de unión y licencias. Todavía no se afirma que las uniones sean posibles con el nivel de detalle disponible. La procedencia y la licencia verificadas se registrarán en [docs/fuentes.md](docs/fuentes.md).

## Indicadores para el dashboard

| Indicador | Pregunta sencilla |
|---|---|
| Cumplimiento de la operación | ¿Se presta el servicio programado? |
| Regularidad | ¿El tiempo entre buses es estable o errático? |
| Efecto racimo | ¿Con qué frecuencia llegan varios buses juntos y luego ninguno? |
| Velocidad o tiempo de recorrido por tramo | ¿En qué tramos se avanza más despacio? |
| Perfil socioeconómico de la zona | ¿Quién vive y viaja donde el servicio es peor? |

Se espera comparar por **troncal y zona**. La definición y el cálculo exactos de los indicadores dependerán de los campos realmente disponibles en las fuentes históricas.

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

La propuesta indica que el enlace del repositorio, la presentación y el dashboard se envían antes de la medianoche del día anterior a la sustentación. **No se registra aquí una fecha oficial concreta**; se mantiene por confirmar y este repositorio no constituye una entrega.

## Equipo y trabajo propuesto

| Integrante | Responsabilidad principal propuesta |
|---|---|
| Emanuel [apellido por completar] | Obtener, limpiar e integrar las fuentes 1 y 2; calcular indicadores de confiabilidad; organizar el repositorio. |
| Segundo integrante [nombre por completar] | Preparar la fuente 3, hacer la unión espacial por UPZ y construir el dashboard. |
| Ambos | Exploración, implicaciones éticas, recomendaciones y presentación ejecutiva. |

La distribución es **provisional** y se ajustará entre los dos integrantes.

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
