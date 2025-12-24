import logging
import os
import unittest
import libsbml as ls
import pandas as pd

from tests.conf import TEST_MODELS_PATH
from sbmlpbkutils import PbkModelValidator, PbkModelAnnotator
from sbmlpbkutils import ErrorCode, ValidationStatus

class PbkModelValidatorTests(unittest.TestCase):

    def test_validate_compartment_valid(self):
        annotations_df = self._fake_single_annotation_record(
            'Gut',
            'compartment',
            'BQM_IS',
            'http://purl.obolibrary.org/obo/PBPKO_00477'
        )
        document = self._annotate_model('simple/simple.sbml', annotations_df)
        validator = PbkModelValidator()
        element = document.getElementBySId('Gut')
        result = validator.check_element_annotation(element)
        self.assertTrue(result.level == ValidationStatus.OK)

    def test_validate_compartment_not_valid(self):
        annotations_df = self._fake_single_annotation_record(
            'Gut',
            'compartment',
            'BQB_IS',
            'http://purl.obolibrary.org/obo/PBPKO_00477'
        )
        document = self._annotate_model('simple/simple.sbml', annotations_df)
        validator = PbkModelValidator()
        element = document.getElementBySId('Gut')
        result = validator.check_element_annotation(element)
        self.assertTrue(result.level == ValidationStatus.ERROR)
        self.assertEqual(result.code, ErrorCode.COMPARTMENT_MISSING_PBPKO_BQM_IS_TERM)

    def test_validate_parameter_no_chebi(self):
        annotations_df = self._fake_single_annotation_record(
            'PCLiver',
            'parameter',
            'BQM_IS',
            'http://purl.obolibrary.org/obo/PBPKO_00165'
        )
        document = self._annotate_model('simple/simple.sbml', annotations_df)
        validator = PbkModelValidator()
        element = document.getElementBySId('PCLiver')
        result = validator.check_element_annotation(element)
        self.assertTrue(result.level == ValidationStatus.ERROR)
        self.assertEqual(result.code, ErrorCode.PARAMETER_MISSING_CHEBI_BQB_IS_TERM)

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
        document = self._annotate_model('simple/simple.sbml', annotations_df)
        validator = PbkModelValidator()
        element = document.getElementBySId('PCLiver')
        result = validator.check_element_annotation(element)
        self.assertTrue(result.level == ValidationStatus.OK)

    def test_validate_parameter_invalid(self):
        annotations_df = self._fake_single_annotation_record(
            'PCLiver',
            'parameter',
            'BQB_IS',
            'http://purl.obolibrary.org/obo/PBPKO_00165'
        )
        document = self._annotate_model('simple/simple.sbml', annotations_df)
        validator = PbkModelValidator()
        element = document.getElementBySId('PCLiver')
        result = validator.check_element_annotation(element)
        self.assertEqual(result.level, ValidationStatus.ERROR)
        self.assertEqual(result.code, ErrorCode.PARAMETER_MISSING_PBPKO_BQM_IS_TERM)

    def test_validate_parameters_duplicate_use(self):
        annotations_df = pd.concat([
            self._fake_single_annotation_record(
                'VLc',
                'parameter',
                'BQM_IS',
                'http://purl.obolibrary.org/obo/PBPKO_00106'
            ),
            self._fake_single_annotation_record(
                'VRc',
                'parameter',
                'BQM_IS',
                'http://purl.obolibrary.org/obo/PBPKO_00106'
            )
        ])
        document = self._annotate_model('simple/simple.sbml', annotations_df)
        validator = PbkModelValidator()
        result = validator.check_parameter_annotations(document)
        self.assertTrue(any(r.level == ValidationStatus.ERROR for r in result))
        records = [r for r in result if r.code == ErrorCode.PARAMETER_MULTIPLE_ANNOTATION_USE]
        self.assertEqual(records[0].level, ValidationStatus.ERROR)
        self.assertEqual(records[0].code, ErrorCode.PARAMETER_MULTIPLE_ANNOTATION_USE)

    def test_validate_parameters_allowed_duplicate_use(self):
        annotations_df = pd.concat([
            self._fake_single_annotation_record(
                'PCLiver_P',
                'parameter',
                'BQM_IS',
                'http://purl.obolibrary.org/obo/PBPKO_00577'
            ),
            self._fake_single_annotation_record(
                'PCLiver_P',
                'parameter',
                'BQB_IS',
                'urn:miriam:chebi:24431'
            ),
            self._fake_single_annotation_record(
                'PCLiver_M',
                'parameter',
                'BQM_IS',
                'http://purl.obolibrary.org/obo/PBPKO_00577'
            ),
            self._fake_single_annotation_record(
                'PCLiver_M',
                'parameter',
                'BQB_IS',
                'urn:miriam:chebi:CHEBI:25212'
            )
        ])
        document = self._annotate_model('simple_metab/simple_metab.sbml', annotations_df)
        validator = PbkModelValidator()
        result = validator.check_parameter_annotations(document)
        messages = [r for r in result if r.code == ErrorCode.PARAMETER_MULTIPLE_ANNOTATION_USE]
        self.assertEqual(len(messages), 0)

    def test_validate_parameters_duplicate_use_chemical_specific(self):
        annotations_df = pd.concat([
            self._fake_single_annotation_record(
                'PCLiver',
                'parameter',
                'BQM_IS',
                'http://purl.obolibrary.org/obo/PBPKO_00165'
            ),
            self._fake_single_annotation_record(
                'PCRest',
                'parameter',
                'BQM_IS',
                'http://purl.obolibrary.org/obo/PBPKO_00165'
            )
        ])
        document = self._annotate_model('simple/simple.sbml', annotations_df)
        validator = PbkModelValidator()
        result = validator.check_parameter_annotations(document)
        messages = [r for r in result if r.code == ErrorCode.PARAMETER_MULTIPLE_ANNOTATION_USE]
        self.assertEqual(len(messages), 0)

    def test_validate_parameter_warning(self):
        '''Annotation of internal parameters is not mandatory. Validation
        should yield a warning.'''
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.sbml')
        document = ls.readSBML(sbml_file)
        element = document.getElementBySId('QC')
        validator = PbkModelValidator()
        result = validator.check_element_annotation(element)
        self.assertEqual(result.level, ValidationStatus.WARNING)
        self.assertEqual(result.code, ErrorCode.PARAMETER_MISSING_PBPKO_BQM_IS_TERM)

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
        sbml_file = os.path.join(TEST_MODELS_PATH, filename)
        document = ls.readSBML(sbml_file)
        annotator = PbkModelAnnotator()
        logger = logging.getLogger(__name__)
        document = annotator.set_model_annotations(document, annotations_df, logger)
        return document

if __name__ == '__main__':
    unittest.main()
