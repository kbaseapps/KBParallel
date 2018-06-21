# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from KBParallel.KBParallelImpl import KBParallel
from KBParallel.KBParallelServer import MethodContext
from KBParallel.authclient import KBaseAuth as _KBaseAuth

from KBParallel.Task import Task
from KBParallel.Runners import ParallelRunner, ParallelLocalRunner, SerialLocalRunner


class KBParallelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('KBParallel'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(cls.token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({
            'token': cls.token,
            'user_id': user_id,
            'provenance': [{
                'service': 'KBParallel',
                'method': 'please_never_use_it_in_production',
                'method_params': []
            }],
            'authenticated': 1
        })
        cls.execution_engine_url = cls.cfg['njs-wrapper-url']
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = KBParallel(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.base_dir = os.path.dirname(__file__)

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
        params = {'message': 'xyzabcxyz', 'workspace_name': self.getWsName()}
        t = Task('echo_test', 'echo', 'dev', params, self.token)
        t.start(self.callback_url, 'local')
        while not t.is_done():
            time.sleep(0.2)
        self.assertTrue(t.success())
        result_package = t.get_task_result_package()
        result_msg = result_package['result_package']['result'][0]['message']
        self.assertEqual(result_msg, 'xyzabcxyz')

    def test_local_task_failure(self):
        params = {
            # Missing required parameter: 'workspace_name'
            'message': 'x'
        }
        t = Task('echo_test', 'echo', 'dev', params, self.token)
        t.start(self.callback_url, 'local')
        while not t.is_done():
            time.sleep(0.2)
        result_package = t.get_task_result_package()
        print('abcd', result_package)
        self.assertFalse(t.success())
        self.assertEqual(result_package['result_package']['result'], None)
        self.assertTrue('Server error' in result_package['result_package']['error'])

    def test_njsw_task_failure(self):
        t = Task('echo_test', 'echo', 'dev', {'throw_error': 1}, self.token)
        t.start(self.execution_engine_url, 'njsw')
        while not t.is_done():
            time.sleep(0.2)
        self.assertFalse(t.success())
        result_package = t.get_task_result_package()
        self.assertEqual(result_package['result_package']['result'], None)
        self.assertTrue('Server error' in result_package['result_package']['error'])

    def test_serial_local_runner(self):
        tasks = []
        for i in range(3):
            params = {'message': str(i), 'workspace_name': self.getWsName()}
            tasks.append(Task('echo_test', 'echo', 'dev', params, self.token))
        slr = SerialLocalRunner(tasks, 1, self.callback_url)
        results = slr.run()
        for i in range(3):
            self.assertEqual(results[i]['result_package']['result'][0]['message'], str(i))

    def test_parallel_local_runner(self):
        tasks = []
        for i in range(5):
            params = {'message': str(i), 'workspace_name': self.getWsName()}
            tasks.append(Task('echo_test', 'echo', 'dev', params, self.token))
        plr = ParallelLocalRunner(tasks, 2, 1, 15, self.callback_url)
        results = plr.run()
        for i in range(5):
            self.assertEqual(results[i]['result_package']['result'][0]['message'], str(i))

    def test_parallel_runner(self):
        tasks = []
        for i in range(4):
            params = {'message': str(i), 'workspace_name': self.getWsName()}
            tasks.append(Task('echo_test', 'echo', 'dev', params, self.token))
        # Note: this test submits to the test endpoint NJS wrapper, so really runs things remotely
        n_local_tasks = 1
        n_njsw_tasks = 2
        plr = ParallelRunner(tasks, 2, n_local_tasks, n_njsw_tasks, 15, self.callback_url,
                             self.execution_engine_url)
        results = plr.run()
        for i in range(4):
            self.assertEqual(results[i]['result_package']['result'][0]['message'], str(i))

    def test_batch_runner_interface(self):
        def build_task(number):
            return {
                'module_name': 'echo_test',
                'function_name': 'echo',
                'version': 'dev',
                'parameters': {
                    'message': 'hola mundo ' + str(number),
                    'workspace_name': self.getWsName()
                }
            }

        params = {
          'tasks': [build_task(0), build_task(1), build_task(2), build_task(3)],
          'runner': 'parallel',
          'concurrent_njsw_tasks': 4,
          'concurrent_local_tasks': 0,
          'max_retries': 2
        }
        results = self.getImpl().run_batch(self.getContext(), params)[0]
        print('results', results['results'])
        self.assertIn('results', results)
        self.assertEqual(len(results['results']), 4)
        for i in range(4):
            self.assertEqual(
                results['results'][i]['result_package']['result'][0]['message'],
                'hola mundo ' + str(i)
            )
