# Soluciones y rúbrica — 5071 — Modelos de inteligencia artificial, simulacro A

[Volver al examen](../../materialak/Mock_Exams_2026-10/EXAMEN_A.md).
Corrección propuesta, no baremo docente. Se admiten alternativas coherentes con
los requisitos. Concede crédito parcial por razonamiento correcto aunque haya
un error aritmético posterior; no cuentes dos veces el mismo mérito.
Los valores calculados son respuestas de casos sintéticos, no resultados de planta.

## 1 — 2 puntos

ML es parte de IA y deep learning parte de ML; IA incluye reglas/razonamiento.
IA débil es específica; fuerte refiere capacidad general, no una etiqueta
justificada por hablar fluidamente. Turing evalúa comportamiento conversacional,
no prueba conciencia ni competencia general. Mantenimiento conocido: experto;
imágenes etiquetadas: supervisado; lecturas sin etiquetas: no supervisado.
Admitir híbridos razonados. Rúbrica 0.5/0.5/0.75/0.25.

## 2 — 2.5 puntos

Base: hechos y reglas; motor: aplica reglas a hechos. R1=min(0.75,0.6)=**0.6**;
R2=max(0.25,0.6)=**0.6**. Pertenencia expresa grado de compatibilidad con un
concepto, no probabilidad de fallo. Fuzzificación convierte entradas en grados;
Mamdani recorta consecuentes por activación y los agrega por máximo. Centroide
= integral(z·μ(z))/integral(μ(z)); faltan formas de consecuentes, universo y
resolución si se discretiza. Umbral rígido cambia abruptamente; fuzzy admite
transición gradual, sin garantizar por sí solo mejor seguridad. Puntos según
los cinco subapartados.

## 3 — 2 puntos

Accuracy=(60+10+70+10)/200=**0.75**. FPR_A=20/80=**0.25**;
FPR_B=10/80=**0.125**: diferencia 0.125, ratio 2. FPR condiciona a negativos
reales; tasa de positivos predichos A=30/100, B=20/100.
Fuentes posibles: representación desigual, etiquetas históricas sesgadas,
variables proxy, medición desigual. Auditar procedencia, soporte y métricas por
grupo, incertidumbre y contexto de uso. Con 100 casos/grupo no se demuestra
causalidad ni cumplimiento de todos los criterios de equidad. No recomendar
una decisión judicial a partir de este caso. Rúbrica 0.75/0.5/0.5/0.25.

## 4 — 2 puntos

Inyección indirecta: datos del documento intentan convertirse en instrucciones.
Separar contenido de instrucciones; herramienta con mínimo privilegio y destinos
permitidos; autorización específica para escritura/exportación; validar argumentos
y registrar acciones sin secretos. Cifrado protege frente a acceso ilegítimo,
minimización reduce lo recogido: son complementarios. Membership inference
intenta inferir pertenencia al entrenamiento; sobreajuste puede facilitarla,
pero no es requisito único. DP requiere mecanismo, sensibilidad, presupuesto y
composición definidos; ruido arbitrario no los prueba. 0.5 por apartado.

## 5 — 1.5 puntos

Finalidad: apoyar o decidir selección laboral; afectados: candidatos y personal.
Preguntas: necesidad de datos/redes; base y finalidad del tratamiento; papel y
uso previsto del sistema para analizar nivel de riesgo; obligaciones de
información, evaluación de impacto, derechos y supervisión que correspondan.
No basta decir «todo uso de IA es alto riesgo» o «consentimiento permite todo».
PbD: eliminar fuentes innecesarias, retención limitada, acceso restringido y
seudonimización donde proceda. Persona revisora con información, tiempo y poder
real de corregir, canal de impugnación. Es una respuesta conceptual al temario,
no dictamen sobre un despliegue. 0.25/0.5/0.5/0.25.
