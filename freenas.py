
import os
import requests
import json
import uuid
import getpass

hostname = '172.20.20.2'


class Freenas(object):
    def __init__(self, hostname):
        self._auth = self.auth_conf()
        self._hostname = hostname
        self._user = self._auth[0]
        self._secret = self._auth[1]
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

        r = requests.request(method, '{}{}'.format(self._ep, resource),
                             data=json.dumps(data), headers={'Content-Type': "application/json"},
                             auth=(self._user, self._secret))

        if r.ok == True:
            return r.json()

        if r.status_code == 401:
            return r.status_code #Change to func retry

        raise ValueError(r)

        #return r
        #if r.status_code == 401:
        #   return r.status_code


        #if r.ok:
        #    try:
        #        return r.json()
        #    except:
        #        if r.reason == 'Unauthorized':
        #            print('oh snap, check passwd')
        #        return r.text
        #raise ValueError(r)



    @classmethod
    def auth_conf(self):
        """Checks for env var, presents prompt for password if None, returns tuple with 2 objects"""
        if not os.environ.get('FREENAS_API_PW'):
            os.environ['FREENAS_API_PW'] = str(getpass.getpass('Key not set.  Please enter root password: '))
        return 'root', os.environ.get('FREENAS_API_PW')


    def create_zvol(self, size):
        """Takes an integer to set volume size in GBs, returns a uuid string"""
        print('creating zvol')
        self.request('pool/dataset',
                     method='POST', data={'type': 'VOLUME',
                                          'name': 'Vol1/name-'+self._uuid, 'volsize': size*1073741824})
        print('Creating zvol {}'.format(self._uuid))
        return self._uuid

    def create_target(self):
        """Takes no argument, returns an integer of the target id"""
        tgt = self.request('iscsi/target',
                           method='POST', data={'name': self._uuid,
                                                'groups': [{'portal': 1, 'initiator': 1}]})
        return tgt['id']

    def create_extent(self):
        """Takes no argument, returns an integer of the extent id"""
        ext = self.request('iscsi/extent',
                           method='POST', data={'name': self._uuid, 'type': 'DISK',
                                                'disk': 'zvol/Vol1/'+self._uuid, 'enabled': True})
        return ext['id']

    def assoc_target(self, tgt_id, ext_id):
        """Takes two integer arguments and returns nothing"""
        self.request('iscsi/targetextent',
                     method='POST', data={'extent': ext_id, 'target': tgt_id})

    def get_assoc_target(self):
        return self.request('iscsi/targetextent')

    def get_users(self):
        return self.request('user')


