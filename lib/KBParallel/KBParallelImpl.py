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
import json
import logging
from biokbase.njs_wrapper.client import NarrativeJobService as NJS


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
    
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.7"
    GIT_URL = "https://github.com/sean-mccorkle/KBparallel"
    GIT_COMMIT_HASH = "e09860b56e22e348eb6ffc78b6b75517296761cc"

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

        # logging
        self.__LOGGER = logging.getLogger('KBaseRNASeq')
        if 'log_level' in config:
              self.__LOGGER.setLevel(config['log_level'])
        else:
              self.__LOGGER.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(filename)s - %(lineno)d - %(ip)s - %(levelname)s - %(message)s")
        formatter.converter = time.gmtime
        streamHandler.setFormatter(formatter)
        self.__LOGGER.addHandler(streamHandler)
        self.__LOGGER.info("Logger was set")

        #END_CONSTRUCTOR
        pass


    def run(self, ctx, input_params):
        """
        :param input_params: instance of type "KBParallelrunInputParams"
           (Input parameters for run() method. method - optional method where
           _prepare(), _runEach() and _collect() suffixes are applied,
           prepare_method - optional method (if defined overrides _prepare
           suffix rule), is_local - optional flag defining way of scheduling
           sub-job, in case is_local=false sub-jobs are scheduled against
           remote execution engine, if is_local=true then sub_jobs are run as
           local functions through CALLBACK mechanism, default value is
           false, global_input - input data which is supposed to be sent as a
           part to <module_name>.<method_name>_prepare() method, time_limit -
           time limit in seconds, equals to 5000 by default.) -> structure:
           parameter "method" of type "FullMethodQualifier" (module_name -
           SDK module name (ie. ManyHellos, RNAseq), method_name - method in
           SDK module (TopHatcall, Hiseqcall etc each will have own
           _prepare(), _runEach(), _collect() methods defined), service_ver -
           optional version of SDK module (may be dev/beta/release, or
           symantic version or particular git commit hash), it's release by
           default,) -> structure: parameter "module_name" of String,
           parameter "method_name" of String, parameter "service_ver" of
           String, parameter "prepare_method" of type "FullMethodQualifier"
           (module_name - SDK module name (ie. ManyHellos, RNAseq),
           method_name - method in SDK module (TopHatcall, Hiseqcall etc each
           will have own _prepare(), _runEach(), _collect() methods defined),
           service_ver - optional version of SDK module (may be
           dev/beta/release, or symantic version or particular git commit
           hash), it's release by default,) -> structure: parameter
           "module_name" of String, parameter "method_name" of String,
           parameter "service_ver" of String, parameter "is_local" of type
           "boolean" (A boolean - 0 for false, 1 for true. @range (0, 1)),
           parameter "global_input" of unspecified object, parameter
           "time_limit" of Long
        :returns: instance of unspecified object
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN run
        self.__LOGGER.debug("Input params:\n" + pformat( input_params ))

        token = ctx['token']
        method = input_params.get('method')


        #instantiate ManyHellos client here
        self.__LOGGER.info( "Initiate baseclient .." )
        client = _BaseClient(self.callbackURL, token=token)


        # issue prepare call
        self.__LOGGER.info( "Invoke prepare()")
        prepare_input_params = {'global_input_params': input_params["global_params"], 
                                'global_method': method}
        prepare_method_name = None
        prepare_service_ver = None
        if 'prepare_method' in input_params:
            prepare_method = input_params.get('prepare_method')
            prepare_method_name = (prepare_method['module_name'] + '.' + 
                                   prepare_method['method_name'])
            prepare_service_ver = prepare_method.get('service_ver')
        else:
            if not method:
                raise ValueError("Global method wasn't defined but task doesn't provide " +
                                 "local _runEach alternative")
            module_name = method['module_name']
            method_name = method['method_name']
            prepare_method_name = module_name + '.' + method_name + "_prepare"
            prepare_service_ver = method.get('service_ver', "release")
        schedule = client.call_method(prepare_method_name,
                                      [prepare_input_params], 
                                      service_ver = prepare_service_ver,
                                      context=None)
        self.__LOGGER.debug( "Back in run")
        tasks = schedule['tasks']
        collect_method = schedule.get('collect_method', None)
        self.__LOGGER.info("Task list:\n" + pformat(tasks) )

        # initiate NJS wrapper
        self.__LOGGER.info( "Initiating Execution Engine")
        exec_engine_url = None
        remote_ee_client = None
        is_local = ('is_local' in input_params and input_params['is_local'] == 1)
        if is_local:
            exec_engine_url = self.callbackURL
        else:
            exec_engine_url = self.config['njs-wrapper-url']
            remote_ee_client = NJS(url=self.config['njs-wrapper-url'], token=token)
        exec_engine_client = _BaseClient(exec_engine_url, token=token)

        jobid_list = []         # list of jobids when launched
        job_running_list = []   # list of booleans which are True if the job is queued or running, False when completed
        job_timeout_list = []   # list of job timeout values, None until the job starts
        njobs = 0
        job_input_result_map = {}
        for task in tasks:
            self.__LOGGER.info( "Launching task:" + pformat(task) )
            task_method_module_name = None
            task_service_ver = None
            if 'method' in task:
                task_method = task['method']
                task_method_module_name = (task_method['module_name'] + '.' + 
                                           task_method['method_name'])
                task_service_ver = task_method.get('service_ver', None)
            else:
                if not method:
                    raise ValueError("Global method wasn't defined but task doesn't provide " +
                                     "local _runEach alternative")
                module_name = method['module_name']
                method_name = method['method_name']
                task_method_module_name = module_name + '.' + method_name + "_runEach"
                task_service_ver = method.get('service_ver', "release")
            task_input = task['input_arguments']

            if not isinstance(task_input, list): #for sementic compatibility w/ prepare and collect
                task_input = [task_input]
            
            jobid = exec_engine_client._submit_job(task_method_module_name,
                                                   task_input, 
                                                   service_ver=task_service_ver)
            self.__LOGGER.info( "Job_id: ", jobid )
            jobid_list.append( jobid )
            job_running_list.append( True )
            job_timeout_list.append( None )
            job_input_result_map[jobid] = {'input': task}
            njobs = njobs + 1

        # Polling loop to see when job is finished

        self.__LOGGER.info("Polling " +  njobs + " NJS job status")
        self.__LOGGER.info(pformat(job_running_list))
        njobs_remaining = njobs      # this will count down to 0 when all jobs completed
        try:
            while njobs_remaining > 0:
    
                # poll each job
                for j in range(0, njobs):
                    if job_running_list[j]:     # only consider those which are still running
                        jobid = jobid_list[j]
                        task = job_input_result_map[jobid]['input']
                        task_module_name = None
                        if 'method' in task:
                            task_module_name = task['method']['module_name']
                        else:
                            task_module_name = method['module_name']
                        job_state_desc = exec_engine_client._check_job(task_module_name, jobid )
                        self.__LOGGER.info( "Job state:" + pformat(job_state_desc))
    
                        if job_state_desc["finished"] == 1: # has this job completed
                            self.__LOGGER.info( "**************job ", j, " is done***********" )
                            job_running_list[j] = False
                            njobs_remaining = njobs_remaining - 1
    
                            if "error" in job_state_desc:                                # if it crashed, 
                                self.__LOGGER.info( "************** job ", j, " has crashed*********" )
                                raise Exception("jobs canceled because of failure")
                            elif 'result' in job_state_desc:
                                job_result = job_state_desc['result']
                                if len(job_result) == 1:
                                    job_result = job_result[0]
                                job_input_result_map[jobid_list[j]]['result'] = job_result
                            else:
                                raise Exception("Unexpected job state (no error/result fields")
                        else:                                                            # if its running, check for timeout
                            self.__LOGGER.info( "checking timeout for this job" )
                            # check timeout of job
                            if job_timeout_list[j] == None :
                                job_timeout_list[j] = time.time() + 60 * self.config['time_limit']   # start the clock if just started
                            if time.time() > job_timeout_list[j] :
                                print "*************TIMEOUT****************"
                                raise Exception("jobs canceled because of timeout")
    
                time.sleep( self.checkwait )
        finally:
            if is_local:
                # TODO: make sure we stop all local sub-containers in SDK CALLBACK
                pass
            else:
                jobs_to_stop = reduce_list( jobid_list, job_running_list )
                if len(jobs_to_stop) > 0:
                    self.__LOGGER.info("Stopping all sub-jobs...")
                    for jobid in jobs_to_stop:
                        try:
                            remote_ee_client.cancel_job( { 'job_id': jobid } )
                        except:
                            self.__LOGGER.info("Error canceling job " + jobid)

        # at this point, NJS informed us that job is finished, must now check error status

        # Question: best way to determine a successful completion or not from the
        #           jobs state

        self.__LOGGER.info( "about to invoke collect()" )
        input_result_pairs = [job_input_result_map[key] for key in job_input_result_map]
        collect_input_params = {'global_params': input_params["global_params"],
                                'input_result_pairs': input_result_pairs}
        collect_module_method_name = None
        collect_service_ver = None
        if collect_method:
            collect_module_method_name = (collect_method['module_name'] + '.' + 
                                          collect_method['method_name'])
            collect_service_ver = collect_method['service_ver']
        else:
            if not method:
                raise ValueError("Global method wasn't defined but schedule doesn't provide " +
                                 "local _collect alternative")
            module_name = method['module_name']
            method_name = method['method_name']
            collect_module_method_name = module_name + '.' + method_name + "_collect"
            collect_service_ver = method.get('service_ver', "release")
        self.__LOGGER.info("Collect input: " + json.dumps(collect_input_params))
        returnVal = client.call_method(collect_module_method_name,
                                 [collect_input_params], 
                                 service_ver = collect_service_ver,
                                 context=None)
        self.__LOGGER.info("Result:\n" + pformat(returnVal))
        #END run

        # At some point might do deeper type checking...
        if not isinstance(returnVal, object):
            raise ValueError('Method run return value ' +
                             'returnVal is not type object as required.')
        # return the results
        return [returnVal]

    def job_status(self, ctx, input_params):
        """
        :param input_params: instance of type "KBParallelstatusInputParams"
           (status() method) -> structure: parameter "joblist" of list of
           String
        :returns: instance of type "KBParallelstatusOutputObj" -> structure:
           parameter "num_jobs_checked" of Long, parameter "jobstatus" of
           list of String
        """
        # ctx is the context object
        # return variables are: ret
        #BEGIN job_status
        ret = notyet( "job_status" )
        #END job_status

        # At some point might do deeper type checking...
        if not isinstance(ret, dict):
            raise ValueError('Method job_status return value ' +
                             'ret is not type dict as required.')
        # return the results
        return [ret]

    def cancel_run(self, ctx, input_params):
        """
        :param input_params: instance of type "KBParallelcancel_runInput"
           (cancel_run() method) -> structure:
        :returns: instance of type "KBParallelcancel_runOutput" -> structure:
        """
        # ctx is the context object
        # return variables are: ret
        #BEGIN cancel_run
        ret = notyet( "cancel_run" )
        #END cancel_run

        # At some point might do deeper type checking...
        if not isinstance(ret, dict):
            raise ValueError('Method cancel_run return value ' +
                             'ret is not type dict as required.')
        # return the results
        return [ret]

    def getlog(self, ctx, input_params):
        """
        :param input_params: instance of type "KBParallelgetlogInput"
           (getlog() method) -> structure:
        :returns: instance of type "KBParallelgetlogOutput" -> structure:
        """
        # ctx is the context object
        # return variables are: ret
        #BEGIN getlog
        ret = notyet( "getlog" )
        #END getlog

        # At some point might do deeper type checking...
        if not isinstance(ret, dict):
            raise ValueError('Method getlog return value ' +
                             'ret is not type dict as required.')
        # return the results
        return [ret]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
