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
    GIT_COMMIT_HASH = "b76a9224cdbcf7471fee888cbc535d6dbd8065b4"

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
        :param params: instance of type "RunBatchParams" (runner =
           local_serial | local_parallel | parallel local_serial will run
           tasks on the node in serial, ignoring the concurrent task limits
           local_parallel will run multiple tasks on the node in parallel,
           and will ignore the njsw_task parameter. Unless you know where
           your job will run, you probably don't want to set this higher than
           2 parallel will look at both the local task and njsw task limits
           and operate appropriately. Therefore, you could always just select
           this option and tweak the task limits to get either serial_local
           or parallel_local behavior. TODO: wsid - if defined, the workspace
           id or name (service will handle either string or int) on which to
           attach the job. Anyone with permissions to that WS will be able to
           view job status for this run. parent_job_id is an optional
           parameter that allows you to manually set the parent_job_id of all
           tasks that KBParallel will run.) -> structure: parameter "tasks"
           of list of type "Task" (Specifies a task to run.  Parameters is an
           arbitrary data object passed to the function.  If it is a list,
           the params will be interpreted as) -> structure: parameter
           "function" of type "Function" (Specifies a specific KBase module
           function to run) -> structure: parameter "module_name" of String,
           parameter "function_name" of String, parameter "version" of
           String, parameter "params" of unspecified object, parameter
           "runner" of String, parameter "concurrent_local_tasks" of Long,
           parameter "concurrent_njsw_tasks" of Long, parameter "max_retries"
           of Long, parameter "parent_job_id" of String
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
