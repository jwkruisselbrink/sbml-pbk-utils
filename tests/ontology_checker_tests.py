import unittest
import sys

from sbmlpbkutils.ontology_checker import OntologyChecker

sys.path.append('../sbmlpbkutils/')

class OntologyCheckerTests(unittest.TestCase):

    def test_check_in_pbpko(self):
        checker = OntologyChecker()
        self.assertTrue(checker.check_in_pbpko("http://purl.obolibrary.org/obo/PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("https://purl.obolibrary.org/obo/PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("PBPKO_00450"))
        self.assertTrue(checker.check_in_pbpko("obo:PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("obo/PBPKO_00450"))
        self.assertFalse(checker.check_in_pbpko("obo.PBPKO_0x450"))

    def test_find_by_label(self):
        checker = OntologyChecker()
        result = checker.find_by_label('*arameter*')
        #for item in result:
            #print(f'[{item.iri}] - {item.label}')
        self.assertTrue(result)

    def test_get_pbpko_compartments(self):
        checker = OntologyChecker()
        result = checker.get_compartment_classes()
        self.assertTrue(list(result))

    def test_is_compartment(self):
        checker = OntologyChecker()
        result = checker.get_compartment_classes()
        self.assertTrue(checker.check_is_compartment("http://purl.obolibrary.org/obo/PBPKO_00477"))
        self.assertFalse(checker.check_is_compartment("http://purl.obolibrary.org/obo/PBPKO_00029")) 
        self.assertFalse(checker.check_is_compartment("XXXX")) 
        for item in result:
            #print(f'[{item.iri}] - {item.label}')
            self.assertTrue(checker.check_is_compartment(item.iri))

    def test_get_pbpko_parameters(self):
        checker = OntologyChecker()
        result = checker.get_parameter_classes()
        self.assertTrue(result)

    def test_is_parameter(self):
        checker = OntologyChecker()
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
