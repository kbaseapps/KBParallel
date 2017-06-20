
from KBParallel.Task import Task
from KBParallel.Runners import ParallelRunner, ParallelLocalRunner, SerialLocalRunner


class BatchRunner(object):

    def __init__(self, callback_url, cfg, token):
        self.callback_url = callback_url
        self.cfg = cfg
        self.token = token


    def run(self, parameters):

        validated_params = self.validate_params(parameters)
        tasks = self.build_tasks(validated_params['tasks'])

        max_retries = 1

        if validated_params['runner'] == 'local_serial':
            slr = SerialLocalRunner(tasks, max_retries, self.callback_url)
            return slr.run()

        if validated_params['runner'] == 'local_parallel':
            # tasks, max_retries, n_concurrent_tasks, total_checks_per_min, callback_url
            total_checks_per_min = 30
            plr = ParallelLocalRunner(tasks, max_retries, validated_params['concurrent_local_tasks'],
                                      total_checks_per_min, self.callback_url)
            return plr.run()

        if validated_params['runner'] == 'parallel':
            # tasks, max_retries, n_concurrent_tasks, total_checks_per_min, callback_url
            total_checks_per_min = 30
            plr = ParallelLocalRunner(tasks, max_retries, validated_params['concurrent_local_tasks'],
                                      validated_params['concurrent_local_tasks'], total_checks_per_min,
                                      total_checks_per_min, self.callback_url)
            return plr.run()

        # this path should not be reachable
        raise ValueError('Unknown runner type, or other strange internal error')



    def build_tasks(self, task_specs):
        tasks = []
        for t in task_specs:
            # @TODO - better error checking
            version = 'release'
            if 'version' in t:
                version = t['version']
            tasks.append(Task(t['module_name'], t['function_name'], version,
                              t['parameters'], self.token))
        return tasks


    def validate_params(self, parameters):
        validated_params = {}

        if 'tasks' not in parameters:
            raise ValueError('"tasks" field giving a list of tasks is required, but was missing')
        if not parameters['tasks']:
            raise ValueError('Nothing to run- tasks list was empty or not set')
        validated_params['tasks'] = parameters['tasks']

        if 'runner' not in parameters:
            raise ValueError('"runner" field giving a list of tasks is required, but was missing')
        if parameters['runner'] not in ['local_serial', 'local_parallel', 'parallel']:
            raise ValueError('Unknown or unsupported runner type = ' + str(parameters['runner']))
        validated_params['runner'] = parameters['runner']

        # get number of concurrent local tasks- keep in a range between 1 and 20 for now
        validated_params['concurrent_local_tasks'] = 2
        if 'concurrent_local_tasks' in parameters:
            clt = int(parameters['concurrent_local_tasks'])
            if clt < 1:
                clt = 1
            if clt > 20:
                clt = 20
            validated_params['concurrent_local_tasks'] = clt

        validated_params['concurrent_njsw_tasks'] = 0
        if 'concurrent_njsw_tasks' in parameters:
            cnjswt = int(parameters['concurrent_njsw_tasks'])
            if cnjswt < 1:
                cnjswt = 1
            if cnjswt > 50:
                cnjswt = 50
            validated_params['concurrent_njsw_tasks'] = cnjswt

        return validated_params
