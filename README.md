[![Build Status](https://travis-ci.org/mccorkle/KBParallel.svg?branch=master)](https://travis-ci.org/mccorkle/KBParallel)

# KBParallel
---
To test:
```
kb-sdk test -s 
```

edit test_local/test.cfg with ci entrypoint, test user and its password

```
kb-sdk test -s
```


## Example Usage
```
kbp = KBParallel(url=https://ci.kbase.us/services/kbparallel, token=ctx[token])
report = kbp.run({ module_name : RNASeq,
                              method_name : "CallTophat",
                              service_ver: "beta",
                              prepare_params : [{ "sample_set" : "1234/5/6", 
                                                               "genome" : "1234/7/1",
                                                               " }]
                              collect_params : [{ "alignment_set_name" : "toy_alignmt" }],
                              time_limit : 1500})
```
