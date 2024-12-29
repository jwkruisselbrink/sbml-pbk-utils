import libsbml as ls
import os
import sys
import unittest

from sbmlpbkutils import PbkModelInfosExtractor

sys.path.append('../sbmlpbkutils/')

__test_outputs_path__ = './tests/__testoutputs__'
__test_models_path__ = './tests/models/'

class PbkModelInfosExtractorTests(unittest.TestCase):

    def setUp(self):
        from pathlib import Path
        Path(__test_outputs_path__).mkdir(parents=True, exist_ok=True)

    def test_get_input_compartments_simple(self):
        sbml_file = os.path.join(__test_models_path__, 'simple.annotated.sbml')
        document = ls.readSBML(sbml_file)
        infos_extractor = PbkModelInfosExtractor(document)
        result = infos_extractor.get_input_compartments()
        self.assertEqual(len(result), 1)
        self.assertIn('Gut', result.keys())

    def test_get_input_compartments_euromix(self):
        sbml_file = os.path.join(__test_models_path__, 'euromix.annotated.sbml')
        document = ls.readSBML(sbml_file)
        infos_extractor = PbkModelInfosExtractor(document)
        result = infos_extractor.get_input_compartments()
        self.assertEqual(len(result), 3)
        self.assertIn('Gut', result.keys())
        self.assertIn('Air', result.keys())
        self.assertIn('Skin_sc_e', result.keys())

    def test_get_input_species_simple(self):
        sbml_file = os.path.join(__test_models_path__, 'simple.annotated.sbml')
        document = ls.readSBML(sbml_file)
        infos_extractor = PbkModelInfosExtractor(document)
        result = infos_extractor.get_input_species()
        self.assertEqual(len(result), 1)
        self.assertIn('AGut', result.keys())

    def test_get_input_species_euromix(self):
        sbml_file = os.path.join(__test_models_path__, 'euromix.annotated.sbml')
        document = ls.readSBML(sbml_file)
        infos_extractor = PbkModelInfosExtractor(document)
        result = infos_extractor.get_input_species()
        self.assertEqual(len(result), 3)
        self.assertIn('QGut', result.keys())
        self.assertIn('QAir', result.keys())
        self.assertIn('QSkin_sc_e', result.keys())

if __name__ == '__main__':
    unittest.main()
