---
name: vocpub-validity
description: Update RDF skos:ConceptScheme files to satisfy the VocPub Profile, applying the maintained predicate and IRI replacements and checking for SHACL Violations with the VocPub validator. Use when asked for VocPub validity or conformance fixes.
---

# VocPub Validity

Update the requested skos:ConceptScheme files so that validation against the VocPub Profile ShapesGraph at <https://linked.data.gov.au/def/vocpub/validator> produces no results with severity `sh:Violation`.

## Maintained actions

### 1. Replace predicates

Apply these mappings to predicates in the requested vocabulary files. Resolve prefixes to full IRIs; do not replace matching text inside literals or change subject/object IRIs under this action.

```yaml
dcterms:contributor: schema:contributor
dcterms:created: schema:dateCreated
dcterms:creator: schema:creator
dcterms:description: schema:description
dcterms:isFormatOf: prof:wasDerivedFrom
dcterms:license: schema:license
dcterms:modified: schema:dateModified
dcterms:publisher: schema:publisher
dcterms:rights: schema:copyrightNotice
dcterms:source: schema:citation
```

Namespaces:

- `dcterms:` — `http://purl.org/dc/terms/`
- `schema:` — `https://schema.org/`
- `prof:` — `http://www.w3.org/ns/dx/prof/`

These mappings preserve the user's supplied terms. `prof:wasDerivedFrom` may have been intended as `prov:wasDerivedFrom`. Check this against the validator and flag any discrepancy; do not silently substitute a different mapping. Ask for clarification if resolving the discrepancy requires changing the maintained action.

### 2. Replace the licence IRI

Replace the exact RDF IRI:

```text
http://creativecommons.org/licences/by/4.0
```

with:

```text
http://purl.org/NET/rdflicense/cc-by4.0
```

Match RDF IRI terms wherever they occur in the requested files, including prefixed representations of the same IRI. Do not alter literal text or assume other spellings, protocols, or trailing-slash variants are included.

### 3. Establish top concepts and complete reciprocal links

Before completing reciprocal links, check that the object of every `skos:hasTopConcept` statement and the subject of every `skos:topConceptOf` statement is a `skos:Concept`, not a `skos:Collection` or `skos:OrderedCollection`. Do not propagate invalid links or add Concept typing to a Collection to make validation pass. Report invalid or unverified endpoints and recommend a repair supported by the vocabulary; do not guess a replacement.

For each valid `concept skos:topConceptOf scheme` statement, add the missing `scheme skos:hasTopConcept concept` statement. Conversely, for each valid `scheme skos:hasTopConcept concept` statement, add the missing `concept skos:topConceptOf scheme` statement. Preserve existing links and avoid duplicates. Apply this per scheme.

After adding local `rdfs:isDefinedBy` links in action 4, apply the Soil Profile rule: for every `skos:Concept` explicitly defined by a ConceptScheme via `rdfs:isDefinedBy` and having no `skos:broader` values, add `skos:topConceptOf` pointing to that scheme and the reciprocal `skos:hasTopConcept` link. Exclude Collections and OrderedCollections, even if also typed as Concepts. Preserve existing hierarchy links and avoid duplicates. Do not select Concepts merely because they occur in the file or belong to a scheme; require the defining-scheme link.

### 4. Link local Concepts and Collections to their defining scheme

For every `skos:Concept` and `skos:Collection` (including `skos:OrderedCollection`) whose IRI is within the ConceptScheme's namespace, add `rdfs:isDefinedBy` with that ConceptScheme as its object, unless the triple already exists. Use the standard case-sensitive predicate `rdfs:isDefinedBy` (`http://www.w3.org/2000/01/rdf-schema#isDefinedBy`); the original request's `rdfs:isDefinedby` is a spelling error.

Determine the scheme's namespace from the vocabulary's namespace declarations and IRI structure, respecting path or fragment boundaries. Sharing a host or a broad parent prefix alone does not establish a shared namespace. Exclude external Concepts and Collections. When multiple schemes are present, use existing scheme membership and namespace evidence to select the defining scheme; flag ambiguous cases rather than inventing an association. Preserve existing statements.

### 5. Record the conformance update

Only after the required validation has completed with zero `sh:Violation` results, add a `skos:changeNote` to each updated `skos:ConceptScheme` with the literal text `{YEAR}-{MONTH}-{DAY}: Updated to be VocPub conformant`. Resolve `{YEAR}`, `{MONTH}`, and `{DAY}` at execution time using the user's local date, with a four-digit year, two-digit month, and two-digit day (YYYY-MM-DD). Preserve historical change notes and avoid adding an identical note twice. Do not add a conformance note when validation fails or cannot run. After adding the note, reformat and revalidate the final file. If that validation fails, remove the note added by this run and reformat and revalidate again; report the remaining issues without claiming conformance.

### 6. Update the modification date

Set `schema:dateModified` on each updated `skos:ConceptScheme` to today's date at execution time in the user's local timezone. Use an `xsd:date` literal in YYYY-MM-DD form, replacing the previous modification date rather than appending a competing value. Add the property if absent. Do not hard-code the date when this skill was written or alter `schema:dateCreated`.

### 7. Add local Collection membership

For every local `skos:Collection` (including `skos:OrderedCollection`), add `skos:inScheme` pointing to its ConceptScheme if the triple is missing. Use the namespace and scheme-selection rules in action 4. Preserve existing membership and do not assign external Collections to the local scheme.

## Apply and validate

- Limit edits to the requested vocabulary files. Preserve unrelated statements, literal values, language tags, and datatypes. Update prefix declarations as needed.
- The maintained actions are an initial, extensible list, not proof of conformance. Inspect remaining validation results and fix issues within the requested scope where the correct repair is established. Apart from the execution-date metadata explicitly required above, do not invent missing creators, dates, licences, or other metadata; request missing facts when necessary.
- For every created or modified `.ttl` file, use the installed `turtle-format` skill and run `kurra file reformat "path/to/file.ttl"` after the last edit. If formatting fails or kurra is unavailable, report that blocker.
- After executing the maintained rules other than the conditional conformance note and formatting, test every target file using this required command, replacing `{TARGET-FILE}` with its path:

  ```sh
  kurra shacl validate "{TARGET-FILE}" --shacl "https://linked.data.gov.au/def/vocpub/validator"
  ```

- Inspect the validation report rather than relying on the process exit code alone. Success means zero `sh:Violation` results. Report warnings and informational results separately; do not confuse them with Violations. If any validity issues remain, display recommendations for additional updates, identifying the affected resources, failed constraints, and concrete proposed repairs or missing information. Re-run the required command after any further edits and formatting.
- For final reporting, if more than 20 `sh:Violation` results remain, use kurra's SHACL results summary mode:

  ```sh
  kurra shacl validate "{TARGET-FILE}" --shacl "https://linked.data.gov.au/def/vocpub/validator" -y
  ```

  Present the summary and recommendations grouped by failed constraint rather than listing every result. Consult detailed results as needed to identify affected resources and propose concrete repairs. For 20 or fewer Violations, report the remaining issues directly.
- Summarize changed files, replacements, validation outcome, and unresolved issues. If the ShapesGraph cannot be retrieved or validation cannot run, state that conformance remains unverified.

Extend the maintained actions when the user provides additional rules.
