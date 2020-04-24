from KBParallel.baseclient import BaseClient
from KBParallel.baseclient import ServerError

from installed_clients.execution_engine2Client import execution_engine2 as EE2


class Job:
    """
    A job that runs the module and method specified by a Task. Contains a job_id and a reference to
    the task that spawned it.

    A Task can have many Jobs. If a Task immediately succeeds, then it will only have one Job. If a
    Task fails twice, then succeeds, then it will have three Jobs.
    """

    def __init__(self, **kwargs):
        """
        Initialize a new job for a task and run it immediately, either locally with the callback
        server or remotely with NJS
        Keyword arguments:
          task - required - Task object (see ./task.py)
          task_manager - required - TaskManager object (see ./task_manager.py)
          run_location - required - one of 'local' or 'njsw'
        """
        self.task = kwargs['task']
        self.task_manager = kwargs['task_manager']
        self.error = None
        self.location = kwargs['run_location']
        if self.location == 'local':
            token = self.task_manager.context['token']
            self.base_client = BaseClient(self.task_manager.callback_url, token=token)
            self.run_local()
        else:
            self.ee2 = EE2(self.task_manager.ee2_url)
            self.run_remotely()

    def run_local(self):
        """Run a job locally using the callback server."""
        try:
            self.job_id = self.base_client._submit_job(
                self.task.full_name,
                [self.task.params],  # The RPC server expects this in a list
                service_ver=self.task.service_ver
            )
        except Exception as err:
            self.set_failed_state(err)

    def run_remotely(self):
        """Run a task remotely using NJSW."""
        parent_job_id = self.task_manager.parent_job_id
        try:
            params = self.task.params
            runjob_params = {
                "method": self.task.full_name,
                "params": [params],
                'service_ver': self.task.service_ver,
                'parent_job_id': parent_job_id,
                "app_id": self.task.full_name.split(".")[0],
                'wsid': self.task_manager.workspace_id,
                'remote_url': self.task_manager.ee2_url,
            }
            self.job_id = self.ee2.run_job(params=runjob_params)
        except Exception as err:
            self.set_failed_state(err)
            raise (err)

    def set_failed_state(self, err):
        """Mark the job as failed from an exception that was thrown."""
        self.error = err
        self.task.handle_job_results({'error': str(err)})

    def check_status(self):
        """Check the status of this job, either on NJS or locally."""
        if self.error:
            # An error has already been thrown; nothing to do.
            return
        if self.location == 'local':
            results = self.check_local_status()
        else:
            results = self.check_ee2_status()
        self.task.handle_job_results(results)

    def check_local_status(self):
        """Check the result of a running local job using BaseClient."""
        module = self.task.module_name
        try:
            status = self.base_client._check_job(module, self.job_id)
        except ServerError as err:
            self.error = err
            status = {'finished': 1, 'job_state': 'suspend', 'error': str(err)}
        return status

    def check_ee2_status(self):
        """Check the result of a job running on NJS."""

        cjp = {'job_id': self.job_id, 'projection': []}
        job_state = self.ee2.check_job(params=cjp)
        self.error = job_state.get('error')
        return job_state
