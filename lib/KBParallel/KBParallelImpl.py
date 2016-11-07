# -*- coding: utf-8 -*-
#BEGIN_HEADER
from pprint import pprint
try:
    # baseclient and this client are in a package
    from .baseclient import BaseClient as _BaseClient  # @UnusedImport
except:
    # no they aren't
    from baseclient import BaseClient as _BaseClient  # @Reimport
import time
import os
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
    GIT_COMMIT_HASH = "f6f87a2564155925d2cf8c2b072bc210c4c7a6c5"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.config = config
        self.checkwait = 1     # seconds between checkjob calls

        # set default time limit
        if not 'time_limit' in config:
            self.config['time_limit'] = 5000000

        #END_CONSTRUCTOR
        pass


    def run(self, ctx, input_params):
        """
        :param input_params: instance of type "KBParallelrunInputParams"
           (Input parameters for run() method. module_name - SDK module name
           (ie. ManyHellos, RNAseq), method_name - method in SDK module
           (TopHatcall, Hiseqcall etc each will have own _prepare(),
           _runEach(), _collect() methods defined), service_ver - optional
           version of SDK module (may be dev/beta/release, or symantic
           version or particular git commit hash), it's release by default,
           is_local - optional flag defining way of scheduling sub-job, in
           case is_local=false sub-jobs are scheduled against remote
           execution engine, if is_local=true then sub_jobs are run as local
           functions through CALLBACK mechanism, default value is false,
           global_input - input data which is supposed to be sent to
           <module_name>.<method_name>_prepare() method, max_num_jobs -
           maximum number of sub-jobs, equals to 5 by default, time_limit -
           time limit in seconds, equals to 5000 by default.) -> structure:
           parameter "module_name" of String, parameter "method_name" of
           String, parameter "service_ver" of String, parameter "is_local" of
           type "boolean" (A boolean - 0 for false, 1 for true. @range (0,
           1)), parameter "global_input" of list of unspecified object,
           parameter "max_num_jobs" of Long, parameter "time_limit" of Long
        :returns: instance of type "Report" (A simple Report of a method run
           in KBase. It only provides for now a way to display a fixed width
           text output summary message, a list of warnings, and a list of
           objects created (each with descriptions). @optional warnings
           file_links html_links direct_html direct_html_link_index @metadata
           ws length(warnings) as Warnings @metadata ws length(text_message)
           as Size(characters) @metadata ws length(objects_created) as
           Objects Created) -> structure: parameter "text_message" of String,
           parameter "warnings" of list of String, parameter
           "objects_created" of list of type "WorkspaceObject" (Represents a
           Workspace object with some brief description text that can be
           associated with the object. @optional description) -> structure:
           parameter "ref" of type "ws_id" (@id ws), parameter "description"
           of String, parameter "file_links" of list of type "LinkedFile"
           (Represents a file or html archive that the report should like to
           @optional description) -> structure: parameter "handle" of type
           "handle_ref" (Reference to a handle @id handle), parameter
           "description" of String, parameter "name" of String, parameter
           "URL" of String, parameter "html_links" of list of type
           "LinkedFile" (Represents a file or html archive that the report
           should like to @optional description) -> structure: parameter
           "handle" of type "handle_ref" (Reference to a handle @id handle),
           parameter "description" of String, parameter "name" of String,
           parameter "URL" of String, parameter "direct_html" of String,
           parameter "direct_html_link_index" of Long
        """
        # ctx is the context object
        # return variables are: rep
        #BEGIN run
        print( "Hi this is KBParallel.run() input_params are")
        pprint( input_params )

        token = ctx['token']
        module_name = input_params['module_name']
        method_name = input_params['method_name']
        module_method = module_name + '.' + method_name
        service_ver = "beta"
        if 'service_ver' in input_params and input_params['service_ver'] is not None: 
            service_ver = input_params['service_ver'] 


        #instantiate ManyHellos client here
        print( "about to initiate client .." )
        client = _BaseClient(self.callbackURL, token=token)


        # issue prepare call
        print( "about to invoke prepare()")
        tasks_ret = client.call_method(module_method + "_prepare",
                                       input_params["global_params"], 
                                       service_ver = service_ver,
                                       context=None)
        print( "back in run")
        tasks = tasks_ret        # Question: why do we need tasks_ret at all?
        pprint( tasks )

        # initiate NJS wrapper
        print( "initiating Execution Engine")
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
            pprint( ["   launching task", task]  )
            #r1 = mh.manyHellos_runEach( ctx, task )
            #pprint( r1 )
            
            jobid = exec_engine_client._submit_job(module_method + "_runEach",
                                                   [task], 
                                                   service_ver=service_ver)
            print( "job_id", jobid )
            jobid_list.append( jobid )
            job_running_list.append( True )
            job_timeout_list.append( None )
            job_input_result_map[jobid] = {"input": [task]}
            njobs = njobs + 1

        # Polling loop to see when job is finished

        print("polling ", njobs, " NJS job status")
        pprint(job_running_list)
        njobs_remaining = njobs      # this will count down to 0 when all jobs completed
        try:
            while njobs_remaining > 0:
    
                # poll each job
                for j in range(0, njobs):
                    if job_running_list[j]:     # only consider those which are still running
                        job_state_desc = exec_engine_client._check_job(module_name, jobid_list[j] )
                        pprint( job_state_desc )
    
                        if job_state_desc["finished"] == 1: # has this job completed
                            print( "**************job ", j, " is done***********" )
                            job_running_list[j] = False
                            njobs_remaining = njobs_remaining - 1
    
                            if "error" in job_state_desc:                                # if it crashed, 
                                print( "************** job ", j, " has crashed*********" )
                                raise Exception("jobs canceled because of failure")
                            elif 'result' in job_state_desc:
                                job_input_result_map[jobid_list[j]]['output'] = job_state_desc['result']
                            else:
                                raise Exception("Unexpected job state (no error/result fields")
                        else:                                                            # if its running, check for timeout
                            print( "checking timeout for this job" )
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
                    print("Stopping all sub-jobs...")
                    for jobid in jobs_to_stop:
                        try:
                            remote_ee_client.cancel_job( { 'job_id': jobid } )
                        except:
                            print("Error canceling job " + jobid)

        # at this point, NJS informed us that job is finished, must now check error status

        # Question: best way to determine a successful completion or not from the
        #           jobs state

        print( "about to invoke collect()" )
        job_input_result_list = [job_input_result_map[key] for key in job_input_result_map]
        # TODO: we should be able to send job_input_result_list to collect-method
        res = client.call_method(module_method + "_collect", 
                                 input_params["global_params"], 
                                 service_ver = service_ver,
                                 context=None)
        pprint( res )
        # for now, return a dummy object with a string message

        rep = { 'msg': "default KBparallel.run() return value" }
        #END run

        # At some point might do deeper type checking...
        if not isinstance(rep, dict):
            raise ValueError('Method run return value ' +
                             'rep is not type dict as required.')
        # return the results
        return [rep]

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
