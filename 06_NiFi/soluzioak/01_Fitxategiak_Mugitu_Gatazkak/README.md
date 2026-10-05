# NiFi 1. Kasua: Fitxategiak Mugitu eta Gatazkak Kudeatu (Caso 1)

## Ejecución verificada y evidencia

2026-10-02: NiFi 2.0.0 movió los tres archivos originales. Se reintrodujo
`proba_01.txt` con otro contenido; el original quedó idéntico y la nueva
entrada se guardó en `gatazkak` con prefijo de tiempo. Resultado: tres
archivos normales, uno de conflicto y cuatro eventos RECEIVE. El fallo de
PutFile por conflicto es intencionado y se verifica por la salida alternativa.
[Resultado](evidencias/resultado_2026-10-02.json),
[archivos reales](evidencias/irteera/) y
[provenance](evidencias/flow_01_fitxategiak_mugitu_provenance.json).


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
   # Biltegiaren erroan:
   bash 06_NiFi/soluzioak/scripts/reset_samples.sh
   ```
   Scriptak Composeko `06_MariaDB_MongoDB_Laborategia_DF2.2/ariketak/`
   muntatzean idazten du eta lehendik dauden lagin sarrerak ordezkatzen ditu.

2. **Fluxua abiarazi:**
   - Egiaztatu `sarrera/` karpeta hustu dela eta `irteera/` karpetan `proba_01.txt` eta `proba_02.txt` agertu direla.

3. **Gatazka simulatu:**
   - Sortu berriro `proba_01.txt` fitxategia `sarrera/` karpetan:
     ```bash
     echo "Proba 01 berria (gatazka sortuko du)" > 06_NiFi/soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2/ariketak/01-ariketa-getfile-putfile/sarrera/proba_01.txt
     ```
   - Egiaztatu `irteera/` karpetako jatorrizkoa ez dela ukitu, eta `irteera/gatazkak/` karpetan `<epoch_timestamp>-proba_01.txt` izenarekin gorde dela!


## Laboratorio aislado y reproducción

Los comandos siguientes se ejecutan desde la raíz y prueban los casos 1-6 en
una única instancia dedicada. No usan `infra/`, bases de datos personales ni
el canvas de otra instancia. Requieren Docker, Python 3 y las imágenes
`iabd-nifi:2.0.0-local`, `mongo:7.0` y `mysql:8.4`. Si falta la imagen local:

```bash
docker build -t iabd-nifi:2.0.0-local \
  06_NiFi/soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2
```

```bash
python 06_NiFi/soluzioak/scripts/nifi_lab_stack.py up
python 06_NiFi/soluzioak/scripts/nifi_lab_verificar.py prepare
python 06_NiFi/soluzioak/scripts/nifi_lab_ejecutar.py
python 06_NiFi/soluzioak/scripts/nifi_lab_evidencias.py
python 06_NiFi/soluzioak/scripts/nifi_lab_comparar.py
python 06_NiFi/soluzioak/scripts/nifi_lab_resultados.py
python 06_NiFi/soluzioak/scripts/nifi_lab_validar_evidencias.py
python 06_NiFi/soluzioak/scripts/nifi_lab_stack.py down
```

[Preparador](../scripts/nifi_lab_stack.py): Compose sanitizado embebido,
proyecto `bigdata-nifi-lab-20261002`, red dedicada y endpoint
`https://localhost:18443` publicado solo en loopback. Genera credenciales
aleatorias en `/tmp/bigdata-nifi-lab-20261002/credentials.json` y `.env`, con
modo 600 dentro de un directorio 700; exporta el certificado de NiFi y verifica
TLS y el hostname `localhost`. Ningún secreto entra en Git. No muestra tokens.
MySQL/MongoDB no publican puertos. No se sobreescribe un laboratorio existente.

[Importador](../scripts/nifi_lab_verificar.py) crea un PG propio y remapea
servicios/rutas solo dentro del laboratorio. [Ejecutor](../scripts/nifi_lab_ejecutar.py)
ejecuta SQL y GenerateFlowFile mediante `RUN_ONCE`; GetFile sondea entradas
con `Keep Source File=false` y se detiene al cerrar la prueba. Espera como
máximo diez minutos para
la carga SQL completa (puede necesitar ajuste en otra máquina), evita duplicar la carga SQL si las
colecciones ya tienen documentos y detiene su PG al terminar. Es una prueba
local: modifica solo directorios temporales, grupos y bases de datos del lab.
[Exportador](../scripts/nifi_lab_evidencias.py) guarda estados y provenance
acotado a 100 eventos por procesador; las listas largas de linaje conservan
20 UUID y el conteo total. Liberar resultados de consulta no borra eventos.
[Comparador](../scripts/nifi_lab_comparar.py) coteja todas las filas SQL/Mongo.
[Verificador de resultados](../scripts/nifi_lab_resultados.py) compara y archiva
los archivos reales y los documentos de muestra, sin guardar las filas de clientes.

La receta reúne los pasos ejecutados en esta sesión; no se ha repetido un
segundo arranque completo desde cero con el script conjunto. `down` retira
solo los contenedores y volúmenes del proyecto dedicado y conserva los
archivos temporales del host. Si se comparte con el caso 7, detener primero
su sidecar MinIO y coordinar el cierre. La evidencia versionada permite
[validación sin Docker](../scripts/nifi_lab_validar_evidencias.py).

**Límites:** ejecución real de NiFi por REST, contenido, logs y provenance;
no hay captura GUI. T3 abrió el HTTPS del lab pero no pudo cargar su
certificado en el navegador. La validación REST sí usa certificado verificado.
No se han accedido APIs con claves reales ni AWS.
