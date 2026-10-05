# Interpretación de datos con Orange · tarea 63638

[Entrega PDF](Interpretacion_Datos_Orange.pdf): **Introducción, Desarrollo con capturas de pantalla y Conclusiones**, conforme a la [tarea Moodle](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63638). Dataset libre elegido: Iris, 150 flores y 50 por especie; longitud/anchura en cm. No es una segunda evaluación de KNN: se interpreta descriptivamente el patrón de los pétalos.

## Artefactos y evidencia

- [Workflow](Interpretacion_Iris.ows): File → Scatter Plot y Distributions. La ruta relativa apunta a `../datos/iris/iris.csv`. Si cambias de ubicación, selecciona esa tabla en File.
- [Scatter Plot](orange_scatter.png) y [Distributions](orange_distribucion.png): capturas de widgets nativos Orange 3.40 mostrados en Wayland, obtenidas mediante `QWidget.grab()`. Se cargaron los datos reales en los widgets; no son gráficos recreados ni capturas de otras aplicaciones.
- [Resumen](resumen.json): hash de fuente, tamaño, ausentes, medias por especie y correlación global (0,9629). Ese valor es asociación entre medidas, no causalidad ni precisión de un modelo.
- [Captura reproducible](capturar_orange.py) y [generador PDF](sortu_pdf.py). El workflow se exporta desde los settings de los widgets que se capturan, y su XML se valida con el parser de Orange.

Desde la raíz del repositorio, usando el entorno Orange ya instalado en esta máquina:

```bash
XDG_RUNTIME_DIR=/run/user/$(id -u) WAYLAND_DISPLAY=wayland-1 QT_QPA_PLATFORM=wayland \
  /home/tears/.local/share/uv/tools/orange3/bin/python \
  03_ML_5072/soluzioak/Interpretacion_Datos/capturar_orange.py
uv run --with reportlab==5.0.1 python \
  03_ML_5072/soluzioak/Interpretacion_Datos/sortu_pdf.py
```

En otra máquina instala Orange3 y sustituye el intérprete/socket según tu sesión Qt. La captura exige sesión gráfica; no modifica configuración del escritorio. Recalcula las medias desde la misma tabla y escribe solo los artefactos de esta carpeta.

**Verificado el 2026-10-02:** dimensiones 150×4 y ausencia de missing, hash de entrada, ejes/categorías y contenido de capturas, PDF renderizado de tres páginas inspeccionado. La vista de distribuciones usa intervalos de 0,5 cm. Setosa se separa en esta proyección; versicolor y virginica se solapan. No se infiere generalización a otras muestras. El PDF está preparado localmente; no se ha enviado a Moodle.
