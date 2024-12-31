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
    COMPARTMENT_MISSING_BQM_TERM = 10
    COMPARTMENT_MISSING_PBPKO_BQM_TERM = 11
    COMPARTMENT_MULTIPLE_PBPKO_BQM_TERMS = 12
    COMPARTMENT_INVALID_PBPKO_BQM_TERM = 13
    PARAMETER_MISSING_BQM_TERM = 20
    PARAMETER_MISSING_PBPKO_BQM_TERM = 21
    PARAMETER_MULTIPLE_PBPKO_BQM_TERMS = 22
    PARAMETER_INVALID_PBPKO_BQM_TERM = 23
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

    # Check compartment annotations
    self.validate_compartment_annotations(sbmlDoc, logger)

    # Check parameter annotations
    self.validate_parameter_annotations(sbmlDoc, logger)

    # Check species annotations
    self.validate_species_annotations(sbmlDoc, logger)

  def validate_units(
    self,
    sbmlDoc: ls.SBMLDocument,
    logger: Logger
  ):
    """Runs consistency checks on the units."""
    sbmlDoc.setConsistencyChecks(ls.LIBSBML_CAT_UNITS_CONSISTENCY, self.ucheck)
    failures = sbmlDoc.checkConsistency()
    if failures > 0:
      for i in range(failures):
        severity = sbmlDoc.getError(i).getSeverity()
        if (severity == ls.LIBSBML_SEV_ERROR) or (severity == ls.LIBSBML_SEV_FATAL):
          logger.error(sbmlDoc.getError(i).getMessage())
        else:
          logger.warning(sbmlDoc.getError(i).getMessage())

  def validate_compartment_annotations(
    self,
    sbmlDoc: ls.SBMLDocument,
    logger: Logger
  ):
    """Check compartment annotations. Each compartment should have a BQM_IS
    relation referring to a term of the PBPK ontology."""
    for i in range(0, sbmlDoc.model.getNumCompartments()):
      c = sbmlDoc.model.getCompartment(i)
      (valid, messages) = self.check_compartment_annotation(c)
      for record in messages:
        if record.level == StatusLevel.CRITICAL:
          logger.critical(record.message)
        if record.level == StatusLevel.ERROR:
          logger.error(record.message)
        elif record.level == StatusLevel.WARNING:
          logger.warning(record.message)
        elif record.level == StatusLevel.INFO:
          logger.info(record.message)

  def validate_parameter_annotations(
    self,
    sbmlDoc: ls.SBMLDocument,
    logger: Logger
  ):
    """Check parameter annotations. Each parameter should have a BQM_IS
    relation referring to a term of the PBPK ontology."""
    for i in range(0, sbmlDoc.model.getNumParameters()):
      c = sbmlDoc.model.getParameter(i)
      (valid, messages) = self.check_parameter_annotation(c)
      for record in messages:
        if record.level == StatusLevel.CRITICAL:
          logger.critical(record.message)
        if record.level == StatusLevel.ERROR:
          logger.error(record.message)
        elif record.level == StatusLevel.WARNING:
          logger.warning(record.message)
        elif record.level == StatusLevel.INFO:
          logger.info(record.message)

  def validate_species_annotations(
    self,
    sbmlDoc: ls.SBMLDocument,
    logger: Logger
  ):
    """Check species annotations. Each species should have a BQM_IS
    relation referring to a term of the PBPK ontology."""
    for i in range(0, sbmlDoc.model.getNumSpecies()):
      c = sbmlDoc.model.getSpecies(i)
      (valid, messages) = self.check_species_annotation(c)
      for record in messages:
        if record.level == StatusLevel.CRITICAL:
          logger.critical(record.message)
        if record.level == StatusLevel.ERROR:
          logger.error(record.message)
        elif record.level == StatusLevel.WARNING:
          logger.warning(record.message)
        elif record.level == StatusLevel.INFO:
          logger.info(record.message)

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
          msg = f"No BQM_IS annotation found refering to a PBPKO term for parameter [{element.getId()}]."
          status = StatusLevel.ERROR if element.getConstant() else StatusLevel.WARNING
          messages.append(ValidationRecord(status, ErrorCode.PARAMETER_MISSING_BQM_TERM, msg))
          valid = not element.getConstant()
      else:
          pbpko_terms = [term for term in cv_terms['BQM_IS'] if self.ontology_checker.check_in_pbpko(term)]
          if not pbpko_terms:
              msg = f"No BQM_IS annotation found refering to a PBPKO term for parameter [{element.getId()}]."
              messages.append(ValidationRecord(StatusLevel.ERROR, ErrorCode.PARAMETER_MISSING_PBPKO_BQM_TERM, msg))
              valid = False
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

  def _get_cv_terms_by_type(
      self,
      element: ls.SBase
  ):
      lookup = {}
      cv_terms = element.getCVTerms()
      for term in cv_terms:
          num_resources = term.getNumResources()
          for j in range(num_resources):
              if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER:
                  qualifier_type = _biological_qualifier_ids_lookup[term.getBiologicalQualifierType()]
              elif term.getQualifierType() == ls.MODEL_QUALIFIER:
                  qualifier_type = _model_qualifier_ids_lookup[term.getModelQualifierType()]
              if qualifier_type not in lookup:
                  lookup[qualifier_type] = []
              lookup[qualifier_type].append(term.getResourceURI(j))
      return lookup
