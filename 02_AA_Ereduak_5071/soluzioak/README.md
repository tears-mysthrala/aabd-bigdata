# 02_AA_Ereduak_5071 — soluciones

[Nuevas actividades de seguridad y privacidad · 7 de octubre](Segurtasuna_Pribatasuna_2026-10-07/README.md): seis respuestas propias, demos ejecutadas y proyecto integrador.

La resolución integral (3 paradigmas + fuzzy + feature engineering + ANEXO1/4) vive en `../../01_Erronka1_CNC_Guard/soluzioak/Ebazpena_CNC_Guard_eta_AA_Ereduak.md`.
No duplicar: cualquier añadido específico 5071 va aquí y se referencia desde allí.

## IE1 — Sarrera

- [Sarrera: ariketa eta eztabaida](IE1_Sarrera_Ariketak.md): kronologia Deep Blue/AlphaGo/ChatGPT, inferentzia-zuhaitza, sistema aditua (9 arau) eta MYCINen erantzukizunari buruzko erantzun-ereduak.

## Etika — jarduera osagarriak

- [Etikako ariketa osagarriak](etikako_ariketa_osagarriak.md): fairness metrikak eta talde-argudioaren ereduak, GDPR 22. artikuluaren fluxua C-203/22 benetako kasuari aplikatuta, SHAP/LIME azalpena, mini EIA, tailerreko kameraren mehatxu- eta defentsa-azterketa, zehaztasuna/gardentasuna/pribatutasuna tentsioa, ALTAIren zazpi dimentsioko ebaluazio-fitxa eta protokolo pertsonal betegarria. 3.1, 12.0 eta 6.1 notebooken eskaera osoak checkout-ean falta dira; fitxan ez dago egiaztatu gabeko puntuaziorik edo aurkikuntzarik.

## IE6 — Marko legala

- [Ariketen eta amaierako jardueren erantzun-ereduak](IE6_Marko_Legala/ariketak_eta_jarduerak.md): GDPR 1.1, AI Act 2.1, 911ko EEEa eta bost jarduera. Iturri juridiko ofizialak 2026-09-24an egiaztatuta; ikasgelako kasuak hipotetikoak dira.
- [Proiektu integratzailearen txosten teknikoa](IE6_Marko_Legala/proiektu_integratzailea_txostena.md): hezkuntza-laguntzako tresna fikziozkoaren GDPR/AI Act azterketa, EEE, arrisku-kontrolak eta «aldatu» gomendioa.
- [Ikasleentzako gardentasun-orriaren zirriborroa](IE6_Marko_Legala/gardentasun_orria.md) eta [barneko gainbegiratze-protokoloa](IE6_Marko_Legala/protokolo_barnekoa.md): kontaktu eta datu errealak bete beharreko eredu didaktikoak.
- [15 minutuko aurkezpenaren gidoia](IE6_Marko_Legala/aurkezpena_esquema.md): 11 diapositibako edukia, denborak eta speaker-notes aipamenak. [PPTX editagarria](IE6_Marko_Legala/aurkezpena_15min.pptx) ere badago (portada + 11 diapositiba); ez du benetako aurkezpena egin dela frogatzen.

## Cómo trabajar las respuestas

Empieza por IE1 (conceptos y reglas), continúa con ética (métricas, argumentos
y límites) y después IE6 (aplicación a casos hipotéticos). Cada respuesta debe
identificar el supuesto, justificar la elección y mencionar cuándo cambiaría.
Los campos `[...]` de plantillas requieren datos propios; una plantilla disponible
no equivale a una entrega personal realizada. Los textos jurídicos indican sus
fuentes y fecha de consulta; esta revisión documental no actualiza su vigencia.

La solución numérica de COMPAS está fuera de esta carpeta:
[notebook de sesgo histórico](../materialak/Alborapenak/2.2_compas_historikoa_soluzioa.ipynb).
Lee primero sus filtros, umbral y definiciones de FPR/FNR. Su código actual
descarga el CSV por HTTPS y usa umbral 7; no utiliza automáticamente la copia
local. [Preparación y límites](../materialak/Alborapenak/README.md). El archivo
[2.1 AI Act](../materialak/2.1_ai_act_arrisku_mailak_sailkatzen.ipynb) conserva
una tabla sin completar: consulta la respuesta desarrollada en IE6; el título
«SOLUZIOA» del notebook no demuestra que esa tabla esté resuelta.

En COMPAS comprueba denominadores por grupo antes de comparar porcentajes;
una diferencia observada no demuestra su causa. En los casos escritos, comprueba
que cada conclusión siga de los hechos/supuestos y fuentes indicados. En
[auditoría de ejercicios](../../00_Transversal/AUDITORIA_EJERCICIOS.md) se
identifican cuadernos externos ausentes y evidencias humanas pendientes.
