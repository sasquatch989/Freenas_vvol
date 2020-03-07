import unittest
from freenas import Freenas

a = Freenas('172.20.20.2', 'root', 'asdf;lkj:LKJ')
class TestFreenas(unittest.TestCase):
    def test_get_iscsi_assoc_targets(self):
        '''Test for auth success'''
        self.assertEqual(a.request('iscsi/targetextent'), 'ok')
