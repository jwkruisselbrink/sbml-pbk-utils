import unittest
import sys

from sbmlpbkutils import PbkOntologyChecker

sys.path.append('../sbmlpbkutils/')

class PbkOntologyCheckerTests(unittest.TestCase):

    def test_check_in_pbpko(self):
        checker = PbkOntologyChecker()
        self.assertTrue(checker.check_in_pbpko("http://purl.obolibrary.org/obo/PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("https://purl.obolibrary.org/obo/PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("PBPKO_00450"))
        self.assertTrue(checker.check_in_pbpko("obo:PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("obo/PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("obo.PBPKO_0x450"))

    def test_find_by_label(self):
        checker = PbkOntologyChecker()
        result = checker.find_by_label('*arameter*')
        #for item in result:
            #print(f'[{item.iri}] - {item.label}')
        self.assertTrue(result)

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

    def test_get_element(self):
        checker = PbkOntologyChecker()
        result = checker.get_class("http://purl.obolibrary.org/obo/PBPKO_00477")
        print(result)
        self.assertEqual(result.iri, "http://purl.obolibrary.org/obo/PBPKO_00477")
        self.assertEqual(result.label[0], "Gut")
        self.assertEqual(result.IAO_0000115[0], "It is a part of digestive system")

    def test_is_compartment(self):
        checker = PbkOntologyChecker()
        result = checker.get_compartment_classes()
        self.assertTrue(checker.check_is_compartment("http://purl.obolibrary.org/obo/PBPKO_00477"))
        self.assertFalse(checker.check_is_compartment("http://purl.obolibrary.org/obo/PBPKO_00029")) 
        self.assertFalse(checker.check_is_compartment("XXXX")) 
        for item in result:
            #print(f'[{item.iri}] - {item.label}')
            self.assertTrue(checker.check_is_compartment(item.iri))

    def test_get_pbpko_parameters(self):
        checker = PbkOntologyChecker()
        result = checker.get_parameter_classes()
        self.assertTrue(result)

    def test_is_parameter(self):
        checker = PbkOntologyChecker()
        result = checker.get_parameter_classes()
        self.assertFalse(checker.check_is_parameter("http://purl.obolibrary.org/obo/PBPKO_00477"))
        self.assertTrue(checker.check_is_parameter("http://purl.obolibrary.org/obo/PBPKO_00029")) 
        self.assertTrue(checker.check_is_parameter("http://purl.obolibrary.org/obo/PBPKO_00078"))
        self.assertFalse(checker.check_is_parameter("XXXX")) 
        for item in result:
            #print(f'[{item.iri}] - {item.label}')
            self.assertTrue(checker.check_is_parameter(item.iri))

if __name__ == '__main__':
    unittest.main()
