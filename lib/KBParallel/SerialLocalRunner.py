
import time


def next_time_interval():
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
