import unittest
import sys
import os
import libsbml as ls
from sbmlpbkutils import ParametrisationsTemplateGenerator
sys.path.append('../sbmlpbkutils/')

__test_models_path__ = './tests/models/'

class ParametrisationsTemplateGeneratorTests(unittest.TestCase):

    def test_export_term_empty_simple(self):
        generator = ParametrisationsTemplateGenerator()
        sbml_file = os.path.join(__test_models_path__, 'simple.sbml') 
        document = ls.readSBML(sbml_file)
        model = document.getModel()
        df = generator.generate(model)
        self.assertEqual(df.ndim, 2)

    def test_export_term_simple_annotated(self):
        generator = ParametrisationsTemplateGenerator()
        sbml_file = os.path.join(__test_models_path__, 'simple.annotated.sbml') 
        document = ls.readSBML(sbml_file)
        model = document.getModel()
        df = generator.generate(model)
        self.assertEqual(df.ndim, 2)

if __name__ == '__main__':
    unittest.main()