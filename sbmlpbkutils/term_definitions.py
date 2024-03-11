TermDefinitions = [
    # Model terms: species
    {
        "name": "mammals",
        "element_type": "model",
        "description": "Model for mammals (mammalia).",
        "synonyms": [
            "mammalia",
            "mammals"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:hasTaxon",
                "URI": "taxonomy/40674"
            }
        ]
    },
    {
        "name": "human",
        "element_type": "model",
        "description": "Model for human (homo sapiens).",
        "synonyms": [
            "homo sapiens",
            "human"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:hasTaxon",
                "URI": "taxonomy/9606"
            }
        ]
    },
    # Compartment terms
    {
        "name": "adipose tissue",
        "element_type": "compartment",
        "description": "Adipose tissue (fat) compartment.",
        "synonyms": [
            "fat",
            "adipose tissue"
        ],
        "recommended_id": "Fat",
        "common_ids": [
            "fat",
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/UBERON:0001013"
            }
        ]
    },
    {
        "name": "alveolar air",
        "element_type": "compartment",
        "description": "Alveolar air compartment.",
        "synonyms": [],
        "recommended_id": "Air",
        "common_ids": [
            "Air",
        ],
        "resources": [
            {
                "qualifier": "bqmodel:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00458"
            },
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/NCIT_C150891"
            }
        ]
    },
    {
        "name": "arterial blood",
        "element_type": "compartment",
        "description": "Arterial blood compartment.",
        "synonyms": [],
        "recommended_id": "Art",
        "common_ids": [
            "art",
        ],
        "resources": [
            {
                "qualifier": "bqmodel:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00462"
            },
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/UBERON:0013755"
            }
        ]
    },
    {
        "name": "arterial blood plasma",
        "element_type": "compartment",
        "description": "Arterial blood plasma compartment.",
        "synonyms": [],
        "recommended_id": "Art_Plas",
        "common_ids": [
            "Art_Plas",
            "Art_Plasma"
        ],
    },
    {
        "name": "blood",
        "element_type": "compartment",
        "description": "Blood compartment.",
        "synonyms": [],
        "recommended_id": "Blood",
        "common_ids": [
            "Blood"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/UBERON:0000178"
            }
        ]
    },
    {
        "name": "blood plasma",
        "element_type": "compartment",
        "description": "Blood plasma compartment.",
        "synonyms": [],
        "recommended_id": "Plasma",
        "common_ids": [
            "Plasma"
            "Blood_plasma"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/UBERON:0001969"
            }
        ]
    },
    {
        "name": "filtrate",
        "element_type": "compartment",
        "description": "Filtrate compartment.",
        "synonyms": [],
        "recommended_id": "Filtrate",
        "common_ids": [
            "filtrate",
            "fil"
        ]
    },
    {
        "name": "gut",
        "element_type": "compartment",
        "description": "Gut (digestive tract) compartment.",
        "synonyms": [],
        "recommended_id": "Gut",
        "common_ids": [
            "gut"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/UBERON:0001555"
            }
        ]
    },
    {
        "name": "kidney",
        "element_type": "compartment",
        "description": "Kidney compartment.",
        "synonyms": [],
        "recommended_id": "Kidney",
        "common_ids": [
            "kidney",
            "kid"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/UBERON:0002113"
            }
        ]
    },
    {
        "name": "liver",
        "element_type": "compartment",
        "description": "Liver compartment.",
        "synonyms": [],
        "recommended_id": "Liver",
        "common_ids": [
            "liver",
            "liv"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/UBERON:0002107"
            }
        ]
    },
    {
        "name": "lung",
        "element_type": "compartment",
        "description": "Lung compartment.",
        "synonyms": [],
        "recommended_id": "Lung",
        "common_ids": [
            "lung",
            "lungs"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/UBERON:0000479"
            }
        ]
    },
    {
        "name": "poorly perfused tissue",
        "element_type": "compartment",
        "description": "Poorly perfused tissue compartment.",
        "synonyms": [],
        "recommended_id": "Poor",
        "common_ids": [
            "Poor"
        ],
        "resources": [
            {
                "qualifier": "bqmodel:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00465"
            }
        ]
    },
    {
        "name": "rest-of-body",
        "element_type": "compartment",
        "description": "Rest-of-body compartment.",
        "synonyms": [],
        "recommended_id": "Rest",
        "common_ids": [
            "rest-of-body",
            "rest",
            "periphery"
        ],
        "resources": [
            {
                "qualifier": "bqmodel:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00460"
            }
        ]
    },
    {
        "name": "richly perfused tissue",
        "element_type": "compartment",
        "description": "Richly perfused tissue compartment.",
        "synonyms": [],
        "recommended_id": "Rich",
        "common_ids": [
            "Rich"
        ],
        "resources": [
            {
                "qualifier": "bqmodel:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00464"
            }
        ]
    },
    {
        "name": "skin",
        "element_type": "compartment",
        "description": "Skin compartment.",
        "synonyms": [],
        "recommended_id": "Skin",
        "common_ids": [
            "Skin"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/UBERON:0002097"
            }
        ]
    },
    {
        "name": "skin exposed",
        "element_type": "compartment",
        "description": "Exposed skin compartment.",
        "synonyms": [],
        "recommended_id": "Skin_e",
        "common_ids": [
            "Skin_e"
        ],
        "resources": []
    },
    {
        "name": "skin unexposed",
        "element_type": "compartment",
        "description": "Unexposed skin compartment.",
        "synonyms": [],
        "recommended_id": "Skin_u",
        "common_ids": [
            "Skin_u"
        ],
        "resources": []
    },
    {
        "name": "stratum corneum",
        "element_type": "compartment",
        "description": "Stratum corneum compartment.",
        "synonyms": [],
        "recommended_id": "SC",
        "common_ids": [
            "SC",
            "Skin_sc"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/UBERON:0002027"
            }
        ]
    },
    {
        "name": "stratum corneum exposed skin",
        "element_type": "compartment",
        "description": "Stratum corneum of exposed skin compartment.",
        "synonyms": [],
        "recommended_id": "SC_e",
        "common_ids": [
            "SC_e",
            "Skin_sc_e"
        ],
        "resources": [
            {
                "qualifier": "bqmodel:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00469"
            }
        ]
    },
    {
        "name": "stratum corneum unexposed skin",
        "element_type": "compartment",
        "description": "Stratum corneum of unexposed skin compartment.",
        "synonyms": [],
        "recommended_id": "SC_u",
        "common_ids": [
            "SC_u",
            "Skin_sc_u"
        ],
        "resources": [
            {
                "qualifier": "bqmodel:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00468"
            }
        ]
    },
    {
        "name": "urine",
        "element_type": "compartment",
        "description": "Urine compartment.",
        "synonyms": [],
        "recommended_id": "Urine",
        "common_ids": [
            "urine"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/UBERON:0001088"
            }
        ]
    },
    {
        "name": "venous blood",
        "element_type": "compartment",
        "description": "Venous blood compartment.",
        "synonyms": [],
        "recommended_id": "Ven",
        "common_ids": [
            "Ven"
        ],
        "resources": [
            {
                "qualifier": "bqmodel:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00463"
            },
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/UBERON:0013756"
            }
        ]
    },
    {
        "name": "venous blood plasma",
        "element_type": "compartment",
        "description": "Venous blood plasma compartment.",
        "synonyms": [],
        "recommended_id": "Ven_Plas",
        "common_ids": [
            "Ven_Plas"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "obo/NCIT_C132462"
            }
        ]
    },
    {
        "name": "viable epidermis",
        "element_type": "compartment",
        "description": "Viable epidermis compartment.",
        "synonyms": [],
        "recommended_id": "VE",
        "common_ids": [
            "VE",
            "Skin_ve"
        ]
    },
    {
        "name": "viable epidermis exposed",
        "element_type": "compartment",
        "description": "Viable epidermis of exposed skin compartment.",
        "synonyms": [],
        "recommended_id": "VE_u",
        "common_ids": [
            "VE_u",
            "Skin_ve_u"
        ],
        "resources": [
            {
                "qualifier": "bqmodel:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00467"
            }
        ]
    },
    {
        "name": "viable epidermis unexposed",
        "element_type": "compartment",
        "description": "Viable epidermis of unexposed skin compartment.",
        "synonyms": [],
        "recommended_id": "VE_u",
        "common_ids": [
            "VE_u",
            "Skin_ve_u"
        ],
        "resources": [
            {
                "qualifier": "bqmodel:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00466"
            }
        ]
    },
    # Species terms
    {
        "name": "metabolite",
        "element_type": "species",
        "description": "Species is a metabolite.",
        "synonyms": [],
        "common_ids": [
            "metabolite"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://identifiers.org/CHEBI:25212"
            }
        ]
    },
    {
        "name": "simple chemical",
        "element_type": "species",
        "description": "Species is a simple chemical.",
        "synonyms": [],
        "common_ids": [
            "simple chemical"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://identifiers.org/SBO:0000247"
            }
        ]
    },
    # Parameters: main
    {
        "name": "physiological parameter",
        "element_type": "parameter",
        "description": "Pyhisiological parameter.",
        "synonyms": [],
        "common_ids": [
        ],
        "resources": [
            {
                "qualifier": "bqmodel:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00007"
            }
        ]
    },
    {
        "name": "physicochemical parameter",
        "element_type": "parameter",
        "description": "Physicochemical parameter.",
        "synonyms": [],
        "common_ids": [
        ],
        "resources": [
            {
                "qualifier": "bqmodel:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00128"
            }
        ]
    },
    {
        "name": "metabolic parameter",
        "element_type": "parameter",
        "description": "Metabolic parameter.",
        "synonyms": [],
        "common_ids": [
        ],
        "resources": [
            {
                "qualifier": "bqmodel:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00190"
            }
        ]
    },
    # Parameters: physiological
    {
        "name": "body mass",
        "element_type": "parameter",
        "description": "Body mass (or body weight) parameter.",
        "synonyms": [],
        "recommended_id": "BW",
        "common_ids": [
            "BM",
            "BW",
            "body mass",
            "body weight"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00009"
            },
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/NCIT_C81328"
            },
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/CMO_0000012"
            }
        ]
    },
    {
        "name": "body surface area",
        "element_type": "parameter",
        "description": "Body surface area (BSA) parameter.",
        "synonyms": [],
        "recommended_id": "BSA",
        "common_ids": [
            "BSA"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00011"
            },
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/NCIT_C25157"
            }
        ]
    },
    {
        "name": "cardiac blood output",
        "element_type": "parameter",
        "description": "Cardiac blood output as a function of body weight.",
        "synonyms": [],
        "recommended_id": "QCC",
        "common_ids": [
            "QCC"
        ]
    },
    {
        "name": "alveolar ventilation rate",
        "element_type": "parameter",
        "description": "Alveolar ventilation rate.",
        "synonyms": [],
        "recommended_id": "Falv",
        "common_ids": [
            "Falv"
        ]
    },
    {
        "name": "thickness stratum corneum",
        "element_type": "parameter",
        "description": "Thickness stratum corneum.",
        "synonyms": [],
        "recommended_id": "Height_sc",
        "common_ids": [
            "Height_sc"
        ]
    },
    {
        "name": "thickness viable epidermis",
        "element_type": "parameter",
        "description": "Thickness viable epidermis.",
        "synonyms": [],
        "recommended_id": "Height_ve",
        "common_ids": [
            "Height_ve",
            "Height_vs"
        ]
    },
    {
        "name": "tissue density",
        "element_type": "parameter",
        "description": "Density of the tissues.",
        "synonyms": [],
        "recommended_id": "rho",
        "common_ids": [
            "rho"
        ]
    },
    # Parameters: physiological - compartment volumes
    {
        "name": "alveolar volume",
        "element_type": "parameter",
        "description": "Alveolar volume.",
        "synonyms": [],
        "recommended_id": "VAlv",
        "common_ids": [
            "VAlv"
        ]
    },
    {
        "name": "arterial blood plasma volume",
        "element_type": "parameter",
        "description": "Volume of arterial blood plasma.",
        "synonyms": [],
        "recommended_id": "VArt_Plas",
        "common_ids": [
            "VArt_Plas",
            "VArt_Plasma"
        ]
    },
    {
        "name": "fat volume",
        "element_type": "parameter",
        "description": "Volume of adipose tissue or fat compartment.",
        "synonyms": [],
        "recommended_id": "VFat",
        "common_ids": [
            "VFat",
            "VF"
        ]
    },
    {
        "name": "gut volume",
        "element_type": "parameter",
        "description": "Volume of the gut.",
        "synonyms": [],
        "recommended_id": "VGut",
        "common_ids": [
            "VGut",
            "VG"
        ]
    },
    {
        "name": "kidney volume",
        "element_type": "parameter",
        "description": "Volume of kidney compartment.",
        "synonyms": [],
        "recommended_id": "VKidney",
        "common_ids": [
            "VKidney",
            "VK"
        ]
    },
    {
        "name": "liver volume",
        "element_type": "parameter",
        "description": "Volume of liver compartment.",
        "synonyms": [],
        "recommended_id": "VLiver",
        "common_ids": [
            "VLiver",
            "VL"
        ]
    },
    {
        "name": "lung volume",
        "element_type": "parameter",
        "description": "Volume of the lung compartment.",
        "synonyms": [],
        "recommended_id": "VLung",
        "common_ids": [
            "VLung",
            "VLun"
        ]
    },
    {
        "name": "plasma volume",
        "element_type": "parameter",
        "description": "Volume of blood plasma.",
        "synonyms": [],
        "recommended_id": "VPlasma",
        "common_ids": [
            "VPlasma",
            "VPlas"
        ]
    },
    {
        "name": "rest-of-body volume",
        "element_type": "parameter",
        "description": "Volume of rest-of-body compartment.",
        "synonyms": [],
        "recommended_id": "VRest",
        "common_ids": [
            "VRest",
            "VR"
        ]
    },
    {
        "name": "skin volume",
        "element_type": "parameter",
        "description": "Volume of skin.",
        "synonyms": [],
        "recommended_id": "VSkin",
        "common_ids": [
            "VSkin",
            "VSk"
        ]
    },
    {
        "name": "stratum corneum volume",
        "element_type": "parameter",
        "description": "Volume of stratum corneum.",
        "synonyms": [],
        "recommended_id": "VSC",
        "common_ids": [
            "VSC"
        ]
    },
    {
        "name": "venous blood plasma volume",
        "element_type": "parameter",
        "description": "Volume of blood plasma.",
        "synonyms": [],
        "recommended_id": "VVen_Plas",
        "common_ids": [
            "VVen_Plas",
            "VVen_Plasma"
        ]
    },
    {
        "name": "viable epidermis corneum volume",
        "element_type": "parameter",
        "description": "Volume of viable epidermis.",
        "synonyms": [],
        "recommended_id": "VVE",
        "common_ids": [
            "VVE"
        ]
    },
    # Parameters: chemical
    {
        "name": "molar weight",
        "element_type": "parameter",
        "description": "Molecular weight.",
        "synonyms": [],
        "recommended_id": "MW",
        "common_ids": [
            "MW"
        ]
    },
    {
        "name": "logP",
        "element_type": "parameter",
        "description": "logP descriptor.",
        "synonyms": [],
        "recommended_id": "logP",
        "common_ids": [
            "logP"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://semanticscience.org/resource/CHEMINF_000251"
            }
        ]
    },
    # Parameters: chemical - partition coefficients
    {
        "name": "partition coefficient",
        "element_type": "parameter",
        "description": "Partition coefficient.",
        "synonyms": [],
        "common_ids": [
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00167"
            }
        ]
    },
    {
        "name": "partition coefficient fat/plasma",
        "element_type": "parameter",
        "description": "Partition coefficient fat/plasma.",
        "synonyms": [],
        "recommended_id": "PC_Fat_Plas",
        "common_ids": [
            "PF",
            "PC_Fat_Plas",
            "PC_Fat_Plasma"
        ]
    },
    {
        "name": "partition coefficient gut/plasma",
        "element_type": "parameter",
        "description": "Partition coefficient gut/plasma.",
        "synonyms": [],
        "recommended_id": "PC_Gut_Plas",
        "common_ids": [
            "PG",
            "PC_Gut_Plas",
            "PC_Gut_Plasma"
        ]
    },
    {
        "name": "partition coefficient kidney/plasma",
        "element_type": "parameter",
        "description": "Partition coefficient kidney/plasma.",
        "synonyms": [],
        "recommended_id": "PC_Kid_Plas",
        "common_ids": [
            "PK",
            "PC_Kid_Plas",
            "PC_Kidney_Plasma"
        ]
    },
    {
        "name": "partition coefficient liver/plasma",
        "element_type": "parameter",
        "description": "Partition coefficient liver/plasma.",
        "synonyms": [],
        "recommended_id": "PC_Liv_Plas",
        "common_ids": [
            "PL",
            "PC_Liv_Plas",
            "PC_Liver_Plasma"
        ]
    },
    {
        "name": "partition coefficient lung/plasma",
        "element_type": "parameter",
        "description": "Partition coefficient lung/plasma.",
        "synonyms": [],
        "recommended_id": "PC_Lun_Plas",
        "common_ids": [
            "PLun",
            "PC_Lun_Plas",
            "PC_Lun_Plasma"
        ]
    },
    {
        "name": "partition coefficient rest-of-body/plasma",
        "element_type": "parameter",
        "description": "Partition coefficient rest-of-body/plasma.",
        "synonyms": [],
        "recommended_id": "PC_Rest_Plas",
        "common_ids": [
            "PR",
            "PC_Rest_Plas",
            "PC_Rest_Plasma"
        ]
    },
    {
        "name": "partition coefficient skin/plasma",
        "element_type": "parameter",
        "description": "Partition coefficient skin/plasma.",
        "synonyms": [],
        "recommended_id": "PC_Skin_Plas",
        "common_ids": [
            "PSk",
            "PC_Skin_Plas",
            "PC_Skin_Plasma"
        ]
    },
    # Chemical - other
    {
        "name": "hepatic clearance rate",
        "element_type": "parameter",
        "description": "Hepatic (or metabolic) clearnace rate.",
        "synonyms": [],
        "recommended_id": "CLH",
        "common_ids": [
            "CLH"
        ],
        "resources": [
            {
                "qualifier": "bqbiol:is",
                "URI": "http://purl.obolibrary.org/obo/OMIT_0009720"
            }
        ]
    },
    {
        "name": "unbound fraction in blood",
        "element_type": "parameter",
        "description": "Unbound fraction in blood.",
        "synonyms": [],
        "recommended_id": "fub",
        "common_ids": [
            "fub"
        ],
        "resources": []
    },
    {
        "name": "oral absorption rate constant",
        "element_type": "parameter",
        "description": "Oral 1st order absorption rate constant.",
        "synonyms": [],
        "recommended_id": "kGut",
        "common_ids": [
            "kGut"
        ],
        "resources": []
    }
]
