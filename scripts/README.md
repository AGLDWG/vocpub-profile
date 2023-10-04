# Scripts

This directory contains Python scripts used to assist with the publication of this Profile and for reuse by profile users.

The scripts are:

* `combine.py`
    * merges the `validate.ttl` SHACL validator and `inferencer.py`, the SHACL inferencing script that expands data graphs before validation, according to several SKOS rules
    * this is run automatically when changes are made to this repository so `combine.py` is always up-to-date with respect to its constituent parts
* `validate.py`
    * validates given data using the `cmobined.ttl` - the consolidated validator created by `combine.py`
