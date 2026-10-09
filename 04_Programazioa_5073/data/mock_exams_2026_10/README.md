# CSV del simulacro de Programación

[Enunciado](../../materialak/Mock_Exams_2026-10/EXAMEN_A.md).
Datos **sintéticos**, generados el 9 de octubre de 2026 para autoestudio;
no contienen personas ni mediciones reales. Generador: random.Random(42), cuatro
cámaras ficticias C01–C04, 80 lecturas cada una. Etiqueta positiva cada décima
lectura; temperatura gaussiana media -7 para positiva/-18 para negativa, sigma
3.8; potencia media 3100/2300 W, sigma 650, recortada a cero. Redondeo 3 decimales.
No es serie temporal ni detector validado; patrones fueron introducidos por diseño.

Columnas originales tienen espacios/mayúsculas intencionados. Tras normalizar:
camara_id (grupo), registro_id (ID), temperatura_c (°C), potencia_w (W), averia
(entero 0/1, anomalía actual). Reglas del simulacro: temperatura [-30,15],
potencia [0,6000], valores finitos, etiqueta 0/1. IDs no son features.

Por cámara: fila lógica 3 temperatura=-40, 5 potencia ausente, 7 temperatura=250.
Se duplican exactamente C01-020 y C02-020 y se barajan todas las filas con el
mismo generador tras generar valores. CSV: 322 filas; limpieza deja 308,
32 positivas. Test cámara C04: 77 lecturas/8 positivas; train: 231/24.
Estos conteos se comprobaron localmente. El CSV es entrada fija: no sobrescribirlo.
