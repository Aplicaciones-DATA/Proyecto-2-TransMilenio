# Fuentes socioeconómicas y territoriales

Las copias originales están en la carpeta local `fuentes_compartidas/socioeconomicos/`,
fuera de Git. Se comparten con el equipo en la carpeta privada
[`Proyecto 2 TransMilenio - datos/fuentes_socioeconomicas`](https://drive.google.com/drive/folders/1CsKIa3GcVX0xB4JXHd_3oMNvLILT2hTX) de Google Drive.
No se modifican los archivos originales para el análisis.

| Archivo local y en Drive | Fuente oficial | Año o cobertura | Licencia |
|---|---|---|---|
| `em2021.csv` | [Encuesta Multipropósito 2021, SDP](https://datosabiertos.bogota.gov.co/dataset/encuesta-multiproposito-2021-sdp/resource/b3fd892e-b9f9-4f34-ac22-6cc50612eac9) | Encuesta 2021, Bogotá y municipios cercanos | CC BY 4.0 |
| `diccionario_em2021.ods` | [Metadatos de la encuesta](https://datosabiertos.bogota.gov.co/dataset/encuesta-multiproposito-2021-sdp) | Variables de EM2021 | CC BY 4.0 |
| `variables_adicionales_em2021.csv` | [Variables adicionales](https://datosabiertos.bogota.gov.co/dataset/encuesta-multiproposito-2021-sdp/resource/ba44798f-5257-4c5c-8a57-0966da1bb4fa) | Indicadores derivados de EM2021 | CC BY 4.0 |
| `diccionario_variables_adicionales_em2021.ods` | [Metadatos de variables adicionales](https://datosabiertos.bogota.gov.co/dataset/encuesta-multiproposito-2021-sdp) | Variables derivadas | CC BY 4.0 |
| `geometria_upz_indicador_espacio_publico.zip` | [Indicador Espacio Público UPZ, IDECA](https://datosabiertos.bogota.gov.co/dataset/indicador-espacio-publico-upz) | Capa geográfica por 112 UPZ; fuente derivada, no límites puros | CC BY-SA 4.0 |
| `proyecciones_poblacion_upz_2005_2035.ods` | [Proyecciones de población, SDP](https://datosabiertos.bogota.gov.co/dataset/proyecciones-y-retroproyecciones-de-poblacion-2005-2035) | Serie 2005–2035 por UPZ | CC BY 4.0 |
| `limites_localidades_bogota.json` | [Localidad. Bogotá D.C., SDP](https://datosabiertos.bogota.gov.co/dataset/localidad-bogota-d-c) | 20 localidades | CC BY 4.0 |

## Revisión inicial y límites de integración

- El CSV principal tiene 1.553 columnas. Incluye `COD_LOCALIDAD`,
  `COD_UPZ_GRUPO` y el factor `FEX_C`. Algunas UPZ aparecen **agrupadas**
  en un solo código (por ejemplo, `811` agrupa varias UPZ), por lo que no se
  debe unir cada fila de la encuesta directamente con uno de los 112 polígonos.
- La encuesta incluye Bogotá y municipios cercanos. Hay filas sin
  `COD_LOCALIDAD` de Bogotá; hay que filtrar la población antes de agregar.
- La geometría descargada de UPZ proviene de un **indicador espacial**, no de
  una capa de límites independientes. Tiene 112 entidades y un campo
  `CODIGO_UPZ`. Aunque el catálogo la llama GeoJSON, el ZIP contiene JSON
  con estructura Esri; no se debe leer como GeoJSON estándar sin convertirlo.
  Verificar cobertura, año y correspondencia antes de usarla
  como límite para asignar estaciones.
- Si la agrupación de UPZ impide una unión exacta, la alternativa más clara es
  trabajar por **localidad**: agregar la encuesta con `COD_LOCALIDAD` y
  asignar cada estación a una de las 20 localidades mediante la geometría
  oficial. La unión espacial y los factores de expansión aún deben validarse.
- La encuesta representa 2021 y la operación de TransMilenio se observa en
  2026. El contexto socioeconómico no describe automáticamente a quienes
  validaron en una estación ni prueba cambios individuales o causalidad.
- El archivo de FONCEP sobre pensionados no reemplaza la encuesta: cubre solo
  pensionados de esa entidad, no toda la población mayor ni todos los usuarios.

Las URLs exactas y tamaños originales están disponibles en los metadatos de
cada recurso del portal oficial. El script
`src/publicar_fuentes_socioeconomicas.py` verifica tamaño y huellas antes
de subir y después comprueba que Drive recibió los mismos bytes.
