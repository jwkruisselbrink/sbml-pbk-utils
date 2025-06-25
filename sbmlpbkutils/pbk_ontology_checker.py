from owlready2 import *

onto_path.append("./.cache")
pbpko_path = "https://raw.githubusercontent.com/InSilicoVida-Research-Lab/pbpko/refs/heads/develop/Robot/ontologies/pbpko.owl"
ncbitaxon_path = "https://purl.obolibrary.org/obo/ncbitaxon/subsets/taxslim.owl"
ncbitaxon = World()
pbpko = World()

class PbkOntologyChecker():

    ncbitaxon_namespaces = [
        {
            "prefix": "obo",
            "separator": ":",
            "url": "http://purl.obolibrary.org/obo/"
        },
        {
            "prefix": "urn:miriam:taxonomy",
            "separator": ":",
            "url": "http://purl.obolibrary.org/obo/NCBITaxon_"
        },
        {
            "prefix": "http://identifiers.org/taxonomy",
            "separator": "/",
            "url": "http://purl.obolibrary.org/obo/NCBITaxon_"
        }
    ]

    pbpko_namespaces = [{
        "prefix": "obo",
        "separator": ":",
        "url": "http://purl.obolibrary.org/obo/"
    }]

    def __init__(self) -> None:
        self.pbpko = pbpko
        self.pbpko.get_ontology(pbpko_path).load()
        self.ncbitaxon = ncbitaxon
        self.ncbitaxon.get_ontology(ncbitaxon_path).load()
        self.ncbitaxon_obo = self.ncbitaxon.get_namespace("http://purl.obolibrary.org/obo/")
        self.pbpko_obo = self.pbpko.get_namespace("http://purl.obolibrary.org/obo/")
        time.sleep(0.0001)

    def check_in_pbpko(self, iri: str):
        return self._check_iri_in_ontology(iri, self.pbpko, self.pbpko_namespaces)

    def check_in_ncbitaxon(self, iri: str):
        return self._check_iri_in_ontology(iri, self.ncbitaxon, self.ncbitaxon_namespaces)

    def get_pbpko_class(self, iri):
        return self._get_class(iri, self.pbpko, self.pbpko_namespaces)

    def get_ncbitaxon_class(self, iri):
        return self._get_class(iri, self.ncbitaxon, self.ncbitaxon_namespaces)

    def check_in_chebi(self, iri: str):
        # Regex for short namespace + ChEBI ID
        short_iri_pattern = r"^obo:CHEBI_\d+$"
        # Full regex for namespace + ChEBI ID
        full_iri_pattern = r"^http://purl.obolibrary.org/obo/CHEBI_\d+$"
        return bool(re.match(short_iri_pattern, iri)) \
            or bool(re.match(full_iri_pattern, iri))

    def get_available_classes(self, element_type: str):
        if element_type == 'taxon':
            return self.get_mammal_taxon_classes()
        if element_type == 'compartment':
            return self.get_compartment_classes()
        if element_type == 'parameter':
            return self.get_parameter_classes()
        if element_type == 'species':
            return self.get_species_classes()

    def get_mammal_taxon_classes(self):
        return list(self.ncbitaxon_obo.NCBITaxon_40674.descendants())

    def get_compartment_classes(self):
        return list(self.pbpko_obo.PBPKO_00446.descendants())

    def get_species_classes(self):
        return list(self.pbpko_obo.PBPKO_00252.descendants())

    def get_parameter_classes(self):
        return list(self.pbpko_obo.PBPKO_00002.descendants())

    def check_is_animal_species(self, iri: str):
        element = self._get_class(iri, self.ncbitaxon, self.ncbitaxon_namespaces)
        return element is not None and self.ncbitaxon_obo.NCBITaxon_40674 in element.ancestors()

    def check_is_compartment(self, iri: str):
        pbpko_class = self._get_class(iri, self.pbpko, self.pbpko_namespaces)
        return pbpko_class is not None and self.pbpko_obo.PBPKO_00446 in pbpko_class.ancestors()

    def check_is_input_compartment(self, iri: str):
        return self.check_is_oral_input_compartment(iri) \
            or self.check_is_dermal_input_compartment(iri) \
            or self.check_is_inhalation_input_compartment(iri)

    def check_is_oral_input_compartment(self, iri: str):
        pbpko_class = self._get_class(iri, self.pbpko, self.pbpko_namespaces)
        return pbpko_class is not None and pbpko_class is self.pbpko_obo.PBPKO_00477

    def check_is_dermal_input_compartment(self, iri: str):
        pbpko_class = self._get_class(iri, self.pbpko, self.pbpko_namespaces)
        return pbpko_class \
            and (pbpko_class is self.pbpko_obo.PBPKO_00470 \
                or pbpko_class is self.pbpko_obo.PBPKO_00458)

    def check_is_inhalation_input_compartment(self, iri: str):
        pbpko_class = self._get_class(iri, self.pbpko, self.pbpko_namespaces)
        # Lung compartment or sub-class of lung compartment (e.g. alveolar air)
        return pbpko_class \
            and (pbpko_class is self.pbpko_obo.PBPKO_00559 \
            or self.pbpko_obo.PBPKO_00559 in pbpko_class.ancestors())

    def check_is_parameter(self, iri: str):
        element = self._get_class(iri, self.pbpko, self.pbpko_namespaces)
        return element is not None and self.pbpko_obo.PBPKO_00002 in element.ancestors()

    def check_is_biochemical_parameter(self, iri: str):
        element = self._get_class(iri, self.pbpko, self.pbpko_namespaces)
        return element is not None and self.pbpko_obo.PBPKO_00139 in element.ancestors()

    def check_is_physicochemical_parameter(self, iri: str):
        element = self._get_class(iri, self.pbpko, self.pbpko_namespaces)
        return element is not None and self.pbpko_obo.PBPKO_00126 in element.ancestors()

    def check_is_chemical_specific_parameter(self, iri: str):
        return self.check_is_biochemical_parameter(iri) \
            or self.check_is_physicochemical_parameter(iri)

    def check_is_physiological_parameter(self, iri: str):
        element = self._get_class(iri, self.pbpko, self.pbpko_namespaces)
        return element is not None and self.pbpko_obo.PBPKO_00006 in element.ancestors()

    def check_is_species(self, iri: str):
        element = self._get_class(iri, self.pbpko, self.pbpko_namespaces)
        return element is not None and self.pbpko_obo.PBPKO_00002 in element.ancestors()

    def _check_iri_in_ontology(self, iri: str, onto, onto_namespaces):
        onto_class = self._get_class(iri, onto, onto_namespaces)
        return onto_class is not None

    def _get_class(self, iri, onto, onto_namespaces):
        # Check in classes, individuals, and properties
        result = onto.search_one(iri = iri) 
        if result is None:
            # If an ontology definition is provided, check the modified IRI
            for onto_namespace in onto_namespaces:
                # Replace the namespace in the IRI
                modified_iri = iri.replace(f'{onto_namespace['prefix']}{onto_namespace['separator']}', onto_namespace['url'])
                result = onto.search_one(iri = modified_iri)
                if result is not None:
                    break
        return result
