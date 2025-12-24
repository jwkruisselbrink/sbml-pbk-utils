import glob
import os
from pathlib import Path
import unittest

import libsbml as ls
from tests.conf import TEST_OUTPUT_PATH, TEST_MODELS_PATH
from sbmlpbkutils import ParametrisationsTemplateGenerator

class ParametrisationsTemplateCreationTests(unittest.TestCase):

    def setUp(self):
        self.out_path = os.path.join(TEST_OUTPUT_PATH, 'reports')
        os.makedirs(self.out_path, exist_ok=True)

    def test_generate_parameterisation_templates(self):
        sbml_files = glob.glob(f'{TEST_MODELS_PATH}/**/*.sbml', recursive=True)
        for sbml_file in sbml_files:
            document = ls.readSBML(sbml_file)
            model = document.getModel()
            stem = Path(sbml_file).stem

            generator = ParametrisationsTemplateGenerator()
            (df_instance, df_params) = generator.generate(model)
            self.assertEqual(df_params.ndim, 2)

            csv_file = os.path.join(self.out_path, f'{stem}.instance.csv')
            df_instance.to_csv(csv_file, index=False)
            csv_file = os.path.join(self.out_path, f'{stem}.instance_params.csv')
            df_params.to_csv(csv_file, index=False)

if __name__ == '__main__':
    unittest.main()