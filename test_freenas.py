import unittest
import freenas
import os

hostname = '172.20.20.2'

class TestFreenas(unittest.TestCase):
    def test_auth_success(self):
        '''Test for auth success'''
        self.assertEqual(freenas.Freenas(hostname), True)

        #self.assertEqual(freenas.Freenas(hostname).request('auth/check_user',
        #                           method='POST', data={'username': 'api',
        #                                                'password': 'api'
        #                                                }
        #                           ), True)

    #def test_create_vvol(self):
    #    '''Test if zvol is created'''
    #    self.assertEqual(f.create_zvol(10), f._uuid)