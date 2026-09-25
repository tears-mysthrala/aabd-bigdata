# 4.4: `.gitignore` laborategi isolatua

2026-09-25ean `/tmp`-ko Git repo berri batean `.gitignore`, `.venv/`,
fikziozko `.env` (`API_KEY=ezkutua123`) eta `PULL_REQUEST_TEMPLATE.md`
sortu dira, **commit edo push gabe**. `git status --short`-ek
`.gitignore` eta PR txantiloia bakarrik erakutsi ditu. `git check-ignore -v`
irteerak `.venv/pyvenv.cfg` lehenengo patroiarekin eta `.env` bigarrenarekin
baztertu direla erakutsi du.

Hau 4.4ko bazterketa-teknikaren proba da. PDFak 4.3ko benetako bi
lankideen GitHub repoan egitea eskatzen du; repo hori eta benetako PRak
ez daude hemen, eta ez dira sortu.
