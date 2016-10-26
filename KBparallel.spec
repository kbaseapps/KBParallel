/*
A KBase module: KBparallel
*/
#include <KBaseReport.spec>

module KBparallel {
    /*
        Insert your typespec information here.
    */

    /*
       run() method 
    */

    typedef structure {
        string module_name;         /* ManyHellos  RNAseq */
        string method_name;         /* manyHellos (TopHatcall, Hiseqcall etc each will have own _prepare(), _runEach(), _collect() methods defined */
        string service_ver;         /* ie. "beta" */
        list<UnspecifiedObject>  method_params; /* list of parameters specific to the job */
        string client_class_name;   /* None */
        int   time_limit;           /* minutes? */
    } KBparallelrunInputParams;

    typedef structure {
         KBaseReport.Report  report;
         string              msg;        /* any additional message */
    }  KBparallelOutputObj;

    async funcdef run( KBparallelrunInputParams input_params ) returns( KBparallelOutputObj rep ) authentication required;

    /*
       status() method
    */

    typedef structure {
        list<int>  joblist;
    } KBparallelstatusInputParams;

    typedef structure {
        int num_jobs_checked;
        list<string> jobstatus;
    } KBparallelstatusOutputObj;

    funcdef status( KBparallelstatusInputParams input_params ) returns( KBparallelstatusOutputObj ret ) authentication required;

    /*
       cancel_run() method
    */

    typedef string KBparallelcancel_runInput;
    typedef string KBparallelcancel_runOutput;

    funcdef cancel_run( KBparallelcancel_runInput input_params ) returns( KBparallelcancel_runOutput ret ) authentication required;

    /*
       getlog() method
    */

    typedef string KBparallelgetlogInput;
    typedef string KBparallelgetlogOutput;

    funcdef getlog( KBparallelgetlogInput input_params) returns( KBparallelgetlogOutput ret ) authentication required;

};
