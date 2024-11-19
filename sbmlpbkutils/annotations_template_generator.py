import libsbml as ls
import pandas as pd

from sbmlpbkutils.pbk_model_annotator import PbkModelAnnotator
from . import TermDefinitions
from . import UnitDefinitions
from . import QualifierDefinitions

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
            columns=["element_id", "sbml_type", "element_name", "unit", "annotation_type", "qualifier", "URI", "description", "remark"]
        )
        return terms

    def get_document_level_terms(self, model):
        element_type="document"
        dt = []
        dt.append([
            "substanceUnits",
            element_type,
            "model substances unit",
            self.get_unit_string(model.getSubstanceUnits()),
            "",
            "",
            "",
            "Model substances unit.",
            ""
        ])
        dt.append([
            "timeUnits",
            element_type,
            "model time unit",
            self.get_unit_string(model.getTimeUnits()),
            "",
            "",
            "",
            "Model time unit.",
            ""
        ])
        dt.append([
            "volumeUnits",
            element_type,
            "model volume unit",
            self.get_unit_string(model.getVolumeUnits()),
            "",
            "",
            "",
            "Model volume unit.",
            ""
        ])
        return dt

    def get_compartment_terms(self, model, try_fill):
        element_type="compartment"
        required_qualifiers = ['BQM_IS', 'BQB_IS']
        dt = []
        for i in range(0,model.getNumCompartments()):
            element = model.getCompartment(i)
            element_terms = self.get_element_terms(element, element_type, required_qualifiers, try_fill)
            dt.extend(element_terms)
        return dt

    def get_species_terms(self, model, try_fill):
        element_type="species"
        required_qualifiers = ['BQM_IS']
        dt = []
        for i in range(0,model.getNumSpecies()):
            element = model.getSpecies(i)
            element_terms = self.get_element_terms(element, element_type, required_qualifiers, try_fill)
            dt.extend(element_terms)
        return dt

    def get_parameter_terms(self, model, try_fill):
        element_type="parameter"
        required_qualifiers = ['BQM_IS']
        dt = []
        for i in range(0,model.getNumParameters()):
            element = model.getParameter(i)
            element_terms = self.get_element_terms(element, element_type, required_qualifiers, try_fill)
            dt.extend(element_terms)
        return dt

    def get_element_terms(self, element, element_type, required_qualifiers, try_fill):
        dt = []
        name = element.getName()
        description = ''

        # Try to find matching term definition for element
        matched_term = self.find_term_definition(element, element_type)
        matched_term_resources = None
        if (matched_term is not None):
            if try_fill and 'name' in matched_term.keys():
                name = matched_term['name']
            if try_fill and'description' in matched_term.keys():
                description = matched_term['description']
            if 'resources' in matched_term.keys() and len(matched_term['resources']) > 0:
                matched_term_resources = matched_term['resources']

        rows = 0

        for qualifierDefinition in QualifierDefinitions:
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
                    (self.get_unit_string(element.getUnits()) if rows == 0 else ''),
                    "rdf",
                    qualifier_id,
                    uri,
                    (description if rows == 0 else ''),
                    ""
                ])
                rows += 1

        return dt

    def find_term_definition(self, element, element_type):
        """Tries to find a resource definition for the specified element."""
        element_id = element.getId()
        for index, value in enumerate(TermDefinitions):
            if value['element_type'] == element_type:
                if 'recommended_id' in value.keys() \
                    and element_id.lower() == value['recommended_id'].lower():
                    return value
                elif 'common_ids' in value.keys() \
                    and any(element_id.lower() == val.lower() for val in value['common_ids']):
                    return value
        return None

    def get_unit_string(self, unit):
        """Tries to get the (UCUM formated) unit string of the specified element."""
        if (unit):
            for index, value in enumerate(UnitDefinitions):
                if unit.lower() == value['id'].lower() \
                    or any(val.lower() == unit.lower() for val in value['synonyms']):
                    return value['UCUM'] if value['UCUM'] else value['id']
        return ""
