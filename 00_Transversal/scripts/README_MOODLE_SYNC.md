# Sincronización de Moodle

El servicio `moodle-sync.timer` ejecuta `run_moodle_sync.sh` cada hora.
Las credenciales se leen de `~/.config/moodle-sync.env`; no se versionan.
El wrapper usa un bloqueo para impedir dos ciclos automáticos simultáneos.

## Qué se comprueba

- Se recorren las secciones del curso y las secciones adicionales encontradas
  en su navegación. Se descargan recursos, archivos de carpetas y adjuntos del
  enunciado de tareas; las entregas personales del alumnado se excluyen.
- El manifiesto conserva `assignments`: título, sección, URL, enunciado y
  fechas generales de cada tarea, incluso cuando no tiene adjuntos. Se leen
  únicamente `#intro` y `.activity-dates`, nunca entregas o calificaciones.
- Se compara SHA-256 del contenido, también cuando el tamaño no cambia.
- Los aliases internos se resuelven a su ruta canónica. Las rutas que escapan
  del repositorio y los accesos a `.git` se rechazan.
- Un recurso envuelto en una página Moodle se resuelve a su archivo adjunto.
  Las páginas de sesión o login no se guardan como PDF, CSV o notebook.
- Los DOCX nuevos o modificados se convierten a Markdown. Un DOCX sin cambios
  no regenera su Markdown existente, que puede contener correcciones docentes.
- Los enlaces externos quedan en `MOODLE_URLs.md`. Los notebooks de Google se
  intentan descargar sin cookies de Moodle y se valida su estructura JSON.
  Un enlace registrado no equivale a una descarga ni a acceso Google verificado.
- Antes de comparar o guardar un notebook se limpia su metadata personal
  de Colab/Jupyter y las rutas locales de sus outputs. Se conservan código,
  narrativa y resultados docentes. El SHA-256 del manifiesto corresponde a
  la copia limpia guardada, no a los bytes originales del proveedor. Cambios
  únicamente en identidades o metadata de ejecución no generan novedades.

## Google Drive privado: cuenta del centro

La sesión de Moodle no autentica Google Drive. Si un cuaderno se abre con la
cuenta del centro pero no se descarga públicamente, hace falta autorizar esa
cuenta para el sincronizador. El conector de Drive de la conversación y el
servicio local tienen autorizaciones independientes.

El servicio admite OAuth de Google y descarga esos `.ipynb` mediante Drive API.
No lee cookies del navegador, no cambia permisos de archivos y no solicita
contraseñas. El scope `drive.readonly` permite leer los archivos accesibles de
la cuenta, no únicamente estos ocho; el sincronizador solo pide los IDs
enlazados desde Moodle. Revisa ese alcance al autorizar.

1. Sigue la [configuración oficial de Google](https://developers.google.com/workspace/drive/api/quickstart/python):
   activa Drive API en un proyecto, configura el consentimiento y crea un
   cliente OAuth de tipo **Desktop app**. Si el proyecto es externo y está en
   modo de prueba, añade tu cuenta del centro como usuario de prueba. La
   política del centro puede requerir que su administrador apruebe la app.
2. Guarda el JSON del cliente **fuera del repositorio**, por ejemplo en
   `~/.local/share/aabd-moodle-sync/client_secret_google.json`, con permisos 600.
3. Desde la raíz del repositorio, inicia la autorización local:

   ```bash
   uv run --with 'google-auth==2.58.1' --with 'google-auth-oauthlib==1.4.1' \
     00_Transversal/scripts/google_drive_auth.py \
     --client "$HOME/.local/share/aabd-moodle-sync/client_secret_google.json"
   ```

   Selecciona **la cuenta del centro** en el navegador. La recepción de OAuth
   usa únicamente `127.0.0.1`, un puerto temporal, estado OAuth y PKCE.
4. La autorización se guarda en
   `~/.local/share/aabd-moodle-sync/google-drive-token.json`, con permisos 600.
   El servicio detecta esa ruta automáticamente. Una ruta alternativa se
   configura con `GOOGLE_DRIVE_TOKEN_FILE` en `~/.config/moodle-sync.env`;
   debe permanecer fuera de Git. No pegues el contenido del JSON en ese archivo.
5. Ejecuta un ciclo de verificación sin publicación:

   ```bash
   uv run --with playwright --with requests --with beautifulsoup4 \
     --with python-docx --with 'google-auth==2.58.1' \
     00_Transversal/scripts/moodle_sync.py --no-publish
   ```

   Ese comando necesita `MOODLE_USER` y `MOODLE_PASS` en el entorno, igual que
   el servicio. Comprueba los estados y hashes del manifiesto. Autorizar OAuth
   no demuestra por sí solo que los ocho archivos permitan descarga.

El servicio renueva y guarda los tokens de forma atómica sin login interactivo cuando Google lo permite. Si
la autorización caduca o se revoca, hay que repetir el paso de autorización;
no se convierte el fallo en una descarga válida. Un fallo al cargar o renovar
OAuth permite continuar las descargas de Moodle y probar los enlaces públicos;
el manifiesto registra el aviso y cualquier cuaderno que siga sin descargarse.
Si falla la descarga autenticada también se intenta la pública, con una sesión
separada que no recibe credenciales. Los mensajes del manifiesto
distinguen falta de OAuth local de errores HTTP de la API. Sin OAuth se conserva
el intento de descarga pública y el bloqueo de publicación de material pendiente.

**Estado verificado el 28 de septiembre de 2026:** cliente Desktop y autorización
de la cuenta del centro configurados fuera de Git, con permisos 600. Los ocho
cuadernos se descargaron realmente mediante Drive API y se contrastaron sus
SHA-256. El ciclo completo registró 52 archivos verificados, 55 actividades,
0 errores y 0 fuentes pendientes. Esto verifica la descarga, no la ejecución
ni la corrección didáctica de los cuadernos.

En una app externa en modo **En pruebas**, Google limita normalmente la
autorización renovable a siete días para este scope: puede ser necesario repetir
el consentimiento. Véase la [caducidad oficial de tokens](https://developers.google.com/identity/protocols/oauth2#expiration).
No se ha publicado la app ni cambiado su público para evitar esa limitación.

La cobertura y los hashes quedan en
[`MOODLE_SYNC_ESTADO.json`](../MOODLE_SYNC_ESTADO.json). El campo `errors`
recoge fallos de Moodle; `unavailable` recoge fuentes externas no descargadas
o actividades que requieren revisión manual. Las referencias web son enlaces,
no copias del sitio. El manifiesto no afirma que los contenidos sean correctos
didácticamente ni que las soluciones estén ejecutadas.

## Publicación

`--no-publish` descarga y valida sin commit ni push. Requiere las mismas
credenciales en el entorno que el servicio. No ejecutes dos ciclos a la vez.
Para una comprobación manual se admite `--browser-cdp <puerto>`: reutiliza
una sesión de Chromium que el usuario haya autorizado y autenticado. Se conecta
solo a loopback, lee únicamente cookies de Moodle en memoria, comprueba la
sesión y conserva el navegador abierto. No exporta cookies ni cambia las
credenciales del servicio. El modo horario sigue usando su login existente.

`--prepare-review` además prepara un commit local aislado para revisión,
sin subirlo: consulta el remoto para elegir su base, pero no cambia la rama,
el índice ni los archivos del usuario.

Si hay errores de Moodle, el modo automático termina con error y no publica.
Si Moodle se ha verificado pero queda material externo/manual pendiente, el
ciclo termina normalmente con el aviso **«material pendiente»**, sin commit ni
push. El código de salida cero indica que el ciclo ha terminado; no certifica
cobertura completa ni publicación. El manifiesto conserva el contador
`unavailable` y las fuentes que faltan. Se exige cobertura completa antes de
commit/push automáticos.
`--no-publish` permite verificar una cobertura parcial y dejar sus límites
documentados sin publicar. El modo automático compara **siempre** el material
gestionado con la rama remota base, también si el ciclo no descargó nada.
Así recupera material cuyo push falló después de un commit anterior.

La publicación usa `moodle_publish.py`: construye un snapshot con un índice
temporal a partir del remoto y añade solo el material verificado, sus Markdown
derivados, los registros de enlaces y el manifiesto. No publica el HEAD del
usuario ni incorpora sus commits o cambios ajenos. No modifica su rama ni su
índice y no propaga borrados. Las rutas con escapes, symlinks o archivos
ausentes se rechazan.

Garantías del snapshot diario (con regresiones en `test_moodle_publish.py`):

- Antes de reutilizar la rama `moodle-sync/<base>/<fecha>`, su diff contra
  la base debe estar contenido en el material verificado del ciclo; si la
  rama trae un fichero ajeno, la publicación se rechaza en vez de heredarlo.
- La fusión es por ruta y falla cerrada: una ruta se publica cuando la
  rama no la ha cambiado desde la base, y se preserva la rama cuando el
  checkout conserva la versión de la base. Si base, rama y checkout
  difieren los tres, la publicación se rechaza (conflicto) porque el orden
  causal no puede probarse. Para los ciclos automáticos, se observan la base
  y la rama diaria **antes** de descargar/verificar las fuentes. Si ambas
  siguen en esos mismos commits al publicar, se admite la actualización
  verificada posterior, aunque haya tres versiones distintas. Si el remoto
  avanza, la base cambia o el ciclo cruza de fecha, se rechaza la observación
  y se exige un ciclo completo nuevo; observar solo al final no es válido.
  Sin esa observación se mantienen las reglas conservadoras anteriores.
  Cada ciclo pasa el
  conjunto gestionado completo (`SYNC_MANAGED`) que quiere preservar.
- Antes de crear el commit se contrastan los SHA-256 de los blobs del índice
  temporal con los hashes del ciclo verificado, también para archivos binarios.
  Una edición local posterior a la descarga o una versión conservada que no
  corresponda al manifiesto bloquea la publicación; no viaja contenido sin verificar.

El snapshot diario se sube a una rama estable
`moodle-sync/<base>/<fecha>` y se comprueba el commit realmente publicado.
Si el ciclo encuentra más cambios el mismo día, añade un commit de avance
rápido a esa misma rama; no crea otra rama por hash. **Nunca se fuerza un push
ni se escribe directamente en `master`**. Al comienzo de la siguiente jornada
se puede abrir una PR con la rama del día anterior y, después de integrarla,
el siguiente ciclo diario parte de la nueva base remota. Publicar la rama no
equivale a integrar el material.
Si la rama diaria ya es ancestro de la base (merge mediante PR), un ciclo
sin novedades termina como material ya integrado. Si llegan nuevas descargas
ese mismo día, continúa la misma rama a partir de la base actual mediante
avance rápido, conservando los cambios de código y documentación integrados.
El remoto y la base se pueden indicar con `MOODLE_GIT_REMOTE` (por defecto
`origin`) y `MOODLE_BASE_BRANCH` (`master`), sin cambiar credenciales ni reglas
de protección.

Regresiones locales, sin Moodle ni GitHub real:

```bash
uv run --with pytest --with requests --with beautifulsoup4 python -m pytest -q 00_Transversal/scripts/test_moodle_publish.py 00_Transversal/scripts/test_moodle_sync_auth.py
```

Usan un remoto bare con `master` protegida y comprueban recuperación tras un
push fallido, idempotencia, conservación de HEAD/índice/cambios locales,
exclusión de commits ajenos, preparación sin push y rechazo de rutas inválidas.
También se verifican varios ciclos sucesivos, carreras desde checkouts
independientes con observaciones previas y limpieza idempotente de notebooks.

Los registros locales `moodle_sync.log` y el journal se conservan fuera del
contenido publicado. No adjuntes HTML de sesión, cookies ni credenciales a una
incidencia de sincronización.

## Verificación manual del 28 de septiembre de 2026

- Último ciclo real con `--no-publish` y OAuth: 13 secciones, 55 actividades, 52 archivos
  verificados, **0 errores y 0 fuentes pendientes**. Los 52 SHA-256 del manifiesto se
  contrastaron de nuevo con los archivos guardados.
- Se registraron cuatro referencias web y ocho notebooks externos descargados.
  Antes de configurar OAuth, la consulta de esos IDs con el conector de Drive devolvió
  HTTP 404 en todos: no permite distinguir archivos retirados de falta de acceso
  de la cuenta conectada. La autorización local independiente devolvió HTTP 200
  y permiso de descarga para los ocho, y permitió guardar copias verificadas.
- Los ocho cuadernos cumplen el esquema `nbformat` 4, sin ejecutar sus celdas.
  Se comprobó una renovación real del token con Google, su guardado privado
  y una lectura posterior de metadatos. Gitleaks no detectó secretos en el
  material de Programación. Las ramas de fallo de OAuth y descarga pública
  alternativa no se han provocado contra servicios reales.
- La guía original `ML_ereduak_euskaraz.html` se descargó desde `pluginfile.php`.
  La página envolvente `view.php`, con datos de sesión, se retiró del árbol y del
  historial publicable. Su evidencia se conserva fuera del repositorio con
  permisos privados; no se borraron los registros de sincronización.
- Comprobaciones locales: aliases internos, escapes de ruta, rechazo de HTML de
  login, cambios de igual tamaño, contenido idéntico y redirecciones sin reenviar
  cookies. Se comprobó mediante simulación que una cobertura parcial bloquea
  la publicación y que el push usa el HEAD de la rama actual y verifica su hash.
- En esa primera verificación no se hizo push ni merge: se esperaba a disponer
  también de los ocho notebooks. Posteriormente el usuario autorizó la
  publicación e integración manual de lo verificado. El temporizador sigue sin
  publicar mientras el manifiesto indique material pendiente.

## Rechazo de login y bloqueo de cuenta

Un aviso explícito de cuenta bloqueada o login inválido detiene el ciclo
tras ese intento, con mensaje fijo y sin copiar datos de la página. Los
fallos de red conservan los reintentos limitados. La detección se verifica
con `test_moodle_sync_auth.py`; no evita todos los posibles bloqueos ni
renueva credenciales.

Si Moodle bloquea la cuenta, pausa el timer para que no siga intentando:

```bash
systemctl --user stop moodle-sync.timer
```

El usuario debe abrir el enlace de desbloqueo enviado por Moodle. No copiar
el enlace, cookies ni contraseñas al chat o al repositorio. Después verifica
un único ciclo del servicio y, si termina correctamente, reactiva el timer:

```bash
systemctl --user start moodle-sync.service
systemctl --user show moodle-sync.service -p Result -p ExecMainStatus
systemctl --user start moodle-sync.timer
```

Si sigue fallando, deja el timer pausado y diagnostica el acceso configurado;
no cambies credenciales automáticamente. `inactive (dead)` en el servicio
oneshot puede ser normal: contrastar `Result=success` y `ExecMainStatus=0`.

El recuento de archivos actualizados corresponde solo a cambios reales del ciclo. El material pendiente de integrar en Git se comprueba por separado contra la base remota, sin volver a anunciarlo como descarga nueva cada hora.
