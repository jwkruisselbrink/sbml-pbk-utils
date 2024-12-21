from owlready2 import *

pbpko_path = "https://raw.githubusercontent.com/Crispae/pbpko/refs/heads/main/Robot/ontologies/pbpko.owl"

class PbkOntologyChecker():

    pbpko_namespaces = [{
        "key": "obo",
        "separator": ":",
        "url": "http://purl.obolibrary.org/obo/"
    }]

    def __init__(self) -> None:
        self.onto = get_ontology(pbpko_path)
        self.onto.load()
        self.obo = get_namespace("http://purl.obolibrary.org/obo/")

    def find_by_label(self, label):
        return list(self.onto.search(label = label))

    def check_in_pbpko(self, iri):
        return self.check_iri_in_ontology(iri, self.pbpko_namespaces)

    def get_available_classes(self, element_type):
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

    def check_is_compartment(self, iri):
        element = self.get_class(iri, self.pbpko_namespaces)
        return element is not None and self.obo.PBPKO_00446 in element.ancestors()

    def check_is_parameter(self, iri):
        element = self.get_class(iri, self.pbpko_namespaces)
        return element is not None and self.obo.PBPKO_00002 in element.ancestors()

    def check_is_species(self, iri):
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

    def check_iri_in_ontology(self, iri, replacement_namespaces=None):
        return self.get_class(iri, replacement_namespaces) is not None
