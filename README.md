# SBML PBK Utils

The `sbmlpbkutils` package is a small Python package that contains utility functions for FAIR PBK model implementation in SBML. It provides a number of utility functions and classes for annotating, validating and running SBML PBK models. It is currently being developed in an explorative manner to evaluate the use of SBML as a harmonized exchange format for FAIR PBK models, and to develop and test a strategy/standard for annotation of terms and units specifically for PBK models. In its current state it should therefore be regarded as an experimental toolset.

## Installation

### Install from GitHub

To install the latest version available on the main GitHub branch type:

````
pip install git+https://github.com/jwkruisselbrink/sbml-pbk-utils.git@main
````

To install a specific version, use the version tag. For instance, for version `v0.2.0`, use:

````
pip install git+https://github.com/jwkruisselbrink/sbml-pbk-utils.git@v0.2.0
````

Given the experimental nature of this package, there currently no plans to publish it on PyPI.

## Using this package

### SBML model annotation

The [PbkModelAnnotator](sbmlpbkutils/pbk_model_annotator.py) class can be used to annotate the elements and units of a PBK model implementation in SBML using a separate CSV file. This class is based on, and uses parts of, the annotation script of [SBMLutils](https://sbmlutils.readthedocs.io/en/latest/notebooks/sbml_annotator.html#Annotate-existing-model). However, in addition to annotation of the model using RDF triples, it also sets the model units and element names. 

```python
from sbmlpbkutils import PbkModelAnnotator

# Create a new annotator instance
annotator = PbkModelAnnotator()

# Annotate the SBML file using the annotations CSV file
# and write annotated SBML to specified output file
annotator.annotate(
  'path/to/sbml_file.xml',
  'path/to/annotations_file.csv',
  'path/to/annotated_sbml_file.xml'
)
```

The structure of the CSV file is also based on the external annotations file format of [SBMLutils](https://sbmlutils.readthedocs.io/en/latest/notebooks/sbml_annotator.html#Annotate-existing-model), but again with some changes to also allow for annotation of units.

| Field           | Description                                              |
|-----------------|----------------------------------------------------------|
| element_id      | Identifier of the model element that is to be annotated. |
| sbml_type       | Type of the model element that is to be annotated. Options: `model`, `document`, `compartment`, `species`, `parameter`. |
| element_name    | For specification of element name: the name of the model element. |
| unit            | For unit annotation: the unit associated with the model element. Units should be compliant with the synonyms of the [unit definitions](src/unit_definitions.py). This catalogue of unit definitions aims to align as much as possible with the [Unified Code for Units of Measure (UCUM)](https://ucum.org/) and the [QUDT Ontologies](https://qudt.org/). |
| annotation_type | For RDF annotation: type of the SBML term-annotation (default RDF). |
| qualifier       | For RDF annotation: [BioModels Qualifier](https://github.com/combine-org/combine-specifications/blob/main/specifications/qualifiers-1.1.md#model-qualifiers) of the annotation (RDF predicate). Model qualifier types: `BQM_IS`, `BQM_IS_DESCRIBED_BY`, `BQM_IS_DERIVED_FROM`, `BQM_IS_INSTANCE_OF`, `BQM_HAS_INSTANCE`. Biological qualifier types: `BQB_IS`, `BQB_HAS_PART`, `BQB_IS_PART_OF`, `BQB_IS_VERSION_OF`, `BQB_HAS_VERSION`, `BQB_IS_HOMOLOG_TO`, `BQB_IS_DESCRIBED_BY`, `BQB_IS_ENCODED_BY`, `BQB_ENCODES`, `BQB_OCCURS_IN`, `BQB_HAS_PROPERTY`, `BQB_IS_PROPERTY_OF`, `BQB_HAS_TAXON`. |
| URI             | For RDF annotation: annotation resource URI for the term-annotation (RDF object). The [term definitions](src/term_definitions.py) file contains definitions of commonly used model terms, together with recommended resource URIs. This file is still under construction, but is intended to align with a common, harmonized annotation standard for PBK models. It is planned to include resources URIs from the [PBPK ontology](https://github.com/Crispae/pbpko/tree/main) in the near future. |

For specification of the SBML model global substance unit, time unit, and volume unit, use **element_id** values of *substanceUnits*, *timeUnits*, and *volumeUnits* with **sbml_type** *document*.

For an example of an annotations file, see the [annotations file](https://github.com/rivm-syso/euromix-to-sbml/blob/main/model/euromix.annotations.csv) of the SBML EuroMix PBK model re-implementation.

### SBML validation

Having a harmonized standard for implementation of PBK models allows for various types of automated tooling. Automatic validation can be included to check for model errors, model consistency, consitency of units, and also on more PBK-model specific aspects (such as mass balance). The [PbkModelValidator](sbmlpbkutils/pbk_model_validator.py) class provides functionality to run validation checks on PBK model implementations in SBML.

```python
from sbmlpbkutils import PbkModelValidator

# Create a new validator instance
validator = PbkModelValidator(True)

# Validate the annotated SBML PBK model implementation
validator.validate('path/to/sbml_file.xml')
```

This is a first version in which some rudimentary file and consistency checks are performed. The validation report is printed to the console. This first version is inspired by the [example](https://synonym.caltech.edu/software/libsbml/5.18.0/docs/formatted/python-api/validate_s_b_m_l_8py-example.html) presented in the libSBML documentation.

- Every compartment should have a BQM_IS annotation linking associating the compartment with a known compartment of the PBPK ontology.
- Every parameter should have a BQM_IS annotation linking associating the compartment with a known parameter of the PBPK ontology.
- Pyhisical compartments should have a BQB_IS annotation linking associating the compartment with a biological entity (organ, tissue, body fluid) of the UBERON ontology.

## About the development

As mentioned, this pacakage is currently being developed in an explorative manner to evaluate the use of SBML as a harmonized exchange format for FAIR PBK models, and to develop and test a strategy/standard for annotation of terms and units specifically for PBK models. The aim is to adopt and/or align with already existing initiatives as much as possible.

At present, the following elements are considered essential elements for building up a standard for FAIR PBK modelling:

- Use of the [Systems Biology Markup Language (SBML)](https://sbml.org/) as a harmonized publication and exchange format for PBK models, which should bridge the gap between the various different model implementation languages that are currently used by PBK model developers.
- The [SBMLutils](https://github.com/matthiaskoenig/sbmlutils) Python package provides convenient utilities for manipulation and annotation of SBML models. It also serves as a major source of inspiration for this PBK utils package. The reason for creating a package specifically for PBK models is to include also tooling that is specifically tailored to the sub-domain of PBK models.
- The [libSBML](https://github.com/sbmlteam/python-libsbml) python package provides the essential functionality for manipulating SBML models. For instance, for enriching SBML model implementations with annotations, units and descriptions of the model elements.
- For (semantic) annotation of PBK models, the controlled vocabularies of the following ontologies are considered relevant:
  - Use of the (currently being developed) [PBPK ontology](https://github.com/Crispae/pbpko/tree/main) for annotation of all model elements (e.g., compartments, species, parameters).
  - Alignment with the [Unified Code for Units of Measure (UCUM)](https://ucum.org/) and the [QUDT Ontologies](https://qudt.org/) for annotation of units, combined with the facilities for specification of units available in SBML.
  - Use of the [UBERON](https://obophenotype.github.io/uberon/about/) ontology for relating PBK model compartments to the biological entities they represent.
