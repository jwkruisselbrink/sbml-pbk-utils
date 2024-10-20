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

    def test_remove_all_annotations(self):
        sbml_file = os.path.join(__test_models_path__, 'euromix.annotated.sbml') 
        annotator = PbkModelAnnotator()
        document = ls.readSBML(sbml_file)
        annotator.remove_all_annotations(document)
        sbml_basename = os.path.basename(sbml_file)
        out_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.clean.sbml'))
        ls.writeSBML(document, out_file)

    def test_annotate_document_invalid(self):
        annotations_df = pd.DataFrame({
            'xxx': ['A', 'B', 'C', 'D'],
            'yyy': [20, 21, 19, 18]
        })
        with self.assertRaises(ValueError):
            _ = self.annotate_model('example.sbml', annotations_df, 'annotation_invalid_doc')

    def test_annotate_document_set_unit(self):
        annotations_df = self.fake_single_annotation_record()
        annotations_df.at[0, 'element_id'] = 'Blood'
        annotations_df.at[0, 'unit'] = 'mL'
        document = self.annotate_model('example.sbml', annotations_df, 'annotation_set_unit')
        self.assertIsNotNone(document)
        model = document.getModel()
        unit_defs = []
        for i in range(0, model.getNumUnitDefinitions()):
            if (model.getUnitDefinition(i).getId() == 'MilliL'):
                unit_def = model.getUnitDefinition(i)
                break
        self.assertIsNotNone(unit_def)
        element = model.getElementBySId('Blood')
        self.assertEqual(element.getUnits(), 'MilliL')

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

    def test_update_element_info_set_name(self):
        # Arrange
        sbml_file = os.path.join(__test_models_path__, 'euromix.annotated.sbml') 
        annotator = PbkModelAnnotator()
        document = ls.readSBML(sbml_file)
        logger = logging.getLogger(__name__)
        element_id = 'Air'
        new_name = 'XXX'

        # Act
        annotator.update_element_info(document, element_id, logger, new_name)

        # Assert
        model = document.getModel()
        element = model.getElementBySId(element_id)
        element_name = element.getName()
        self.assertEqual(element_name, new_name)

    def test_update_element_info_set_unit(self):
        # Arrange
        sbml_file = os.path.join(__test_models_path__, 'euromix.annotated.sbml') 
        annotator = PbkModelAnnotator()
        document = ls.readSBML(sbml_file)
        logger = logging.getLogger(__name__)
        element_id = 'Air'
        new_unit = 'MilliL'

        # Act
        annotator.update_element_info(document, element_id, logger, unit_id=new_unit)

        # Assert
        model = document.getModel()
        element = model.getElementBySId(element_id)
        element_unit = element.getUnits()
        self.assertEqual(element_unit, new_unit)

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
