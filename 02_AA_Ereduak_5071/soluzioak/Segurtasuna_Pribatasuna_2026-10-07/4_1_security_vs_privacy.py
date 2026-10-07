# %% [markdown]
# # 4.1 — Security y Privacy by Design
# Original: [4.1_security_vs_privacy_sailkapena_soluzioa.ipynb](../../materialak/4.1_security_vs_privacy_sailkapena_soluzioa.ipynb).
# Objetivo: clasificar por finalidad principal y explicar solapamientos, sin garantías absolutas.

# %% [markdown]
# ## Clasificación de las siete medidas
# | Medida | Finalidad principal | Justificación / referencia |
# |---|---|---|
# | Seudonimizar entrenamiento | Privacy | Reducir vinculación con personas; RGPD 4.5/25 |
# | Fallback ante ataque | Security | Mantener control/disponibilidad; supervisión art. 14 IA si aplica |
# | No recoger teléfono | Privacy | Minimización; RGPD 5.1.c/25 |
# | Filtrar prompt injection | Security | Integridad del comportamiento; art. 15 IA si aplica |
# | Entrenamiento DP | Privacy | Acotar cambio por participación individual bajo hipótesis/budget |
# | Registrar quién consulta | Security | Auditoría; puede apoyar accountability y afectar privacidad |
# | Control de acceso API | Security | Autorización/mínimo privilegio; también protege datos personales |
# Resultado por objetivo principal: Privacy 3, Security 4. No son categorías mutuamente excluyentes ni una declaración de que las obligaciones de alto riesgo se aplican a cualquier chatbot.

# %% [markdown]
# ## Complementariedad y caso de crédito
# Solo PbD: menos información expuesta, pero un fallo de autorización puede filtrar los datos restantes. Solo SbD: protege accesos, pero no justifica recoger datos innecesarios ni conservarlos indefinidamente.
# En un sistema de crédito: autenticar y autorizar consultas por expediente, limitar volumen, detectar entradas malformadas y permitir revisión humana; recoger solo variables justificadas, separar identificadores, evaluar sesgos y fugas, limitar retención y tramitar derechos. Prompt injection es pertinente si existe una interfaz LLM, no por el mero uso de un clasificador tabular.
# Ante una brecha, seudonimización reduce vinculación pero conserva condición de datos personales y riesgo de reidentificación. DP limita matemáticamente diferencias entre datasets vecinos cuando se implementa con garantías; no elimina todos los ataques ni asegura que no se reconozca a nadie. Minimizar y borrar reduce lo disponible para robar.
# No multiplicamos probabilidades suponiendo independencia entre controles: un mismo acceso comprometido puede vencer varias capas correlacionadas. Evaluar escenarios y daño residual concreto.
# Prueba conceptual: un log puede ser medida de seguridad y a la vez contener datos personales. La clasificación indica su objetivo, no exención de RGPD. Comparar controles, finalidad, qué protege cada uno y qué permanece vulnerable.

# %% [markdown]
# ## Fuentes y alcance
# Referencias primarias: [RGPD](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [Reglamento de IA](https://eur-lex.europa.eu/eli/reg/2024/1689/oj), [LOPDGDD](https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673), [EDPB: seudonimización](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisation-pseudonymisation_en).
# Lectura docente contrastada el 7 de octubre de 2026. La clasificación depende de finalidad, funciones y contexto; citar artículos no certifica cumplimiento. Una EIA ética complementa, pero no sustituye, una EIPD del RGPD ni una evaluación de conformidad. No se han auditado empresas, personas o sistemas reales.
