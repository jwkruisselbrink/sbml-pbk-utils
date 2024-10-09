import unittest
import uuid
import sys
import os
import logging
import libsbml as ls
import pandas as pd
from pathlib import Path
from sbmlpbkutils.pbk_model_annotator import PbkModelAnnotator

sys.path.append('../sbmlpbkutils/')

__test_outputs_path__ = './tests/__testoutputs__'
__test_models_path__ = './tests/models/'

class PbkModelAnnotatorTests(unittest.TestCase):

    def create_file_logger(self, logfile: str) -> logging.Logger:
        logger = logging.getLogger(uuid.uuid4().hex)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(logfile, 'w+')
        formatter = logging.Formatter('[%(levelname)s] - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    def setUp(self):
        from pathlib import Path
        Path(__test_outputs_path__).mkdir(parents=True, exist_ok=True)

    @classmethod
    def setUpClass(cls):
        cls.sbml_files = []
        files = os.listdir(__test_models_path__)
        for file in files:
            if file.endswith('.sbml') and not file.endswith('annotated.sbml'):
                cls.sbml_files.append(__test_models_path__ + file)

    def test_annotate(self):
        annotator = PbkModelAnnotator()
        for sbml_file in self.sbml_files:
            sbml_basename = os.path.basename(sbml_file)
            annotations_file = Path(sbml_file).with_suffix('.annotations.csv')
            log_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.annotation.log'))
            logger = self.create_file_logger(log_file)
            _ = annotator.annotate(sbml_file, annotations_file, logger)

    def test_annotate_document_invalid(self):
        annotator = PbkModelAnnotator()
        sbml_file = os.path.join(__test_models_path__, 'example.sbml') 
        document = ls.readSBML(sbml_file)
        annotations_df = pd.DataFrame({
            'xxx': ['A', 'B', 'C', 'D'],
            'yyy': [20, 21, 19, 18]
        })
        sbml_basename = os.path.basename(sbml_file)
        log_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.annotation_invalid.log'))
        logger = self.create_file_logger(log_file)
        with self.assertRaises(ValueError):
            annotator.annotate_document(document, annotations_df, logger)

    def test_annotate_document_invalid_rdf(self):
        annotator = PbkModelAnnotator()
        sbml_file = os.path.join(__test_models_path__, 'example.sbml') 
        document = ls.readSBML(sbml_file)
        annotations_df = pd.DataFrame({
            'element_id': ['Blood'],
            'sbml_type': ['compartment'],
            'element_name': ['Blood'],
            'unit': ['L'],
            'annotation_type': ['xxx'],
            'qualifier': ['BQB_IS'],
            'URI': ['http://purl.obolibrary.org/obo/UBERON_0000178']
        })
        sbml_basename = os.path.basename(sbml_file)
        log_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.annotation_invalid_rdf.log'))
        logger = self.create_file_logger(log_file)
        with self.assertRaises(ValueError):
            annotator.annotate_document(document, annotations_df, logger)

if __name__ == '__main__':
    unittest.main()
