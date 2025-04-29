# VocPub Profile
## How to validate

This document describes how you can use validators, such as the [VocPub Profile](https://linked.data.gov.au/def/vocpub)'s validator, to test whether data is valid according to it a specification.

Validation using SHACL validators involves applying a [SHACL](https://www.w3.org/TR/shacl/) validator file, such as [the one provided in this profile](https://linked.data.gov.au/def/vocpub/validator) to data using one of many available validator tools. Different approaches and tools are:

1. **Online validation**
    * [KurrawongAI's RDFTools](http://rdftools.dev.kurrawong.ai)
      * Pre-loaded with a number of validators, including [the one provided in this profile](https://linked.data.gov.au/def/vocpub/validator)
      * You can supply your own validator too
      * You can past in RDF data or upload a data file
    * [SHACL Playground](https://shacl.org/playground/)
        * Simply go to the web page, copy the validator file's contents into the _Shapes Graph_ text box and your target data into the _Data Graph_ text box and hit the "Update" button! The tool will present any errors found to you on screen.
3. **Command line validation**
    * [pySHACL](https://github.com/RDFLib/pySHACL)
        * This is a Python tool that can run as a desktop command line application - see it's docs
    * [Jena's SHACL](https://jena.apache.org/documentation/shacl/index.html)
        * the SHACL implementation within the Java-based Jena RDF toolkit
        * presented as a command line application and also as a Java library
4. **Integrated application validation**
    * use pySHACL or Jena's SHACL tooling within your own scripts or programs
    * See pySHACL's & Jena's documentation

## Expanded data option

This profile provides two options for validation: 

* validation of present data
    * standard validation of data using `validator.ttl`
* validation of expanded data
    * validation of data after it has been expanded with the rules in `expander.ttl`

The KurrawongAI RDFTools system provides allows selection of either option