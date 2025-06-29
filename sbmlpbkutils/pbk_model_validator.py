import os.path
import libsbml as ls
from logging import Logger
from enum import Enum

from . import PbkOntologyChecker
from .pbk_model_annotator import _biological_qualifier_ids_lookup, _model_qualifier_ids_lookup

class StatusLevel(Enum):
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class ErrorCode(Enum):
    UNDEFINED = -1
    MODEL_MISSING_TAXON_SPECIFICATION = 1
    MODEL_MISSING_NCBITAXON_BQB_HAS_TAXON_TERM = 2
    MODEL_INVALID_NCBITAXON_BQB_HAS_TAXON_TERM = 3
    MODEL_MISSING_CHEMICAL_SPECIFICATION = 4
    COMPARTMENT_MISSING_BQM_TERM = 10
    COMPARTMENT_MISSING_PBPKO_BQM_TERM = 11
    COMPARTMENT_MULTIPLE_PBPKO_BQM_TERMS = 12
    COMPARTMENT_INVALID_PBPKO_BQM_TERM = 13
    COMPARTMENT_MULTIPLE_ANNOTATION_USE = 17,
    PARAMETER_MISSING_BQM_TERM = 20
    PARAMETER_MISSING_PBPKO_BQM_TERM = 21
    PARAMETER_MULTIPLE_PBPKO_BQM_TERMS = 22
    PARAMETER_INVALID_PBPKO_BQM_TERM = 23
    PARAMETER_MISSING_BQB_IS_TERM = 24,
    PARAMETER_MULTIPLE_CHEBI_BQB_IS_TERMS = 25,
    PARAMETER_MULTIPLE_ANNOTATION_USE = 27,
    SPECIES_MISSING_BQM_TERM = 30
    SPECIES_MISSING_PBPKO_BQM_TERM = 31
    SPECIES_MULTIPLE_PBPKO_BQM_TERMS = 32
    SPECIES_INVALID_PBPKO_BQM_TERM = 33

class ValidationRecord(object):
    def __init__(
        self,
        level: StatusLevel,
        code: ErrorCode,
        message: str
    ):
        self.level = level
        self.message = message
        self.code = code

    def log(self, logger: Logger):
        if self.level == StatusLevel.CRITICAL:
          logger.critical(self.message)
        if self.level == StatusLevel.ERROR:
          logger.error(self.message)
        elif self.level == StatusLevel.WARNING:
          logger.warning(self.message)
        elif self.level == StatusLevel.INFO:
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
    sbmlDoc  = ls.readSBML(file)

    # Check for document errors
    errors = sbmlDoc.getNumErrors()
    criticalErrors = False
    if errors > 0:
      for i in range(errors):
        severity = sbmlDoc.getError(i).getSeverity()
        if (severity == ls.LIBSBML_SEV_ERROR) or (severity == ls.LIBSBML_SEV_FATAL):
          logger.error(sbmlDoc.getError(i).getMessage())
          criticalErrors = True
        else:
          logger.warning(sbmlDoc.getError(i).getMessage())

    # Skip consistency checks when serious errors were encountered
    if criticalErrors:
      return

    # Run unit consistency checks
    self.validate_units(sbmlDoc, logger)

    # Check model annotations
    (model_valid, model_messages) = self.check_model_annotations(sbmlDoc)
    for record in model_messages:
      record.log(logger)

    # Check compartment annotations
    (comps_valid, comps_messages) = self.check_compartment_annotations(sbmlDoc)
    for record in comps_messages:
      record.log(logger)

    # Check parameter annotations
    (parms_valid, parm_messages) = self.check_parameter_annotations(sbmlDoc)
    for record in parm_messages:
      record.log(logger)

    # Check species annotations
    (specs_valid, specs_messages) = self.check_species_annotations(sbmlDoc)
    for record in specs_messages:
      record.log(logger)

  def validate_units(
    self,
    sbmlDoc: ls.SBMLDocument,
    logger: Logger
  ):
    """Runs consistency checks on the units."""
    sbmlDoc.setConsistencyChecks(ls.LIBSBML_CAT_UNITS_CONSISTENCY, self.ucheck)
    failures = sbmlDoc.checkConsistencyWithStrictUnits()
    if failures > 0:
      for i in range(failures):
        error = sbmlDoc.getError(i)
        error_code = error.getErrorId()
        severity = error.getSeverity()
        if (severity == ls.LIBSBML_SEV_ERROR \
          or severity == ls.LIBSBML_SEV_FATAL) \
          and error_code != ls.UndeclaredUnits:
          logger.error(sbmlDoc.getError(i).getMessage())
        else:
          logger.warning(sbmlDoc.getError(i).getMessage())

  def check_model_annotations(
    self,
    sbmlDoc: ls.SBMLDocument
  ) -> tuple[bool, list[ValidationRecord]]:
    """Check compartment annotations. Each compartment should have a BQM_IS
    relation referring to a term of the PBPK ontology."""
    valid = True
    messages = []

    (taxon_valid, taxon_record) = self.check_model_taxon(sbmlDoc)
    if not taxon_valid:
      valid = False
      messages.append(taxon_record)

    (chemicals_valid, chemical_record) = self.check_model_chemicals(sbmlDoc)
    if not chemicals_valid:
      valid = False
      messages.append(chemical_record)

    return (valid, messages)

  def check_model_taxon(
    self,
    sbmlDoc: ls.SBMLDocument
  ) -> tuple[bool, ValidationRecord]:
    """Check modelled (animal) species. A model should have at least 
    one BQB_HAS_TAXON annotation refering to a NCBI taxon."""
    cv_terms = sbmlDoc.getModel().getCVTerms()
    for term in cv_terms:
        if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER \
          and term.getBiologicalQualifierType() == ls.BQB_HAS_TAXON:
          num_resources = term.getNumResources()
          for j in range(num_resources):
            iri = term.getResourceURI(j)
            if self.ontology_checker.check_is_animal_species(iri):
              return (True, None)
    msg = f"No model level BQB_HAS_TAXON annotation found refering to an NCBI taxon."
    record = ValidationRecord(StatusLevel.ERROR, ErrorCode.MODEL_MISSING_TAXON_SPECIFICATION, msg)
    return (False, record)

  def check_model_chemicals(
    self,
    sbmlDoc: ls.SBMLDocument
  ) -> tuple[bool, ValidationRecord]:
    """Check model chemical applicability domain annotation. A model should have at least 
    one BQB_HAS_PROPERTY annotation refering to a ChEBI chemical entity."""
    cv_terms = sbmlDoc.getModel().getCVTerms()
    for term in cv_terms:
        if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER \
          and term.getBiologicalQualifierType() == ls.BQB_HAS_PROPERTY:
          num_resources = term.getNumResources()
          for j in range(num_resources):
            iri = term.getResourceURI(j)
            if self.ontology_checker.check_is_chemical_entity(iri):
              return (True, None)
    msg = f"No model level BQB_HAS_PROPERTY annotation found refering to a ChEBI chemical entity."
    record = ValidationRecord(StatusLevel.ERROR, ErrorCode.MODEL_MISSING_CHEMICAL_SPECIFICATION, msg)
    return (False, record)
  
  def check_compartment_annotations(
    self,
    sbmlDoc: ls.SBMLDocument
  ) -> tuple[bool, list[ValidationRecord]]:
    """Check compartment annotations. Each compartment should have a BQM_IS
    relation referring to a term of the PBPK ontology."""
    valid = True
    messages = []

    # Collect all compartment elements
    elements = []
    for i in range(0, sbmlDoc.model.getNumCompartments()):
      elements.append(sbmlDoc.model.getCompartment(i))

    # Check individual compartment annotations
    for element in elements:
      (cur_valid, cur_messages) = self.check_compartment_annotation(element)
      valid = valid and cur_valid
      messages.extend(cur_messages) 

    # Get lookup by qualifier and IRI
    lookup = self._get_annotations_lookup(elements)
    for key, values in lookup.items():
      if (len(values) > 1):
        iri = key[2]
        is_pbpko_compartment = self.ontology_checker.check_is_compartment(iri)
        if (is_pbpko_compartment):
          if (key[0] == ls.MODEL_QUALIFIER and key[1] == ls.BQM_IS):
            element_ids_str = ','.join(values)
            msg = f"PBPKO term [{iri}] used as BQM_IS resource by multiple compartments [{element_ids_str}]."
            messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.PARAMETER_MULTIPLE_ANNOTATION_USE, msg))
            valid = False

    return (valid, messages)

  def check_species_annotations(
    self,
    sbmlDoc: ls.SBMLDocument
  ) -> tuple[bool, list[ValidationRecord]]:
    """Check species annotations. Each species should have a BQM_IS
    relation referring to a term of the PBPK ontology."""
    valid = True
    messages = []
    for i in range(0, sbmlDoc.model.getNumSpecies()):
      c = sbmlDoc.model.getSpecies(i)
      (cur_valid, cur_messages) = self.check_species_annotation(c)
      valid = valid and cur_valid
      messages.extend(cur_messages) 
    return (valid, messages)

  def check_parameter_annotations(
    self,
    sbmlDoc: ls.SBMLDocument
  ) -> tuple[bool, list[ValidationRecord]]:
    """Check parameter annotations. Each parameter should have a BQM_IS
    relation referring to a term of the PBPK ontology."""
    valid = True
    messages = []

    # Collect parameter elements
    elements = []
    for i in range(0, sbmlDoc.model.getNumParameters()):
      elements.append(sbmlDoc.model.getParameter(i))

    # Check individual paramter annotations
    for element in elements:
      (cur_valid, cur_messages) = self.check_parameter_annotation(element)
      valid = valid and cur_valid
      messages.extend(cur_messages) 

    # Get lookup by qualifier and IRI
    lookup = self._get_annotations_lookup(elements)
    for key, values in lookup.items():
      if (len(values) > 1):
        iri = key[2]
        if (self.ontology_checker.check_is_parameter(iri)):
          if (key[0] == ls.MODEL_QUALIFIER and key[1] == ls.BQM_IS):
            if not self.ontology_checker.check_is_chemical_specific_parameter(iri):
              # For parameters that are not chemical specific, the same IRI can only be used once for a BQM_IS
              element_ids_str = ','.join(values)
              msg = f"PBPKO term [{iri}] used as BQM_IS resource by multiple parameters [{element_ids_str}]."
              messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.PARAMETER_MULTIPLE_ANNOTATION_USE, msg))
              valid = False
            # TODO: else-check for chemical specific parameters: check for different chemical
    return (valid, messages)

  def check_element_annotation(
      self,
      element: ls.SBase
  ) -> tuple[bool, list[ValidationRecord]]:
      if (element.getTypeCode() == ls.SBML_COMPARTMENT):
          return self.check_compartment_annotation(element)
      if (element.getTypeCode() == ls.SBML_PARAMETER):
          return self.check_parameter_annotation(element)
      if (element.getTypeCode() == ls.SBML_SPECIES):
          return self.check_species_annotation(element)
      else:
          return None

  def check_compartment_annotation(
      self,
      element: ls.Compartment
  ) -> tuple[bool, list[ValidationRecord]]:
      valid = True
      messages = []
      cv_terms = self._get_cv_terms_by_type(element)
      if 'BQM_IS' not in cv_terms:
          msg = f"No BQM_IS annotation found refering to a PBPKO term for compartment [{element.getId()}]."
          messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.COMPARTMENT_MISSING_BQM_TERM, msg))
          valid = False
      else:
          pbpko_terms = [term for term in cv_terms['BQM_IS'] if self.ontology_checker.check_in_pbpko(term)]
          if not pbpko_terms:
              msg = f"No BQM_IS annotation found refering to a PBPKO term for compartment [{element.getId()}]."
              messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.COMPARTMENT_MISSING_PBPKO_BQM_TERM, msg))
              valid = False
          elif len(pbpko_terms) > 1:
              msg = f"Found multiple BQM_IS annotations refering to a PBPKO term for compartment [{element.getId()}]."
              messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.COMPARTMENT_MULTIPLE_PBPKO_BQM_TERMS, msg))
              valid = False
          else:
              pbpko_term = pbpko_terms[0]
              if not self.ontology_checker.check_is_compartment(pbpko_term):
                  msg = f"Specified BQM_IS resource [{pbpko_term}] for compartment [{element.getId()}] does not refer to a compartment."
                  messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.COMPARTMENT_INVALID_PBPKO_BQM_TERM, msg))
                  valid = False
      return (valid, messages)

  def check_parameter_annotation(
      self,
      element: ls.Parameter
  ) -> tuple[bool, list[ValidationRecord]]:
      valid = True
      messages = []
      cv_terms = self._get_cv_terms_by_type(element)
      if 'BQM_IS' not in cv_terms:
          level = "" if element.getConstant() else "internal "
          msg = f"No BQM_IS annotation found refering to a PBPKO term for {level}parameter [{element.getId()}]."
          status = StatusLevel.ERROR if element.getConstant() else StatusLevel.WARNING
          messages.append(ValidationRecord(status, ErrorCode.PARAMETER_MISSING_BQM_TERM, msg))
          valid = not element.getConstant()
      else:
          pbpko_terms = [term for term in cv_terms['BQM_IS'] if self.ontology_checker.check_in_pbpko(term)]
          if not pbpko_terms:
              level = "" if element.getConstant() else "internal "
              msg = f"No BQM_IS annotation found refering to a PBPKO term for {level}parameter [{element.getId()}]."
              status = StatusLevel.ERROR if element.getConstant() else StatusLevel.WARNING
              messages.append(ValidationRecord(status, ErrorCode.PARAMETER_MISSING_BQM_TERM, msg))
              valid = not element.getConstant()
          elif len(pbpko_terms) > 1:
              msg = f"Found multiple BQM_IS annotations refering to a PBPKO term for parameter [{element.getId()}]."
              messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.PARAMETER_MULTIPLE_PBPKO_BQM_TERMS, msg))
              valid = False
          else:
              pbpko_term = pbpko_terms[0]
              if not self.ontology_checker.check_is_parameter(pbpko_term):
                  msg = f"Specified BQM_IS resource [{pbpko_term}] for parameter [{element.getId()}] does not refer to a parameter."
                  messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.PARAMETER_INVALID_PBPKO_BQM_TERM, msg))
                  valid = False
              else:
                if self.ontology_checker.check_is_chemical_specific_parameter(pbpko_term):
                  chebi_terms = [term for term in cv_terms['BQB_IS'] if self.ontology_checker.check_in_chebi(term)] \
                    if 'BQB_IS' in cv_terms else []
                  if not chebi_terms:
                      msg = f"No BQB_IS annotation found refering to a ChEBI term for chemical specific parameter [{element.getId()}]."
                      status = StatusLevel.ERROR if element.getConstant() else StatusLevel.WARNING
                      messages.append(ValidationRecord(status, ErrorCode.PARAMETER_MISSING_BQB_IS_TERM, msg))
                      valid = not element.getConstant()
                  elif len(pbpko_terms) > 1:
                        msg = f"Found multiple BQB_IS annotations refering to a ChEBI term for parameter [{element.getId()}]."
                        messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.PARAMETER_MULTIPLE_CHEBI_BQB_IS_TERMS, msg))
                        valid = False
      return (valid, messages)

  def check_species_annotation(
      self,
      element: ls.Species
  ) -> tuple[bool, list[ValidationRecord]]:
      valid = True
      messages = []
      cv_terms = self._get_cv_terms_by_type(element)
      if 'BQM_IS' not in cv_terms:
          msg = f"No BQM_IS annotation found refering to a PBPKO term for species [{element.getId()}]."
          messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.SPECIES_MISSING_BQM_TERM, msg))
          valid = False
      else:
          pbpko_terms = [term for term in cv_terms['BQM_IS'] if self.ontology_checker.check_in_pbpko(term)]
          if not pbpko_terms:
              msg = f"No BQM_IS annotation found refering to a PBPKO term for species [{element.getId()}]."
              messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.SPECIES_MISSING_PBPKO_BQM_TERM, msg))
              valid = False
          elif len(pbpko_terms) > 1:
              msg = f"Found multiple BQM_IS annotations refering to a PBPKO term for species [{element.getId()}]."
              messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.SPECIES_MULTIPLE_PBPKO_BQM_TERMS, msg))
              valid = False
          else:
              pbpko_term = pbpko_terms[0]
              if not self.ontology_checker.check_is_species(pbpko_term):
                  msg = f"Specified BQM_IS resource [{pbpko_term}] for species [{element.getId()}] does not refer to a species."
                  messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.SPECIES_INVALID_PBPKO_BQM_TERM, msg))
                  valid = False
      return (valid, messages)

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
                elif qualifier_type == ls.MODEL_QUALIFIER:
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
          elif term.getQualifierType() == ls.MODEL_QUALIFIER:
              qualifier_type = _model_qualifier_ids_lookup[term.getModelQualifierType()]
          if qualifier_type not in lookup:
              lookup[qualifier_type] = []
          num_resources = term.getNumResources()
          for j in range(num_resources):
              lookup[qualifier_type].append(term.getResourceURI(j))
      return lookup
