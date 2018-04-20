# KBParallel
---
A low level module for managing simple bulk execution in KBase.


To test:
```
kb-sdk test 
```

edit test_local/test.cfg with ci entrypoint, test user and its password

```
kb-sdk test
```

## Installation

```
kb-sdk install KBParallel
```


## Example Usage
Please read all comments since a lot of key info is there.  

```
# invoke from an App like any other KBase SDK function call
parallel_runner = KBParallel(self.callback_url)

# build a list of tasks
# ---------------------
# The parameters `'parameters': { ... }` are the parameters that are sent to 
# `align_reads_to_assembly_app`.  For instance, if you are trying to align 
# multiple fastq files in parallel, then the parameters will include 
# the paths to the fastqs.
tasks = [{'module_name': 'kb_Bowtie2',
         'function_name': 'align_reads_to_assembly_app',
         'version': 'dev',
         'parameters': { ... }
         },
         ...
         ]

# NOTE: modules called by kbparallel (i.e. kb_Bowtie2) have to be registered in appdev as 'release', 
# 'beta', or 'dev'.


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


```
# results data structure
# ----------------------
# The results of the function being called by kbparallel 
# (align_reads_to_assembly_app), must be returned or it will not be accessable; 
# for instance, if align_reads_to_assembly_app creates a new alignment 
# file, the path to this file must be returned in the output dictionary. 

results =>
{u'results': [{u'is_error': 0,
               u'result_package': {u'error': None,
                                   u'function': {u'function_name': u'align_reads_to_assembly_app',
                                                 u'module_name': u'kb_Bowtie2',
                                                 u'version': u'dev'
                                                 },
                                   u'result': [ ... Function call returned data ... ]
                                   u'run_context': {u'job_id': u'81e3f2c4-5386-45f3-9bbf-d5a7bd23731a',
                                                    u'location': u'local'}}
              },
              ...
              ]

```

### Some Examples
1) for a simple hello world example running 3 tasks that just create a .txt file using 1 local & 2 njsw nodes:  

To try it, search for "kbparallel example" in 'dev'.  https://gitlab.com/jfroula/kbparallel_example.git

2) for an example that actually does something, see:  

search for bowtie2 or "Align Reads using Bowtie2 v2.3.2".  https://github.com/kbaseapps/kb_Bowtie2. 

This example is tricky because it calls the same function ("align" in Bowtie2Aligner.py) twice, once to set up the parallel tasks (runs this section first `if input_info['run_mode'] == 'sample_set'`)  

and then again to run each task (runs this section second `if input_info['run_mode'] == 'single_library':`).  This section actually does the work by calling single\_reads\_lib\_run.  
