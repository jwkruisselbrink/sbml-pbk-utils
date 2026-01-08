import os
from typing import List
import unittest

import libsbml as ls
from parameterized import parameterized

from tests.conf import TEST_MODELS_PATH
from sbmlpbkutils import PbkModelInfosExtractor

class PbkModelInfosExtractorTests(unittest.TestCase):

    @parameterized.expand([
        ("simple/simple.annotated.sbml", ['Gut']),
        ("euromix/euromix.annotated.sbml", ['Air', 'Gut', 'Skin_sc_e'])
    ])
    def test_get_input_compartments(self, model_file: str, expected: List[str]):
        sbml_file = os.path.join(TEST_MODELS_PATH, model_file)
        document = ls.readSBML(sbml_file)
        infos_extractor = PbkModelInfosExtractor(document)
        result = infos_extractor.get_input_compartments()
        self.assertEqual(len(result), len(expected))
        self.assertListEqual(expected, sorted(result.keys()))

    @parameterized.expand([
        ("simple/simple.annotated.sbml", ['Mammalia'])
    ])
    def test_get_model_animal_species(self, model_file: str, expected: List[str]):
        sbml_file = os.path.join(TEST_MODELS_PATH, model_file)
        document = ls.readSBML(sbml_file)
        infos_extractor = PbkModelInfosExtractor(document)
        result = infos_extractor.get_model_animal_species()
        self.assertEqual(len(result), len(expected))
        self.assertListEqual(expected, sorted([r.label[0] for r in result]))

    @parameterized.expand([
        ("simple/simple.annotated.sbml", ['AGut']),
        ("euromix/euromix.annotated.sbml", ['QAir', 'QGut', 'QSkin_sc_e'])
    ])
    def test_get_input_species(self, model_file: str, expected: List[str]):
        sbml_file = os.path.join(TEST_MODELS_PATH, model_file)
        document = ls.readSBML(sbml_file)
        infos_extractor = PbkModelInfosExtractor(document)
        result = infos_extractor.get_input_species()
        self.assertEqual(len(result), len(expected))
        self.assertListEqual(expected, sorted(result.keys()))

if __name__ == '__main__':
    unittest.main()
