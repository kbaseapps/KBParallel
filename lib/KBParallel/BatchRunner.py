
from KBParallel.Task import Task

class BatchRunner(object):

    def __init__(self):
        pass


    def run(self, parameters):



        # build task list
        tasks = []
        for t in task_specification_list:
            tasks.append(Task(self, module_name, function_name, version, parameters, token))




        tasks = []
        for tas



        pass




    def build_tasks(self, task_specification_list):
        tasks = []
        for t in task_specification_list:



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




