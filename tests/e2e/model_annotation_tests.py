import glob
import os
import unittest
from pathlib import Path
import libsbml as ls

from tests.conf import TEST_OUTPUT_PATH, TEST_MODELS_PATH
from tests.helpers import create_file_logger
from sbmlpbkutils import PbkModelAnnotator, PbkModelValidator, AnnotationsTemplateGenerator

class ModelAnnotationTests(unittest.TestCase):

    def setUp(self):
        self.out_path = os.path.join(TEST_OUTPUT_PATH, 'annotation')
        os.makedirs(self.out_path, exist_ok=True)

    def test_annotation(self):
        sbml_files = glob.glob(f'{TEST_MODELS_PATH}/**/*[!annotated].sbml', recursive=True)
        for sbml_file in sbml_files:
            sbml_basename = os.path.basename(sbml_file)
            annotations_file = Path(sbml_file).with_suffix('.annotations.csv')

            # Create file logger
            log_file = os.path.join(self.out_path, Path(sbml_basename).with_suffix('.annotation.log'))
            logger = create_file_logger(log_file)

            # Load file and annotate
            document = ls.readSBML(sbml_file)
            annotator = PbkModelAnnotator()
            annotator.annotate(
                document,
                annotations_file = str(annotations_file),
                logger=logger
            )
            self.assertIsNotNone(document)

            # Write annotated SBML file
            out_file = os.path.join(self.out_path, Path(sbml_basename).with_suffix('.annotated.sbml'))
            ls.writeSBML(document, out_file)

    def test_clear_annotations(self):
        models = glob.glob(f'{TEST_MODELS_PATH}/**/*.annotated.sbml', recursive=True)
        for sbml_file in models:
            # Load SBML file
            document = ls.readSBML(sbml_file)

            # Create annotator and clean
            annotator = PbkModelAnnotator()
            annotator.clear_all_element_annotations(document)
            sbml_basename = os.path.basename(sbml_file)

            # Write cleaned SBML file
            out_file = os.path.join(self.out_path, Path(sbml_basename).with_suffix('.clean.sbml'))
            ls.writeSBML(document, out_file)

    def test_validate(self):
        # Iterate over all SBML models and validate
        sbml_files = glob.glob(f'{TEST_MODELS_PATH}/**/*.sbml', recursive=True)
        for sbml_file in sbml_files:
            sbml_basename = os.path.basename(sbml_file)

            # Create file logger
            log_file = os.path.join(self.out_path, Path(sbml_basename).with_suffix('.validation.log'))
            logger = create_file_logger(log_file)

            # Create validator and validate
            validator = PbkModelValidator()
            validator.validate(sbml_file, logger)

    def test_export_annotations_csv(self):
        generator = AnnotationsTemplateGenerator()
        models = glob.glob(f'{TEST_MODELS_PATH}/**/*.sbml', recursive=True)
        for sbml_file in models:
            document = ls.readSBML(sbml_file)
            model = document.getModel()
            df = generator.generate(model)
            self.assertEqual(df.ndim, 2)
            sbml_basename = os.path.basename(sbml_file)
            stem = Path(sbml_basename).stem
            csv_file = os.path.join(self.out_path, f'{stem}.csv')
            df.to_csv(csv_file, index=False)

if __name__ == '__main__':
    unittest.main()
