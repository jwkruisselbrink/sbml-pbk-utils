from owlready2 import *

pbpko_path = "https://raw.githubusercontent.com/Crispae/pbpko/refs/heads/main/Robot/ontologies/pbpko.owl"

class PbkOntologyChecker():

    pbpko_namespaces = [{
        "key": "obo",
        "separator": ":",
        "url": "http://purl.obolibrary.org/obo/"
    }]

    pbpko_namespaces = [{
        "key": "obo",
        "separator": ":",
        "url": "http://purl.obolibrary.org/obo/"
    }]

    def __init__(self) -> None:
        self.onto = get_ontology(pbpko_path)
        self.onto.load()
        self.obo = get_namespace("http://purl.obolibrary.org/obo/")

    def find_by_label(self, label: str):
        return list(self.onto.search(label = label))

    def check_in_pbpko(self, iri: str):
        return self.check_iri_in_ontology(iri, self.pbpko_namespaces)

    def check_in_chebi(self, iri: str):
        # Regex for short namespace + ChEBI ID
        short_iri_pattern = r"^obo:CHEBI_\d+$"
        # Full regex for namespace + ChEBI ID
        full_iri_pattern = r"^http://purl.obolibrary.org/obo/CHEBI_\d+$"
        return bool(re.match(short_iri_pattern, iri)) \
            or bool(re.match(full_iri_pattern, iri))

    def get_available_classes(self, element_type: str):
        if element_type == 'compartment':
            return self.get_compartment_classes()
        if element_type == 'parameter':
            return self.get_parameter_classes()
        if element_type == 'species':
            return self.get_species_classes()

    def get_parameter_classes(self):
        return list(self.obo.PBPKO_00002.descendants())

    def get_compartment_classes(self):
        return list(self.obo.PBPKO_00446.descendants())

    def get_species_classes(self):
        return list(self.obo.PBPKO_00252.descendants())

    def check_is_compartment(self, iri: str):
        pbpko_class = self.get_class(iri, self.pbpko_namespaces)
        return pbpko_class is not None and self.obo.PBPKO_00446 in pbpko_class.ancestors()

    def check_is_input_compartment(self, iri: str):
        return self.check_is_oral_input_compartment(iri) \
            or self.check_is_dermal_input_compartment(iri) \
            or self.check_is_inhalation_input_compartment(iri)

    def check_is_oral_input_compartment(self, iri: str):
        pbpko_class = self.get_class(iri, self.pbpko_namespaces)
        return pbpko_class is not None and pbpko_class is self.obo.PBPKO_00477

    def check_is_dermal_input_compartment(self, iri: str):
        pbpko_class = self.get_class(iri, self.pbpko_namespaces)
        return pbpko_class \
            and (pbpko_class is self.obo.PBPKO_00470 \
                or pbpko_class is self.obo.PBPKO_00458)

    def check_is_inhalation_input_compartment(self, iri: str):
        pbpko_class = self.get_class(iri, self.pbpko_namespaces)
        return pbpko_class is not None and pbpko_class is self.obo.PBPKO_00448

    def check_is_parameter(self, iri: str):
        element = self.get_class(iri, self.pbpko_namespaces)
        return element is not None and self.obo.PBPKO_00002 in element.ancestors()

    def check_is_biochemical_parameter(self, iri: str):
        element = self.get_class(iri, self.pbpko_namespaces)
        return element is not None and self.obo.PBPKO_00139 in element.ancestors()

    def check_is_physicochemical_parameter(self, iri: str):
        element = self.get_class(iri, self.pbpko_namespaces)
        return element is not None and self.obo.PBPKO_00126 in element.ancestors()

    def check_is_chemical_specific_parameter(self, iri: str):
        return self.check_is_biochemical_parameter(iri) \
            or self.check_is_physicochemical_parameter(iri)

    def check_is_physiological_parameter(self, iri: str):
        element = self.get_class(iri, self.pbpko_namespaces)
        return element is not None and self.obo.PBPKO_00006 in element.ancestors()

    def check_is_species(self, iri: str):
        element = self.get_class(iri, self.pbpko_namespaces)
        return element is not None and self.obo.PBPKO_00002 in element.ancestors()

    def get_class(self, iri, replacement_namespaces=None):
        # Check in classes, individuals, and properties
        result = self.onto.search_one(iri = iri) 
        if result is None:
            # If a replacement namespace is provided, check the modified IRI
            for replacement_namespace in replacement_namespaces:
                # Replace the namespace in the IRI
                modified_iri = iri.replace(f'{replacement_namespace['key']}{replacement_namespace['separator']}', replacement_namespace['url'])
                result = self.onto.search_one(iri = modified_iri)
                if result is not None:
                    break

        return result

    def check_iri_in_ontology(self, iri: str, replacement_namespaces=None):
        return self.get_class(iri, replacement_namespaces) is not None

