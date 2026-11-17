# Registro local de archivos del proyecto

Los datos voluminosos se guardan en la carpeta local `PROY FINAL`, fuera del repositorio público. Las fechas de las carpetas diarias son **fechas de los datos**, no necesariamente fechas de descarga.

## Validaciones troncales

Fuente oficial: <https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html>. Cada ZIP contiene un CSV con el nombre de la fecha. Los tres ZIP pasaron la comprobación de integridad del archivo comprimido.

| Fecha de los datos | Archivo en `registros_diarios/FECHA/` | Tamaño comprimido | SHA-256 |
|---|---|---:|---|
| 2026-11-13 | `validacionTroncal20261113.zip` | 129.045.988 bytes | `80B5719A7FE28DD2ACE7D66191B866A8DA58FCC930EB920F778E9E2B29A1759D` |
| 2026-11-14 | `validacionTroncal20261114.zip` | 82.938.525 bytes | `8C65058B4B0A82CB4CACD49A694BB37025869E065CCDCB7BF71E73928DAEC5B5` |
| 2026-11-15 | `validacionTroncal20261115.zip` | 38.888.150 bytes | `05AFD55FCA4DD997DEA2AF3FE28C6516697A652CFCBC54A4289B6BFC6F6533AD` |

El archivo del **2026-11-16** aún respondía `404` en la consulta hecha después de medianoche del 17 de noviembre. La carpeta `2026-11-17` está creada como espacio de trabajo, **sin registros descargados todavía**.

## Programación GTFS y capturas puntuales

- `fuentes_compartidas/gtfs/GTFS_descargado_2026-11-16.zip`: copia del GTFS estático íntegro que ya estaba en Descargas, 71.000.036 bytes, SHA-256 `C9E376ED47DA377469BB4E1FF25777EDDC0881C9198E037C881551068C773ADA`. No representa vehículos observados el 16 de noviembre.
- `registros_diarios/2026-11-16/gtfs_rt/captura_2307/`: copias de `alerts (1).pb`, `positions (1).pb` y `tripupdates (1).pb` que ya estaban en Descargas. Son **una captura puntual**, no un histórico del día.
- `registros_diarios/2026-11-16/gtfs_rt/muestra_2226_2243/`: carpeta reservada para las 24 alertas examinadas previamente. La carpeta original `DATOS - Muestra 0.1` estaba vacía al organizar los archivos; por tanto, no se copiaron esas capturas ni se afirmará que están conservadas aquí.

Los CSV de validaciones incluyen campos como `Numero_Tarjeta` y saldos. No subir los ZIP ni filas individuales al repositorio público. Para el análisis, seleccionar solo las columnas necesarias, agregar por estación y franja y documentar cualquier limitación de cobertura. La capa geográfica y el indicador sociodemográfico aún están pendientes; sus carpetas existen en `fuentes_compartidas/territorio/` y `fuentes_compartidas/sociodemografia/`.
