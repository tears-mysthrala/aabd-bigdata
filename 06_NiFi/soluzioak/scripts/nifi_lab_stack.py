#!/usr/bin/env python3
"""Create/stop only the isolated lab; private credentials remain in /tmp.

The project, network and containers are dedicated; no personal infra is used.
MySQL 8.4 is the available source engine; this is not a MariaDB compatibility test.
"""
import argparse
import json
import secrets
import ssl
import subprocess
import time
from pathlib import Path
from nifi_lab_verificar import LAB, BASE, Lab

COMPOSE = 'name: bigdata-nifi-lab-20261002\nservices:\n  nifi:\n    image: iabd-nifi:2.0.0-local\n    container_name: bigdata-nifi-lab-20261002-nifi\n    hostname: nifi\n    environment:\n      SINGLE_USER_CREDENTIALS_USERNAME: ${NIFI_USER}\n      SINGLE_USER_CREDENTIALS_PASSWORD: ${NIFI_PASSWORD}\n      NIFI_SENSITIVE_PROPS_KEY: ${NIFI_SENSITIVE_PROPS_KEY}\n      NIFI_JVM_HEAP_INIT: 512m\n      NIFI_JVM_HEAP_MAX: 2g\n      NIFI_WEB_HTTPS_HOST: 0.0.0.0\n      NIFI_WEB_PROXY_HOST: localhost:18443,127.0.0.1:18443\n    ports:\n      - "127.0.0.1:18443:8443"\n    volumes:\n      - ./data:/opt/nifi/ariketak\n    networks: [lab]\n  mongo:\n    image: mongo:7.0\n    container_name: bigdata-nifi-lab-20261002-mongo\n    networks: [lab]\n  mysql:\n    image: mysql:8.4\n    container_name: bigdata-nifi-lab-20261002-mysql\n    environment:\n      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}\n      MYSQL_DATABASE: retail_db\n      MYSQL_USER: iabd\n      MYSQL_PASSWORD: ${MYSQL_PASSWORD}\n    volumes:\n      - /home/tears/bigdata/06_NiFi/soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2/create_db.sql:/docker-entrypoint-initdb.d/01.sql:ro\n    networks: [lab]\nnetworks:\n  lab:\n    name: bigdata-nifi-lab-20261002-net\n'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['up', 'down'])
    args = parser.parse_args()
    if args.action == 'up':
        LAB.mkdir(mode=0o700, exist_ok=True)
        LAB.chmod(0o700)
        if (LAB / 'credentials.json').exists():
            raise SystemExit('Existing lab credentials: do not overwrite a running/shared lab')
        credentials = {
            'NIFI_USER': 'labuser', 'NIFI_PASSWORD': secrets.token_urlsafe(24),
            'NIFI_SENSITIVE_PROPS_KEY': secrets.token_urlsafe(32),
            'MYSQL_ROOT_PASSWORD': secrets.token_urlsafe(24),
            'MYSQL_PASSWORD': secrets.token_urlsafe(24)}
        for name, data in [('credentials.json', json.dumps(credentials)),
                           ('.env', '\n'.join(f'{k}={v}' for k,v in credentials.items())+'\n')]:
            path = LAB / name
            path.write_text(data)
            path.chmod(0o600)
        (LAB / 'data').mkdir()
        source = BASE / '06_MariaDB_MongoDB_Laborategia_DF2.2/create_db.sql'
        compose = COMPOSE.replace('/home/tears/bigdata/06_NiFi/soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2/create_db.sql', str(source))
        (LAB / 'compose.yml').write_text(compose)
        subprocess.run(['docker', 'compose', '-f', str(LAB/'compose.yml'), 'up', '-d'], check=True)
        for _ in range(90):
            try:
                cert = LAB/'nifi-cert.pem'
                cert.write_text(ssl.get_server_certificate(('localhost',18443)))
                cert.chmod(0o600)
                Lab()
                print('Dedicated NiFi lab ready on https://localhost:18443; certificate verified')
                return
            except (OSError, RuntimeError):
                time.sleep(2)
        raise SystemExit('NiFi startup/authentication timed out; lab left available for diagnosis')
    else:
        # Removes dedicated containers and anonymous volumes only, preserves host files.
        if not (LAB/'compose.yml').exists():
            raise SystemExit('Dedicated compose file not found')
        subprocess.run(['docker', 'compose', '-f', str(LAB/'compose.yml'), 'down', '--volumes'], check=True)

if __name__ == '__main__':
    main()
