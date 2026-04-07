"""SBML unit definitions and utilities.

This module defines common SBML unit definitions, utility functions for
locating and classifying unit definitions, and helpers for converting
libSBML unit objects to string representations.
"""

import enum
import libsbml as ls

class UnitType(enum.Enum):
    """Categories of units used for unit classification."""
    DIMENSIONLESS = 1           # Unitless/dimensionless
    MASS_UNIT = 2               # Grams or moles
    VOLUME_UNIT = 3             # Liters
    TIME_UNIT = 4               # Seconds
    CONCENTRATION_UNIT = 5      # Grams per mass or volume
    TEMPERATURE_UNIT = 6        # Temperature (Kelvin)
    OTHER = 99                  # Anything other than the above

_si_prefix_string = {
    3: 'k',
    2: 'h',
    1: 'da',
    0: '',
    -1: 'd',
    -2: 'c',
    -3: 'm',
    -6: 'u',
    -9: 'n',
    -12: 'p',
}

_si_prefix_strings_ext = {
    3: 'kilo',
    2: 'hecto',
    1: 'deca',
    0: '',
    -1: 'deci',
    -2: 'centi',
    -3: 'milli',
    -6: 'micro',
    -9: 'nano',
    -12: 'pico',
}

_id_prefix_lookup = {
    3: 'Kilo',
    0: '',
    -1: 'Deci',
    -2: 'Centi',
    -3: 'Milli',
    -6: 'Micro',
    -9: 'Nano',
    -12: 'Pico',
}

_time_unit_id_lookup = {
    's': 'SEC',
    'min': 'MIN',
    'h': 'HR',
    'd': 'DAY',
    'y': 'YR'
}

_time_unit_multipliers = {
    1: 's',
    60: 'min',
    3600: 'h',
    86400: 'd',
    31557600: 'y'
}

_base_unit_strings = {
    ls.UNIT_KIND_DIMENSIONLESS: '',
    ls.UNIT_KIND_SECOND: 's',
    ls.UNIT_KIND_GRAM: 'g',
    ls.UNIT_KIND_LITER: 'L',
    ls.UNIT_KIND_LITRE: 'L',
    ls.UNIT_KIND_METER: 'm',
    ls.UNIT_KIND_METRE: 'm',
    ls.UNIT_KIND_MOLE: 'mol',
    ls.UNIT_KIND_KELVIN: 'K'
}

_base_unit_strings_ext = {
    ls.UNIT_KIND_DIMENSIONLESS: '',
    ls.UNIT_KIND_SECOND: 'second',
    ls.UNIT_KIND_GRAM: 'gram',
    ls.UNIT_KIND_LITER: 'liter',
    ls.UNIT_KIND_LITRE: 'liter',
    ls.UNIT_KIND_METER: 'meter',
    ls.UNIT_KIND_METRE: 'meter',
    ls.UNIT_KIND_MOLE: 'mole',
    ls.UNIT_KIND_KELVIN: 'Kelvin'
}

def create_area_units() -> None:
    numerator_exponents = [0, -1, -2, -3]
    for numerator_exponent in numerator_exponents:
        # Construct unit ID
        numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
        unit_id = f'{numerator_prefix_id}M2'

        # Construct unit string
        numerator_prefix_si = _si_prefix_string[numerator_exponent]
        unit_str = f'{numerator_prefix_si}m2'

        # Construct synonyms
        synonyms = [
            unit_str,
            f'{numerator_prefix_si}m2',
            f'{numerator_prefix_si}m^2'
        ]

        # Create and add definitions
        definition = {
            "id" : unit_id,
            "qudt" : "",
            "UCUM" : unit_str,
            "synonyms" : synonyms,
            "units": [
                { "kind": ls.UNIT_KIND_METRE, "exponent": 2, "multiplier": 1, "scale": numerator_exponent }
            ]
        }
        unit_definitions.append(definition)

def create_gram_units() -> None:
    mass_exponents = [3, 0, -3, -6, -9, -12]
    for exponent in mass_exponents:
        # Construct unit ID
        id_prefix = _id_prefix_lookup[exponent]
        unit_id = f'{id_prefix}GM'

        # Construct unit string
        si_prefix = _si_prefix_string[exponent]
        unit_str = f'{si_prefix}g'

        # Create and add definitions
        definition = {
            "id" : unit_id,
            "qudt" : "",
            "UCUM" : unit_str,
            "synonyms" : [unit_str],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": exponent }
            ]
        }
        unit_definitions.append(definition)

def create_gram_per_gram_units() -> None:
    numerator_mass_exponents = [0, -3, -6, -9, -12]
    denominator_mass_exponents = [3, 0, -3, -6]
    for numerator_exponent in numerator_mass_exponents:
        for denominator_exponent in denominator_mass_exponents:
            # Construct unit ID
            numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
            denominator_prefix_id = _id_prefix_lookup[denominator_exponent]
            unit_id = f'{numerator_prefix_id}GM_PER_{denominator_prefix_id}GM'

            # Construct unit string
            numerator_prefix_si = _si_prefix_string[numerator_exponent]
            denominator_prefix_si = _si_prefix_string[denominator_exponent]
            unit_str = f'{numerator_prefix_si}g/{denominator_prefix_si}g'

            # Construct synonyms
            synonyms = [
                unit_str,
                f'{numerator_prefix_si}g.{denominator_prefix_si}g-1'
            ]

            # Create and add definitions
            definition = {
                "id" : unit_id,
                "qudt" : "",
                "UCUM" : unit_str,
                "synonyms" : synonyms,
                "units": [
                    { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": numerator_exponent },
                    { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": denominator_exponent }
                ]
            }
            unit_definitions.append(definition)

def create_gram_per_liter_units() -> None:
    numerator_exponents = [3, 0, -3, -6, -9, -12]
    denominator_exponents = [0, -3, -6]
    for numerator_exponent in numerator_exponents:
        for denominator_exponent in denominator_exponents:
            # Construct unit ID
            numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
            denominator_prefix_id = _id_prefix_lookup[denominator_exponent]
            unit_id = f'{numerator_prefix_id}GM_PER_{denominator_prefix_id}L'

            # Construct unit string
            numerator_prefix_si = _si_prefix_string[numerator_exponent]
            denominator_prefix_si = _si_prefix_string[denominator_exponent]
            unit_str = f'{numerator_prefix_si}g/{denominator_prefix_si}L'

            # Construct synonyms
            synonyms = [
                unit_str,
                f'{numerator_prefix_si}g.{denominator_prefix_si}L-1'
            ]

            # Create and add definitions
            definition = {
                "id" : unit_id,
                "qudt" : "",
                "UCUM" : unit_str,
                "synonyms" : synonyms,
                "units": [
                    { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": numerator_exponent },
                    { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": denominator_exponent }
                ]
            }
            unit_definitions.append(definition)

def create_gram_per_time_units() -> None:
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    mass_exponents = [0, -3, -6, -9, -12]
    time_units = ['s', 'min', 'h', 'd']
    for mol_unit_exponent in mass_exponents:
        for time_unit in time_units:
            # Construct unit ID
            mass_unit_prefix_id = _id_prefix_lookup[mol_unit_exponent]
            unit_id = f'{mass_unit_prefix_id}GM_PER_{_time_unit_id_lookup[time_unit]}'

            # Construct unit string
            mass_unit_prefix_si = _si_prefix_string[mol_unit_exponent]
            unit_str = f'{mass_unit_prefix_si}g/{time_unit}'

            # Construct synonyms
            synonyms = [
                unit_str,
                f'{mass_unit_prefix_si}g.{time_unit}-1'
            ]
            time_unit_multiplier = inv_map[time_unit]

            # Create and add definitions
            definition = {
                "id" : unit_id,
                "qudt" : "",
                "UCUM" : unit_str,
                "synonyms" : synonyms,
                "units": [
                    { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": mol_unit_exponent },
                    { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 }
                ]
            }
            unit_definitions.append(definition)

def create_gram_per_time_per_allometric_mass_units() -> None:
    time_units = ['h', 'd', 'min', 's']
    numerator_exponents = [0, -3, -6, -9, -12]
    denominator_exponents = [3]
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    for numerator_exponent in numerator_exponents:
        for denominator_exponent in denominator_exponents:
            for time_unit in time_units:
                # Construct unit ID
                numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
                denominator_prefix_id = _id_prefix_lookup[denominator_exponent]
                unit_id = f'{numerator_prefix_id}GM_PER_{_time_unit_id_lookup[time_unit]}_PER_{denominator_prefix_id}GM0P75'

                # Construct unit string
                numerator_prefix_si = _si_prefix_string[numerator_exponent]
                denominator_prefix_si = _si_prefix_string[denominator_exponent]
                unit_str = f'{numerator_prefix_si}g/{time_unit}/{denominator_prefix_si}g^0.75'

                # Construct synonyms
                synonyms = [
                    unit_str,
                    f'{numerator_prefix_si}g/{time_unit}/{denominator_prefix_si}g0.75',
                    f'{numerator_prefix_si}g/{time_unit}/{denominator_prefix_si}g^0.75',
                    f'{numerator_prefix_si}g/({time_unit}.{denominator_prefix_si}g0.75)',
                    f'{numerator_prefix_si}g.{time_unit}-1.{denominator_prefix_si}g-0.75',
                    f'{numerator_prefix_si}g/({time_unit}.{denominator_prefix_si}g^0.75)',
                    f'{numerator_prefix_si}g.{time_unit}^-1.{denominator_prefix_si}g^-0.75'
                ]
                time_unit_multiplier = inv_map[time_unit]

                # Create and add definitions
                definition = {
                    "id" : unit_id,
                    "qudt" : "",
                    "UCUM" : unit_str,
                    "synonyms" : synonyms,
                    "units": [
                        { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": numerator_exponent },
                        { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 },
                        { "kind": ls.UNIT_KIND_GRAM, "exponent": -0.75, "multiplier": 1, "scale": 3 },
                    ]
                }
                unit_definitions.append(definition)

def create_gram_per_time_per_gram_units() -> None:
    time_units = ['h', 'd']
    numerator_exponents = [0, -3, -6, -9, -12]
    denominator_exponents = [3, 0, -3, -6]
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    for numerator_exponent in numerator_exponents:
        for denominator_exponent in denominator_exponents:
            for time_unit in time_units:
                # Construct unit ID
                numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
                denominator_prefix_id = _id_prefix_lookup[denominator_exponent]
                unit_id = f'{numerator_prefix_id}GM_PER_{_time_unit_id_lookup[time_unit]}_PER_{denominator_prefix_id}GM'

                # Construct unit string
                numerator_prefix_si = _si_prefix_string[numerator_exponent]
                denominator_prefix_si = _si_prefix_string[denominator_exponent]
                unit_str = f'{numerator_prefix_si}g/{time_unit}/{denominator_prefix_si}g'

                # Construct synonyms
                synonyms = [
                    unit_str,
                    f'{numerator_prefix_si}g/({time_unit}.{denominator_prefix_si}g)',
                    f'{numerator_prefix_si}g.{time_unit}-1.{denominator_prefix_si}g-1'
                ]
                time_unit_multiplier = inv_map[time_unit]

                # Create and add definitions
                definition = {
                    "id" : unit_id,
                    "qudt" : "",
                    "UCUM" : unit_str,
                    "synonyms" : synonyms,
                    "units": [
                        { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": numerator_exponent },
                        { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 },
                        { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": denominator_exponent }
                    ]
                }
                unit_definitions.append(definition)

def create_gram_per_time_per_volume_units() -> None:
    time_units = ['h', 'd', 'min', 's']
    numerator_exponents = [0, -3, -6, -9, -12]
    denominator_exponents = [3, 0, -3, -6]
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    for numerator_exponent in numerator_exponents:
        for denominator_exponent in denominator_exponents:
            for time_unit in time_units:
                # Construct unit ID
                numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
                denominator_prefix_id = _id_prefix_lookup[denominator_exponent]
                unit_id = f'{numerator_prefix_id}GM_PER_{_time_unit_id_lookup[time_unit]}_PER_{denominator_prefix_id}L'

                # Construct unit string
                numerator_prefix_si = _si_prefix_string[numerator_exponent]
                denominator_prefix_si = _si_prefix_string[denominator_exponent]
                unit_str = f'{numerator_prefix_si}g/{time_unit}/{denominator_prefix_si}L'

                # Construct synonyms
                synonyms = [
                    unit_str,
                    f'{numerator_prefix_si}g/{time_unit}/{denominator_prefix_si}L',
                    f'{numerator_prefix_si}g/({time_unit}.{denominator_prefix_si}L)',
                    f'{numerator_prefix_si}g.{time_unit}-1.{denominator_prefix_si}L-1'
                ]
                time_unit_multiplier = inv_map[time_unit]

                # Create and add definitions
                definition = {
                    "id" : unit_id,
                    "qudt" : "",
                    "UCUM" : unit_str,
                    "synonyms" : synonyms,
                    "units": [
                        { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": numerator_exponent },
                        { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 },
                        { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": denominator_exponent }
                    ]
                }
                unit_definitions.append(definition)

def create_length_units() -> None:
    numerator_exponents = [0, -1, -2, -3]
    for numerator_exponent in numerator_exponents:
        # Construct unit ID
        numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
        unit_id = f'{numerator_prefix_id}M'

        # Construct unit string
        numerator_prefix_si = _si_prefix_string[numerator_exponent]
        unit_str = f'{numerator_prefix_si}m'

        # Construct synonyms
        synonyms = [
            unit_str,
            f'{numerator_prefix_si}m'
        ]

        # Create and add definitions
        definition = {
            "id" : unit_id,
            "qudt" : "",
            "UCUM" : unit_str,
            "synonyms" : synonyms,
            "units": [
                { "kind": ls.UNIT_KIND_METRE, "exponent": 1, "multiplier": 1, "scale": numerator_exponent }
            ]
        }
        unit_definitions.append(definition)

def create_length_per_time_units() -> None:
    time_units = ['h', 'd', 'min', 's']
    numerator_exponents = [0, -1, -2, -3]
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    for numerator_exponent in numerator_exponents:
        for time_unit in time_units:
            # Construct unit ID
            numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
            unit_id = f'{numerator_prefix_id}M_PER_{_time_unit_id_lookup[time_unit]}'

            # Construct unit string
            numerator_prefix_si = _si_prefix_string[numerator_exponent]
            unit_str = f'{numerator_prefix_si}m/{time_unit}'

            # Construct synonyms
            synonyms = [
                unit_str,
                f'{numerator_prefix_si}m/{time_unit}',
                f'{numerator_prefix_si}m.{time_unit}-1'
            ]
            time_unit_multiplier = inv_map[time_unit]

            # Create and add definitions
            definition = {
                "id" : unit_id,
                "qudt" : "",
                "UCUM" : unit_str,
                "synonyms" : synonyms,
                "units": [
                    { "kind": ls.UNIT_KIND_METRE, "exponent": 1, "multiplier": 1, "scale": numerator_exponent },
                    { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 },
                ]
            }
            unit_definitions.append(definition)

def create_liter_per_gram_per_time_units() -> None:
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    time_units = ['s', 'min', 'h', 'd']
    numerator_unit_exponents = [0, -3, -6, -9, -12]
    denominator_unit_exponents = [3, 0, -3, -6, -9, -12]
    for numerator_unit_exponent in numerator_unit_exponents:
        for denominator_unit_exponent in denominator_unit_exponents:
            for time_unit in time_units:
                # Construct unit ID
                id_prefix_numerator = _id_prefix_lookup[numerator_unit_exponent]
                id_prefix_denominator = _id_prefix_lookup[denominator_unit_exponent]
                unit_id = f'{id_prefix_numerator}L_PER_{id_prefix_denominator}GM_PER_{_time_unit_id_lookup[time_unit]}'

                # Construct unit string
                si_prefix_numerator = _si_prefix_string[numerator_unit_exponent]
                si_prefix_denominator = _si_prefix_string[denominator_unit_exponent]
                unit_str = f'{si_prefix_numerator}L/{si_prefix_denominator}g/{time_unit}'

                # Construct synonyms
                synonyms = [
                    unit_str,
                    f'{si_prefix_numerator}L/{si_prefix_denominator}g/{time_unit}',
                    f'{si_prefix_numerator}L/({si_prefix_denominator}g.{time_unit})',
                    f'{si_prefix_numerator}L.{si_prefix_denominator}g-1.{time_unit}-1'
                ]
                time_unit_multiplier = inv_map[time_unit]

                # Create and add definitions
                definition = {
                    "id" : unit_id,
                    "qudt" : "",
                    "UCUM" : unit_str,
                    "synonyms" : synonyms,
                    "units": [
                        { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": numerator_unit_exponent },
                        { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": denominator_unit_exponent },
                        { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 }
                    ]
                }
                unit_definitions.append(definition)

def create_liter_per_gram_units() -> None:
    numerator_exponents = [0, -3, -6, -9, -12]
    denominator_exponents = [3, 0, -3, -6]
    for numerator_exponent in numerator_exponents:
        for denominator_exponent in denominator_exponents:
            # Construct unit ID
            numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
            denominator_prefix_id = _id_prefix_lookup[denominator_exponent]
            unit_id = f'{numerator_prefix_id}L_PER_{denominator_prefix_id}GM'

            # Construct unit string
            numerator_prefix_si = _si_prefix_string[numerator_exponent]
            denominator_prefix_si = _si_prefix_string[denominator_exponent]
            unit_str = f'{numerator_prefix_si}L/{denominator_prefix_si}g'

            # Construct synonyms
            synonyms = [
                unit_str,
                f'{numerator_prefix_si}L/{denominator_prefix_si}g',
                f'{numerator_prefix_si}L.{denominator_prefix_si}g-1'
            ]

            # Create and add definitions
            definition = {
                "id" : unit_id,
                "qudt" : "",
                "UCUM" : unit_str,
                "synonyms" : synonyms,
                "units": [
                    { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": numerator_exponent },
                    { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": denominator_exponent }
                ]
            }
            unit_definitions.append(definition)

def create_liter_per_time_per_gram_units() -> None:
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    time_units = ['s', 'min', 'h', 'd']
    mol_unit_exponents = [0, -3, -6, -9, -12]
    gram_unit_exponents = [3, 0, -3, -6, -9, -12]
    for mol_unit_exponent in mol_unit_exponents:
        for gram_unit_exponent in gram_unit_exponents:
            for time_unit in time_units:
                # Construct unit ID
                mol_unit_prefix_id = _id_prefix_lookup[mol_unit_exponent]
                gram_unit_prefix_id = _id_prefix_lookup[gram_unit_exponent]
                unit_id = f'{mol_unit_prefix_id}L_PER_{_time_unit_id_lookup[time_unit]}_PER_{gram_unit_prefix_id}GM'

                # Construct unit string
                mol_unit_prefix_si = _si_prefix_string[mol_unit_exponent]
                gram_unit_prefix_si = _si_prefix_string[gram_unit_exponent]
                unit_str = f'{mol_unit_prefix_si}L/{time_unit}/{gram_unit_prefix_si}g'

                # Construct synonyms
                synonyms = [
                    unit_str,
                    f'{mol_unit_prefix_si}L/{time_unit}/{gram_unit_prefix_si}g',
                    f'{mol_unit_prefix_si}L/({time_unit}.{gram_unit_prefix_si}g)',
                    f'{mol_unit_prefix_si}L.{time_unit}-1.{gram_unit_prefix_si}g-1'
                ]
                time_unit_multiplier = inv_map[time_unit]

                # Create and add definitions
                definition = {
                    "id" : unit_id,
                    "qudt" : "",
                    "UCUM" : unit_str,
                    "synonyms" : synonyms,
                    "units": [
                        { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": mol_unit_exponent },
                        { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 },
                        { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": gram_unit_exponent }
                    ]
                }
                unit_definitions.append(definition)

def create_liter_per_time_per_allometric_mass_units() -> None:
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    time_units = ['s', 'min', 'h', 'd']
    mol_unit_exponents = [0, -3, -6, -9, -12]
    gram_unit_exponents = [3]
    for mol_unit_exponent in mol_unit_exponents:
        for gram_unit_exponent in gram_unit_exponents:
            for time_unit in time_units:
                # Construct unit ID
                mol_unit_prefix_id = _id_prefix_lookup[mol_unit_exponent]
                gram_unit_prefix_id = _id_prefix_lookup[gram_unit_exponent]
                unit_id = f'{mol_unit_prefix_id}L_PER_{_time_unit_id_lookup[time_unit]}_PER_{gram_unit_prefix_id}GM0P75'

                # Construct unit string
                mol_unit_prefix_si = _si_prefix_string[mol_unit_exponent]
                gram_unit_prefix_si = _si_prefix_string[gram_unit_exponent]
                unit_str = f'{mol_unit_prefix_si}L/{time_unit}/{gram_unit_prefix_si}g^0.75'

                # Construct synonyms
                synonyms = [
                    unit_str,
                    f'{mol_unit_prefix_si}L/{time_unit}/{gram_unit_prefix_si}g^0.75',
                    f'{mol_unit_prefix_si}L/{time_unit}/{gram_unit_prefix_si}g0.75',
                    f'{mol_unit_prefix_si}L/({time_unit}.{gram_unit_prefix_si}g^0.75)',
                    f'{mol_unit_prefix_si}L/({time_unit}.{gram_unit_prefix_si}g0.75)',
                    f'{mol_unit_prefix_si}L.{time_unit}-1.{gram_unit_prefix_si}g^-0.75',
                    f'{mol_unit_prefix_si}L.{time_unit}-1.{gram_unit_prefix_si}g-0.75'
                ]
                time_unit_multiplier = inv_map[time_unit]

                # Create and add definitions
                definition = {
                    "id" : unit_id,
                    "qudt" : "",
                    "UCUM" : unit_str,
                    "synonyms" : synonyms,
                    "units": [
                        { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": mol_unit_exponent },
                        { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 },
                        { "kind": ls.UNIT_KIND_GRAM, "exponent": -0.75, "multiplier": 1, "scale": gram_unit_exponent }
                    ]
                }
                unit_definitions.append(definition)

def create_liter_per_time_units() -> None:
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    volume_exponents = [0, -3, -6, -9, -12]
    time_units = ['s', 'min', 'h', 'd']
    for mol_unit_exponent in volume_exponents:
        for time_unit in time_units:
            # Construct unit ID
            mass_unit_prefix_id = _id_prefix_lookup[mol_unit_exponent]
            unit_id = f'{mass_unit_prefix_id}L_PER_{_time_unit_id_lookup[time_unit]}'

            # Construct unit string
            mass_unit_prefix_si = _si_prefix_string[mol_unit_exponent]
            unit_str = f'{mass_unit_prefix_si}L/{time_unit}'

            # Construct synonyms
            synonyms = [
                unit_str,
                f'{mass_unit_prefix_si}L.{time_unit}-1'
            ]
            time_unit_multiplier = inv_map[time_unit]

            # Create and add definitions
            definition = {
                "id" : unit_id,
                "qudt" : "",
                "UCUM" : unit_str,
                "synonyms" : synonyms,
                "units": [
                    { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": mol_unit_exponent },
                    { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 }
                ]
            }
            unit_definitions.append(definition)

def create_liter_units() -> None:
    exponents = [0, -1, -2, -3, -6]
    for exponent in exponents:
        # Construct unit ID
        id_prefix = _id_prefix_lookup[exponent]
        unit_id = f'{id_prefix}L'

        # Construct unit string
        si_prefix = _si_prefix_string[exponent]
        unit_str = f'{si_prefix}L'

        # Create and add definitions
        definition = {
            "id" : unit_id,
            "qudt" : "",
            "UCUM" : unit_str,
            "synonyms" : [unit_str],
            "units": [
                { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": exponent }
            ]
        }
        unit_definitions.append(definition)

def create_molar_mass_unit() -> None:
    unit_definitions.append({
        "id" : "GM_PER_MOL",
        "qudt" : "GM-PER-MOL",
        "UCUM" : "g/mol",
        "synonyms" : [
            "g/mol",
            "g.mol-1",
            "g_per_mol"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_MOLE, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    })

def create_mol_per_time_per_allometric_mass_units() -> None:
    time_units = ['h', 'd', 'min', 's']
    numerator_exponents = [0, -3, -6, -9, -12]
    denominator_exponents = [3]
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    for numerator_exponent in numerator_exponents:
        for denominator_exponent in denominator_exponents:
            for time_unit in time_units:
                # Construct unit ID
                numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
                denominator_prefix_id = _id_prefix_lookup[denominator_exponent]
                unit_id = f'{numerator_prefix_id}MOL_PER_{_time_unit_id_lookup[time_unit]}_PER_{denominator_prefix_id}GM0P75'

                # Construct unit string
                numerator_prefix_si = _si_prefix_string[numerator_exponent]
                denominator_prefix_si = _si_prefix_string[denominator_exponent]
                unit_str = f'{numerator_prefix_si}mol/{time_unit}/{denominator_prefix_si}g^0.75'

                # Construct synonyms
                synonyms = [
                    unit_str,
                    f'{numerator_prefix_si}mol/{time_unit}/{denominator_prefix_si}g0.75',
                    f'{numerator_prefix_si}mol/{time_unit}/{denominator_prefix_si}g^0.75',
                    f'{numerator_prefix_si}mol/({time_unit}.{denominator_prefix_si}g0.75)',
                    f'{numerator_prefix_si}mol.{time_unit}-1.{denominator_prefix_si}g-0.75',
                    f'{numerator_prefix_si}mol/({time_unit}.{denominator_prefix_si}g^0.75)',
                    f'{numerator_prefix_si}mol.{time_unit}^-1.{denominator_prefix_si}g^-0.75'
                ]
                time_unit_multiplier = inv_map[time_unit]

                # Create and add definitions
                definition = {
                    "id" : unit_id,
                    "qudt" : "",
                    "UCUM" : unit_str,
                    "synonyms" : synonyms,
                    "units": [
                        { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": numerator_exponent },
                        { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 },
                        { "kind": ls.UNIT_KIND_GRAM, "exponent": -0.75, "multiplier": 1, "scale": 3 },
                    ]
                }
                unit_definitions.append(definition)

def create_mol_per_time_per_mol_units() -> None:
    time_units = ['h', 'd', 'min', 's']
    numerator_exponents = [0, -3, -6, -9, -12]
    denominator_exponents = [3, 0, -3, -6, -9, -12]
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    for numerator_exponent in numerator_exponents:
        for denominator_exponent in denominator_exponents:
            for time_unit in time_units:
                # Construct unit ID
                numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
                denominator_prefix_id = _id_prefix_lookup[denominator_exponent]
                unit_id = f'{numerator_prefix_id}MOL_PER_{_time_unit_id_lookup[time_unit]}_PER_{denominator_prefix_id}MOL'

                # Construct unit string
                numerator_prefix_si = _si_prefix_string[numerator_exponent]
                denominator_prefix_si = _si_prefix_string[denominator_exponent]
                unit_str = f'{numerator_prefix_si}mol/{time_unit}/{denominator_prefix_si}mol'

                # Construct synonyms
                synonyms = [
                    unit_str,
                    f'{numerator_prefix_si}mol/{time_unit}/{denominator_prefix_si}mol',
                    f'{numerator_prefix_si}mol/({time_unit}.{denominator_prefix_si}mol)',
                    f'{numerator_prefix_si}mol.{time_unit}-1.{denominator_prefix_si}mol-1'
                ]
                time_unit_multiplier = inv_map[time_unit]

                # Create and add definitions
                definition = {
                    "id" : unit_id,
                    "qudt" : "",
                    "UCUM" : unit_str,
                    "synonyms" : synonyms,
                    "units": [
                        { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": numerator_exponent },
                        { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 },
                        { "kind": ls.UNIT_KIND_MOLE, "exponent": -1, "multiplier": 1, "scale": denominator_exponent }
                    ]
                }
                unit_definitions.append(definition)

def create_mol_per_time_per_volume_units() -> None:
    time_units = ['h', 'd', 'min', 's']
    numerator_exponents = [0, -3, -6, -9, -12]
    denominator_exponents = [3, 0, -3, -6]
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    for numerator_exponent in numerator_exponents:
        for denominator_exponent in denominator_exponents:
            for time_unit in time_units:
                # Construct unit ID
                numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
                denominator_prefix_id = _id_prefix_lookup[denominator_exponent]
                unit_id = f'{numerator_prefix_id}MOL_PER_{_time_unit_id_lookup[time_unit]}_PER_{denominator_prefix_id}L'

                # Construct unit string
                numerator_prefix_si = _si_prefix_string[numerator_exponent]
                denominator_prefix_si = _si_prefix_string[denominator_exponent]
                unit_str = f'{numerator_prefix_si}mol/{time_unit}/{denominator_prefix_si}L'

                # Construct synonyms
                synonyms = [
                    unit_str,
                    f'{numerator_prefix_si}mol/{time_unit}/{denominator_prefix_si}L',
                    f'{numerator_prefix_si}mol/({time_unit}.{denominator_prefix_si}L)',
                    f'{numerator_prefix_si}mol.{time_unit}-1.{denominator_prefix_si}L-1'
                ]
                time_unit_multiplier = inv_map[time_unit]

                # Create and add definitions
                definition = {
                    "id" : unit_id,
                    "qudt" : "",
                    "UCUM" : unit_str,
                    "synonyms" : synonyms,
                    "units": [
                        { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": numerator_exponent },
                        { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 },
                        { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": denominator_exponent }
                    ]
                }
                unit_definitions.append(definition)

def create_mol_per_gram_units() -> None:
    numerator_mass_exponents = [0, -3, -6, -9, -12]
    denominator_mass_exponents = [3, 0, -3, -6, -9]
    for numerator_exponent in numerator_mass_exponents:
        for denominator_exponent in denominator_mass_exponents:
            # Construct unit ID
            numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
            denominator_prefix_id = _id_prefix_lookup[denominator_exponent]
            unit_id = f'{numerator_prefix_id}MOL_PER_{denominator_prefix_id}GM'

            # Construct unit string
            numerator_prefix_si = _si_prefix_string[numerator_exponent]
            denominator_prefix_si = _si_prefix_string[denominator_exponent]
            unit_str = f'{numerator_prefix_si}mol/{denominator_prefix_si}g'

            # Construct synonyms
            synonyms = [
                unit_str,
                f'{numerator_prefix_si}mol.{denominator_prefix_si}g-1'
            ]

            # Create and add definitions
            definition = {
                "id" : unit_id,
                "qudt" : "",
                "UCUM" : unit_str,
                "synonyms" : synonyms,
                "units": [
                    { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": numerator_exponent },
                    { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": denominator_exponent }
                ]
            }
            unit_definitions.append(definition)

def create_mol_per_liter_per_time_units() -> None:
    time_units = ['h', 'd', 'min', 's']
    numerator_exponents = [0, -3, -6, -9, -12]
    denominator_exponents = [3, 0, -3, -6]
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    for numerator_exponent in numerator_exponents:
        for denominator_exponent in denominator_exponents:
            for time_unit in time_units:
                # Construct unit ID
                numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
                denominator_prefix_id = _id_prefix_lookup[denominator_exponent]
                unit_id = f'{numerator_prefix_id}MOL_PER_{denominator_prefix_id}L_PER_{_time_unit_id_lookup[time_unit]}'

                # Construct unit string
                numerator_prefix_si = _si_prefix_string[numerator_exponent]
                denominator_prefix_si = _si_prefix_string[denominator_exponent]
                unit_str = f'{numerator_prefix_si}mol/{denominator_prefix_si}L/{time_unit}'

                # Construct synonyms
                synonyms = [
                    unit_str,
                    f'{numerator_prefix_si}mol/{denominator_prefix_si}L/{time_unit}',
                    f'{numerator_prefix_si}mol/({denominator_prefix_si}L.{time_unit})',
                    f'{numerator_prefix_si}mol.{denominator_prefix_si}L-1.{time_unit}-1'
                ]
                time_unit_multiplier = inv_map[time_unit]

                # Create and add definitions
                definition = {
                    "id" : unit_id,
                    "qudt" : "",
                    "UCUM" : unit_str,
                    "synonyms" : synonyms,
                    "units": [
                        { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": numerator_exponent },
                        { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": denominator_exponent },
                        { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 }
                    ]
                }
                unit_definitions.append(definition)

def create_mol_per_liter_units() -> None:
    numerator_mass_exponents = [3, 0, -3, -6, -9, -12]
    denominator_mass_exponents = [0, -3, -6]
    for numerator_exponent in numerator_mass_exponents:
        for denominator_exponent in denominator_mass_exponents:
            # Construct unit ID
            numerator_prefix_id = _id_prefix_lookup[numerator_exponent]
            denominator_prefix_id = _id_prefix_lookup[denominator_exponent]
            unit_id = f'{numerator_prefix_id}MOL_PER_{denominator_prefix_id}L'

            # Construct unit string
            numerator_prefix_si = _si_prefix_string[numerator_exponent]
            denominator_prefix_si = _si_prefix_string[denominator_exponent]
            unit_str = f'{numerator_prefix_si}mol/{denominator_prefix_si}L'

            # Construct synonyms
            synonyms = [
                unit_str,
                f'{numerator_prefix_si}mol.{denominator_prefix_si}L-1'
            ]

            # Create and add definitions
            definition = {
                "id" : unit_id,
                "qudt" : "",
                "UCUM" : unit_str,
                "synonyms" : synonyms,
                "units": [
                    { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": numerator_exponent },
                    { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": denominator_exponent }
                ]
            }
            unit_definitions.append(definition)

def create_mol_per_time_per_gram_units() -> None:
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    time_units = ['s', 'min', 'h', 'd']
    mol_unit_exponents = [0, -3, -6, -9, -12]
    gram_unit_exponents = [3, 0, -3, -6, -9, -12]
    for mol_unit_exponent in mol_unit_exponents:
        for gram_unit_exponent in gram_unit_exponents:
            for time_unit in time_units:
                # Construct unit ID
                mol_unit_prefix_id = _id_prefix_lookup[mol_unit_exponent]
                gram_unit_prefix_id = _id_prefix_lookup[gram_unit_exponent]
                unit_id = f'{mol_unit_prefix_id}MOL_PER_{_time_unit_id_lookup[time_unit]}_PER_{gram_unit_prefix_id}GM'

                # Construct unit string
                mol_unit_prefix_si = _si_prefix_string[mol_unit_exponent]
                gram_unit_prefix_si = _si_prefix_string[gram_unit_exponent]
                unit_str = f'{mol_unit_prefix_si}mol/{time_unit}/{gram_unit_prefix_si}g'

                # Construct synonyms
                synonyms = [
                    unit_str,
                    f'{mol_unit_prefix_si}mol/({time_unit}.{gram_unit_prefix_si}g)',
                    f'{mol_unit_prefix_si}mol.{time_unit}-1.{gram_unit_prefix_si}g-1'
                ]
                time_unit_multiplier = inv_map[time_unit]

                # Create and add definitions
                definition = {
                    "id" : unit_id,
                    "qudt" : "",
                    "UCUM" : unit_str,
                    "synonyms" : synonyms,
                    "units": [
                        { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": mol_unit_exponent },
                        { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 },
                        { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": gram_unit_exponent }
                    ]
                }
                unit_definitions.append(definition)

def create_mol_per_time_units() -> None:
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    mass_exponents = [0, -3, -6, -9, -12]
    time_units = ['s', 'min', 'h', 'd']
    for mol_unit_exponent in mass_exponents:
        for time_unit in time_units:
            # Construct unit ID
            mol_unit_prefix_id = _id_prefix_lookup[mol_unit_exponent]
            unit_id = f'{mol_unit_prefix_id}MOL_PER_{_time_unit_id_lookup[time_unit]}'

            # Construct unit string
            mol_unit_prefix_si = _si_prefix_string[mol_unit_exponent]
            unit_str = f'{mol_unit_prefix_si}mol/{time_unit}'

            # Construct synonyms
            synonyms = [
                unit_str,
                f'{mol_unit_prefix_si}mol.{time_unit}-1'
            ]
            time_unit_multiplier = inv_map[time_unit]

            # Create and add definitions
            definition = {
                "id" : unit_id,
                "qudt" : "",
                "UCUM" : unit_str,
                "synonyms" : synonyms,
                "units": [
                    { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": mol_unit_exponent },
                    { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 }
                ]
            }
            unit_definitions.append(definition)

def create_mol_units() -> None:
    exponents = [0, -3, -6, -9, -12]
    for exponent in exponents:
        # Construct unit ID
        id_prefix = _id_prefix_lookup[exponent]
        unit_id = f'{id_prefix}MOL'

        # Construct unit string
        si_prefix = _si_prefix_string[exponent]
        unit_str = f'{si_prefix}mol'

        # Create and add definitions
        definition = {
            "id" : unit_id,
            "qudt" : "",
            "UCUM" : unit_str,
            "synonyms" : [unit_str],
            "units": [
                { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": exponent }
            ]
        }
        unit_definitions.append(definition)

def create_per_time_units() -> None:
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    time_units = ['s', 'min', 'h', 'd', 'y']
    for time_unit in time_units:
        # Construct unit ID
        unit_id = f'PER_{_time_unit_id_lookup[time_unit]}'

        # Construct unit string
        unit_str = f'/{time_unit}'

        # Construct synonyms
        synonyms = [
            unit_str,
            f'1/{time_unit}',
            f'{time_unit}-1'
        ]
        time_unit_multiplier = inv_map[time_unit]

        # Create and add definitions
        definition = {
            "id" : unit_id,
            "qudt" : "",
            "UCUM" : unit_str,
            "synonyms" : synonyms,
            "units": [
                { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": time_unit_multiplier, "scale": 0 }
            ]
        }
        unit_definitions.append(definition)

def create_time_units() -> None:
    inv_map = {v: k for k, v in _time_unit_multipliers.items()}
    time_units = ['s', 'min', 'h', 'd', 'y']
    for time_unit in time_units:
        # Construct unit ID
        unit_id = f'{_time_unit_id_lookup[time_unit]}'

        # Construct unit string
        unit_str = f'{time_unit}'

        # Construct synonyms
        synonyms = [
            unit_str
        ]
        time_unit_multiplier = inv_map[time_unit]

        # Create and add definitions
        definition = {
            "id" : unit_id,
            "qudt" : "",
            "UCUM" : unit_str,
            "synonyms" : synonyms,
            "units": [
                { "kind": ls.UNIT_KIND_SECOND, "exponent": 1, "multiplier": time_unit_multiplier, "scale": 0 },
            ]
        }
        unit_definitions.append(definition)

def create_pressure_units() -> None:
    unit_definitions.append({
        "id" : "PA",
        "qudt" : "PA",
        "UCUM" : "Pa",
        "synonyms" : [
            "Pa",
            "N/m^2",
            "kg/m/s^2",
            "kg/(m.s^2)",
            "kg.m-1.s-2"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 3 },
            { "kind": ls.UNIT_KIND_METRE, "exponent": -1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -2, "multiplier": 1, "scale": 0 }
        ]
    })

def create_temperature_units() -> None:
    unit_definitions.append({
        "id" : "K",
        "qudt" : "K",
        "UCUM" : "K",
        "synonyms" : [
            "K",
            "Kelvin"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_KELVIN, "exponent": 1, "multiplier": 1, "scale": 0 }
        ]
    })

def create_per_time_per_allometric_mass_units():
    # Allometrically scaled rate constant units scaled by body weight using allometric scaling
    per_time_per_allometric_mass_units = [
    {
        "id" : "PER_HR_KiloGM0P25",
        "qudt" : "",
        "UCUM" : "1/h.kg^0.25",
        "synonyms" : [
            "1/h.kg^0.25",
            "/h.kg^0.25",
            "1/h/kg^-0.25",
            "/h/kg^-0.25",
            "1/(h.kg^-0.25)",
            "/(h.kg^-0.25)",
            "h-1.kg0.25"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 0.25, "multiplier": 1, "scale": 3 },
        ]
    },
    {
        "id" : "PER_DAY_KiloGM0P25",
        "qudt" : "",
        "UCUM" : "1/d.kg^0.25",
        "synonyms" : [
            "1/d.kg^0.25",
            "/d.kg^0.25",
            "1/d/kg^-0.25",
            "/d/kg^-0.25",
            "1/(d.kg^-0.25)",
            "/(d.kg^-0.25)",
            "d-1.kg0.25"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 86400, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 0.25, "multiplier": 1, "scale": 3 },
        ]
    },
    {
        "id" : "PER_HR_PER_KiloGM0P25",
        "qudt" : "",
        "UCUM" : "1/h/kg^0.25",
        "synonyms" : [
            "1/h/kg^0.25",
            "/h/kg^0.25",
            "1/h/kg^0.25",
            "/h/kg^0.25",
            "1/(h.kg^0.25)",
            "/(h.kg^0.25)",
            "1/h.kg^-0.25",
            "/h.kg^-0.25",
            "h-1.kg-0.25"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -0.25, "multiplier": 1, "scale": 3 },
        ]
    },
    {
        "id" : "PER_DAY_PER_KiloGM0P25",
        "qudt" : "",
        "UCUM" : "1/d/kg^0.25",
        "synonyms" : [
            "1/d/kg^0.25",
            "/d/kg^0.25",
            "1/d/kg^0.25",
            "/d/kg^0.25",
            "1/(d.kg^0.25)",
            "/(d.kg^0.25)",
            "1/d.kg^-0.25",
            "/d.kg^-0.25",
            "d-1.kg-0.25"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 86400, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -0.25, "multiplier": 1, "scale": 3 },
        ]
    },
    {
        "id" : "PER_HR_PER_KiloGM0P75",
        "qudt" : "",
        "UCUM" : "1/(h.kg^0.75)",
        "synonyms" : [
            "1/h/kg^0.75",
            "/h/kg^0.75",
            "1/(h.kg^0.75)",
            "/(h.kg^0.75)",
            "h-1.kg-0.75"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -0.75, "multiplier": 1, "scale": 3 },
        ]
    },
    {
        "id" : "PER_DAY_PER_KiloGM0P75",
        "qudt" : "",
        "UCUM" : "1/(d.kg^0.75)",
        "synonyms" : [
            "1/d/kg^0.75",
            "/d/kg^0.75",
            "1/(d.kg^0.75)",
            "/(d.kg^0.75)",
            "d-1.kg-0.75"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 86400, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -0.75, "multiplier": 1, "scale": 3 },
        ]
    }
    ]
    unit_definitions.extend(per_time_per_allometric_mass_units)

# Unit definitions, translating a unit string to the elementary unit
# compositions following the SBML structure.
# Unit IDs should match up with vocabulary of QUDT (https://qudt.org/2.1/vocab/unit)
# except that the '-' character is replaced by '_' due to restrictions of SBML.
unit_definitions = [
    {
        "id" : "UNITLESS",
        "qudt" : "UNITLESS",
        "UCUM" : "",
        "synonyms" : [
            "unitless",
            "dimensionless"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_DIMENSIONLESS, "exponent": 1, "multiplier": 1, "scale": 0 }
        ]
    }
]

def get_volume_unit_definitions() -> list[dict]:
    """Return single-part volume unit definitions.

    Returns:
    list[dict]: A list of unit definition dictionaries representing volume units.
    """
    res = []
    for _, unit_def in enumerate(unit_definitions):
        if len(unit_def['units']) == 1 \
            and _is_volume_unit_part(unit_def['units'][0]):
            res.append(unit_def)
    return res

def get_mass_unit_definitions() -> list[dict]:
    """Return single-part mass unit definitions.

    Returns:
    list[dict]: A list of unit definition dictionaries representing mass units.
    """
    res = []
    for _, unit_def in enumerate(unit_definitions):
        if len(unit_def['units']) == 1 \
            and _is_mass_unit_part(unit_def['units'][0]):
            res.append(unit_def)
    return res

def get_time_unit_definitions() -> list[dict]:
    """Return single-part time unit definitions.

    Returns:
    list[dict]: A list of unit definition dictionaries representing time units.
    """
    res = []
    for _, unit_def in enumerate(unit_definitions):
        if len(unit_def['units']) == 1 \
            and _is_time_unit_part(unit_def['units'][0]):
            res.append(unit_def)
    return res

def get_temperature_unit_definitions() -> list[dict]:
    """Return single-part temperature unit definitions.

    Returns:
    list[dict]: A list of unit definition dictionaries representing temperature units.
    """
    res = []
    for _, unit_def in enumerate(unit_definitions):
        if len(unit_def['units']) == 1 \
            and _is_temperature_unit_part(unit_def['units'][0]):
            res.append(unit_def)
    return res

def get_unit_definition(
    unit_str: str
) -> dict | None:
    """
    Find unit definition that corresponds with the provided string.

    Parameters:
    unit_str (str): A unit identifier or synonym to search for.

    Returns:
    dict | None: The matching unit definition dictionary, or None if not found.
    """
    res = None
    for _, value in enumerate(unit_definitions):
        if value['id'].lower() == unit_str.lower() \
            or any(val.lower() == unit_str.lower() for val in value['synonyms']):
            res = value
            break
    return res

def get_ucum_unit_string(
    unit_str: str
) -> str:
    """Return the UCUM representation for a unit string.

    Parameters:
    unit_str (str): A unit string to search for.

    Returns:
    str: The UCUM formatted unit string if found, otherwise an empty string.
    """
    if unit_str:
        for _, value in enumerate(unit_definitions):
            if unit_str.lower() == value['id'].lower() \
                or any(val.lower() == unit_str.lower() for val in value['synonyms']):
                return value['UCUM'] if value['UCUM'] else value['id']
    return ""

def set_unit_definition(
    sbml_unit_definition: ls.UnitDefinition,
    definition
):
    """Populate a libSBML UnitDefinition from a unit definition dictionary.

    Parameters:
    sbml_unit_definition (libsbml.UnitDefinition): The libSBML UnitDefinition object to populate.
    definition (dict): The source unit definition dictionary.
    """
    definition_id = definition["id"]
    sbml_unit_definition.setId(definition_id)
    for unit_part in definition["units"]:
        u = sbml_unit_definition.createUnit()
        u.setKind(unit_part["kind"])
        u.setExponent(unit_part["exponent"])
        u.setMultiplier(unit_part["multiplier"])
        u.setScale(unit_part["scale"])

def create_unit_string(
    unit: ls.UnitDefinition,
    ext: bool = False
) -> str:
    """Build a textual string representation of an SBML UnitDefinition.

    Parameters:
    unit (libsbml.UnitDefinition): The SBML unit definition to convert.
    ext (bool, optional):  If True, use extended unit names (e.g. 'liter' instead of 'L').

    Returns:
    str: A combined unit string, or 'dimensionless' when no unit parts exist.
    """
    unit_string_parts = []
    for i in range(unit.getNumUnits()):
        unit_part = unit.getUnit(i)
        unit_part_string = _create_unit_part_string(unit_part, ext, i == 0)
        if unit_part_string:
            unit_string_parts.append(unit_part_string)
    result = ''.join(unit_string_parts) if unit_string_parts else 'dimensionless'
    return result

def _create_unit_part_string(
    u: ls.Unit,
    ext: bool = False,
    is_first: bool = False,
) -> str:
    """Format a single SBML Unit part into a string.

    Parameters:
    u (libsbml.Unit): The SBML unit part to format.
    ext (bool, optional): If True, return extended unit names.
    is_first (bool, optional): If True, omit the leading operator for the first unit part.

    Returns:
    str: The formatted unit part string.
    """
    kind = u.getKind()
    scale = u.getScale()
    exponent = u.getExponentAsDouble()
    multiplier = u.getMultiplier()
    if kind == ls.UNIT_KIND_SECOND:
        effective_multiplier = multiplier * (10 ** scale)
        if effective_multiplier in _time_unit_multipliers:
            base_unit_str = _time_unit_multipliers[effective_multiplier]
            multiplier = 1
            scale = 0
        else:
            base_unit_str = 's'
    else:
        base_unit_str = _base_unit_strings_ext.get(kind) if ext else _base_unit_strings.get(kind)

    scale_str = _si_prefix_strings_ext.get(scale) if ext else _si_prefix_string.get(scale)
    if exponent >= 0:
        if is_first:
            operator_str = ''
        else:
            operator_str = '.'
    else:
        operator_str = '/'
        exponent = -exponent
    exponent_str = f"^{exponent:g}" if exponent != 1 else ''
    multiplier_str = f"{multiplier}." if multiplier != 1 else ''
    ucum_unit = f"{operator_str}{multiplier_str}{scale_str}{base_unit_str}{exponent_str}"
    return ucum_unit

def get_unit_type(unit_def: dict) -> UnitType:
    """Classify a unit definition into a UnitType category.

    Parameters:
    unit_def (dict): A unit definition dictionary from :data:`unit_definitions`.

    Returns:
    UnitType: The inferred category for the unit definition.
    """
    if len(unit_def['units']) == 1:
        unit = unit_def['units'][0]
        if unit['kind'] == ls.UNIT_KIND_DIMENSIONLESS:
            return UnitType.DIMENSIONLESS
        if _is_mass_unit_part(unit):
            return UnitType.MASS_UNIT
        if _is_volume_unit_part(unit):
            return UnitType.VOLUME_UNIT
        if _is_time_unit_part(unit):
            return UnitType.TIME_UNIT
        if _is_temperature_unit_part(unit):
            return UnitType.TEMPERATURE_UNIT
        return UnitType.OTHER
    if len(unit_def['units']) == 2:
        if any(_is_mass_unit_part(part) for part in unit_def['units']) \
            and (any(_is_per_volume_unit_part(part) for part in unit_def['units']) \
            or any(_is_per_mass_unit_part(part) for part in unit_def['units'])):
            return UnitType.CONCENTRATION_UNIT
    return UnitType.OTHER

def _is_mass_unit_part(unit_part: dict):
    """Return True when the unit part is a mass unit with exponent 1."""
    return (unit_part['kind'] == ls.UNIT_KIND_GRAM \
        or unit_part['kind'] == ls.UNIT_KIND_MOLE) \
        and unit_part['exponent'] == 1

def _is_per_mass_unit_part(unit_part: dict):
    """Return True when the unit part is a per-mass unit with exponent -1."""
    return (unit_part['kind'] == ls.UNIT_KIND_GRAM \
        or unit_part['kind'] == ls.UNIT_KIND_MOLE) \
        and unit_part['exponent'] == -1

def _is_volume_unit_part(unit_part: dict):
    """Return True when the unit part is a volume unit with exponent 1."""
    return (unit_part['kind'] == ls.UNIT_KIND_LITRE \
        or unit_part['kind'] == ls.UNIT_KIND_LITER) \
        and unit_part['exponent'] == 1

def _is_per_volume_unit_part(unit_part: dict):
    """Return True when the unit part is a per-volume unit with exponent -1."""
    return (unit_part['kind'] == ls.UNIT_KIND_LITRE \
        or unit_part['kind'] == ls.UNIT_KIND_LITER) \
        and unit_part['exponent'] == -1

def _is_time_unit_part(unit_part: dict):
    """Return True when the unit part is a time unit with exponent 1."""
    return unit_part['kind'] == ls.UNIT_KIND_SECOND \
        and unit_part['exponent'] == 1

def _is_temperature_unit_part(unit_part: dict):
    """Return True when the unit part is a temperature unit with exponent 1."""
    return unit_part['kind'] == ls.UNIT_KIND_KELVIN \
        and unit_part['exponent'] == 1


create_area_units()
create_gram_units()
create_gram_per_gram_units()
create_gram_per_liter_units()
create_gram_per_time_units()
create_gram_per_time_per_allometric_mass_units()
create_gram_per_time_per_gram_units()
create_gram_per_time_per_volume_units()
create_length_per_time_units()
create_length_units()
create_liter_per_gram_units()
create_liter_per_gram_per_time_units()
create_liter_per_time_per_allometric_mass_units()
create_liter_per_time_per_gram_units()
create_liter_per_time_units()
create_liter_units()
create_molar_mass_unit()
create_mol_per_gram_units()
create_mol_per_liter_units()
create_mol_per_liter_per_time_units()
create_mol_per_time_per_allometric_mass_units()
create_mol_per_time_per_gram_units()
create_mol_per_time_per_mol_units()
create_mol_per_time_per_volume_units()
create_mol_per_time_units()
create_mol_units()
create_per_time_units()
create_per_time_per_allometric_mass_units()
create_time_units()
create_pressure_units()
create_temperature_units()
