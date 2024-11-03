import libsbml as ls
from sbmlpbkutils.qualifier_definitions import BiologicalQualifierIdsLookup, ModelQualifierIdsLookup

from sbmlpbkutils.ontology_checker import OntologyChecker
from sbmlpbkutils.validation_record import StatusLevel, ValidationRecord

class PbkModelAnnotationsValidator:
    def __init__(self):
        self.ontology_checker = OntologyChecker()

    def check_element_annotation(
        self,
        element: ls.SBase
    ) -> tuple[bool, list[ValidationRecord]]:
        if (element.getTypeCode() == ls.SBML_COMPARTMENT):
            return self.check_compartment_annotation(element)
        else:
            return None

    def check_compartment_annotation(
        self,
        element: ls.SBase
    ) -> tuple[bool, list[ValidationRecord]]:
        valid = True
        messages = []
        cv_terms = self.get_cv_terms_by_type(element)
        if 'BQM_IS' not in cv_terms:
            msg = f"No BQM_IS annotation found for compartment [{element.getId()}]."
            messages.append(ValidationRecord(StatusLevel.ERROR, msg))
            valid = False
        else:
            pbpko_terms = [term for term in cv_terms['BQM_IS'] if self.ontology_checker.check_in_pbpko(term)]
            if not pbpko_terms:
                msg = f"No BQM_IS annotation found refering to a PBPKO term for compartment [{element.getId()}]."
                messages.append(ValidationRecord(StatusLevel.ERROR, msg))
                valid = False
            elif len(pbpko_terms) > 1:
                msg = f"Found multiple BQM_IS annotations refering to a PBPKO term for compartment [{element.getId()}]."
                messages.append(ValidationRecord(StatusLevel.ERROR, msg))
                valid = False
            else:
                pbpko_term = pbpko_terms[0]
                if not self.ontology_checker.check_is_compartment(pbpko_term):
                    msg = f"Specified BQM_IS resource [{pbpko_term}] for compartment [{element.getId()}] does not refer to a compartment."
                    messages.append(ValidationRecord(StatusLevel.ERROR, msg))
                    valid = False
        return (valid, messages)

    def get_cv_terms_by_type(self, element):
        lookup = {}
        cvTerms = element.getCVTerms()
        for term in cvTerms:
            num_resources = term.getNumResources()
            for j in range(num_resources):
                if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER:
                    qualifier_type = BiologicalQualifierIdsLookup[term.getBiologicalQualifierType()]
                elif term.getQualifierType() == ls.MODEL_QUALIFIER:
                    qualifier_type = ModelQualifierIdsLookup[term.getModelQualifierType()]
                if qualifier_type not in lookup:
                    lookup[qualifier_type] = []
                lookup[qualifier_type].append(term.getResourceURI(j))
        return lookup
