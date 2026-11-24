import json
import gzip
import io
import os
import tempfile
import unittest
import zipfile
from datetime import date, datetime
from pathlib import Path
from unittest.mock import MagicMock, call, patch

from src.recolectar_a_drive import ZONA, archivo_existe, buscar_o_crear_carpeta, comprimir_pb, descargar_bytes, fecha_permitida, franjas_para_fecha, impedir_suspension_mientras_captura, leer_archivo_drive, leer_configuracion, preparar_token_para_cliente, recolectar_dia, restaurar_suspension, separar_franja


class RespuestaFalsa:
    def __init__(self, contenido, tipo):
        self.contenido = contenido
        self.headers = {"Content-Type": tipo}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.contenido


class PruebasRecolector(unittest.TestCase):
    def crear_gtfs_zip(self, tablas=None):
        if tablas is None:
            tablas = ("agency.txt", "routes.txt", "trips.txt", "stops.txt", "stop_times.txt")
        salida = io.BytesIO()
        with zipfile.ZipFile(salida, "w") as archivo:
            for tabla in tablas:
                archivo.writestr(tabla, "ejemplo")
        return salida.getvalue()

    def test_franja(self):
        inicio, fin = separar_franja("06:00-08:30")
        self.assertLess(inicio, fin)

    def test_sin_franjas_no_inicia(self):
        datos = {"correo_esperado": "ejemplo@correo.com", "carpeta_drive_id": "id", "franjas": []}
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "config.json"
            ruta.write_text(json.dumps(datos), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "franjas"):
                leer_configuracion(ruta)

    def test_url_no_verificada_no_inicia(self):
        datos = {"correo_esperado": "ejemplo@correo.com", "carpeta_drive_id": "id",
                 "franjas": ["06:00-07:00"], "fuentes": {}}
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "config.json"
            ruta.write_text(json.dumps(datos), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "HTTPS"):
                leer_configuracion(ruta)

    def test_intervalo_de_fechas(self):
        datos = {"fecha_inicio": "2026-11-23", "fecha_fin": "2026-11-29"}
        self.assertFalse(fecha_permitida(datos, date(2026, 11, 22)))
        self.assertTrue(fecha_permitida(datos, date(2026, 11, 23)))
        self.assertTrue(fecha_permitida(datos, date(2026, 11, 29)))
        self.assertFalse(fecha_permitida(datos, date(2026, 11, 30)))

    def test_franjas_de_cierre_segun_el_dia(self):
        datos = {
            "franjas": ["10:00-12:00", "17:00-19:00"],
            "franjas_adicionales_por_fecha": {
                "2026-11-21": ["22:00-23:00"],
                "2026-11-22": ["21:00-22:00"],
                "2026-11-23": ["22:00-23:00"],
            },
        }
        self.assertIn("22:00-23:00", franjas_para_fecha(datos, date(2026, 11, 21)))
        self.assertIn("21:00-22:00", franjas_para_fecha(datos, date(2026, 11, 22)))
        self.assertNotIn("22:00-23:00", franjas_para_fecha(datos, date(2026, 11, 22)))
        self.assertIn("22:00-23:00", franjas_para_fecha(datos, date(2026, 11, 23)))
        self.assertNotIn("22:00-23:00", franjas_para_fecha(datos, date(2026, 11, 20)))

    def test_la_franja_de_14_a_16_es_diaria(self):
        datos = {"franjas": ["10:00-12:00", "14:00-16:00", "17:00-19:00"]}
        self.assertIn("14:00-16:00", franjas_para_fecha(datos, date(2026, 11, 21)))
        self.assertIn("14:00-16:00", franjas_para_fecha(datos, date(2026, 11, 22)))
        self.assertNotIn("respaldo", datos)

    def test_captura_de_14_a_16_no_depende_de_la_manana(self):
        datos = {
            "franjas": ["10:00-12:00", "14:00-16:00", "17:00-19:00"],
            "fecha_inicio": "2026-11-21", "fecha_fin": "2026-11-23",
            "carpeta_drive_id": "carpeta", "cada_segundos": 26,
        }
        servicio = MagicMock()
        servicio.files.return_value.list.return_value.execute.return_value = {
            "files": [{"name": "positions_20261122T103000-0500.pb.gz"}]
        }
        reloj_antes = datetime(2026, 11, 22, 15, 0, tzinfo=ZONA)
        reloj_fin = datetime(2026, 11, 22, 16, 0, tzinfo=ZONA)
        with patch("src.recolectar_a_drive.datetime", wraps=datetime) as reloj, \
             patch("src.recolectar_a_drive.buscar_o_crear_carpeta", return_value="carpeta"), \
             patch("src.recolectar_a_drive.archivo_existe", return_value=True), \
             patch("src.recolectar_a_drive.capturar_una_vez") as capturar, \
             patch("src.recolectar_a_drive.time.monotonic", side_effect=[10, 10.1]), \
             patch("src.recolectar_a_drive.time.sleep"):
            reloj.now.side_effect = [reloj_antes, reloj_antes, reloj_antes,
                                     reloj_antes, reloj_antes, reloj_fin]
            recolectar_dia(servicio, datos, "14:00-16:00")
        capturar.assert_called_once()

    def test_gtfs_no_retrasa_la_captura_en_tiempo_real(self):
        datos = {
            "franjas": ["14:00-16:00"],
            "fecha_inicio": "2026-11-21", "fecha_fin": "2026-11-23",
            "carpeta_drive_id": "carpeta", "cada_segundos": 26,
            "fuentes": {"gtfs": "https://ejemplo.test/GTFS.zip"},
        }
        eventos = []
        reloj_antes = datetime(2026, 11, 22, 15, 0, tzinfo=ZONA)
        reloj_fin = datetime(2026, 11, 22, 16, 0, tzinfo=ZONA)
        with patch("src.recolectar_a_drive.datetime", wraps=datetime) as reloj, \
             patch("src.recolectar_a_drive.buscar_o_crear_carpeta", return_value="carpeta"), \
             patch("src.recolectar_a_drive.archivo_existe", return_value=False), \
             patch("src.recolectar_a_drive.capturar_una_vez") as capturar, \
             patch("src.recolectar_a_drive.descargar_bytes") as descargar, \
             patch("src.recolectar_a_drive.subir_bytes"), \
             patch("src.recolectar_a_drive.time.monotonic", side_effect=[10, 10.1]), \
             patch("src.recolectar_a_drive.time.sleep"):
            reloj.now.side_effect = [reloj_antes, reloj_antes, reloj_antes,
                                     reloj_antes, reloj_antes, reloj_fin, reloj_fin]
            capturar.side_effect = lambda *args: eventos.append("tiempo_real")
            descargar.side_effect = lambda *args: eventos.append("gtfs") or b"zip"
            recolectar_dia(MagicMock(), datos, "14:00-16:00")
        self.assertEqual(eventos, ["tiempo_real", "gtfs"])

    def test_el_domingo_no_inicia_la_franja_de_las_22(self):
        datos = {
            "franjas": ["10:00-12:00", "17:00-19:00"],
            "franjas_adicionales_por_fecha": {"2026-11-22": ["21:00-22:00"]},
        }
        with patch("src.recolectar_a_drive.datetime") as reloj:
            reloj.now.return_value = datetime(2026, 11, 22, 20, 55, tzinfo=ZONA)
            with self.assertRaisesRegex(ValueError, "no está en la configuración"):
                recolectar_dia(None, datos, "22:00-23:00")

    def test_franja_adicional_solapada_se_rechaza(self):
        datos = {
            "correo_esperado": "ejemplo@correo.com", "carpeta_drive_id": "id",
            "franjas": ["10:00-12:00", "17:00-19:00"],
            "franjas_adicionales_por_fecha": {"2026-11-21": ["18:00-20:00"]},
            "fuentes": {nombre: "https://ejemplo.test/datos" for nombre in ("positions", "tripupdates", "alerts", "gtfs")},
            "fecha_inicio": "2026-11-18", "fecha_fin": "2026-11-23",
        }
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "config.json"
            ruta.write_text(json.dumps(datos), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "solaparse"):
                leer_configuracion(ruta)

    def test_franja_no_configurada_se_rechaza(self):
        with self.assertRaisesRegex(ValueError, "no está en la configuración"):
            recolectar_dia(None, {"franjas": ["06:30-08:30"]}, "17:00-19:00")

    def test_franja_pasada_no_crea_carpetas(self):
        datos = {
            "franjas": ["10:00-12:00"],
            "fecha_inicio": "2026-11-21", "fecha_fin": "2026-11-23",
            "carpeta_drive_id": "carpeta", "cada_segundos": 26,
        }
        with patch("src.recolectar_a_drive.datetime", wraps=datetime) as reloj, \
             patch("src.recolectar_a_drive.buscar_o_crear_carpeta") as crear:
            reloj.now.return_value = datetime(2026, 11, 21, 15, 0, tzinfo=ZONA)
            recolectar_dia(None, datos, "10:00-12:00")
        crear.assert_not_called()

    def test_carpeta_duplicada_elige_la_que_tiene_archivos(self):
        servicio = MagicMock()
        servicio.files.return_value.list.return_value.execute.side_effect = [
            {"files": [{"id": "vacia", "createdTime": "2026-11-21T20:08:39Z"},
                       {"id": "con_datos", "createdTime": "2026-11-21T20:08:40Z"}]},
            {"files": []},
            {"files": [{"id": "archivo"}]},
        ]
        self.assertEqual(buscar_o_crear_carpeta(servicio, "2026-11-21", "padre"), "con_datos")
        servicio.files.return_value.create.assert_not_called()

    def test_carpeta_duplicada_vacia_elige_la_mas_antigua(self):
        servicio = MagicMock()
        servicio.files.return_value.list.return_value.execute.side_effect = [
            {"files": [{"id": "nueva", "createdTime": "2026-11-21T20:08:40Z"},
                       {"id": "antigua", "createdTime": "2026-11-21T20:08:39Z"}]},
            {"files": []},
            {"files": []},
        ]
        self.assertEqual(buscar_o_crear_carpeta(servicio, "2026-11-21", "padre"), "antigua")

    def test_carpeta_duplicada_con_datos_en_ambas_se_detiene(self):
        servicio = MagicMock()
        servicio.files.return_value.list.return_value.execute.side_effect = [
            {"files": [{"id": "una"}, {"id": "otra"}]},
            {"files": [{"id": "archivo_1"}]},
            {"files": [{"id": "archivo_2"}]},
        ]
        with self.assertRaisesRegex(RuntimeError, "requieren revisión manual"):
            buscar_o_crear_carpeta(servicio, "2026-11-21", "padre")

    def test_franjas_habituales_no_se_solapan(self):
        datos = {
            "correo_esperado": "ejemplo@correo.com", "carpeta_drive_id": "id",
            "franjas": ["10:00-12:00", "14:00-16:00", "17:00-19:00"],
            "fuentes": {nombre: "https://ejemplo.test/datos" for nombre in ("positions", "tripupdates", "alerts", "gtfs")},
            "fecha_inicio": "2026-11-18", "fecha_fin": "2026-11-23",
        }
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "config.json"
            ruta.write_text(json.dumps(datos), encoding="utf-8")
            self.assertIn("14:00-16:00", leer_configuracion(ruta)["franjas"])
            datos["franjas"][1] = "11:00-13:00"
            ruta.write_text(json.dumps(datos), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "solaparse"):
                leer_configuracion(ruta)

    def test_cadencia_incorrecta_se_rechaza_antes_de_subir(self):
        with self.assertRaisesRegex(ValueError, "26 segundos"):
            recolectar_dia(None, {"franjas": ["06:30-08:30"], "cada_segundos": 30})

    def test_mantenimiento_no_se_guarda_como_datos(self):
        respuesta = RespuestaFalsa(b"<html>Mantenimiento</html>", "text/html")
        with patch("src.recolectar_a_drive.urlopen", return_value=respuesta):
            with self.assertRaisesRegex(ValueError, "mantenimiento"):
                descargar_bytes("https://ejemplo.test/positions.pb", "positions")

    def test_zip_valido(self):
        gtfs = self.crear_gtfs_zip()
        respuesta = RespuestaFalsa(gtfs, "application/zip")
        with patch("src.recolectar_a_drive.urlopen", return_value=respuesta):
            self.assertEqual(descargar_bytes("https://ejemplo.test/GTFS.zip", "gtfs"), gtfs)

    def test_zip_truncado_no_se_sube(self):
        respuesta = RespuestaFalsa(self.crear_gtfs_zip()[:-30], "application/zip")
        with patch("src.recolectar_a_drive.urlopen", return_value=respuesta):
            with self.assertRaisesRegex(ValueError, "incompleto o dañado"):
                descargar_bytes("https://ejemplo.test/GTFS.zip", "gtfs")

    def test_zip_sin_tabla_necesaria_no_se_sube(self):
        gtfs = self.crear_gtfs_zip(("agency.txt", "routes.txt", "trips.txt", "stops.txt"))
        respuesta = RespuestaFalsa(gtfs, "application/zip")
        with patch("src.recolectar_a_drive.urlopen", return_value=respuesta):
            with self.assertRaisesRegex(ValueError, "stop_times.txt"):
                descargar_bytes("https://ejemplo.test/GTFS.zip", "gtfs")

    def test_pb_valido_con_tipo_texto_del_servidor(self):
        datos = b"\x0a\x0d\x0a\x03" + b"2.0\x10" + b"contenido"
        respuesta = RespuestaFalsa(datos, "text/plain")
        with patch("src.recolectar_a_drive.urlopen", return_value=respuesta):
            self.assertEqual(descargar_bytes("https://ejemplo.test/positions.pb", "positions"), datos)

    def test_texto_no_se_guarda_como_pb(self):
        respuesta = RespuestaFalsa(b"Servicio temporalmente suspendido", "text/plain")
        with patch("src.recolectar_a_drive.urlopen", return_value=respuesta):
            with self.assertRaisesRegex(ValueError, "GTFS-Realtime"):
                descargar_bytes("https://ejemplo.test/positions.pb", "positions")

    def test_compresion_sin_perdida(self):
        original = b"datos de ejemplo" * 100
        comprimido = comprimir_pb(original)
        self.assertEqual(gzip.decompress(comprimido), original)
        self.assertLess(len(comprimido), len(original))

    def test_lectura_desde_drive_devuelve_bytes(self):
        servicio = MagicMock()
        servicio.files.return_value.get_media.return_value.execute.return_value = b"datos remotos"
        self.assertEqual(leer_archivo_drive(servicio, "id-de-prueba"), b"datos remotos")
        servicio.files.return_value.get_media.assert_called_once_with(fileId="id-de-prueba")

    def test_busquedas_drive_usan_page_size_oficial(self):
        servicio = MagicMock()
        servicio.files.return_value.list.return_value.execute.return_value = {"files": []}
        self.assertFalse(archivo_existe(servicio, "prueba.pb.gz", "carpeta"))
        self.assertEqual(servicio.files.return_value.list.call_args.kwargs["pageSize"], 1)

        servicio.files.return_value.create.return_value.execute.return_value = {"id": "nueva"}
        self.assertEqual(buscar_o_crear_carpeta(servicio, "2026-11-18", "padre"), "nueva")
        self.assertEqual(servicio.files.return_value.list.call_args.kwargs["pageSize"], 10)

    def test_rotacion_de_secreto_mantiene_el_cliente(self):
        anterior = {"client_id": "mismo-cliente", "client_secret": "anterior", "refresh_token": "ejemplo"}
        nuevo = {"client_id": "mismo-cliente", "client_secret": "nuevo"}
        actualizado = preparar_token_para_cliente(anterior, nuevo)
        self.assertEqual(actualizado["client_secret"], "nuevo")
        self.assertEqual(actualizado["refresh_token"], "ejemplo")
        self.assertEqual(anterior["client_secret"], "anterior")

    def test_rotacion_rechaza_otro_cliente(self):
        anterior = {"client_id": "cliente-a", "client_secret": "anterior"}
        nuevo = {"client_id": "cliente-b", "client_secret": "nuevo"}
        with self.assertRaisesRegex(RuntimeError, "otro cliente"):
            preparar_token_para_cliente(anterior, nuevo)

    def test_suspension_se_impide_solo_durante_la_captura(self):
        if os.name != "nt":
            self.skipTest("La prueba corresponde a Windows")
        with patch("src.recolectar_a_drive.ctypes.WinDLL") as biblioteca:
            funcion = biblioteca.return_value.SetThreadExecutionState
            funcion.return_value = 1
            solicitud = impedir_suspension_mientras_captura()
            restaurar_suspension(solicitud)
            self.assertEqual(funcion.call_args_list, [call(0x80000001), call(0x80000000)])


if __name__ == "__main__":
    unittest.main()
