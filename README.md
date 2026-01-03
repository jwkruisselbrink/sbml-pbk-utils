# SBML PBK Utils

[![Licence](https://img.shields.io/github/license/jwkruisselbrink/sbml-pbk-utils)](https://github.com/jwkruisselbrink/sbml-pbk-utils/blob/main/LICENSE)
[![Build](https://img.shields.io/github/actions/workflow/status/jwkruisselbrink/sbml-pbk-utils/build.yml?label=build)](https://github.com/jwkruisselbrink/sbml-pbk-utils/actions/workflows/build.yml)
[![Unit-test](https://img.shields.io/github/actions/workflow/status/jwkruisselbrink/sbml-pbk-utils/unit-test.yml?label=unit-test)](https://github.com/jwkruisselbrink/sbml-pbk-utils/actions/workflows/unit-test.yml)

`sbmlpbkutils` is a small Python package that contains utility functions to aid in the development of PBK model implementations in SBML, compliant with the [FAIR PBK standard](https://fair-pbk.github.io/fair-pbk-standard). It provides functionality for annotating and validating SBML PBK models, generation of model summary reports, and for defining and running model simulation scenarios.

This package is currently being developed in an explorative manner to evaluate the use of SBML as a harmonized exchange format for FAIR PBK models. In its current state it should therefore be regarded as an experimental toolset.

## Main features

The package provides the following core functionalities:

- **[Model annotation](docs/annotation.md):** annotate SBML PBK models using a CSV annotations table (element id, unit, qualifier, URI) and Set model creators using a citations CFF file.
- **[Model validation](docs/validation.md):** run model-level checks (taxon/chemical annotations), compartment/species/parameter checks and unit consistency checks.
- **[Report generation](docs/reporting.md):** extract model overview (units, number of species, compartments, input routes), and element-level infos and generate Markdown summary reports.
For more information on use and examples, 
- **[Simulation](docs/simulation.md):** run PBK model simulation scenarios and compare model outputs against each other and against reference data.

Detailed usage instructions and examples are provided in the respective documentation sections.

## Installation

Given the experimental status of this package, there are currently no plans to publish it on PyPI. The package can be installed directly from GitHub using `pip`.

To install a specific version, use the version tag. For instance, for version `v0.34.0`, use:

````
pip install git+https://github.com/jwkruisselbrink/sbml-pbk-utils.git@v0.34.0
````

To install the latest version available on the main Git branch, type:

````
pip install git+https://github.com/jwkruisselbrink/sbml-pbk-utils.git@main
````

## About the development

This package is currently being developed in an explorative manner to evaluate the use of SBML as a harmonized exchange format for FAIR PBK models. It is developed in parallel with the [FAIR PBK standard](https://fair-pbk.github.io/fair-pbk-standard). The aim is to adopt and/or align with already existing initiatives as much as possible. 

In particular, this package uses and builds on the following main resources:

- Use of the [Systems Biology Markup Language (SBML)](https://sbml.org/) as a harmonized publication and exchange format for PBK models to bridge the gap between the various different model implementation languages that are currently used by PBK model developers.
- The [sbmlutils](https://github.com/matthiaskoenig/sbmlutils) Python package provides utilities for annotation of SBML models. It also serves as a major source of inspiration for this PBK utils package. The reason for creating a package specifically for PBK models is to include also tooling that is specifically tailored to the sub-domain of PBK models.
- The [libSBML](https://github.com/sbmlteam/python-libsbml) python package provides the essential functionality for manipulating SBML models. For instance, for enriching SBML model implementations with annotations, units and descriptions of the model elements.
- For (semantic) annotation of PBK models, the controlled vocabularies of the following ontologies are considered relevant:
  - Use of the [PBPK ontology](https://github.com/InSilicoVida-Research-Lab/pbpko) for annotation of all model elements (e.g., compartments, species, parameters).
  - Use of the [ChEBI](https://www.ebi.ac.uk/chebi/) ontology for associating PBK model elements with the chemical entities they represent.
  - Use of the [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy) for associating PBK models with the (classes of) animal species for which they are applicable.
  - Alignment with the [Unified Code for Units of Measure (UCUM)](https://ucum.org/) and the [QUDT Ontologies](https://qudt.org/) for annotation of units, combined with the facilities for specification of units available in SBML.
