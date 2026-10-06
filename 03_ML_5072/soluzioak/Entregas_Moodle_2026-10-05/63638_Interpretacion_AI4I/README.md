# Tarea 63638: interpretación individual de AI4I con Orange

**Revisión preparada con capturas nativas de Orange; no subida a Moodle.**
El original `AI4I_Orange_txostena.pdf` de `materialak/` se conserva sin modificar;
este paquete contiene un informe nuevo con evidencia de origen verificable.

El enunciado exige elegir un dataset, graficarlo e interpretarlo en Orange,
y presentar un PDF individual con Introducción, Desarrollo con capturas y
Conclusiones. `AI4I_Interpretacion_Orange.pdf` cumple esa estructura en cuatro
páginas: carga, Scatter Plot, Distributions y conclusiones con fuentes.

## Archivos de la entrega

| Archivo | Contenido |
| --- | --- |
| `AI4I_Interpretacion_Orange.pdf` | Informe académico principal; 4 páginas. |
| `Interpretacion_AI4I.ows` | Flujo real File → Scatter Plot / Distributions. |
| `datos/ai4i2020.csv` | CSV oficial UCI, conservado byte a byte tras extracción. |
| `datos/ai4i2020_orange.tab` | Mismos valores y columnas, con tipos/roles de Orange. |
| `capturas/*.png` | Tres capturas nativas de los widgets mostrados en Wayland. |
| `scripts/` y `reproducir.sh` | Recalcular, capturar, reabrir flujo, crear y verificar PDF. |
| `evidencias/` | Fuentes, hashes, estadísticas, ejecución, revisión visual y renders. |
| `SHA256SUMS` | Integridad del paquete, verificable sin Orange. |

Se conservan **10.000 filas y 14 columnas**, sin valores vacíos. En Orange se
declaran 6 atributos (Type y cinco medidas), 1 clase categórica Machine failure
y 7 metadatos (UDI, Product ID y cinco indicadores de fallo). Este cambio
declara roles, sin eliminar ni modificar las observaciones.

Comprobaciones recalculadas: 339 fallos, 9.661 registros sin fallo; tasa 3,39 %;
correlación velocidad/par -0,8750270863. El informe muestra medias, medianas y
tasas por intervalos, y explica desequilibrio, solapamiento, datos sintéticos
y ausencia de evidencia causal. No se entrena ni evalúa un clasificador.

## Abrir el flujo en otra instalación

1. Extraer todo el paquete, conservando `datos/` junto al `.ows`.
2. Abrir `Interpretacion_AI4I.ows` con Orange (validado con **3.40.0**).
3. Abrir File y comprobar 10.000 instancias. Si la instalación pide localizar
   el archivo, seleccionar `datos/ai4i2020_orange.tab`.
4. Abrir Scatter Plot: X = Rotational speed [rpm], Y = Torque [Nm],
   Color y Shape = Machine failure. Leyenda: 0 sin fallo; 1 fallo.
5. Abrir Distributions: variable Torque [Nm], Split by Machine failure,
   anchura 5 Nm; Show probabilities desmarcado (frecuencias absolutas).

El flujo se ha **reabierto con el motor real WidgetsScheme**: resolución de
la ruta relativa, señal de datos en los tres widgets, 10.000 filas, 339 fallos,
ejes, color, variable, separación y anchura recuperados correctamente.
La comprobación está en `evidencias/flujo_reabierto.json`.

## Verificar sin abrir Orange

Desde esta carpeta:

```bash
sha256sum -c SHA256SUMS
python3 scripts/verificar.py
```

El segundo comando necesita Python 3 y las herramientas Poppler `pdfinfo`,
`pdftotext` y `pdfimages`. Verifica la igualdad exacta CSV/.tab, forma de los
datos, etiqueta de fallo, hashes, estructura del flujo, secciones del PDF,
cuatro páginas y tres imágenes incorporadas. No considera estos controles
una revisión visual: esa evidencia se registra por separado.

Para recalcular solo estadísticas y la tabla Orange se usa Python estándar:

```bash
python3 scripts/estadisticas.py
```

## Reproducir las capturas y el PDF

La automatización de captura requiere **Linux, una sesión Wayland activa** y
Orange 3.40.0 con Qt; el informe y el flujo también se pueden consultar desde
una instalación gráfica compatible en otro sistema. No se actualiza Orange.
El entorno verificado usa Python 3.13.13 y ReportLab 5.0.1.

```bash
# En este equipo usa el Python Orange ya instalado.
bash reproducir.sh

# En otra instalación Linux se indica el Python que ya contiene Orange.
ORANGE_PYTHON=/ruta/al/python/con/Orange bash reproducir.sh
```

`reproducir.sh` usa `flock /tmp/aabd-orange-entregas-20261005.lock` para todas
las ejecuciones que importan Orange y mantiene una sola ejecución a la vez.
Configura `XDG_RUNTIME_DIR=/run/user/$(id -u)`, `WAYLAND_DISPLAY=wayland-1`
(o el valor disponible) y `QT_QPA_PLATFORM=wayland`. Solo muestra y cierra
sus propios widgets. Captura sus ventanas mediante `QWidget.grab()`;
no toma imágenes de ventanas ajenas ni recrea la interfaz en un gráfico.

La única dependencia de generación del PDF se obtiene mediante
`uv run --with reportlab==5.0.1`. Las estadísticas no necesitan paquetes.
No se descargan ni ejecutan scripts remotos. La tipografía utiliza DejaVu
Sans si está disponible, con alternativa Helvetica.

La reproducción genera nueva evidencia y nuevos hashes. Después hay que
renderizar y revisar visualmente el nuevo PDF: una revisión antigua no
acredita el archivo regenerado.

```bash
pdftoppm -r 100 -png AI4I_Interpretacion_Orange.pdf evidencias/pdf_render/pagina
# Abrir y revisar las cuatro PNG completas antes de certificar el nuevo PDF.
python3 scripts/verificar.py --actualizar-hashes
```

## Fuente y licencia

El CSV se obtuvo el 5 de octubre de 2026 exclusivamente del ZIP oficial de
[UCI AI4I 2020, dataset 601](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset).
El archivo y la ficha se atribuyen a **AI4I 2020 Predictive Maintenance Dataset
(2020), UCI Machine Learning Repository**, DOI
[10.24432/C5HS5C](https://doi.org/10.24432/C5HS5C), licencia **CC BY 4.0**.
La fuente describe un dataset sintético. El CSV original no se ha alterado;
la adaptación `.tab` declara tipos y roles para Orange.

SHA-256 del CSV original:
`dc6630cd9b1f0f853922fad78a1b6436570d3f1ec863f1dd5c4340ac56bc8a8e`.
URL de descarga, hash del ZIP y hash del informe original conservado figuran
en `evidencias/fuente.json`.

Documentación oficial de Orange:
[Scatter Plot](https://orangedatamining.com/widget-catalog/visualize/scatterplot/) y
[Distributions](https://orangedatamining.com/widget-catalog/visualize/distributions/).

La revisión visual registrada corresponde al PDF incluido, con las tres
capturas reales. Este paquete no acredita subida a Moodle, recepción,
evaluación del profesor ni calificación.
