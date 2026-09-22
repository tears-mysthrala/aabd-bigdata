# SBOM de `~/bigdata` — nota de alcance y CRA

Generado: 2026-09-21 · Herramienta: `syft 1.51.0` · Fuente: directorio `/home/tears/bigdata`.

- `sbom.cyclonedx.json`: CycloneDX **1.7**, 3505 componentes.
- `sbom.spdx.json`: SPDX **2.3**, 2220 paquetes.
- `sbom-release.sh <version> [ruta]`: SBOM versionada por release en `releases/<version>/` + `INDICE.csv`. Una release no se sobrescribe.
- `SOPORTE.md`: periodo de soporte declarado por módulo (todo en `lab — sin soporte` hasta reutilizar).
- `FICHA-TECNICA.md`: plantilla de ficha por módulo reutilizado (Anexo VII).
- Política de vulnerabilidades: `/home/tears/bigdata/SECURITY.md` (detalle CNC en `erronka1/cnc_guard_setup/SECURITY.md`).
- Regenerar base: `syft /home/tears/bigdata -o cyclonedx-json=SBOM/sbom.cyclonedx.json -o spdx-json=SBOM/sbom.spdx.json`
- Imágenes de laboratorio (declaradas en `soluzioak/03_DataFlow_Apache_NiFi/06_MariaDB_MongoDB_Laborategia/docker-compose.yml`,
  no descargadas aquí): `apache/nifi:2.0.0`, `mysql:8.4`, `mongo:7.0`, más `mysql-connector-j-8.0.31.jar`.
  Tras `docker pull`, generar su SBOM por imagen: `syft mysql:8.4 -o cyclonedx-json=SBOM/sbom-mysql.cyclonedx.json`.

## Estado normativo UE (consultado hoy, 2026-09-21)

Reglamento (UE) 2024/2847 (CRA): en vigor desde 10-12-2024.
- 11-06-2026: aplicables las reglas de organismos de evaluación de la conformidad.
- **11-09-2026 (hace 10 días): aplicables las obligaciones de notificación del art. 14**
  (vulnerabilidades explotadas activamente e incidentes graves: aviso 24h, notificación 72h,
  informe final 14 días/1 mes, vía plataforma única ENISA).
- **11-12-2027: aplicación plena**, incluida la SBOM (Anexo I, parte II, punto 1).

Requisito SBOM del CRA (piso legal, no formato impuesto):
- Documento legible por máquina, en formato de uso común (en la práctica: CycloneDX o SPDX),
  que cubra **como mínimo las dependencias de primer nivel**, y mantenerlo actualizado.
- Forma parte de la documentación técnica (Anexo VII): se entrega a la autoridad de vigilancia
  **previa solicitud motivada**, no hay obligación de publicarlo. Conservarlo 10 años tras la
  comercialización o durante el periodo de soporte si es mayor.
- Sin acto de ejecución aún que fije formato/campos; la referencia técnica más concreta es
  BSI TR-03183-2 v2.1.0 (CycloneDX ≥1.6 o SPDX ≥3.0.1, JSON/XML). Este SBOM cumple el piso del
  Reglamento (CycloneDX 1.7; SPDX 2.3 = ISO/IEC 5962:2021). Si un cliente/autoridad exige
  SPDX 3.x, regenerar con una herramienta que lo emita.
- La SBOM **no** contiene información de vulnerabilidades (dato estático); para eso: VEX/CSAF
  y gestión de vulnerabilidades continua.

## Alcance honesto

`~/bigdata` es un laboratorio académico, **no** un producto con elementos digitales
comercializado en la UE. Este SBOM es higiene de inventario (saber qué librerías/JARs/imágenes
usa el lab), **no** una declaración de conformidad CRA ni la sustituye: el CRA exige además
requisitos esenciales del Anexo I, evaluación, soporte, actualizaciones de seguridad,
documentación técnica completa y notificaciones. Regenerar el SBOM con cada cambio de
dependencias; una SBOM de hoy caduca en el primer `uv lock --upgrade`.
