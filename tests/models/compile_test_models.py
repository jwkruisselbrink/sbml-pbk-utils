import os
import uuid
import tellurium as te
import libsbml as ls
import logging
from pathlib import Path
import sys

sys.path.append("./")

from sbmlpbkutils import PbkModelValidator
from sbmlpbkutils import AnnotationsTemplateGenerator
from sbmlpbkutils import PbkModelAnnotator

def create_file_logger(logfile: str) -> logging.Logger:
    logger = logging.getLogger(uuid.uuid4().hex)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logfile, 'w+')
    formatter = logging.Formatter('[%(levelname)s] - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

for file in os.listdir('./tests/models/'):
    if file.endswith('.ant'):
        ant_file = os.path.join('./tests/models', file)
        sbml_file = Path(ant_file).with_suffix('.sbml')
        r = te.loada(ant_file)
        r.exportToSBML(sbml_file)

for file in os.listdir('./tests/models/'):
    if file.endswith('.sbml') and not file.endswith('annotated.sbml'):
        sbml_file = os.path.join('./tests/models', file)
        document = ls.readSBML(sbml_file)
        model = document.getModel()

        annotations_file = Path(sbml_file).with_suffix('.annotations.csv')
        if not os.path.exists(annotations_file):
            # create annotations (csv) file if it does not exist
            annotations_template_generator = AnnotationsTemplateGenerator()
            annotations = annotations_template_generator.generate(model)
            annotations.to_csv(annotations_file, index=False)

        annotations_log_file = Path(sbml_file).with_suffix('.annotations.log')
        annotated_sbml_file = Path(sbml_file).with_suffix('.annotated.sbml')
        annotator = PbkModelAnnotator()
        logger = create_file_logger(annotations_log_file)
        document = annotator.annotate(
            document,
            annotations_file,
            logger = logger
        )
        ls.writeSBML(document, str(annotated_sbml_file))

        validation_log_file = Path(sbml_file).with_suffix('.validation.log')
        validator = PbkModelValidator()
        logger = create_file_logger(validation_log_file)
        validator.validate(annotated_sbml_file, logger)
