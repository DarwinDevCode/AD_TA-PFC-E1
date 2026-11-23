import json
import sqlite3
import threading
from datetime import datetime, timezone

ENVIADA = "Enviada"
VALIDACION_PENDIENTE = "Validación pendiente"
VALIDADA = "Validada"
SIN_REGISTRO_ACADEMICO = "Sin registro académico"


class PostulacionDuplicada(Exception):
    pass


def ahora() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class RepositorioPostulaciones:
    def __init__(self, ruta: str):
        self._conexion = sqlite3.connect(ruta, check_same_thread=False)
        self._conexion.row_factory = sqlite3.Row
        self._bloqueo = threading.Lock()
        with self._bloqueo, self._conexion:
            self._conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS postulaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    estudiante_id TEXT NOT NULL,
                    asignatura TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    estado_validacion TEXT NOT NULL,
                    elegibilidad TEXT,
                    fecha_registro TEXT NOT NULL,
                    fecha_validacion TEXT,
                    UNIQUE (estudiante_id, asignatura)
                )
                """
            )

    def crear(self, estudiante_id: str, asignatura: str) -> dict:
        try:
            with self._bloqueo, self._conexion:
                cursor = self._conexion.execute(
                    "INSERT INTO postulaciones (estudiante_id, asignatura, estado, estado_validacion, fecha_registro)"
                    " VALUES (?, ?, ?, ?, ?)",
                    (estudiante_id, asignatura, ENVIADA, VALIDACION_PENDIENTE, ahora()),
                )
        except sqlite3.IntegrityError as error:
            raise PostulacionDuplicada from error
        return self.obtener(cursor.lastrowid)

    def obtener(self, postulacion_id: int) -> dict | None:
        with self._bloqueo:
            fila = self._conexion.execute("SELECT * FROM postulaciones WHERE id = ?", (postulacion_id,)).fetchone()
        return self._a_dict(fila) if fila else None

    def listar(self) -> list[dict]:
        with self._bloqueo:
            filas = self._conexion.execute("SELECT * FROM postulaciones ORDER BY id").fetchall()
        return [self._a_dict(f) for f in filas]

    def pendientes(self) -> list[dict]:
        with self._bloqueo:
            filas = self._conexion.execute(
                "SELECT * FROM postulaciones WHERE estado_validacion = ? ORDER BY id", (VALIDACION_PENDIENTE,)
            ).fetchall()
        return [self._a_dict(f) for f in filas]

    def registrar_validacion(self, postulacion_id: int, estado_validacion: str, elegibilidad: dict | None) -> None:
        with self._bloqueo, self._conexion:
            self._conexion.execute(
                "UPDATE postulaciones SET estado_validacion = ?, elegibilidad = ?, fecha_validacion = ? WHERE id = ?",
                (estado_validacion, json.dumps(elegibilidad) if elegibilidad else None, ahora(), postulacion_id),
            )

    def cerrar(self) -> None:
        self._conexion.close()

    @staticmethod
    def _a_dict(fila: sqlite3.Row) -> dict:
        return {
            "id": fila["id"],
            "estudianteId": fila["estudiante_id"],
            "asignatura": fila["asignatura"],
            "estado": fila["estado"],
            "estadoValidacion": fila["estado_validacion"],
            "elegibilidad": json.loads(fila["elegibilidad"]) if fila["elegibilidad"] else None,
            "fechaRegistro": fila["fecha_registro"],
            "fechaValidacion": fila["fecha_validacion"],
        }
