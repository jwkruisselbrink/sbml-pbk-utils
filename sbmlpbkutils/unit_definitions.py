import enum
import libsbml as ls

class UnitType(enum.Enum):
    DIMENSIONLESS = 1           # Unitless/dimensionless
    MASS_UNIT = 2               # Grams or moles
    VOLUME_UNIT = 3             # Liters
    TIME_UNIT = 4               # Seconds
    CONCENTRATION_UNIT = 5,     # Grams per mass or volume
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
    ls.UNIT_KIND_MOLE: 'mol'
}

_base_unit_strings_ext = {
    ls.UNIT_KIND_DIMENSIONLESS: '',
    ls.UNIT_KIND_SECOND: 'second',
    ls.UNIT_KIND_GRAM: 'gram',
    ls.UNIT_KIND_LITER: 'liter',
    ls.UNIT_KIND_LITRE: 'liter',
    ls.UNIT_KIND_METER: 'meter',
    ls.UNIT_KIND_METRE: 'meter',
    ls.UNIT_KIND_MOLE: 'mole'
}

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
    },
    # Amount/volume units
    {
        "id" : "MOL",
        "qudt" : "MOL",
        "UCUM" : "mol",
        "synonyms" : [
            "mol"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "MilliMOL",
        "qudt" : "MilliMOL",
        "UCUM" : "mmol",
        "synonyms" : [
            "mmol"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 }
        ]
    },
    {
        "id" : "MicroMOL",
        "qudt" : "MicroMOL",
        "UCUM" : "umol",
        "synonyms" : [
            "umol"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -6 }
        ]
    },
    {
        "id" : "NanoMOL",
        "qudt" : "NanoMOL",
        "UCUM" : "nmol",
        "synonyms" : [
            "nmol"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -9 }
        ]
    },
    {
        "id" : "PicoMOL",
        "qudt" : "PicoMOL",
        "UCUM" : "pmol",
        "synonyms" : [
            "pmol"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -12 }
        ]
    },
    {
        "id" : "KiloGM",
        "qudt" : "KiloGM",
        "UCUM" : "kg",
        "synonyms" : [
            "kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 3 }
        ]
    },
    {
        "id" : "GM",
        "qudt" : "GM",
        "UCUM" : "g",
        "synonyms" : [
            "g"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "MilliGM",
        "qudt" : "MilliGM",
        "UCUM" : "mg",
        "synonyms" : [
            "mg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -3 }
        ]
    },
    {
        "id" : "MicroGM",
        "qudt" : "MicroGM",
        "UCUM" : "ug",
        "synonyms" : [
            "ug"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -6 }
        ]
    },
    {
        "id" : "NanoGM",
        "qudt" : "NanoGM",
        "UCUM" : "ng",
        "synonyms" : [
            "ng"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -9 }
        ]
    },
    {
        "id" : "PicoGM",
        "qudt" : "PicoGM",
        "UCUM" : "pg",
        "synonyms" : [
            "pg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -12 }
        ]
    },
    {
        "id" : "L",
        "qudt" : "L",
        "UCUM" : "L",
        "synonyms" : [
            "L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "MilliL",
        "qudt" : "MilliL",
        "UCUM" : "mL",
        "synonyms" : [
            "mL"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": -3 }
        ]
    },
    {
        "id" : "CentiL",
        "qudt" : "CentiL",
        "UCUM" : "cL",
        "synonyms" : [
            "cL"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": -2 }
        ]
    },
    {
        "id" : "DeciL",
        "qudt" : "DeciL",
        "UCUM" : "dL",
        "synonyms" : [
            "dL"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": -1 }
        ]
    },
    {
        "id" : "MicroL",
        "qudt" : "MicroL",
        "UCUM" : "uL",
        "synonyms" : [
            "uL"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": -6 }
        ]
    },
    # Molas mass
    {
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
    },
    # Per mass concentrations units
    {
        "id" : "MicroGM_PER_KiloGM",
        "qudt" : "MicroGM-PER-KiloGM",
        "UCUM" : "ug/kg",
        "synonyms" : [
            "ug/kg",
            "ug_per_kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -6 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
        ]
    },
    {
        "id" : "MilliGM_PER_KiloGM",
        "qudt" : "MilliGM-PER-KiloGM",
        "UCUM" : "mg/kg",
        "synonyms" : [
            "mg/kg",
            "mg_per_kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
        ]
    },
    {
        "id" : "GM_PER_KiloGM",
        "qudt" : "GM-PER-KiloGM",
        "UCUM" : "g/kg",
        "synonyms" : [
            "g/kg",
            "g_per_kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
        ]
    },
    {
        "id" : "MicroGM_PER_GM",
        "qudt" : "MicroGM-PER-GM",
        "UCUM" : "ug/g",
        "synonyms" : [
            "ug/g",
            "ug_per_g"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -6 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "MilliGM_PER_GM",
        "qudt" : "MilliGM-PER-GM",
        "UCUM" : "mg/kg",
        "synonyms" : [
            "mg/g",
            "mg_per_g"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "GM_PER_GM",
        "qudt" : "GM-PER-GM",
        "UCUM" : "g/g",
        "synonyms" : [
            "g/g",
            "g_per_g"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "MOL_PER_KiloGM",
        "qudt" : "MOL-PER-KiloGM",
        "UCUM" : "mol/kg",
        "synonyms" : [
            "mol/kg",
            "mol_per_kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
        ]
    },
    {
        "id" : "MilliMOL_PER_KiloGM",
        "qudt" : "MilliMOL-PER-KiloGM",
        "UCUM" : "mmol/kg",
        "synonyms" : [
            "mmol/kg",
            "mmol_per_kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
        ]
    },
    {
        "id" : "MicroMOL_PER_KiloGM",
        "qudt" : "MicroMOL-PER-KiloGM",
        "UCUM" : "umol/kg",
        "synonyms" : [
            "umol/kg",
            "umol_per_kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -6 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
        ]
    },
    {
        "id" : "NanoMOL_PER_KiloGM",
        "qudt" : "NanoMOL-PER-KiloGM",
        "UCUM" : "nmol/kg",
        "synonyms" : [
            "nmol/kg",
            "nmol_per_kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -9 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
        ]
    },
    {
        "id" : "PicoMOL_PER_KiloGM",
        "qudt" : "PicoMOL-PER-KiloGM",
        "UCUM" : "pmol/kg",
        "synonyms" : [
            "pmol/kg",
            "pmol_per_kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -12 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
        ]
    },
    {
        "id" : "MOL_PER_GM",
        "qudt" : "MOL-PER-GM",
        "UCUM" : "mol/g",
        "synonyms" : [
            "mol/g",
            "mol_per_g"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "MilliMOL_PER_GM",
        "qudt" : "MilliMOL-PER-GM",
        "UCUM" : "mmol/g",
        "synonyms" : [
            "mmol/g",
            "mmol_per_g"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "MicroMOL_PER_GM",
        "qudt" : "MicroMOL-PER-GM",
        "UCUM" : "umol/g",
        "synonyms" : [
            "umol/g",
            "umol_per_g"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -6 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "NanoMOL_PER_GM",
        "qudt" : "NanoMOL-PER-GM",
        "UCUM" : "nmol/g",
        "synonyms" : [
            "nmol/g",
            "nmol_per_g"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -9 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "PicoMOL_PER_MilliGM",
        "qudt" : "PicoMOL-PER-MilliGM",
        "UCUM" : "pmol/mg",
        "synonyms" : [
            "pmol/mg",
            "pmol_per_mg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -12 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": -3 }
        ]
    },
    {
        "id" : "L_PER_KiloGM",
        "qudt" : "L-PER-KiloGM",
        "UCUM" : "L/kg",
        "synonyms" : [
            "L/kg",
            "L_per_kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
        ]
    },
    # Per volume concentrations units
    {
        "id" : "MicroGM_PER_L",
        "qudt" : "MicroGM-PER-L",
        "UCUM" : "ug/L",
        "synonyms" : [
            "ug_per_L",
            "ug/L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -6 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "MilliGM_PER_L",
        "qudt" : "MilliGM-PER-L",
        "UCUM" : "mg/L",
        "synonyms" : [
            "mg_per_L",
            "mg/L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "GM_PER_L",
        "qudt" : "GM-PER-L",
        "UCUM" : "g/L",
        "synonyms" : [
            "g_per_L",
            "g/L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "KiloGM_PER_L",
        "qudt" : "KiloGM-PER-L",
        "UCUM" : "kg/L",
        "synonyms" : [
            "kg_per_L",
            "kg/L",
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 3 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "MOL_PER_L",
        "qudt" : "MOL-PER-L",
        "UCUM" : "mol/L",
        "synonyms" : [
            "mol_per_L",
            "mol/L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "MilliMOL_PER_L",
        "qudt" : "MilliMOL-PER-L",
        "UCUM" : "mmol/L",
        "synonyms" : [
            "mmol_per_L",
            "mmol/L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "MicroMOL_PER_L",
        "qudt" : "MicroMOL-PER-L",
        "UCUM" : "umol/L",
        "synonyms" : [
            "umol_per_L",
            "umol/L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -6 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    # Time units
    {
        "id" : "SEC",
        "qudt" : "SEC",
        "UCUM" : "s",
        "synonyms" : [
            "seconds",
            "s"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": 1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "MIN",
        "qudt" : "MIN",
        "UCUM" : "min",
        "synonyms" : [
            "minutes",
            "minute",
            "min"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": 1, "multiplier": 60, "scale": 0 }
        ]
    },
    {
        "id" : "HR",
        "qudt" : "HR",
        "UCUM" : "h",
        "synonyms" : [
            "hours",
            "h"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": 1, "multiplier": 3600, "scale": 0 }
        ]
    },
    {
        "id" : "DAY",
        "qudt" : "DAY",
        "UCUM" : "d",
        "synonyms" : [
            "days",
            "d"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": 1, "multiplier": 24 * 3600, "scale": 0 }
        ]
    },
    {
        "id" : "YR",
        "qudt" : "YR",
        "UCUM" : "y",
        "synonyms" : [
            "years",
            "year",
            "yr",
            "y"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": 1, "multiplier": 365.25 * 24 * 3600, "scale": 0 }
        ]
    },
    # Rate units
    {
        "id" : "PER_SEC",
        "qudt" : "PER-SEC",
        "UCUM" : "/s",
        "synonyms" : [
            "per_second",
            "1/sec",
            "1/s",
            "/s",
            "s-1"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "PER_H",
        "qudt" : "PER-H",
        "UCUM" : "/h",
        "synonyms" : [
            "per_hour",
            "1/h",
            "/h",
            "h-1"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 0 }
        ]
    },
    {
        "id" : "PER_DAY",
        "qudt" : "PER-DAY",
        "UCUM" : "/d",
        "synonyms" : [
            "per_day",
            "1/day",
            "1/d",
            "/d",
            "d-1"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 24 * 3600, "scale": 0 }
        ]
    },
    {
        "id" : "MilliMOL_PER_HR",
        "qudt" : "MilliMOL-PER-HR",
        "UCUM" : "mmol/h",
        "synonyms" : [
            "mmol_per_hour",
            "mmol/h"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 0 }
        ]
    },
    {
        "id" : "MOL_PER_HR",
        "qudt" : "MOL-PER-HR",
        "UCUM" : "mol/h",
        "synonyms" : [
            "mol/h",
            "mol_per_hour"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 0 }
        ]
    },
    {
        "id" : "L_PER_HR",
        "qudt" : "L-PER-HR",
        "UCUM" : "L/h",
        "synonyms" : [
            "L_per_h",
            "L/h",
            "L.h-1"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 0 }
        ]
    },
    {
        "id" : "L_PER_DAY",
        "qudt" : "L-PER-DAY",
        "UCUM" : "L/day",
        "synonyms" : [
            "L_PER_DAY",
            "L/d",
            "L.d-1"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 86400, "scale": 0 }
        ]
    },
    {
        "id" : "CentiM_PER_HR",
        "qudt" : "CentiM-PER-HR",
        "UCUM" : "cm/h",
        "synonyms" : [
            "cm_per_hour",
            "cm/h",
            "cm.h-1"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_METRE, "exponent": 1, "multiplier": 1, "scale": -2 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 0 }
        ]
    },
    {
        "id" : "DeciM_PER_HR",
        "qudt" : "DeciM-PER-HR",
        "UCUM" : "dm/h",
        "synonyms" : [
            "dm_per_hour",
            "dm/h",
            "dm.h-1"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_METRE, "exponent": 1, "multiplier": 1, "scale": -1 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 0 }
        ]
    },
    # Rate per mass units
    {
        "id" : "L_PER_KiloGM_HR",
        "qudt" : "L-PER-KiloGM-HR",
        "UCUM" : "L/(kg.h)",
        "synonyms" : [
            "L_per_kg_h",
            "L/(kg.h)",
            "L/kg/h",
            "L.kg-1.h-1"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 0 },
        ]
    },
    {
        "id" : "MilliMOL_PER_L_HR",
        "qudt" : "MilliMOL-PER-L-HR",
        "UCUM" : "mmol/(L.h)",
        "synonyms" : [
            "mmol/(L.h)",
            "mmol/L/h",
            "mM_per_L_h",
            "mM.L-1.h-1"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 0 },
        ]
    },
    {
        "id" : "L_PER_DAY_PER_KiloGM0P75",
        "qudt" : "",
        "UCUM" : "L/(d.kg^0.75)",
        "synonyms" : [
            "L_PER_DAY_PER_KiloGM3DIV4",
            "L/d/kg^0.75",
            "L/(d.kg^0.75)",
            "L.d-1.kg-0.75"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 86400, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -0.75, "multiplier": 1, "scale": 3 },
        ]
    },
    {
        "id" : "PER_DAY_PER_KiloGM0P25",
        "qudt" : "",
        "UCUM" : "1/(d.kg^0.25)",
        "synonyms" : [
            "PER_DAY_PER_KiloGM0P25",
            "1/d/kg^0.25",
            "/d/kg^0.25",
            "1/(d.kg^0.25)",
            "/(d.kg^0.25)",
            "d-1.kg-0.25"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 86400, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -0.25, "multiplier": 1, "scale": 3 },
        ]
    },
    {
        "id" : "MicroGM_PER_DAY_PER_KiloGM0P75",
        "qudt" : "",
        "UCUM" : "ug/(d.kg^0.75)",
        "synonyms" : [
            "MicroGM_PER_DAY_PER_KiloGM3DIV4",
            "ug/d/kg^0.75",
            "ug/(d.kg^0.75)",
            "ug.d-1.kg-0.75"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -6 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 86400, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -0.75, "multiplier": 1, "scale": 3 },
        ]
    },
    {
        "id" : "PicoMOL_PER_MIN_PER_PicoMOL",
        "qudt" : "",
        "UCUM" : "pmol/min/pmol",
        "synonyms" : [
            "pmol/min/pmol",
            "pmol/(min.pmol)"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -12 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 60, "scale": 0 },
            { "kind": ls.UNIT_KIND_MOLE, "exponent": -1, "multiplier": 1, "scale": -12 },
        ]
    },
    {
        "id" : "PicoMOL_PER_MIN_PER_MilliGM",
        "qudt" : "",
        "UCUM" : "pmol/min/mg",
        "synonyms" : [
            "pmol/min/mg",
            "pmol/(min.mg)"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -12 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 60, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": -3 },
        ]
    },
    {
        "id" : "MicroMOL_PER_HR_PER_KiloGM",
        "qudt" : "",
        "UCUM" : "umol/hr/kg",
        "synonyms" : [
            "umol/hr/kg",
            "umol/h/kg",
            "umol/(hr.kg)",
            "umol/(h.kg)"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -6 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 },
        ]
    },
    {
        "id" : "NanoMOL_PER_MIN_PER_MilliL",
        "qudt" : "",
        "UCUM" : "nmol/min/mL",
        "synonyms" : [
            "nmol/min/mL",
            "nmol/(min.mL)"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -9 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 60, "scale": 0 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": -3 },
        ]
    },
    # Area units
    {
        "id" : "CentiM2",
        "qudt" : "CentiM2",
        "UCUM" : "cm2",
        "synonyms" : [
            "cm_square",
            "cm^2",
            "cm2"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_METRE, "exponent": 2, "multiplier": 1, "scale": -2 },
        ]
    },
    {
        "id" : "DeciM2",
        "qudt" : "DeciM2",
        "UCUM" : "dm2",
        "synonyms" : [
            "dm_square",
            "dm^2",
            "dm2"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_METRE, "exponent": 2, "multiplier": 1, "scale": -1 },
        ]
    },
    # Length units
    {
        "id" : "CentiM",
        "qudt" : "CentiM",
        "UCUM" : "cm",
        "synonyms" : [
            "cm"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_METRE, "exponent": 1, "multiplier": 1, "scale": -2 },
        ]
    },
    {
        "id" : "DeciM",
        "qudt" : "DeciM",
        "UCUM" : "dm",
        "synonyms" : [
            "dm"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_METRE, "exponent": 1, "multiplier": 1, "scale": -1 },
        ]
    },
    # Pressure units
    {
        "id" : "PA",
        "qudt" : "PA",
        "UCUM" : "Pa",
        "synonyms" : [
            "KiloGM-PER-M-SEC2",
            "N-PER-M2",
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
    }
]

def get_volume_unit_definitions() -> list[dict]:
    res = []
    for index, unit_def in enumerate(unit_definitions):
        if len(unit_def['units']) == 1 \
            and _is_volume_unit_part(unit_def['units'][0]):
            res.append(unit_def)
    return res

def get_mass_unit_definitions() -> list[dict]:
    res = []
    for index, unit_def in enumerate(unit_definitions):
        if len(unit_def['units']) == 1 \
            and _is_mass_unit_part(unit_def['units'][0]):
            res.append(unit_def)
    return res

def get_time_unit_definitions() -> list[dict]:
    res = []
    for index, unit_def in enumerate(unit_definitions):
        if len(unit_def['units']) == 1 \
            and _is_time_unit_part(unit_def['units'][0]):
            res.append(unit_def)
    return res

def get_unit_definition(
    unit_str: str
) -> dict:
    """
    Find unit definition that corresponds with the provided string.
    Returns none if no matching unit definition was found.
    """
    res = None
    for index, value in enumerate(unit_definitions):
        if value['id'].lower() == unit_str.lower() \
            or any(val.lower() == unit_str.lower() for val in value['synonyms']):
            res = value
            break
    return res

def get_ucum_unit_string(
    unit_str: str
) -> str:
    """Tries to get the (UCUM formated) unit string of the specified element."""
    if (unit_str):
        for index, value in enumerate(unit_definitions):
            if unit_str.lower() == value['id'].lower() \
                or any(val.lower() == unit_str.lower() for val in value['synonyms']):
                return value['UCUM'] if value['UCUM'] else value['id']
    return ""

def set_unit_definition(
    sbml_unit_definition: ls.UnitDefinition,
    definition
):
    """ Sets the libSBML unit definition according to the unit definition."""
    id = definition["id"]
    sbml_unit_definition.setId(id)
    for unitPart in definition["units"]:
        u = sbml_unit_definition.createUnit()
        u.setKind(unitPart["kind"])
        u.setExponent(unitPart["exponent"])
        u.setMultiplier(unitPart["multiplier"])
        u.setScale(unitPart["scale"])

def create_unit_string(
    unit: ls.UnitDefinition,
    ext: bool = False
) -> str:
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
    kind = u.getKind()
    scale = u.getScale()
    exponent = u.getExponentAsDouble()
    multiplier = u.getMultiplier()
    if kind == ls.UNIT_KIND_SECOND:
        if multiplier in _time_unit_multipliers.keys():
            base_unit_str = _time_unit_multipliers[multiplier]
            multiplier = 1
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
    if len(unit_def['units']) == 1:
        unit = unit_def['units'][0]
        if unit['kind'] == ls.UNIT_KIND_DIMENSIONLESS:
            return UnitType.DIMENSIONLESS
        elif _is_mass_unit_part(unit):
            return UnitType.MASS_UNIT
        elif _is_volume_unit_part(unit):
            return UnitType.VOLUME_UNIT
        elif _is_time_unit_part(unit):
            return UnitType.TIME_UNIT
        else:
            return UnitType.OTHER
    elif len(unit_def['units']) == 2:
        if any(_is_mass_unit_part(part) for part in unit_def['units']) \
            and (any(_is_per_volume_unit_part(part) for part in unit_def['units']) \
            or any(_is_per_mass_unit_part(part) for part in unit_def['units'])):
                return UnitType.CONCENTRATION_UNIT
    else:
        return UnitType.OTHER

def _is_mass_unit_part(unit_part: dict):
    return (unit_part['kind'] == ls.UNIT_KIND_GRAM \
        or unit_part['kind'] == ls.UNIT_KIND_MOLE) \
        and unit_part['exponent'] == 1

def _is_per_mass_unit_part(unit_part: dict):
    return (unit_part['kind'] == ls.UNIT_KIND_GRAM \
        or unit_part['kind'] == ls.UNIT_KIND_MOLE) \
        and unit_part['exponent'] == -1

def _is_volume_unit_part(unit_part: dict):
    return (unit_part['kind'] == ls.UNIT_KIND_LITRE \
        or unit_part['kind'] == ls.UNIT_KIND_LITER) \
        and unit_part['exponent'] == 1

def _is_per_volume_unit_part(unit_part: dict):
    return (unit_part['kind'] == ls.UNIT_KIND_LITRE \
        or unit_part['kind'] == ls.UNIT_KIND_LITER) \
        and unit_part['exponent'] == -1

def _is_time_unit_part(unit_part: dict):
    return unit_part['kind'] == ls.UNIT_KIND_SECOND \
        and unit_part['exponent'] == 1

def _is_per_time_unit_part(unit_part: dict):
    return unit_part['kind'] == ls.UNIT_KIND_SECOND \
        and unit_part['exponent'] == -1
