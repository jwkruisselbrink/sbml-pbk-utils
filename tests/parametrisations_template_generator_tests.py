import unittest
import sys
import os
import libsbml as ls
from sbmlpbkutils import ParametrisationsTemplateGenerator
sys.path.append('../sbmlpbkutils/')

class ParametrisationsTemplateGeneratorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sbml_files = []
        files = os.listdir('./tests/models/')
        for file in files:
            if file.endswith('.sbml'):
                cls.sbml_files.append('./tests/models/' + file)

    def test_export_terms(self):
        generator = ParametrisationsTemplateGenerator()
        for sbml_file in self.sbml_files:
            document = ls.readSBML(sbml_file)
            model = document.getModel()
            df = generator.generate(model)
            self.assertEqual(df.ndim, 2)

if __name__ == '__main__':
    unittest.main()