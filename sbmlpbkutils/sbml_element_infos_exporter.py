import libsbml as ls
import pandas as pd
from . import TermDefinitions
from . import UnitDefinitions

class SbmlElementInfosExporter:

    def exportTerms(self, model):
        dt = []
        dt_model = self.getDocumentTerms(model)
        dt.extend(dt_model)
        dt_compartments = self.getCompartmentTerms(model)
        dt.extend(dt_compartments)
        dt_species = self.getSpeciesTerms(model)
        dt.extend(dt_species)
        dt_parameters = self.getParameterTerms(model)
        dt.extend(dt_parameters)
        terms = pd.DataFrame(
            dt,
            columns=["element_id", "sbml_type", "element_name", "unit", "URI", "description", "remark"]
        )
        return terms
    
    def getDocumentTerms(self, model):
        element_type="document"
        dt = []
        dt.append([
            "substanceUnits",
            element_type,
            "model substances unit",
            self.getUnitString(model.getSubstanceUnits()),
            "",
            "Model substances unit.",
            ""
        ])
        dt.append([
            "timeUnits",
            element_type,
            "model time unit",
            self.getUnitString(model.getTimeUnits()),
            "",
            "Model time unit.",
            ""
        ])
        dt.append([
            "volumeUnits",
            element_type,
            "model volume unit",
            self.getUnitString(model.getVolumeUnits()),
            "",
            "Model volume unit.",
            ""
        ])
        return dt

    def getCompartmentTerms(self, model):
        element_type="compartment"
        dt = []
        for i in range(0,model.getNumCompartments()):
            element = model.getCompartment(i)

            name = element.getName()
            description = ''
            uri = self.getTerm(element)

            # Try to find resource definition for element
            resource = self.getResourceDefinition(element, element_type)
            if (resource is not None):
                if 'resources' in resource.keys() and len(resource['resources']) > 0:
                    uri = resource['resources'][0]['URI']
                if 'name' in resource.keys():
                    name = resource['name']
                if 'description' in resource.keys():
                    description = resource['description']

            dt.append([
                element.getId(),
                element_type,
                name,
                self.getUnitString(element.getUnits()),
                uri,
                description,
                ""
            ])
        return dt

    def getSpeciesTerms(self, model):
        element_type="species"
        dt = []
        for i in range(0,model.getNumSpecies()):
            element = model.getSpecies(i)

            name = element.getName()
            description = ''
            uri = self.getTerm(element)

            # Try to find resource definition for element
            resource = self.getResourceDefinition(element, element_type)
            if (resource is not None):
                if 'resources' in resource.keys() and len(resource['resources']) > 0:
                    uri = resource['resources'][0]['URI']
                if 'name' in resource.keys():
                    name = resource['name']
                if 'description' in resource.keys():
                    description = resource['description']

            dt.append([
                element.getId(),
                element_type,
                name,
                self.getUnitString(element.getUnits()),
                uri,
                description,
                ""
            ])
        return dt

    def getParameterTerms(self, model):
        element_type="parameter"
        dt = []
        for i in range(0,model.getNumParameters()):
            element = model.getParameter(i)

            name = element.getName()
            description = ''
            uri = self.getTerm(element)

            # Try to find resource definition for element
            resource = self.getResourceDefinition(element, element_type)
            if (resource is not None):
                if 'resources' in resource.keys() and len(resource['resources']) > 0:
                    uri = resource['resources'][0]['URI']
                if 'name' in resource.keys():
                    name = resource['name']
                if 'description' in resource.keys():
                    description = resource['description']

            dt.append([
                element.getId(),
                element_type,
                name,
                self.getUnitString(element.getUnits()),
                uri,
                description,
                ""
            ])
        return dt

    def getResourceDefinition(self, element, element_type):
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

    def getUnitString(self, unit):
        """Tries to get the (UCUM formated) unit string of the specified element."""
        if (unit):
            for index, value in enumerate(UnitDefinitions):
                if unit.lower() == value['id'].lower() \
                    or any(val.lower() == unit.lower() for val in value['synonyms']):
                    return value['UCUM'] if value['UCUM'] else value['id']
        return ""

    def getTerm(self, element):
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
