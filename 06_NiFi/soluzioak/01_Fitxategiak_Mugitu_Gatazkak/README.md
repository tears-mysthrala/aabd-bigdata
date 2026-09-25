# NiFi 1. Kasua: Fitxategiak Mugitu eta Gatazkak Kudeatu (Caso 1)

> **Modulua / Gai-arloa:** Big Data Aplikatua · 01 DataFlow · Apache NiFi  
> **Fluxuaren Definizioa:** [`flow_01_fitxategiak_mugitu.json`](flow_01_fitxategiak_mugitu.json)  
> **Iturria:** `GIDA Apache NiFi instalazioa eta kasu praktikoak 1-2-3-4.pdf` (3–12 orr.)

---

## 1. Helburua eta Testuingurua (Objetivo)

Fitxategiak sarrera-direktorio batetik (`/sarrera`) irteera-direktorio batera (`/irteera`) transferitzea datu-galerarik gabe. 
Helmugan izen bera duen fitxategi bat badago (**gatazka / conflict**):
1. Fitxategia **ez da gainidatziko**.
2. NiFi Expression Language (NEL) bidez denbora-zigilu unikoa (*timestamp*) gehituko zaio.
3. Fitxategi berrizendatua gatazka-direktorio berezi batera (`/irteera/gatazkak`) bideratuko da.

---

## 2. Arkitektura eta Fluxuaren Diagrama (Mermaid)

```mermaid
flowchart LR
    A["1. FitxategiaEskuratu<br/>(GetFile: /sarrera)"] -->|success| B["2. FitxategiaJarri<br/>(PutFile: /irteera)"]
    B -->|success| C(["✅ Helmuga Arrunta (Amaitu)"])
    B -->|failure (conflict)| D["3. UpdateAttribute<br/>(Gehitu timestamp unikoa)"]
    D -->|success| E["4. GatazkaFitxategiaMugitu<br/>(PutFile: /irteera/gatazkak)"]
    E -->|success| F(["🛡️ Gatazka Gordeta (Amaitu)"])

    classDef proc fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef term fill:#0f766e,stroke:#2dd4bf,stroke-width:2px,color:#ffffff;
    class A,B,D,E proc;
    class C,F term;
```

---

## 3. Prozesadoreen Konfigurazio Zehatza (Configuración)

| Prozesadorea | Mota / Klasea | Posizioa | Propietate Gakoak | Balioa / Azalpena |
| :--- | :--- | :--- | :--- | :--- |
| **`FitxategiaEskuratu`** | `GetFile` | `(100, 150)` | `Input Directory`<br/>`Keep Source File`<br/>`Minimum File Age`<br/>`File Filter` | `/opt/nifi/ariketak/01-ariketa-getfile-putfile/sarrera`<br/>`false` (iturburuko fitxategia ezabatu mugitzean)<br/>`2 sec` (idazketa partzialak saihesteko)<br/>`[^\.].*` (ezkutuak ez diren guztiak) |
| **`FitxategiaJarri`** | `PutFile` | `(550, 150)` | `Directory`<br/>`Conflict Resolution Strategy` | `/opt/nifi/ariketak/01-ariketa-getfile-putfile/irteera`<br/>**`fail`** (izen bera badago, failure harremanera bidali) |
| **`UpdateAttribute`** | `UpdateAttribute` | `(550, 400)` | Propietate dinamikoa: `filename` | **`${now():toNumber()}-${filename}`**<br/>Uneko epoch milisegundoak eransten dizkio izenari, bikoiztasuna ezabatuz |
| **`GatazkaFitxategiaMugitu`**| `PutFile` | `(1000, 400)` | `Directory`<br/>`Conflict Resolution Strategy` | `/opt/nifi/ariketak/01-ariketa-getfile-putfile/irteera/gatazkak`<br/>`fail` |

---

## 4. Erlazioen Kudeaketa (Relationships)

- **`FitxategiaEskuratu`**: `success` $\rightarrow$ `FitxategiaJarri`.
- **`FitxategiaJarri`**: 
  - `success`: **Auto-terminate** (fitxategia arrakastaz idatzi da).
  - `failure`: $\rightarrow$ `UpdateAttribute` (gatazka kudeatzeko bideratzea).
- **`UpdateAttribute`**: `success` $\rightarrow$ `GatazkaFitxategiaMugitu`.
- **`GatazkaFitxategiaMugitu`**: `success` eta `failure`: **Auto-terminate**.

---

## 5. Exekuzio eta Egiaztapen Proba (Cómo probar)

1. **Sarrerako laginak sortu:**
   ```bash
   mkdir -p /home/tears/nifi/ariketak/01-ariketa-getfile-putfile/sarrera
   mkdir -p /home/tears/nifi/ariketak/01-ariketa-getfile-putfile/irteera/gatazkak
   echo "Proba 01 edukia" > /home/tears/nifi/ariketak/01-ariketa-getfile-putfile/sarrera/proba_01.txt
   echo "Proba 02 edukia" > /home/tears/nifi/ariketak/01-ariketa-getfile-putfile/sarrera/proba_02.txt
   ```

2. **Fluxua abiarazi:**
   - Egiaztatu `sarrera/` karpeta hustu dela eta `irteera/` karpetan `proba_01.txt` eta `proba_02.txt` agertu direla.

3. **Gatazka simulatu:**
   - Sortu berriro `proba_01.txt` fitxategia `sarrera/` karpetan:
     ```bash
     echo "Proba 01 berria (gatazka sortuko du)" > /home/tears/nifi/ariketak/01-ariketa-getfile-putfile/sarrera/proba_01.txt
     ```
   - Egiaztatu `irteera/` karpetako jatorrizkoa ez dela ukitu, eta `irteera/gatazkak/` karpetan `<epoch_timestamp>-proba_01.txt` izenarekin gorde dela!
