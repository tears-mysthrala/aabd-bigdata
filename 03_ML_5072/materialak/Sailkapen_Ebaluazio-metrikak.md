# Sailkapen Metrikak Machine Learning-en (transkripzioa)

Jatorria: Moodle `id=64238` baliabidea (`Sailkapen Ebaluazio-metrikak.png`,
`03_ML_5072/materialak/`). Irudiaren testu-transkripzio fidela, bilagarria
egiteko (ikusi jatorrizko PNGa diseinu osoarekin).

## 1. Zehaztasuna (Accuracy)

**Accuracy = (TP + TN) / Guztizkoa**

- Zer neurtzen du: Asmatutako kasu guztien ehunekoa (positibo zein negatibo).
- Noiz erabili: Klaseak OREKATUTA daudenean (%50 / %50).
- Kautela: Klase desorekatuetan oso engainagarria izan daiteke.

## 2. Doitasuna (Precision)

**Precision = TP / (TP + FP)**

- Zer neurtzen du: 'Positibo' iragarritako guztietatik zenbat diren benetan Positibo.
- Gakoa: Positibo Faltsuek (FP) kostu handia dutenean.
- Adibidea (SPAM): Mezu legeko bat (FP) SPAMera bideratzea oso kalitatiboki kaltegarria da.

## 3. Estaldura (Recall)

**Recall = TP / (TP + FN)**

- Zer neurtzen du: Benetako Positibo guztietatik zenbat harrapatu dituen ereduak.
- Gakoa: Negatibo Faltsuek (FN) kostu handia dutenean.
- Adibidea (Minbizia): Gaixorik dagoen norbaiti (FN) 'osasuntsu zaude' esatea arriskutsua da.

## 4. F1 Puntuazioa (F1-Score)

**F1 = 2 · (Precision · Recall) / (Precision + Recall)**

- Zer neurtzen du: Precision eta Recall-en arteko batez besteko harmonikoa.
- Noiz erabili: Precision eta Recall-en arteko oreka behar denean.
- Ezin hobea: Klase desorekatuak daudenean.

> **Ohar didaktikoa (ez da irudikoa):** F1-ak negatibo zuzenak (TN) ez ditu
> kontuan hartzen; klase desorekatuetan erabilgarria da positiboen
> Precision/Recall oreka bada helburua, ez orokorrean "ezin hobea".

## 5. ROC-AUC (ROC-AUC Score)

**AUC ∈ [0.5, 1.0]** (0.5 = Ausaz, 1.0 = Perfektua)

> **Ohar didaktikoa (ez da irudikoa):** AUC teorikoki [0, 1] da; 0.5etik behera
> ausaz baino okerragoa (alderantzizko sailkatzailea).

- Zer neurtzen du: Bi klaseak bereizteko gaitasun orokorra atalase guztietan.
- Gakoa: Probabilitateak (y_proba) erabiltzen ditu, ez iragarpen Finkoak (y_irag).
- Ez du atalase zehatz baten mende egoten (orokorra da).
