import time

from datetime import datetime
from requests.exceptions import ConnectionError

from pprint import pprint

from KBParallel.baseclient import BaseClient


class TaskProvider(object):

    def __init__(self, tasks):
        self.tasks = tasks
        self.next_task_index = 0

    def claim_next_task(self):
        if self.next_task_index < len(self.tasks):
            next_task = self.tasks[self.next_task_index]
            self.next_task_index += 1
            return next_task
        else:
            return None


class Task(object):

    def __init__(self, module_name, function_name, version, parameters, token,
                 n_connection_retries=5, retry_wait_time=5):

        self.module_name = module_name
        self.function_name = function_name

        self.version = 'release'
        if version:
            self.version = version

        if isinstance(parameters, list) or isinstance(parameters, tuple):
            self.parameters = parameters
        else:
            self.parameters = [parameters]

        self.token = token

        self.execution_engine = None
        self._job_id = None

        self.last_state = None

        self._final_job_state = None
        self.run_location = None

        self.N_CONNECTION_RETRIES = n_connection_retries
        self.RETRY_WAIT_TIME = retry_wait_time


    def start(self, runner_url, run_location):
        ''' runner_url should be set to either:
                callback_server_url - runs locally
                njsw_url - submits to run on a cluster
        '''
        if self._job_id:
            if self._final_job_state:
                self._job_id = None
                self._final_job_state = None
                self.run_location = None
            else:
                raise ValueError('Cannot start task- already running and has not completed')
        self.execution_engine = BaseClient(runner_url, token=self.token)
        self._job_id = self.execution_engine._submit_job(self.module_name + '.' + self.function_name,
                                                         self.parameters,
                                                         service_ver=self.version)
        self.run_location = run_location
        print(str(datetime.now()) + ' - RUNNER SUBMITTING TASK: ' + str(self._job_id) + ' on ' + self.run_location)
        return self._job_id


    def is_done(self):
        ''' check if a job is done; returns True if it is, false otherwise '''
        self.check_job_state()
        if self._final_job_state:
            return True
        return False


    def success(self):
        ''' returns True if finished, no errors were reported, and result is defined.  False otherwise '''
        self.check_job_state()
        if self._final_job_state:
            if 'error' in self._final_job_state and self._final_job_state['errror']:
                return False
            if 'result' in self._final_job_state and self._final_job_state['result']:
                return True
        return False


    def get_task_result_package(self):
        ''' If the job is not finished, throws an exception.
            If the job is finished, returns a structure that looks like:
            {
                'is_error': True | False
                'result_package': {
                                    'function': { 'module_name': module_name, 'fun
                                    'error': None or error content from job state
                                    '
                'final_job_state: { ... }
            }
        '''
        if not self.is_done():
            raise ValueError('Cannot get result package - task is not done.')

        result_package = {'function': {'module_name': self.module_name,
                                       'function_name': self.function_name,
                                       'version': self.version},
                          'error': None,
                          'result': None,
                          'run_context': {'location': self.run_location,
                                          'job_id': self._job_id}
                          }
        if 'error' in self._final_job_state and self._final_job_state['error']:
            result_package['error'] = self._final_job_state['error']
        if 'result' in self._final_job_state and self._final_job_state['result']:
            result_package['result'] = self._final_job_state['result']

        result = {'result_package': result_package,
                  'is_error': not self.success(),
                  'final_job_state': self._final_job_state}
        return result


    def check_job_state(self):
        ''' If the job isn't complete yet, check the job state and return '''
        if not self._job_id:
            raise ValueError('Cannot check task status - task has not been started yet.')
        # if the task already completed, don't check and just return
        if self._final_job_state:
            return self._final_job_state

        # otherwise we need to call the execution engine
        for k in range(0, self.N_CONNECTION_RETRIES):
            try:
                job_state = self.execution_engine._check_job(self.module_name, self._job_id)
                break
            except ConnectionError as e:
                print('WARNING: ConnectionError calling _check_job(job_id=' + self._job_id + ') waiting ' +
                      self.RETRY_WAIT_TIME + ' and retrying')
                pprint(e)
            time.sleep(self.RETRY_WAIT_TIME)

        # job is finished, so remember that
        if job_state['finished'] == 1:
            self._final_job_state = job_state

        if 'job_state' in job_state:
            if self.last_state != job_state['job_state']:
                self.last_state = job_state['job_state']
                print(str(datetime.now()) + ' - RUNNER TASK: ' + str(self._job_id) + ' on ' + self.run_location +
                      ' now on job state: ' + self.last_state)

        return job_state


    def get_job_id(self):
        if not self._job_id:
            raise ValueError('Cannot get task job_id - task has not been started yet.')
        return self._job_id
