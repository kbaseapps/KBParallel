import time
import sys
from datetime import datetime

from KBParallel.Task import TaskProvider
from KBParallel.ParallelTaskTracker import ParallelTaskTracker


class ParallelRunner(object):

    def __init__(self, tasks, max_retries, n_local_concurrent_tasks, n_remote_concurrent_tasks,
                 total_checks_per_min, callback_url, execution_engine_url):
        self.tasks = tasks
        self.max_retries = max_retries
        self.callback_url = callback_url
        self.execution_engine_url = execution_engine_url
        self.n_local_concurrent_tasks = n_local_concurrent_tasks
        self.n_remote_concurrent_tasks = n_remote_concurrent_tasks
        self.update_time_delay = total_checks_per_min / 60

    def run(self):
        task_provider = TaskProvider(self.tasks)
        local_task_tracker = ParallelTaskTracker(task_provider, self.n_local_concurrent_tasks, self.max_retries,
                                                 self.callback_url, 'local')

        remote_task_tracker = ParallelTaskTracker(task_provider, self.n_remote_concurrent_tasks, self.max_retries,
                                                  self.execution_engine_url, 'njsw')

        local_task_tracker.start()
        remote_task_tracker.start()
        n_local_completed = 0
        n_remote_completed = 0
        while local_task_tracker.n_running_tasks() > 0 or remote_task_tracker.n_running_tasks() > 0:
            completed_local = local_task_tracker.check_all(self.update_time_delay)
            completed_remote = remote_task_tracker.check_all(self.update_time_delay)

            if len(completed_local) > 0 or len(completed_remote) > 0:
                n_local_completed += len(completed_local)
                n_remote_completed += len(completed_remote)
                print(str(datetime.now()) + ' - RUNNER STATUS UPDATE: completed ' +
                      str(n_local_completed + n_remote_completed) + ' of ' + str(len(self.tasks)) + ' tasks')
            sys.stdout.flush()

        print(str(datetime.now()) + ' - RUNNER STATUS UPDATE: completed ' +
              str(n_local_completed + n_remote_completed) + ' of ' + str(len(self.tasks)) + ' tasks')
        result_packages = []
        for t in self.tasks:
            result_packages.append(t.get_task_result_package())

        return result_packages


class ParallelLocalRunner(object):

    def __init__(self, tasks, max_retries, n_concurrent_tasks, total_checks_per_min, callback_url):
        self.tasks = tasks
        self.max_retries = max_retries
        self.callback_url = callback_url
        self.n_concurrent_tasks = n_concurrent_tasks
        self.update_time_delay = total_checks_per_min / 60

    def run(self):
        task_provider = TaskProvider(self.tasks)
        task_tracker = ParallelTaskTracker(task_provider, self.n_concurrent_tasks, self.max_retries,
                                           self.callback_url, 'local')

        task_tracker.start()
        while task_tracker.n_running_tasks() > 0:
            task_tracker.check_all(self.update_time_delay)

        result_packages = []
        for t in self.tasks:
            result_packages.append(t.get_task_result_package())

        return result_packages




def next_time_interval():
    ''' simple iterator to provide times for lookups for the SerialLocalRunner '''
    total_time = 0
    current_interval = 1

    # first 20s, check every second
    while total_time < 20:
        total_time += current_interval
        yield current_interval

    # first 5min, check every 5s
    current_interval = 5
    while total_time < 300:
        total_time += current_interval
        yield current_interval

    # after 5min, check every 15s
    current_interval = 15
    while True:
        yield current_interval


class SerialLocalRunner(object):

    def __init__(self, tasks, max_retries, callback_url):
        self.tasks = tasks
        self.max_retries = max_retries
        self.callback_url = callback_url

    def run(self):
        result_packages = []
        for t in range(0, len(self.tasks)):
            task = self.tasks[t]
            print(str(time.time()) + ' - SerialLocalRunner - starting task ' +
                  str(t + 1) + ' of ' + str(len(self.tasks)))
            n_tries = 0
            while n_tries < self.max_retries:
                n_tries += 1
                # start the task
                task.start(self.callback_url, 'local')
                # check until its done
                for time_interval in next_time_interval():
                    time.sleep(time_interval)
                    if task.is_done():
                        break
                # if it is done and successful, great
                if task.success():
                    break
                # otherwise, we try again
            result_packages.append(task.get_task_result_package())

        return result_packages
