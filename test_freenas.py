import unittest
import freenas
import os

auth = freenas.auth_conf()
f = freenas.Freenas('172.20.20.2', auth)


class TestFreenas(unittest.TestCase):
    def test_auth_success(self):
        '''Test for auth success'''
        self.assertEqual(f.request('auth/check_user',
                                   method='POST', data={'username': 'root',
                                                        'password': auth[1]
                                                        }
                                   ), True)

    def test_create_vvol(self):
        '''Test if zvol is created'''
        self.assertEqual(f.create_zvol(10), f._uuid)