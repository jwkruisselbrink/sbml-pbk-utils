import unittest
import sys
import os
from pathlib import Path
import libsbml as ls
from sbmlpbkutils import AnnotationsTemplateGenerator

sys.path.append('../sbmlpbkutils/')

__test_outputs_path__ = './tests/__testoutputs__'
__test_models_path__ = './tests/models/'

class AnnotationsTemplateGeneratorTests(unittest.TestCase):

    def setUp(self):
        Path(__test_outputs_path__).mkdir(parents=True, exist_ok=True)

    @classmethod
    def setUpClass(cls):
        cls.sbml_files = [
            os.path.join(__test_models_path__, 'simple.sbml'),
            os.path.join(__test_models_path__, 'simple.annotated.sbml'),
            os.path.join(__test_models_path__, 'euromix.sbml'),
            os.path.join(__test_models_path__, 'euromix.annotated.sbml')
        ]

    def test_get_annotations_template(self):
        # Arrange
        sbml_file = os.path.join(__test_models_path__, 'simple.sbml') 
        document = ls.readSBML(sbml_file)
        model = document.getModel()
        generator = AnnotationsTemplateGenerator()
        df = generator.generate(model, False)

        # Check if template contains record for extent unit
        self.assertEqual(len(df.loc[df['element_id'] == 'extentUnits']), 1)

    def test_generate_no_fill(self):
        generator = AnnotationsTemplateGenerator()
        for sbml_file in self.sbml_files:
            document = ls.readSBML(sbml_file)
            model = document.getModel()
            df = generator.generate(model, False)
            self.assertEqual(df.ndim, 2)
            sbml_basename = os.path.basename(sbml_file)
            stem = Path(sbml_basename).stem
            csv_file = os.path.join(__test_outputs_path__, f'{stem}_no_fill.csv')
            df.to_csv(csv_file, index=False)

    def test_generate_try_fill(self):
        generator = AnnotationsTemplateGenerator()
        for sbml_file in self.sbml_files:
            document = ls.readSBML(sbml_file)
            model = document.getModel()
            df = generator.generate(model, True)
            self.assertEqual(df.ndim, 2)
            sbml_basename = os.path.basename(sbml_file)
            stem = Path(sbml_basename).stem
            csv_file = os.path.join(__test_outputs_path__, f'{stem}_try_fill.csv')
            df.to_csv(csv_file, index=False)

if __name__ == '__main__':
    unittest.main()
