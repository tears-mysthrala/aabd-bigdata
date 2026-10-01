# CNC Guard erronkako laguntza-materialak

Hemen daude erronkako entregak prestatzen laguntzeko fitxategiak:

- [Erronkako entregen txantiloia](Erronka_Entregak_Txantiloia.md): ekipo-kontratua eta rolak, helburu pertsonalak, behin-behineko eta behin betiko proposamen bereiziak, talde-plangintza/kontrol-puntuak eta azken aurkezpenaren egitura.
- [Autoebaluazio eta koebaluazio txantiloiak](Ebaluazioa_Txantiloia.md): norberaren autoebaluaziorako eta taldekide bakoitzari buruzko koebaluazio bereizirako eremu hutsak.
- [Tortilla PERT/Gantt ariketaren ebazpena](Patata_Tortila_PERT_Gantt_Ebazpena.md): plangintza-ariketa horren erantzun-eredua.
- [CNC Guard proiektuaren laburpena](Ebazpena_CNC_Guard_eta_AA_Ereduak.md): proiektuaren testuinguru teknikoa eta eredu-arkitektura.

Txantiloiak erronkaren [txostenean](../materialak/1Erronka_ikaslearen_txostena.docx.pdf), [ANEXO1ean](../materialak/ANEXO1-Eus.md) eta [ANEXO4an](../materialak/ANEXO4.md) oinarrituta daude. Formatu editagarri honetan ez dago benetako talde-identitaterik, izenik, rol-esleipenik, konpromisorik, sinadurarik, bertaratze-daturik, proposamen adosturik edo ebaluazio-irizpenik. Ikasleek eta irakasleek benetako datu eta ebidentziekin bete behar dituzte. Aurkezpenaren atala antolaketa-gida hutsa da; txostenak ez du diapositiba-sekuentzia zehatzik ezartzen.

## Cómo estudiar y comprobar estas entregas

1. Lee el enunciado y el resumen técnico para distinguir objetivos propuestos
   de componentes implementados.
2. Para ejecutar, sigue el [README del proyecto](../proyecto_cnc_guard/README.md):
   define entorno, dato `cnc_10M.csv`, pruebas y límites. El CSV grande se genera
   localmente y no se incluye en Git; no basta con abrir el notebook para tenerlo.
3. Para planificación, [PERT/Gantt](Patata_Tortila_PERT_Gantt_Ebazpena.md)
   explica dependencias, tiempos y supuestos. Recorre cada arco y comprueba que
   ningún inicio anteceda al fin de sus predecesores; 35/44 minutos corresponden
   a sus supuestos de recursos paralelos/un solo cocinero.
4. Para entregas de equipo, copia las plantillas y completa únicamente tus
   hechos reales. No rellenes nombres, firmas, asistencias o autoevaluaciones
   con datos inventados.

El prototipo clasifica errores sintéticos del mismo instante. Su accuracy alta
no equivale a detectar bien la clase minoritaria: lee también F1 y la matriz de
confusión. Ni los resultados sintéticos ni las pruebas de funciones demuestran
anticipación temporal de averías en una CNC real.
