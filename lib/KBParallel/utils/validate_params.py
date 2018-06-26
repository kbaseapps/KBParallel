"""
Validate and set defaults for the arguments to .run_batch, passed into KBParallelImpl
"""


def validate_params(params):
    """
    Validate the parameters passed to KBParallel.run_batch
    Also refer to the type def for run_batch in KBParallel.spec
    """
    if 'tasks' not in params or not params['tasks']:
        raise ValueError('"tasks" field with a list of tasks is required.')
    if 'runner' not in params:
        raise ValueError('"runner" field is required')
    if params['runner'] not in ['local_serial', 'local_parallel', 'parallel']:
        raise ValueError('Unknown or unsupported runner type: ' + str(params['runner']))
    # Set some defaults for the concurrent task limits based on the runner type
    if params['runner'] == 'local_parallel':
        params.setdefault('concurrent_local_tasks', 2)
    else:
        params.setdefault('concurrent_local_tasks', 1)
    if params['runner'] == 'parallel':
        params.setdefault('concurrent_njsw_tasks', 3)
    else:
        params.setdefault('concurrent_njsw_tasks', 0)
    if 'concurrent_local_tasks' in params:
        # Clamp the range of concurrent_local_tasks between 0 and 20
        params['concurrent_local_tasks'] = max(0, min(params['concurrent_local_tasks'], 20))
    if 'concurrent_njsw_tasks' in params:
        # Clamp the range of concurrent_njsw_tasks between 0 and 50
        params['concurrent_njsw_tasks'] = max(0, min(params['concurrent_njsw_tasks'], 50))
    if 'max_retries' in params and params['max_retries'] is not None:
        # Clamp max retries between 1 and 5
        params['max_retries'] = max(1, min(params['max_retries'], 5))
    params.setdefault('max_retries', 1)
    return params
