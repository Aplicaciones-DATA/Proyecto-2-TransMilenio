# Fuentes del análisis

| Fuente | Cobertura y unidad | Uso en el proyecto | Acceso |
| --- | --- | --- | --- |
| Validaciones troncales de TransMilenio | Del 18 al 23 de noviembre de 2026. Cada fila original registra un acceso. | Contamos entradas por fecha, hora y código de estación. | [Catálogo oficial](https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html) |
| GTFS estático de TransMilenio | Archivos de cada fecha del 18 al 24 de noviembre de 2026. Contienen rutas, viajes, estaciones, calendarios y horarios. | Contamos pasos de servicios troncales activos por estación y hora. | [Archivos diarios compartidos](https://drive.google.com/drive/folders/1hMytx7v1RhFU9_6_hH5dFCz4cq79T0ZN) · [Portal oficial](https://gtfs.transmilenio.gov.co/) |
| Límites de localidad de la SDP | 20 localidades de Bogotá. Geometrías en longitud y latitud. | Ubicamos el punto de cada estación principal dentro de un polígono. | [Datos Abiertos Bogotá](https://datosabiertos.bogota.gov.co/dataset/localidad-bogota-d-c) |
| Encuesta Multipropósito 2021, DANE y SDP | Resultados expandidos para Bogotá urbana por localidad. | Usamos los cuadros publicados 211A, 321A y 312A como contexto territorial. | [Publicación oficial y anexos](https://www.dane.gov.co/index.php/estadisticas-por-tema/pobreza-y-condiciones-de-vida/encuesta-multiproposito) |

El catálogo de validaciones y el de límites identifican la licencia CC BY 4.0. El repositorio conserva el código y los resúmenes agregados con sus fuentes. Los archivos diarios y microdatos se conservan fuera de Git.

El 24 tiene GTFS disponible. Las validaciones de esa fecha no estaban disponibles en la última comprobación. Los detalles del catálogo socioeconómico y los universos están en [fuentes socioeconómicas](fuentes_socioeconomicas.md).
