# Resultados exploratorios del 19 al 23 de noviembre de 2026

## Pregunta y corte acordados

El equipo escogió la siguiente pregunta: **¿cómo varían las entradas registradas frente a los pasos de bus programados entre franjas pico y valle, días hábiles y fines de semana, y estaciones troncales de los días comparables? ¿Qué contexto muestran las localidades donde se encuentran esas estaciones?** La pregunta queda cerrada como decisión del equipo. Este documento describe cinco días, del **19 al 23 de noviembre de 2026**: tres días hábiles y dos de fin de semana. No representa todo el mes ni toda la red.

El **18 de noviembre se excluyó** de este nuevo corte porque dos conteos de pasos programados para las mismas 2.931 claves estación–fecha–hora no coinciden: el cruce local suma **235.072** y el CSV corregido utilizado antes suma **248.283**. Sí existe un ZIP GTFS local de esa fecha; el problema es que no se ha podido identificar el archivo y/o la regla que reproduce el segundo conteo. Las validaciones del 18 no se usan en los indicadores ni en los gráficos de este documento. Los originales no se modificaron; la auditoría del corte anterior permanece en el historial de Git.

## Qué muestran los datos filtrados

| Indicador del 19 al 23 | Valor | Interpretación |
| --- | ---: | --- |
| Entradas registradas | 7.252.722 | Validaciones de ingreso, no personas únicas. |
| Entradas comparables | 6.353.794 | Entradas con al menos un paso programado en la misma estación, fecha y hora. |
| Pasos programados en filas comparables | 1.063.752 | Denominador del indicador, no todos los pasos de la red. |
| Entradas por paso programado comparable | 5,97 | Cociente de las dos filas anteriores, no ocupación de buses. |
| Cobertura de entradas para el cociente | 87,61 % | Porcentaje de entradas con un paso emparejado; las restantes no equivalen a cero buses. |

La unidad de la tabla principal es **estación + fecha + hora**. La razón se calcula como la **suma de entradas comparables dividida por la suma de pasos programados de esas mismas filas**. No se promedian cocientes por fila ni se cambian valores sin correspondencia por cero. Las franjas de trabajo son pico **06:00–08:59 y 16:00–18:59**, valle **09:00–15:59**, y las demás horas se mantienen aparte. Son reglas del análisis, no una definición oficial de TransMilenio.

| Tipo de día | Pico | Valle | Lectura prudente |
| --- | ---: | ---: | --- |
| Tres días hábiles | 7,91 | 6,20 | En estos tres días, la relación entradas/pasos fue mayor en pico. |
| Dos días de fin de semana | 5,62 | 5,78 | En estos dos días, la diferencia fue pequeña y en sentido contrario. |

En el corte filtrado, los mayores **volúmenes** de entradas incluyen Portal Norte (**283.353**), Portal Américas (**268.751**) y Portal Suba (**225.693**). Esos totales indican dónde se registraron más entradas, pero por sí solos no prueban saturación ni servicio insuficiente. El ranking por entradas **por paso** responde otra pregunta y debe usar exclusivamente filas comparables.

El archivo filtrado conserva **151 estaciones**; **135** tienen coordenadas y **133** tienen localidad asignada. Las filas con coordenadas representan **6.428.527 entradas** (**88,64 %** del total) y las que tienen localidad, **6.319.643** (**87,13 %**). Por tanto, un punto ausente del mapa no significa demanda cero. El contexto de la Encuesta Multipropósito corresponde a **residentes de 2021** de la localidad, no a las personas que validaron en 2026. No debe confundirse localidad de la estación con residencia del pasajero. Dos tablas sociales contienen indicadores y universos distintos: no se deben mezclar sus porcentajes. Véanse [fuentes](fuentes.md) y [fuentes socioeconómicas](fuentes_socioeconomicas.md).

## Conclusiones provisionales y siguiente comprobación

En los tres días hábiles incluidos, el cociente entradas/pasos programados fue mayor en las franjas pico que en valle. En los dos días de fin de semana no se observó el mismo contraste. Los mapas y el ranking permiten escoger estaciones para una revisión, pero **no miden si los buses efectivamente llegaron, su ocupación o la causa de las diferencias**. La recomendación proporcional a esta evidencia es verificar la operación real y ampliar el periodo antes de proponer cambios de servicio. Estas conclusiones son provisionales hasta que el equipo revise los gráficos y el Word analítico correspondientes al corte de cinco días.

## Reproducción y estado de los productos

Los agregados de cinco días se obtuvieron filtrando los CSV derivados por fechas **19–23/11** y se cotejaron con los cinco resúmenes diarios. Para repetir el cruce desde fuentes originales, conservar intactos los ZIP oficiales de validaciones y GTFS en `../registros_diarios/AAAA-MM-DD/` y ejecutar desde la raíz del repositorio:

```powershell
19..23 | ForEach-Object { py .\src\comparar_validaciones_gtfs.py "2026-11-$_" }
```

Este comando **solo** genera los cruces diarios; no actualiza por sí solo las tablas territoriales ni Power BI. La [copia revisada del PBIX](TransMilenio_19-23_manana_tarde_revisado.pbix) está publicada en este repositorio. El [paquete del Drive compartido](https://drive.google.com/file/d/1JJ2RuE9qTF57AE5q8ZbDaqOlNWgkDA-o/view?usp=drivesdk) incluye seis CSV derivados necesarios para actualizar el tablero en otro equipo. La copia revisada conserva el periodo 19–23/11 y la comparación entre mañana, tarde y valle. La publicación en GitHub fue posterior y **no sustituyó el envío oficial del 24/11**; las copias anteriores del tablero son históricas.

El análisis figura por figura está en el [documento Word](analisis_graficos_19_23_2026.docx), dentro de `docs/`. También están las [consideraciones éticas](Consideraciones_eticas_Proyecto_2_TransMilenio.docx) y la [presentación de trabajo](BORRADOR%20%C2%B7%20Proyecto%202%20TransMilenio%20%C2%B7%2019%E2%80%9323%20nov.%202026.pptx). Las interpretaciones deben discutirse con el equipo antes de tratarlas como conclusiones definitivas.

La diferencia no conciliada del 18 sigue documentada como una limitación histórica, no como una fecha faltante. El 24 tampoco se incluye: en la última revisión no estaban disponibles sus validaciones oficiales para emparejar con el GTFS de ese mismo día. La cobertura, los indicadores sociales y los datos GPS deben citarse con su año, unidad y límites. Las auditorías y la documentación del tablero anterior permanecen en el historial de Git.
