
import sys
import requests
import json
import uuid

hostname = '172.20.20.2'
auth=('root', 'asdf;lkj:LKJ')

class Freenas(object):
    def __init__(self, hostname, auth):
        self._hostname = hostname
        self._user = auth[0]
        self._secret = auth[1]
        self._ep = 'http://{}/api/v2.0/'.format(self._hostname)
        self._uuid = str(uuid.uuid4())

    def request(self, resource, method='GET', data=None):
        """
            Takes arguments for requests
       :type data: object
       """
        print(resource, method, data)
        if data is None:
            data = {}

        r = requests.request(method, '{}{}'.format(self._ep, resource), data=json.dumps(data), headers={'Content-Type': "application/json"}, auth=(self._user, self._secret))

        if r.ok:
            try:
                return r.json()
            except:
                return r.text
        raise ValueError(r)

    def create_zvol(self):
        """Takes a volume size in GBs and returns a uuid"""
        self.request('pool/dataset', method='POST', data={'type': 'VOLUME', 'name': 'Vol1/name-'+self._uuid, 'volsize': 10485760000})
        print('Creating zvol {}'.format(self._uuid))
        return self._uuid

    def create_target(self):
        tgt = self.request('iscsi/target', method='POST', data={'name': 'tgt-'+self._uuid, 'groups': [{'portal': 1, 'initiator': 1}]})
        return tgt['id']

    def create_extent(self):
        ext = self.request('iscsi/extent', method='POST', data={'name': 'ext-'+self._uuid, 'type': 'DISK', 'disk': 'zvol/Vol1/name-'+self._uuid, 'enabled': True})
        return ext['id']

    def assoc_target(self, tgt_id, ext_id):
        self.request('iscsi/targetextent', method='POST', data={'extent': ext_id, 'target': tgt_id})

    def get_assoc_target(self):
        return self.request('iscsi/targetextent')

    def get_users(self):
        return self.request('user')

#z=Freenas(hostname, auth)
#b = z.get_users()
#for i in b:
#   if i['username'] == 'api':
#        print(i['id'])
