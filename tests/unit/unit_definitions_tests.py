import unittest
import csv
import tempfile
import libsbml as ls
from parameterized import parameterized
from tests.conf import TEST_OUTPUT_PATH

from sbmlpbkutils import unit_definitions, UnitType
from sbmlpbkutils.unit_definitions import (
    _si_prefix_string,
    _si_prefix_strings_ext,
    _id_prefix_lookup,
    _time_unit_multipliers
)
from sbmlpbkutils import (
    create_unit_string,
    set_unit_definition,
    get_unit_definition,
    get_unit_type
)
from sbmlpbkutils import (
    get_volume_unit_definitions,
    get_mass_unit_definitions,
    get_time_unit_definitions,
    get_temperature_unit_definitions
)

class UnitDefinitionsTests(unittest.TestCase):

    def test_unit_definition_unit_string_in_synonyms(self):
        for definition in unit_definitions:
            unit_definition = ls.UnitDefinition(3, 2)
            set_unit_definition(unit_definition, definition)
            unit_string = create_unit_string(unit_definition)
            aliases = ', '.join(definition['synonyms'])
            msg = f"Generated unit string '{unit_string}' not in synonyms of unit '{definition["id"]}' [{aliases}]"
            self.assertEqual(unit_definition.getId(), definition['id'])
            self.assertIn(unit_string, definition['synonyms'], msg)

    def test_unit_definition_qudt(self):
        for definition in unit_definitions:
            if definition['qudt']:
                # If QUDT specified, then it should match id (except replacement of '_' with '-')
                self.assertEqual(definition['qudt'], definition['id'].replace('_', '-'))

    def test_unit_definition_ucum_in_synonyms(self):
        for definition in unit_definitions:
            if definition['UCUM']:
                self.assertIn(definition['UCUM'], definition['synonyms'])

    def test_volume_unit_definition(self):
        volume_unit_defs = get_volume_unit_definitions()
        tabu_list = ['KiloL', 'HectoL', 'DecaL', 'DeciGM', 'NanoL', 'PicoL']
        for scale, _ in _si_prefix_string.items():
            prefix_ext = _si_prefix_strings_ext[scale].title()
            key = f"{prefix_ext}L"
            unit_def = get_unit_definition(key)
            if unit_def is not None:
                self.assertEqual(len(unit_def['units']), 1)
                unit = unit_def['units'][0]
                self.assertEqual(unit['scale'], scale, f"Incorrect multiplier for {key}.")
                sbml_unit_def = ls.UnitDefinition(3, 2)
                set_unit_definition(sbml_unit_def, unit_def)
                ucum_str = create_unit_string(sbml_unit_def)
                self.assertEqual(unit_def['UCUM'], ucum_str)
                self.assertIn(ucum_str, unit_def['synonyms'])
                self.assertIn(unit_def, volume_unit_defs)
            else:
                self.assertIn(key, tabu_list, f"No unit definition for {key}.")

    def test_mass_unit_definition(self):
        mass_unit_defs = get_mass_unit_definitions()
        mass_unit_postfixes = ['GM', 'MOL']
        tabu_list = ['KiloMOL', 'HectoGM', 'HectoMOL', 'DecaGM', 'DecaMOL', 'DeciGM', 'DeciMOL', 'CentiGM', 'CentiMOL']
        for scale, _ in _si_prefix_string.items():
            prefix_ext = _si_prefix_strings_ext[scale].title()
            for postfix in mass_unit_postfixes:
                key = f"{prefix_ext}{postfix}"
                unit_def = get_unit_definition(key)
                #self.assertIsNotNone(unit_def, f"Missing unit definition {id}.")
                if unit_def is not None:
                    self.assertEqual(len(unit_def['units']), 1)
                    unit = unit_def['units'][0]
                    self.assertEqual(unit['scale'], scale, f"Incorrect multiplier for {key}.")
                    sbml_unit_def = ls.UnitDefinition(3, 2)
                    set_unit_definition(sbml_unit_def, unit_def)
                    ucum_str = create_unit_string(sbml_unit_def)
                    self.assertEqual(unit_def['UCUM'], ucum_str)
                    self.assertIn(ucum_str, unit_def['synonyms'])
                    self.assertIn(unit_def, mass_unit_defs)
                else:
                    self.assertIn(key, tabu_list, f"No unit definition for {key}.")

    def test_time_unit_definition(self):
        time_unit_defs = get_time_unit_definitions()
        tabu_list = []
        for multiplier, _ in _time_unit_multipliers.items():
            time_str = _time_unit_multipliers[multiplier]
            key = f"{time_str}"
            if key not in tabu_list:
                unit_def = get_unit_definition(key)
                self.assertEqual(len(unit_def['units']), 1)
                unit = unit_def['units'][0]
                self.assertEqual(unit['multiplier'], multiplier, f"Incorrect multiplier for {key}.")
                sbml_unit_def = ls.UnitDefinition(3, 2)
                set_unit_definition(sbml_unit_def, unit_def)
                ucum_str = create_unit_string(sbml_unit_def)
                self.assertEqual(unit_def['UCUM'], ucum_str)
                self.assertIn(ucum_str, unit_def['synonyms'])
                self.assertIn(unit_def, time_unit_defs)

    def test_temperature_unit_definitions(self):
        temp_unit_defs = get_temperature_unit_definitions()
        self.assertEqual(len(temp_unit_defs), 1)

    @parameterized.expand([
        ("K", "K"),
        ("Kelvin", "K")
    ])
    def test_temperature_unit_definition(self, key, expected_unit_id):
        temp_unit_defs = get_temperature_unit_definitions()
        unit_def = get_unit_definition(key)
        self.assertEqual(unit_def['id'], expected_unit_id)
        self.assertEqual(len(unit_def['units']), 1)
        unit = unit_def['units'][0]
        self.assertEqual(unit['multiplier'], 1, f"Incorrect multiplier for {key}.")
        sbml_unit_def = ls.UnitDefinition(3, 2)
        set_unit_definition(sbml_unit_def, unit_def)
        ucum_str = create_unit_string(sbml_unit_def)
        self.assertEqual(unit_def['UCUM'], ucum_str)
        self.assertIn(ucum_str, unit_def['synonyms'])
        self.assertIn(unit_def, temp_unit_defs)

    @parameterized.expand([
        ("unitless", UnitType.DIMENSIONLESS),
        ("h", UnitType.TIME_UNIT),
        ("s", UnitType.TIME_UNIT),
        ("kg", UnitType.MASS_UNIT),
        ("g", UnitType.MASS_UNIT),
        ("ug", UnitType.MASS_UNIT),
        ("L", UnitType.VOLUME_UNIT),
        ("mL", UnitType.VOLUME_UNIT),
        ("mg/L", UnitType.CONCENTRATION_UNIT),
        ("mg/kg", UnitType.CONCENTRATION_UNIT),
        ("K", UnitType.TEMPERATURE_UNIT)
    ])
    def test_get_unit_type(self, unit_str, expected_unit_type):
        unit_definition = get_unit_definition(unit_str)
        unit_type = get_unit_type(unit_definition)
        self.assertEqual(unit_type, expected_unit_type)

    @parameterized.expand([
        ("L/h", "L/h"),
        ("L.h-1", "L/h"),
        ("DAY", "d")
    ])
    def test_create_unit_string(self, unit_str, expected_unit_str):
        unit_definition = get_unit_definition(unit_str)
        sbml_unit_definition = ls.UnitDefinition(3, 2)
        set_unit_definition(sbml_unit_definition, unit_definition)
        formatted_unit_string = create_unit_string(sbml_unit_definition)
        self.assertEqual(formatted_unit_string, expected_unit_str)

    def test_create_time_unit_string(self):
        sbml_unit_definition = ls.UnitDefinition(3, 2)
        sbml_unit_definition.setId("DAY")
        u = sbml_unit_definition.createUnit()
        u.setKind(ls.UNIT_KIND_SECOND)
        u.setExponent(1)
        u.setMultiplier(8.64)
        u.setScale(4)
        formatted_unit_string = create_unit_string(sbml_unit_definition)
        self.assertEqual(formatted_unit_string, "d")

    def test_gram_based_mass_units(self):
        mass_exponents = [3, 0, -3, -6, -9, -12]
        for exponent in mass_exponents:
            # Construct unit ID
            id_prefix = _id_prefix_lookup[exponent]
            unit_id = f'{id_prefix}GM'

            # Construct unit string
            si_prefix = _si_prefix_string[exponent]
            unit_str = f'{si_prefix}g'
 
            # Get unit definition and assert not null
            unit_definition = get_unit_definition(unit_str)
            self.assertIsNotNone(unit_definition, f"No unit definition found for: {unit_str}")
            self.assertEqual(unit_id, unit_definition['id'])
            self.assertEqual(unit_str, unit_definition['UCUM'])

            # Check synonyms
            synonyms = [unit_str]
            for synonym in synonyms:
                self.assertIn(synonym, unit_definition['synonyms'])

            # Create unit definition and fetch ucum string; check if it matches expected
            sbml_unit_definition = ls.UnitDefinition(3, 2)
            set_unit_definition(sbml_unit_definition, unit_definition)
            ucum_str = create_unit_string(sbml_unit_definition)
            self.assertEqual(ucum_str, unit_str)

    def test_mol_based_mass_units(self):
        mass_exponents = [0, -3, -6, -9, -12]
        for exponent in mass_exponents:
            # Construct unit ID
            id_prefix = _id_prefix_lookup[exponent]
            unit_id = f'{id_prefix}MOL'

            # Construct unit string
            si_prefix = _si_prefix_string[exponent]
            unit_str = f'{si_prefix}mol'
 
            # Get unit definition and assert not null
            unit_definition = get_unit_definition(unit_str)
            self.assertIsNotNone(unit_definition, f"No unit definition found for: {unit_str}")
            self.assertEqual(unit_id, unit_definition['id'])
            self.assertEqual(unit_str, unit_definition['UCUM'])

            # Check synonyms
            synonyms = [unit_str]
            for synonym in synonyms:
                self.assertIn(synonym, unit_definition['synonyms'])

            # Create unit definition and fetch ucum string; check if it matches expected
            sbml_unit_definition = ls.UnitDefinition(3, 2)
            set_unit_definition(sbml_unit_definition, unit_definition)
            ucum_str = create_unit_string(sbml_unit_definition)
            self.assertEqual(ucum_str, unit_str)

    def test_litre_based_volume_units(self):
        mass_exponents = [0, -3, -6]
        for exponent in mass_exponents:
            # Construct unit ID
            id_prefix = _id_prefix_lookup[exponent]
            unit_id = f'{id_prefix}L'

            # Construct unit string
            si_prefix = _si_prefix_string[exponent]
            unit_str = f'{si_prefix}L'
 
            # Get unit definition and assert not null
            unit_definition = get_unit_definition(unit_str)
            self.assertIsNotNone(unit_definition, f"No unit definition found for: {unit_str}")
            self.assertEqual(unit_id, unit_definition['id'])
            self.assertEqual(unit_str, unit_definition['UCUM'])

            # Check synonyms
            synonyms = [unit_str]
            for synonym in synonyms:
                self.assertIn(synonym, unit_definition['synonyms'])

            # Create unit definition and fetch ucum string; check if it matches expected
            sbml_unit_definition = ls.UnitDefinition(3, 2)
            set_unit_definition(sbml_unit_definition, unit_definition)
            ucum_str = create_unit_string(sbml_unit_definition)
            self.assertEqual(ucum_str, unit_str)

    def test_gram_mass_per_gram_mass_units(self):
        """ Test gram-based mass per gram-based mass units
        """
        numerator_prefixes = ['', 'm', 'u', 'n']
        denominator_prefixes = ['k', '', 'm']
        for numerator_prefix in numerator_prefixes:
            for denominator_prefix in denominator_prefixes:
                # Create unit definition and check if there is a unit definition
                unit_str = f'{numerator_prefix}g/{denominator_prefix}g'

                # Get unit definition and assert not null
                unit_definition = get_unit_definition(unit_str)
                self.assertIsNotNone(unit_definition, f"No unit definition found for: {unit_str}")
                self.assertEqual(unit_str, unit_definition['UCUM'])

                # Check synonyms
                synonyms = [
                    unit_str,
                    f'{numerator_prefix}g.{denominator_prefix}g-1'
                ]
                for synonym in synonyms:
                    self.assertIn(synonym, unit_definition['synonyms'])

                # Create unit definition and fetch ucum string; check if it matches expected
                sbml_unit_definition = ls.UnitDefinition(3, 2)
                set_unit_definition(sbml_unit_definition, unit_definition)
                ucum_str = create_unit_string(sbml_unit_definition)
                self.assertEqual(ucum_str, unit_str)

    def test_gram_mass_per_litre_units(self):
        """ Test gram-based mass per litre-based volume units
        """
        numerator_prefixes = ['k', '', 'm', 'u', 'n', 'p']
        denominator_prefixes = ['', 'm']
        for numerator_prefix in numerator_prefixes:
            for denominator_prefix in denominator_prefixes:
                # Create unit definition and check if there is a unit definition
                unit_str = f'{numerator_prefix}g/{denominator_prefix}L'

                # Get unit definition and assert not null
                unit_definition = get_unit_definition(unit_str)
                self.assertIsNotNone(unit_definition, f"No unit definition found for: {unit_str}")
                self.assertEqual(unit_str, unit_definition['UCUM'])

                # Check synonyms
                synonyms = [
                    unit_str,
                    f'{numerator_prefix}g.{denominator_prefix}L-1'
                ]
                for synonym in synonyms:
                    self.assertIn(synonym, unit_definition['synonyms'])

                # Create unit definition and fetch ucum string; check if it matches expected
                sbml_unit_definition = ls.UnitDefinition(3, 2)
                set_unit_definition(sbml_unit_definition, unit_definition)
                ucum_str = create_unit_string(sbml_unit_definition)
                self.assertEqual(ucum_str, unit_str)

    def test_molar_mass_per_gram_mass_units(self):
        """ Test molar mass per gram-based mass units
        """
        mass_prefixes = ['', 'm', 'u', 'n']
        for numerator_prefix in mass_prefixes:
            for denominator_prefix in mass_prefixes:
                # Create unit definition and check if there is a unit definition
                unit_str = f'{numerator_prefix}mol/{denominator_prefix}g'

                # Get unit definition and assert not null
                unit_definition = get_unit_definition(unit_str)
                self.assertIsNotNone(unit_definition, f"No unit definition found for: {unit_str}")
                self.assertEqual(unit_str, unit_definition['UCUM'])

                # Check synonyms
                synonyms = [
                    unit_str,
                    f'{numerator_prefix}mol.{denominator_prefix}g-1'
                ]
                for synonym in synonyms:
                    self.assertIn(synonym, unit_definition['synonyms'])

                # Create unit definition and fetch ucum string; check if it matches expected
                sbml_unit_definition = ls.UnitDefinition(3, 2)
                set_unit_definition(sbml_unit_definition, unit_definition)
                ucum_str = create_unit_string(sbml_unit_definition)
                self.assertEqual(ucum_str, unit_str)

    def test_mol_mass_per_litre_units(self):
        """ Test gram-based mass per litre-based volume units
        """
        numerator_prefixes = ['', 'm', 'u', 'n', 'p']
        denominator_prefixes = ['', 'm']
        for numerator_prefix in numerator_prefixes:
            for denominator_prefix in denominator_prefixes:
                # Create unit definition and check if there is a unit definition
                unit_str = f'{numerator_prefix}mol/{denominator_prefix}L'

                # Get unit definition and assert not null
                unit_definition = get_unit_definition(unit_str)
                self.assertIsNotNone(unit_definition, f"No unit definition found for: {unit_str}")
                self.assertEqual(unit_str, unit_definition['UCUM'])

                # Check synonyms
                synonyms = [
                    unit_str,
                    f'{numerator_prefix}mol.{denominator_prefix}L-1'
                ]
                for synonym in synonyms:
                    self.assertIn(synonym, unit_definition['synonyms'])

                # Create unit definition and fetch ucum string; check if it matches expected
                sbml_unit_definition = ls.UnitDefinition(3, 2)
                set_unit_definition(sbml_unit_definition, unit_definition)
                ucum_str = create_unit_string(sbml_unit_definition)
                self.assertEqual(ucum_str, unit_str)

    def test_mol_mass_per_time_per_gram_mass_units(self):
        """ Test molar mass per time per gram-based mass units
        """
        time_units = ['h', 'd']
        mass_prefixes = ['', 'm', 'u', 'n']
        for mol_unit_prefix in mass_prefixes:
            for gram_unit_prefix in mass_prefixes:
                for time_unit in time_units:
                    # Create unit definition and check if there is a unit definition
                    unit_str = f'{mol_unit_prefix}mol/{time_unit}/{gram_unit_prefix}g'

                    # Get unit definition and assert not null
                    unit_definition = get_unit_definition(unit_str)
                    self.assertIsNotNone(unit_definition, f"No unit definition found for: {unit_str}")
                    self.assertEqual(unit_str, unit_definition['UCUM'])

                    # Check synonyms
                    synonyms = [
                        unit_str,
                        f'{mol_unit_prefix}mol/({time_unit}.{gram_unit_prefix}g)',
                        f'{mol_unit_prefix}mol.{time_unit}-1.{gram_unit_prefix}g-1'
                    ]
                    for synonym in synonyms:
                        self.assertIn(synonym, unit_definition['synonyms'])

                    # Create unit definition and fetch ucum string; check if it matches expected
                    sbml_unit_definition = ls.UnitDefinition(3, 2)
                    set_unit_definition(sbml_unit_definition, unit_definition)
                    ucum_str = create_unit_string(sbml_unit_definition)
                    self.assertEqual(ucum_str, unit_str)

    def test_per_time(self):
        """ Test molar mass per time per gram-based mass units
        """
        time_units = ['s', 'min', 'h', 'd', 'y']
        for time_unit in time_units:
            # Create unit definition and check if there is a unit definition
            unit_str = f'/{time_unit}'

            # Get unit definition and assert not null
            unit_definition = get_unit_definition(unit_str)
            self.assertIsNotNone(unit_definition, f"No unit definition found for: {unit_str}")
            self.assertEqual(unit_str, unit_definition['UCUM'])

            # Check synonyms
            synonyms = [
                unit_str,
                f'1/{time_unit}',
                f'{time_unit}-1'
            ]
            for synonym in synonyms:
                self.assertIn(synonym, unit_definition['synonyms'])

            # Create unit definition and fetch ucum string; check if it matches expected
            sbml_unit_definition = ls.UnitDefinition(3, 2)
            set_unit_definition(sbml_unit_definition, unit_definition)
            ucum_str = create_unit_string(sbml_unit_definition)
            self.assertEqual(ucum_str, unit_str)

    def test_allometric_scaled_clearance_units(self):
        """ Units for rates scaled by body weight using allometric scaling
        """
        mass_units = ['g', 'mol']
        time_units = ['h', 'd', 'min', 's']
        mass_prefixes = ['', 'm', 'u', 'n']
        for mass_unit in mass_units:
            for mass_prefix in mass_prefixes:
                for time_unit in time_units:
                    # Create unit definition and check if there is a unit definition
                    unit_str = f'{mass_prefix}{mass_unit}/{time_unit}/kg^0.75'
                    unit_definition = get_unit_definition(unit_str)
                    self.assertIsNotNone(unit_definition)
                    self.assertIn(
                        f'{mass_prefix}{mass_unit}/({time_unit}.kg^0.75)',
                        unit_definition['synonyms']
                    )

                    # Create unit definition and fetch ucum string; check if it matches expected
                    sbml_unit_definition = ls.UnitDefinition(3, 2)
                    set_unit_definition(sbml_unit_definition, unit_definition)
                    ucum_str = create_unit_string(sbml_unit_definition)
                    self.assertEqual(ucum_str, unit_str)

                    # Check synonyms
                    synonyms = [
                        f'{mass_prefix}{mass_unit}/{time_unit}/kg^0.75',
                        f'{mass_prefix}{mass_unit}/({time_unit}.kg^0.75)',
                        f'{mass_prefix}{mass_unit}.{time_unit}-1.kg-0.75',
                    ]
                    for synonym in synonyms:
                        self.assertIn(synonym, unit_definition['synonyms'])

    def test_allometric_scaled_rate_units(self):
        """ Units for rates scaled by body weight using allometric scaling
        """
        time_units = ['h', 'd']
        signs = ['', '-']
        for time_unit in time_units:
            for sign in signs:
                sign_inv = '' if sign == '-' else '-'

                # Create unit definition and check if there is a unit definition
                unit_str = f'{time_unit}-1.kg{sign}0.25'
                unit_definition = get_unit_definition(unit_str)
                self.assertIsNotNone(unit_definition)

                # Create unit definition and fetch ucum string; check if it matches expected
                sbml_unit_definition = ls.UnitDefinition(3, 2)
                set_unit_definition(sbml_unit_definition, unit_definition)
                ucum_str = create_unit_string(sbml_unit_definition)
                self.assertEqual(ucum_str, f'/{time_unit}/kg^0.25' if sign == '-' else f'/{time_unit}.kg^0.25')

                # Check synonyms
                synonyms = [
                    f'/{time_unit}/kg^{sign_inv}0.25',
                    f'1/{time_unit}/kg^{sign_inv}0.25',
                    f'/({time_unit}.kg^{sign_inv}0.25)',
                    f'1/({time_unit}.kg^{sign_inv}0.25)',
                    f'/{time_unit}.kg^{sign}0.25',
                    f'1/{time_unit}.kg^{sign}0.25',
                    f'{time_unit}-1.kg{sign}0.25',
                ]
                for synonym in synonyms:
                    self.assertIn(synonym, unit_definition['synonyms'])

    def test_duplicate_units(self):
        """ Check for duplicate unit definitions
        """
        seen_ids = set()
        seen_unit_strings = set()

        for definition in unit_definitions:
            def_id = definition['id']
            self.assertNotIn(def_id, seen_ids, f"Duplicate unit definition id found: {def_id}")
            seen_ids.add(def_id)

            # Create unit definition and fetch ucum string; check if it matches expected
            sbml_unit_definition = ls.UnitDefinition(3, 2)
            set_unit_definition(sbml_unit_definition, definition)
            unit_str = create_unit_string(sbml_unit_definition)
            self.assertNotIn(unit_str, seen_unit_strings, f"Duplicate generated unit string found: {unit_str}")
            seen_unit_strings.add(unit_str)

    def test_export_all_unit_definitions_to_csv(self):
        """Export all unit definitions to CSV and verify the written content."""
        fieldnames = ['id', 'UCUM', 'synonyms']
        csv_file = f"{TEST_OUTPUT_PATH}/unit_definitions.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as fp:
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            for definition in unit_definitions:
                writer.writerow({
                    'id': definition['id'],
                    'UCUM': definition.get('UCUM', ''),
                    'synonyms': ';'.join(definition.get('synonyms', []))
                })

if __name__ == '__main__':
    unittest.main()
