/*
Module for distributing a set of jobs in batch to run either locally or on njsw
*/

module KBParallel {

    /* 
        A boolean - 0 for false, 1 for true.
        @range (0, 1)
    */
    typedef int boolean;

    /* Specifies a specific KBase module function to run */
    typedef structure {
        string module_name;
        string function_name;
        string version;
    } Function;

    /* Specifies a task to run.  Parameters is an arbitrary data object
    passed to the function.  If it is a list, the params will be interpreted
    as 
    */
    typedef structure {
        Function function;
        UnspecifiedObject params;
        /* May be useful in the future to require particular tasks to run locally or not
        boolean run_local;*/
    } Task;

    /*
        location = local | njsw
        job_id = '' | [njsw_job_id]

        May want to add: AWE node ID, client group, total run time, etc
    */
    typedef structure {
        string location;
        string job_id;
    } RunContext;

    typedef structure {
        Function function;
        UnspecifiedObject result;
        UnspecifiedObject error;
        RunContext run_context;
    } ResultPackage;

    typedef structure {
        boolean is_error;
        ResultPackage result_package;
    } TaskResult;

    /*
    The list of results will be in the same order as the input list of tasks.
    */
    typedef structure {
        list <TaskResult> results;
    } BatchResults;


    /* 
        runner = serial_local | parallel_local | parallel
            serial_local will run tasks on the node in serial, ignoring the concurrent
                task limits
            parallel_local will run multiple tasks on the node in parallel, and will
                ignore the njsw_task parameter. Unless you know where your job will
                run, you probably don't want to set this higher than 2
            parallel will look at both the local task and njsw task limits and operate
                appropriately. Therefore, you could always just select this option and
                tweak the task limits to get either serial_local or parallel_local
                behavior.
        
        TODO:
        wsid - if defined, the workspace id or name (service will handle either string or
               int) on which to attach the job. Anyone with permissions to that WS will
               be able to view job status for this run.

    */
    typedef structure {
        list <Task> tasks;

        string runner;

        int concurrent_local_tasks;
        int concurrent_njsw_tasks;
        
        int max_retries;
    } RunBatchParams;


    funcdef run_batch(RunBatchParams params)
        returns (BatchResults results) authentication required;

};
