import os.path
import libsbml as ls
from logging import Logger
from . import TermDefinitions

class PbkModelValidator:

  def __init__(self):
    self.ucheck = True
    self.compartments_bqm_is_resources = {}
    self.compartments_bqb_is_uris = {}
    self.parameters_bqm_is_resources = {}

    for index, termDefinition in enumerate(TermDefinitions):
        if 'resources' in termDefinition.keys():
          resources = termDefinition['resources']
          if termDefinition['element_type'] == "compartment":
            for index, resource in enumerate(resources):
              if resource['qualifier'] == "bqmodel:is":
                self.compartments_bqm_is_resources[resource['URI']] = termDefinition
              elif resource['qualifier'] == "bqbiol:is":
                self.compartments_bqb_is_uris[resource['URI']] = termDefinition
          elif termDefinition['element_type'] == "parameter":
            for index, resource in enumerate(resources):
              if resource['qualifier'] == "bqmodel:is":
                self.parameters_bqm_is_resources[resource['URI']] = termDefinition

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

    # Check compartment annotations
    self.validate_parameter_annotations(sbmlDoc, logger)

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
      cvTerms = c.getCVTerms()
      if not cvTerms:
          logger.error(f"No annotations found for compartment [{c.getId()}].")
      else:
        bqm_is_uris = []
        for term in cvTerms:
            num_resources = term.getNumResources()
            for j in range(num_resources):
                if term.getQualifierType() == ls.MODEL_QUALIFIER and \
                    term.getModelQualifierType() == ls.BQM_IS:
                    bqm_is_uris.append(term.getResourceURI(j))
        if len(bqm_is_uris) == 0:
            logger.error(f"No BQM resource annotations found for compartment [{c.getId()}].")
        else:
          for bqm_is_uri in bqm_is_uris:
            if bqm_is_uri not in self.compartments_bqm_is_resources.keys():
              logger.error(f"Invalid BQM resource [{bqm_is_uri}] found for compartment [{c.getId()}].")

  def validate_parameter_annotations(self, sbmlDoc: ls.SBMLDocument, logger: Logger):
    """Check parameter annotations. Each parameter should have a BQM_IS
    relation referring to a term of the PBPK ontology."""
    for i in range(0, sbmlDoc.model.getNumParameters()):
      parm = sbmlDoc.model.getParameter(i)
      cvTerms = parm.getCVTerms()
      if not cvTerms:
          logger.error(f"No annotations found for parameter [{parm.getId()}].")
      else:
        bqm_is_uris = []
        for term in cvTerms:
            num_resources = term.getNumResources()
            for j in range(num_resources):
                if term.getQualifierType() == ls.MODEL_QUALIFIER and \
                    term.getModelQualifierType() == ls.BQM_IS:
                    bqm_is_uris.append(term.getResourceURI(j))
        if len(bqm_is_uris) == 0:
            logger.error(f"No BQM resource annotations found for parameter [{parm.getId()}].")
        else:
          for bqm_is_uri in bqm_is_uris:
            if bqm_is_uri not in self.parameters_bqm_is_resources.keys():
              logger.error(f"Invalid BQM resource [{bqm_is_uri}] found for parameter [{parm.getId()}].")
