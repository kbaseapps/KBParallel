# -*- coding: utf-8 -*-
import os  # noqa: F401
import time
import unittest
from configparser import ConfigParser
from os import environ

from KBParallel.KBParallelImpl import KBParallel
from KBParallel.KBParallelServer import MethodContext
from KBParallel.authclient import KBaseAuth as _KBaseAuth
from installed_clients.WorkspaceClient import Workspace as workspaceService
from pprint import pprint

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

    # Build some task data fro .run_batch
    def build_task(self, number):
        return {
            'module_name': 'echo_test',
            'function_name': 'echo',
            'version': 'dev',
            'parameters': {
                'message': 'hola mundo ' + str(number),
                'workspace_name': self.getWsName()
            }
        }

    def test_local_task_results(self):
        """Test that local tasks, run via the callback server, return result packages correctly."""
        length = 2
        params = {
          'tasks': [self.build_task(idx) for idx in range(length)],
          'runner': 'parallel',
          'concurrent_njsw_tasks': 0,
          'concurrent_local_tasks': 2
        }
        results = self.getImpl().run_batch(self.getContext(), params)[0]
        self.assertIn('results', results)
        self.assertEqual(len(results['results']), length)
        for i in range(length):
            task_result = results['results'][i]['result_package']
            pprint(task_result)
            self.assertEqual(
                task_result['function'],
                {'method_name': 'echo', 'module_name': 'echo_test', 'version': 'dev'}
            )
            self.assertEqual(task_result['run_context']['location'], 'local')
            self.assertIsInstance(task_result['run_context']['job_id'], str)
            self.assertIsNotNone(task_result['result'])
            self.assertIsNotNone(task_result['result'][0])
            self.assertEqual(task_result['result'][0]['message'], 'hola mundo ' + str(i))

    def test_remote_task_results(self):
        """Test that remote tasks, run via NJS, return result packages correctly."""
        length = 2
        params = {
          'tasks': [self.build_task(idx) for idx in range(length)],
          'runner': 'parallel',
          'concurrent_njsw_tasks': 2,
          'concurrent_local_tasks': 0
        }
        results = self.getImpl().run_batch(self.getContext(), params)[0]
        self.assertIn('results', results)
        self.assertEqual(len(results['results']), length)
        for i in range(length):

            task_result = results['results'][i]['result_package']
            pprint(task_result)
            self.assertEqual(
                task_result['function'],
                {'method_name': 'echo', 'module_name': 'echo_test', 'version': 'dev'}
            )
            self.assertEqual(task_result['run_context']['location'], 'njsw')
            self.assertIsInstance(task_result['run_context']['job_id'], str)
            self.assertEqual(task_result['result'][0]['message'], 'hola mundo ' + str(i))

    def test_local_task_failures(self):
        """Test for failed job results run locally."""
        task = self.build_task(0)
        task['function_name'] = 'echo_fail'
        params = {
          'tasks': [task],
          'runner': 'parallel',
          'concurrent_njsw_tasks': 0,
          'concurrent_local_tasks': 1,
          'max_retries': 2
        }
        results = self.getImpl().run_batch(self.getContext(), params)[0]
        self.assertIn('results', results)
        task_result = results['results'][0]
        self.assertEqual(task_result['is_error'], True)
        self.assertEqual(task_result['result_package']['result'], None)
        self.assertIsInstance(task_result['result_package']['error'], str)

    def test_remote_task_failures(self):
        """Test for failed job results run on NJS."""
        task = self.build_task(0)
        task['function_name'] = 'echo_fail'
        params = {
          'tasks': [task],
          'runner': 'parallel',
          'concurrent_njsw_tasks': 1,
          'concurrent_local_tasks': 0,
          'max_retries': 1
        }
        results = self.getImpl().run_batch(self.getContext(), params)[0]
        self.assertIn('results', results)
        task_result = results['results'][0]
        self.assertEqual(task_result['is_error'], True)
        self.assertEqual(task_result['result_package']['result'], None)

    def test_set_parent_job_id(self):
        """
        Test that the parent_job_id of all spawned jobs matches the parent job ID of
        kbparallel.
        """
        task = self.build_task(0)
        params = {
          'tasks': [task],
          'runner': 'parallel',
          'concurrent_njsw_tasks': 0,
          'concurrent_local_tasks': 1,
          'parent_job_id': 'xyz',
          'max_retries': 1
        }
        results = self.getImpl().run_batch(self.getContext(), params)[0]['results']
        self.assertEqual(results[0]['result_package']['run_context']['parent_job_id'], 'xyz')
