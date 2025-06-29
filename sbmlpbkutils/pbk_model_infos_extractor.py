import libsbml as ls

from . import PbkOntologyChecker

class PbkModelInfosExtractor:

    def __init__(
        self,
        document: ls.SBMLDocument
    ):
        self.document = document
        self.model = self.document.getModel()
        self.onto_checker = PbkOntologyChecker()

    def get_model_animal_species(self):
        result = []
        cv_terms = self.model.getCVTerms()
        if cv_terms is not None:
            for term in cv_terms:
                if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER \
                    and term.getBiologicalQualifierType() == ls.BQB_HAS_TAXON:
                    num_resources = term.getNumResources()
                    for j in range(num_resources):
                        iri = term.getResourceURI(j)
                        taxon = self.onto_checker.get_ncbitaxon_class(iri)
                        if taxon is not None:
                            result.append(taxon)
        return result

    def get_model_chemicals(self):
        result = []
        cv_terms = self.model.getCVTerms()
        if cv_terms is not None:
            for term in cv_terms:
                if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER \
                    and term.getBiologicalQualifierType() == ls.BQB_HAS_PROPERTY:
                    num_resources = term.getNumResources()
                    for j in range(num_resources):
                        iri = term.getResourceURI(j)
                        chemical = self.onto_checker.get_chebi_class(iri)
                        if chemical is not None:
                            result.append(chemical)
        return result

    def get_input_compartments(self):
        input_compartments = {}
        for i in range(0, self.model.getNumCompartments()):
            compartment = self.model.getCompartment(i)
            cv_terms = get_cv_terms_by_type(compartment)
            if ls.BQM_IS in cv_terms:
                for term in cv_terms[ls.BQM_IS]:
                    if self.onto_checker.check_is_oral_input_compartment(term):
                        input_compartments.update({
                            compartment.getId() : "oral",
                        })
                    elif self.onto_checker.check_is_dermal_input_compartment(term):
                        input_compartments.update({
                            compartment.getId() : "dermal",
                        })
                    elif self.onto_checker.check_is_inhalation_input_compartment(term):
                        input_compartments.update({
                            compartment.getId() : "inhalation",
                        })
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

    def get_pbko_class(
        self,
        element: ls.SBase
    ):
        cv_terms = element.getCVTerms()
        if cv_terms is not None:
            for term in cv_terms:
                if term.getQualifierType() == ls.MODEL_QUALIFIER:
                    num_resources = term.getNumResources()
                    for j in range(num_resources):
                        iri = term.getResourceURI(j)
                        if self.onto_checker.check_in_pbpko(iri):
                            return self.onto_checker.get_pbpko_class(iri)
        return None

def get_cv_terms_by_type(
    element: ls.SBase
):
    lookup = {}
    cv_terms = element.getCVTerms()
    for term in cv_terms:
        num_resources = term.getNumResources()
        for j in range(num_resources):
            if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER:
                qualifier_type = term.getBiologicalQualifierType()
            elif term.getQualifierType() == ls.MODEL_QUALIFIER:
                qualifier_type = term.getModelQualifierType()
            if qualifier_type not in lookup:
                lookup[qualifier_type] = []
            lookup[qualifier_type].append(term.getResourceURI(j))
    return lookup
