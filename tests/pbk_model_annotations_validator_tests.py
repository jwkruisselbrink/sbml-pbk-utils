import unittest
import sys
import os
import logging
import libsbml as ls
import pandas as pd
from sbmlpbkutils.pbk_model_annotations_validator import PbkModelAnnotationsValidator
from sbmlpbkutils.pbk_model_annotator import PbkModelAnnotator
from sbmlpbkutils.validation_record import ErrorCode, StatusLevel
sys.path.append('../sbmlpbkutils/')

__test_models_path__ = './tests/models/'

class PbkModelAnnotationsValidatorTests(unittest.TestCase):

    def test_validate_compartment_valid(self):
        annotations_df = self.fake_single_annotation_record(
            'Gut',
            'compartment',
            'BQM_IS',
            'http://purl.obolibrary.org/obo/PBPKO_00477'
        )
        document = self.annotate_model('simple.sbml', annotations_df)
        validator = PbkModelAnnotationsValidator()
        element = document.getElementBySId('Gut')
        result = validator.check_element_annotation(element)
        self.assertTrue(result[0])
        self.assertFalse(result[1])

    def test_validate_compartment_not_valid(self):
        annotations_df = self.fake_single_annotation_record(
            'Gut',
            'compartment',
            'BQB_IS',
            'http://purl.obolibrary.org/obo/PBPKO_00477'
        )
        document = self.annotate_model('simple.sbml', annotations_df)
        validator = PbkModelAnnotationsValidator()
        element = document.getElementBySId('Gut')
        result = validator.check_element_annotation(element)
        self.assertFalse(result[0])
        self.assertEqual(result[1][0].code, ErrorCode.COMPARTMENT_MISSING_BQM_TERM)

    def test_validate_parameter_valid(self):
        annotations_df = self.fake_single_annotation_record(
            'PCLiver',
            'parameter',
            'BQM_IS',
            'http://purl.obolibrary.org/obo/PBPKO_00165'
        )
        document = self.annotate_model('simple.sbml', annotations_df)
        validator = PbkModelAnnotationsValidator()
        element = document.getElementBySId('PCLiver')
        result = validator.check_element_annotation(element)
        self.assertTrue(result[0])
        self.assertFalse(result[1])

    def test_validate_parameter_invalid(self):
        annotations_df = self.fake_single_annotation_record(
            'PCLiver',
            'parameter',
            'BQB_IS',
            'http://purl.obolibrary.org/obo/PBPKO_00165'
        )
        document = self.annotate_model('simple.sbml', annotations_df)
        validator = PbkModelAnnotationsValidator()
        element = document.getElementBySId('PCLiver')
        result = validator.check_element_annotation(element)
        self.assertFalse(result[0])
        self.assertEqual(result[1][0].level, StatusLevel.ERROR)
        self.assertEqual(result[1][0].code, ErrorCode.PARAMETER_MISSING_BQM_TERM)

    def fake_single_annotation_record(
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

    def annotate_model(
        self,
        filename: str,
        annotations_df: pd.DataFrame
    ) -> ls.SBMLDocument:
        sbml_file = os.path.join(__test_models_path__, filename) 
        document = ls.readSBML(sbml_file)
        annotator = PbkModelAnnotator()
        logger = logging.getLogger(__name__)
        document = annotator.annotate_document(document, annotations_df, logger)
        return document

if __name__ == '__main__':
    unittest.main()
