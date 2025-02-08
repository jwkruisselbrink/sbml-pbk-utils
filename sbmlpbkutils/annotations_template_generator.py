import libsbml as ls
import pandas as pd

from . import PbkModelAnnotator
from . import term_definitions
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

    def generate(self, model: ls.Model, try_fill: bool = True):
        """Generates an annotations data table 
        file and write results to the specified out file."""
        dt = []
        dt_model = self.get_document_level_terms(model)
        dt.extend(dt_model)
        dt_compartments = self.get_compartment_terms(model, try_fill)
        dt.extend(dt_compartments)
        dt_species = self.get_species_terms(model, try_fill)
        dt.extend(dt_species)
        dt_parameters = self.get_parameter_terms(model, try_fill)
        dt.extend(dt_parameters)
        terms = pd.DataFrame(
            dt,
            columns=["element_id", "sbml_type", "element_name", "unit", "annotation_type", "qualifier", "URI", "remark"]
        )
        return terms

    def get_document_level_terms(self, model: ls.Model):
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

    def get_compartment_terms(self, model, try_fill):
        element_type="compartment"
        required_qualifiers = ['BQM_IS']
        dt = []
        for i in range(0,model.getNumCompartments()):
            element = model.getCompartment(i)
            element_terms = self._get_element_terms(element, element_type, required_qualifiers, try_fill)
            dt.extend(element_terms)
        return dt

    def get_species_terms(
        self,
        model,
        try_fill
    ):
        element_type="species"
        required_qualifiers = ['BQM_IS', 'BQB_IS']
        dt = []
        for i in range(0,model.getNumSpecies()):
            element = model.getSpecies(i)
            element_terms = self._get_element_terms(element, element_type, required_qualifiers, try_fill)
            dt.extend(element_terms)
        return dt

    def get_parameter_terms(
        self,
        model,
        try_fill: bool
    ) -> list[str]:
        element_type="parameter"
        required_qualifiers = ['BQM_IS', 'BQB_IS']
        dt = []
        for i in range(0,model.getNumParameters()):
            element = model.getParameter(i)
            element_terms = self._get_element_terms(element, element_type, required_qualifiers, try_fill)
            dt.extend(element_terms)
        return dt

    def _get_element_terms(
        self,
        element: ls.SBase,
        element_type: str,
        required_qualifiers: list[str],
        try_fill: bool
    ) -> list[str]:
        dt = []
        name = element.getName()

        # Try to find matching term definition for element
        matched_term = self.find_term_definition(element, element_type)
        matched_term_resources = None
        if (matched_term is not None):
            if try_fill and 'name' in matched_term.keys():
                name = matched_term['name']
            if 'resources' in matched_term.keys() and len(matched_term['resources']) > 0:
                matched_term_resources = matched_term['resources']

        rows = 0

        for qualifierDefinition in _qualifier_definitions:
            qualifier = qualifierDefinition['qualifier']
            qualifier_type = qualifierDefinition['type']
            qualifier_id = qualifierDefinition['id']

            # Get current URIs defined in the model for this qualifier
            resources = PbkModelAnnotator.get_cv_terms(element, qualifier_type, qualifier)
            uris = [resource['uri'] for resource in resources]

            # Add URIs from matched term-definition
            if (try_fill and matched_term_resources is not None):
                for resource in matched_term_resources:
                    if (resource['qualifier'] == qualifier_id):
                        uri = resource['URI']
                        if (uri not in uris):
                            uris.append(uri)

            # If no resource URIs were found for this qualifier, but it is a required
            # qualifier, then add an empty record
            if (len(uris) == 0 and qualifier_id in required_qualifiers):
                uris = ['']

            for uri in uris:
                dt.append([
                    element.getId(),
                    element_type,
                    (name if rows == 0 else ''),
                    (get_ucum_unit_string(element.getUnits()) if rows == 0 else ''),
                    "rdf",
                    qualifier_id,
                    uri,
                    ""
                ])
                rows += 1

        return dt

    def find_term_definition(
        self,
        element: ls.SBase,
        element_type: str
    ):
        """Tries to find a resource definition for the specified element."""
        element_id = element.getId()
        for index, value in enumerate(term_definitions):
            if value['element_type'] == element_type:
                if 'recommended_id' in value.keys() \
                    and element_id.lower() == value['recommended_id'].lower():
                    return value
                elif 'common_identifiers' in value.keys() \
                    and any(element_id.lower() == val.lower() for val in value['common_identifiers']):
                    return value
        return None
