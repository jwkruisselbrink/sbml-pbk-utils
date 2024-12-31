import unittest
import sys
import libsbml as ls
from parameterized import parameterized

from sbmlpbkutils import unit_definitions, UnitTypes
from sbmlpbkutils.unit_definitions import _si_prefix_string, _si_prefix_strings_ext, _time_unit_multipliers
from sbmlpbkutils import create_unit_string, set_unit_definition, get_unit_definition, get_unit_type
from sbmlpbkutils import get_volume_unit_definitions, get_mass_unit_definitions, get_time_unit_definitions

sys.path.append('../sbmlpbkutils/')

__test_outputs_path__ = './tests/__testoutputs__'
__test_models_path__ = './tests/models/'

class UnitDefinitionsTests(unittest.TestCase):

    def test_unit_definition(self):
        for definition in unit_definitions:
            unit_definition = ls.UnitDefinition(3, 2)
            set_unit_definition(unit_definition, definition)
            unit_string = create_unit_string(unit_definition)
            aliases = ', '.join(definition['synonyms'])
            msg = f"Generated unit string '{unit_string}' not in synonyms of unit '{definition["id"]}' [{aliases}]"
            self.assertIn(unit_string, definition['synonyms'], msg)

    def test_volume_unit_definition(self):
        volume_unit_defs = get_volume_unit_definitions()
        tabu_list = ['KiloL', 'HectoL', 'DecaL', 'DeciGM', 'NanoL', 'PicoL']
        for scale, prefix in _si_prefix_string.items():
            prefix_ext = _si_prefix_strings_ext[scale].title()
            id = f"{prefix_ext}L"
            unit_def = get_unit_definition(id)
            #self.assertIsNoaswwtNone(unit_def, f"Missing unit definition {id}.")
            if unit_def is not None:
                self.assertEqual(len(unit_def['units']), 1)
                unit = unit_def['units'][0]
                self.assertEqual(unit['scale'], scale, f"Incorrect multiplier for {id}.")
                sbml_unit_def = ls.UnitDefinition(3, 2)
                set_unit_definition(sbml_unit_def, unit_def)
                ucum_str = create_unit_string(sbml_unit_def)
                self.assertEqual(unit_def['UCUM'], ucum_str)
                self.assertIn(ucum_str, unit_def['synonyms'])
                self.assertIn(unit_def, volume_unit_defs)
            else:
                self.assertIn(id, tabu_list, f"No unit definition for {id}.")

    def test_mass_unit_definition(self):
        mass_unit_defs = get_mass_unit_definitions()
        mass_unit_postfixes = ['GM', 'MOL']
        tabu_list = ['KiloMOL', 'HectoGM', 'HectoMOL', 'DecaGM', 'DecaMOL', 'DeciGM', 'DeciMOL', 'CentiGM', 'CentiMOL']
        for scale, prefix in _si_prefix_string.items():
            prefix_ext = _si_prefix_strings_ext[scale].title()
            for postfix in mass_unit_postfixes:
                id = f"{prefix_ext}{postfix}"
                unit_def = get_unit_definition(id)
                #self.assertIsNotNone(unit_def, f"Missing unit definition {id}.")
                if unit_def is not None:
                    self.assertEqual(len(unit_def['units']), 1)
                    unit = unit_def['units'][0]
                    self.assertEqual(unit['scale'], scale, f"Incorrect multiplier for {id}.")
                    sbml_unit_def = ls.UnitDefinition(3, 2)
                    set_unit_definition(sbml_unit_def, unit_def)
                    ucum_str = create_unit_string(sbml_unit_def)
                    self.assertEqual(unit_def['UCUM'], ucum_str)
                    self.assertIn(ucum_str, unit_def['synonyms'])
                    self.assertIn(unit_def, mass_unit_defs)
                else:
                    self.assertIn(id, tabu_list, f"No unit definition for {id}.")

    def test_time_unit_definition(self):
        time_unit_defs = get_time_unit_definitions()
        tabu_list = []
        for multiplier, prefix in _time_unit_multipliers.items():
            time_str = _time_unit_multipliers[multiplier]
            id = f"{time_str}"
            if id not in tabu_list:
                unit_def = get_unit_definition(id)
                self.assertEqual(len(unit_def['units']), 1)
                unit = unit_def['units'][0]
                self.assertEqual(unit['multiplier'], multiplier, f"Incorrect multiplier for {id}.")
                sbml_unit_def = ls.UnitDefinition(3, 2)
                set_unit_definition(sbml_unit_def, unit_def)
                ucum_str = create_unit_string(sbml_unit_def)
                self.assertEqual(unit_def['UCUM'], ucum_str)
                self.assertIn(ucum_str, unit_def['synonyms'])
                self.assertIn(unit_def, time_unit_defs)

    @parameterized.expand([
        ("unitless", UnitTypes.DIMENSIONLESS),
        ("h", UnitTypes.TIME_UNIT),
        ("s", UnitTypes.TIME_UNIT),
        ("kg", UnitTypes.MASS_UNIT),
        ("g", UnitTypes.MASS_UNIT),
        ("ug", UnitTypes.MASS_UNIT),
        ("L", UnitTypes.VOLUME_UNIT),
        ("mL", UnitTypes.VOLUME_UNIT),
        ("mg/L", UnitTypes.CONCENTRATION_UNIT),
        ("mg/kg", UnitTypes.CONCENTRATION_UNIT)
    ])
    def test_get_unit_type(self, unit_str, expected_unit_type):
        unit_definition = get_unit_definition(unit_str)
        unit_type = get_unit_type(unit_definition)
        self.assertEqual(unit_type, expected_unit_type)

if __name__ == '__main__':
    unittest.main()
