import libsbml as ls

def set_unit_definition(
    unit_definition,
    definition
):
    """ Sets the libSBML unit definition according to the unit definition."""
    id = definition["id"]
    unit_definition.setId(id)
    for unitPart in definition["units"]:
        u = unit_definition.createUnit()
        u.setKind(unitPart["kind"])
        u.setExponent(unitPart["exponent"])
        u.setMultiplier(unitPart["multiplier"])
        u.setScale(unitPart["scale"])

# Unit definitions, translating a unit string to the elementary unit
# compositions following the SBML structure.
# Unit IDs should match up with vocabulary of QUDT (https://qudt.org/2.1/vocab/unit) 
# except that the '-' character is replaced by '_' due to restrictions of SBML.
UnitDefinitions = [
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
        "UCUM" : "hmin",
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
        "id" : "L_PER_DAY_KiloGM3DIV4",
        "qudt" : "",
        "UCUM" : "L/(d.kg^0.75)",
        "synonyms" : [
            "L_PER_DAY_KiloGM3DIV4.75",
            "L/d/kg^0.75",
            "L/(d.kg^0.75)",
            "L.d-1.kg-0.75)"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": 0 },
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
    }
]
