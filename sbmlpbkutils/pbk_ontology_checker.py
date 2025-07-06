import gzip
import shutil
import time
import urllib.request
from pathlib import Path

from owlready2 import World, onto_path

ONTOLOGY_CACHE_DIR = "./.cache"
PBPKO = {
    "url": "https://raw.githubusercontent.com/InSilicoVida-Research-Lab/pbpko/refs/heads/develop/Robot/ontologies/pbpko.owl",
    "filename": "pbpko.owl"
}
CHEBI = {
    "url": "https://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi_lite.owl.gz",
    "filename": "chebi_lite.owl.gz"
}
NCBITAXON = {
    "url": "https://purl.obolibrary.org/obo/ncbitaxon/subsets/taxslim.owl",
    "filename": "taxslim.owl"
}

onto_path.append(ONTOLOGY_CACHE_DIR)
ncbitaxon = World()
pbpko = World()
chebi = World()

class PbkOntologyChecker():

    pbpko_namespaces = [{
        "pattern": "obo:",
        "replacement": "http://purl.obolibrary.org/obo/"
    }]

    ncbitaxon_namespaces = [
        {
            "pattern": "http://identifiers.org/taxonomy/",
            "replacement": "http://purl.obolibrary.org/obo/NCBITaxon_"
        },
        {
            "pattern": "urn:miriam:taxonomy:",
            "replacement": "http://purl.obolibrary.org/obo/NCBITaxon_"
        },
        {
            "pattern": "obo:",
            "replacement": "http://purl.obolibrary.org/obo/"
        }
    ]

    chebi_namespaces = [
        {
            "pattern": "http://identifiers.org/chebi/CHEBI:",
            "replacement": "http://purl.obolibrary.org/obo/CHEBI_"
        },
        {
            "pattern": "http://identifiers.org/CHEBI:",
            "replacement": "http://purl.obolibrary.org/obo/CHEBI_"
        },
        {
            "pattern": "http://identifiers.org/chebi/",
            "replacement": "http://purl.obolibrary.org/obo/CHEBI_"
        },
        {
            "pattern": "urn:miriam:chebi:",
            "replacement": "http://purl.obolibrary.org/obo/CHEBI_"
        },
        {
            "pattern": "obo:",
            "replacement": "http://purl.obolibrary.org/obo/"
        }
    ]

    def __init__(self) -> None:
        self.pbpko = pbpko
        load_ontology(pbpko, PBPKO)
        self.pbpko_obo = self.pbpko.get_namespace("http://purl.obolibrary.org/obo/")
        self.ncbitaxon = ncbitaxon
        load_ontology(ncbitaxon, NCBITAXON)
        self.ncbitaxon_obo = self.ncbitaxon.get_namespace("http://purl.obolibrary.org/obo/")
        self.chebi = chebi
        load_ontology(chebi, CHEBI)
        self.chebi_obo = self.chebi.get_namespace("http://purl.obolibrary.org/obo/")
        time.sleep(0.0001)

    def check_in_pbpko(self, iri: str):
        return self._check_iri_in_ontology(iri, self.pbpko, self.pbpko_namespaces)

    def check_in_ncbitaxon(self, iri: str):
        return self._check_iri_in_ontology(iri, self.ncbitaxon, self.ncbitaxon_namespaces)

    def check_in_chebi(self, iri: str):
        return self._check_iri_in_ontology(iri, self.chebi, self.chebi_namespaces)

    def get_pbpko_class(self, iri):
        return self._get_class(iri, self.pbpko, self.pbpko_namespaces)

    def get_ncbitaxon_class(self, iri):
        return self._get_class(iri, self.ncbitaxon, self.ncbitaxon_namespaces)

    def get_chebi_class(self, iri):
        return self._get_class(iri, self.chebi, self.chebi_namespaces)

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
        '''Checks whether the specified IRI refers to a NCBI taxon (NCBITaxon_40674) or a descendant
        of it.'''
        element = self._get_class(iri, self.ncbitaxon, self.ncbitaxon_namespaces)
        return element is not None and self.ncbitaxon_obo.NCBITaxon_40674 in element.ancestors()

    def check_is_chemical(self, iri: str):
        '''Checks whether the specified IRI refers to a ChEBI chemical entity (CHEBI_24431), a
        descendant of a chemical entity (CHEBI_50906) or a descendant of a role (CHEBI_24431).'''
        element = self._get_class(iri, self.chebi, self.chebi_namespaces)
        return element is not None and (element is self.chebi_obo.CHEBI_24431 \
            or self.chebi_obo.CHEBI_50906 in element.ancestors()
            or self.chebi_obo.CHEBI_24431 in element.ancestors())

    def check_is_compartment(self, iri: str):
        '''Checks whether the specified IRI refers to a PBPKO compartment (PBPKO_00446) or a
        descendant of it.'''
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
                modified_iri = iri.replace(onto_namespace['pattern'], onto_namespace['replacement'])
                result = onto.search_one(iri = modified_iri)
                if result is not None:
                    break
        return result

def load_ontology(world: World, onto_spec):
    cache_dir = Path(ONTOLOGY_CACHE_DIR)
    url = onto_spec["url"]
    filename = onto_spec["filename"]
    is_gzip = filename.endswith(".gz")
    file_path = cache_dir / filename
    owl_filename = filename[:-3] if is_gzip else filename
    owl_path = cache_dir / owl_filename

    # If .owl file not exists
    if not owl_path.exists():
        # Create cache dir if not exists
        cache_dir.mkdir(parents=True, exist_ok=True)

        # Download file if not exists
        if not file_path.exists():
            urllib.request.urlretrieve(url, file_path)

        # Extract .owl file from .gz file
        if is_gzip:
            with gzip.open(file_path, 'rb') as f_in, open(owl_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Raise error if .owl file still not exists
        if not owl_path.exists():
            raise FileNotFoundError(f"Failed to load OWL file [{owl_filename}].")

    # Load with owlready2
    world.get_ontology(owl_filename).load()
