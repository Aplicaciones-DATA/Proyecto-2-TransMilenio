# Resultados y reproducción

## Qué encontramos

| Tipo de día | Pico | Valle |
| --- | ---: | ---: |
| Entre semana, cuatro días | 8,13 | 6,28 |
| Fin de semana, dos días | 5,62 | 5,78 |

Unidad: validaciones por paso programado. El cociente se calcula con la suma de las validaciones comparables dividida por la suma de los pasos de esas mismas filas. Usamos como rangos de análisis propuestos las horas 06–08 y 16–18 para pico, y 09–15 para valle, incluyendo la hora completa. El equipo puede confirmarlos o cambiarlos al reproducir el análisis. Las cifras corresponden **solo al 18–23/11/2026**, no a todo el mes ni a la red completa.

Durante el pico de entre semana, Portal 20 de Julio registró 81.894 validaciones comparables y 2.357 pasos programados (34,75 por paso). Le siguieron Portal Suba (29,01) y Portal 80 (28,99). Las 06:00–06:59 tuvieron el mayor volumen comparable al sumar los seis días, con 822.057 entradas.

Un caso territorial es San Cristóbal, donde queda Portal 20 de Julio. En la EM 2021, el 33,5 % de los hogares reportó ingresos insuficientes para gastos mínimos y el 23,7 % de los ocupados que se desplazaban al trabajo reportó un viaje de más de una hora. En Suba las cifras respectivas fueron 15,8 % y 14,9 %. El indicador de desplazamiento al estudio se conserva con su universo por separado. La [documentación de fuentes socioeconómicas](fuentes_socioeconomicas.md) explica los denominadores.

Como siguiente paso proponemos comprobar frecuencias reales y filas de espera en Portal 20 de Julio en las franjas destacadas. Para estimar ocupación y puntualidad se requieren observaciones de campo. Las conclusiones se circunscriben a los seis días y el 24 queda documentado como oferta programada. El mapa territorial también tiene cobertura incompleta: 133 de 151 estaciones de la tabla integrada tienen localidad y solo 18 localidades aparecen en la comparación.

## Repetir el cruce y la integración

Instala las dependencias del repositorio con `py -m pip install -r requirements.txt`. Coloca los ZIP diarios de validaciones y GTFS en `../registros_diarios/AAAA-MM-DD/`. Para generar cruces locales en PowerShell, desde la raíz del repositorio:

```powershell
18..23 | ForEach-Object { py .\src\comparar_validaciones_gtfs.py "2026-11-$_" }
```

**Límite de reproducción:** el tablero compartido y las cifras de este documento usan para el 18 el archivo detallado corregido por Alejandro, `../data_casi_lista/Comparacion_TransMilenio_2026-11-18_con_localidades.csv` (2.931 filas y 248.283 pasos comparables). El cruce que genera el script anterior a partir del ZIP local del 18 suma 235.072 pasos en esa fecha. Los resultados 19–23 sí coinciden entre versiones. Todavía no está identificado ni documentado el ZIP GTFS exacto ni la regla que produjeron el denominador corregido del 18; por tanto, **el comando anterior no reproduce exactamente el tablero ni esta tabla**. No se debe sustituir el CSV de Alejandro por la salida local del 18 sin resolver esa diferencia. Véanse [bitácora de limpieza](bitacora_limpieza.md) y [documentación del tablero](tablero_powerbi_2026-11-24.md).

Guarda estos insumos oficiales en una carpeta `insumos` fuera de Git. Cambia los nombres de la ruta en el comando si los guardaste en otro sitio.

- [Hogares 2021, DANE](https://www.dane.gov.co/files/investigaciones/multi/Anexo_hogares_EM_2021.xlsx) como `hogares.xlsx`.
- [Personas 2021, DANE](https://www.dane.gov.co/files/investigaciones/multi/Anexo_personas_EM_2021.xlsx) como `personas.xlsx`.
- [Polígonos oficiales en WGS84](https://serviciosgis.catastrobogota.gov.co/arcgis/rest/services/ordenamientoterritorial/localidad/MapServer/0/query?where=1%3D1&outFields=LOCCODIGO%2CLOCNOMBRE&outSR=4326&f=geojson) como `localidades.geojson`.

```powershell
py .\src\integrar_contexto_localidades.py --procesados .\datos\procesados --gtfs "..\registros_diarios\2026-11-18\GTFS (1).zip" --localidades ..\insumos\localidades.geojson --hogares ..\insumos\hogares.xlsx --personas ..\insumos\personas.xlsx --salida .\datos\procesados
```

El nombre `GTFS (1).zip` corresponde al archivo local inventariado para el 18; compruébalo antes de ejecutar en otro equipo. Este comando ilustra la integración desde los cruces locales, **no** la reproducción exacta del resultado corregido del 18. Para reproducir los números publicados hay que incorporar el CSV detallado de Alejandro y documentar su GTFS y regla de cómputo. Para explorar otras franjas, pasa los inicios de cada hora con `--pico` y `--valle`. El código verifica que los rangos no se solapen y que el cruce territorial preserve las filas y totales.

## Recorrido de la demostración

1. Muestra la cobertura y explica qué se cruzó.
2. Filtra entre semana y compara pico con valle. Cambia a fin de semana para mostrar cómo cambia el patrón en la muestra.
3. Abre Portal 20 de Julio y muestra ambos conteos detrás de 34,75.
4. Ubica la estación en San Cristóbal y compara con Suba usando la encuesta como contexto. Indica que son datos de residentes de 2021.
5. Cierra con la verificación de frecuencias reales y filas de espera como acción concreta.
