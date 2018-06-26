# KBParallel

Execute batch jobs in KBase.

## Installation

```
kb-sdk install KBParallel
```


## Example Usage

Below is an example of running `KBParallel.run_batch` -- read the comments for details:

```py
# invoke from an App like any other KBase SDK function call
parallel_runner = KBParallel(self.callback_url)

# build a list of tasks
# ---------------------
# The parameters ('parameters': { ... }) are the parameters that are sent to 
# align_reads_to_assembly_app.  For instance, if you are trying to align 
# multiple fastq files in parallel, then the parameters will include 

tasks = [
  {
    'module_name': 'kb_Bowtie2',
    'function_name': 'align_reads_to_assembly_app',
    'version': 'dev',
    'parameters': { ... }  # your app parameters
  },
  ...
]

# NOTE: modules called by kbparallel (i.e. kb_Bowtie2) have to be registered
# in appdev as 'release', 'beta', or 'dev'.


# configure how tasks are run
# ---------------------------
# you can set how many concurrent jobs you want running on the local 
# machine, and how many nodes you want running in parallel.
# For example, in this case, if you have 5 tasks, 2 will be submitted to 2 njsw nodes and the
# remaining 3 will get run in serial on the local machine. 

batch_run_params = {'tasks': tasks,
                    'runner': 'parallel', # parallel | local_parallel | local_serial
                    'concurrent_local_tasks': 1,
                    'concurrent_njsw_tasks': 2,
                    'max_retries': 2 # how many attempts at running a task before admitting defeat
                    }

# submit the tasks
results = parallel_runner.run_batch(batch_run_params)
```

KBParallel will give you back nested python dictionaries of results for every task that was run.
Below is a description of this data structure.

```py
# results data structure
# ----------------------
# The results of the function being called by kbparallel 
# (align_reads_to_assembly_app), must be returned or it will not be accessible; 
# for instance, if align_reads_to_assembly_app creates a new alignment 
# file, the path to this file must be returned in the output dictionary. 

{
  'results': [
    {
      'is_error': 0,
      'result_package': {
        'error': None,
        'function': {
          'function_name': 'align_reads_to_assembly_app',
          'module_name': 'kb_Bowtie2',
          'version': 'dev'
        },
        'result': [ ... Method call return data ... ]
        'run_context': {
          'job_id': '81e3f2c4-5386-45f3-9bbf-d5a7bd23731a',
          'location': 'local'
        }
      }
    },
    ...
  ]
}
```

### Some Examples

For a simple hello world example that runs 3 tasks in parallel; each job creates a .txt file.  The jobs are run on 1 local & 2 njsw nodes. To try it, search for __kbparallel example__ in 'dev'.  (also see https://gitlab.com/jfroula/kbparallel_example.git) .  

For an example that actually does something: search for __bowtie2__ or __Align Reads using Bowtie2 v2.3.2__.  (also see https://github.com/kbaseapps/kb_Bowtie2) .  

This example is tricky because it calls the same function ("align" in Bowtie2Aligner.py) twice, once to set up the parallel tasks (runs this section first `if input_info['run_mode'] == 'sample_set'`) and then again to run each task (runs this section second `if input_info['run_mode'] == 'single_library':`).  This section actually does the work by calling single\_reads\_lib\_run.  

## Development

### Project anatomy

* `lib/KBParallel/utils/task_manager.py` - The TaskManager creates all the tasks, starts jobs, manages the local
  and remote job queues, and polls for the statuses of running jobs.
* `lib/KBParallel/utils/task.py` - A Task represents a KBase module and method with parameters to
  be run either locally or remotely. A task can have multiple jobs (if some fail).
* `lib/KBParallel/utils/job.py` - A Job represents an attempt to run a Task either on NJS or
  locally.
* `lib/KBParallel/utils/validate_params.py` - Utility to validate the parameters passed into
  `KBParallel.run_batch` and set defaults for the data

### Testing

Edit `test_local/test.cfg` with the following settings:

```
test_token=<your_appdev_developer_token>
kbase_endpoint=https://appdev.kbase.us/services
auth_service_url=https://appdev.kbase.us/services/auth/api/legacy/KBase/Sessions/Login
auth_service_url_allow_insecure=false
```

Then run:

```
kb-sdk test 
```
