# Model annotation

The `PbkModelAnnotator` class can be used to annotate the elements and units of an SBML PBK model implementation using a separate CSV file. Its implementation builds on the [sbmlutils](https://sbmlutils.readthedocs.io/en/latest/notebooks/sbml_annotator.html#Annotate-existing-model) package, but in addition to annotation of the model using RDF triples, it also sets the model units and element names.

The structure of the annotations CSV file is described below. For an example of an annotations file, see the [annotations file](https://github.com/rivm-syso/euromix-to-sbml/blob/main/model/euromix.annotations.csv) of the SBML EuroMix PBK model re-implementation.

## Example of use

The following code example shows how to annotate an SBML PBK model `model.sbml` with annotations provided in the file `annotations.csv`.

```python
from sbmlpbkutils import PbkModelAnnotator
from libsbml import readSBML, writeSBML

annotator = PbkModelAnnotator()
doc = readSBML('model.sbml')
annotator.annotate(doc, annotations_file='annotations.csv', cff_file=None)
# Save annotated model
writeSBML(doc, 'model.annotated.sbml')
```

## Annotations CSV file structure

The CSV file structure is based on the external annotations file format of [sbmlutils](https://sbmlutils.readthedocs.io/en/latest/notebooks/sbml_annotator.html#Annotate-existing-model), but extended to also facilitate specification of units.

Annotations CSV files should have have the following fields:

| Field           | Description                                              |
|-----------------|----------------------------------------------------------|
| element_id      | Identifier of the model element that is to be annotated. Use values `substanceUnits`, `extentUnits`, `timeUnits`, and `volumeUnits` with *sbml_type* `document` for specification of the model-level units. |
| sbml_type       | Type of the model element that is to be annotated. Options: `model`, `document`, `compartment`, `species`, `parameter`. |
| element_name    | For specification of the name of the model element. |
| unit            | For unit annotation: the unit associated with the model element. Units should be compliant with the synonyms of the [unit definitions](sbmlpbkutils/unit_definitions.py). This catalogue of unit definitions aims to align as much as possible with the [Unified Code for Units of Measure (UCUM)](https://ucum.org/) and the [QUDT Ontologies](https://qudt.org/). |
| annotation_type | For RDF annotation: type of the SBML term-annotation (default RDF). |
| qualifier       | For RDF annotation: [BioModels Qualifier](https://github.com/combine-org/combine-specifications/blob/main/specifications/qualifiers-1.1.md#model-qualifiers) of the annotation (RDF predicate). Model qualifier types: `BQM_IS`, `BQM_IS_DESCRIBED_BY`, `BQM_IS_DERIVED_FROM`, `BQM_IS_INSTANCE_OF`, `BQM_HAS_INSTANCE`. Biological qualifier types: `BQB_IS`, `BQB_HAS_PART`, `BQB_IS_PART_OF`, `BQB_IS_VERSION_OF`, `BQB_HAS_VERSION`, `BQB_IS_HOMOLOG_TO`, `BQB_IS_DESCRIBED_BY`, `BQB_IS_ENCODED_BY`, `BQB_ENCODES`, `BQB_OCCURS_IN`, `BQB_HAS_PROPERTY`, `BQB_IS_PROPERTY_OF`, `BQB_HAS_TAXON`. |
| URI             | For RDF annotation: annotation resource URI for the term-annotation (RDF object). |

## Generate an annotations template

The `AnnotationsTemplateGenerator` class can be used to generate a template CSV file for a provided SBML PBK model file, pre-filled with all model elements and, if available, other information from the model.

The example below shows how to run the template generator on a SBML PBK model file `model.sbml` to generate the annotations CSV file template `annotations-template.csv`:

```python
from sbmlpbkutils import AnnotationsTemplateGenerator
from libsbml import readSBML

doc = readSBML('model.sbml')
df = AnnotationsTemplateGenerator().generate(doc.getModel())
df.to_csv('annotations-template.csv', index=False)
```
