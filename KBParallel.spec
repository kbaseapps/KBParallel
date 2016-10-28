/*
A KBase module: KBParallel
*/
#include <KBaseReport.spec>

module KBParallel {
    /*
        Insert your typespec information here.
    */

    /*
       run() method 
    */

    typedef structure {
        string module_name;         /* ie. ManyHellos, RNAseq */
        string method_name;         /* manyHellos (TopHatcall, Hiseqcall etc each will have own _prepare(), _runEach(), _collect() methods defined) */
        string service_ver;         /* ie. "beta", "dev", "release" */
        list<UnspecifiedObject>  prepare_params; /* prepare parameter  and prepare method will generate runEach parameters */
        list<UnspecifiedObject>  collect_params; /* collect parameter */
        string client_class_name;   /* if it is different default $ModuleName.$ModuleNameClient  */
        int   time_limit;           /* minutes? */
    } KBParallelrunInputParams;

    /* SJ: the following is not necessary */
    typedef structure {
         KBaseReport.Report  report;
         string              msg;        /* any additional message */
    }  KBParallelOutputObj;

    async funcdef run( KBParallelrunInputParams input_params ) returns( KBaseReport.Report rep ) authentication required;

    /* Narrative Method Spec call helper function */
    async funcdef run_narrative( KBParallelrunInputParams input_params ) returns( KBaseReport.Report rep ) authentication required;

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

    funcdef status( KBParallelstatusInputParams input_params ) returns( KBParallelstatusOutputObj ret ) authentication required;

    /*
       cancel_run() method
    */

    typedef string KBParallelcancel_runInput;
    typedef string KBParallelcancel_runOutput;

    funcdef cancel_run( KBParallelcancel_runInput input_params ) returns( KBParallelcancel_runOutput ret ) authentication required;

    /*
       getlog() method
    */

    typedef string KBParallelgetlogInput;
    typedef string KBParallelgetlogOutput;

    funcdef getlog( KBParallelgetlogInput input_params) returns( KBParallelgetlogOutput ret ) authentication required;

};
