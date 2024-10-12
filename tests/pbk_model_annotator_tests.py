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
            document = annotator.annotate(sbml_file, annotations_file, logger)
            self.assertIsNotNone(document)

    def test_annotate_document_invalid(self):
        annotator = PbkModelAnnotator()
        annotations_df = pd.DataFrame({
            'xxx': ['A', 'B', 'C', 'D'],
            'yyy': [20, 21, 19, 18]
        })
        with self.assertRaises(ValueError):
            _ = self.annotate_model('example.sbml', annotations_df, 'annotation_invalid_doc')

    def test_annotate_document_invalid_rdf(self):
        annotations_df = self.fake_single_annotation_record()
        annotations_df.at[0, 'annotation_type'] = 'xxx'
        document = self.annotate_model('example.sbml', annotations_df, 'annotation_invalid_rdf')
        self.assertIsNotNone(document)

    def test_annotate_document_invalid_qualifier(self):
        annotations_df = self.fake_single_annotation_record()
        annotations_df.at[0, 'qualifier'] = 'BQB_IS_RELATED_TO'
        document = self.annotate_model('example.sbml', annotations_df, 'annotation_invalid_qualifier')
        self.assertIsNotNone(document)

    def test_annotate_document_invalid_uri(self):
        annotations_df = self.fake_single_annotation_record()
        annotations_df.at[0, 'URI'] = 'UBERON_0000111'
        document = self.annotate_model('example.sbml', annotations_df, 'annotation_invalid_uri')
        self.assertIsNotNone(document)
        #PbkModelAnnotator.print_element_terms(document, 'Blood')

    def fake_single_annotation_record(self) -> pd.DataFrame:
        return pd.DataFrame({
            'element_id': ['Blood'],
            'sbml_type': ['compartment'],
            'element_name': ['Blood'],
            'unit': ['L'],
            'annotation_type': ['rdf'],
            'qualifier': ['BQB_IS'],
            'URI': ['http://purl.obolibrary.org/obo/UBERON_0000178']
        })

    def annotate_model(
        self,
        filename: str,
        annotations_df: pd.DataFrame,
        test_id: str
    ) -> ls.SBMLDocument:
        sbml_file = os.path.join(__test_models_path__, filename) 
        document = ls.readSBML(sbml_file)
        sbml_basename = os.path.basename(sbml_file)
        log_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix(f'.{test_id}.log'))
        logger = self.create_file_logger(log_file)
        annotator = PbkModelAnnotator()
        document = annotator.annotate_document(document, annotations_df, logger)
        return document

if __name__ == '__main__':
    unittest.main()
