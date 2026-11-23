"""Prueba de comunicación I-05 e I-06 con procesos HTTP locales."""

import os
import socket
import subprocess
import sys
import tempfile
import time
from contextlib import ExitStack
from pathlib import Path

import httpx


SRC = Path(__file__).resolve().parents[1]
SERVICIO_A = SRC / "servicio-a-elegibilidad"
SERVICIO_B = SRC / "servicio-b-postulaciones"
INTERVALO_REVALIDACION = 60


def comprobar(condicion, detalle):
    if not condicion:
        raise AssertionError(detalle)


def puertos_locales():
    with ExitStack() as stack:
        sockets = [stack.enter_context(socket.socket()) for _ in range(3)]
        for listener in sockets:
            listener.bind(("127.0.0.1", 0))
        return [listener.getsockname()[1] for listener in sockets]


def detener(proceso):
    if proceso.poll() is None:
        proceso.terminate()
        try:
            proceso.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proceso.kill()
            proceso.wait(timeout=5)


def arrancar(stack, logs, nombre, carpeta, modulo, puerto, entorno=None, factory=False):
    destino = logs / f"{nombre}.log"
    salida = stack.enter_context(destino.open("wb"))
    argumentos = [
        sys.executable, "-m", "uvicorn", modulo,
        "--host", "127.0.0.1", "--port", str(puerto),
    ]
    if factory:
        argumentos.append("--factory")
    proceso = subprocess.Popen(
        argumentos,
        cwd=carpeta,
        env={**os.environ, **(entorno or {})},
        stdin=subprocess.DEVNULL,
        stdout=salida,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    stack.callback(detener, proceso)
    return proceso


def esperar_inicio(cliente, url, proceso):
    limite = time.monotonic() + 15
    while proceso.poll() is None and time.monotonic() < limite:
        try:
            if cliente.get(url, timeout=1).status_code == 200:
                return
        except httpx.TransportError:
            pass
        time.sleep(0.15)
    raise RuntimeError(f"El proceso no respondió en {url}")


def postular(cliente, url, estudiante):
    respuesta = cliente.post(
        f"{url}/postulaciones", json={"estudianteId": estudiante, "asignatura": "ASIG-01"}
    )
    comprobar(respuesta.status_code == 201, f"{estudiante}: {respuesta.status_code} {respuesta.text}")
    return respuesta.json()


def comprobar_flujo(tmp):
    sga_port, a_port, b_port = puertos_locales()
    sga, servicio_a, servicio_b = (
        f"http://127.0.0.1:{puerto}/api/v1" for puerto in (sga_port, a_port, b_port)
    )
    registro_sga = f"{sga}/estudiantes/EST-001/registro-academico?asignatura=ASIG-01"

    with ExitStack() as stack:
        cliente = stack.enter_context(httpx.Client(timeout=5, trust_env=False))
        simulador = arrancar(stack, tmp, "sga", SERVICIO_A, "app.sga_simulado:app", sga_port)
        esperar_inicio(cliente, registro_sga, simulador)

        a = arrancar(
            stack, tmp, "elegibilidad", SERVICIO_A, "app.main:crear_app", a_port,
            {"SGA_URL": sga}, factory=True,
        )
        esperar_inicio(cliente, f"{servicio_a}/salud", a)
        b = arrancar(
            stack, tmp, "postulaciones", SERVICIO_B, "app.main:crear_app", b_port,
            {
                "ELEGIBILIDAD_URL": servicio_a,
                "ELEGIBILIDAD_TIEMPO_ESPERA": "3",
                "REVALIDACION_SEGUNDOS": str(INTERVALO_REVALIDACION),
                "POSTULACIONES_BD": str(tmp / "postulaciones.sqlite3"),
            },
            factory=True,
        )
        esperar_inicio(cliente, f"{servicio_b}/salud", b)

        resultados = (
            ("EST-001", "ELEGIBLE"),
            ("EST-003", "NO_ELEGIBLE"),
            ("EST-008", "INCOMPLETO"),
        )
        for estudiante, esperado in resultados:
            fila = postular(cliente, servicio_b, estudiante)
            comprobar(
                fila["estado"] == "Enviada"
                and fila["estadoValidacion"] == "Validada"
                and (fila["elegibilidad"] or {}).get("estadoGeneral") == esperado,
                fila,
            )
            print(f"{estudiante}: A devolvió {esperado} y B registró el resultado.", flush=True)

        sin_registro = postular(cliente, servicio_b, "EST-999")
        comprobar(sin_registro["estadoValidacion"] == "Sin registro académico", sin_registro)
        print("EST-999: B distinguió la respuesta 404.", flush=True)

        detener(simulador)
        falla = cliente.get(f"{servicio_a}/estudiantes/EST-002/elegibilidad?asignatura=ASIG-01")
        comprobar(
            falla.status_code == 503
            and falla.json()["codigo"] == "SGA_NO_DISPONIBLE"
            and falla.headers.get("Retry-After") == str(INTERVALO_REVALIDACION),
            falla.text,
        )
        fila = postular(cliente, servicio_b, "EST-002")
        comprobar(
            fila["estado"] == "Enviada"
            and fila["estadoValidacion"] == "Validación pendiente"
            and fila["elegibilidad"] is None,
            fila,
        )
        print("SGA detenido: A devolvió 503 y B conservó la postulación pendiente.", flush=True)

        recuperado = arrancar(
            stack, tmp, "sga-recuperado", SERVICIO_A, "app.sga_simulado:app", sga_port
        )
        esperar_inicio(cliente, registro_sga, recuperado)
        print(f"SGA recuperado. Intervalo configurado en B: {INTERVALO_REVALIDACION} s.", flush=True)
        inicio = time.monotonic()
        limite = inicio + INTERVALO_REVALIDACION + 15
        while time.monotonic() < limite:
            respuesta = cliente.get(f"{servicio_b}/postulaciones/{fila['id']}")
            respuesta.raise_for_status()
            actual = respuesta.json()
            if actual["estadoValidacion"] == "Validada":
                comprobar(actual["elegibilidad"]["estadoGeneral"] == "ELEGIBLE", actual)
                candidatos = cliente.get(f"{servicio_b}/postulaciones")
                candidatos.raise_for_status()
                coincidencias = [
                    p["id"] for p in candidatos.json() if p["estudianteId"] == "EST-002"
                ]
                comprobar(coincidencias == [fila["id"]], coincidencias)
                print(f"B revalidó el mismo registro sin duplicados en {time.monotonic()-inicio:.1f} s.")
                break
            time.sleep(0.5)
        else:
            raise AssertionError(f"B no revalidó la postulación {fila['id']} tras recuperar el SGA.")

    solicitudes = [
        linea.split("SGA simulado: ", 1)[1]
        for nombre in ("sga", "sga-recuperado")
        for linea in (tmp / f"{nombre}.log").read_text(encoding="utf-8", errors="replace").splitlines()
        if "SGA simulado: " in linea
    ]
    comprobar(solicitudes and all(ruta.startswith("GET ") for ruta in solicitudes), solicitudes)
    print(f"SGA: {len(solicitudes)} lecturas registradas (incluye comprobaciones de arranque), 0 escrituras.")
    print("Prueba de comunicación superada.")


def main():
    with tempfile.TemporaryDirectory(prefix="sgac-comunicacion-") as temporal:
        tmp = Path(temporal)
        try:
            comprobar_flujo(tmp)
        except (AssertionError, RuntimeError, httpx.HTTPError):
            for log in sorted(tmp.glob("*.log")):
                print(f"--- {log.name} ---", file=sys.stderr)
                for linea in log.read_text(encoding="utf-8", errors="replace").splitlines()[-12:]:
                    print(linea, file=sys.stderr)
            raise


if __name__ == "__main__":
    main()
