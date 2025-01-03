import libsbml as ls
import logging
import os
import pandas as pd
import sys
import unittest
import uuid
from pathlib import Path

from sbmlpbkutils import PbkModelValidator, PbkModelAnnotator
from sbmlpbkutils import ErrorCode, StatusLevel

sys.path.append('../sbmlpbkutils/')

__test_models_path__ = './tests/models/'
__test_outputs_path__ = './tests/__testoutputs__'

class PbkModelValidatorTests(unittest.TestCase):

    def setUp(self):
        from pathlib import Path
        Path(__test_outputs_path__).mkdir(parents=True, exist_ok=True)

    def test_validate_simple(self):
        sbml_file = os.path.join(__test_models_path__, 'simple.sbml')
        validator = PbkModelValidator()
        sbml_basename = os.path.basename(sbml_file)
        log_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.validation.log'))
        logger = self._create_file_logger(log_file)
        validator.validate(sbml_file, logger)

    def test_validate_simple_annotated(self):
        sbml_file = os.path.join(__test_models_path__, 'simple.annotated.sbml')
        validator = PbkModelValidator()
        sbml_basename = os.path.basename(sbml_file)
        log_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.validation.log'))
        logger = self._create_file_logger(log_file)
        validator.validate(sbml_file, logger)

    def test_validate_compartment_valid(self):
        annotations_df = self._fake_single_annotation_record(
            'Gut',
            'compartment',
            'BQM_IS',
            'http://purl.obolibrary.org/obo/PBPKO_00477'
        )
        document = self._annotate_model('simple.sbml', annotations_df)
        validator = PbkModelValidator()
        element = document.getElementBySId('Gut')
        result = validator.check_element_annotation(element)
        self.assertTrue(result[0])
        self.assertFalse(result[1])

    def test_validate_compartment_not_valid(self):
        annotations_df = self._fake_single_annotation_record(
            'Gut',
            'compartment',
            'BQB_IS',
            'http://purl.obolibrary.org/obo/PBPKO_00477'
        )
        document = self._annotate_model('simple.sbml', annotations_df)
        validator = PbkModelValidator()
        element = document.getElementBySId('Gut')
        result = validator.check_element_annotation(element)
        self.assertFalse(result[0])
        self.assertEqual(result[1][0].code, ErrorCode.COMPARTMENT_MISSING_BQM_TERM)

    def test_validate_parameter_no_chebi(self):
        annotations_df = self._fake_single_annotation_record(
            'PCLiver',
            'parameter',
            'BQM_IS',
            'http://purl.obolibrary.org/obo/PBPKO_00165'
        )
        document = self._annotate_model('simple.sbml', annotations_df)
        validator = PbkModelValidator()
        element = document.getElementBySId('PCLiver')
        result = validator.check_element_annotation(element)
        self.assertFalse(result[0])
        self.assertEqual(result[1][0].code, ErrorCode.PARAMETER_MISSING_BQB_IS_TERM)

    def test_validate_parameter_valid(self):
        annotations_df = pd.concat([
            self._fake_single_annotation_record(
                'PCLiver',
                'parameter',
                'BQM_IS',
                'http://purl.obolibrary.org/obo/PBPKO_00165'
            ),
            self._fake_single_annotation_record(
                'PCLiver',
                'parameter',
                'BQB_IS',
                'http://purl.obolibrary.org/obo/CHEBI_25212'
            )
        ])
        document = self._annotate_model('simple.sbml', annotations_df)
        validator = PbkModelValidator()
        element = document.getElementBySId('PCLiver')
        result = validator.check_element_annotation(element)
        self.assertTrue(result[0])
        self.assertFalse(result[1])

    def test_validate_parameter_invalid(self):
        annotations_df = self._fake_single_annotation_record(
            'PCLiver',
            'parameter',
            'BQB_IS',
            'http://purl.obolibrary.org/obo/PBPKO_00165'
        )
        document = self._annotate_model('simple.sbml', annotations_df)
        validator = PbkModelValidator()
        element = document.getElementBySId('PCLiver')
        result = validator.check_element_annotation(element)
        self.assertFalse(result[0])
        self.assertEqual(result[1][0].level, StatusLevel.ERROR)
        self.assertEqual(result[1][0].code, ErrorCode.PARAMETER_MISSING_BQM_TERM)

    def test_validate_parameter_warning(self):
        '''
        Annotation of internal parameters is not mandatory. Validation should yield a warning.
        '''
        sbml_file = os.path.join(__test_models_path__, 'simple.sbml') 
        document = ls.readSBML(sbml_file)
        element = document.getElementBySId('QC')
        validator = PbkModelValidator()
        result = validator.check_element_annotation(element)
        self.assertTrue(result[0])
        self.assertEqual(result[1][0].level, StatusLevel.WARNING)
        self.assertEqual(result[1][0].code, ErrorCode.PARAMETER_MISSING_BQM_TERM)

    def _fake_single_annotation_record(
        self,
        element_id = 'Gut',
        element_type = 'compartment',
        qualifier = 'BQM_IS',
        iri = 'http://purl.obolibrary.org/obo/UBERON_0000178'
    ) -> pd.DataFrame:
        return pd.DataFrame({
            'element_id': [f'{element_id}'],
            'sbml_type': [f'{element_type}'],
            'element_name': ['XXX'],
            'unit': ['L'],
            'annotation_type': ['rdf'],
            'qualifier': [f'{qualifier}'],
            'URI': [f'{iri}']
        })

    def _annotate_model(
        self,
        filename: str,
        annotations_df: pd.DataFrame
    ) -> ls.SBMLDocument:
        sbml_file = os.path.join(__test_models_path__, filename) 
        document = ls.readSBML(sbml_file)
        annotator = PbkModelAnnotator()
        logger = logging.getLogger(__name__)
        document = annotator.set_model_annotations(document, annotations_df, logger)
        return document

    def _create_file_logger(self, logfile: str) -> logging.Logger:
        logger = logging.getLogger(uuid.uuid4().hex)
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(logfile, 'w+')
        formatter = logging.Formatter('[%(levelname)s] - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

if __name__ == '__main__':
    unittest.main()
