import os
from pathlib import Path
from typing import List, Union
import libsbml as ls
import numpy as np
import pandas as pd
from logging import Logger
from sbmlutils import utils
from sbmlutils.metadata.annotator import ModelAnnotator, ExternalAnnotation
from sbmlpbkutils.qualifier_definitions import BiologicalQualifierIdsLookup, ModelQualifierIdsLookup
from pymetadata.core.annotation import RDFAnnotation as Annotation
from pymetadata.identifiers.miriam import BQB, BQM
from . import UnitDefinitions, set_unit_definition

class PbkModelAnnotator:

    def annotate(
        self,
        sbml_file: str,
        annotations_file: str,
        logger: Logger
    ) -> ls.SBMLDocument:
        # Open SBML document using libSBML
        try:
            document = ls.readSBML(sbml_file)
        except Exception as error:
            file_basename = os.path.basename(sbml_file)
            logger.critical(f'Failed to read SBML file [{file_basename}]: {error}')
            raise

        # Read annotations file
        try:
            df = PbkModelAnnotator._read_annotations_df(annotations_file, logger)
            df = df.replace(np.nan, None)
        except Exception as error:
            file_basename = os.path.basename(annotations_file)
            logger.critical(f'Failed to read annotations file [{file_basename}]: {error}')
            raise

        # Annotate
        return self.annotate_document(
            document,
            df,
            logger
        )

    def annotate_document(
        self,
        document: ls.SBMLDocument,
        annotations_df: pd.DataFrame,
        my_logger: Logger
    ) -> ls.SBMLDocument:
        """Annotate the units of the SBML file using the annotations
        file and write results to the specified out file."""
        logger = my_logger
        model = document.getModel()

        logger.info(f'Start model annoation: total {len(annotations_df.index)} annotation records')

        # Read model units
        units_dict = self._get_model_units_dict(model)

        # Check for required columns
        required_columns = ['element_id', 'sbml_type', 'unit']
        missing_columns = list(set(required_columns) - set(annotations_df.columns))
        if missing_columns:
            missing_columns = [f'[{item}]' for item in missing_columns]
            missing_columns_str = str.join(', ', missing_columns)
            msg = f'Missing columns {missing_columns_str} in annotations table.'
            logger.critical(msg)
            raise ValueError(msg)

        # Check for required columns
        if not any(item in annotations_df.columns for item in ['URI', 'resource']):
            msg = f'Missing [URI] or [resource] column in annotations table.'
            logger.critical(msg)
            raise ValueError(msg)

        # Check for required columns
        if not 'qualifier' in annotations_df.columns:
            msg = f'Missing [qualifier] column in annotations table.'
            logger.critical(msg)
            raise ValueError(msg)

        # If the annotations file contains an URI column, then try to add
        # rdf annotations for model elements using SBMLUtils for records
        if ('URI' in annotations_df.columns):
            if (not 'pattern' in annotations_df.columns):
                # If pattern column is missing, then use element id column
                annotations_df['pattern'] = annotations_df['element_id']
            if (not 'annotation_type' in annotations_df.columns):
                # If annotation type column is missing, then add with default value
                annotations_df['annotation_type'] = 'rdf'
            if (not 'resource' in annotations_df.columns):
                # If resource column is missing, then use URI column
                annotations_df['resource'] = annotations_df['URI']

        # Iterate over annotation records
        for index, row in annotations_df.iterrows():
            element_id = str(row["element_id"]).strip() if "element_id" in row and row["element_id"] else None
            element_name = str(row["element_name"]).strip() if "element_name" in row and row["element_name"] else None
            sbml_type = str(row["sbml_type"]).strip() if "sbml_type" in row and row["sbml_type"] else None
            resource = str(row["resource"]).strip() if "resource" in row and row["resource"] else None
            qualifier = str(row["qualifier"]).strip() if "qualifier" in row and row["qualifier"] else None
            unit = str(row["unit"]).strip() if "unit" in row and row["unit"] else None

            # Skip records with empty URI field
            annotation = None
            if resource is not None:
                if row['annotation_type'] != 'rdf':
                    msg = f'Unsupported annotation type "{row['annotation_type']}" for {sbml_type} element "{element_id}".'
                    logger.error(msg)
                else:
                    try:
                        annotation = ExternalAnnotation(row)
                    except:
                        msg = f'Invalid annotation [{qualifier}|{resource}] for {sbml_type} "{element_id}".'
                        logger.error(msg)

            if sbml_type == "document":
                elements = [document]
            elif (element_id):
                elements = self._get_elements_by_pattern(
                    model,
                    sbml_type,
                    element_id
                )
                if not elements:
                    logger.error(f'Could not find {sbml_type} "{element_id}".')

            for element in elements:
                # If unit field is not empty, try set element unit
                if (unit is not None):
                    self._set_element_unit(
                        document,
                        element,
                        element_id,
                        unit,
                        units_dict,
                        True,
                        logger
                    )

                # If name is not empty, try to set element name
                if (element_name is not None
                    and sbml_type != "document"):
                    # If description field is not empty, try set element name
                    self._set_element_name(
                        element,
                        element_name,
                        True,
                        logger
                    )

                # Set annotations
                if annotation is not None:
                    self._set_element_annotation(
                        element,
                        annotation,
                        logger
                    )

        return document

    def remove_all_annotations(
        self,
        document: ls.SBMLDocument
    ):
        model = document.getModel()
        model.unsetAnnotation()

        for i in range(0, model.getNumReactions()):
            re = model.getReaction(i)
            re.unsetAnnotation()

            for j in range(0, re.getNumReactants()):
                rt = re.getReactant(j)
                rt.unsetAnnotation()

            for j in range(0, re.getNumProducts()):
                rt = re.getProduct(j)
                rt.unsetAnnotation()

            for j in range(0, re.getNumModifiers()):
                md = re.getModifier(j)
                md.unsetAnnotation()

            if re.isSetKineticLaw():
                kl = re.getKineticLaw()
                kl.unsetAnnotation()

                for j in range(0, kl.getNumParameters()):
                    pa = kl.getParameter(j)
                    pa.unsetAnnotation()

        for i in range(0, model.getNumSpecies()):
            sp = model.getSpecies(i)
            sp.unsetAnnotation()

        for i in range(0, model.getNumCompartments()):
            sp = model.getCompartment(i)
            sp.unsetAnnotation()

        for i in range(0, model.getNumFunctionDefinitions()):
            sp = model.getFunctionDefinition(i)
            sp.unsetAnnotation()

        for i in range(0, model.getNumUnitDefinitions()):
            sp = model.getUnitDefinition(i)
            sp.unsetAnnotation()

        for i in range(0, model.getNumParameters()):
            sp = model.getParameter(i)
            sp.unsetAnnotation()

        for i in range(0, model.getNumRules()):
            sp = model.getRule(i)
            sp.unsetAnnotation()

        for i in range(0, model.getNumInitialAssignments()):
            sp = model.getInitialAssignment(i)
            sp.unsetAnnotation()

        for i in range(0, model.getNumEvents()):
            sp = model.getEvent(i)
            sp.unsetAnnotation()

            for j in range(0, sp.getNumEventAssignments()):
                ea = sp.getEventAssignment(j)
                ea.unsetAnnotation()

        for i in range(0, model.getNumSpeciesTypes()):
            sp = model.getSpeciesType(i)
            sp.unsetAnnotation()

        for i in range(0, model.getNumConstraints()):
            sp = model.getConstraint(i)
            sp.unsetAnnotation()

    def update_element_info(
        self,
        document: ls.SBMLDocument,
        element_id: str,
        logger: Logger,
        element_name: str = None,
        unit_id: str = None
    ):
        model = document.getModel()
        element = model.getElementBySId(element_id)
        units_dict = self._get_model_units_dict(model)
        if element_name is not None:
            self._set_element_name(
                element,
                element_name,
                True,
                logger
            )
        if unit_id is not None:
            self._set_element_unit(
                document,
                element,
                element_id,
                unit_id,
                units_dict,
                True,
                logger
            )

    def set_element_name(
        self,
        document: ls.SBMLDocument,
        element_id: str,
        element_name: str,
        logger: Logger
    ):
        model = document.getModel()
        element = model.getElementBySId(element_id)
        self._set_element_name(
            element,
            element_name,
            True,
            logger
        )

    def _set_element_name(
        self,
        element: ls.SBase,
        name: str,
        overwrite: bool,
        logger: Logger
    ) -> None:
        """Sets the name of the provided element."""
        if not element.isSetName() or overwrite:
            logger.info(f'Set name of {element} to "{name}".')
            element.setName(name)
        else:
            logger.info(f"Name for {element} already set, not overwriting.")

    def set_element_unit(
        self,
        document: ls.SBMLDocument,
        element_id: str,
        unit_id: str,
        logger: Logger,
    ):
        model = document.getModel()
        element = model.getElementBySId(element_id)
        units_dict = self._get_model_units_dict(model)
        self._set_element_unit(
            document,
            element,
            element_id,
            unit_id,
            units_dict,
            True,
            logger
        )

    def _set_element_unit(
        self,
        document: ls.SBMLDocument,
        element: ls.SBase,
        element_id: str,
        unit_id: str,
        units_dict: dict,
        overwrite: bool,
        logger: Logger
    ):
        """Set element unit of element with specified id and type to the specfied unit."""
        if element.getTypeCode() == ls.SBML_DOCUMENT \
            or element.getTypeCode() == ls.SBML_MODEL:
            model = document.getModel()
            u_def = self._get_or_add_unit_definition(document, unit_id, units_dict, logger)
            if element_id == "timeUnits":
                if not model.isSetTimeUnits() or overwrite:
                    logger.info(f"Set model time unit [{unit_id}].")
                    model.setTimeUnits(u_def.getId())
                elif model.isSetTimeUnits():
                    logger.info(f"Did not set model time unit [{unit_id}]: unit already set.")
            elif element_id == "substanceUnits":
                if not model.isSetSubstanceUnits() or overwrite:
                    logger.info(f"Set model substances unit [{unit_id}].")
                    model.setSubstanceUnits(u_def.getId())
                elif model.isSetSubstanceUnits():
                    logger.info(f"Did not set model substances unit [{unit_id}]: unit already set.")
            elif element_id == "volumeUnits":
                if not model.isSetVolumeUnits() or overwrite:
                    logger.info(f"Set model volume unit [{unit_id}].")
                    model.setVolumeUnits(u_def.getId())
                elif model.isSetVolumeUnits():
                    logger.info(f"Did not set model volume unit [{unit_id}]: unit already set.")
            else:
                logger.info(f"Did not set unit [{unit_id}] for root level element [{element_id}]: not a valid document level element identifier.")
        else:
            if not element.isSetUnits() or overwrite:
                u_def = self._get_or_add_unit_definition(document, unit_id, units_dict, logger)
                if (u_def):
                    logger.info(f"Set unit of {element} to [{unit_id}].")
                    element.setUnits(u_def.getId())
                elif element.isSetUnits():
                    logger.info(f"Did not set unit [{unit_id}] for {element}: unit already set.")
            else:
                logger.info(f"Name for {element} already set, not overwriting.")

    def set_element_annotation(
        self,
        document: ls.SBMLDocument,
        element_id: str,
        qualifier: str,
        iri: str,
        logger: Logger,
        overwrite: bool = True,
    ) -> None:
        """Annotate SBase element based on the provided qualifier and resource IRI.
        """
        model = document.getModel()
        element = model.getElementBySId(element_id)
        annotation = Annotation(
            qualifier=ExternalAnnotation._parse_qualifier_str(qualifier),
            resource=iri
        )
        self._set_element_annotation(
            element,
            annotation,
            logger,
            overwrite
        )

    def _set_element_annotation(
        self,
        element: ls.SBase,
        annotation: Union[ExternalAnnotation|Annotation],
        logger: Logger,
        overwrite: bool = False
    ) -> None:
        """Annotate SBase element based on the provided annotation record.
        """
        try:
            if type(annotation) is ExternalAnnotation:
                external_annotation = annotation
                rdf_annotation = Annotation(
                    qualifier=external_annotation.qualifier,
                    resource=external_annotation.resource
                )
            else:
                rdf_annotation = annotation
            qualifier, resource = rdf_annotation.qualifier.value, rdf_annotation.resource_normalized
        except Exception as error:
            msg = f'Invalid annotation record [{rdf_annotation.qualifier}|{rdf_annotation.resource}]: {error}'
            return

        # Check qualifier type
        if qualifier.startswith("BQB"):
            qualifier_type = ls.BIOLOGICAL_QUALIFIER
            ls_qualifier_str = ModelAnnotator.get_SBMLQualifier(qualifier, "BQB")
            ls_qualifier = ls.BiolQualifierType_fromString(ls_qualifier_str)
        elif qualifier.startswith("BQM"):
            qualifier_type = ls.MODEL_QUALIFIER
            ls_qualifier_str = ModelAnnotator.get_SBMLQualifier(qualifier, "BQM")
            ls_qualifier = ls.ModelQualifierType_fromString(ls_qualifier_str)
        else:
            msg = f"Failed to set [{qualifier}] resource [{resource}] for {element}: unsupported qualifier."
            logger.error(msg)
            return

        # meta id has to be set
        if not element.isSetMetaId():
            element.setMetaId(utils.create_metaid(element))

        # Create or get the CV term
        cv_term: ls.CVTerm = None
        if (overwrite):
            cv_terms = element.getCVTerms()
            for term in cv_terms:
                if term.getQualifierType() == qualifier_type:
                    if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER \
                        and term.getBiologicalQualifierType() == ls_qualifier:
                        cv_term = term
                        break
                    elif term.getQualifierType() == ls.MODEL_QUALIFIER \
                        and term.getModelQualifierType() == ls_qualifier:
                        cv_term = term
                        break

        if cv_term is not None:
            # Update resource if CV term already exists
            current_resources = []
            num_resources = cv_term.getNumResources()
            for i in range(num_resources):
                current_resources.append(cv_term.getResourceURI(i))

            if cv_term.addResource(resource) != ls.LIBSBML_OPERATION_SUCCESS:
                logger.error(f"Failed to add [{qualifier}] resource [{resource}] to {element}.")
                return
            for uri in current_resources:
                if cv_term.removeResource(uri) != ls.LIBSBML_OPERATION_SUCCESS:
                    logger.error(f"Failed to remove current [{qualifier}] resource [{uri}] for {element}.")
                    return
            logger.info(f"Update [{qualifier}] resource [{resource}] to {element}.")
        else:
            # Create new CV term if not overwrite or no overwritable candidate
            cv_term = ls.CVTerm()
            cv_term.setQualifierType(qualifier_type)

            # Set correct type of qualifier
            if qualifier_type == ls.BIOLOGICAL_QUALIFIER:
                if cv_term.setBiologicalQualifierType(ls_qualifier_str) != ls.LIBSBML_OPERATION_SUCCESS:
                    logger.error(f"Failed to set [{qualifier}] resource [{resource}] for {element}.")
                    return
            elif qualifier_type == ls.MODEL_QUALIFIER:
                if cv_term.setModelQualifierType(ls_qualifier_str) != ls.LIBSBML_OPERATION_SUCCESS:
                    logger.error(f"Failed to set [{qualifier}] resource [{resource}] for {element}.")
                    return
            else:
                msg = f"Failed to set [{qualifier}] resource [{resource}] for {element}: unsupported qualifier."
                logger.error(msg)
                return
            if cv_term.addResource(resource) != ls.LIBSBML_OPERATION_SUCCESS:
                msg = f"Failed to set [{qualifier}] resource [{resource}] for {element}: cannot add resource."
                logger.error(msg)
                return
            if element.addCVTerm(cv_term) != ls.LIBSBML_OPERATION_SUCCESS:
                logger.error(f"Failed to add [{qualifier}] resource [{resource}] to {element}.")
                logger.error(msg)
                return
            else:
                logger.info(f"Add [{qualifier}] resource [{resource}] to {element}.")

        # write SBO terms based on the SBO RDF
        if rdf_annotation.collection == "sbo":
            element.setSBOTerm(rdf_annotation.term)

    def _get_elements_by_pattern(
        self,
        model: ls.Model,
        sbml_type: str,
        pattern: str
    ) -> List[ls.SBase]:
        """
        Get list of SBML elements from given ids.
        """
        elements = []
        sbml_ids = [pattern]
        for sid in sbml_ids:
            if sbml_type == "rule":
                e = model.getRuleByVariable(sid)
            elif sbml_type == "unit":
                e = model.getUnitDefinition(sid)
            else:
                # returns the first element with id
                # FIXME: this is very slow in a loop, better solution required via
                e = model.getElementBySId(sid)
            if e is None:
                if sid == model.getId():
                    e = model
                else:
                    continue
            elements.append(e)
        return elements

    def _get_model_units_dict(
        self,
        model: ls.Model
    ) -> dict:
        # Read model units
        units_dict = dict()
        for unit_def in model.getListOfUnitDefinitions():
            units_dict[unit_def.getId()] = unit_def
        return units_dict

    def _get_or_add_unit_definition(
        self,
        doc: ls.SBMLDocument,
        unit_id: str,
        units_dict: dict,
        logger: Logger
    ):
        """Tries to get the unit definition for the specified unit id from the SBML document.
        The unit definition will be created and added to the document if it does not yet exist.
        """
        if (unit_id not in units_dict):
            unit_def = self._find_unit_definition(unit_id)
            if (unit_def is None):
                logger.error(f"Failed to set unit [{unit_id}]: unknown unit definition!")
                return
            model = doc.getModel()
            unit_definition = model.getUnitDefinition(unit_def["id"])
            if (not unit_definition):
                logger.info(f"Add unit definition [{unit_id}].")
                unit_definition = model.createUnitDefinition()
                set_unit_definition(
                    unit_definition,
                    unit_def
                )
            units_dict[unit_id] = unit_definition
        return units_dict[unit_id]

    def _find_unit_definition(
        self,
        str: str
    ):
        """Find unit definition matching the provided string."""
        res = None
        for index, value in enumerate(UnitDefinitions):
            if value['id'].lower() == str.lower() \
                or any(val.lower() == str.lower() for val in value['synonyms']):
                res = value
                break
        return res

    @staticmethod
    def _read_annotations_df(
        file_path: Path,
        logger: Logger,
        file_format: str = "*"
    ) -> pd.DataFrame:
        """Read annotations from given file into DataFrame.
        Supports "xlsx", "tsv", "csv", "json", "*"
        """
        filename, file_extension = os.path.splitext(file_path)
        if file_format == "*":
            file_format = file_extension[1:]  # remove leading dot

        formats = ["xlsx", "tsv", "csv", "json"]
        if file_format not in formats:
            raise IOError(
                f"Annotation format '{file_format}' not in supported formats: "
                f"'{formats}'"
            )

        if file_extension != ("." + file_format):
            logger.warning(
                f"format '{file_format}' not matching file extension "
                f"'{file_extension}' "
                f"for file_path '{file_path}'"
            )

        if file_format == "tsv":
            df = pd.read_csv(file_path, sep="\t", comment="#", skip_blank_lines=True)
        elif file_format == "csv":
            df = pd.read_csv(file_path, sep=",", comment="#", skip_blank_lines=True)
        elif file_format == "json":
            df = pd.read_json(file_path)
        elif file_format == "xlsx":
            df = pd.read_excel(file_path, comment="#", engine="openpyxl")

        df.dropna(axis="index", inplace=True, how="all")
        return df

    def get_cv_terms(
        self,
        element: ls.SBase,
        qualifier_type = None,
        qualifier = None
    ):
        uris = []
        cv_terms = element.getCVTerms()
        for term in cv_terms:
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
                        and (qualifier is None or term.getModelQualifierType() == qualifier):
                        uris.append({
                            'qualifier': ModelQualifierIdsLookup[term.getModelQualifierType()],
                            'uri': term.getResourceURI(j)
                        })
        return uris

    @staticmethod
    def print_element_terms(
        document: ls.SBMLDocument,
        element_id: str
    ) -> None:
        model = document.getModel()
        element = model.getElementBySId(element_id)
        if not element.isSetAnnotation():
            return

        print(f"-----{element.getElementName()} ({element_id}) annotation -----")
        print(element.getAnnotationString())
        print("\n")
