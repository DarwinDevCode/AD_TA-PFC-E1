# Matriz de trazabilidad del SGAC

Matriz preliminar de TA-PFC-E1. Los RF se identifican con la numeración de la planificación del equipo mientras la [sección de requisitos funcionales](secciones/05-requisitos-funcionales.tex) se completa con el acta. Los [RNF](secciones/06-requisitos-no-funcionales.tex) conservan sus cifras provisionales. Los ADR-001 y ADR-002 están aceptados. ADR-001 separa los servicios por capacidad y asigna un dueño a cada dato. ADR-002 define REST para I-02 a I-07 y mensajería asíncrona para I-08 a I-13, con RabbitMQ como intermediario desde E2. El esqueleto de E1 usa REST en I-05 e I-06.

Las interacciones I-01 a I-13 corresponden al [C4 de contenedores](secciones/08-arquitectura-c4.tex) y al [modelo de comunicación](secciones/09-modelo-comunicacion.tex). CAP/PACELC se refiere a las decisiones por dato crítico de la [sección de análisis](secciones/10-analisis-cap-pacelc.tex). Los RNF marcados con asterisco son vínculos propuestos para revisión.

| Requisito funcional | RNF relacionados | C4 e interacción | ADR | CAP/PACELC y verificación pendiente |
| --- | --- | --- | --- | --- |
| RF-01 · Publicar convocatoria | RNF-02, RNF-03 | Coordinación → Web → Postulaciones, I-02 | ADR-001 y ADR-002 (I-02) | El dato de cupos prioriza consistencia. Identificar la interacción que avisa la apertura de la convocatoria. |
| RF-02 · Registrar postulación | RNF-02, RNF-03, RNF-04, RNF-09*, RNF-12 | Estudiante → Web → Postulaciones, I-02. Validación por I-05 | ADR-001 y ADR-002 | Se prioriza la disponibilidad de la recepción. Postulaciones confirma «Enviada» después de persistir la solicitud y deja la validación en «Validación pendiente» si falla la consulta. La [sección 14](secciones/14-esqueleto-funcional.tex) documenta la recuperación con el SGA simulado. |
| RF-03 · Verificar requisitos académicos | RNF-04, RNF-10 | Postulaciones → Elegibilidad → SGA, I-05 e I-06 | ADR-001 y ADR-002 | Se prioriza la consistencia del resultado académico mediante una consulta de solo lectura al SGA. I-05 distingue 200 con resultados por requisito (incluido DATO_FALTANTE), 404 por estudiante inexistente y 503 por SGA indisponible. El 503 deja la validación pendiente para reintento. |
| RF-04 · Revisar documentos | RNF-06*, RNF-07* | Coordinación → Web → Postulaciones, I-02 | ADR-001 y ADR-002 (I-02) | La tabla CAP no tiene una decisión específica de revisión documental. Confirmar si los cambios de estado y las observaciones se incluyen en la auditoría. |
| RF-05 · Consultar estado y recibir avisos | RNF-01, RNF-03, RNF-11, RNF-12 | Consulta por I-02. Avisos por I-08, I-11 e I-13 | ADR-001 y ADR-002 | El panel consulta el último estado persistido por I-02. El aviso por correo puede retrasarse: si el intermediario está caído, el productor conserva el evento y reintenta; si falla el consumidor, el evento espera en la cola. Medir RNF-01 sobre I-02 y verificar la entrega diferida cuando se incorporen notificaciones. |
| RF-06 · Registrar méritos | RNF-06*, RNF-07 | Comisión → Web → Evaluación, I-03 | ADR-001 y ADR-002 (I-03) | Los puntajes priorizan consistencia. Si Evaluación no confirma el registro, debe repetirse la operación. El control de versión rechaza la edición simultánea sobre una versión anterior. |
| RF-07 · Registrar oposición | RNF-06*, RNF-07 | Comisión → Web → Evaluación, I-03. Citación por I-09 | ADR-001 y ADR-002 (I-03 e I-09) | Los puntajes siguen el control de versión de RF-06. La sección 09 identifica I-09 como origen de la citación asíncrona. |
| RF-08 · Consolidar y publicar resultados | RNF-07, RNF-11 | Evaluación, I-03 e I-07. Avisos por I-09, I-11 e I-13 y alta de ayudantías por I-12 | ADR-001 y ADR-002 | Cupos y orden de mérito priorizan consistencia: sin acceso a cupos no se designa y sin postulaciones validadas por I-07 no se consolida ni publica. El cálculo usa un conjunto consolidado de puntajes. Queda por confirmar el desempate. |
| RF-09 · Registrar sesiones | RNF-06* | Ayudante → Web → Seguimiento, I-04 | ADR-001 y ADR-002 (I-04) | La tabla CAP no documenta una decisión específica para el registro de sesiones. |
| RF-10 · Validar planificación semanal | RNF-06* | Ayudante → Web → Seguimiento, I-04. Alta de la ayudantía por I-12 | ADR-001 y ADR-002 (I-04 e I-12) | Seguimiento exige que la ayudantía exista antes de aceptar la planificación. I-04 comprueba el tope de horas y los solapamientos al guardar. |
| RF-11 · Aprobar u observar informes | RNF-06*, RNF-11 | Docente → Web → Seguimiento, I-04. Avisos por I-10, I-11 e I-13 | ADR-001 y ADR-002 | La revisión se registra por I-04 y el aviso se emite después por I-10. Ante una falla se conserva el evento para reintento. La tabla CAP cubre el aviso y deja sin especificar la decisión de aprobación del informe. |
| RF-12 · Descargar certificado | RNF-06* | Ayudante y autoridades → Web → Seguimiento, I-04 como ruta propuesta | ADR-001 y ADR-002 (I-04) | Trazar la secuencia de aprobaciones hasta la emisión del certificado. |

## Requisitos transversales y verificación

| RNF | Enlace en C4, ADR o CAP | Evidencia o decisión pendiente |
| --- | --- | --- |
| RNF-05 · Recuperabilidad | C4 identifica las bases de Postulaciones, Evaluación y Seguimiento. ADR-001 asigna dueño a los datos. | Identificar quién respalda y restaura cada base. Confirmar con infraestructura los intervalos provisionales. |
| RNF-06 · Control de acceso | C4 identifica la aplicación web, los seis roles y el administrador. | Aprobar la matriz rol × operación y probar autenticación y autorización. |
| RNF-07 · Trazabilidad | CAP identifica control de versión en puntajes y persistencia de estados. | Identificar dónde se guarda y cómo se aplica la retención del historial de estados y puntajes. |
| RNF-08 · Cifrado en tránsito | I-01 declara HTTPS. El contrato de I-05 publica una URL HTTP para el entorno local del esqueleto. | La sección 09 prevé HTTPS para I-05 e I-06 en despliegue con red. Verificar TLS en los enlaces aplicables fuera del entorno local. |
| RNF-11 · Despliegue independiente | ADR-001 separa despliegues y ADR-002 desacopla los avisos. I-05 vincula los dos servicios de E1. | Ejecutar la prueba de actualización independiente entre los servicios de E1. La verificación del desacoplamiento de avisos corresponde a la incorporación de RabbitMQ. |

## Cruces prioritarios para cerrar

- Medir RNF-01 en la consulta de estado de I-02. La latencia de I-05 sirve para caracterizar el intercambio entre servicios.
- Usar los OpenAPI aceptados de [I-05](../src/contrato/elegibilidad-v1.yaml) e [I-06](../src/contrato/sga-simulado-v1.yaml) para verificar estados y errores. Al incorporar RabbitMQ, probar por separado la caída del intermediario y la del consumidor.
- Mantener provisionales las metas de rendimiento, capacidad y disponibilidad citadas en los ADR hasta su validación institucional.
- Usar la [matriz de pruebas](../src/pruebas/matriz-pruebas-rnf.md) y los [casos de elegibilidad](../src/pruebas/casos-servicio-a.md) como referencia para registrar la evidencia cuando se ejecuten las pruebas.

Decisiones de arquitectura: [ADR-001](adr/ADR-001-estilo-de-arquitectura.md) y [ADR-002](adr/ADR-002-mecanismo-de-comunicacion.md).
