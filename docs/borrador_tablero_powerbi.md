# Primer boceto estático del tablero de Power BI (histórico)

**Este documento registra el primer boceto, anterior a las descargas del 19–23 de noviembre y a la creación del `.pbix`. Para el estado vigente y los controles actuales, consultar [tablero_powerbi_2026-11-24.md](tablero_powerbi_2026-11-24.md). Las cifras y pendientes de abajo no describen el estado actual.**

Estado: 24 de noviembre de 2026. Este es un borrador para decidir el diseño; aún no existe un archivo `.pbix` verificado.

## Archivos preparados

- `datos/procesados/powerbi_borrador_estacion_hora.csv`: una fila por fecha, hora y estación; 11.488 filas de cuatro días disponibles (14, 15, 16 y 18 de noviembre). Lo genera `src/preparar_borrador_powerbi.py` sin alterar las fuentes originales.
- `outputs/borradores_powerbi/`: seis imágenes preliminares generadas por `src/generar_borradores_powerbi.py`.

## Página 1: qué y cuándo

1. `01_entradas_por_hora.png`: entradas registradas por hora y por día. Permite comparar la forma de la jornada, incluso sábado y domingo.
2. `02_oferta_y_demanda_por_hora.png`: dos gráficos alineados, uno para entradas y otro para pasos **programados**. Solo aparecen el lunes 16 y el miércoles 18, fechas con validaciones y GTFS del mismo día. Las unidades no se mezclan en un mismo eje.
3. `03_relacion_pico_valle.png`: razón entre sumas de entradas y pasos programados en filas comparables. No es ocupación, puntualidad ni porcentaje. Por ahora solo hay dos fechas comparables.
4. `05_estaciones_destacadas.png`: primeras 12 estaciones por entradas observadas en los cuatro días, no una clasificación permanente del sistema.
5. `06_demanda_pico_valle_por_tipo_dia.png`: entradas promedio por hora observada, separando fin de semana (dos días), día hábil (un día) y lunes con servicio dominical (un día). Esta vista compara demanda, no oferta.

## Página 2: dónde y contexto

1. `04_mapa_concentracion_entradas.png`: puntos de estaciones sobre límites de localidades. El color indica entradas registradas; se usa escala logarítmica para distinguir estaciones de magnitudes distintas. Las estaciones georreferenciadas representan el 88,7 % de las entradas de estos cuatro días.
2. Falta el segundo mapa de **indicadores de residentes por localidad** de la Encuesta Multipropósito 2021. Primero se debe validar la variable, el denominador y la agregación territorial. Nunca debe describirse como el perfil de quienes usan cada estación.
3. Después del segundo mapa puede añadirse una dispersión con una observación por localidad para examinar una posible relación descriptiva, sin afirmar causalidad.

## Reglas para interpretar y filtrar

- `validaciones` son entradas registradas, no pasajeros únicos. `pasos_programados` son pasos del horario GTFS, no buses efectivamente observados.
- `comparable=True` indica que existe un paso programado para esa estación, fecha y hora. La razón debe calcularse como **suma de entradas comparables / suma de pasos de esas mismas filas**; no como promedio de razones.
- Para sábado 14 y domingo 15 hay entradas, pero no GTFS emparejado localmente: `pasos_programados` queda vacío. Nunca convertirlo en cero. El lunes 16 se etiqueta aparte porque su GTFS activa servicio dominical; no tratarlo como un día hábil típico.
- Las franjas `06:00–08:59` y `17:00–19:59` (pico) y `09:00–16:59` (valle) son **provisionales**, para discutir el borrador. Las otras horas quedan en `Otras horas`.
- El cruce actual empieza en filas con entradas. Por tanto, la oferta graficada es solo la oferta de estación-hora con entradas observadas y emparejadas; no debe presentarse como toda la oferta de la red. Las conclusiones se limitan a los días disponibles.

## Controles realizados

La tabla tiene 11.488 claves fecha-hora-estación únicas, 5.040 filas comparables, ninguna entrada negativa y ninguna fila comparable con pasos nulos. Los pasos de sábado y domingo se mantienen nulos. Antes de entregar, actualizar las fechas con las capturas finales y volver a revisar cobertura, pares GTFS/validaciones y la unión estación-localidad.

Nota de operación: se intentó abrir Power BI Desktop, pero la ventana no ofreció un estado de aplicación confiable para importar y guardar el informe. No se editó ningún informe abierto ni se creó un `.pbix`; las imágenes y el CSV son avances locales, no sustituyen ese archivo.
