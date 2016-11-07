/*
A KBase module: KBParallel
*/
#include <KBaseReport.spec>

module KBParallel {

    /* 
        A boolean - 0 for false, 1 for true.
        @range (0, 1)
    */
    typedef int boolean;

    /*
        Input parameters for run() method.
        
        module_name - SDK module name (ie. ManyHellos, RNAseq),
        method_name - method in SDK module (TopHatcall, Hiseqcall etc each will have own _prepare(),
            _runEach(), _collect() methods defined),
        service_ver - optional version of SDK module (may be dev/beta/release, or symantic version
            or particular git commit hash), it's release by default,
        is_local - optional flag defining way of scheduling sub-job, in case is_local=false sub-jobs
            are scheduled against remote execution engine, if is_local=true then sub_jobs are run as
            local functions through CALLBACK mechanism, default value is false,
        global_input - input data which is supposed to be sent to 
            <module_name>.<method_name>_prepare() method,
        max_num_jobs - maximum number of sub-jobs, equals to 5 by default,
        time_limit - time limit in seconds, equals to 5000 by default.
    */
    typedef structure {
        string module_name;
        string method_name;
        string service_ver;
        boolean is_local;
        list<UnspecifiedObject> global_input;
        int max_num_jobs;
        int time_limit;
    } KBParallelrunInputParams;

    /*
        msg - any additional message.
    */
    typedef structure {
        KBaseReport.Report report;
        string msg;
    } KBParallelOutputObj;

    async funcdef run( KBParallelrunInputParams input_params ) 
        returns (KBaseReport.Report rep) authentication required;

    /*
        status() method
    */

    typedef structure {
        list<string>  joblist; /* job id could be UUID */
    } KBParallelstatusInputParams;

    typedef structure {
        int num_jobs_checked;
        list<string> jobstatus;
    } KBParallelstatusOutputObj;

    funcdef job_status( KBParallelstatusInputParams input_params ) returns( KBParallelstatusOutputObj ret ) authentication required;

    /*
        cancel_run() method
    */

    typedef structure {
    } KBParallelcancel_runInput;
    
    typedef structure {
    } KBParallelcancel_runOutput;

    funcdef cancel_run( KBParallelcancel_runInput input_params ) returns( KBParallelcancel_runOutput ret ) authentication required;

    /*
        getlog() method
    */

    typedef structure {
    } KBParallelgetlogInput;
    typedef structure {
    } KBParallelgetlogOutput;

    funcdef getlog( KBParallelgetlogInput input_params) returns( KBParallelgetlogOutput ret ) authentication required;

};
