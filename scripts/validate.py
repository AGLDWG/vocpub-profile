"""
This Python script validates a given RDF data file either with or without first expanding the data.

Use:

    ~$ python validate.py {path-to-data-file} -e {true|false}

    where -e means to expand the data before validation
"""

import sys
from pathlib import Path
from rdflib import Graph
from pyshacl import validate


if __name__ == "__main__":
    validators_dir = Path(__file__).parent.parent.absolute() / "validators"

    # load the given vocab RDF file
    g = Graph().parse(sys.argv[1])

    # check expansion option
    expand = False
    if len(sys.argv) == 4:
        if sys.argv[2] == "-e":
            if sys.argv[3] == "true":
                expand = True

    if expand:
        # load the combined validator (inference + validation)
        s = Graph().parse(validators_dir / "combined.ttl")

        # validate, applying SHACL inferencing
        v = validate(g, shacl_graph=s, advanced=True)
    else:
        # load only the plain validator
        s = Graph().parse(validators_dir / "validator.ttl")

        # validate, without applying SHACL inferencing
        v = validate(g, shacl_graph=s)

    print(v[2])
