import unittest
import freenas
import os

auth = freenas.auth_conf()
a = freenas.Freenas('172.20.20.2', auth)

class TestFreenas(unittest.TestCase):
    def test_auth_success(self):
        '''Test for auth success'''
        self.assertEqual(a.request('auth/check_user',
                                   method='POST', data={'username': 'root',
                                                        'password': auth[1]
                                                        }
                                   ), True)
