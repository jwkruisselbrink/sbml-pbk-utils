import libsbml as ls
import pandas as pd
from . import TermDefinitions
from . import UnitDefinitions

class AnnotationsTemplateGenerator:

    def generate(self, model):
        dt = []
        dt_model = self.get_document_level_terms(model)
        dt.extend(dt_model)
        dt_compartments = self.get_compartment_terms(model)
        dt.extend(dt_compartments)
        dt_species = self.get_species_terms(model)
        dt.extend(dt_species)
        dt_parameters = self.get_parameter_terms(model)
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

    def get_compartment_terms(self, model):
        element_type="compartment"
        dt = []
        for i in range(0,model.getNumCompartments()):
            element = model.getCompartment(i)

            name = element.getName()
            description = ''
            qualifier = ''
            uri = self.get_term(element)

            # Try to find resource definition for element
            resource = self.get_resource_definition(element, element_type)
            if (resource is not None):
                if 'name' in resource.keys():
                    name = resource['name']
                if 'description' in resource.keys():
                    description = resource['description']
                if 'resources' in resource.keys() and len(resource['resources']) > 0:
                    qualifier = resource['resources'][0]['qualifier']
                    uri = resource['resources'][0]['URI']

            dt.append([
                element.getId(),
                element_type,
                name,
                self.get_unit_string(element.getUnits()),
                "rdf",
                qualifier,
                uri,
                description,
                ""
            ])
        return dt

    def get_species_terms(self, model):
        element_type="species"
        dt = []
        for i in range(0,model.getNumSpecies()):
            element = model.getSpecies(i)

            name = element.getName()
            description = ''
            qualifier = ''
            uri = self.get_term(element)

            # Try to find resource definition for element
            resource = self.get_resource_definition(element, element_type)
            if (resource is not None):
                if 'name' in resource.keys():
                    name = resource['name']
                if 'description' in resource.keys():
                    description = resource['description']
                if 'resources' in resource.keys() and len(resource['resources']) > 0:
                    qualifier = resource['resources'][0]['qualifier']
                    uri = resource['resources'][0]['URI']

            dt.append([
                element.getId(),
                element_type,
                name,
                self.get_unit_string(element.getUnits()),
                "rdf",
                qualifier,
                uri,
                description,
                ""
            ])
        return dt

    def get_parameter_terms(self, model):
        element_type="parameter"
        dt = []
        for i in range(0,model.getNumParameters()):
            element = model.getParameter(i)

            name = element.getName()
            description = ''
            qualifier = ''
            uri = self.get_term(element)

            # Try to find resource definition for element
            resource = self.get_resource_definition(element, element_type)
            if (resource is not None):
                if 'name' in resource.keys():
                    name = resource['name']
                if 'description' in resource.keys():
                    description = resource['description']
                if 'resources' in resource.keys() and len(resource['resources']) > 0:
                    qualifier = resource['resources'][0]['qualifier']
                    uri = resource['resources'][0]['URI']

            dt.append([
                element.getId(),
                element_type,
                name,
                self.get_unit_string(element.getUnits()),
                "rdf",
                qualifier,
                uri,
                description,
                ""
            ])
        return dt

    def get_resource_definition(self, element, element_type):
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

    def get_term(self, element):
        """Helper function to extract is-a resource URI."""
        cvTerms = element.getCVTerms()
        if cvTerms:
            # Check if there already is an annotation for the element
            for term in cvTerms:
                num_resources = term.getNumResources()
                for j in range(num_resources):
                    if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER and \
                        term.getBiologicalQualifierType() == ls.BQB_IS:
                        return term.getResourceURI(j)

        return None 
