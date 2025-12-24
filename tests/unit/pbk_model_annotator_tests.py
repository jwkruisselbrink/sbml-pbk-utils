import logging
import unittest
import os
from pathlib import Path
import libsbml as ls
from parameterized import parameterized
import pandas as pd

from tests.conf import TEST_OUTPUT_PATH, TEST_MODELS_PATH
from tests.helpers import create_file_logger
from sbmlpbkutils import PbkModelAnnotator

class PbkModelAnnotatorTests(unittest.TestCase):

    def setUp(self):
        self.out_path = os.path.join(TEST_OUTPUT_PATH, 'annotator_tests')
        os.makedirs(self.out_path, exist_ok=True)

    def test_annotate_cff_file(self):
        # Arrange
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.sbml')
        document = ls.readSBML(sbml_file)
        cff_file = './CITATION.cff'
        annotator = PbkModelAnnotator()

        # Act
        annotator.annotate(
            document,
            cff_file = cff_file,
            logger = logging.getLogger(__name__)
        )

        # Assert
        model = document.getModel()
        model_history = model.getModelHistory()
        model_creators = model_history.getListCreators()
        self.assertGreaterEqual(len(model_creators), 1)

        # Write annotated SBML file to test results
        sbml_basename = os.path.basename(sbml_file)
        out_file = os.path.join(self.out_path, Path(sbml_basename).with_suffix('.cff.sbml'))
        ls.writeSBML(document, out_file)

    def test_annotate_document_invalid(self):
        annotations_df = pd.DataFrame({
            'xxx': ['A', 'B', 'C', 'D'],
            'yyy': [20, 21, 19, 18]
        })
        with self.assertRaises(ValueError):
            _ = self._annotate_model('simple.sbml', annotations_df, 'annotation_invalid_doc')

    def test_annotate_document_set_unit(self):
        annotations_df = self._fake_single_annotation_record()
        annotations_df.at[0, 'element_id'] = 'Blood'
        annotations_df.at[0, 'unit'] = 'mL'
        document = self._annotate_model('simple.sbml', annotations_df, 'annotation_set_unit')
        self.assertIsNotNone(document)
        model = document.getModel()
        for i in range(0, model.getNumUnitDefinitions()):
            if model.getUnitDefinition(i).getId() == 'MilliL':
                unit_def = model.getUnitDefinition(i)
                break
        self.assertIsNotNone(unit_def)
        element = model.getElementBySId('Blood')
        self.assertEqual(element.getUnits(), 'MilliL')

    def test_annotate_document_invalid_rdf(self):
        annotations_df = self._fake_single_annotation_record()
        annotations_df.at[0, 'annotation_type'] = 'xxx'
        document = self._annotate_model('simple.sbml', annotations_df, 'annotation_invalid_rdf')
        self.assertIsNotNone(document)

    def test_annotate_document_invalid_qualifier(self):
        annotations_df = self._fake_single_annotation_record()
        annotations_df.at[0, 'qualifier'] = 'BQB_IS_RELATED_TO'
        document = self._annotate_model('simple.sbml', annotations_df, 'annotation_invalid_qualifier')
        self.assertIsNotNone(document)

    def test_annotate_document_invalid_uri(self):
        annotations_df = self._fake_single_annotation_record()
        annotations_df.at[0, 'URI'] = 'UBERON_0000111'
        document = self._annotate_model('simple.sbml', annotations_df, 'annotation_invalid_uri')
        self.assertIsNotNone(document)

    def test_set_element_name(self):
        # Arrange
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.sbml')
        annotator = PbkModelAnnotator()
        document = ls.readSBML(sbml_file)
        element_id = 'Gut'
        new_name = 'XXX'

        # Act
        annotator.set_element_name(document, element_id, new_name)

        # Assert
        model = document.getModel()
        element = model.getElementBySId(element_id)
        element_name = element.getName()
        self.assertEqual(element_name, new_name)

    def test_set_element_unit(self):
        # Arrange
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.sbml')
        annotator = PbkModelAnnotator()
        document = ls.readSBML(sbml_file)
        logger = logging.getLogger(__name__)
        element_id = 'Gut'
        new_unit = 'MilliL'

        # Act
        annotator.set_element_unit(document, element_id, new_unit, logger)

        # Assert
        model = document.getModel()
        element = model.getElementBySId(element_id)
        element_unit = element.getUnits()
        self.assertEqual(element_unit, new_unit)

    @parameterized.expand([
        ("Liver"),
        ("Blood")
    ])
    def test_remove_element_rdf_annotation(self, element_id):
        # Arrange
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.annotated.sbml')
        annotator = PbkModelAnnotator()
        document = ls.readSBML(sbml_file)
        logger = logging.getLogger(__name__)

        # Assert (check whether annotation currently exists)
        model = document.getModel()
        element = model.getElementBySId(element_id)
        cv_terms = PbkModelAnnotator.get_cv_terms(element, ls.MODEL_QUALIFIER, ls.BQM_IS)
        self.assertIn("http://purl.obolibrary.org/obo/PBPKO_", cv_terms[0]['uri'])

        # Act
        annotator.remove_element_rdf_annotation(
            document,
            element_id,
            'BQM_IS',
            logger
        )

        # Assert
        model = document.getModel()
        element = model.getElementBySId(element_id)
        cv_terms = PbkModelAnnotator.get_cv_terms(element, ls.MODEL_QUALIFIER, ls.BQM_IS)
        self.assertEqual(len(cv_terms), 0)

        # Write to SBML
        sbml_out = os.path.join(self.out_path, f'test_remove_element_rdf_annotation_{element_id}.sbml')
        ls.writeSBML(document, sbml_out)

    def test_remove_element_rdf_annotation_already_empty(self):
        # Arrange
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.sbml')
        annotator = PbkModelAnnotator()
        document = ls.readSBML(sbml_file)
        logger = logging.getLogger(__name__)
        element_id = 'Gut'

        # Act
        annotator.remove_element_rdf_annotation(
            document,
            element_id,
            'BQM_IS',
            logger
        )

        # Assert
        model = document.getModel()
        element = model.getElementBySId(element_id)
        cv_terms = PbkModelAnnotator.get_cv_terms(element, ls.MODEL_QUALIFIER, ls.BQM_IS)
        self.assertEqual(len(cv_terms), 0)

    def test_set_model_rdf_annotation(self):
        # Arrange
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.sbml')
        annotator = PbkModelAnnotator()
        document = ls.readSBML(sbml_file)
        logger = logging.getLogger(__name__)

        # Act
        annotator.set_model_rdf_annotation(
            document,
            'BQB_HAS_TAXON',
            "http://identifiers.org/taxonomy/40674",
            logger
        )

        # Assert
        model = document.getModel()
        cv_terms = PbkModelAnnotator.get_cv_terms(model, ls.BIOLOGICAL_QUALIFIER, ls.BQB_HAS_TAXON)
        self.assertEqual(cv_terms[0]['uri'], "https://identifiers.org/taxonomy/40674")

    def test_set_element_rdf_annotation(self):
        # Arrange
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.sbml')
        annotator = PbkModelAnnotator()
        document = ls.readSBML(sbml_file)
        logger = logging.getLogger(__name__)
        element_id = 'Gut'

        # Act
        annotator.set_element_rdf_annotation(
            document,
            element_id,
            'BQM_IS',
            "http://purl.obolibrary.org/obo/PBPKO_00477",
            logger
        )

        # Assert
        model = document.getModel()
        element = model.getElementBySId(element_id)
        cv_terms = PbkModelAnnotator.get_cv_terms(element, ls.MODEL_QUALIFIER, ls.BQM_IS)
        self.assertEqual(cv_terms[0]['uri'], "http://purl.obolibrary.org/obo/PBPKO_00477")

    def test_set_element_rdf_annotation_overwrite(self):
        # Arrange
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.sbml')
        annotator = PbkModelAnnotator()
        document = ls.readSBML(sbml_file)
        logger = logging.getLogger(__name__)
        element_id = 'Gut'

        # Act
        annotator.set_element_rdf_annotation(
            document,
            element_id,
            'BQM_IS',
            "http://purl.obolibrary.org/obo/PBPKO_00450",
            logger
        )
        annotator.set_element_rdf_annotation(
            document,
            element_id,
            'BQM_IS',
            "http://purl.obolibrary.org/obo/PBPKO_00477",
            logger,
            True
        )

        # Assert
        model = document.getModel()
        element = model.getElementBySId(element_id)
        cv_terms = PbkModelAnnotator.get_cv_terms(element, ls.MODEL_QUALIFIER, ls.BQM_IS)
        self.assertEqual(cv_terms[0]['uri'], "http://purl.obolibrary.org/obo/PBPKO_00477")

    def test_set_model_creators(self):
        # Arrange
        creators = [
            {
                'given-names': 'John',
                'family-names': 'Doe',
                'affiliation': 'ACME PBK models',
                'email': 'john.doe@acme-pbk.org'
            }
        ]
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.sbml')
        document = ls.readSBML(sbml_file)
        annotator = PbkModelAnnotator()

        # Act
        annotator.set_model_creators(document, creators)

        # Assert
        model = document.getModel()
        model_history = model.getModelHistory()
        model_creators = model_history.getListCreators()
        self.assertEqual(len(model_creators), 1)
        self.assertEqual(model_creators[0].getFamilyName(), "Doe")
        self.assertEqual(model_creators[0].getGivenName(), "John")
        self.assertEqual(model_creators[0].getOrganization(), "ACME PBK models")
        self.assertEqual(model_creators[0].getEmail(), "john.doe@acme-pbk.org")

    def _fake_single_annotation_record(self) -> pd.DataFrame:
        return pd.DataFrame({
            'element_id': ['Blood'],
            'sbml_type': ['compartment'],
            'element_name': ['Blood'],
            'unit': ['L'],
            'annotation_type': ['rdf'],
            'qualifier': ['BQB_IS'],
            'URI': ['http://purl.obolibrary.org/obo/UBERON_0000178']
        })

    def _annotate_model(
        self,
        filename: str,
        annotations_df: pd.DataFrame,
        test_id: str
    ) -> ls.SBMLDocument:
        model_folder = os.path.join(TEST_MODELS_PATH, Path(filename).stem)
        sbml_file = os.path.join(model_folder, filename)
        document = ls.readSBML(sbml_file)
        sbml_basename = os.path.basename(sbml_file)
        log_file = os.path.join(self.out_path, Path(sbml_basename).with_suffix(f'.{test_id}.log'))
        logger = create_file_logger(log_file)
        annotator = PbkModelAnnotator()
        document = annotator.set_model_annotations(document, annotations_df, logger)
        return document

if __name__ == '__main__':
    unittest.main()
