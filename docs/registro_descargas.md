# Registro local de archivos del proyecto

Los datos voluminosos se guardan en la carpeta local `PROY FINAL`, fuera del repositorio público. Las fechas de las carpetas diarias son **fechas de los datos**, no necesariamente fechas de descarga. El inventario siguiente fue verificado localmente el 24/11/2026; SHA-256 identifica los bytes de cada ZIP original.

## Validaciones troncales

Fuente oficial: <https://validaciones.datosabiertos.transmilenio.gov.co/ValidacionTroncal.html>. Cada ZIP contiene un CSV con el nombre de la fecha. Los ZIP enumerados pasaron la comprobación de integridad del archivo comprimido.

| Fecha de los datos | Archivo en `registros_diarios/FECHA/` | Tamaño comprimido | SHA-256 |
|---|---|---:|---|
| 2026-11-13 | `validacionTroncal20261113.zip` | 129.045.988 bytes | `80B5719A7FE28DD2ACE7D66191B866A8DA58FCC930EB920F778E9E2B29A1759D` |
| 2026-11-14 | `validacionTroncal20261114.zip` | 82.938.525 bytes | `8C65058B4B0A82CB4CACD49A694BB37025869E065CCDCB7BF71E73928DAEC5B5` |
| 2026-11-15 | `validacionTroncal20261115.zip` | 38.888.150 bytes | `05AFD55FCA4DD997DEA2AF3FE28C6516697A652CFCBC54A4289B6BFC6F6533AD` |
| 2026-11-16 | `validacionTroncal20261116.zip` | 34.273.920 bytes | `7846C60848AF31485CA313C6C6BB28C4C3A0649E56E17D31F53545DD63829F0A` |
| 2026-11-18 | `validacionTroncal20261118.zip` | 133.001.145 bytes | `28565D7BC74EA23232C9E30D279543FE0C554EB94007E0F5D4C12E4CD04E8C9D` |
| 2026-11-19 | `validacionTroncal20261119.zip` | 108.398.959 bytes | `33B41B3529E22700EA43D9C2B2A42E229E3581E9CF3DFB4939A2D3F6E95AB9BD` |
| 2026-11-20 | `validacionTroncal20261120.zip` | 129.955.313 bytes | `29CE634DE7E1ADB8ED48902494D562329DA6CB7A1986BA57101C7A4066B12006` |
| 2026-11-21 | `validacionTroncal20261121.zip` | 86.562.498 bytes | `22EC23C73782E11C3F1D1D6629778D742842580E86AC7066B768FC3B8E815901` |
| 2026-11-22 | `validacionTroncal20261122.zip` | 38.184.940 bytes | `752B5C1B2574799BE397B3F7E2E6DCB0B8C995D954E0DB13A914C3209C323582` |
| 2026-11-23 | `validacionTroncal20261123.zip` | 125.304.853 bytes | `05C4FDA0BD728FDA84DD3C342AD17F0EAD81EB4B0FCD7FFAAB11101C971A9252` |

El archivo del **2026-11-16** había respondido `404` en una consulta temprana; se descargó después. El portal aún no mostraba el ZIP del 24/11 al consultar el 24/11 hacia las 20:00 (hora de Bogotá). La carpeta `2026-11-17` no tiene un par validación-GTFS utilizado en el análisis.

## GTFS de las fechas comparables

Fuente: ZIP diarios descargados previamente por el recolector a la carpeta compartida de Drive del proyecto; se copiaron íntegros a `registros_diarios/FECHA/` y se comprobó la integridad de cada ZIP. No son vehículos observados. [GTFS del proyecto en Drive](https://drive.google.com/drive/folders/1hMytx7v1RhFU9_6_hH5dFCz4cq79T0ZN)

| Fecha | Archivo | Bytes | SHA-256 |
|---|---|---:|---|
| 2026-11-16 | `GTFS_descargado_2026-11-16.zip` | 71.000.036 | `C9E376ED47DA377469BB4E1FF25777EDDC0881C9198E037C881551068C773ADA` |
| 2026-11-18 | `GTFS (1).zip` | 119.032.669 | `78F5D375681BB3273076F84B8F314457DDF385AD0DA07DC85C6E27EAB2A2E85F` |
| 2026-11-19 | `GTFS_20261119.zip` | 119.002.018 | `994DC09129D933F6B816D0CF1521DBB3400D0FE995C99BD2B9B6D153CCC728EE` |
| 2026-11-20 | `GTFS_20261120.zip` | 121.079.535 | `5E944453AD61936AB91E056AFA86D744E8F1416D0C2FA332D1B9359E6CAF9466` |
| 2026-11-21 | `GTFS_20261121.zip` | 120.773.456 | `10D362607B8A7C3E1ACB220B812F2488DE4A12D4888EDC6ED6F45EA22DACE047` |
| 2026-11-22 | `GTFS_20261122.zip` | 120.477.925 | `18429FACF445A8FAA4435C0702B03BBF1B5220BC9F52BEE708E21C32BD512829` |
| 2026-11-23 | `GTFS_20261123.zip` | 117.917.842 | `42BB5CBC8EFB70690D4F871999ECA2E53CE0668F095BDAF11BB5B6053D122C21` |

## Programación GTFS y capturas puntuales

- El GTFS del 16/11 también existe en `fuentes_compartidas/gtfs/`; su copia diaria y huella figuran en la tabla anterior. No representa vehículos observados.
- `registros_diarios/2026-11-16/gtfs_rt/captura_2307/`: copias de `alerts (1).pb`, `positions (1).pb` y `tripupdates (1).pb` que ya estaban en Descargas. Son **una captura puntual**, no un histórico del día.
- `registros_diarios/2026-11-16/gtfs_rt/muestra_2226_2243/`: carpeta reservada para las 24 alertas examinadas previamente. La carpeta original `DATOS - Muestra 0.1` estaba vacía al organizar los archivos; por tanto, no se copiaron esas capturas ni se afirmará que están conservadas aquí.

Los CSV de validaciones incluyen campos como `Numero_Tarjeta` y saldos. No subir los ZIP ni filas individuales al repositorio público. Para el análisis, seleccionar solo las columnas necesarias, agregar por estación y franja y documentar cualquier limitación de cobertura. Los archivos socioeconómicos descargados se describen en `fuentes_socioeconomicas.md`.
