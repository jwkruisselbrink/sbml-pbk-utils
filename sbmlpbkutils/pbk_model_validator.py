import os.path
from enum import Enum
from logging import Logger

import libsbml as ls
from . import PbkOntologyChecker
from .pbk_model_annotator import (
    _biological_qualifier_ids_lookup,
    _model_qualifier_ids_lookup
)

class ValidationStatus(Enum):
    OK = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class ErrorCode(Enum):
    UNDEFINED = -1
    MODEL_MISSING_TAXON_SPECIFICATION = 1
    MODEL_MISSING_NCBITAXON_BQB_HAS_TAXON_TERM = 2
    MODEL_INVALID_NCBITAXON_BQB_HAS_TAXON_TERM = 3
    MODEL_MISSING_CHEMICAL_SPECIFICATION = 4
    COMPARTMENT_MISSING_PBPKO_BQM_IS_TERM = 11
    COMPARTMENT_MULTIPLE_PBPKO_BQM_IS_TERMS = 12
    COMPARTMENT_INVALID_PBPKO_BQM_IS_TERM = 13
    COMPARTMENT_MULTIPLE_ANNOTATION_USE = 17
    PARAMETER_MISSING_PBPKO_BQM_IS_TERM = 21
    PARAMETER_MULTIPLE_PBPKO_BQM_IS_TERMS = 22
    PARAMETER_INVALID_PBPKO_BQM_IS_TERM = 23
    PARAMETER_MISSING_CHEBI_BQB_IS_TERM = 24
    PARAMETER_MULTIPLE_CHEBI_BQB_IS_TERMS = 25
    PARAMETER_MULTIPLE_ANNOTATION_USE = 27
    SPECIES_MISSING_PBPKO_BQM_IS_TERM = 31
    SPECIES_MULTIPLE_PBPKO_BQM_IS_TERMS = 32
    SPECIES_INVALID_PBPKO_BQM_IS_TERM = 33

class ValidationRecord(object):
    def __init__(
        self,
        level: ValidationStatus,
        code: ErrorCode = ErrorCode.UNDEFINED,
        message: str = None
    ):
        self.level = level
        self.message = message
        self.code = code

    def log(self, logger: Logger):
        if self.level == ValidationStatus.CRITICAL:
            logger.critical(self.message)
        if self.level == ValidationStatus.ERROR:
            logger.error(self.message)
        elif self.level == ValidationStatus.WARNING:
            logger.warning(self.message)
        elif self.level == ValidationStatus.OK and self.message is not None:
            logger.info(self.message)

class PbkModelValidator:

    def __init__(self):
        self.ucheck = True
        self.ontology_checker = PbkOntologyChecker()

    def validate(
        self,
        file: str,
        logger: Logger
    ):
        """Runs all validation checks."""
        if not os.path.exists(file):
            logger.error(f'File [{file}] not found.')
            return

        # Read SBML document
        doc  = ls.readSBML(file)

        # Check for document errors
        errors = doc.getNumErrors()
        critical_errors = False
        if errors > 0:
            for i in range(errors):
                severity = doc.getError(i).getSeverity()
                if severity in { ls.LIBSBML_SEV_ERROR, ls.LIBSBML_SEV_FATAL }:
                    logger.error(doc.getError(i).getMessage())
                    critical_errors = True
                else:
                    logger.warning(doc.getError(i).getMessage())

        # Skip consistency checks when serious errors were encountered
        if critical_errors:
            return

        # Run unit consistency checks
        self.validate_units(doc, logger)

        # Check model annotations
        model_messages = self.check_model_annotations(doc)
        for record in model_messages:
            record.log(logger)

        # Check compartment annotations
        comps_messages = self.check_compartment_annotations(doc)
        for record in comps_messages:
            record.log(logger)

        # Check parameter annotations
        parm_messages = self.check_parameter_annotations(doc)
        for record in parm_messages:
            record.log(logger)

        # Check species annotations
        specs_messages = self.check_species_annotations(doc)
        for record in specs_messages:
            record.log(logger)

    def validate_units(
        self,
        doc: ls.SBMLDocument,
        logger: Logger
    ):
        """Runs consistency checks on the units."""
        doc.setConsistencyChecks(ls.LIBSBML_CAT_UNITS_CONSISTENCY, self.ucheck)
        failures = doc.checkConsistencyWithStrictUnits()
        if failures > 0:
            for i in range(failures):
                error = doc.getError(i)
                error_code = error.getErrorId()
                severity = error.getSeverity()
                if severity in { ls.LIBSBML_SEV_ERROR, ls.LIBSBML_SEV_FATAL} \
                    and error_code != ls.UndeclaredUnits:
                    logger.error(doc.getError(i).getMessage())
                else:
                    logger.warning(doc.getError(i).getMessage())

    def check_model_annotations(
        self,
        doc: ls.SBMLDocument
    ) -> list[ValidationRecord]:
        """Check compartment annotations. Each compartment should have a BQM_IS
        relation referring to a term of the PBPK ontology."""
        result = [
            self.check_model_taxon(doc),
            self.check_model_chemicals(doc)
        ]
        return result

    def check_model_taxon(
        self,
        doc: ls.SBMLDocument
    ) -> ValidationRecord:
        """Check modelled (animal) species. A model should have at least 
        one BQB_HAS_TAXON annotation refering to a NCBI taxon."""
        cv_terms = doc.getModel().getCVTerms()
        for term in cv_terms:
            if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER \
                and term.getBiologicalQualifierType() == ls.BQB_HAS_TAXON:
                num_resources = term.getNumResources()
                for j in range(num_resources):
                    iri = term.getResourceURI(j)
                    if self.ontology_checker.check_is_animal_species(iri):
                        return ValidationRecord(ValidationStatus.OK)
        return ValidationRecord(
            ValidationStatus.ERROR,
            ErrorCode.MODEL_MISSING_TAXON_SPECIFICATION,
            "No model level BQB_HAS_TAXON annotation found refering to an NCBI taxon."
        )

    def check_model_chemicals(
        self,
        doc: ls.SBMLDocument
    ) -> ValidationRecord:
        """Check model chemical applicability domain annotation. A model should have at least 
        one BQB_HAS_PROPERTY annotation refering to a ChEBI chemical entity."""
        cv_terms = doc.getModel().getCVTerms()
        for term in cv_terms:
            if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER \
                and term.getBiologicalQualifierType() == ls.BQB_HAS_PROPERTY:
                num_resources = term.getNumResources()
                for j in range(num_resources):
                    iri = term.getResourceURI(j)
                    if self.ontology_checker.check_is_chemical(iri):
                        return ValidationRecord(ValidationStatus.OK)
        return ValidationRecord(
            ValidationStatus.ERROR,
            ErrorCode.MODEL_MISSING_CHEMICAL_SPECIFICATION,
            "No model level BQB_HAS_PROPERTY annotation found refering to a ChEBI chemical entity."
        )

    def check_compartment_annotations(
        self,
        doc: ls.SBMLDocument
    ) -> list[ValidationRecord]:
        """Check compartment annotations. Each compartment should have a BQM_IS
        relation referring to a term of the PBPK ontology."""
        result = []

        # Collect all compartment elements
        elements = []
        for i in range(0, doc.model.getNumCompartments()):
            elements.append(doc.model.getCompartment(i))

        # Check individual compartment annotations
        for element in elements:
            result.append(self.check_compartment_annotation(element))

        # Get lookup by qualifier and IRI
        lookup = self._get_annotations_lookup(elements)
        for key, values in lookup.items():
            if len(values) > 1:
                iri = key[2]
                if self.ontology_checker.check_is_compartment(iri):
                    if (key[0] == ls.MODEL_QUALIFIER and key[1] == ls.BQM_IS):
                        element_ids_str = ','.join(values)
                        msg = f"PBPKO term [{iri}] used as BQM_IS resource by multiple compartments [{element_ids_str}]."
                        result.append(
                            ValidationRecord(
                                ValidationStatus.ERROR,
                                ErrorCode.PARAMETER_MULTIPLE_ANNOTATION_USE,
                                msg
                            )
                        )

        return result

    def check_species_annotations(
        self,
        doc: ls.SBMLDocument
    ) -> list[ValidationRecord]:
        """Check species annotations. Each species should have a BQM_IS
        relation referring to a term of the PBPK ontology."""
        result = []
        for i in range(0, doc.model.getNumSpecies()):
            c = doc.model.getSpecies(i)
            result.append(self.check_species_annotation(c))
        return result

    def check_parameter_annotations(
        self,
        doc: ls.SBMLDocument
    ) -> list[ValidationRecord]:
        """Check parameter annotations. Each parameter should have a BQM_IS
        relation referring to a term of the PBPK ontology."""
        result = []

        # Collect parameter elements
        elements = []
        for i in range(0, doc.model.getNumParameters()):
            elements.append(doc.model.getParameter(i))

        # Check individual paramter annotations
        for element in elements:
            result.append(self.check_parameter_annotation(element))

        # Get lookup by qualifier and IRI
        lookup = self._get_annotations_lookup(elements)
        for key, values in lookup.items():
            if len(values) > 1:
                iri = key[2]
                if self.ontology_checker.check_is_parameter(iri):
                    if (key[0] == ls.MODEL_QUALIFIER and key[1] == ls.BQM_IS):
                        if not self.ontology_checker.check_is_chemical_specific_parameter(iri):
                            # For parameters that are not chemical specific, the same IRI can only
                            # be used once for a BQM_IS
                            element_ids_str = ','.join(values)
                            msg = f"PBPKO term [{iri}] used as BQM_IS resource by multiple parameters [{element_ids_str}]."
                            result.append(
                                ValidationRecord(
                                    ValidationStatus.ERROR,
                                    ErrorCode.PARAMETER_MULTIPLE_ANNOTATION_USE,
                                    msg
                                )
                            )
                        else:
                            # For chemical specific parameters, check whether they have different
                            # BQB_IS ChEBI terms
                            elements = [doc.getElementBySId(element_id) for element_id in values]
                            chebi_terms = [
                                self._get_chebi_bqb_is_annotation(element)
                                for element in elements
                            ]
                            non_none_terms = [term for term in chebi_terms if term is not None]
                            if len(set(non_none_terms)) != len(non_none_terms):
                                result.append(
                                    ValidationRecord(
                                        ValidationStatus.ERROR,
                                        ErrorCode.PARAMETER_MULTIPLE_ANNOTATION_USE,
                                        msg
                                    )
                                )

        return result

    def check_element_annotation(
        self,
        element: ls.SBase
    ) -> ValidationRecord:
        if element.getTypeCode() == ls.SBML_COMPARTMENT:
            return self.check_compartment_annotation(element)
        if element.getTypeCode() == ls.SBML_PARAMETER:
            return self.check_parameter_annotation(element)
        if element.getTypeCode() == ls.SBML_SPECIES:
            return self.check_species_annotation(element)
        return None

    def check_compartment_annotation(
        self,
        element: ls.Compartment
    ) -> ValidationRecord:
        cv_terms = self._get_cv_terms_by_type(element)
        if 'BQM_IS' not in cv_terms:
            msg = f"No BQM_IS annotation found refering to a PBPKO term for compartment [{element.getId()}]."
            return ValidationRecord(
                ValidationStatus.ERROR,
                ErrorCode.COMPARTMENT_MISSING_PBPKO_BQM_IS_TERM,
                msg
            )
        else:
            pbpko_terms = [term for term in cv_terms['BQM_IS'] if self.ontology_checker.check_in_pbpko(term)]
            if not pbpko_terms:
                msg = f"No BQM_IS annotation found refering to a PBPKO term for compartment [{element.getId()}]."
                return ValidationRecord(
                    ValidationStatus.ERROR,
                    ErrorCode.COMPARTMENT_MISSING_PBPKO_BQM_IS_TERM,
                    msg
                )
            elif len(pbpko_terms) > 1:
                msg = f"Found multiple BQM_IS annotations refering to a PBPKO term for compartment [{element.getId()}]."
                return ValidationRecord(
                    ValidationStatus.ERROR,
                    ErrorCode.COMPARTMENT_MULTIPLE_PBPKO_BQM_IS_TERMS,
                    msg
                )
            else:
                pbpko_term = pbpko_terms[0]
                if not self.ontology_checker.check_is_compartment(pbpko_term):
                    msg = f"Specified BQM_IS resource [{pbpko_term}] for compartment [{element.getId()}] does not refer to a compartment."
                    return ValidationRecord(
                        ValidationStatus.ERROR,
                        ErrorCode.COMPARTMENT_INVALID_PBPKO_BQM_IS_TERM,
                        msg
                    )
        return ValidationRecord(ValidationStatus.OK)

    def check_parameter_annotation(
        self,
        element: ls.Parameter
    ) -> ValidationRecord:
        cv_terms = self._get_cv_terms_by_type(element)
        if 'BQM_IS' not in cv_terms:
            param_scope = "" if element.getConstant() else "internal "
            return ValidationRecord(
                level = ValidationStatus.ERROR if element.getConstant() else ValidationStatus.WARNING,
                code = ErrorCode.PARAMETER_MISSING_PBPKO_BQM_IS_TERM,
                message = f"No BQM_IS annotation found refering to a PBPKO term for {param_scope}parameter [{element.getId()}]."
            )
        else:
            pbpko_terms = [term for term in cv_terms['BQM_IS'] if self.ontology_checker.check_in_pbpko(term)]
            if not pbpko_terms:
                param_scope = "" if element.getConstant() else "internal "
                return ValidationRecord(
                    level = ValidationStatus.ERROR if element.getConstant() else ValidationStatus.WARNING,
                    code = ErrorCode.PARAMETER_MISSING_PBPKO_BQM_IS_TERM,
                    message = f"No BQM_IS annotation found refering to a PBPKO term for {param_scope}parameter [{element.getId()}]."
                )
            elif len(pbpko_terms) > 1:
                return ValidationRecord(
                    level = ValidationStatus.ERROR,
                    code = ErrorCode.PARAMETER_MULTIPLE_PBPKO_BQM_IS_TERMS,
                    message = f"Found multiple BQM_IS annotations refering to a PBPKO term for parameter [{element.getId()}]."
                )
            else:
                pbpko_term = pbpko_terms[0]
                if not self.ontology_checker.check_is_parameter(pbpko_term):
                    return ValidationRecord(
                        level = ValidationStatus.ERROR,
                        code = ErrorCode.PARAMETER_INVALID_PBPKO_BQM_IS_TERM,
                        message = f"Specified BQM_IS resource [{pbpko_term}] for parameter [{element.getId()}] does not refer to a parameter."
                    )
                else:
                    if self.ontology_checker.check_is_chemical_specific_parameter(pbpko_term):
                        chebi_terms = [term for term in cv_terms['BQB_IS'] if self.ontology_checker.check_in_chebi(term)] \
                            if 'BQB_IS' in cv_terms else []
                        if not chebi_terms:
                            return ValidationRecord(
                                level = ValidationStatus.ERROR if element.getConstant() else ValidationStatus.WARNING,
                                code = ErrorCode.PARAMETER_MISSING_CHEBI_BQB_IS_TERM,
                                message = f"No BQB_IS annotation found refering to a ChEBI term for chemical specific parameter [{element.getId()}]."
                            )
                        elif len(chebi_terms) > 1:
                            return ValidationRecord(
                                level = ValidationStatus.ERROR,
                                code = ErrorCode.PARAMETER_MULTIPLE_CHEBI_BQB_IS_TERMS,
                                message = f"Found multiple BQB_IS annotations refering to a ChEBI term for parameter [{element.getId()}]."
                            )
        return ValidationRecord(ValidationStatus.OK)

    def check_species_annotation(
        self,
        element: ls.Species
    ) -> ValidationRecord:
        cv_terms = self._get_cv_terms_by_type(element)
        if 'BQM_IS' not in cv_terms:
            msg = f"No BQM_IS annotation found refering to a PBPKO term for species [{element.getId()}]."
            return ValidationRecord(
                ValidationStatus.ERROR,
                ErrorCode.SPECIES_MISSING_PBPKO_BQM_IS_TERM,
                msg
            )
        else:
            pbpko_terms = [term for term in cv_terms['BQM_IS'] if self.ontology_checker.check_in_pbpko(term)]
            if not pbpko_terms:
                msg = f"No BQM_IS annotation found refering to a PBPKO term for species [{element.getId()}]."
                return ValidationRecord(
                    ValidationStatus.ERROR,
                    ErrorCode.SPECIES_MISSING_PBPKO_BQM_IS_TERM,
                    msg
                )
            elif len(pbpko_terms) > 1:
                msg = f"Found multiple BQM_IS annotations refering to a PBPKO term for species [{element.getId()}]."
                return ValidationRecord(
                    ValidationStatus.ERROR,
                    ErrorCode.SPECIES_MULTIPLE_PBPKO_BQM_IS_TERMS,
                    msg
                )
            else:
                pbpko_term = pbpko_terms[0]
                if not self.ontology_checker.check_is_species(pbpko_term):
                    msg = f"Specified BQM_IS resource [{pbpko_term}] for species [{element.getId()}] does not refer to a species."
                    return ValidationRecord(
                        ValidationStatus.ERROR,
                        ErrorCode.SPECIES_INVALID_PBPKO_BQM_IS_TERM,
                        msg
                    )
        return ValidationRecord(ValidationStatus.OK)

    def _get_annotations_lookup(self, elements):
        lookup = {}
        for element in elements:
            element_id = element.getId()
            cv_terms = element.getCVTerms()
            for term in cv_terms:
                num_resources = term.getNumResources()
                for j in range(num_resources):
                    qualifier_type = term.getQualifierType()
                    if qualifier_type == ls.BIOLOGICAL_QUALIFIER:
                        qualifier_id = term.getBiologicalQualifierType()
                    else:
                        qualifier_id = term.getModelQualifierType()
                    iri = term.getResourceURI(j)
                    key = (qualifier_type, qualifier_id, iri)
                    if key not in lookup:
                        lookup[key] = [element_id]
                    else:
                        lookup[key].append(element_id)
        return lookup

    def _get_cv_terms_by_type(
        self,
        element: ls.SBase
    ):
        lookup = {}
        cv_terms = element.getCVTerms()
        for term in cv_terms:
            if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER:
                qualifier_type = _biological_qualifier_ids_lookup[term.getBiologicalQualifierType()]
            else:
                qualifier_type = _model_qualifier_ids_lookup[term.getModelQualifierType()]
            if qualifier_type not in lookup:
                lookup[qualifier_type] = []
            num_resources = term.getNumResources()
            for j in range(num_resources):
                lookup[qualifier_type].append(term.getResourceURI(j))
        return lookup

    def _get_chebi_bqb_is_annotation(
        self,
        element: ls.SBase,
    ):
        annotations = self._get_annotations(element, ls.BIOLOGICAL_QUALIFIER, ls.BQB_IS)
        annotations = [iri for iri in annotations 
                       if self.ontology_checker.check_is_chemical(iri)]
        if len(annotations) > 0:
            return annotations[0]
        return None

    def _get_annotations(
        self,
        element: ls.SBase,
        qualifier_type: int,
        qualifier: int
    ):
        result = []
        cv_terms = element.getCVTerms()
        for term in cv_terms:
            if qualifier_type == ls.BIOLOGICAL_QUALIFIER \
                and term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER \
                and term.getBiologicalQualifierType() == qualifier:
                num_resources = term.getNumResources()
                for j in range(num_resources):
                    result.append(term.getResourceURI(j))
            elif qualifier_type == ls.BIOLOGICAL_QUALIFIER \
                and term.getQualifierType() == ls.MODEL_QUALIFIER \
                and term.getModelQualifierType() == qualifier:
                num_resources = term.getNumResources()
                for j in range(num_resources):
                    result.append(term.getResourceURI(j))
        return result
