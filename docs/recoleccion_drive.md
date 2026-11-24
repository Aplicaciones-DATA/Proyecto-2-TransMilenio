# Recolección GTFS a Drive por franjas diarias

El recolector `src/recolectar_a_drive.py` funciona **en el PC encendido** durante las franjas acordadas. Recibe cada respuesta en memoria y la sube a Google Drive; no deja los `.pb` ni el ZIP en el disco. Mientras trabaja solicita a Windows que no suspenda el equipo y retira esa solicitud al terminar; no cambia el plan general de energía. El Programador de tareas puede iniciarlo automáticamente con la sesión de Windows abierta y despertar el PC de suspensión si está conectado a la corriente, pero **no puede encender un PC completamente apagado**. Si se apaga, se cierra la sesión, se cierra la tapa o se pierde internet, faltarán capturas. Drive es almacenamiento, no ejecuta el programa.

## Destino

Se creó en la cuenta personal de Emanuel la carpeta `Proyecto 2 TransMilenio - datos`, con `GTFS_diario` y `capturas_tiempo_real`. El programa creará dentro de cada una una carpeta `AAAA-MM-DD`. Los nombres de captura incluyen fecha, hora y zona horaria de Bogotá. Antes de cualquier carga, comprobará que la cuenta de la API coincida con `correo_esperado`.

La configuración privada `config/captura_local.json` contiene el correo y el ID de la carpeta. Está excluida de Git. `config/captura.example.json` es solo una plantilla pública.

## Preparación y primeras capturas verificadas

1. La prueba acordada cubre del **18 al 23 de noviembre de 2026**, ambos incluidos. Las franjas habituales son **10:00–12:00**, **14:00–16:00** y **17:00–19:00** todos los días (hora de Bogotá); la de 14:00–16:00 ya **no depende** de que falten datos de la mañana. Desde el **21**, se suma la última hora: **22:00–23:00 el sábado 21 y el lunes 23**, y **21:00–22:00 el domingo 22**. La primera mañana posible fue el 19; el 18 ya había pasado esa franja cuando se cambió el horario. El programa no capturará fuera de estas fechas.
2. Las URL reales de los archivos `.pb` y ZIP aportados se recuperaron de sus metadatos de descarga (`Zone.Identifier`) y se comprobaron el 18-11-2026. `https://gtfs.transmilenio.gov.co/positions.pb`, `tripupdates.pb` y `alerts.pb` respondieron con cabecera binaria GTFS-Realtime; `https://gtfs.transmilenio.gov.co/GTFS.zip` se descargó y validó íntegramente. A las 12:00 aproximadamente, las respuestas en memoria midieron 635.688, 8.255.068, 65.756 y 120.905.452 bytes, respectivamente; no se guardaron ni subieron en esta comprobación. Estas cuatro URL ya están en la configuración privada. El servidor etiqueta los `.pb` como `text/plain`, aunque su contenido es binario, por lo que el recolector valida la cabecera del contenido en vez de confiar solo en ese encabezado. No se usaron las URL de `gis.transmilenio.gov.co/gtfs/`, que devolvieron HTTP 500.
3. La conexión OAuth de `emanuelcollazos41@gmail.com` ya está verificada. El titular creó un secreto nuevo y descargó el JSON; se movió a `%LOCALAPPDATA%/Proyecto2TransMilenio/oauth_client.json`, fuera del repositorio. El secreto usado en la prueba anterior, expuesto en una salida privada de herramientas, se inhabilitó y borró con su aprobación. El token se renovó ante Google usando el secreto nuevo, se comprobó la cuenta con Drive API y se guardó solo después de verificar el correo. No se pegó ningún secreto en el chat ni en GitHub. El secreto original del cliente (distinto del expuesto) sigue habilitado en Cloud y puede inhabilitarse tras comprobar la primera captura real.

   El 18-11-2026 se verificó que la consola corresponde a `emanuelcollazos41@gmail.com`. El titular completó la verificación en dos pasos. No se inició una prueba gratuita ni se añadió facturación.
4. El ambiente virtual local `.venv` usa Python 3.11 y tiene las dependencias del recolector (`google-api-python-client`, `google-auth-oauthlib`, `tzdata`). **Dieciocho pruebas unitarias** pasaron, incluidas dos para la rotación del secreto y una para la solicitud temporal de evitar suspensión. Esta última se probó también en Windows y se retiró al acabar. La verificación del GTFS comprueba que el ZIP sea íntegro y tenga las tablas básicas; se comprobó con el GTFS aportado anteriormente, de 71.000.036 bytes, y con el de la URL actual, de 120.905.452 bytes, sin modificar ninguno.
5. Se hicieron dos pruebas reales de escritura y lectura en Drive; la segunda, ya con el secreto nuevo, subió un archivo `.pb.gz` de 67 bytes a la carpeta privada y los bytes recuperados coincidieron. Estos archivos **no** son capturas de TransMilenio. El 18-11-2026 se inició la tarea de la tarde a las 16:11 y se comprobó en Drive la carga del GTFS diario íntegro de **120.905.452 bytes**.
6. El 19-11-2026, al faltar la captura de 10:00–12:00 porque el PC estuvo apagado, se inició manualmente el respaldo a las 15:36. La consulta a Drive no encontró archivos `positions` de la mañana; el programa comenzó a subir `positions`, `tripupdates` y `alerts` reales. Las primeras capturas de posiciones se separaron 26 segundos. Esto verifica el arranque y algunos ciclos, **no** todavía la cobertura completa de la franja ni la calidad de todos los registros.

## Ejecución futura

Con las fechas y URL verificadas en `config/captura_local.json`, el programa se inicia desde la raíz del proyecto con `python src/recolectar_a_drive.py --config config/captura_local.json --oauth-cliente RUTA_PRIVADA_DEL_CLIENTE`. La primera autorización, si se aprueba, requiere agregar `--autorizar` y completar el consentimiento en Google. `--franja 10:00-12:00`, `--franja 14:00-16:00` o `--franja 17:00-19:00` permite ejecutar solo una franja habitual. La franja de 14:00–16:00 se captura **aunque también existan datos de 10:00–12:00**. Las franjas nocturnas se definen por fecha en `franjas_adicionales_por_fecha`: `--franja 22:00-23:00` se acepta solo el 21 y el 23; `--franja 21:00-22:00`, solo el 22. Si el PC se enciende a mitad de una franja, capturará solo el tiempo restante. Si se ejecuta fuera de las fechas acordadas, terminará sin descargar nada.

El GTFS se intenta una vez al día y se omite si ya existe. **Se procesa después de la franja de tiempo real** para que descargar y subir el ZIP grande no retrase las posiciones cuando el PC arranca tarde. Antes de subirlo se revisa la integridad del ZIP y la presencia de `agency.txt`, `routes.txt`, `trips.txt`, `stops.txt` y `stop_times.txt`; así no se guarda una descarga truncada como si fuese completa. Durante cada franja se intenta capturar los tres archivos de tiempo real cada 26 segundos; si un ciclo tarda más, no se ejecutan ciclos simultáneos. Los fallos se imprimen y **no** se guardan como datos válidos. Los datos se mantienen privados hasta verificar permisos de redistribución.

Los archivos de tiempo real se guardan como `.pb.gz`: son los mismos bytes `.pb` comprimidos **sin pérdida** en memoria. Se conserva la huella SHA-256 del `.pb` original en la descripción del archivo de Drive. En las tres muestras aportadas, una toma de 8,85 MB pasó a 1,84 MB; a 26 segundos durante las seis horas habituales serían aproximadamente **1,5 GB/día**, y con la hora nocturna **1,75 GB/día**, **solo si el tamaño de las capturas futuras se parece al de esa muestra**. El GTFS diario agrega espacio aparte. El volumen real y la velocidad de subida deben medirse en la prueba.

## Uso desde VS Code

Una vez autorizado, el código puede leer un archivo almacenado en Drive mediante la API y mantenerlo en memoria para analizarlo; la función `leer_archivo_drive` muestra esa ruta. Un archivo grande sigue consumiendo RAM mientras se procesa. Para tablas de varios días conviene descargar o leer por lotes pequeños y agregar resultados, sin replicar todo el histórico en el disco.

En VS Code, después de la autorización inicial y con las dependencias instaladas, se puede usar este ejemplo. El `ID_DEL_ARCHIVO` se obtiene del enlace del archivo concreto en Drive; **no** es el ID de la carpeta.

```python
import json
import os
from pathlib import Path
from src.recolectar_a_drive import credenciales_drive, servicio_drive, leer_archivo_drive

config = json.loads(Path("config/captura_local.json").read_text(encoding="utf-8"))
token = Path(os.environ["LOCALAPPDATA"]) / "Proyecto2TransMilenio" / "drive_token.json"
credenciales = credenciales_drive("RUTA_PRIVADA_DEL_CLIENTE", token)
servicio = servicio_drive(credenciales, config["correo_esperado"])
datos = leer_archivo_drive(servicio, "ID_DEL_ARCHIVO")
print("Bytes leídos desde Drive:", len(datos))

# Para un archivo .pb.gz, recuperar el PB original en memoria:
import gzip
pb_original = gzip.decompress(datos)
```

Esto no crea una copia permanente. Sí usa la conexión a internet y memoria del computador durante la lectura.

## Tareas de Windows registradas

Las tareas `Proyecto2TransMilenio_Manana` y `Proyecto2TransMilenio_Tarde` arrancan diariamente a las **09:55** y **16:55**. El 19-11-2026 se registró `Proyecto2TransMilenio_Respaldo_14a16` para arrancar a las **13:55 del 20 al 23**, hora de Bogotá. **Conserva ese nombre histórico, pero desde el cambio del 21 ejecuta una franja normal cada día, sin consultar la mañana.** Todas vencen después del 23-11-2026, eligen una sola franja, tienen `StartWhenAvailable` y pueden despertar un PC suspendido si está conectado a la corriente. Usan la sesión abierta del usuario (`InteractiveToken`): **no encienden un PC apagado ni funcionan si nadie ha iniciado sesión**. Si el PC arranca tarde, Windows intenta lanzar la tarea perdida, pero el programa omite la franja que ya terminó. El 19 la tarea matutina se ejecutó a las 15:26 con resultado 0, sin recuperar 10:00–12:00; por eso el respaldo de ese día se inició manualmente a las 15:36. La tarde conserva su arranque automático a las 16:55. Conviene dejar el PC enchufado, con la sesión iniciada y la tapa abierta.

Se añadieron dos tareas **de una sola ejecución por fecha**, sin cambiar las anteriores: `Proyecto2TransMilenio_Cierre_22a23` arranca a las **21:55** el sábado 21 y el lunes 23; `Proyecto2TransMilenio_Cierre_Domingo_21a22` arranca a las **20:55** el domingo 22. El recolector espera hasta la hora exacta de inicio y termina al cerrar la franja. Ambas tareas quedaron `Ready`, con `StartWhenAvailable`, `WakeToRun` y sesión interactiva. Se comprobó la configuración y pasaron las pruebas locales; **todavía no hay una captura nocturna real**. El PC debe permanecer encendido o suspendido con corriente, con la sesión iniciada y acceso a internet.

El Programador ejecuta Python **sin abrir una ventana**, de modo que no ver el programa en pantalla no demuestra que esté detenido. Para verificarlo, revisar el estado y `LastTaskResult` de la tarea y comprobar que aparecen archivos nuevos con la hora correcta en `capturas_tiempo_real/AAAA-MM-DD` de Drive. El 21 de noviembre, dos tareas atrasadas arrancaron simultáneamente y crearon carpetas de fecha duplicadas: una carpeta GTFS vacía adicional y una carpeta de tiempo real vacía adicional. La carpeta de tiempo real con datos del 14:00–16:00 conserva **354 archivos** al revisarla. El intento automático de las 17:00 terminó con código 1 porque el recolector anterior rechazaba las carpetas duplicadas. El código local nuevo elige la única carpeta con archivos, o la más antigua si todas están vacías, sin borrar ni mover nada; si varias carpetas duplicadas contienen archivos, se detiene para revisión manual. También omite una tarea cuya franja ya terminó **antes** de crear carpetas. Tras el cambio, se reinició la tarea vespertina y aparecieron capturas nuevas de posiciones, actualizaciones y alertas desde las 17:15. Las carpetas vacías duplicadas permanecen en Drive para no borrar datos sin revisión.

## Posible medición de puntualidad por estación

`stops.txt` contiene las coordenadas de las paradas y `stop_times.txt` las horas previstas por `trip_id` y `stop_id`. Las capturas `positions.pb` contienen la posición y marca de tiempo de cada bus. Una revisión **puntual** del 18-11-2026 a las 16:09 halló 6.326 posiciones, 3.311 de 3.312 `stop_id` del feed en el GTFS del día y 2.518 de 6.325 `trip_id` del feed en ese GTFS. La coincidencia de identificadores debe comprobarse de nuevo por fecha, ruta y servicio antes de comparar horarios.

En esa misma captura no se observó `current_status` en las posiciones ni `stop_time_update` en el feed de actualizaciones. Por ello `stop_id` puede indicar la siguiente parada, no una llegada confirmada. La cercanía del GPS a las coordenadas de una estación permitiría **inferir** un paso usando varias capturas consecutivas, orden de paradas, frescura y un radio calibrado; por sí sola no prueba que el bus se detuvo ni fija una hora exacta de llegada. Solo para viajes con `trip_id` enlazado y horario activo podría calcularse una diferencia aproximada entre paso observado y hora programada; para los demás, conviene medir regularidad por ruta/estación en lugar de incumplimiento individual.
