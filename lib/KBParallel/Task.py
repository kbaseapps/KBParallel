from KBParallel.baseclient import BaseClient


class Task(object):

    def __init__(self, module_name, function_name, version, parameters, token):

        self.module_name = module_name
        self.function_name = function_name

        self.version = 'release'
        if version:
            self.version = version

        self.parameters = parameters

        self.token = token

        self.execution_engine = None
        self._job_id = None

        self._final_job_state = None
        self.run_location = None


    def start(self, runner_url, run_location):
        ''' runner_url should be set to either:
                callback_server_url - runs locally
                njsw_url - submits to run on a cluster
        '''
        self.execution_engine = BaseClient(runner_url, token=self._token)
        self._job_id = self._execution_engine._submit_job(self.function_specification_string,
                                                          self.parameters,
                                                          service_ver=self.version)
        self.run_location = run_location
        return self._job_id


    def is_done(self):
        ''' check if a job is done; returns True if it is, false otherwise '''
        self.check_job_state()
        if self._final_job_state:
            return True
        return False


    def finished_successfully(self):
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
            result_package['error'] = self.final_job_state['error']
        if 'result' in self._final_job_state and self._final_job_state['result']:
            result_package['result'] = self.final_job_state['result']

        result = {'result_package': result_package,
                  'is_error': not self.finished_successfully(),
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
        job_state = self._execution_engine._check_job(self.module_name, self._job_id)

        # job is finished, so remember that
        if job_state['finished'] == 1:
            self._final_job_state = job_state

        return job_state


    def get_job_id(self):
        if not self._job_id:
            raise ValueError('Cannot get task job_id - task has not been started yet.')
        return self._job_id
