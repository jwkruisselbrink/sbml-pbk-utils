import os
from pathlib import Path
from typing import List
import libsbml as ls
import numpy as np
import pandas as pd
from logging import Logger
from sbmlutils import utils
from sbmlutils.metadata.annotator import ModelAnnotator, ExternalAnnotation
from pymetadata.core.annotation import RDFAnnotation as Annotation
from . import UnitDefinitions

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
            df = PbkModelAnnotator.read_annotations_df(annotations_file, logger)
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
        logger: Logger
    ) -> ls.SBMLDocument:
        """Annotate the units of the SBML file using the annotations
        file and write results to the specified out file."""

        model = document.getModel()

        logger.info(f'Start model annoation: total {len(annotations_df.index)} annotation records')

        # Read model units
        units_dict = dict()
        for unit_def in model.getListOfUnitDefinitions():
            units_dict[unit_def.getId()] = unit_def

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
            element_id = str(row["element_id"])
            sbml_type = str(row["sbml_type"])

            # Skip records with empty URI field
            if row['resource'] is not None:
                if row['annotation_type'] != 'rdf':
                    msg = f"Unsupported annotation type [{row['annotation_type']}]."
                    logger.critical(msg)
                    raise ValueError(msg)
                annotation = ExternalAnnotation(row)
            else:
                annotation = None

            if sbml_type == "document":
                elements = [document]
            elif (element_id):
                elements = self.get_elements_by_pattern(
                    model,
                    sbml_type,
                    element_id,
                    logger
                )
                if not elements:
                    logger.error(f'Could not find {sbml_type} element with identifier "{element_id}".')

            for element in elements:
                # If unit field is not empty, try set element unit
                if (row["unit"] is not None):
                    self.set_element_unit(
                        document,
                        element,
                        element_id,
                        row["unit"],
                        units_dict,
                        True,
                        logger
                    )

                # If name is not empty, try to set element name
                if ("element_name" in row \
                    and row["element_name"] is not None
                    and row["sbml_type"] != "document"):
                    # If description field is not empty, try set element name
                    self.set_element_name(
                        element,
                        row["element_name"],
                        True,
                        logger
                    )

                # Set annotations
                if annotation is not None:
                    if annotation.annotation_type == "rdf":
                        rdf_annotation = Annotation(
                            qualifier=annotation.qualifier,
                            resource=annotation.resource  # type: ignore
                        )
                        self.annotate_sbase(element, rdf_annotation, logger)

                        # write SBO terms based on the SBO RDF
                        if rdf_annotation.collection == "sbo":
                            element.setSBOTerm(rdf_annotation.term)
                    else:
                        msg = f'Annotation type not supported: "{annotation.annotation_type}"'
                        logger.critical(msg)
                        raise ValueError(msg)

        return document

    def annotate_sbase(
        self,
        element: ls.SBase, 
        annotation: Annotation,
        logger: Logger
    ) -> None:
        """Annotate SBase based on given annotation data.
        """
        qualifier, resource = annotation.qualifier.value, annotation.resource_normalized
        cv: ls.CVTerm = ls.CVTerm()

        # set correct type of qualifier
        if isinstance(qualifier, str):
            if qualifier.startswith("BQB"):
                cv.setQualifierType(ls.BIOLOGICAL_QUALIFIER)
                sbml_qualifier = ModelAnnotator.get_SBMLQualifier(qualifier, "BQB")
                success = self.is_libsbml_operation_success(cv.setBiologicalQualifierType(sbml_qualifier))
                if not success:
                    logger.error(f"Failed to set [{qualifier}] resource [{resource}] for {element}.")
                    return
            elif qualifier.startswith("BQM"):
                cv.setQualifierType(ls.MODEL_QUALIFIER)
                sbml_qualifier = ModelAnnotator.get_SBMLQualifier(qualifier, "BQM")
                success = self.is_libsbml_operation_success(cv.setModelQualifierType(sbml_qualifier))
                if not success:
                    logger.error(f"Failed to set [{qualifier}] resource [{resource}] for {element}.")
                    return
            else:
                msg = f"Failed to set [{qualifier}] resource [{resource}] for {element}: unsupported qualifier."
                logger.error(msg)
                return
        else:
            msg = (
                f"Failed to set [{qualifier}] resource [{resource}] for {element}: "
                f"qualifier is not a string, but: [{qualifier}] of type [{type(qualifier)}]."
            )
            logger.error(msg)
            return

        # meta id has to be set
        if not element.isSetMetaId():
            element.setMetaId(utils.create_metaid(element))

        success = self.is_libsbml_operation_success(cv.addResource(resource))
        success = self.is_libsbml_operation_success(element.addCVTerm(cv))

        if not success:
            logger.error(f"Failed to add [{qualifier}] resource [{resource}] to {element}.")
        else:
            logger.info(f"Add [{qualifier}] resource [{resource}] to {element}.")

    def is_libsbml_operation_success(self, value: int) -> bool:
        valid = True
        if value is None:
            valid = False
        elif isinstance(value, int):
            if value != ls.LIBSBML_OPERATION_SUCCESS:
                valid = False
        return valid

    def set_element_unit(
        self,
        doc: ls.SBMLDocument,
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
            model = doc.getModel()
            uDef = self.get_or_add_unit_definition(doc, unit_id, units_dict, logger)
            if element_id == "timeUnits":
                if not model.isSetTimeUnits() or overwrite:
                    logger.info(f"Set model time unit [{unit_id}].")
                    model.setTimeUnits(uDef.getId())
                elif model.isSetTimeUnits():
                    logger.info(f"Did not set model time unit [{unit_id}]: unit already set.")
            elif element_id == "substanceUnits":
                if not model.isSetSubstanceUnits() or overwrite:
                    logger.info(f"Set model substances unit [{unit_id}].")
                    model.setSubstanceUnits(uDef.getId())
                elif model.isSetSubstanceUnits():
                    logger.info(f"Did not set model substances unit [{unit_id}]: unit already set.")
            elif element_id == "volumeUnits":
                if not model.isSetVolumeUnits() or overwrite:
                    logger.info(f"Set model volume unit [{unit_id}].")
                    model.setVolumeUnits(uDef.getId())
                elif model.isSetVolumeUnits():
                    logger.info(f"Did not set model volume unit [{unit_id}]: unit already set.")
            else:
                logger.info(f"Did not set unit [{unit_id}] for root level element [{element_id}]: not a valid document level element identifier.")

        else:
            if not element.isSetUnits() or overwrite:
                uDef = self.get_or_add_unit_definition(doc, unit_id, units_dict, logger)
                if (uDef):
                    logger.info(f"Set unit of {element} to [{unit_id}].")
                    element.setUnits(uDef.getId())
                elif element.isSetUnits():
                    logger.info(f"Did not set unit [{unit_id}] for {element}: unit already set.")
            else:
                logger.info(f"Name for {element} already set, not overwriting.")

    def set_element_name(
        self,
        element: ls.SBase,
        name: str,
        overwrite: bool,
        logger: Logger
    ) -> None:
        """Set element unit of element with specified id and type to the specfied unit."""
        if not element.isSetName() or overwrite:
            logger.info(f'Set name of {element} to "{name}".')
            element.setName(name)
        else:
            logger.info(f"Name for {element} already set, not overwriting.")

    def get_elements_by_pattern(
        self,
        model: ls.Model,
        sbml_type: str,
        pattern: str,
        logger: Logger
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

    def get_or_add_unit_definition(
        self,
        doc: ls.SBMLDocument,
        unitId: str,
        unitsDictionary: dict,
        logger: Logger
    ):
        """Tries to get the unit definition for the specified unit id from the SBML document.
        The unit definition will be created and added to the document if it does not yet exist.
        """
        if (unitId not in unitsDictionary):
            unitDef = self.find_unit_definition(unitId)
            if (unitDef is None):
                logger.error(f"Failed to set unit [{unitId}]: unknown unit definition!")
                return
            model = doc.getModel()
            uDef = model.getUnitDefinition(unitDef["id"])
            if (not uDef):
                unitDefId = unitDef["id"]
                logger.info(f"Adding unit definition [{unitDefId}] for [{unitId}]")
                uDef = model.createUnitDefinition()
                uDef.setId(unitDefId)
                for unitPart in unitDef["units"]:
                    u = uDef.createUnit()
                    u.setKind(unitPart["kind"])
                    u.setExponent(unitPart["exponent"])
                    u.setMultiplier(unitPart["multiplier"])
                    u.setScale(unitPart["scale"])
            unitsDictionary[unitId] = uDef
        return unitsDictionary[unitId]

    def find_unit_definition(
        self,
        str: str
    ):
        """Find unit definition matching the provided string."""
        res = None
        for index, value in enumerate(UnitDefinitions):
            if any(val.lower() == str.lower() for val in value['synonyms']):
                res = value
                break
        return res

    @staticmethod
    def read_annotations_df(
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
