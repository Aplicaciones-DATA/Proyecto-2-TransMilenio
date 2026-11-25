# Proyecto 2 — Entradas y oferta programada de TransMilenio

Hicimos este proyecto para **Aplicaciones en Ciencia de Datos (DATA-1002)** en la Universidad de los Andes, con el profesor **Nicolás Mejía Martínez**. Nuestra propuesta es del **11 de noviembre de 2026**.

**Equipo:** Chiudacchang Collazos Trujillo y Alejandro Rojas.

**Estado al 25/11/2026:** el análisis vigente compara el **19–23 de noviembre**; se excluyó el 18 porque su conteo de pasos programados no se pudo conciliar entre dos versiones. Consulta los [resultados](docs/resultados.md), los [resúmenes agregados](datos/analisis/) y la [última copia del tablero Power BI](docs/TransMilenio_19-23_manana_tarde_revisado.pbix). Los CSV necesarios para actualizarlo están en el [paquete del Drive compartido](https://drive.google.com/file/d/1JJ2RuE9qTF57AE5q8ZbDaqOlNWgkDA-o/view?usp=drivesdk). El [análisis de gráficos](docs/analisis_graficos_19_23_2026.docx), las [consideraciones éticas](docs/Consideraciones_eticas_Proyecto_2_TransMilenio.docx) y la [presentación](docs/BORRADOR%20%C2%B7%20Proyecto%202%20TransMilenio%20%C2%B7%2019%E2%80%9323%20nov.%202026.pptx) están en `docs/`. Estos materiales posteriores no sustituyen la entrega oficial del 24/11. Los archivos crudos y las credenciales no están en GitHub.

## Acceso al histórico de datos

Guardamos los archivos grandes en la carpeta compartida de Google Drive. Desde aquí se puede abrir el histórico del proyecto.

- [Abrir todos los datos del proyecto](https://drive.google.com/drive/folders/1ZOasXuot0GN8eZCVPzYohVKkKF73UT4z)
- [GTFS diario](https://drive.google.com/drive/folders/1hMytx7v1RhFU9_6_hH5dFCz4cq79T0ZN): archivos de oferta programada.
- [Capturas de tiempo real](https://drive.google.com/drive/folders/121V5T0E_hdcwRwBGJb0WFIQGq5BnJxo7): posiciones, actualizaciones de viajes y alertas guardadas por el recolector.

Organizamos los archivos por fecha en carpetas `AAAA-MM-DD`. Cada vez que el recolector termina una carga, las capturas quedan en la carpeta del día. Para consultar o descargar los archivos hace falta tener acceso al Drive compartido.

En Drive dejamos el GTFS diario y las capturas `.pb.gz` del piloto; descargamos las validaciones por separado. El [manifiesto de `datos/raw`](datos/raw/README.md) explica dónde están esos originales y cómo se usan sin publicarlos en GitHub. Aquí conservamos código, documentación y pequeños agregados para mantener liviana la descarga.

## Resumen y propósito

La **propuesta original** buscaba evaluar la confiabilidad del servicio. El alcance que sí permiten estos datos es descriptivo: comparar entradas registradas con **pasos de bus programados**, por estación, franja y tipo de día. La Encuesta Multipropósito 2021 aporta contexto de las localidades, pero no describe a los pasajeros individuales. El análisis ayuda a identificar estaciones para estudiar con más detalle; no demuestra retrasos, ocupación ni efecto racimo.

Nos interesa el tema porque las demoras y los intervalos irregulares afectan la rutina de quienes dependen de TransMilenio para llegar al trabajo o al estudio, sobre todo si viven lejos y tienen pocas alternativas de transporte. Con los datos abiertos buscamos aportar evidencia para decidir dónde revisar primero el servicio.

## Preguntas del proyecto

> **Pregunta principal.** ¿En qué estaciones y horas se registran más entradas frente a los pasos de bus programados, y cómo cambia esa relación entre el pico de la mañana, el pico de la tarde, las horas de menor afluencia y los días hábiles o de fin de semana?

> **Pregunta de contexto.** ¿Qué características sociales y de movilidad tienen las localidades donde se ubican esas estaciones?

Para la primera pregunta contamos las entradas registradas sin restringirlas por motivo del viaje. Las franjas adoptadas para este análisis son **pico de la mañana 06:00–08:59**, **valle 09:00–15:59** y **pico de la tarde 16:00–18:59**; las otras horas quedan aparte. Son franjas de trabajo, no una clasificación oficial de TransMilenio. Separamos días hábiles y fin de semana. Un «paso programado» es una llegada prevista en el GTFS a una estación, no un bus observado por GPS.

Para la segunda usamos la [Encuesta Multipropósito 2021](https://datosabiertos.bogota.gov.co/dataset/encuesta-multiproposito-2021-sdp) como contexto de las localidades. Los cuadros expandidos del DANE aportan indicadores de capacidad de los hogares para cubrir gastos y tiempos de viaje al trabajo y al estudio, cada uno con su propio universo y denominador. Describen a residentes de **2021**, no a quienes ingresaron por una estación en **2026**.

La relación `entradas comparables / pasos programados comparables` no mide ocupación ni puntualidad. El piloto de posiciones en tiempo real es otra fuente y **no** se mezcla con este indicador, porque aún no está verificado el emparejamiento de cada vehículo con su viaje programado. Las descargas y huellas constan en [el registro](docs/registro_descargas.md).

### Preguntas de la propuesta inicial

> ¿Qué troncales y zonas de Bogotá reciben el servicio menos confiable de TransMilenio, y qué población depende de ellas?

En la propuesta también nos preguntamos lo siguiente.

1. ¿Cuánto se aleja la operación real de la programada en cada troncal?
2. ¿Dónde aparece con mayor frecuencia el **efecto racimo** (varios buses juntos y después un intervalo largo sin servicio)?
3. ¿Coinciden las zonas con peor servicio con las de menores ingresos o mayor dependencia del transporte público?

### Historia del cambio de alcance

La pregunta anterior pertenece a la propuesta original. En la primera exploración todavía no había un histórico verificado de paso real de buses ni una correspondencia completa entre los `trip_id` de posiciones y del GTFS. Después se inició un piloto de recolección; su cobertura y calidad aún deben comprobarse. Por eso el equipo trabaja con entradas observadas y oferta **programada**, no con un supuesto indicador de confiabilidad real.

La comparación vigente usa GTFS estático diario, validaciones por estación y hora, correspondencia estación-localidad y agregados sociodemográficos por localidad. Es una señal descriptiva de oferta **programada**, no una medida de puntualidad, ocupación real o discriminación. El [notebook inicial](notebooks/01_exploracion_oferta_programada.ipynb) explora rutas y viajes; el [documento del tablero del 24/11](docs/tablero_powerbi_2026-11-24.md) registra una versión histórica. Para abrir el tablero vigente en otro equipo, usa la [guía de traslado](docs/abrir_tablero_en_otro_equipo.md).

Las descargas locales y sus huellas se documentan en [el registro de descargas](docs/registro_descargas.md). Los archivos diarios y las capturas `.pb` no se publican en este repositorio.

## Fuentes de datos

| Fuente | Qué aporta | Unión usada | Límite |
|---|---|---|---|
| [Validaciones troncales de TransMilenio](https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html) | Entradas registradas | Fecha, estación y hora | Una validación no equivale a una persona única. El análisis vigente cubre 19–23/11/2026. |
| GTFS estático diario de TransMilenio | Pasos de bus **programados**, rutas y paradas con coordenadas | Misma fecha, estación y hora que las validaciones | La programación no demuestra que el bus haya pasado realmente. |
| [Encuesta Multipropósito 2021](https://datosabiertos.bogota.gov.co/dataset/encuesta-multiproposito-2021-sdp) y [límites de localidades](https://datosabiertos.bogota.gov.co/dataset/localidad-bogota-d-c) | Contexto social y de movilidad de residentes | Localidad de la estación | La encuesta es de 2021 y no describe a quienes validaron en 2026. |

Conservamos las capturas GTFS-Realtime del piloto en Drive. Describimos las fuentes y sus límites en [docs/fuentes.md](docs/fuentes.md).

Los originales están fuera de Git. El **18/11 se excluyó** del análisis vigente: existe un ZIP GTFS, pero su conteo de pasos no reproduce el CSV corregido utilizado en una versión anterior. No lo tratamos como un día sin datos ni mezclamos sus cifras con el corte actual. El **24/11 tampoco se incluye** porque no se incorporaron validaciones oficiales comparables de esa fecha. La [auditoría de datos](docs/auditoria_datos_tablero_2026-11-25.md), la [auditoría de cobertura de estaciones](docs/auditoria_cobertura_estaciones_2026-11-24.md) y las [fuentes territoriales](docs/fuentes_socioeconomicas.md) documentan estas decisiones y límites. Algunos documentos fechados el 24/11 describen el corte histórico **18–23**; para las cifras vigentes debe consultarse [resultados](docs/resultados.md).

## Indicadores del tablero actual y límites

| Indicador | Qué muestra |
|---|---|
| Validaciones registradas | Cuántas entradas hay por fecha, hora y estación; no personas únicas. |
| Pasos programados | Cuántas llegadas figuran en el GTFS; no llegadas reales. |
| Entradas por paso programado | Suma de entradas comparables dividida por suma de pasos de esas mismas filas. No es ocupación ni puntualidad. |
| Cobertura de comparación | Proporción de validaciones que cuentan con paso programado emparejado; varía por fecha y estación. |
| Contexto territorial | Indicadores de residentes de la localidad donde se ubica la estación, no perfil de pasajeros. |

Cumplimiento real, regularidad, efecto racimo y velocidad son preguntas de la **propuesta original**, pendientes de un histórico de posiciones y un emparejamiento verificado con los viajes. No aparecen como hechos calculados en el tablero actual. [Propuesta original; `docs/resultados.md`]

## Metodología

1. Definimos la pregunta y qué decisión queremos apoyar.
2. Revisamos qué mide cada fuente, qué fechas cubre y cómo podemos cruzarla con las demás.
3. Preparamos las bases y comprobamos cuántas filas coinciden. Registramos las decisiones en la [bitácora de limpieza](docs/bitacora_limpieza.md).
4. Comparamos los resultados por estación y hora para preparar las visualizaciones.
5. En el dashboard presentamos las comparaciones junto con sus límites.

### Cruce verificado

Agrupamos los registros por fecha, estación y hora. Para calcular el indicador usamos las filas en las que encontramos la estación en el GTFS y había pasos programados. Si agrupamos varias estaciones u horas, dividimos el total de validaciones comparables por el total de pasos programados de esas mismas filas.

Del **19 al 23 de noviembre de 2026** registramos **7.252.722 entradas**. De ellas, **6.353.794** tienen al menos un paso programado en la misma estación, fecha y hora: una cobertura del **87,61 %**. En esas filas comparables hubo **1.063.752 pasos programados**, de modo que la razón total fue **5,97 entradas por paso programado**. Los registros sin paso comparable no se interpretan como cero buses. El archivo incluye **151 estaciones**: 135 con coordenadas y 133 con localidad asignada. Un punto ausente del mapa no significa demanda nula.

Para generar los cruces diarios, guardamos los ZIP oficiales de cada fecha en `registros_diarios/AAAA-MM-DD/`, al lado del repositorio. Con las dependencias de `requirements.txt` instaladas, ejecutamos este comando en PowerShell desde la raíz del proyecto. El 18 queda fuera porque su denominador sigue sin conciliarse; los detalles están en [resultados](docs/resultados.md).

```powershell
19..23 | ForEach-Object { py .\src\comparar_validaciones_gtfs.py "2026-11-$_" }
```

### Resultados del análisis

- En los **tres días hábiles**, la razón entradas/pasos comparables fue **8,14** en el pico de la mañana, **7,66** en el de la tarde y **6,20** en valle. Los dos picos juntos dieron **7,91**.
- En los **dos días de fin de semana** fue **5,70** en la mañana, **5,54** en la tarde y **5,78** en valle. La diferencia no reprodujo el patrón de los días hábiles.
- Por volumen total de entradas destacaron **Portal Norte (283.353)**, **Portal Américas (268.751)** y **Portal Suba (225.693)**. Volumen alto no equivale automáticamente a saturación.
- El contexto social se compara **por localidad**, como descripción de residentes de 2021. No identifica la residencia ni el nivel socioeconómico de los pasajeros de una estación.

En [resultados y reproducción](docs/resultados.md) dejamos las franjas, las fuentes y los cálculos. Los [resúmenes agregados](datos/analisis/) permiten revisar las cifras; el [análisis de gráficos](docs/analisis_graficos_19_23_2026.docx) desarrolla las interpretaciones con sus límites.

## Entregables y estado

| Entregable | Contenido |
|---|---|
| **Repositorio público** | Código, organización de carpetas, procedencia y límites conocidos de reproducción y licencia de cada fuente. |
| **Dashboard** | [PBIX revisado del corte 19–23](docs/TransMilenio_19-23_manana_tarde_revisado.pbix), con indicadores, comparación por franjas y mapas. Para actualizarlo en otro equipo hacen falta los CSV derivados y seguir la [guía de apertura](docs/abrir_tablero_en_otro_equipo.md). |
| **Presentación ejecutiva** | [Archivo de trabajo](docs/BORRADOR%20%C2%B7%20Proyecto%202%20TransMilenio%20%C2%B7%2019%E2%80%9323%20nov.%202026.pptx) con problema, fuentes, hallazgos y límites. Su nombre conserva la etiqueta «BORRADOR». |
| **Documentación adicional** | [Análisis de gráficos](docs/analisis_graficos_19_23_2026.docx), [consideraciones éticas](docs/Consideraciones_eticas_Proyecto_2_TransMilenio.docx), [resultados](docs/resultados.md) y [bitácora de limpieza](docs/bitacora_limpieza.md). |

La actividad **Group 7: Proyecto 2** cerró el **24/11/2026 a las 23:59**. El historial de Bloque Neón registra el envío de Alejandro a las **23:58** (recibo **5080470**) con un ZIP y enlaces al repositorio, al PBIX y a la presentación. Ese comprobante acredita el envío, no la revisión o calificación del profesor. Los documentos y el PBIX enlazados arriba se publicaron **después**; no sustituyen lo enviado a Bloque Neón.

## Criterios éticos y límites de interpretación

- La estación donde alguien valida puede estar cerca de su trabajo o estudio, no de su vivienda. No atribuimos a los pasajeros los ingresos o condiciones de los residentes de esa localidad.
- Si vemos pocas validaciones en una estación, revisamos la cobertura y la oferta antes de sacar conclusiones sobre la necesidad de servicio. Esa cifra por sí sola no justifica reducir buses, porque podría perjudicar a personas que dependen del servicio.
- Trabajamos con agregados por estación y hora para cuidar la privacidad de los registros y mantener el análisis centrado en el servicio.
- Limitamos las conclusiones a cinco días y a las estaciones que pudimos comparar. Para hablar de puntualidad u ocupación necesitaríamos datos adicionales y un emparejamiento validado de los vehículos.
- Citamos las fuentes y registramos sus licencias en el repositorio.

El [documento ético](docs/Consideraciones_eticas_Proyecto_2_TransMilenio.docx) desarrolla estos riesgos. Como pasos futuros, conviene ampliar el periodo, documentar la versión exacta del GTFS del 18 y validar el enlace entre posiciones GPS y viajes antes de estudiar cumplimiento real de horarios.

## Organización del repositorio

```text
.
├── README.md                 # Propósito, metodología, alcance y estado
├── .gitignore                # Entornos, cachés y datos no autorizados para publicación
├── requirements.txt          # Dependencias Python usadas por scripts y notebooks
├── datos/
│   ├── raw/                  # Manifiesto público; originales privados o externos, sin alterar
│   ├── procesados/           # Resultados intermedios locales, excluidos de Git
│   └── analisis/             # Cuatro agregados pequeños del análisis corregido
├── notebooks/                # Exploración y análisis reproducible
├── src/                      # Funciones o scripts reutilizables
├── outputs/                  # Paquetes y figuras de trabajo locales, excluidos de Git
├── reports/                  # Materiales de comunicación históricos
└── docs/
    ├── fuentes.md            # Procedencia, cobertura, licencia y llaves
    ├── bitacora_limpieza.md  # Decisiones y efectos de preparación
    ├── resultados.md         # Corte y cifras vigentes del 19–23
    └── *.docx, *.pptx, *.pbix # Análisis, presentación y tablero publicados
```

Separamos los datos crudos de los procesados y dejamos el código, los notebooks y la documentación en sus propias carpetas. Usamos `.gitkeep` para que Git conserve las carpetas vacías. Guardamos los originales tal como los descargamos y revisamos la licencia antes de publicar datos.

## Referencias indicadas en la propuesta

- Alcaldía de Bogotá (2026), «Datos abiertos en tiempo real: TransMilenio conecta la operación del sistema con la tecnología de Bogotá» (`bogota.gov.co`).
- Datos Abiertos Bogotá, sección TransMilenio (`datosabiertos.bogota.gov.co/organization/transmilenio`).
- TransMilenio S. A., GTFS estáticos diarios (`datosabiertos-transmilenio.hub.arcgis.com`).
- Secretaría Distrital de Planeación, Encuesta Multipropósito 2021 (`datosabiertos.bogota.gov.co`).
- Datos Abiertos Bogotá, límites de Unidades de Planeamiento Zonal (`datosabiertos.bogota.gov.co`).
- Universidad de los Andes (2026), «Proyecto 2: Profundización e Impacto», DATA-1002.

Conservamos las referencias de la propuesta y anotamos en `docs/fuentes.md` qué enlaces, versiones y licencias hemos podido verificar.
