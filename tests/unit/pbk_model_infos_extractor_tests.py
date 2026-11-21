import os
from typing import List
import unittest

import libsbml as ls
from parameterized import parameterized

from tests.conf import TEST_MODELS_PATH
from sbmlpbkutils import PbkModelInfosExtractor

class PbkModelInfosExtractorTests(unittest.TestCase):

    @parameterized.expand([
        ("rate", "/s"),
        ("fraction", "UNITLESS"),
        ("concentration", "mol"),
        ("length", "m"),
    ])
    def test_get_parameter_infos_with_predefined_and_defined_units(self, parameter_id, expected_unit):
        sbml_file = os.path.join(TEST_MODELS_PATH, 'default_units/default_units.sbml')
        document = ls.readSBML(sbml_file)
        self.assertEqual(document.getNumErrors(), 0, document.getErrorLog().toString())
        extractor = PbkModelInfosExtractor(document)

        infos = extractor.get_parameter_infos()
        self.assertEqual({info.id for info in infos}, {"rate", "fraction", "concentration", "length"})
        info = next(info for info in infos if info.id == parameter_id)
        self.assertEqual(info.unit, expected_unit)
        self.assertTrue(info.has_unit())
        self.assertTrue(info.is_constant)

    @parameterized.expand([
        ("simple_oral/simple_oral.annotated.sbml", ['Gut']),
        ("simple_dermal/simple_dermal.annotated.sbml", ['Skin']),
        ("simple_inhalation/simple_inhalation.annotated.sbml", ['Alveolar'])
    ])
    def test_get_input_compartments(self, model_file: str, expected: List[str]):
        sbml_file = os.path.join(TEST_MODELS_PATH, model_file)
        document = ls.readSBML(sbml_file)
        infos_extractor = PbkModelInfosExtractor(document)
        result = infos_extractor.get_input_compartments()
        self.assertEqual(len(result), len(expected))
        self.assertListEqual(expected, sorted(result.keys()))

    @parameterized.expand([
        ("simple_oral/simple_oral.annotated.sbml", ['Mammalia'])
    ])
    def test_get_model_animal_species(self, model_file: str, expected: List[str]):
        sbml_file = os.path.join(TEST_MODELS_PATH, model_file)
        document = ls.readSBML(sbml_file)
        infos_extractor = PbkModelInfosExtractor(document)
        result = infos_extractor.get_model_animal_species()
        self.assertEqual(len(result), len(expected))
        self.assertListEqual(expected, sorted([r.label[0] for r in result]))

    @parameterized.expand([
        ("simple_oral/simple_oral.annotated.sbml", ['AGut']),
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
