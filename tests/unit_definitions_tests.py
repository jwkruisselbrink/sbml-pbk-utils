import unittest
import sys
import libsbml as ls
from sbmlpbkutils.unit_definitions import set_unit_definition
from sbmlpbkutils.unit_definitions import UnitDefinitions
from sbmlpbkutils.unit_string_generator import UnitStringGenerator

sys.path.append('../sbmlpbkutils/')

__test_outputs_path__ = './tests/__testoutputs__'
__test_models_path__ = './tests/models/'

class UnitDefinitionsTests(unittest.TestCase):

    def test_unit_definition(self):
        unit_string_generator = UnitStringGenerator()
        for definition in UnitDefinitions:
            unit_definition = ls.UnitDefinition(3, 2)
            set_unit_definition(unit_definition, definition)
            unit_string = unit_string_generator.create_unit_string(unit_definition)
            aliases = ', '.join(definition['synonyms'])
            msg = f"Generated unit string '{unit_string}' not in synonyms of unit '{definition["id"]}' [{aliases}]"
            self.assertIn(unit_string, definition['synonyms'], msg)

if __name__ == '__main__':
    unittest.main()
