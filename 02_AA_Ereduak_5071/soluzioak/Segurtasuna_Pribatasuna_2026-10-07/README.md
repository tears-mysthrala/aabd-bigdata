# Seguridad y privacidad — actividades del 7 de octubre

Respuestas propias de los seis cuadernos nuevos de Moodle. Conservan la identificación del original y responden a sus bloques y reflexiones; no alteran `materialak/`. Las explicaciones están antes del código y también como comentarios en los scripts equivalentes.

| Actividad | Cuaderno | Script | Contenido |
|---|---|---|---|
| 1.1 | [Prompt injection](1_1_prompt_injection.ipynb) | [Python](1_1_prompt_injection.py) | Tres ataques, defensa en capas, cuatro bypasses y reflexión |
| 1.2 | [Membership inference](1_2_membership_inference.ipynb) | [Python](1_2_membership_inference.py) | Modelo, histogramas, ataque/defensa, Laplace ilustrativo, derechos |
| 3.1 | [Auditoría PbD](3_1_privacy_by_design.ipynb) | [Lectura equivalente](3_1_privacy_by_design.py) | Inventario, siete principios, rediseño, exclusiones y normativa |
| 4.1 | [Security/Privacy](4_1_security_vs_privacy.ipynb) | [Lectura equivalente](4_1_security_vs_privacy.py) | Siete medidas, complementariedad y caso de crédito |
| 5.1 | [EIA tráfico](5_1_eia_trafico.ipynb) | [Lectura equivalente](5_1_eia_trafico.py) | Clasificación condicionada, dos EIA, recomendaciones y alternativas |
| 6.0 | [Proyecto integrador](6_0_proiektu_integratzailea.ipynb) | [Lectura equivalente](6_0_proiektu_integratzailea.py) | Cuatro sesiones, amenazas, arquitectura, PbD, EIA y trade-offs |

La [presentación de 13 diapositivas](aurkezpena.html) desarrolla el caso del proyecto; abrirla en navegador o imprimir a PDF. Es un artefacto preparado, no evidencia de exposición en clase.

## Preparación y reproducción

Desde esta carpeta (Python 3.13 y uv):

```bash
uv sync --frozen
MPLBACKEND=Agg uv run --frozen python 1_1_prompt_injection.py
MPLBACKEND=Agg uv run --frozen python 1_2_membership_inference.py
```

Para el notebook, seleccionar el Python de `.venv` como kernel y ejecutar en orden desde esta carpeta. `uv.lock` fija versiones y cada práctica conserva aislamiento lógico. Los otros cuatro cuadernos son respuestas escritas: no contienen celdas de cálculo ni afirman pruebas de sistemas reales. Sus `.py` son versiones de lectura en comentarios, no simuladores.

## Evidencia actual y límites

[EJECUCION.json](EJECUCION.json) registra validación de esquema y ejecución de cuatro celdas de cálculo entre 1.1/1.2; los cuatro cuadernos escritos tienen cero celdas ejecutables. Los scripts 1.1/1.2 también se ejecutaron. Las figuras y métricas están guardadas en los notebooks.

En la ejecución actual, train accuracy 1.000 y test 0.915. Ataque exploratorio 0.641, defensa por agrupación 0.616: reducción 0.025, ventaja residual 0.116 frente a azar. Con calibración separada, evaluación 0.645/0.631. No se presupone mejora general ni anonimato; el ruido Laplace no acredita DP del modelo completo. No se hacen llamadas LLM ni ataques a servicios.

Se corrigen las erratas de interpretación, afirmaciones legales no acreditadas y contradicción de despliegue del [issue #15](https://github.com/tears-mysthrala/aabd-bigdata/issues/15) en estas variantes. Las referencias jurídicas son materiales de estudio: finalidad/rol/contexto y normativa aplicable determinan obligaciones; no se certifica cumplimiento. [Auditoría de dependencias](AUDITORIA_DEPENDENCIAS.json): sin vulnerabilidades conocidas detectadas en el entorno instalado, no garantía permanente.
