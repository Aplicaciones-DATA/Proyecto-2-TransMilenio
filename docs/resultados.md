# Resultados y reproducción

## Qué encontramos

| Tipo de día | Pico | Valle |
| --- | ---: | ---: |
| Entre semana, cuatro días | 8,13 | 6,28 |
| Fin de semana, dos días | 5,62 | 5,78 |

Unidad: validaciones por paso programado. El cociente se calcula con la suma de las validaciones comparables dividida por la suma de los pasos de esas mismas filas. Usamos como rangos de análisis propuestos las horas 06–08 y 16–18 para pico, y 09–15 para valle, incluyendo la hora completa. El equipo puede confirmarlos o cambiarlos al reproducir el análisis.

Durante el pico de entre semana, Portal 20 de Julio registró 81.894 validaciones comparables y 2.357 pasos programados (34,75 por paso). Le siguieron Portal Suba (29,01) y Portal 80 (28,99). Las 06:00–06:59 tuvieron el mayor volumen comparable al sumar los seis días, con 822.057 entradas.

Un caso territorial es San Cristóbal, donde queda Portal 20 de Julio. En la EM 2021, el 33,5 % de los hogares reportó ingresos insuficientes para gastos mínimos y el 23,7 % de los ocupados que se desplazaban al trabajo reportó un viaje de más de una hora. En Suba las cifras respectivas fueron 15,8 % y 14,9 %. El indicador de desplazamiento al estudio se conserva con su universo por separado. La [documentación de fuentes socioeconómicas](fuentes_socioeconomicas.md) explica los denominadores.

Como siguiente paso proponemos comprobar frecuencias reales y filas de espera en Portal 20 de Julio en las franjas destacadas. Para estimar ocupación y puntualidad se requieren observaciones de campo. Las conclusiones se circunscriben a los seis días y el 24 queda documentado como oferta programada.

## Repetir el cruce y la integración

Instala las dependencias del repositorio con `py -m pip install -r requirements.txt`. Coloca los ZIP diarios de validaciones y GTFS en `../registros_diarios/AAAA-MM-DD/`. Para generar los cruces de la muestra en PowerShell, desde la raíz del repositorio:

```powershell
18..23 | ForEach-Object { py .\src\comparar_validaciones_gtfs.py "2026-11-$_" }
```

Guarda estos insumos oficiales en una carpeta `insumos` fuera de Git. Cambia los nombres de la ruta en el comando si los guardaste en otro sitio.

- [Hogares 2021, DANE](https://www.dane.gov.co/files/investigaciones/multi/Anexo_hogares_EM_2021.xlsx) como `hogares.xlsx`.
- [Personas 2021, DANE](https://www.dane.gov.co/files/investigaciones/multi/Anexo_personas_EM_2021.xlsx) como `personas.xlsx`.
- [Polígonos oficiales en WGS84](https://serviciosgis.catastrobogota.gov.co/arcgis/rest/services/ordenamientoterritorial/localidad/MapServer/0/query?where=1%3D1&outFields=LOCCODIGO%2CLOCNOMBRE&outSR=4326&f=geojson) como `localidades.geojson`.

```powershell
py .\src\integrar_contexto_localidades.py --procesados .\datos\procesados --gtfs ..\registros_diarios\2026-11-18\GTFS_20261118.zip --localidades ..\insumos\localidades.geojson --hogares ..\insumos\hogares.xlsx --personas ..\insumos\personas.xlsx --salida .\datos\procesados
```

Para repetir el periodo exacto de este informe, usa una carpeta de procesados con los seis cruces del 18 al 23. Para explorar otras franjas, pasa los inicios de cada hora con `--pico` y `--valle`. El código verifica que los rangos no se solapen y que el cruce territorial preserve las filas y totales.

## Recorrido de la demostración

1. Muestra la cobertura y explica qué se cruzó.
2. Filtra entre semana y compara pico con valle. Cambia a fin de semana para mostrar cómo cambia el patrón en la muestra.
3. Abre Portal 20 de Julio y muestra ambos conteos detrás de 34,75.
4. Ubica la estación en San Cristóbal y compara con Suba usando la encuesta como contexto. Indica que son datos de residentes de 2021.
5. Cierra con la verificación de frecuencias reales y filas de espera como acción concreta.
