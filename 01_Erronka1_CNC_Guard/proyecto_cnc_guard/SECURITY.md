# Política de seguridad

## Alcance

CNC Guard es una plantilla académica que procesa datos de mantenimiento y modelos de juguete. No debe conectarse a una CNC, red OT, broker, base de datos industrial o sistema de producción sin una autorización escrita, un entorno de pruebas aislado y un plan de reversión.

## Cómo informar de una vulnerabilidad

No publiques vulnerabilidades, credenciales, tokens, direcciones industriales ni archivos de datos sensibles en issues o pull requests.

En el repositorio de GitHub, utiliza **Security → Report a vulnerability** para crear un aviso privado. Si esa función no está habilitada, contacta de forma privada con los mantenedores del repositorio mediante el canal institucional del equipo docente. Incluye:

- descripción reproducible y versión o commit afectado;
- impacto, especialmente si puede afectar a una máquina o una red OT;
- pasos mínimos para reproducirlo, sin datos reales;
- logs saneados y una propuesta de mitigación si la tienes.

No realices pruebas activas contra máquinas, brokers o servicios de terceros para confirmar un hallazgo.

## Qué esperar

Confirmaremos la recepción en un plazo razonable y coordinaremos la evaluación con los responsables del repositorio. La corrección, el crédito y la publicación se decidirán según el impacto, la capacidad del equipo y las obligaciones académicas. No garantizamos un plazo de corrección para un proyecto de aula.

## Reglas de seguridad del proyecto

- Ejecuta Jupyter solo en `127.0.0.1` y conserva el token de autenticación.
- No uses `sudo pip`, `--system` ni dependencias instaladas fuera de `uv.lock`.
- Revisa los cambios de dependencias y ejecuta `pip-audit` antes de entregas importantes.
- Mantén permisos mínimos en GitHub Actions: el CI tiene `contents: read` y no recibe secretos.
- No uses `pull_request_target` para ejecutar código de una pull request.
- Trata `pickle` y `joblib` como formatos ejecutables: carga solo modelos generados y verificados por el propio equipo.
- El lock y el SBOM documentan dependencias Python, pero no certifican la seguridad del host, del firmware ni de una integración industrial.