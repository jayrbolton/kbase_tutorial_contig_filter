# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from jayrboltonTest.jayrboltonTestImpl import jayrboltonTest
from jayrboltonTest.jayrboltonTestServer import MethodContext
from jayrboltonTest.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace

_ASSEMBLY_REF = "33009/6/1"


class jayrboltonTestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('jayrboltonTest'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'jayrboltonTest',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = jayrboltonTest(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_jayrbolton_contig_filter(self):
        """
        Test the contig filter method with a sample assembly.
        """
        ret = self.serviceImpl.jayrbolton_contig_filter(self.ctx, {
            'workspace_name': self.wsName,
            'assembly_input_ref': _ASSEMBLY_REF,
            'min_length': 500000
        })
        print('ret is', ret)
