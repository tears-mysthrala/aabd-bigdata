#!/usr/bin/env python3
"""Scoped NiFi 2 lab runner. Credentials/certificate stay outside the repository.

Only localhost:18443 is accepted. Never deletes groups or edits the root canvas.
Imports stopped snapshots below a freshly created cases 1-6 group.
"""
import argparse
import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
LAB = Path('/tmp/bigdata-nifi-lab-20261002')


class Lab:
    def __init__(self, directory=LAB):
        self.directory = Path(directory)
        self.credentials = json.loads((self.directory / 'credentials.json').read_text())
        self.context = ssl.create_default_context(cafile=str(self.directory / 'nifi-cert.pem'))
        self.token = None
        self.token = self.api('/access/token', 'POST', urllib.parse.urlencode({
            'username': self.credentials['NIFI_USER'], 'password': self.credentials['NIFI_PASSWORD']
        }), 'application/x-www-form-urlencoded')

    def api(self, path, method='GET', payload=None, content_type='application/json'):
        headers = {'Content-Type': content_type}
        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token
        if isinstance(payload, (dict, list)):
            payload = json.dumps(payload)
        body = payload.encode() if isinstance(payload, str) else payload
        request = urllib.request.Request('https://localhost:18443/nifi-api' + path, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, context=self.context, timeout=60) as response:
                raw = response.read().decode()
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return raw
        except urllib.error.HTTPError as error:
            # Avoid credentials/token in error logs; endpoints and response diagnostics only.
            raise RuntimeError(f'{method} {path}: HTTP {error.code}: {error.read().decode()[:1500]}') from error

    def create_group(self, parent, name):
        return self.api(f'/process-groups/{parent}/process-groups', 'POST', {
            'revision': {'version': 0}, 'component': {'name': name, 'position': {'x': 100, 'y': 100}}
        })['id']

    def service(self, pg, name, kind, artifact, properties):
        entity = self.api(f'/process-groups/{pg}/controller-services', 'POST', {
            'revision': {'version': 0}, 'component': {'name': name, 'type': kind,
            'bundle': {'group': 'org.apache.nifi', 'artifact': artifact, 'version': '2.0.0'}, 'properties': properties}})
        self.enable(entity['id'])
        return entity['id']

    def enable(self, identifier):
        for _ in range(30):
            entity = self.api(f'/controller-services/{identifier}')
            component = entity['component']
            if component.get('validationStatus') != 'VALIDATING':
                if component.get('validationErrors'):
                    raise RuntimeError(f"Service {component['name']}: {component['validationErrors']}")
                self.api(f'/controller-services/{identifier}/run-status', 'PUT', {
                    'revision': entity['revision'], 'state': 'ENABLED'})
                return
            time.sleep(.2)
        raise RuntimeError('Service validation timed out')

    def import_flow(self, pg, file, services, key):
        snapshot = json.loads(Path(file).read_text())
        encoded = json.dumps(snapshot)
        for old, new in services.items():
            encoded = encoded.replace(old, new)
        snapshot = json.loads(encoded)
        # Input/output isolation is a lab adaptation; the canonical topology is preserved.
        for processor in snapshot['flowContents']['processors']:
            processor['scheduledState'] = 'ENABLED'
            for name in ('Input Directory', 'Directory'):
                value = processor['properties'].get(name)
                if value:
                    relative = value.removeprefix('/opt/nifi/ariketak/').split('/', 1)[1]
                    processor['properties'][name] = f'/opt/nifi/ariketak/{key}/{relative}'
                    host = self.directory / 'data' / key / relative
                    host.mkdir(parents=True, exist_ok=True)
                    host.chmod(0o777)
        for port in snapshot['flowContents'].get('inputPorts', []) + snapshot['flowContents'].get('outputPorts', []):
            port['scheduledState'] = 'ENABLED'
        new = self.api(f'/process-groups/{pg}/process-groups/import', 'POST', {
            'revisionDTO': {'version': 0}, 'flowSnapshot': snapshot,
            'positionDTO': {'x': 100, 'y': 100}, 'groupName': key,
            'disconnectedNodeAcknowledged': False})['id']
        for entity in self.api(f'/flow/process-groups/{new}/controller-services').get('controllerServices', []):
            if entity['component']['parentGroupId'] == new:
                self.enable(entity['id'])
        return new

    def flow(self, pg):
        return self.api(f'/flow/process-groups/{pg}')['processGroupFlow']['flow']

    def state(self, pg, state):
        return self.api(f'/flow/process-groups/{pg}', 'PUT', {'id': pg, 'state': state})

    def processor(self, identifier, state):
        entity = self.api('/processors/' + identifier)
        return self.api('/processors/' + identifier + '/run-status', 'PUT', {
            'revision': entity['revision'], 'state': state, 'disconnectedNodeAcknowledged': False})

    def status(self, pg):
        return self.api(f'/flow/process-groups/{pg}/status?recursive=true')

    def prepare(self):
        root = self.api('/flow/process-groups/root')['processGroupFlow']['id']
        if any(p['component']['name'] == 'LAB 2026-10-02 cases 1-6'
               for p in self.flow(root)['processGroups']):
            raise RuntimeError('Lab cases group already exists; use status/stop rather than import twice')
        owner = self.create_group(root, 'LAB 2026-10-02 cases 1-6')
        services = {
            '6f352988-b5e5-3e19-882e-66fca64f6ea1': self.service(owner, 'Lab Mongo', 'org.apache.nifi.mongodb.MongoDBControllerService', 'nifi-mongodb-services-nar', {'mongo-uri': 'mongodb://mongo:27017'}),
            '74888e3f-4e6e-3a48-b543-c2162080cfa1': self.service(owner, 'Lab MySQL', 'org.apache.nifi.dbcp.DBCPConnectionPool', 'nifi-dbcp-service-nar', {
                'Database Connection URL': 'jdbc:mysql://mysql:3306/retail_db', 'Database Driver Class Name': 'com.mysql.cj.jdbc.Driver',
                'database-driver-locations': '/opt/mysql-connector-j-8.0.31.jar', 'Database User': 'iabd', 'Password': self.credentials['MYSQL_PASSWORD']}),
            '1e207816-ca56-38af-8d4f-4408c7fc579f': self.service(owner, 'Lab NDJSON writer', 'org.apache.nifi.json.JsonRecordSetWriter', 'nifi-record-serialization-services-nar', {'output-grouping': 'output-oneline'}),
            'f0cb7f47-a0e5-3e6e-8c48-c28b0792890c': self.service(owner, 'Lab JSON reader', 'org.apache.nifi.json.JsonTreeReader', 'nifi-record-serialization-services-nar', {'schema-access-strategy': 'infer-schema'})}
        groups = {}
        for file in sorted(BASE.glob('0[1-6]*/flow*.json')):
            key = file.stem
            groups[key] = self.import_flow(owner, file, services, key)
            print('Imported', key, groups[key], flush=True)
            (self.directory / 'cases-state.json').write_text(json.dumps(
                {'owner': owner, 'services': services, 'groups': groups}, indent=2))
        state = {'owner': owner, 'services': services, 'groups': groups}
        (self.directory / 'cases-state.json').write_text(json.dumps(state, indent=2))
        return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'status', 'stop'])
    parser.add_argument('--lab-dir', type=Path, default=LAB)
    args = parser.parse_args()
    lab = Lab(args.lab_dir)
    if args.action == 'prepare':
        lab.prepare()
    else:
        state = json.loads((args.lab_dir / 'cases-state.json').read_text())
        if args.action == 'stop':
            lab.state(state['owner'], 'STOPPED')
        print(json.dumps(lab.status(state['owner']), indent=2))


if __name__ == '__main__':
    main()
