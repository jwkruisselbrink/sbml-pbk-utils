from pathlib import Path
import unittest
import sys
import os
import libsbml as ls

from sbmlpbkutils import ParametrisationsTemplateGenerator

sys.path.append('../sbmlpbkutils/')

__test_outputs_path__ = './tests/__testoutputs__'
__test_models_path__ = './tests/models/'

class ParametrisationsTemplateGeneratorTests(unittest.TestCase):

    def setUp(self):
        from pathlib import Path
        Path(__test_outputs_path__).mkdir(parents=True, exist_ok=True)

    @classmethod
    def setUpClass(cls):
        cls.sbml_files = [
            os.path.join(__test_models_path__, 'simple.sbml'),
            os.path.join(__test_models_path__, 'simple.annotated.sbml'),
            os.path.join(__test_models_path__, 'euromix.sbml'),
            os.path.join(__test_models_path__, 'euromix.annotated.sbml')
        ]

    def test_generate_parameterisation_tepmlate_simple(self):
        generator = ParametrisationsTemplateGenerator()
        sbml_file = os.path.join(__test_models_path__, 'simple.sbml') 
        document = ls.readSBML(sbml_file)
        model = document.getModel()
        df = generator.generate(model)
        self.assertEqual(df.ndim, 2)

    def test_generate_parameterisation_tepmlate(self):
        generator = ParametrisationsTemplateGenerator()
        for sbml_file in self.sbml_files:
            document = ls.readSBML(sbml_file)
            model = document.getModel()
            df = generator.generate(model)
            self.assertEqual(df.ndim, 2)
            stem = Path(sbml_file).stem
            csv_file = os.path.join(__test_outputs_path__, f'{stem}.parametrisation.csv')
            df.to_csv(csv_file, index=False)

if __name__ == '__main__':
    unittest.main()