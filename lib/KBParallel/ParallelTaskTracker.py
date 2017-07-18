import time

from pprint import pprint
from requests.exceptions import ConnectionError
from NarrativeJobService.NarrativeJobServiceClient import NarrativeJobService


class ParallelTaskTracker(object):
    ''' give a task provider to give tasks and a number of concurrent tasks, this
        will provide an interface for starting and tracking those tasks. This does
        not automatically schedule checks- instead you need to make calls to
        check_all to update the status of jobs that are running '''

    def __init__(self, task_provider, concurrent_tasks, retries, execution_engine_url, execution_location,
                 n_connection_retries=5, retry_wait_time=20):

        self.task_provider = task_provider
        self.concurrent_tasks = concurrent_tasks
        self.retries = retries

        self.execution_engine_url = execution_engine_url
        self.execution_location = execution_location
        self.njsw = None
        if self.execution_location == 'njsw':
            self.njsw = NarrativeJobService(self.execution_engine_url)

        self.active_tasks = []

        self.N_CONNECTION_RETRIES = n_connection_retries
        self.RETRY_WAIT_TIME = retry_wait_time

    def start(self):
        self._top_off_task_list()

    def n_running_tasks(self):
        return len(self.active_tasks)

    def check_all_individually(self, time_delay=0):
        '''
        Check the state of running tasks and add more if some are complete. This
        function checks tasks individually, which you must do for local tasks. If
        you are tracking a set of jobs running on NJSW, you should use the
        check_all_batch function instead.

        checks status of all running tasks.  If something is complete and ran
        successfully, then another task will be requested and started. If a task
        completed in an error, the code will attempt to retry up to the number
        of retries. If it is still an error, it will be pulled off the list and
        another job will be fetched.  time_delay provides a way to limit the rate
        of checks by introducing an artificial delay between each status call
        to the job engine (provide a length of time in seconds).
        '''

        # note- these loops can maybe can be optimized but probably not worth it if
        # the number of concurrent tasks are less than say 100, which seems likely for a while.

        # first if we have space, try to add some more tasks
        self._top_off_task_list()

        completed_tasks = []
        has_empty_slots = False

        for t in self.active_tasks:
            time.sleep(time_delay)
            task = t['task']
            if task.is_done():
                # if it was finished successfully or we've exceeded the number of
                # retries, then take it off the list and try to get another task
                if task.success() or t['try'] < self.retries:
                    completed_tasks.append(task.get_task_result_package())
                    next_task = self.task_provider.claim_next_task()
                    if next_task:
                        next_task.start(self.execution_engine_url, self.execution_location)
                        t['task'] = next_task
                        t['try'] = 1
                    else:
                        has_empty_slots = True
                        t['task'] = None
                        t['try'] = 1
                # otherwise we have failed, but can try again
                else:
                    t['try'] += 1
                    t['task'].start(self.execution_engine_url, self.execution_location)

        # TODO: swap empty tasks to the end of the list, then chop them off
        # for now an easier implementation is just to copy to a new list
        if has_empty_slots:
            current_active_tasks = []
            for t in self.active_tasks:
                if t['task']:
                    current_active_tasks.append(t)
            self.active_tasks = current_active_tasks

        return completed_tasks

    def check_all_batch(self, time_delay=0):
        if not self.njsw:
            raise ValueError('Cannot check_all_batch for this tracker: Tracker is not attached to NJSW')

        # first if we have space, try to add some more tasks
        self._top_off_task_list()

        has_empty_slots = False

        # get batch list of jobs to check
        job_id_list = []
        for t in self.active_tasks:
            job_id_list.append(t['task'].get_job_id())

        # check em
        time.sleep(time_delay)
        for k in range(0, self.N_CONNECTION_RETRIES):
            try:
                jobs_status = self.njsw.check_jobs({'job_ids': job_id_list, 'with_job_params': 0})
                break
            except ConnectionError as e:
                print('WARNING: ConnectionError calling njsw.check_jobs(...) waiting ' +
                      str(self.RETRY_WAIT_TIME) + ' and retrying')
                print('Error was: ' + str(e))
            time.sleep(self.RETRY_WAIT_TIME)

        job_states = jobs_status['job_states']
        check_errors = jobs_status['check_error']  # errors in checking a job state will be reported here

        # update the job states for the tasks, and move them to completed if done
        completed_tasks = []
        for t in self.active_tasks:
            task = t['task']
            job_id = t['task'].get_job_id()
            if job_id in job_states:
                task.set_job_state(job_states[job_id])
            elif job_id in check_errors:
                print('WARNING: Task ' + str(job_id) + ' state could not be retrieved. There was an error' +
                      'reported:')
                pprint(check_errors[job_id])
                continue
            else:
                raise ValueError('ERROR: Task ' + str(job_id) + ' state could not be retrieved.' +
                                 ' There was no error reported- it just went missing! This is' +
                                 ' probably an internal NJSW or UJS error.')

            if task.is_done(recheck=False):
                # if it was finished successfully or we've exceeded the number of
                # retries, then take it off the list and try to get another task
                if task.success() or t['try'] < self.retries:
                    completed_tasks.append(task.get_task_result_package())
                    next_task = self.task_provider.claim_next_task()
                    if next_task:
                        next_task.start(self.execution_engine_url, self.execution_location)
                        t['task'] = next_task
                        t['try'] = 1
                    else:
                        has_empty_slots = True
                        t['task'] = None
                        t['try'] = 1
                # otherwise we have failed, but can try again
                else:
                    t['try'] += 1
                    t['task'].start(self.execution_engine_url, self.execution_location)

        # TODO: swap empty tasks to the end of the list, then chop them off
        # for now an easier implementation is just to copy to a new list
        if has_empty_slots:
            current_active_tasks = []
            for t in self.active_tasks:
                if t['task']:
                    current_active_tasks.append(t)
            self.active_tasks = current_active_tasks

        return completed_tasks

    def _top_off_task_list(self):
        # keep taking tasks until we're full
        while len(self.active_tasks) < self.concurrent_tasks:
            next_task = self.task_provider.claim_next_task()
            if not next_task:
                break
            self.active_tasks.append({'task': next_task, 'try': 1})
            next_task.start(self.execution_engine_url, self.execution_location)
