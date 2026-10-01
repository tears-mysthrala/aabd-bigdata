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

## Qué está pendiente

Los porcentajes y conclusiones «esperados» del texto son referencias del material,
no una ejecución nueva de este checkout. Esta revisión **no ha reconciliado
esas cifras con el umbral 7**, no ha recalculado outputs ni ha verificado
afirmaciones causales o jurídicas. Para entregar la actividad, conserva tus
tablas ejecutadas y argumenta las garantías/limitaciones; no cites las cifras
preescritas como si las hubieras obtenido.

[Respuestas de ética y marco legal](../../soluzioak/README.md) y
[matriz de cobertura](../../../00_Transversal/AUDITORIA_EJERCICIOS.md).
