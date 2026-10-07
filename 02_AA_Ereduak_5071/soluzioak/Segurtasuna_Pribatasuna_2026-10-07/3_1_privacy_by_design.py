# %% [markdown]
# # 3.1 — Auditoría PbD de monitorización laboral
# Original: [3.1_privacy_by_design_auditoria_soluzioa.ipynb](../../materialak/3.1_privacy_by_design_auditoria_soluzioa.ipynb).
# Caso hipotético: herramienta que pretende medir productividad por actividad digital. No afirmamos que un fabricante concreto recopile estas categorías ni que se haya auditado una empresa.

# %% [markdown]
# ## Inventario y necesidad
# | Dato potencial | Riesgo y decisión para este caso |
# |---|---|
# | Inicio/fin de jornada | Personal; conservar solo con finalidad y base definidas |
# | Aplicaciones activas | Perfilado; sustituir por carga declarada por proyecto |
# | Pulsaciones y contenido escrito | Puede captar comunicaciones/secretos; excluir |
# | Movimientos/clics | Proxy pobre de productividad; excluir |
# | URLs e historial | Puede revelar salud/creencias; excluir |
# | Capturas de pantalla | Contenido ajeno al objetivo; excluir |
# | Webcam/atención | Intrusiva; excluir; imagen no equivale automáticamente a biometría especial |
# | Metadatos/contenido de correo | Relaciones y comunicaciones; excluir de productividad |
# | Reuniones y participantes | Preferir volumen agregado sin participantes |
# | Geolocalización | Excluir: no necesaria para balancear carga |
# | USB/impresión | Separar la finalidad DLP de la de productividad |
# Los identificadores, email e IP también son personales. Datos biométricos para identificación unívoca pueden ser categorías especiales (RGPD 4.14/9); una webcam por sí sola no demuestra ese tratamiento.

# %% [markdown]
# ## Siete principios de Cavoukian
# | Principio | Defecto bajo los supuestos del caso | Rediseño |
# |---|---|---|
# | Proactivo | Sin evaluación previa | EIPD si procede y participación antes de pilotar |
# | Privacidad por defecto | Recogida exhaustiva | Solo carga agregada de proyecto |
# | Integrada en diseño | Monitorización añadida sin requisitos | Requisitos de minimización, ACL y borrado desde inicio |
# | Funcionalidad completa | Actividad confundida con rendimiento | Medir entregables/carga sin vigilancia individual |
# | Ciclo de vida | Retención indefinida | Calendario con borrado y verificación de backups |
# | Transparencia | No se explica el perfilado | Aviso claro, datos/finalidad/destinatarios/derechos |
# | Respeto al usuario | Sin reclamación | Acceso, rectificación y revisión humana |
# No se da por probado que una herramienta real incumpla los siete: habría que revisar evidencia y contrato.
#
# ## Rediseño operativo
# Finalidad: balancear carga mensual por equipos. Recoger tareas declaradas y tiempos agregados de proyecto. No generar rankings ni decisiones individuales automatizadas. Suprimir grupos menores de cinco como precaución didáctica; cinco no garantiza anonimato (pueden existir inferencias por diferencias y datos auxiliares). Separar claves de seudónimos, acceso por función y doble autorización para casos excepcionales. Hash de email sin secreto no anonimiza; usar un identificador aleatorio con tabla de correspondencia separada o HMAC gestionado fuera del informe.
# Por defecto: cámara/capturas/teclado/URL/GPS desactivados. La actividad voluntaria adicional no convierte el consentimiento laboral en libre automáticamente; documentar la base jurídica necesaria y proporcional por finalidad.
# Propuesta de retención, no plazo legal universal: datos de detalle hasta 30 días para corrección, agregados 90 días para comparar carga, después borrado o anonimización demostrada. Excepciones justificadas y acotadas; auditar accesos, borrados y copias. Cifrado, claves separadas y formación. DP puede ayudar a publicar agregados con sensibilidad y composición justificadas, no mediante un ε arbitrario.
# Excluir en este diseño webcam, contenido de teclado/correo, actividad privada fuera de jornada y ranking nominal. Esto responde al objetivo mínimo, no afirma una prohibición absoluta de toda videovigilancia laboral.

# %% [markdown]
# ## Normas y reflexión
# RGPD 5 (finalidad/minimización/retención), 6 (base jurídica), 9 cuando proceda, 22 cuando haya decisiones exclusivamente automatizadas relevantes, 25 (diseño/defecto), 32 (seguridad), 35 (EIPD según riesgo), 88 (contexto laboral). LOPDGDD 87 regula dispositivos, 88 desconexión, 89 videovigilancia/sonido y 90 geolocalización; no se confunden sus objetos. Estatuto de los Trabajadores 20.3: control respetando dignidad; 64: información/consulta según supuesto. IA para evaluar rendimiento laboral: examinar anexo III.4 y art. 6, no asumir que cualquier software de horario es IA de alto riesgo.
# El coste inicial aumenta por análisis, controles y revisión, pero reduce datos expuestos, reclamaciones y retrabajo. Se retira la supuesta multa AEPD de seis millones del original: no se dispone de referencia que la acredite. No se inventa un precedente alternativo.
# En industria regulada, separar seguridad física de productividad: una necesidad de seguridad no autoriza todos los sensores ni elimina el análisis de proporcionalidad y base jurídica. Verificar requisitos sectoriales concretos antes de citar una obligación de notificar a CSN/AEMPS o de obtener un acuerdo universal.
# Comprobación documental: inventario ≥7, siete principios, rediseño, exclusiones y ≥5 artículos cubiertos. No hay ejecución ni auditoría empresarial real.

# %% [markdown]
# ## Fuentes y alcance
# Referencias primarias: [RGPD](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [Reglamento de IA](https://eur-lex.europa.eu/eli/reg/2024/1689/oj), [LOPDGDD](https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673), [EDPB: seudonimización](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisation-pseudonymisation_en).
# Lectura docente contrastada el 7 de octubre de 2026. La clasificación depende de finalidad, funciones y contexto; citar artículos no certifica cumplimiento. Una EIA ética complementa, pero no sustituye, una EIPD del RGPD ni una evaluación de conformidad. No se han auditado empresas, personas o sistemas reales.
