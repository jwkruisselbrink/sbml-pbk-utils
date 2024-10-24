import libsbml as ls

from sbmlpbkutils.qualifier_definitions import BiologicalQualifierIdsLookup, ModelQualifierIdsLookup
from sbmlpbkutils.term_definitions import TermDefinitions

class PbkModelInfosExtractor:

    def __init__(self, filename):
        self.filename = filename
        self.document = ls.readSBML(self.filename)
        self.model = self.document.getModel()
        self.terms_by_uri_lookup = self.init_terms_by_uri_lookup()

    def init_terms_by_uri_lookup(self):
        """Tries to find a resource definition for the specified element."""
        result = {}
        for value in TermDefinitions:
            if ('resources' in value.keys()):
                for resource in value['resources']:
                    result.update({
                        f'{resource['qualifier']}#{resource['URI']}': value
                    })
        return result

    def get_input_compartments(self):
        input_compartments = {}
        for i in range(0, self.model.getNumCompartments()):
            compartment = self.model.getCompartment(i)
            cv_terms = self.get_cv_terms(compartment)
            for cv_term in cv_terms:
                lookup_key = f'{cv_term['qualifier']}#{cv_term['uri']}'
                if (lookup_key in self.terms_by_uri_lookup.keys()):
                    term_definition = self.terms_by_uri_lookup[lookup_key]
                    if ('exposure_route' in term_definition.keys()):
                        input_compartments.update({
                            compartment.getId() : term_definition['exposure_route'],
                        })
                        continue
        return input_compartments

    def get_input_species(self):
        input_compartments = self.get_input_compartments()
        input_species = {}
        for i in range(0, self.model.getNumSpecies()):
            element = self.model.getSpecies(i)
            species = self.model.getSpecies(i)
            compartment = element.getCompartment()
            if (compartment in input_compartments.keys()):
                input_species.update({
                    species.getId() : input_compartments[compartment]
                })
        return input_species

    def get_cv_terms(self, element, qualifier_type = None, qualifier = None):
        uris = []
        cvTerms = element.getCVTerms()
        for term in cvTerms:
            num_resources = term.getNumResources()
            for j in range(num_resources):
                if qualifier_type == None or term.getQualifierType() == qualifier_type:
                    if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER \
                        and (qualifier is None or term.getBiologicalQualifierType() == qualifier):
                        uris.append({
                            'qualifier': BiologicalQualifierIdsLookup[term.getBiologicalQualifierType()],
                            'uri': term.getResourceURI(j) 
                        })
                    elif term.getQualifierType() == ls.MODEL_QUALIFIER \
                        and (qualifier is None or term.getBiologicalQualifierType() == qualifier):
                        uris.append({
                            'qualifier': ModelQualifierIdsLookup[term.getModelQualifierType()],
                            'uri': term.getResourceURI(j) 
                        })
        return uris

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