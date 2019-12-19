import time

from KBParallel.utils.task import Task
from KBParallel.utils.log import log
from pprint import pprint

class TaskManager:
    """
    This manages a batch run of many tasks, keeping a limited queue of jobs, tracking job
    responses and failures.

    When task_manager.execute_all() completes, then task_manager.results will be filled.

    task_manager.results is an array with an entry for each completed task.
    Each entry has the format:
    {
      'result_package': {
        'function': {'module_name': str, 'method_name': str, 'version': str},
        'error': str,
        'result': str,
        'run_context': {'location': str, 'job_id': str}
      },
      'is_error': int (1 or 0),
      'final_job_state': { <raw data from checking njs or local job> }
    }
    The above format may not seem ideal or logical, but it is preserved for backwards compatibilty
    purposes.
    """

    def __init__(self, **kwargs):
        """
        Create a new JobManager -- this is called by KBParallelImpl.run_batch
        Keyword arguments:
          params - parameters passed to KBParallel.run_batch (see KBParallel.spec)
        """
        self.callback_url = kwargs['callback_url']
        self.ee2_url = kwargs['config']['ee2-url']
        self.params = kwargs['params']
        self.parent_job_id = self.params.get('parent_job_id')
        self.workspace_id = self.params.get('workspace_id')
        self.context = kwargs['context']
        self.total_tasks = len(kwargs['params']['tasks'])
        self.max_retries = int(kwargs['params']['max_retries'])
        # Lists of Task objects (see ./task.py)
        # We keep an original list of tasks that we don't mutate so we can construct any final
        # results in the same order as the task data given by the user.
        self.tasks = [Task(task, self) for task in kwargs['params']['tasks']]
        self.pending_tasks = list(self.tasks)  # Tasks that still need to be run
        self.running_tasks = []
        self.completed_tasks = []
        # Total currently running local and remote jobs
        self.local_running_jobs = 0
        self.remote_running_jobs = 0
        # Final results when all tasks are completed
        self.results = []

    def execute_all(self):
        """
        Run all tasks to completion. Blocks until all tasks have either succeeded or failed the
        maximum amount.
        """
        max_local = self.params['concurrent_local_tasks']
        max_remote = self.params['concurrent_njsw_tasks']
        interval = generate_sleep_interval()
        # While not all tasks have completed:
        while len(self.completed_tasks) < self.total_tasks:
            # Check the status of every running task
            for (idx, task) in enumerate(self.running_tasks):
                task.current_job.check_status()
                finished_running = task.completed or task.current_job.error
                if finished_running:
                    if task.current_job.location == 'local':
                        self.local_running_jobs -= 1
                    else:
                        self.remote_running_jobs -= 1
                if task.completed:
                    # Task either succeeded or failed the maximum times. Move it into the
                    # completed_tasks list.
                    log('task completed:', task.full_name)
                    self.running_tasks.pop(idx)
                    self.completed_tasks.append(task)
                elif task.current_job.error:
                    # Task failed, but can be retried.
                    log('task failed, trying again:', task.full_name)
                    self.running_tasks.pop(idx)
                    self.pending_tasks.append(task)
                else:
                    log('task still running:', task.full_name)
            # Queue up all pending tasks
            while len(self.pending_tasks) and self.local_running_jobs < max_local:
                task = self.pending_tasks.pop()
                log('starting local task', task.full_name)
                task.start_job('local')
                self.running_tasks.append(task)
                self.local_running_jobs += 1
            while len(self.pending_tasks) and self.remote_running_jobs < max_remote:
                task = self.pending_tasks.pop()
                log('starting remote task', task.full_name)
                task.start_job('njsw')
                self.running_tasks.append(task)
                self.remote_running_jobs += 1
            time.sleep(next(interval))
        log('all tasks completed')
        # All tasks have completed
        for task in self.tasks:
            self.append_to_results(task)

    def append_to_results(self, task):
        """Append data from a completed task to our results dictionary."""
        job_results = task.results
        result = {
          'result_package': {
            'function': {
                'module_name': task.module_name,
                'method_name': task.method_name,
                'version': task.service_ver
            },
            'error': str(job_results.get('error')),
            'result': job_results.get('job_output'),
            'run_context': {
                'location': task.current_job.location,
                'job_id': task.current_job.job_id,
                'parent_job_id': self.parent_job_id
            }
          },
          'is_error': 'error' in job_results,
          'final_job_state': job_results
        }
        print("Source task is")
        pprint(task)
        pprint(task.results )
        print("About to add this result")
        pprint(result)

        self.results.append(result)


# Utilities

def generate_sleep_interval():
    """Generate a sleep interval for checking job statuses based on a total time."""
    total_time = 0
    interval = 1
    # Initially wait 1s between polling
    while total_time < 20:
        total_time += interval
        yield interval
    # After 20s, wait 5s
    interval = 5
    while total_time < 300:
        total_time += interval
        yield interval
    # After 3 mins, wait 15s
    interval = 15
    while True:
        yield interval
