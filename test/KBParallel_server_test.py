# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from KBParallel.KBParallelImpl import KBParallel
from KBParallel.KBParallelServer import MethodContext

from KBParallel.Task import Task
from KBParallel.SerialLocalRunner import SerialLocalRunner


class KBParallelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = environ.get('KB_AUTH_TOKEN', None)

        user_id = requests.post(
            'https://kbase.us/services/authorization/Sessions/Login',
            data='token={}&fields=user_id'.format(cls.token)).json()['user_id']
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': cls.token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'KBParallel',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('KBParallel'):
            cls.cfg[nameval[0]] = nameval[1]

        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=cls.token)
        cls.serviceImpl = KBParallel(cls.cfg)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_KBParallel_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx



    def test_task(self):
        t = Task('KBParallelTestModule', 'do_something', 'dev', {'number': 5}, self.token)
        t.start(self.callback_url, 'local')

        while not t.is_done():
            time.sleep(0.2)

        self.assertTrue(t.success(), True)
        result_package = t.get_task_result_package()
        pprint(result_package)
        self.assertEqual(result_package['result_package']['result'][0]['new_number'], 500)


    def test_serial_runner(self):

        tasks = []
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 1}, self.token))
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 2}, self.token))
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 3}, self.token))
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 4}, self.token))

        slr = SerialLocalRunner(tasks, 1, self.callback_url)
        results = slr.run()



    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    #def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        #pass

    def test_KBParallel(self):
        return
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #ret = self.getImpl().manyHellos( self.getContext(), input_params )
        print( "in test_KBParallel()")
        input_params = { 'method': {'module_name': 'ManyHellos',
                                    'method_name': 'manyHellos',
                                    'service_ver': 'dev'},
                         'is_local': 1,
                         'global_params': {'num_jobs' : 3, 
                                           'msg': "Hello_",
                                           'workspace': self.getWsName()}
                       }
        res= self.getImpl().run( self.getContext(), input_params )
        #res= self.getImpl().run_narrative( self.getContext(), in_params )
        pprint( res )

        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods

