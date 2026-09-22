# Ficha técnica por módulo reutilizado (esqueleto local, Anexo VII CRA)

Copiar esta plantilla a la carpeta del módulo al reutilizarlo
(p. ej. `FICHA-TECNICA-0.1.0.md`) y rellenarla. Nada de aquí se publica:
se entrega a la autoridad de vigilancia solo previa solicitud motivada.

## 1. Identificación
- [ ] Nombre del producto / módulo y versión (misma que `SBOM/releases/<version>/`).
- [ ] Finalidad prevista y usos razonablemente previsibles (y usos excluidos).
- [ ] Responsable y fecha.

## 2. Diseño y requisitos esenciales (Anexo I, parte I)
- [ ] Superficie de ataque descrita (entradas, red, ficheros, credenciales).
- [ ] Medidas aplicadas por requisito (control de acceso, secretos fuera del repo,
      loopback por defecto, validación de entradas, mínimos privilegios).
- [ ] Dependencias externas y por qué cada una es necesaria.

## 3. Gestión de vulnerabilidades (Anexo I, parte II)
- [ ] SBOM archivada: `SBOM/releases/<version>/` (CycloneDX + SPDX).
- [ ] Política de divulgación coordinada: ver `/home/tears/bigdata/SECURITY.md`.
- [ ] Dirección de contacto de vulnerabilidades: ________________ (rellenar al reutilizar).
- [ ] Procedimiento de distribución segura de actualizaciones de seguridad.
- [ ] Compromiso de notificación (art. 14, aplicable desde 11-09-2026):
      aviso 24h / notificación 72h / informe final 14 días–1 mes vía plataforma ENISA.
      (Solo al comercializar en la UE; en lab basta conocer el procedimiento.)

## 4. Actualizaciones y soporte
- [ ] Periodo de soporte declarado (ver `SOPORTE.md`).
- [ ] Cómo se avisa al usuario de updates de seguridad y cómo se instalan.

## 5. Historial
- [ ] Cambios frente a la versión anterior y motivo (¿modificación sustancial?).
- [ ] Fecha de archivo y dónde se conserva (mínimo 10 años o soporte, lo mayor).

Nota VEX/CSAF: la SBOM no incluye explotabilidad. Si una autoridad o cliente
pregunta si te afecta un CVE concreto, se responde con un VEX puntual,
que se genera entonces, no se pre-publica.
