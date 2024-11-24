import os.path
import libsbml as ls
from logging import Logger

from sbmlpbkutils.pbk_model_annotations_validator import PbkModelAnnotationsValidator
from sbmlpbkutils.validation_record import StatusLevel

class PbkModelValidator:

  def __init__(self):
    self.ucheck = True
    self.annotations_validator = PbkModelAnnotationsValidator()

  def validate(self, file: str, logger: Logger):
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

  def validate_units(self, sbmlDoc: ls.SBMLDocument, logger: Logger):
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

  def validate_compartment_annotations(self, sbmlDoc: ls.SBMLDocument, logger: Logger):
    """Check compartment annotations. Each compartment should have a BQM_IS
    relation referring to a term of the PBPK ontology."""
    for i in range(0, sbmlDoc.model.getNumCompartments()):
      c = sbmlDoc.model.getCompartment(i)
      (valid, messages) = self.annotations_validator.check_compartment_annotation(c)
      for record in messages:
        if record.level == StatusLevel.CRITICAL:
          logger.critical(record.message)
        if record.level == StatusLevel.ERROR:
          logger.error(record.message)
        elif record.level == StatusLevel.WARNING:
          logger.warning(record.message)
        elif record.level == StatusLevel.INFO:
          logger.info(record.message)

  def validate_parameter_annotations(self, sbmlDoc: ls.SBMLDocument, logger: Logger):
    """Check parameter annotations. Each parameter should have a BQM_IS
    relation referring to a term of the PBPK ontology."""
    for i in range(0, sbmlDoc.model.getNumParameters()):
      c = sbmlDoc.model.getParameter(i)
      (valid, messages) = self.annotations_validator.check_parameter_annotation(c)
      for record in messages:
        if record.level == StatusLevel.CRITICAL:
          logger.critical(record.message)
        if record.level == StatusLevel.ERROR:
          logger.error(record.message)
        elif record.level == StatusLevel.WARNING:
          logger.warning(record.message)
        elif record.level == StatusLevel.INFO:
          logger.info(record.message)

  def validate_species_annotations(self, sbmlDoc: ls.SBMLDocument, logger: Logger):
    """Check species annotations. Each species should have a BQM_IS
    relation referring to a term of the PBPK ontology."""
    for i in range(0, sbmlDoc.model.getNumSpecies()):
      c = sbmlDoc.model.getSpecies(i)
      (valid, messages) = self.annotations_validator.check_species_annotation(c)
      for record in messages:
        if record.level == StatusLevel.CRITICAL:
          logger.critical(record.message)
        if record.level == StatusLevel.ERROR:
          logger.error(record.message)
        elif record.level == StatusLevel.WARNING:
          logger.warning(record.message)
        elif record.level == StatusLevel.INFO:
          logger.info(record.message)
