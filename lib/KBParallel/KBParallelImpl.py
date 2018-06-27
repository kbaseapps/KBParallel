# -*- coding: utf-8 -*-
#BEGIN_HEADER
import time
import os
import sys
import logging

from KBParallel.utils.validate_params import validate_params
from KBParallel.utils.task_manager import TaskManager
#END_HEADER


class KBParallel:
    '''
    Module Name:
    KBParallel

    Module Description:
    Module for distributing a set of jobs in batch to run either locally or on njsw
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.4.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = "9c0d4e88bd5535a46a95aee3d0835775e002641f"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.config = config
        # logging
        self.__LOGGER = logging.getLogger('KBParallel')
        if 'log_level' in config:
            self.__LOGGER.setLevel(config['log_level'])
        else:
            self.__LOGGER.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s")
        formatter.converter = time.gmtime
        streamHandler.setFormatter(formatter)
        self.__LOGGER.addHandler(streamHandler)
        #END_CONSTRUCTOR
        pass


    def run_batch(self, ctx, params):
        """
        Run many tasks in parallel, either locally or remotely.
        :param params: instance of type "RunBatchParams" (* Run a set of
           multiple batch jobs, either locally or remotely. If run remotely,
           they will be * started using NarrativeJobService#run_job. If run
           locally, the job will be started using the * callback server. * *
           Required arguments: *   tasks - a list of task objects to be run
           in batch (see the Task type). * Optional arguments: *   runner -
           one of 'local_serial', 'local_parallel', or 'parallel': *     
           local_serial - run tasks on the node in serial, ignoring the
           concurrent task limits *      local_parallel - run multiple tasks
           on the node in parallel. Unless you know where your *        job
           will run, you probably don't want to set this higher than 2 *     
           parallel - look at both the local task and njsw task limits and
           operate appropriately. *        Therefore, you could always just
           select this option and tweak the task limits to get *       
           either serial_local or parallel_local behavior. *  
           concurrent_njsw_tasks - how many concurrent tasks to run remotely
           on NJS. This has a *     maximum of 50. *   concurrent_local_tasks
           - how many concurrent tasks to run locally. This has a hard
           maximum *     of 20, but you will only want to set this to about 2
           due to resource limitations. *   max_retries - how many times to
           re-attempt failed jobs. This has a minimum of 1 and *     maximum
           of 5. *   parent_job_id - you can manually pass in a custom job ID
           which will be assigned to NJS *     sub-jobs that are spawned by
           KBParallel. This is useful if you need to track the running *    
           tasks that were started by KBParallel. *   workspace_id - a custom
           workspace ID to assign to new NJS jobs that are spawned by *    
           KBParallel.) -> structure: parameter "tasks" of list of type
           "Task" (* Specifies a task to run by module name, method name,
           version, and parameters. Parameters is * an arbitrary data object
           passed to the function.) -> structure: parameter "function" of
           type "Function" (Specifies a specific KBase module function to
           run) -> structure: parameter "module_name" of String, parameter
           "function_name" of String, parameter "version" of String,
           parameter "params" of unspecified object, parameter "runner" of
           String, parameter "concurrent_local_tasks" of Long, parameter
           "concurrent_njsw_tasks" of Long, parameter "max_retries" of Long,
           parameter "parent_job_id" of String, parameter "workspace_id" of
           type "workspace_id" (* Workspace ID reference in the format
           'workspace_id/object_id/version' * @id ws)
        :returns: instance of type "BatchResults" (The list of results will
           be in the same order as the input list of tasks.) -> structure:
           parameter "results" of list of type "TaskResult" -> structure:
           parameter "is_error" of type "boolean" (A boolean - 0 for false, 1
           for true. @range (0, 1)), parameter "result_package" of type
           "ResultPackage" -> structure: parameter "function" of type
           "Function" (Specifies a specific KBase module function to run) ->
           structure: parameter "module_name" of String, parameter
           "function_name" of String, parameter "version" of String,
           parameter "result" of unspecified object, parameter "error" of
           unspecified object, parameter "run_context" of type "RunContext"
           (location = local | njsw job_id = '' | [njsw_job_id] May want to
           add: AWE node ID, client group, total run time, etc) -> structure:
           parameter "location" of String, parameter "job_id" of String
        """
        # ctx is the context object
        # return variables are: results
        #BEGIN run_batch
        params = validate_params(params)
        task_manager = TaskManager(
            callback_url=self.callbackURL,
            config=self.config,
            context=ctx,
            params=params
        )
        task_manager.execute_all()
        results = {'results': task_manager.results}
        #END run_batch

        # At some point might do deeper type checking...
        if not isinstance(results, dict):
            raise ValueError('Method run_batch return value ' +
                             'results is not type dict as required.')
        # return the results
        return [results]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
