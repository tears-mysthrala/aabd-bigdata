# COMPAS: leer y comprobar la solución de sesgo histórico

El [notebook](2.2_compas_historikoa_soluzioa.ipynb) compara métricas entre
grupos a partir del dataset de ProPublica. Requiere NumPy, Pandas y Matplotlib;
[requirements.txt](requirements.txt) agrupa dependencias de muchos otros
ejercicios de percepción (incluye NLP/visión); no necesitas instalarlas todas
para COMPAS. Los comandos siguientes preparan solo los paquetes que importa.
Desde la raíz del repositorio:

```bash
cd 02_AA_Ereduak_5071/materialak/Alborapenak
uv venv .venv
uv pip install --python .venv/bin/python numpy pandas matplotlib
```

Abre el notebook con un kernel de ese entorno y ejecuta en orden. La celda de
carga actual **descarga por HTTPS** aunque haya un CSV local. Para trabajar sin
red puedes cambiar en tu copia la entrada de `pd.read_csv` a
`compas-scores-two-years.csv`, anotando la versión utilizada; este documento
no cambia el código del material.

## Método y lectura

El código filtra por ventana ±30 días, registros/etiquetas válidos y después
define predicción de alto riesgo con **`decile_score >= 7`**. Un umbral diferente
cambia la matriz de confusión y sus tasas. La tabla de cada grupo usa:

- FPR = FP/(FP+TN): entre no reincidentes, cuántos se predicen de alto riesgo.
- FNR = FN/(FN+TP): entre reincidentes, cuántos se predicen de bajo riesgo.
- TPR = TP/(TP+FN): proporción detectada entre reincidentes.
- Base rate: fracción de reincidentes en el grupo tras el filtrado.

Registra los tamaños de grupo, filtros y umbral junto a las tasas. Comprueba
que FP+TN y TP+FN tengan observaciones antes de comparar. La curva agrupada
por score muestra tasas observadas y tamaños por nivel; parecidos visuales
no bastan para afirmar calibración estadística ni equivalencia entre grupos.

## Solución reconciliada y ejecutada

La [copia de solución](../../soluzioak/COMPAS/COMPAS_reconciliado.ipynb) conserva
el material original y recalcula métricas reales con su umbral **>=7**: FPR
22,79%/8,27% y FNR 49,25%/72,02% para African-American/Caucasian, respectivamente,
sobre 5.278 registros filtrados (3.175/2.103). El contraste **>=5** está separado:
FPR 42,34%/22,01% y FNR 28,48%/49,64%. Los porcentajes «esperados» del original
no se atribuyen al umbral 7 ni se fuerzan como reproducción exacta de ProPublica.

La [guía de reproducción y resultados](../../soluzioak/COMPAS/README.md) incluye
fuente fijada por commit/hash, entorno, comandos, denominadores y límites.
La fuente individual se mantiene en caché privada fuera del repositorio;
la solución exporta únicamente agregados y dos figuras. El notebook se ejecutó
con nbclient y se validó con nbformat. Las tasas por decil **no** se presentan
como prueba de calibración probabilística; no hay inferencia causal ni un
veredicto jurídico basado en estos números.

[Respuestas de ética y marco legal](../../soluzioak/README.md) y
[matriz de cobertura](../../../00_Transversal/AUDITORIA_EJERCICIOS.md).
