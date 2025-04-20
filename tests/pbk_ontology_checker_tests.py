import unittest
import sys
from parameterized import parameterized
from sbmlpbkutils import PbkOntologyChecker

sys.path.append('../sbmlpbkutils/')

class PbkOntologyCheckerTests(unittest.TestCase):

    def test_check_in_ncbitaxon(self):
        checker = PbkOntologyChecker()
        self.assertTrue(checker.check_in_ncbitaxon("http://purl.obolibrary.org/obo/NCBITaxon_9606"))
        self.assertTrue(checker.check_in_ncbitaxon("obo:NCBITaxon_9606"))
        self.assertTrue(checker.check_in_ncbitaxon("urn:miriam:taxonomy:10095"))
        self.assertFalse(checker.check_in_ncbitaxon("https://purl.obolibrary.org/obo/NCBITaxon_9606"))
        self.assertFalse(checker.check_in_ncbitaxon("NCBITaxon_9606"))
        self.assertFalse(checker.check_in_ncbitaxon("obo/NCBITaxon_9606"))
        self.assertFalse(checker.check_in_ncbitaxon("obo.NCBITaxon_9606"))
        self.assertFalse(checker.check_in_ncbitaxon("obo:PBPKO_00450"))

    def test_check_in_pbpko(self):
        checker = PbkOntologyChecker()
        self.assertTrue(checker.check_in_pbpko("http://purl.obolibrary.org/obo/PBPKO_00450"))
        self.assertTrue(checker.check_in_pbpko("obo:PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("https://purl.obolibrary.org/obo/PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("obo/PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("obo.PBPKO_0x450"))

    def test_check_in_chebi(self):
        checker = PbkOntologyChecker()
        self.assertTrue(checker.check_in_chebi("http://purl.obolibrary.org/obo/CHEBI_25212"))
        self.assertFalse(checker.check_in_chebi("https://purl.obolibrary.org/obo/CHEBI_25212"))
        self.assertFalse(checker.check_in_chebi("https://purl.obolibrary.org/obo/PBPKO_00450"))
        self.assertTrue(checker.check_in_chebi("obo:CHEBI_25212"))
        self.assertFalse(checker.check_in_chebi("obo/CHEBI_25212"))
        self.assertFalse(checker.check_in_chebi("obo.CHEBI_25212"))

    def test_get_pbpko_class(self):
        checker = PbkOntologyChecker()
        result = checker.get_pbpko_class("http://purl.obolibrary.org/obo/PBPKO_00477")
        self.assertEqual(result.iri, "http://purl.obolibrary.org/obo/PBPKO_00477")
        self.assertEqual(result.label[0], "gut compartment")
        self.assertTrue(result.IAO_0000115[0])

    def test_get_ncbitaxon_class(self):
        iri = "http://purl.obolibrary.org/obo/NCBITaxon_40674"
        iri_full = "http://purl.obolibrary.org/obo/NCBITaxon_40674"
        checker = PbkOntologyChecker()
        result = checker.get_ncbitaxon_class(iri)
        self.assertEqual(result.iri, iri_full)
        self.assertEqual(result.label[0], "Mammalia")

    def test_get_pbpko_compartments(self):
        checker = PbkOntologyChecker()
        result = checker.get_compartment_classes()
        self.assertTrue(list(result))

    def test_get_pbpko_parameters(self):
        checker = PbkOntologyChecker()
        result = checker.get_parameter_classes()
        self.assertTrue(list(result))

    def test_get_pbpko_species(self):
        checker = PbkOntologyChecker()
        result = checker.get_species_classes()
        self.assertTrue(list(result))

    def test_get_ncbitaxon_mammalia(self):
        checker = PbkOntologyChecker()
        result = checker.get_mammal_taxon_classes()
        self.assertTrue(list(result))

    @parameterized.expand([
        ("http://purl.obolibrary.org/obo/NCBITaxon_9606"),
        ("urn:miriam:taxonomy:9606")
    ])
    def test_is_taxon_mammalia(self, iri):
        checker = PbkOntologyChecker()
        self.assertTrue(checker.check_is_animal_species(iri))

    def test_is_compartment(self):
        checker = PbkOntologyChecker()
        self.assertTrue(checker.check_is_compartment("http://purl.obolibrary.org/obo/PBPKO_00477"))
        self.assertFalse(checker.check_is_compartment("http://purl.obolibrary.org/obo/PBPKO_00029")) 
        self.assertFalse(checker.check_is_compartment("XXXX")) 
        result = checker.get_compartment_classes()
        for item in result:
            self.assertTrue(checker.check_is_compartment(item.iri))

    def test_is_input_compartment(self):
        checker = PbkOntologyChecker()
        # Alveolar air compartment (should be true)
        self.assertTrue(checker.check_is_input_compartment("http://purl.obolibrary.org/obo/PBPKO_00448"))
        # Gut compartment (should be true)
        self.assertTrue(checker.check_is_input_compartment("http://purl.obolibrary.org/obo/PBPKO_00477"))
        # Skin compartment (should be true)
        self.assertTrue(checker.check_is_input_compartment("http://purl.obolibrary.org/obo/PBPKO_00470"))
        # Stratum corneum exposed skin compartment compartment (should be true)
        self.assertTrue(checker.check_is_input_compartment("http://purl.obolibrary.org/obo/PBPKO_00458"))
        # Heart compartment (should be false)
        self.assertFalse(checker.check_is_input_compartment("http://purl.obolibrary.org/obo/PBPKO_00480"))
        # Invalid iri (should be false)
        self.assertFalse(checker.check_is_input_compartment("XXXX"))

    def test_is_inhalation_compartment(self):
        checker = PbkOntologyChecker()
        # Alveolar air compartment (should be true)
        self.assertTrue(checker.check_is_inhalation_input_compartment("http://purl.obolibrary.org/obo/PBPKO_00448"))
        # Lung compartment (should be true)
        self.assertTrue(checker.check_is_inhalation_input_compartment("http://purl.obolibrary.org/obo/PBPKO_00559"))
        # Skin compartment (should be false)
        self.assertFalse(checker.check_is_inhalation_input_compartment("http://purl.obolibrary.org/obo/PBPKO_00470"))

    def test_get_pbpko_parameters(self):
        checker = PbkOntologyChecker()
        result = checker.get_parameter_classes()
        self.assertTrue(result)

    def test_is_parameter(self):
        checker = PbkOntologyChecker()
        self.assertFalse(checker.check_is_parameter("http://purl.obolibrary.org/obo/PBPKO_00477"))
        self.assertTrue(checker.check_is_parameter("http://purl.obolibrary.org/obo/PBPKO_00029")) 
        self.assertTrue(checker.check_is_parameter("http://purl.obolibrary.org/obo/PBPKO_00078"))
        self.assertFalse(checker.check_is_parameter("XXXX")) 
        result = checker.get_parameter_classes()
        for item in result:
            #print(f'[{item.iri}] - {item.label}')
            self.assertTrue(checker.check_is_parameter(item.iri))

    def test_is_biochemical_parameter(self):
        checker = PbkOntologyChecker()
        # Partition coefficient: True
        self.assertTrue(checker.check_is_biochemical_parameter("http://purl.obolibrary.org/obo/PBPKO_00165"))

        # logP: False
        self.assertFalse(checker.check_is_biochemical_parameter("http://purl.obolibrary.org/obo/PBPKO_00130"))

        # BW: False
        self.assertFalse(checker.check_is_biochemical_parameter("http://purl.obolibrary.org/obo/PBPKO_00008"))

        # Invalid URI: False
        self.assertFalse(checker.check_is_biochemical_parameter("XXXX")) 
        result = checker.get_parameter_classes()
        for item in result:
            #print(f'[{item.iri}] - {item.label}')
            self.assertTrue(checker.check_is_parameter(item.iri))

    def test_is_physicochemical_parameter(self):
        checker = PbkOntologyChecker()
        # Partition coefficient: False
        self.assertFalse(checker.check_is_physicochemical_parameter("http://purl.obolibrary.org/obo/PBPKO_00165"))

        # logP: True
        self.assertTrue(checker.check_is_physicochemical_parameter("http://purl.obolibrary.org/obo/PBPKO_00130"))

        # BW: False
        self.assertFalse(checker.check_is_physicochemical_parameter("http://purl.obolibrary.org/obo/PBPKO_00008"))

        # Invalid URI: False
        self.assertFalse(checker.check_is_physicochemical_parameter("XXXX")) 
        result = checker.get_parameter_classes()
        for item in result:
            #print(f'[{item.iri}] - {item.label}')
            self.assertTrue(checker.check_is_parameter(item.iri))

    def test_is_physiological_parameter(self):
        checker = PbkOntologyChecker()
        # Partition coefficient: False
        self.assertFalse(checker.check_is_physiological_parameter("http://purl.obolibrary.org/obo/PBPKO_00165"))

        # logP: False
        self.assertFalse(checker.check_is_physiological_parameter("http://purl.obolibrary.org/obo/PBPKO_00130"))

        # BW: True
        self.assertTrue(checker.check_is_physiological_parameter("http://purl.obolibrary.org/obo/PBPKO_00008"))

        # Invalid URI: False
        self.assertFalse(checker.check_is_physiological_parameter("XXXX")) 
        result = checker.get_parameter_classes()
        for item in result:
            #print(f'[{item.iri}] - {item.label}')
            self.assertTrue(checker.check_is_parameter(item.iri))

    def test_is_chemical_specific_parameter(self):
        checker = PbkOntologyChecker()
        # Partition coefficient: False
        self.assertTrue(checker.check_is_chemical_specific_parameter("http://purl.obolibrary.org/obo/PBPKO_00165"))

        # logP: True
        self.assertTrue(checker.check_is_chemical_specific_parameter("http://purl.obolibrary.org/obo/PBPKO_00130"))

        # BW: True
        self.assertFalse(checker.check_is_chemical_specific_parameter("http://purl.obolibrary.org/obo/PBPKO_00008"))

        # Invalid URI: False
        self.assertFalse(checker.check_is_chemical_specific_parameter("XXXX")) 
        result = checker.get_parameter_classes()
        for item in result:
            #print(f'[{item.iri}] - {item.label}')
            self.assertTrue(checker.check_is_parameter(item.iri))

if __name__ == '__main__':
    unittest.main()
