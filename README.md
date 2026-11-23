# Sistema de Gestión de Ayudantías de Cátedra (SGAC)

**Actividad:** TA-PFC-E1 — Proyecto Fin de Curso de Aplicaciones Distribuidas.

## Descripción del proyecto

El SGAC es una propuesta para gestionar convocatorias, postulaciones, evaluación, seguimiento y certificación de ayudantes de cátedra en la UTEQ. La arquitectura definida en ADR-001 separa servicios por capacidad de negocio. La integración con el SGA se simula con consultas de solo lectura; no se utiliza acceso a registros institucionales reales.

## Integrantes y roles

| Integrante | Rol |
| --- | --- |
| SANCHEZ VERA DARWIN JOEL | Arquitecto |
| MUÑOZ VERA MELANIE MICHELLE | Líder de Desarrollo y Responsable de Calidad (dos roles) |
| QUINTERO RICO LUIS DAVID | Responsable de Documentación |

**Periodo académico consignado en la portada:** octubre de 2026 – febrero de 2027. Confirmación institucional de los roles: PENDIENTE DE DEFINIR.

**Link del video:** https://drive.google.com/drive/folders/1cz2WF7eTlp2MVnRtzyxq3t1MDS0v-Pkc?usp=drive_link

## Aportes de Melanie Muñoz Vera a E1

- **Desarrollo:** implementó el [servicio A de elegibilidad](src/servicio-a-elegibilidad/README.md) y el SGA simulado de solo lectura. Preparó los [14 casos de elegibilidad](src/pruebas/casos-servicio-a.md) según el contrato OpenAPI y verificó la comunicación con el servicio B de postulaciones.
- **Calidad:** documentó [12 requisitos no funcionales](docs/secciones/06-requisitos-no-funcionales.tex) y su [matriz de pruebas](src/pruebas/matriz-pruebas-rnf.md), [siete riesgos técnicos](docs/secciones/12-analisis-riesgos.tex) y la [matriz de trazabilidad](docs/matriz-trazabilidad.md) entre RF, RNF, C4, ADR y CAP/PACELC. Las cifras sujetas a validación institucional siguen siendo provisionales.
- **Evidencia de integración:** documentó los resultados en la [sección 14](docs/secciones/14-esqueleto-funcional.tex). Al restablecer el SGA simulado, se revalidaron las 20 postulaciones sintéticas, con 0 pérdidas y 0 duplicados.

## Estructura del repositorio

- `src/`: contratos, servicios y pruebas del esqueleto funcional.
- `docs/`: documento LaTeX, secciones, bibliografía y PDF compilado.
- `docs/adr/`: decisiones arquitectónicas ADR-001 y ADR-002.
- `docs/diagramas/`: archivos editables de los niveles C4.
- `evidencias/`: levantamiento, sesiones de diseño y capturas.
- `BITACORA.md`: registro de sesiones y decisiones reales del equipo.
- `README.md`: orientación para la ejecución y la documentación.

## Ejecución del esqueleto

### Instalación

Usa Python 3.12 y ejecuta los comandos desde la raíz del repositorio.

En Windows (PowerShell):

```powershell
py -3.12 -m venv src/servicio-a-elegibilidad/.venv
$pythonSGAC = '.\src\servicio-a-elegibilidad\.venv\Scripts\python.exe'
& $pythonSGAC -m pip install -r src/servicio-a-elegibilidad/requirements.txt -r src/servicio-b-postulaciones/requirements.txt
& $pythonSGAC -X utf8 src/pruebas/prueba-comunicacion.py
```

En Linux o macOS:

```sh
python3.12 -m venv src/servicio-a-elegibilidad/.venv
python_sgac=src/servicio-a-elegibilidad/.venv/bin/python
"$python_sgac" -m pip install -r src/servicio-a-elegibilidad/requirements.txt -r src/servicio-b-postulaciones/requirements.txt
"$python_sgac" -X utf8 src/pruebas/prueba-comunicacion.py
```

### Prueba de comunicación

La prueba arranca el SGA simulado, elegibilidad (A) y postulaciones (B)
en puertos locales disponibles. Usa datos sintéticos y una base SQLite
temporal. Cuenta con el intervalo de revalidación de 60 segundos, por lo
que puede tardar algo más de un minuto.

El resultado esperado es `Prueba de comunicación superada.` Se comprueban
los resultados de elegibilidad, la respuesta de estudiante sin registro,
el `503` al detener el SGA y la revalidación de la misma postulación
cuando el SGA vuelve a estar disponible. Al terminar se comprueba que
el simulador recibió solo lecturas.

### Arranque manual

En tres terminales, desde la carpeta indicada, ejecuta cada comando con
el Python del entorno virtual anterior. Inicia primero el SGA y el
servicio A, y luego el servicio B.

| Carpeta | Comando de Python | Puerto local |
| --- | --- | --- |
| `src/servicio-a-elegibilidad` | `python -m uvicorn app.sga_simulado:app --port 8090` | 8090 |
| `src/servicio-a-elegibilidad` | `python -m uvicorn app.main:crear_app --factory --port 8081` | 8081 |
| `src/servicio-b-postulaciones` | `python -m uvicorn app.main:crear_app --factory --port 8080` | 8080 |

Las operaciones y variables de configuración están en los README de
[elegibilidad](src/servicio-a-elegibilidad/README.md) y
[postulaciones](src/servicio-b-postulaciones/README.md).

## Compilación del documento

- **Compilador:** `pdflatex` y `biber`.
- **Archivo principal:** `docs/main.tex`.
- **Dependencias:** TeX Live o MiKTeX con `pdflatex`, `biber`, `inputenc` UTF-8, `fontenc` T1, `lmodern`, `babel` español, `csquotes`, `geometry`, `graphicx`, `booktabs`, `tabularx`, `longtable`, `hyperref`, `biblatex` y `biblatex-ieee`.

Desde `docs/` ejecutar, en este orden:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
biber main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

El resultado es `docs/main.pdf`. En MiKTeX, las versiones de `biber` y `biblatex` deben ser compatibles. Para una entrega reproducible, el proceso debe funcionar en un clon limpio y sin referencias sin resolver (`??`).

## Estado de la documentación para E1

El informe se integra desde [`docs/main.tex`](docs/main.tex) en un solo documento LaTeX. Las secciones de contexto, objetivos y los doce requisitos funcionales están incorporadas a `main` mediante el [PR #11](https://github.com/DarwinDevCode/AD_TA-PFC-E1/pull/11). El levantamiento se integró mediante el [PR #10](https://github.com/DarwinDevCode/AD_TA-PFC-E1/pull/10). La sección de calidad, el esqueleto y las capturas también están integrados.

| Entregable | Archivo o evidencia | Estado registrado |
| --- | --- | --- |
| Documento y PDF integrado | [`docs/main.tex`](docs/main.tex), [`docs/main.pdf`](docs/main.pdf) | PDF actualizado en el [PR #56](https://github.com/DarwinDevCode/AD_TA-PFC-E1/pull/56); falta la comprobación en clon limpio del issue #38. |
| Levantamiento | [Guion y acta](evidencias/levantamiento/) | Archivos publicados en `main`. La firma o grabación con consentimiento y el contraste de respuestas reales siguen pendientes de acreditar. |
| Contexto, objetivos y doce RF | [Secciones 02, 03 y 05](docs/secciones/) | Redactados e integrados. La trazabilidad a fuentes reales se revisa en el [issue #6](https://github.com/DarwinDevCode/AD_TA-PFC-E1/issues/6). |
| Plan, portada, aportes e IA | [Secciones 00, 13, 15 y 16](docs/secciones/) | Integradas, con tareas de verificación documental en #35, #36 y #37; Darwin debe completar su declaración individual si corresponde. |
| Requisitos no funcionales y riesgos | [Secciones 06 y 12](docs/secciones/) | Integrados con metas cuantificadas provisionales. |
| Servicios y pruebas | [`src/`](src/) | Servicio A, servicio B, SGA simulado y prueba de comunicación reproducible disponibles. |
| Capturas | [Tres capturas de ejecución](evidencias/capturas/) | Registradas en el [PR #55](https://github.com/DarwinDevCode/AD_TA-PFC-E1/pull/55). |
| Video | [Carpeta de video](https://drive.google.com/drive/folders/1cz2WF7eTlp2MVnRtzyxq3t1MDS0v-Pkc?usp=drive_link) | Enlace incorporado al repositorio; verificar el acceso anónimo y la duración de 5 a 7 minutos. |

Las cifras de capacidad, disponibilidad, rendimiento y recuperación son **metas de diseño propuestas**; no equivalen a mediciones institucionales de la UTEQ ni a respuestas comprobadas del entrevistado.

## Comprobaciones para el cierre

Antes de entregar E1, acreditar la entrevista con firma o grabación consentida, completar las sesiones reales de la bitácora, comprobar el esqueleto y la compilación LaTeX desde un clon limpio, revisar los DOI y verificar que el video ya enlazado sea público y cumpla la duración exigida. El PDF de identificación para el SGA debe tener una sola página.

## Organización y trazabilidad

- [Issues del repositorio](https://github.com/DarwinDevCode/AD_TA-PFC-E1/issues).
- [Decisiones de arquitectura](docs/adr/).
- [Documento LaTeX](docs/main.tex).
- [Trabajo de levantamiento](evidencias/levantamiento/): la conformidad de la entrevista debe acreditarse antes de declararlo validado.
- **Tablero GitHub Projects E1–E4:** [SGAC — Plan del proyecto](https://github.com/users/DarwinDevCode/projects/14). El enlace específico a la vista «Cronograma» sigue pendiente de comprobación.
