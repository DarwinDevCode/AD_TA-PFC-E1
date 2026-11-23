# Servicio A: elegibilidad

Implementa la consulta académica de RF-03. Recibe solicitudes de postulaciones por [I-05](../contrato/elegibilidad-v1.yaml) y consulta el [SGA simulado por I-06](../contrato/sga-simulado-v1.yaml). El simulador se ejecuta como un proceso separado y usa registros sintéticos de la asignatura `ASIG-01`.

## Instalación y arranque

Desde `src/servicio-a-elegibilidad/`, con Python 3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-dev.txt
```

En dos terminales, desde la misma carpeta, iniciar primero el simulador y después elegibilidad:

```powershell
.\.venv\Scripts\python -m uvicorn app.sga_simulado:app --port 8090
```

```powershell
.\.venv\Scripts\python -m uvicorn app.main:crear_app --factory --port 8081
```

En Linux o macOS, usar `python3 -m venv .venv` y `.venv/bin/python` en los comandos restantes. La URL del SGA simulado puede cambiarse con `SGA_URL`; por defecto es `http://localhost:8090/api/v1`.

## Consultas y pruebas

```powershell
curl.exe http://localhost:8081/api/v1/salud
curl.exe "http://localhost:8081/api/v1/estudiantes/EST-001/elegibilidad?asignatura=ASIG-01"
.\.venv\Scripts\python -m pytest
```

La primera consulta devuelve `200` y `{"estado":"OK"}`. La segunda devuelve `200` y `estadoGeneral: ELEGIBLE` para el registro de ejemplo. Una consulta válida de un estudiante sin registro devuelve `404`. Si el SGA falla o agota los 2 segundos, elegibilidad devuelve `503` y `Retry-After: 60`. Los reintentos de la postulación corresponden al servicio B.

La prueba de solo lectura puede seguirse en el registro de solicitudes del SGA simulado. Los resultados esperados se documentan en los [casos de prueba](../pruebas/casos-servicio-a.md).
