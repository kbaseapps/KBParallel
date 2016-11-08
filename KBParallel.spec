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
        module_name - SDK module name (ie. ManyHellos, RNAseq),
        method_name - method in SDK module (TopHatcall, Hiseqcall etc each will have own _prepare(),
            _runEach(), _collect() methods defined),
        service_ver - optional version of SDK module (may be dev/beta/release, or symantic version
            or particular git commit hash), it's release by default,
    */
    typedef structure {
        string module_name;
        string method_name;
        string service_ver;
    } FullMethodQualifier;

    /*
        Input parameters for run() method.

        method - optional method where _prepare(), _runEach() and _collect() suffixes are applied,
        prepare_method - optional method (if defined overrides _prepare suffix rule),
        is_local - optional flag defining way of scheduling sub-job, in case is_local=false sub-jobs
            are scheduled against remote execution engine, if is_local=true then sub_jobs are run as
            local functions through CALLBACK mechanism, default value is false,
        global_input - input data which is supposed to be sent as a part to 
            <module_name>.<method_name>_prepare() method,
        time_limit - time limit in seconds, equals to 5000 by default.
    */
    typedef structure {
        FullMethodQualifier method;
        FullMethodQualifier prepare_method;
        boolean is_local;
        UnspecifiedObject global_input;
        int time_limit;
    } KBParallelrunInputParams;

    async funcdef run(KBParallelrunInputParams input_params)
        returns (UnspecifiedObject) authentication required;

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

    funcdef job_status(KBParallelstatusInputParams input_params) returns(KBParallelstatusOutputObj ret) authentication required;

    /*
        cancel_run() method
    */

    typedef structure {
    } KBParallelcancel_runInput;
    
    typedef structure {
    } KBParallelcancel_runOutput;

    funcdef cancel_run(KBParallelcancel_runInput input_params) returns(KBParallelcancel_runOutput ret) authentication required;

    /*
        getlog() method
    */

    typedef structure {
    } KBParallelgetlogInput;
    
    typedef structure {
    } KBParallelgetlogOutput;

    funcdef getlog( KBParallelgetlogInput input_params) returns( KBParallelgetlogOutput ret ) authentication required;

};
