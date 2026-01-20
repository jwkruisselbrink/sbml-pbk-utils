import unittest
from parameterized import parameterized

from sbmlpbkutils import PbkOntologyChecker

class PbkOntologyCheckerTests(unittest.TestCase):

    @parameterized.expand([
        ("http://purl.obolibrary.org/obo/NCBITaxon_9606", True),
        ("https://purl.obolibrary.org/obo/NCBITaxon_9606", True),
        ("http://identifiers.org/taxonomy/40674", True),
        ("https://identifiers.org/taxonomy/40674", True),
        ("obo:NCBITaxon_9606", True),
        ("urn:miriam:taxonomy:10095", True),
        ("NCBITaxon_9606", False),
        ("obo/NCBITaxon_9606", False),
        ("obo.NCBITaxon_9606", False),
        ("obo:PBPKO_00450", False)
    ])
    def test_check_in_ncbitaxon(self, iri, expected):
        checker = PbkOntologyChecker()
        self.assertEqual(expected, checker.check_in_ncbitaxon(iri))

    def test_check_in_pbpko(self):
        checker = PbkOntologyChecker()
        self.assertTrue(checker.check_in_pbpko("http://purl.obolibrary.org/obo/PBPKO_00450"))
        self.assertTrue(checker.check_in_pbpko("https://purl.obolibrary.org/obo/PBPKO_00450"))
        self.assertTrue(checker.check_in_pbpko("obo:PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("obo/PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("obo.PBPKO_0x450"))

    @parameterized.expand([
        ("http://purl.obolibrary.org/obo/CHEBI_25212", True),
        ("https://purl.obolibrary.org/obo/CHEBI_25212", True),
        ("https://purl.obolibrary.org/obo/PBPKO_00450", False),
        ("http://identifiers.org/chebi/CHEBI:24431", True),
        ("https://identifiers.org/chebi/CHEBI:24431", True),
        ("http://identifiers.org/CHEBI:24431", True),
        ("https://identifiers.org/CHEBI:24431", True),
        ("obo:CHEBI_25212", True),
        ("obo/CHEBI_25212", False),
        ("obo.CHEBI_25212", False)
    ])
    def test_check_in_chebi(self, iri, expected):
        checker = PbkOntologyChecker()
        self.assertEqual(expected, checker.check_in_chebi(iri))

    def test_get_pbpko_class(self):
        checker = PbkOntologyChecker()
        result = checker.get_pbpko_class("http://purl.obolibrary.org/obo/PBPKO_00477")
        self.assertEqual(result.iri, "http://purl.obolibrary.org/obo/PBPKO_00477")
        self.assertEqual(result.label[0], "gut compartment")
        self.assertTrue(result.IAO_0000115[0])

    @parameterized.expand([
        ("40674", "Mammalia"),
        ("9606", "Homo sapiens")
    ])
    def test_get_ncbitaxon_class(self, term_id, label_exp):
        checker = PbkOntologyChecker()
        iri_expected = f"http://purl.obolibrary.org/obo/NCBITaxon_{term_id}"
        patterns = [
            "http://purl.obolibrary.org/obo/NCBITaxon_",
            "https://purl.obolibrary.org/obo/NCBITaxon_",
            "http://identifiers.org/taxonomy/",
            "https://identifiers.org/taxonomy/",
            "urn:miriam:taxonomy:",
            "obo:NCBITaxon_",
        ]
        for pattern in patterns:
            iri = f"{pattern}{term_id}"
            result = checker.get_ncbitaxon_class(iri)
            self.assertIsNotNone(result)
            self.assertEqual(result.iri, iri_expected)
            self.assertEqual(result.label[0], label_exp)

    @parameterized.expand([
        ("24431", "chemical entity"),
        ("25212", "metabolite"),
        ("35549", "perfluorooctanoic acid")
    ])
    def test_get_chebi_class(self, term_id, label_exp):
        checker = PbkOntologyChecker()
        iri_expected = f"http://purl.obolibrary.org/obo/CHEBI_{term_id}"
        patterns = [
            "http://purl.obolibrary.org/obo/CHEBI_",
            "https://purl.obolibrary.org/obo/CHEBI_",
            "http://identifiers.org/chebi/CHEBI:",
            "https://identifiers.org/chebi/CHEBI:",
            "http://identifiers.org/CHEBI:",
            "https://identifiers.org/CHEBI:",
            "urn:miriam:chebi:",
            "obo:CHEBI_",
        ]
        for pattern in patterns:
            iri = f"{pattern}{term_id}"
            result = checker.get_chebi_class(iri)
            self.assertIsNotNone(result)
            self.assertEqual(result.iri, iri_expected)
            self.assertEqual(result.label[0], label_exp)

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

    @parameterized.expand([
        ("http://identifiers.org/chebi/CHEBI:24431", True), # chemical entity
        ("http://identifiers.org/chebi/CHEBI:25212", True), # metabolite
        ("http://identifiers.org/chebi/CHEBI:33585", True), # lead molecular entity
        ("urn:miriam:chebi:24431", True),
        ("http://purl.obolibrary.org/obo/NCBITaxon_9606", False)
    ])
    def test_is_chemical(self, iri, expected):
        checker = PbkOntologyChecker()
        self.assertEqual(checker.check_is_chemical(iri), expected)

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

    @parameterized.expand([
        ("http://purl.obolibrary.org/obo/PBPKO_00477", False), # gut compartment
        ("http://purl.obolibrary.org/obo/PBPKO_00029", True),
        ("http://purl.obolibrary.org/obo/PBPKO_00078", True),
        ("http://purl.obolibrary.org/obo/PBPKO_00650", True),
        ("http://purl.obolibrary.org/obo/PBPKO_00", False),
        ("http://purl.obolibrary.org/obo/PBPKO_00446", False)
    ])
    def test_is_parameter(self, uri, expected):
        checker = PbkOntologyChecker()
        self.assertEqual(checker.check_is_parameter(uri), expected)

    def test_is_parameter_all(self):
        checker = PbkOntologyChecker()
        result = checker.get_parameter_classes()
        for item in result:
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
