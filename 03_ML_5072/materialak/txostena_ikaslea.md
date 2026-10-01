# Sailkapen Txostena (Ikaslearen Txantiloia)

Txosten honek **Iris loreen datu-multzoa** erabiliz egindako sailkapen-ariketaren emaitzak eta ondorioak laburbiltzen ditu. Ariketa egin ondoren, osatu hutsuneak zure emaitza eta hausnarketekin.

## 1. Helburua
Ariketa honen helburua sailkatzaile lineal baten (**Erregresio Logistikoa**) eta sailkatzaile ez-lineal baten (**KNN**) portaera alboz albo alderatzea da. Lorearen sepalaren neurriak (luzera eta zabalera) erabiliz, lorea zein klasekoa den (Setosa, Versicolor, Virginica) iragartzea da helburua.

## 2. Emaitzak eta Zehaztasuna
Eredu bakoitza Iris datu-multzoko lehenengo bi ezaugarriekin entrenatu ondoren, osatu taula hau lortu duzun zehaztasunarekin (accuracy):

| Eredua | Doitasuna (Accuracy) | Muga Mota |
| :--- | :--- | :--- |
| **Erregresio Logistikoa** | `[OSATU HEMEN: Zehaztasun %]` | Lineala (Lerro zuzenak) |
| **KNN (K=3)** | `[OSATU HEMEN: Zehaztasun %]` | Ez-lineala (Kurbatua) |

## 3. Erabaki-Mugen Analisi Bisuala
Ereduak hobeto ulertzeko, euren erabaki-mugak planoan marraztu ditugu:

![Erabaki Mugak](irudiak/erabaki_mugak.png)

### Hausnarketa galderak (Osatu zure hitzekin):

1. **Setosa klasearen banaketa**: Nola sailkatzen du Setosa klasea (puntu urdinak) eredu bakoitzak? Erraza al da beste klaseetatik banatzea?
   * *Erantzun hemen*: 

2. **Lerro zuzenak vs kurba kurbatuak**: Zer ezberdintasun nabaritzen duzu Erregresio Logistikoaren erabaki-mugen (lerroak) eta KNNren erabaki-mugen (kurbak) artean? Zein moldatzen da hobeto datu-puntu isolatuetara?
   * *Erantzun hemen*: 

3. **Overfitting arriskua**: KNN ereduan bizilagun kopurua oso txikia bada ($K=1$ adibidez), zer gertatuko litzateke mugekin? Hausnartu ereduak orokortzeko duen gaitasunari buruz.
   * *Erantzun hemen*: 
