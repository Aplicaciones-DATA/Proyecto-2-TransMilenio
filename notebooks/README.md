# Cuadernos del proyecto

Estos dos cuadernos son **exploratorios**. Sirven para entender las fuentes paso a paso; el tablero final se alimenta de las tablas preparadas por los programas de `src/`, no directamente de las salidas de los cuadernos.

1. `01_exploracion_oferta_programada.ipynb`: abre cuatro tablas de **un** GTFS local y cuenta rutas y viajes publicados. No indica los buses que circularon ni selecciona una fecha de servicio. Antes de ejecutarlo, coloca `agency.txt`, `routes.txt`, `trips.txt` y `stops.txt` en `datos/raw/gtfs/` y anota de qué ZIP salieron.
2. `02_demanda_observada_estaciones.ipynb`: lee por bloques **todos** los ZIP `validacionTroncal*.zip` que encuentre en `../registros_diarios/AAAA-MM-DD/`, cuenta entradas por fecha, hora y estación, y guarda un CSV con las fechas en el nombre. Revisa primero la lista de ZIP: puede haber días que no quieras comparar. Si el archivo de salida ya existe, el cuaderno se detiene para no sobrescribirlo.

El archivo `datos/procesados/validaciones_por_estacion_hora.csv` es una salida histórica del cuaderno 02; no representa todos los ZIP actuales. El tablero usa `datos/procesados/powerbi_tabla_integrada_provisional.csv` y las tablas asociadas. La preparación, limpieza y cruces —incluidos los aportes de Alejandro— están documentados en `docs/bitacora_limpieza.md` y en los programas de `src/`.

Para reproducir los cuadernos, abre la carpeta raíz del proyecto en VS Code, instala `requirements.txt`, selecciona el entorno del proyecto como kernel de Python y ejecuta las celdas en orden. Los archivos crudos y las credenciales no se suben a GitHub.
