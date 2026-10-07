# %% [markdown]
# # 6.0 — Proyecto integrador: chatbot de atención con RAG
# Original: [6.0_proiektu_integratzailea_soluzioa.ipynb](../../materialak/6.0_proiektu_integratzailea_soluzioa.ipynb).
# Entrega propia para las cuatro sesiones: red-team, defensa, PbD/EIA y síntesis. Caso hipotético, sin llamadas a proveedor ni datos de clientes. Chatbot público para información y zona autenticada para expedientes. No toma decisiones de contratación, crédito o salud.
# Clasificación: por esa finalidad no se identifica automáticamente un supuesto del anexo III; revisar art. 6 según funciones reales. «GPAI» describe el modelo de propósito general y sus obligaciones de proveedor, no un nivel de riesgo medio del chatbot. Transparencia art. 50, prohibiciones art. 5 y RGPD según datos. No se acredita cumplimiento.

# %% [markdown]
# ## Sesión 1 — Red-team y ciclo de vida
# | Vector | Momento/escenario concreto | Probabilidad cualitativa / impacto | Detección y límites |
# |---|---|---|---|
# | Data poisoning | Documento falso añadido al repositorio de tarifas | Media / respuestas falsas y fraude | Origen, revisión y versionado; en RAG no altera pesos; instrucciones insertadas son indirect injection |
# | Prompt injection | Usuario o documento pide consultar expediente ajeno | Alta / fuga y acciones no autorizadas | Señales semánticas; ACL independiente del modelo; regex no cubre todo |
# | Model leakage/extraction | Consultas masivas para reproducir comportamiento o extraer prompt | Media / propiedad intelectual y configuración | Cuotas, monitorización y no incluir secretos; extraer un prompt no equivale a copiar pesos |
# | Membership inference | Diferenciar si un contrato está en el índice por respuestas | Media / existencia confidencial | Retrieval por ACL, respuestas uniformes sin confirmar documentos no autorizados; distinto de pertenencia al entrenamiento |
# Probabilidades son valoraciones del supuesto, no frecuencias medidas. Prioridad: injection con recuperación no autorizada por exposición pública e impacto; documentar poisoning por separado. Activos: documentos, expedientes, configuración, logs y credenciales del proveedor. Entrenamiento del proveedor no controlado por el operador; ingesta/índice/inferencia sí requieren controles propios.

# %% [markdown]
# ## Sesión 2 — Defensa y diagrama
# ```mermaid
# flowchart LR
#  U[Usuario] --> A[Autenticación y cuotas]
#  A --> R[Retrieval con ACL del servidor]
#  D[Documentos revisados y versionados] --> R
#  R --> L[LLM: contenido no fiable delimitado]
#  L --> V[Validación de salida y autorización de acciones]
#  V --> O[Respuesta o revisión humana]
#  V --> E[Evento mínimo de auditoría]
# ```
# Tres pilares: resiliencia con aislamiento/retrieval autorizado; contingencia con kill-switch y alternativa humana; precisión/reproducibilidad con conjunto versionado de preguntas, tasa de errores y modelo/prompt registrados.
# Seis principios: minimizar superficie (sin envío de correo/pagos), defensa en capas (entrada/retrieval/salida), privilegio mínimo (por usuario/expediente), fail-secure (negar ante autorización dudosa), auditoría (eventos mínimos íntegros) y contingencia (retirar versión y recuperar anterior probada).
# Controles requeridos y aceptación: ACL con pruebas cruzadas entre usuarios, separación de roles sin permisos textuales, cuotas, validación PII/acciones con medición de falsos negativos, logs mínimos/retención, alertas investigables, fallback probado, rollback probado, corpus adversarial revisado, revisión de cambios del prompt. Todos son **propuestos/no acreditados** hasta aportar prueba; ninguna casilla se marca aplicada sin evidencia. La autoconfianza textual «70%» del LLM no es un criterio calibrado de seguridad.

# %% [markdown]
# ## Sesión 3 — PbD, técnicas y EIA
# | Cavoukian | Aplicación al caso |
# |---|---|
# | Proactivo | EIPD cuando proceda y threat model antes del piloto |
# | Defecto | No guardar conversación íntegra ni usarla para entrenamiento por defecto |
# | Integrado | ACL/minimización/borrado como requisitos de arquitectura |
# | Funcionalidad | Resolver tarifas; derivar cuestiones sensibles a personal |
# | Ciclo completo | Sesión efímera; propuesta 30 días de eventos mínimos con justificación; controlar backups |
# | Transparencia | Explicar que es IA, fuentes y límites/canal de reclamación |
# | Respeto | Derechos, revisión humana y alternativas accesibles |
# Técnicas: seudonimización para eventos (mantienen condición personal); minimización de RAG y logs; anonimización solo si se acredita irreversibilidad/contexto; DP para estadísticas con sensibilidad y composición, no ε universal; DP-SGD solo si hubiera fine-tuning y se justifica necesidad/budget; federated learning no necesario para este repositorio central; edge puede reducir datos si hubiera cliente local, no se presupone.
#
# | EIA-Seguridad | Estado | Condición de salida |
# |---|---|---|
# | Stress/adversarial tests | No acreditados | Corpus y resultados medidos con responsables |
# | Detección | No acreditada | Tasa de detección/falsos positivos y proceso de respuesta |
# | Fail-safe | No acreditado | Prueba de retirada y atención humana |
# | Auditoría | No acreditada | Integridad/acceso/retención probados |
# | Superficie | Diseño propuesto | Inventario y pruebas de interfaces/ACL |
#
# | EIA-Privacidad | Estado | Condición de salida |
# |---|---|---|
# | Inventario de datos | Propuesto | Verificar documentos, clientes, proveedor y transferencias |
# | PbD técnico | No acreditado | ACL, minimización y borrado demostrados |
# | Derechos | Propuestos | Canal, responsables y plazo aplicable probados |
# | Transparencia | Propuesta | Aviso visible/comprensible revisado |
# | Ciclo de vida | Propuesto | Calendario coherente y prueba de borrado/backups |
# **Decisión EIA: no desplegar hasta cerrar controles bloqueantes y revisar riesgo residual.** Misma decisión en todo el informe. No se inventan red-teams trimestrales, una auditoría externa o certificaciones.

# %% [markdown]
# ## Sesión 4 — Trade-offs, marco y presentación
# Precisión/privacidad: medir utilidad con mínimos datos; retener conversación completa no es necesario para métricas de errores. Transparencia/seguridad: explicar finalidad y derechos sin revelar configuración sensible, pero ocultar configuración no sustituye autorización. Privacidad/negocio: publicar categorías agregadas con supresión de grupos pequeños y análisis de enlace/diferencias; medir tendencia sin perfiles individuales.
# RGPD 5/6 (finalidad/base por operación), 22 si se añadieran decisiones exclusivamente automatizadas relevantes, 25/32 diseño y seguridad, 35 EIPD según riesgo; 33 notificación a autoridad, cuando proceda, en 72h desde conocimiento; 34 comunicación a afectados si alto riesgo, sin aplicar el mismo plazo automáticamente; 36 consulta previa según residual. IA 5 y 50 según función, 53–55 obligaciones del proveedor GPAI y 9–15 solo si aplica alto riesgo. LO 3/2018 complementa RGPD, no una «transposición» de un reglamento.
# Semáforo: rojo — ACL cruzadas, resistencia a documentos no fiables, fallback, inventario/base/retención sin verificar; amarillo — automatización de pruebas y afinado de detección una vez cerrados rojos; verde — únicamente el diseño documental completado, no seguridad/cumplimiento del sistema. **No desplegar hasta cerrar los rojos con evidencia.** No se inventa un plazo de 4–6 semanas ni una plantilla de dos ingenieros.
#
# Guion de 13 diapositivas para exposición (no presentación humana realizada):
# 1. Caso, objetivo y límite; 2. clasificación condicionada; 3. poisoning; 4. injection; 5. extracción; 6. pertenencia; 7. diagrama; 8. seis principios SbD; 9. siete PbD y técnicas; 10. EIA y pendientes; 11. tres trade-offs; 12. tres prioridades (ACL, pruebas/fallback, privacidad); 13. responsables/evidencias y decisión no-go.
# Extensión a otros ciclos: administración — prestaciones, examinar anexo III.5 y decisiones/derechos; salud — función de producto sanitario/componente de seguridad y art. 6.1/anexo I, no afirmar que toda imagen médica encaja en III.5; educación — evaluar admisión/resultados y anexo III.3. En cada uno adaptar amenazas, minimización y supervisión, no copiar la clasificación del chatbot.
# Validación: cobertura documental de cuatro vectores, tres pilares, seis principios, siete PbD, dos EIA, tres tensiones y 13 slides. No se ha implementado ni desplegado un chatbot real.

# %% [markdown]
# ## Fuentes y alcance
# Referencias primarias: [RGPD](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [Reglamento de IA](https://eur-lex.europa.eu/eli/reg/2024/1689/oj), [LOPDGDD](https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673), [EDPB: seudonimización](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisation-pseudonymisation_en).
# Lectura docente contrastada el 7 de octubre de 2026. La clasificación depende de finalidad, funciones y contexto; citar artículos no certifica cumplimiento. Una EIA ética complementa, pero no sustituye, una EIPD del RGPD ni una evaluación de conformidad. No se han auditado empresas, personas o sistemas reales.
