import libsbml as ls

QualifierDefinitions = [
    {
        "id": "BQM_IS",
        "qualifier": ls.BQM_IS,
        "type": ls.MODEL_QUALIFIER
    },
    {
        "id": "BQM_IS_DESCRIBED_BY",
        "qualifier": ls.BQM_IS_DESCRIBED_BY,
        "type": ls.MODEL_QUALIFIER
    },
    {
        "id": "BQM_IS_DERIVED_FROM",
        "qualifier": ls.BQM_IS_DERIVED_FROM,
        "type": ls.MODEL_QUALIFIER
    },
    {
        "id": "BQM_IS_INSTANCE_OF",
        "qualifier": ls.BQM_IS_INSTANCE_OF,
        "type": ls.MODEL_QUALIFIER
    },
    {
        "id": "BQM_HAS_INSTANCE",
        "qualifier": ls.BQM_HAS_INSTANCE,
        "type": ls.MODEL_QUALIFIER
    },
    {
        "id": "BQM_UNKNOWN",
        "qualifier": ls.BQM_UNKNOWN,
        "type": ls.MODEL_QUALIFIER
    },
    {
        "id": "BQB_IS",
        "qualifier": ls.BQB_IS,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_HAS_PART",
        "qualifier": ls.BQB_HAS_PART,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_IS_PART_OF",
        "qualifier": ls.BQB_IS_PART_OF,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_IS_VERSION_OF",
        "qualifier": ls.BQB_IS_VERSION_OF,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_HAS_VERSION",
        "qualifier": ls.BQB_HAS_VERSION,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_IS_HOMOLOG_TO",
        "qualifier": ls.BQB_IS_HOMOLOG_TO,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_IS_DESCRIBED_BY",
        "qualifier": ls.BQB_IS_DESCRIBED_BY,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_IS_ENCODED_BY",
        "qualifier": ls.BQB_IS_ENCODED_BY,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_ENCODES",
        "qualifier": ls.BQB_ENCODES,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_OCCURS_IN",
        "qualifier": ls.BQB_OCCURS_IN,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_HAS_PROPERTY",
        "qualifier": ls.BQB_HAS_PROPERTY,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_IS_PROPERTY_OF",
        "qualifier": ls.BQB_IS_PROPERTY_OF,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_HAS_TAXON",
        "qualifier": ls.BQB_HAS_TAXON,
        "type": ls.BIOLOGICAL_QUALIFIER
    },
    {
        "id": "BQB_UNKNOWN",
        "qualifier": ls.BQB_UNKNOWN,
        "type": ls.BIOLOGICAL_QUALIFIER
    }
]

ModelQualifierIdsLookup = {
    ls.BQM_IS : "BQM_IS",
    ls.BQM_IS_DESCRIBED_BY : "BQM_IS_DESCRIBED_BY",
    ls.BQM_IS_DERIVED_FROM : "BQM_IS_DERIVED_FROM",
    ls.BQM_IS_INSTANCE_OF : "BQM_IS_INSTANCE_OF",
    ls.BQM_HAS_INSTANCE : "BQM_HAS_INSTANCE",
    ls.BQM_UNKNOWN : "BQM_UNKNOWN"
}

BiologicalQualifierIdsLookup = {
    ls.BQB_IS : "BQB_IS",
    ls.BQB_HAS_PART : "BQB_HAS_PART",
    ls.BQB_IS_PART_OF : "BQB_IS_PART_OF",
    ls.BQB_IS_VERSION_OF : "BQB_IS_VERSION_OF",
    ls.BQB_HAS_VERSION : "BQB_HAS_VERSION",
    ls.BQB_IS_HOMOLOG_TO : "BQB_IS_HOMOLOG_TO",
    ls.BQB_IS_DESCRIBED_BY : "BQB_IS_DESCRIBED_BY",
    ls.BQB_IS_ENCODED_BY : "BQB_IS_ENCODED_BY",
    ls.BQB_ENCODES : "BQB_ENCODES",
    ls.BQB_OCCURS_IN : "BQB_OCCURS_IN",
    ls.BQB_HAS_PROPERTY : "BQB_HAS_PROPERTY",
    ls.BQB_IS_PROPERTY_OF : "BQB_IS_PROPERTY_OF",
    ls.BQB_HAS_TAXON : "BQB_HAS_TAXON",
    ls.BQB_UNKNOWN : "BQB_UNKNOWN"
}
