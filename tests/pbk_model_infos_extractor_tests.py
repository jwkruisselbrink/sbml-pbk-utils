import unittest
import sys
import os
import libsbml as ls
from pathlib import Path
from sbmlpbkutils import AnnotationsTemplateGenerator
from sbmlpbkutils.pbk_model_infos_extractor import PbkModelInfosExtractor
sys.path.append('../sbmlpbkutils/')

__test_outputs_path__ = './tests/__testoutputs__'

class PbkModelInfosExtractorTests(unittest.TestCase):

    def setUp(self):
        from pathlib import Path
        Path(__test_outputs_path__).mkdir(parents=True, exist_ok=True)

    @classmethod
    def setUpClass(cls):
        cls.sbml_files = []
        files = os.listdir('./tests/models/')
        for file in files:
            if file.endswith('.annotated.sbml'):
                cls.sbml_files.append('./tests/models/' + file)

    def test_get_input_compartments(self):
        for sbml_file in self.sbml_files:
            infosExporter = PbkModelInfosExtractor(sbml_file)
            result = infosExporter.get_input_compartments()
            self.assertEqual(len(result), 3)
            self.assertIn('Gut', result.keys())
            self.assertIn('Air', result.keys())
            self.assertIn('Skin_sc_e', result.keys())

    def test_get_input_species(self):
        for sbml_file in self.sbml_files:
            infosExporter = PbkModelInfosExtractor(sbml_file)
            result = infosExporter.get_input_species()
            self.assertEqual(len(result), 3)
            self.assertIn('QGut', result.keys())
            self.assertIn('QAir', result.keys())
            self.assertIn('QSkin_sc_e', result.keys())

if __name__ == '__main__':
    unittest.main()
