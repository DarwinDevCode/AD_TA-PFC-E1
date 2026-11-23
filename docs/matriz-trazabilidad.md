# Matriz de trazabilidad del SGAC

Matriz preliminar de TA-PFC-E1. Los RF se identifican con la numeración de la planificación del equipo mientras la [sección de requisitos funcionales](secciones/05-requisitos-funcionales.tex) se completa con el acta. Los [RNF](secciones/06-requisitos-no-funcionales.tex) conservan sus cifras provisionales. Los ADR-001 y ADR-002 figuran como propuestos en la versión revisada.

Las interacciones I-01 a I-13 corresponden al [C4 de contenedores](secciones/08-arquitectura-c4.tex) y al [modelo de comunicación](secciones/09-modelo-comunicacion.tex). CAP/PACELC se refiere a las decisiones por dato crítico de la [sección de análisis](secciones/10-analisis-cap-pacelc.tex). Los RNF marcados con asterisco son vínculos propuestos para revisión.

| Requisito funcional | RNF relacionados | C4 e interacción | ADR | CAP/PACELC y verificación pendiente |
| --- | --- | --- | --- | --- |
| RF-01 · Publicar convocatoria | RNF-02, RNF-03 | Coordinación → Web → Postulaciones, I-02 | ADR-001 y ADR-002 (I-02) | El dato de cupos prioriza consistencia. Identificar la interacción que avisa la apertura de la convocatoria. |
| RF-02 · Registrar postulación | RNF-02, RNF-03, RNF-04, RNF-09*, RNF-12 | Estudiante → Web → Postulaciones, I-02. Validación por I-05 | ADR-001 y ADR-002 | La recepción continúa si falla elegibilidad y la confirmación sigue a la persistencia. Aclarar qué verá el usuario al guardar durante la falla: «Enviada» o «Validación pendiente». |
| RF-03 · Verificar requisitos académicos | RNF-04, RNF-10 | Postulaciones → Elegibilidad → SGA, I-05 e I-06 | ADR-001 y ADR-002 | Priorizar la consistencia del resultado académico. Distinguir indisponibilidad, dato faltante y registro inexistente. Alinear los resultados y errores entre el RF, la sección 09 y el OpenAPI. |
| RF-04 · Revisar documentos | RNF-06*, RNF-07* | Coordinación → Web → Postulaciones, I-02 | ADR-001 y ADR-002 (I-02) | La tabla CAP no tiene una decisión específica de revisión documental. Confirmar si los cambios de estado y las observaciones se incluyen en la auditoría. |
| RF-05 · Consultar estado y recibir avisos | RNF-01, RNF-03, RNF-11, RNF-12 | Consulta por I-02. Avisos por I-08, I-11 e I-13 | ADR-001 y ADR-002 | La consulta presenta el último estado persistido y el correo puede retrasarse. Medir RNF-01 sobre I-02. Falta explicitar cómo se recibe el aviso en el panel y qué pasa si el productor no llega al intermediario. |
| RF-06 · Registrar méritos | RNF-06*, RNF-07 | Comisión → Web → Evaluación, I-03 | ADR-001 y ADR-002 (I-03) | Los puntajes priorizan consistencia. El control de versión debe evitar sobrescrituras al editar en paralelo. |
| RF-07 · Registrar oposición | RNF-06*, RNF-07 | Comisión → Web → Evaluación, I-03 | ADR-001 y ADR-002 (I-03) | CAP cubre los puntajes. Falta vincular la citación de oposición a una interacción explícita. |
| RF-08 · Consolidar y publicar resultados | RNF-07, RNF-11 | Evaluación, I-03 e I-07. Publicación y avisos, I-09 e I-11 a I-13 | ADR-001 y ADR-002 | Cupos y orden de mérito priorizan consistencia. Falta confirmar el criterio de desempate de la historia de usuario. |
| RF-09 · Registrar sesiones | RNF-06* | Ayudante → Web → Seguimiento, I-04 | ADR-001 y ADR-002 (I-04) | La tabla CAP no documenta una decisión específica para el registro de sesiones. |
| RF-10 · Validar planificación semanal | RNF-06* | Ayudante → Web → Seguimiento, I-04. Alta de la ayudantía por I-12 | ADR-001 y ADR-002 (I-04 e I-12) | Seguimiento verifica el tope de horas y los solapamientos. Hacer visible la planificación en la etiqueta I-04 del C4. |
| RF-11 · Aprobar u observar informes | RNF-06*, RNF-11 | Docente → Web → Seguimiento, I-04. Avisos por I-10, I-11 e I-13 | ADR-001 y ADR-002 | El aviso puede retrasarse. La tabla CAP no explicita el tratamiento de la decisión de aprobación del informe. |
| RF-12 · Descargar certificado | RNF-06* | Ayudante y autoridades → Web → Seguimiento, I-04 como ruta propuesta | ADR-001 y ADR-002 (I-04) | Trazar la secuencia de aprobaciones hasta la emisión del certificado. |

## Requisitos transversales y verificación

| RNF | Enlace en C4, ADR o CAP | Evidencia o decisión pendiente |
| --- | --- | --- |
| RNF-05 · Recuperabilidad | C4 identifica las bases de Postulaciones, Evaluación y Seguimiento. ADR-001 asigna dueño a los datos. | Identificar quién respalda y restaura cada base. Validar con el acta los intervalos provisionales. |
| RNF-06 · Control de acceso | C4 identifica la aplicación web, los seis roles y el administrador. | Aprobar la matriz rol × operación y probar autenticación y autorización. |
| RNF-07 · Trazabilidad | CAP identifica control de versión en puntajes y persistencia de estados. | Identificar dónde se guarda y cómo se aplica la retención del historial de estados y puntajes. |
| RNF-08 · Cifrado en tránsito | I-01 declara HTTPS. El contrato de I-05 publica una URL HTTP para el entorno local del esqueleto. | Explicitar qué enlaces externos requieren TLS y diferenciar su verificación del alcance local. |
| RNF-11 · Despliegue independiente | ADR-001 separa despliegues y ADR-002 desacopla los avisos. I-05 vincula los dos servicios de E1. | Ejecutar la prueba de actualización independiente entre Elegibilidad y Postulaciones cuando existan los servicios. |

## Cruces prioritarios para cerrar

- Medir RNF-01 en la consulta de estado de I-02. La latencia de I-05 sirve para caracterizar el intercambio entre servicios.
- Alinear RF-02 y RF-03 con los estados y errores del [OpenAPI propuesto](../src/contrato/elegibilidad-v1.yaml), y documentar en CAP qué sucede cuando falla el enlace entre un productor de avisos y el intermediario.
- Mantener como supuestos las cifras de RNF-02 y RNF-03 citadas en ADR-001 hasta contrastarlas con el acta.
- Usar la [matriz de pruebas](../src/pruebas/matriz-pruebas-rnf.md) y los [casos de elegibilidad](../src/pruebas/casos-servicio-a.md) como referencia para registrar la evidencia cuando se ejecuten las pruebas.

Decisiones de arquitectura: [ADR-001](adr/ADR-001-estilo-de-arquitectura.md) y [ADR-002](adr/ADR-002-mecanismo-de-comunicacion.md).
