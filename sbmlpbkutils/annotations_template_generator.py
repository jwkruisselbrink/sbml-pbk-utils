import pandas as pd
import libsbml as ls

from . import PbkModelAnnotator
from . import get_ucum_unit_string

_qualifier_definitions = [
    {
        "id": "BQM_IS",
        "qualifier": ls.BQM_IS,
        "type": ls.MODEL_QUALIFIER
    },
    {
        "id": "BQM_IS_DESCRIBED_BY",
        "qualifier": ls.BQM_IS_DESCRIBED_BY,
        "type": ls.MODEL_QUALIFIER
    },
    {
        "id": "BQM_IS_DERIVED_FROM",
        "qualifier": ls.BQM_IS_DERIVED_FROM,
        "type": ls.MODEL_QUALIFIER
    },
    {
        "id": "BQM_IS_INSTANCE_OF",
        "qualifier": ls.BQM_IS_INSTANCE_OF,
        "type": ls.MODEL_QUALIFIER
    },
    {
        "id": "BQM_HAS_INSTANCE",
        "qualifier": ls.BQM_HAS_INSTANCE,
        "type": ls.MODEL_QUALIFIER
    },
    {
        "id": "BQM_UNKNOWN",
        "qualifier": ls.BQM_UNKNOWN,
        "type": ls.MODEL_QUALIFIER
    },
    {
        "id": "BQB_IS",
        "qualifier": ls.BQB_IS,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_HAS_PART",
        "qualifier": ls.BQB_HAS_PART,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_IS_PART_OF",
        "qualifier": ls.BQB_IS_PART_OF,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_IS_VERSION_OF",
        "qualifier": ls.BQB_IS_VERSION_OF,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_HAS_VERSION",
        "qualifier": ls.BQB_HAS_VERSION,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_IS_HOMOLOG_TO",
        "qualifier": ls.BQB_IS_HOMOLOG_TO,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_IS_DESCRIBED_BY",
        "qualifier": ls.BQB_IS_DESCRIBED_BY,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_IS_ENCODED_BY",
        "qualifier": ls.BQB_IS_ENCODED_BY,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_ENCODES",
        "qualifier": ls.BQB_ENCODES,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_OCCURS_IN",
        "qualifier": ls.BQB_OCCURS_IN,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_HAS_PROPERTY",
        "qualifier": ls.BQB_HAS_PROPERTY,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_IS_PROPERTY_OF",
        "qualifier": ls.BQB_IS_PROPERTY_OF,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_HAS_TAXON",
        "qualifier": ls.BQB_HAS_TAXON,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_UNKNOWN",
        "qualifier": ls.BQB_UNKNOWN,
        "type": ls.BIOLOGICAL_QUALIFIER
    }
]

class AnnotationsTemplateGenerator:

    def generate(
        self,
        model: ls.Model
    ):
        """Generates an annotations data table 
        file and write results to the specified out file."""
        dt = []
        dt_doc = self._get_document_level_terms(model)
        dt.extend(dt_doc)
        dt_model = self._get_model_level_terms(model)
        dt.extend(dt_model)
        dt_compartments = self._get_compartment_terms(model)
        dt.extend(dt_compartments)
        dt_species = self._get_species_terms(model)
        dt.extend(dt_species)
        dt_parameters = self._get_parameter_terms(model)
        dt.extend(dt_parameters)
        terms = pd.DataFrame(
            dt,
            columns=[
                "element_id",
                "sbml_type",
                "element_name",
                "unit",
                "annotation_type",
                "qualifier",
                "URI",
                "remark"
            ]
        )
        return terms

    def _get_document_level_terms(
        self,
        model: ls.Model
    ) -> list[str]:
        element_type="document"
        dt = []
        dt.append([
            "substanceUnits",
            element_type,
            "model substances unit",
            get_ucum_unit_string(model.getSubstanceUnits()),
            "",
            "",
            "",
            ""
        ])
        dt.append([
            "extentUnits",
            element_type,
            "model extent unit",
            get_ucum_unit_string(model.getExtentUnits()),
            "",
            "",
            "",
            ""
        ])
        dt.append([
            "timeUnits",
            element_type,
            "model time unit",
            get_ucum_unit_string(model.getTimeUnits()),
            "",
            "",
            "",
            ""
        ])
        dt.append([
            "volumeUnits",
            element_type,
            "model volume unit",
            get_ucum_unit_string(model.getVolumeUnits()),
            "",
            "",
            "",
            ""
        ])
        return dt

    def _get_model_level_terms(
        self,
        model: ls.Model
    ):
        element_type="model"
        dt = []
        required_qualifiers = ['BQB_HAS_PROPERTY', 'BQB_HAS_TAXON']
        element_terms = self._get_element_terms(
            model,
            element_type,
            required_qualifiers
        )
        dt.extend(element_terms)
        return dt

    def _get_compartment_terms(
        self,
        model: ls.Model
    ) -> list[str]:
        element_type="compartment"
        required_qualifiers = ['BQM_IS']
        dt = []
        for i in range(0,model.getNumCompartments()):
            element = model.getCompartment(i)
            element_terms = self._get_element_terms(
                element,
                element_type,
                required_qualifiers
            )
            dt.extend(element_terms)
        return dt

    def _get_species_terms(
        self,
        model: ls.Model
    ) -> list[str]:
        element_type="species"
        required_qualifiers = ['BQM_IS', 'BQB_IS']
        dt = []
        for i in range(0,model.getNumSpecies()):
            element = model.getSpecies(i)
            element_terms = self._get_element_terms(
                element,
                element_type,
                required_qualifiers
            )
            dt.extend(element_terms)
        return dt

    def _get_parameter_terms(
        self,
        model: ls.Model
    ) -> list[str]:
        element_type="parameter"
        required_qualifiers = ['BQM_IS', 'BQB_IS']
        dt = []
        for i in range(0,model.getNumParameters()):
            element = model.getParameter(i)
            element_terms = self._get_element_terms(
                element,
                element_type,
                required_qualifiers
            )
            dt.extend(element_terms)
        return dt

    def _get_element_terms(
        self,
        element: ls.SBase,
        element_type: str,
        required_qualifiers: list[str]
    ) -> list[str]:
        dt = []
        name = element.getName()

        rows = 0
        for qualifier_def in _qualifier_definitions:
            qualifier = qualifier_def['qualifier']
            qualifier_type = qualifier_def['type']
            qualifier_id = qualifier_def['id']

            # Get current URIs defined in the model for this qualifier
            resources = PbkModelAnnotator.get_cv_terms(element, qualifier_type, qualifier)
            uris = [resource['uri'] for resource in resources]

            # If no resource URIs were found for this qualifier, but it is a required
            # qualifier, then add an empty record
            if (len(uris) == 0 and qualifier_id in required_qualifiers):
                uris = ['']

            unit_str = (get_ucum_unit_string(element.getUnits())
                if isinstance(element, (ls.Compartment, ls.Species, ls.Parameter))
                else ''
            )
            for uri in uris:
                dt.append([
                    element.getId(),
                    element_type,
                    (name if rows == 0 else ''),
                    (unit_str if rows == 0 else ''),
                    "rdf",
                    qualifier_id,
                    uri,
                    ""
                ])
                rows += 1

        return dt
