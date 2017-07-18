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
from KBParallel.Runners import ParallelRunner, ParallelLocalRunner, SerialLocalRunner


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

        cls.execution_engine_url = cls.cfg['njs-wrapper-url']
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

        self.assertTrue(t.success())
        result_package = t.get_task_result_package()
        self.assertEqual(result_package['result_package']['result'][0]['new_number'], 500)


    def test_local_task_failure(self):
        t = Task('KBParallelTestModule', 'do_something', 'dev', {'throw_error': 1}, self.token)
        t.start(self.callback_url, 'local')

        while not t.is_done():
            time.sleep(0.2)
        self.assertFalse(t.success())
        result_package = t.get_task_result_package()
        self.assertEqual(result_package['result_package']['result'], None)
        self.assertTrue('doing as you wish' in result_package['result_package']['error'])


    def test_njsw_task_failure(self):
        t = Task('KBParallelTestModule', 'do_something', 'dev', {'throw_error': 1}, self.token)
        t.start(self.execution_engine_url, 'njsw')

        while not t.is_done():
            time.sleep(0.2)

        self.assertFalse(t.success())
        result_package = t.get_task_result_package()
        self.assertEqual(result_package['result_package']['result'], None)
        self.assertTrue('doing as you wish' in result_package['result_package']['error'])


    def test_serial_local_runner(self):
        tasks = []
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 1}, self.token))
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 2}, self.token))
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 3}, self.token))

        slr = SerialLocalRunner(tasks, 1, self.callback_url)
        results = slr.run()

        self.assertEqual(results[0]['result_package']['result'][0]['new_number'], 100)
        self.assertEqual(results[1]['result_package']['result'][0]['new_number'], 200)
        self.assertEqual(results[2]['result_package']['result'][0]['new_number'], 300)


    def test_parallel_local_runner(self):
        tasks = []
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 1}, self.token))
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 2}, self.token))
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 3}, self.token))
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 4}, self.token))
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 5}, self.token))

        plr = ParallelLocalRunner(tasks, 2, 1, 15, self.callback_url)
        results = plr.run()

        self.assertEqual(results[0]['result_package']['result'][0]['new_number'], 100)
        self.assertEqual(results[1]['result_package']['result'][0]['new_number'], 200)
        self.assertEqual(results[2]['result_package']['result'][0]['new_number'], 300)
        self.assertEqual(results[3]['result_package']['result'][0]['new_number'], 400)
        self.assertEqual(results[4]['result_package']['result'][0]['new_number'], 500)


    def test_parallel_runner(self):
        tasks = []
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 1}, self.token))
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 2}, self.token))
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 3}, self.token))
        tasks.append(Task('KBParallelTestModule', 'do_something', 'dev', {'number': 4}, self.token))

        # Note: this test submits to the test endpoint NJS wrapper, so really runs things remotely
        n_local_tasks = 1
        n_njsw_tasks = 2
        plr = ParallelRunner(tasks, 2, n_local_tasks, n_njsw_tasks, 15, self.callback_url, self.execution_engine_url)
        results = plr.run()

        self.assertEqual(results[0]['result_package']['result'][0]['new_number'], 100)
        self.assertEqual(results[1]['result_package']['result'][0]['new_number'], 200)
        self.assertEqual(results[2]['result_package']['result'][0]['new_number'], 300)
        self.assertEqual(results[3]['result_package']['result'][0]['new_number'], 400)


    def test_batch_runner_interface(self):
        def build_task_spec(number):
            return {'module_name': 'KBParallelTestModule',
                    'function_name': 'do_something',
                    'version': 'dev',
                    'parameters': {'number': number}}


        params = {'tasks': [build_task_spec(1),
                            build_task_spec(2),
                            build_task_spec(3)
                            ],
                  'runner': 'local_parallel'
                  }

        results = self.getImpl().run_batch(self.getContext(), params)[0]
        self.assertIn('results', results)
        self.assertEqual(len(results['results']), 3)
        self.assertEqual(results['results'][0]['result_package']['result'][0]['new_number'], 100)
        self.assertEqual(results['results'][1]['result_package']['result'][0]['new_number'], 200)
        self.assertEqual(results['results'][2]['result_package']['result'][0]['new_number'], 300)
