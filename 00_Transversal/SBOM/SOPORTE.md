# Periodo de soporte declarado (plantilla local, CRA art. 13)

El CRA exige declarar cuánto tiempo se da soporte de seguridad a cada producto
y mantener la documentación durante ese periodo (o 10 años, lo mayor).
Mientras un módulo sea solo lab académico, su fila dice `lab — sin soporte`.
Al reutilizar un módulo fuera del lab, se rellena su fila: eso fija el
compromiso y el archivo de SBOMs versionadas que hay que conservar.

| Módulo / ruta | Estado | Versión en uso | Soporte hasta | Responsable |
|---|---|---|---|---|
| `01_Erronka1_CNC_Guard/proyecto_cnc_guard` | lab — sin soporte | — | — | — |
| `06_NiFi/soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2` | lab — sin soporte | — | — | — |
| `04_Programazioa_5073/soluzioak` | lab — sin soporte | — | — | — |

Baseline: `releases/0.1.0/` (2026-09-22, 3199 componentes, alcance `~/bigdata`).
Rutas antiguas (`erronka1/…`, `soluzioak/03_…`) → ver `../../INDICE.md` (reorg 2026-09-22, symlinks compat).

Regla: cada versión en uso tiene su SBOM en `SBOM/releases/<version>/`
(generada con `sbom-release.sh`). Sin SBOM archivada no hay reutilización.
