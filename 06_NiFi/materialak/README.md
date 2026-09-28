# Material docente de NiFi: notas de seguridad y vigencia

Los PDF son material original de clase. Sus comandos `docker run` y el Compose
original del ejercicio 6 incluían credenciales conocidas, etiquetas `latest`
y puertos publicados en todas las interfaces. No se deben ejecutar
literalmente en una máquina conectada a una red.

El Compose de `06-ariketa-mariadb-mongodb/` se ha ajustado para publicar
8443/3306/27017 solo en `127.0.0.1` y exigir las contraseñas desde variables
de entorno. Deben ser únicas para cada laboratorio. MongoDB sigue sin
autenticación dentro de la red Docker de ese ejemplo, por lo que este stack
solo sirve para un laboratorio aislado. Para la práctica integrada, usar el
Compose y las instrucciones de
`../soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2/`.

La presencia de un flow JSON o de un comando en el PDF no demuestra que
NiFi, MongoDB ni un servicio HTTP estén funcionando.
