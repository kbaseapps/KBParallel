
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
```
# invoke from an App like any other KBase SDK function call
parallel_runner = KBParallel(self.callback_url)

# build a list of tasks
tasks = [{'module_name': 'kb_Bowtie2',
         'function_name': 'align_reads_to_assembly_app',
         'version': 'dev',
         'parameters': { ... }
         },
         ...
         ]

# configure how tasks are run
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
