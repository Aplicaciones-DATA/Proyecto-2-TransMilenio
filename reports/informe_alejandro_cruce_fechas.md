# Proyecto 2 — cruce inicial de validaciones y oferta programada

Alejandro: el indicador anterior quedaba vacío porque mezclaba validaciones del 15–16 de noviembre con horarios GTFS descargados para el 18–23. Ya obtuvimos parejas de archivos para **el 16 y el 18 de noviembre de 2026**. El programa aplica el calendario y las excepciones de servicio GTFS, convierte el código de estación de validaciones al código GTFS y cruza **fecha + estación + hora**. También considera los horarios GTFS que pasan de las 24:00 y pertenecen al día siguiente.

| Día | Validaciones troncales | Validaciones con paso programado comparable | Cobertura | Estaciones comparables |
|---|---:|---:|---:|---:|
| 16 de noviembre | 535.674 | 471.411 | 88,00 % | 132 |
| 18 de noviembre | 1.952.375 | 1.712.098 | 87,69 % | 132 |

Los resultados están en `datos/procesados/comparacion_estacion_hora_YYYY-MM-DD.csv` y `resumen_comparacion_YYYY-MM-DD.csv` (archivos locales excluidos de Git). Se reproducen con `python src/comparar_validaciones_gtfs.py 2026-11-16` o cambiando la fecha a `2026-11-18`, después de instalar `requirements.txt`. Los ZIP originales siguen intactos.

**Qué significa el indicador:** validaciones por paso programado es una medida exploratoria de presión de demanda frente a oferta *planificada*. No equivale a ocupación real ni a puntualidad. Las estaciones u horas sin paso programado se marcan **no comparables**; no se les asigna cero. En los dos días, aproximadamente el 12 % de las validaciones quedó sin correspondencia y requiere revisar códigos de estación, cobertura horaria o diferencias entre fuentes antes de sacar conclusiones.

**GPS:** puede incorporarse después para estimar paso real y puntualidad, pero **no bloquea** este primer análisis. Para ello aún hace falta verificar identificadores de vehículo/viaje y cobertura de posiciones consecutivas.

**Contexto territorial:** las siete fuentes oficiales de Encuesta Multipropósito 2021, diccionarios, población y capas geográficas están en la [carpeta compartida de Drive](https://drive.google.com/drive/folders/1CsKIa3GcVX0xB4JXHd_3oMNvLILT2hTX), accesible para el equipo. La encuesta agrupa algunas UPZ; por eso **no** debemos unirla directamente con cada polígono UPZ. La localidad es alternativa, tras validar la asignación espacial. Además, la encuesta es de 2021 y las validaciones de 2026: solo aporta contexto agregado, no describe a cada pasajero.

**Siguiente paso:** ampliar el cruce a más días con ambos archivos, auditar las estaciones no comparables y escoger unas pocas estaciones/horas para presentar gráficos y hallazgos prudentes.

Fuentes: [GTFS Schedule Reference](https://gtfs.org/documentation/schedule/reference/), [validaciones oficiales](https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html), [Encuesta Multipropósito 2021](https://datosabiertos.bogota.gov.co/dataset/encuesta-multiproposito-2021-sdp). Detalle de archivos y licencias en `docs/fuentes_socioeconomicas.md`.
