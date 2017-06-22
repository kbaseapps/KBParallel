# -*- coding: utf-8 -*-
#BEGIN_HEADER
from pprint import pprint,pformat
try:
    # baseclient and this client are in a package
    from .baseclient import BaseClient as _BaseClient  # @UnusedImport
except:
    # no they aren't
    from baseclient import BaseClient as _BaseClient  # @Reimport
import time
import os
import sys
import json
import logging
from biokbase.njs_wrapper.client import NarrativeJobService as NJS

from KBParallel.BatchRunner import BatchRunner

def notyet( msg ):
    return( msg + " is not implemented yet" )

# return a list of vals where corresponding values of include are True
def reduce_list( vals, include ):
    result_vals = []
    for j in range( len( vals ) ):
        if include[j]:
            result_vals.append( vals[j])
    return( result_vals )


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
    VERSION = "0.0.8"
    GIT_URL = "git@github.com:kbaseapps/KBParallel"
    GIT_COMMIT_HASH = "cc8be3deafe57c33f6a0605ea88c308092af1dac"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.config = config

        if not 'check_interval' in config:
            self.config['check_interval'] = 30
        self.checkwait = int(self.config['check_interval']) # seconds between checkjob calls

        # set default time limit
        if not 'time_limit' in config:
            self.config['time_limit'] = 5000000

        if not 'sync_cb_time_limit' in config:
            self.config['sync_cb_time_limit'] = 14400 # 4 hours for large genome object

        # logging
        self.__LOGGER = logging.getLogger('KBaseRNASeq')
        if 'log_level' in config:
              self.__LOGGER.setLevel(config['log_level'])
        else:
              self.__LOGGER.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s")
        formatter.converter = time.gmtime
        streamHandler.setFormatter(formatter)
        self.__LOGGER.addHandler(streamHandler)
        self.__LOGGER.info("Logger was set")

        #END_CONSTRUCTOR
        pass


    def run_batch(self, ctx, params):
        """
        :param params: instance of type "RunBatchParams" (runner =
           serial_local | parallel_local | parallel) -> structure: parameter
           "tasks" of list of type "Task" (Specifies a task to run. 
           Parameters is an arbitrary data object passed to the function.  If
           it is a list, the params will be interpreted as) -> structure:
           parameter "function" of type "Function" (Specifies a specific
           KBase module function to run) -> structure: parameter
           "module_name" of String, parameter "function_name" of String,
           parameter "version" of String, parameter "params" of unspecified
           object, parameter "runner" of String, parameter
           "concurrent_local_tasks" of Long, parameter
           "concurrent_njsw_tasks" of Long, parameter "max_retries" of Long
        :returns: instance of type "BatchResults" (The list of results will
           be in the same order as the input list of tasks.) -> structure:
           parameter "results" of list of type "TaskResult" -> structure:
           parameter "function" of type "Function" (Specifies a specific
           KBase module function to run) -> structure: parameter
           "module_name" of String, parameter "function_name" of String,
           parameter "version" of String, parameter "params" of unspecified
           object, parameter "returned" of unspecified object, parameter
           "error" of unspecified object, parameter "run_context" of type
           "RunContext" (location = local | njsw job_id = '' | [njsw_job_id]
           May want to add: AWE node ID, client group, total run time, etc)
           -> structure: parameter "location" of String, parameter "job_id"
           of String
        """
        # ctx is the context object
        # return variables are: results
        #BEGIN run_batch
        br = BatchRunner(self.callbackURL, self.config, ctx['token'])
        result_packages = br.run(params)
        results = {'results': result_packages}
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
