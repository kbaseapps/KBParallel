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

    /*
     * Specifies a task to run by module name, method name, version, and parameters. Parameters is
     * an arbitrary data object passed to the function.
     */
    typedef structure {
        Function function;
        UnspecifiedObject params;
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
     * Run a set of multiple batch jobs, either locally or remotely. If run remotely, they will be
     * started using NarrativeJobService#run_job. If run locally, the job will be started using the
     * callback server.
     *
     * Required arguments:
     *   tasks - a list of task objects to be run in batch (see the Task type).
     * Optional arguments:
     *   runner - one of 'local_serial', 'local_parallel', or 'parallel':
     *      local_serial - run tasks on the node in serial, ignoring the concurrent task limits
     *      local_parallel - run multiple tasks on the node in parallel. Unless you know where your
     *        job will run, you probably don't want to set this higher than 2
     *      parallel - look at both the local task and njsw task limits and operate appropriately.
     *        Therefore, you could always just select this option and tweak the task limits to get
     *        either serial_local or parallel_local behavior.
     *   concurrent_njsw_tasks - how many concurrent tasks to run remotely on NJS. This has a
     *     maximum of 50.
     *   concurrent_local_tasks - how many concurrent tasks to run locally. This has a hard maximum
     *     of 20, but you will only want to set this to about 2 due to resource limitations.
     *   max_retries - how many times to re-attempt failed jobs. This has a minimum of 1 and
     *     maximum of 5.
     *   parent_job_id - you can manually pass in a custom job ID which will be assigned to NJS
     *     sub-jobs that are spawned by KBParallel. This is useful if you need to track the running
     *     tasks that were started by KBParallel.
     *   workspace_id - a custom workspace ID to assign to new NJS jobs that are spawned by
     *     KBParallel.
    */
    typedef structure {
        list <Task> tasks;
        string runner;
        int concurrent_local_tasks;
        int concurrent_njsw_tasks;
        int max_retries;
        string parent_job_id;
        int workspace_id;
    } RunBatchParams;


    /*
     * Run many tasks in parallel, either locally or remotely.
     */
    funcdef run_batch(RunBatchParams params)
        returns (BatchResults results) authentication required;

};
