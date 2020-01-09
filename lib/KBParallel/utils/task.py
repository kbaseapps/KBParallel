from KBParallel.utils.job import Job


class Task:
    """
    An object representing a task to be run either locally or remotely.
    Contains module_name, method_name, and parameters for a task.

    Also contains a list of jobs that were run, a count of run failures, error messages, and
    responses.

    If a task is running, then it will have a .current_job field that points to the currently
    running Job object.
    """

    def __init__(self, args, task_manager):
        """
        Create a new task, passing in the parameters for a Task (see KBParallel.spec)
        keys in `args`:
          module_name - required - module name to run
          function_name - required - method name in the module to run
          params - required - parameters to pass to the method
          task_manager - required - task manager that created this task
        Also pass in a TaskManager instance as the second parameter
        """
        self.task_manager = task_manager
        self.method_name = args['function_name']
        self.module_name = args['module_name']
        self.full_name = self.module_name + '.' + self.method_name
        self.service_ver = args['version']
        self.params = args['parameters']
        self.failures = 0
        self.jobs = []
        self.results = None
        self.current_job = None
        self.completed = False

    def start_job(self, run_location):
        """Spawn a new job for this task."""
        job = Job(
            task=self,
            task_manager=self.task_manager,
            run_location=run_location
        )
        self.current_job = job
        self.jobs.append(job)

    def handle_job_results(self, results):
        """Update the results for a finished current_job."""
        if results.get('error'):
            self.failures += 1
        elif results.get('finished'):
            self.completed = True
            self.results = results
        if self.failures == self.task_manager.max_retries:
            self.completed = True
            self.results = results
