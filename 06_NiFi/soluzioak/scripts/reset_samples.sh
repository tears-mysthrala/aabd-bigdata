#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARIKETAK="$DIR/ariketak"

echo "Restoring sample files for exercises..."

# 01-ariketa-getfile-putfile
mkdir -p "$ARIKETAK/01-ariketa-getfile-putfile/sarrera"
mkdir -p "$ARIKETAK/01-ariketa-getfile-putfile/irteera/gatazkak"
echo "Proba 01 edukia" > "$ARIKETAK/01-ariketa-getfile-putfile/sarrera/proba_01.txt"
echo "Proba 02 edukia" > "$ARIKETAK/01-ariketa-getfile-putfile/sarrera/proba_02.txt"
echo "Proba 03 edukia" > "$ARIKETAK/01-ariketa-getfile-putfile/sarrera/proba_03.txt"

# 02-ariketa-csv-iragazi
mkdir -p "$ARIKETAK/02-ariketa-csv-iragazi/sarrera"
mkdir -p "$ARIKETAK/02-ariketa-csv-iragazi/irteera"
cat << 'EOF' > "$ARIKETAK/02-ariketa-csv-iragazi/sarrera/salmentak.csv"
ProductID;Date;Zip;Units;Revenue;Country
725;1/15/1999;41540;1;115.5;Germany
850;2/03/1999;75000;3;245.0;France
425;3/21/1999;28013;1;87.25;Spain
725;4/12/1999;75008;5;577.5;France
910;5/05/1999;10115;2;230.0;Germany
850;6/30/1999;69001;4;392.0;France
EOF

# 03-ariketa-atributuak-linajea
mkdir -p "$ARIKETAK/03-ariketa-atributuak-linajea/irteera"

# 05-ariketa-csv-json
mkdir -p "$ARIKETAK/05-ariketa-csv-json/sarrera"
mkdir -p "$ARIKETAK/05-ariketa-csv-json/irteera"
cat << 'EOF' > "$ARIKETAK/05-ariketa-csv-json/sarrera/datuak.csv"
id;izena;adina;hiria;soldata
1;Ane;28;Donostia;32000.50
2;Mikel;34;Bilbo;41000.00
3;Jon;22;Gasteiz;24500.75
4;Leire;41;Iruña;53000.20
5;Aitor;30;Eibar;36000.00
EOF

# 06-ariketa-mariadb-mongodb
mkdir -p "$ARIKETAK/06-ariketa-mariadb-mongodb"
[ -f /tmp/mysql-connector-j-8.0.31.jar ] && cp /tmp/mysql-connector-j-8.0.31.jar "$ARIKETAK/06-ariketa-mariadb-mongodb/"
[ -f /tmp/create_db.sql ] && cp /tmp/create_db.sql "$ARIKETAK/06-ariketa-mariadb-mongodb/"

# 07-ariketa-aemet-datalake
mkdir -p "$ARIKETAK/07-ariketa-aemet-datalake"

chmod -R 777 "$ARIKETAK"
echo "Sample files successfully restored in $ARIKETAK!"
