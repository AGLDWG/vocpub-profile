"""
This Python script reads the SHACL validator validator.ttl and the data expander expander.ttl and combines them into one
SHACL RDF file: expander.ttl

It also alters the IRI and the name of the combined validator and adds a scope note, to distinguish it from the
validator.ttl
"""

from pathlib import Path
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import SDO, SKOS

validators_dir = Path(__file__).parent.parent.absolute() / "validators"

g1 = Graph().parse(validators_dir / "validator.ttl")

g2 = Graph().parse(validators_dir / "expander.ttl")

g3 = g1 + g2

# create new IRI for this validator
original_validator_iri = URIRef("https://w3id.org/profile/vocpub/validator")
new_validator_iri = URIRef("https://w3id.org/profile/vocpub/validator-combined")
for p, o in g3.predicate_objects(original_validator_iri):
    g3.remove((original_validator_iri, p, o))
    g3.add((new_validator_iri, p, o))
for s, p in g3.subject_predicates(original_validator_iri):
    g3.remove((s, p, original_validator_iri))
    g3.add((s, p, new_validator_iri))

# update this validator's name
g3.remove((original_validator_iri, SDO.name, None))
g3.add((original_validator_iri, SDO.name, Literal("VocPub Combined Validator")))

# add a scopeNote to this validator
g3.add((
    new_validator_iri,
    SKOS.scopeNote,
    Literal("This validator applies a series of data expansion rules to a given data graph before validating it")
))

g3.serialize(destination=str(validators_dir / "validator-combined.ttl"), format="longturtle")
