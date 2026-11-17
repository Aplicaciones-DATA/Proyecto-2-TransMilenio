# Registro de fuentes

Antes de publicar resultados, completar para cada fuente la URL exacta, fecha de consulta, versión, cobertura temporal y geográfica, unidad de análisis, campos disponibles, licencia y posibles restricciones. Ya se verificó la descarga e integridad de tres días de validaciones, pero **su compatibilidad con las estaciones del GTFS aún no se ha comprobado**. El inventario local está en [registro_descargas.md](registro_descargas.md).

| Fuente | URL y versión exactas | Cobertura y unidad | Licencia y permiso de redistribución | Llave disponible | Estado |
|---|---|---|---|---|---|
| Históricos de operación de TransMilenio, Datos Abiertos Bogotá | Pendiente | Pendiente | Pendiente | Ruta, estación o troncal y fecha: verificar | Por descargar |
| GTFS estático de TransMilenio | [Portal oficial](https://gtfs.transmilenio.gov.co/); copia local del 16-11-2026, SHA-256 `c9e376ed47da377469bb4e1ff25777eddc0881c9198e037c881551068c773ada` | Programación declarada para 2026; rutas, viajes y paradas | Permiso de redistribución por confirmar | `route_id`, `trip_id`, `stop_id`; coincidencia con tiempo real por validar | ZIP local íntegro; análisis inicial |
| Validaciones de ingreso por estación | [Portal de validaciones](https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html) | Archivos diarios 13–15 de noviembre de 2026; campos de fecha y estación presentes, granularidad útil por verificar | Portal indica CC-BY 4.0; revisar tratamiento ético de columnas sensibles | Estación y fecha/franja: correspondencia con GTFS por verificar | Tres ZIP descargados e íntegros, sin analizar aún |
| Encuesta Multipropósito 2021 + límites de UPZ | Pendiente | Pendiente | Pendiente | Coordenadas de parada a UPZ/localidad: verificar | Por descargar |

Si una fuente no permite análisis por UPZ, documentar la decisión de trabajar por localidad o evaluar la Encuesta de Movilidad 2023. No subir datos crudos a un repositorio público sin comprobar su licencia.

## Inventario mínimo para la pregunta exploratoria

Para una prueba de **un día** hacen falta cuatro tipos de archivos: (1) un `GTFS.zip` íntegro para la oferta programada; (2) un archivo diario de validaciones de ingreso para demanda por estación y hora; (3) una capa geográfica de UPZ; y (4) una tabla de indicadores sociodemográficos por UPZ. Si se estudian más días, se requiere un archivo de validaciones por día y comprobar si la versión de GTFS cambió. Una muestra de `positions.pb` es opcional para explorar la operación, pero no sustituye las validaciones de pasajeros.

El GTFS local revisado el 16 de noviembre de 2026 tiene 11 miembros y pasó la verificación de integridad ZIP. Sus 937 rutas, 101.136 viajes y 8.290 paradas son datos **programados**, no observaciones de ejecución. Su publicación en el repositorio permanece pendiente de verificar licencia; el notebook pide extraerlo localmente en `datos/raw/gtfs/`, carpeta excluida de Git.
