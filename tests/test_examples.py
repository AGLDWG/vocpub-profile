from pathlib import Path
from pyshacl import validate
from rdflib import Graph

EG_DIR = Path(__file__).parent.parent.resolve() / "examples"
VALIDATORS_DIR = Path(__file__).parent.parent.resolve() / "validators"

def test_examples():
    for f in sorted(list(EG_DIR.glob("*.ttl"))):
        validity = False if "invalid" in str(f.name) else True

        if "GA" in str(f.name):
            validator = VALIDATORS_DIR / "validator.ga.ttl"
        elif "multilang" in str(f.name):
            validator = VALIDATORS_DIR / "validator.multilang.ttl"
        else:
            validator = VALIDATORS_DIR / "validator.ttl"

        data_g = Graph().parse(f)
        validator_g = Graph().parse(validator)

        if "build" in str(f.name):
            validator_g.parse(VALIDATORS_DIR / "expander.ttl")

        v = validate(data_g, shacl_graph=validator_g, allow_warnings=True, advanced=True)
        assert v[0] == validity, print(f.name)