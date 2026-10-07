# %% [markdown]
# # 5.1 — EIA de un sistema de tráfico
# Original: [5.1_eia_aplikatu_soluzioa.ipynb](../../materialak/5.1_eia_aplikatu_soluzioa.ipynb).
# Supuesto docente: cámaras para contar/predecir tráfico y posible control de señales. No existe despliegue municipal auditado: donde faltan pruebas se escribe «no acreditado», no «incumplimiento demostrado».

# %% [markdown]
# ## Clasificación condicionada
# Si la IA es componente de seguridad en gestión/operación de tráfico, examinar art. 6 y anexo III.2. Contar coches para estadística no basta por sí mismo para demostrar ese encaje. Si se añaden funciones biométricas, revisar finalidad/tipo y anexo III.1. El art. 5.1.h sobre identificación biométrica remota en tiempo real en espacios públicos se refiere a fines de aplicación de la ley y tiene excepciones estrictas; no es una prohibición genérica de toda cámara municipal. No asumir que identificar matrículas equivale a identificación biométrica de personas.
# Para alto riesgo, examinar arts. 9–15 (riesgo, datos, documentación, logs, información, supervisión, precisión/robustez) y obligaciones según rol/fase/calendario. RGPD: arts. 5/6, 9 si biometría especial, 13/14, 25/32 y 35 según tratamiento/riesgo. EIA ética ≠ EIPD. No se exige automáticamente un registro AESIA o consulta previa en todos los proyectos; art. 36 RGPD se analiza si queda alto riesgo sin mitigar.
#
# ## EIA-Seguridad
# | Pregunta | Estado del supuesto | Medida/evidencia para cerrar |
# |---|---|---|
# | Pruebas adversariales | No acreditadas | Dataset offline con perturbaciones digitales; métricas por escenario y revisión |
# | Detección de manipulación | No acreditada | Monitorizar calidad, timestamps, drift; medir falsos positivos/negativos |
# | Fail-safe | No acreditado | Validar retorno al controlador convencional con responsables de seguridad |
# | Superficie reducida | No acreditada | Autenticación, ACL, segmentación y revisión de interfaces |
# | Auditoría | No acreditada | Eventos mínimos íntegros, retención justificada y verificación de accesos |
# No se ataca tráfico real, no se manipulan cámaras y no se prescribe «ámbar intermitente» como solución universal. El estado seguro depende de ingeniería del sistema.
#
# ## EIA-Privacidad
# | Pregunta | Estado | Medida/evidencia para cerrar |
# |---|---|---|
# | Inventario | Pendiente | Identificar imágenes, matrículas, trayectorias y destinatarios |
# | PbD/defecto | Pendiente | Contar en edge sin transmitir imágenes si satisface objetivo |
# | Derechos | Pendiente | Responsable/contacto y procedimiento con excepciones justificadas |
# | Transparencia | Pendiente | Avisos e información accesible de finalidad/base/retención |
# | Ciclo de vida | Pendiente | Preferir no conservar vídeo; plazos necesarios, borrado y backups probados |
# Un hash de matrícula/MAC sigue siendo enlazable y potencialmente personal; ni ruido ni hashing prueban anonimización. Difuminar tras capturar reduce exposición, no elimina el tratamiento previo. La matrícula no se necesita para simple conteo. No se declaran datos FCD anónimos sin verificar reidentificación/contratos.

# %% [markdown]
# ## Medidas por finalidad y recomendación
# Security: reducir interfaces, TLS/autenticación, mínimo privilegio, fallback validado, auditoría mínima, contingencia y pruebas de adversario. Privacy: evaluar antes, conteos como defecto, minimización/edge, retención mínima, información/derechos y análisis de agregación/DP si se publica estadística.
# **No desplegar control automático en la situación no acreditada.** Condiciones de salida: finalidad/base definidas, clasificación documentada, EIPD cuando proceda, pruebas de seguridad/fallback aprobadas, minimización y derechos probados. Después puede proponerse un piloto offline o supervisado, sin presentarlo como ya ejecutado.
# Tres elementos del informe: (1) necesidad/proporcionalidad frente a alternativas; (2) riesgos y medidas con responsable/evidencia/residual; (3) participación/derechos/revisión y decisión firmada. La autoridad competente de protección de datos y el supervisor IA dependen del tratamiento y ámbito.
# Alternativas: lazos inductivos o tubos neumáticos para conteo; cámara con conteo local sin identificación si lo anterior no basta. Evaluar precisión/coste y recoger solo lo necesario. No basta con decir que un proveedor garantiza anonimato.
# Esta respuesta identifica al menos tres controles no acreditados de cada bloque y responde clasificación, alternativas, recomendación y contenidos de informe. Ninguna fila acredita una prueba municipal real.

# %% [markdown]
# ## Fuentes y alcance
# Referencias primarias: [RGPD](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [Reglamento de IA](https://eur-lex.europa.eu/eli/reg/2024/1689/oj), [LOPDGDD](https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673), [EDPB: seudonimización](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisation-pseudonymisation_en).
# Lectura docente contrastada el 7 de octubre de 2026. La clasificación depende de finalidad, funciones y contexto; citar artículos no certifica cumplimiento. Una EIA ética complementa, pero no sustituye, una EIPD del RGPD ni una evaluación de conformidad. No se han auditado empresas, personas o sistemas reales.
