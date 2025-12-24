import unittest
import os

import libsbml as ls
from tests.conf import TEST_MODELS_PATH
from sbmlpbkutils import ParametrisationsTemplateGenerator

class ParametrisationTemplateGeneratorTests(unittest.TestCase):

    def test_generate_parameterisation_template_simple(self):
        generator = ParametrisationsTemplateGenerator()
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.sbml')
        document = ls.readSBML(sbml_file)
        model = document.getModel()
        df = generator.generate_parameters_df(model)
        self.assertEqual(df.ndim, 2)

if __name__ == '__main__':
    unittest.main()
