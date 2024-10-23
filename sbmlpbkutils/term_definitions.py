TermDefinitions = [
    {
        "name": "mus sp.",
        "element_type": "model",
        "description": "",
        "synonyms": [
            "mice"
        ],
        "resources": [
            {
                "qualifier": "BQB_HAS_TAXON",
                "URI": "https://identifiers.org/taxonomy/10095"
            }
        ]
    },
    {
        "name": "homo sapiens",
        "element_type": "model",
        "description": "",
        "synonyms": [
            "human"
        ],
        "resources": [
            {
                "qualifier": "BQB_HAS_TAXON",
                "URI": "https://identifiers.org/taxonomy/9606"
            }
        ]
    },
    {
        "name": "mammalia",
        "element_type": "model",
        "description": "",
        "synonyms": [
            "mammals"
        ],
        "resources": [
            {
                "qualifier": "BQB_HAS_TAXON",
                "URI": "https://identifiers.org/taxonomy/40674"
            }
        ]
    },
    {
        "name": "physiologically based pharmacokinetic model",
        "element_type": "model",
        "description": "",
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://identifiers.org/mamo/MAMO_0000203"
            }
        ]
    },
    {
        "name": "ordinary differential equation model",
        "element_type": "model",
        "description": "",
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://identifiers.org/mamo/MAMO_0000046"
            }
        ]
    },
    {
        "name": "perfusion limited PBK model",
        "element_type": "model",
        "description": "",
        "resources": []
    },
    {
        "name": "permeability limited PBK model",
        "element_type": "model",
        "description": "",
        "resources": []
    },
    {
        "name": "hybrid perfusion limited/permeability PBK model (transfer model?)",
        "element_type": "model",
        "description": "",
        "resources": []
    },
    {
        "name": "lifetime model",
        "element_type": "model",
        "description": "",
        "resources": []
    },
    {
        "name": "adipose tissue compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing adipose tissue (or fat).",
        "synonyms": [
            "fat tissue"
        ],
        "common_ids": [
            "Adipose"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00460"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0001013"
            }
        ]
    },
    {
        "name": "administrative compartment",
        "element_type": "compartment",
        "description": "PBK model compartment not related to a physical entity but introduced for administrative purposes (e.g., mass balance).",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00457"
            }
        ]
    },
    {
        "name": "alveolar air compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing alveolar air (i.e., air in the lungs).",
        "synonyms": [
            "air in the lungs"
        ],
        "common_ids": [
            "Air"
        ],
        "exposure_route": "inhalation",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00458"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/NCIT_C150891"
            }
        ]
    },
    {
        "name": "arterial blood compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing arterial blood.",
        "common_ids": [
            "Art"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00462"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0013755"
            }
        ]
    },
    {
        "name": "arterial blood plasma",
        "element_type": "compartment",
        "description": "PBK model compartment representing blood plasma.",
        "common_ids": [
            "Art_Plasma"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00451"
            }
        ]
    },
    {
        "name": "bladder compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the bladder (used e.g., as a urine delay compartment).",
        "common_ids": [
            "Bladder"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00402"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0004228"
            }
        ]
    },
    {
        "name": "blood compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing blood (whole blood).",
        "common_ids": [
            "Blood"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00464"
            }
        ]
    },
    {
        "name": "blood plasma compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing blood plasma.",
        "common_ids": [
            "Plasma"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00488"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0001969"
            }
        ]
    },
    {
        "name": "brain compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing brain tissue.",
        "common_ids": [
            "Brain"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00466"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0000955"
            }
        ]
    },
    {
        "name": "digestive tract compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the digestive tract.",
        "synonyms": [
            "digestive tract"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0001555"
            }
        ]
    },
    {
        "name": "digestive system compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the digestive system.",
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0001007"
            }
        ]
    },
    {
        "name": "excreta compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing excreta (e.g., urine and feces). ",
        "synonyms": [
            "excretion"
        ],
        "common_ids": [
            "Excretion"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0000174"
            }
        ]
    },
    {
        "name": "feces compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing feces.",
        "common_ids": [
            "Feces"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0001988"
            }
        ]
    },
    {
        "name": "filtrate compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the filtrate.",
        "common_ids": [
            "Filtrate"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00397"
            }
        ]
    },
    {
        "name": "gut compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the gut.",
        "common_ids": [
            "Gut"
        ],
        "exposure_route": "oral",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00477"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0001555"
            }
        ]
    },
    {
        "name": "gut lumen compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the lumen of digestive tract.",
        "common_ids": [
            "Lumen"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00478"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0006909"
            }
        ]
    },
    {
        "name": "gonads compaterment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the gonads.",
        "common_ids": [
            "Gonads"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0000991"
            }
        ]
    },
    {
        "name": "heart compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the heart.",
        "common_ids": [
            "Heart"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00480"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0000948"
            }
        ]
    },
    {
        "name": "intestine compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the intestine.",
        "common_ids": [
            "Intestine"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0000160"
            }
        ]
    },
    {
        "name": "kidney compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the kidney.",
        "common_ids": [
            "Kidney"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0002113"
            }
        ]
    },
    {
        "name": "liver compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the liver.",
        "common_ids": [
            "Liver"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0002107 "
            }
        ]
    },
    {
        "name": "lung compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the lung.",
        "common_ids": [
            "Lung"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0002048"
            }
        ]
    },
    {
        "name": "poorly perfused tissue compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the poorly perfused tissue.",
        "common_ids": [
            "Poor"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00454"
            }
        ]
    },
    {
        "name": "systemic exposure compartment",
        "element_type": "compartment",
        "description": "Administrative PBK model compartment representing systemic exposure (aggregated from multiple routes).",
        "common_ids": [
            "Systemic"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00459"
            }
        ]
    },
    {
        "name": "rest-of-body compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the rest of the body (periphery).",
        "synonyms": [
            "rest-of-body",
            "periphery"
        ],
        "common_ids": [
            "Rest"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00450"
            }
        ]
    },
    {
        "name": "richly perfused tissue compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing richly perfused tissue.",
        "common_ids": [
            "Rich"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00453"
            }
        ]
    },
    {
        "name": "skin compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the skin.",
        "common_ids": [
            "Skin"
        ],
        "exposure_route": "dermal",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00470"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0002097"
            }
        ]
    },
    {
        "name": "spleen compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the spleen.",
        "common_ids": [
            "Spleen"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00492"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0002106"
            }
        ]
    },
    {
        "name": "stomach compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the stomach.",
        "common_ids": [
            "Stomach"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0000945"
            }
        ]
    },
    {
        "name": "stratum corneum unexposed skin compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the stratum corneum (the outermost layer of the epidermis) of unexposed skin.",
        "common_ids": [
            "Skin_SC_u"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00457"
            }
        ]
    },
    {
        "name": "stratum corneum exposed skin compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the stratum corneum (the outermost layer of the epidermis) of exposed skin.",
        "common_ids": [
            "Skin_SC_e"
        ],
        "exposure_route": "dermal",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00458"
            }
        ]
    },
    {
        "name": "stratum corneum compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the stratum corneum (the outermost layer of the epidermis).",
        "synonyms": [
            "outer layer of the skin"
        ],
        "common_ids": [
            "Skin_SC"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0002027"
            }
        ]
    },
    {
        "name": "urine compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing urine.",
        "common_ids": [
            "Urine"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0001088"
            }
        ]
    },
    {
        "name": "uterus compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the uterus.",
        "common_ids": [
            "Uterus"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0000995"
            }
        ]
    },
    {
        "name": "venous blood compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing venous blood.",
        "common_ids": [
            "Ven"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00452"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/UBERON_0013756"
            }
        ]
    },
    {
        "name": "venous blood plasma compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing venous blood plasma.",
        "common_ids": [
            "Ven_Plasma"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00463"
            }
        ]
    },
    {
        "name": "viable epidermis compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the viable epidermis.",
        "common_ids": [
            "Skin_VE"
        ],
        "resources": []
    },
    {
        "name": "viable epidermis exposed skin compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the viable epidermis of exposed skin.",
        "common_ids": [
            "Skin_VE_e"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00467"
            }
        ]
    },
    {
        "name": "viable epidermis unexposed skin compartment",
        "element_type": "compartment",
        "description": "PBK model compartment representing the viable epidermis of unexposed skin.",
        "common_ids": [
            "Skin_VE_u"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00466"
            }
        ]
    },
    {
        "name": "amount of chemical in adipose tissue",
        "element_type": "species",
        "description": "The amount of a chemical substance in adipose tissue (fat).",
        "resources": []
    },
    {
        "name": "amount of chemical in arterial blood",
        "element_type": "species",
        "description": "The amount of a chemical substance in arterial blood.",
        "resources": []
    },
    {
        "name": "amount of chemical in blood",
        "element_type": "species",
        "description": "The amount of a chemical substance in blood.",
        "common_ids": [
            "ABlood"
        ],
        "resources": []
    },
    {
        "name": "amount of chemical in gut",
        "element_type": "species",
        "description": "The amount of a chemical substance in the gut.",
        "resources": []
    },
    {
        "name": "amount of chemical in kidney",
        "element_type": "species",
        "description": "The amount of a chemical substance in the kidney.",
        "resources": []
    },
    {
        "name": "amount of chemical in liver",
        "element_type": "species",
        "description": "The amount of a chemical substance in the liver.",
        "resources": []
    },
    {
        "name": "amount of chemical in plasma",
        "element_type": "species",
        "description": "The amount of a chemical substance in plasma.",
        "resources": []
    },
    {
        "name": "amount of chemical in poorly perfused tissue",
        "element_type": "species",
        "description": "The amount of a chemical substance in poorly perfused tissue.",
        "resources": []
    },
    {
        "name": "amount of chemical in rest-of-body",
        "element_type": "species",
        "description": "The amount of a chemical substance in the rest-of-body",
        "resources": []
    },
    {
        "name": "amount of chemical in richly perfused tissue",
        "element_type": "species",
        "description": "The amount of a chemical substance in richly perfused tissue.",
        "resources": []
    },
    {
        "name": "amount of chemical in skin",
        "element_type": "species",
        "description": "The amount of a chemical substance in skin tissue.",
        "resources": []
    },
    {
        "name": "amount of chemical in urine",
        "element_type": "species",
        "description": "The amount of a chemical substance in urine.",
        "resources": []
    },
    {
        "name": "amount of chemical in venous blood",
        "element_type": "species",
        "description": "The amount of a chemical substance in venous blood.",
        "common_ids": [
            "AVen"
        ],
        "resources": []
    },
    {
        "name": "physiological parameter",
        "element_type": "parameter",
        "description": "",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PKPBO_00003"
            }
        ]
    },
    {
        "name": "age",
        "element_type": "parameter",
        "description": "PBK model parameter representing the (initial) age of the modelled entity.",
        "synonyms": [
            "age"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/ExO_0000102"
            }
        ]
    },
    {
        "name": "body weight",
        "element_type": "parameter",
        "description": "PBK model parameter representing the (initial) body weight of the modelled entity.",
        "synonyms": [
            "body mass"
        ],
        "common_ids": [
            "BW",
            "BM"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00009"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/NCIT_C81328"
            }
        ]
    },
    {
        "name": "body surface area",
        "element_type": "parameter",
        "description": "PBK model parameter representing the (initial) body surface area of the modelled entity.",
        "common_ids": [
            "BSA"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/NCIT_C25157"
            }
        ]
    },
    {
        "name": "sex",
        "element_type": "parameter",
        "description": "PBK model parameter representing the (initial) sex of the modelled entity.",
        "common_ids": [
            "Sex"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00123"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/NCIT_C43816"
            }
        ]
    },
    {
        "name": "absorption rate constant gut",
        "element_type": "parameter",
        "description": "",
        "synonyms": [
            "oral absorption rate"
        ],
        "common_ids": [
            "kGut"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PKPBO_00126"
            }
        ]
    },
    {
        "name": "creatinine excretion rate",
        "element_type": "parameter",
        "description": "",
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/NCIT_C150817"
            }
        ]
    },
    {
        "name": "excretion rate",
        "element_type": "parameter",
        "description": "",
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/NCIT_C85534"
            }
        ]
    },
    {
        "name": "urinary excretion rate",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "hepatic clearance rate",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "CLH"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PKPBO_00215"
            }
        ]
    },
    {
        "name": "renal elimination rate constant",
        "element_type": "parameter",
        "description": "",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PKPBO_00218"
            }
        ]
    },
    {
        "name": "alveolar ventilation rate",
        "element_type": "parameter",
        "description": "",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00114"
            }
        ]
    },
    {
        "name": "blood flow rate",
        "element_type": "parameter",
        "description": "Total blood flow.",
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/NCIT_C94866"
            }
        ]
    },
    {
        "name": "blood flow going to physiological compartment",
        "element_type": "parameter",
        "description": "Blood flow going to a physiological compartment.",
        "resources": []
    },
    {
        "name": "blood flow going to adipose tissue",
        "element_type": "parameter",
        "description": "",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00032"
            }
        ]
    },
    {
        "name": "blood flow going to liver",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "blood flow going to the kidney",
        "element_type": "parameter",
        "description": "",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00026"
            }
        ]
    },
    {
        "name": "blood flow going to poorly perfused tissue",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "blood flow going to rest-of-body",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "blood flow going to richly perfused tissue",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "blood flow going to skin",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "blood flow going to exposed skin",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "blood flow going to unexposed skin",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "fraction of total blood flow going to physiological compartment",
        "element_type": "parameter",
        "description": "Fraction of the total blood flow going to a physiological compartment.",
        "resources": []
    },
    {
        "name": "fraction of total blood flow going to adipose tissue",
        "element_type": "parameter",
        "description": "Fraction of the total blood flow going to the adipose tissue (fat).",
        "resources": []
    },
    {
        "name": "fraction of total blood flow going to liver",
        "element_type": "parameter",
        "description": "Fraction of the total blood flow going to the liver.",
        "resources": []
    },
    {
        "name": "fraction of total blood flow going to poorly perfused tissue",
        "element_type": "parameter",
        "description": "Fraction of the total blood flow going to poorly perfused tissue.",
        "resources": []
    },
    {
        "name": "fraction of total blood flow going to rest-of-body",
        "element_type": "parameter",
        "description": "Fraction of the total blood flow going to the rest-of-body.",
        "resources": []
    },
    {
        "name": "fraction of total blood flow going to richly perfused tissue",
        "element_type": "parameter",
        "description": "Fraction of the total blood flow going to richly perfused tissue.",
        "resources": []
    },
    {
        "name": "fraction of total blood flow going to skin",
        "element_type": "parameter",
        "description": "Fraction of the total blood flow going to the skin.",
        "resources": []
    },
    {
        "name": "fraction of total blood flow going to exposed skin",
        "element_type": "parameter",
        "description": "Fraction of the total blood flow going to the exposed skin.",
        "resources": []
    },
    {
        "name": "fraction of total blood flow going to unexposed skin",
        "element_type": "parameter",
        "description": "Fraction of the total blood flow going to the unexposed skin.",
        "resources": []
    },
    {
        "name": "ratio blood to total body mass",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "ratio blood to total body volume",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "ratio gut to total body mass",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "ratio gut to total body volume",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "ratio fat to total body mass",
        "element_type": "parameter",
        "description": "",
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/CMO_0003945"
            }
        ]
    },
    {
        "name": "ratio fat to total body volume",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "ratio kidney to total body mass",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "ratio kidney to total body volume",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "ratio liver to total body mass",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "ratio liver to total body volume",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "ratio plasma to total body mass",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "ratio plasma to total body volume",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "ratio rest-of-body to total body mass",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "ratio rest-of-body to total body volume",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "tissue density",
        "element_type": "parameter",
        "description": "Density of tissue expressed as a ratio mass over volume.",
        "resources": []
    },
    {
        "name": "skin thickness",
        "element_type": "parameter",
        "description": "Thickness of the skin in metres (SI base unit metres).",
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/OBA_VT0001200"
            }
        ]
    },
    {
        "name": "thickness stratum corneum",
        "element_type": "parameter",
        "description": "Thickness of the stratum corneum (SI base unit metres).",
        "resources": []
    },
    {
        "name": "thickness viable epidermis",
        "element_type": "parameter",
        "description": "Thickness of the viable epidermis (SI base unit metres).",
        "resources": []
    },
    {
        "name": "compartment volume",
        "element_type": "parameter",
        "description": "Total volume of a physiological compartment (specified in litres or cubic metres).",
        "resources": []
    },
    {
        "name": "volume adipose tissue",
        "element_type": "parameter",
        "description": "Total volume of adipose tissue (specified in litres or cubic metres).",
        "common_ids": [
            "V_Fat"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00085"
            }
        ]
    },
    {
        "name": "volume arterial blood",
        "element_type": "parameter",
        "description": "Total volume of the arterial blood (specified in litres or cubic metres).",
        "resources": []
    },
    {
        "name": "volume arterial blood plasma",
        "element_type": "parameter",
        "description": "Total volume of the arterial blood plasma (specified in litres or cubic metres).",
        "resources": []
    },
    {
        "name": "volume of bone",
        "element_type": "parameter",
        "description": "Total volume of the bone (specified in litres or cubic metres).",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00091"
            }
        ]
    },
    {
        "name": "volume blood",
        "element_type": "parameter",
        "description": "Total volume of the blood (specified in litres or cubic metres).",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00108"
            }
        ]
    },
    {
        "name": "volume blood plasma",
        "element_type": "parameter",
        "description": "Total volume of the blood plasma (specified in litres or cubic metres).",
        "resources": []
    },
    {
        "name": "volume gut",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "volume liver",
        "element_type": "parameter",
        "description": "Total volume of the liver (specified in litres or cubic metres).",
        "common_ids": [
            "V_Liver"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PKPBO_00069"
            }
        ]
    },
    {
        "name": "volume poorly perfused tissue",
        "element_type": "parameter",
        "description": "Total volume of the poorly perfused tissue (specified in litres or cubic metres).",
        "common_ids": [
            "V_Poor"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PKPBO_00091"
            }
        ]
    },
    {
        "name": "volume richly perfused tissue",
        "element_type": "parameter",
        "description": "Total volume of the richly perfused tissue (specified in litres or cubic metres).",
        "common_ids": [
            "V_Rich"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PKPBO_00093"
            }
        ]
    },
    {
        "name": "volume skin",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "volume skin exposed",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "volume skin unexposed",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "volume stratum corneum",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "volume stratum corneum exposed",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "volume stratum corneum unexposed",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "volume venous blood",
        "element_type": "parameter",
        "description": "",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00122"
            }
        ]
    },
    {
        "name": "volume venous blood plasma",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "volume viable epidermis",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "volume viable epidermis exposed",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "volume viable epidermis unexposed",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "physicochemical parameter",
        "element_type": "parameter",
        "description": "",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00126"
            }
        ]
    },
    {
        "name": "diffusion coefficient",
        "element_type": "parameter",
        "description": "",
        "synonyms": [
            "diffusion rate"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00431"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://biomodels.net/SBO/SBO_0000491"
            }
        ]
    },
    {
        "name": "fraction unbound in blood",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "fub"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PKPBO_00134"
            }
        ]
    },
    {
        "name": "partition coefficient",
        "element_type": "parameter",
        "description": "The ratio of the concentration of a drug/chemical in a particular tissue to its concentration in plasma at equilibrium.",
        "synonyms": [
            "partition coefficient"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00165"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/NCIT_C20610"
            }
        ]
    },
    {
        "name": "partition coefficient adipose tissue over blood",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Fat_Plasma"
        ],
        "resources": []
    },
    {
        "name": "partition coefficient adipose tissue over plasma",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Fat_Plasma"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00174"
            }
        ]
    },
    {
        "name": "partition coefficient blood over air",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Blood_Air"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00183"
            }
        ]
    },
    {
        "name": "partition coefficient muscle over blood (poorly perfused tissue)",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "partition coefficient viscera over blood (richly perfused tissue)",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "partition coefficient liver over blood",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Liver_Blood"
        ],
        "resources": []
    },
    {
        "name": "partition coefficient viable skin over blood",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Skin_Blood"
        ],
        "resources": []
    },
    {
        "name": "partition coefficient viable skin over stratum corneum",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Skin_Sc"
        ],
        "resources": []
    },
    {
        "name": "partition coefficient liver over blood",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Liver_Plasma"
        ],
        "resources": []
    },
    {
        "name": "partition coefficient liver over plasma",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Liver_Plasma"
        ],
        "resources": []
    },
    {
        "name": "partition coefficient kidney over blood",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Kidney_Plasma"
        ],
        "resources": []
    },
    {
        "name": "partition coefficient kidney over plasma",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Kidney_Plasma"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00171"
            }
        ]
    },
    {
        "name": "partition coefficient poorly perfused tissue over blood",
        "element_type": "parameter",
        "description": "",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00181"
            }
        ]
    },
    {
        "name": "partition coefficient poorly perfused tissue over plasma",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "partition coefficient skin over blood",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Skin_Plasma"
        ],
        "resources": []
    },
    {
        "name": "partition coefficient skin over plasma",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Skin_Plasma"
        ],
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00176"
            }
        ]
    },
    {
        "name": "partition coefficient rest-of-body over blood",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Rest_Plasma"
        ],
        "resources": []
    },
    {
        "name": "partition coefficient rest-of-body over plasma",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Rest_Plasma"
        ],
        "resources": []
    },
    {
        "name": "partition coefficient richly perfused tissue over blood",
        "element_type": "parameter",
        "description": "",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00180"
            }
        ]
    },
    {
        "name": "partition coefficient richly perfused tissue over plasma",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "partition coefficient stratum corneum over blood",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "partition coefficient stratum corneum over plasma",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "partition coefficient viable epidermis over blood",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "partition coefficient viable epidermis over plasma",
        "element_type": "parameter",
        "description": "",
        "resources": []
    },
    {
        "name": "particion coefficient gut over plasma",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Gut_Blood"
        ],
        "resources": []
    },
    {
        "name": "partition coefficient lung over plasma",
        "element_type": "parameter",
        "description": "",
        "common_ids": [
            "PC_Lung_Plasma"
        ],
        "resources": []
    },
    {
        "name": "maximal velocity",
        "element_type": "parameter",
        "description": "",
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://biomodels.net/SBO/SBO_0000186"
            }
        ]
    },
    {
        "name": "biochemical parameter",
        "element_type": "parameter",
        "description": "Biochemical parameters refer to the various chemical and biological measurements that can be analyzed in bodily fluids, such as blood, urine, or cerebrospinal fluid",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00139"
            }
        ]
    },
    {
        "name": "PBK model parameter",
        "element_type": "parameter",
        "description": "Different types of parameters involved in PBK modelling.",
        "resources": [
            {
                "qualifier": "BQM_IS",
                "URI": "http://purl.obolibrary.org/obo/PBPKO_00002"
            },
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/STATO_0000034"
            }
        ]
    },
    {
        "name": "hematocrit",
        "element_type": "parameter",
        "description": "Percentage (or fraction) of total blood volume that is made up of red blood cells.",
        "common_ids": [
            "Htc"
        ],
        "resources": [
            {
                "qualifier": "BQB_IS",
                "URI": "http://purl.obolibrary.org/obo/CMO_0000037"
            }
        ]
    }
]
