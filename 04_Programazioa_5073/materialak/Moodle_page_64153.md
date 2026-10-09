# AZTERKETA PRESTATZEKO GIDA Orria

Fuente: https://elearning20.hezkuntza.net/012053/mod/page/view.php?id=64153

Copia automática del texto docente; no incluye el envoltorio de sesión.

AABD 1. Erronka: Azterketa Prestatzeko Gida
Dokumentu honen helburua lehen erronkako otsaileko deialdiko azterketa prestatzen laguntzea da (deialdi ofizialak, ekainean). Azterketak bi zati izango ditu:
Teorikoa (3 puntu)
eta
Praktikoa (7 puntu)
.
1. ZATIA: AZTERKETA TEORIKOA (3 Puntu)
Nola izango da?
30 test galdera (a, b, c, d aukerekin). Galdera okerrak zigortuko dira.
Materiala:
EZ
da onartzen apunterik edo ordenagailurik zati honetarako.
Zer prestatu behar duzu?
Apunteetan (PDF) lantzen diren kontzeptuak, bereziki
ideia nagusi
gisa edo
kontuz
abisuekin markatuta daudenak. Ebaluatuko dena zera da: teknologia bakoitza
ZERGATIK
eta
ZERTARAKO
erabiltzen den ulertzea, kode zehatza buruz jakitea baino gehiago.
Autoebaluaziorako Galdera Ereduak (Adibideak)
Hona hemen azterketan aurki ditzakezun galdera moten 5 adibide:
1. Zein da Java programazio-lengoaiaren indargunea eta erabilera tipikoa Adimen Artifizialeko proiektuetan?
a) Estatistika eta bistaratze aurreratua, ikerketa akademikoan. b) ML ekosistema zabalena, datu-zientzian eta LLM ereduen sorkuntzan. c) Errendimendu altua eta ekoizpen-sistema sendoak, Big Data ingurunean (Hadoop, Spark). d) Nabigatzaileen integrazioa, ereduak bezeroaren aldean exekutatzeko.
(Erantzun zuzena: C)
2. Zer da Model Context Protocol (MCP) eta zein da bere funtzio nagusia agenteen ekosisteman?
a) Pythonen bertsio berri bat instalatzeko protokolo segurua da. b) Agentea kanpoko sistemetara (datu-baseak, GitHub, Slack) modu estandarrean konektatzeko balio duen protokoloa da (agenteen "USB ataka"). c) IDE desberdinen artean itxura grafikoa partekatzeko fitxategi-formatua da. d) Git adarrak automatikoki batzeko tresna da.
(Erantzun zuzena: B)
3. Matplotlib liburutegian, zein da grafiko baten egitura osatzen duten bi oinarrizko kontzeptuak bereizteko modua?
a) Window eta Panel. b) Figure (orri osoa) eta Axes (grafiko indibiduala bere ardatzekin). c) Canvas eta Plot. d) Graph eta Chart.
(Erantzun zuzena: B)
4. Datu-garbiketan, zertarako erabiltzen da dropna() funtzioa Pandas-en?
a) Datu-base osoa ezabatzeko memoria askatzeko. b) Balio falten (NaN) ordez batezbestekoa jartzeko. c) Balio faltadun errenkadak edo zutabeak ezabatzeko. d) Bikoiztutako datuak garbitzeko.
(Erantzun zuzena: C)
5. REST API baten bidez ML eredua eskaintzean (FastAPI-rekin, adibidez), noiz eta nola da egokiena eredua kargatzea?
a) Bezeroak GET eskaera bat egiten duen bakoitzean. b) APIaren abiaraztean (startup-ean) behin bakarrik, eskaera bakoitzean ehunka megabyte deskargatzea saihesteko. c) POST eskaera bat jasotzen den bakoitzean. d) Aplikazioa itxiko denean soilik.
(Erantzun zuzena: B)
2. ZATIA: AZTERKETA PRAKTIKOA (7 Puntu)
Nola izango da?
Problemaren testuinguru bat eta CSV datu-multzo zikin bat emango zaizkizu. Jupyter Notebook batean programazio ariketa bat ebatzi beharko duzu.
Materiala:
BAI
, klaseko apunteen kopia izango duzue makina birtualean, PDFak. (Internet ez da erabilgarri egongo, ezta LLM/AI laguntzailerik ere).
Aholkua:
Ez ikasi kodea buruz, ulertu zati bakoitzak zer egiten duen, emango zaizun testuinguru BERRIRA egokitu behar baituzu. ML eraiketarako 5 pausoak argi eta eskuragarri izan.
Ebaluatuko diren Trebetasun Praktikoak (Checklist-a)
Azterketa praktikoan 7 puntuko nota ateratzeko, honako hauek menperatu behar dituzu:
Python Oinarriak:
list comprehension
bat idaztea zerrendak edo zutabe izenak eraldatzeko (adibidez, letrak aldatzeko edo karaktereak ordezkatzeko).
Pandas Iragazkiak:
Datu-garbiketa Scikit-Learn erabili gabe egitea. Jakin behar duzu errenkadak baldintzen arabera kentzen (adibidez, balio negatiboak ekiditen) eta balio nuluak (
NaN
) kudeatzen.
ML Pipeline-en Eraikuntza:
Scikit-Learn
liburutegiko
Pipeline
bat sortzea, aurreprozesamendu pauso bat (adib.
StandardScaler
) eta ML eredu sailkatzaile edo erregresiorako bat lotuz.
Klaseen Desoreka Kudeatzea:
Ulertzea nola eta zergatik aplikatu behar den
class_weight='balanced'
parametroa (edo noiz ez den beharrezkoa ereduaren arabera).
Metriken Interpretazioa:
Ereduaren iragarpenak egitea eta
Accuracy
-tik haratago joatea. Esate baterako,
Recall
metrika kalkulatzekotan, kasu zehatz horretarako zergatik den metrika kritikoa argudiatzen jakin behar duzu.
Classification_report
eta
Confusion-Matrix ZUZEN
interpretatzea eta deskribatzea.
API Eskemak (Pydantic):
Datu-sarrerak balioztatuko dituen
BaseModel
klase bat sortzea eta
@field_validator
bat inplementatzea neurrigabeko datuak (adibidez, 0 baino txikiagoak direnak) blokeatzeko.
