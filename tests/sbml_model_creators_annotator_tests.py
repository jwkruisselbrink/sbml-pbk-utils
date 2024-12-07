import unittest
import sys
import os
import libsbml as ls
from pathlib import Path
from sbmlpbkutils.sbml_model_creators_annotator import SbmlModelCreatorsAnnotator
sys.path.append('../sbmlpbkutils/')

__test_outputs_path__ = './tests/__testoutputs__'
__test_models_path__ = './tests/models/'

class SbmlModelCreatorsAnnotatorTests(unittest.TestCase):

    def test_set_model_creators_from_cff(self):
        # Arrange
        sbml_file = os.path.join(__test_models_path__, 'simple.sbml') 
        document = ls.readSBML(sbml_file)
        cff_file = './CITATION.cff'
        annotator = SbmlModelCreatorsAnnotator()

        # Act
        annotator.set_model_creators_from_cff(document, cff_file)

        # Assert
        model = document.getModel()
        model_history = model.getModelHistory()
        model_creators = model_history.getListCreators()
        self.assertGreaterEqual(len(model_creators), 1)

        # Write annotated SBML file to test results
        sbml_basename = os.path.basename(sbml_file)
        out_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.cff.sbml'))
        ls.writeSBML(document, out_file)

    def test_set_model_creators(self):
        # Arrange
        creators = [
             {
                  'given-names': 'John',
                  'family-names': 'Doe',
                  'affiliation': 'ACME PBK models',
                  'email': 'john.doe@acme-pbk.org'
             }
        ]
        sbml_file = os.path.join(__test_models_path__, 'simple.sbml') 
        document = ls.readSBML(sbml_file)
        annotator = SbmlModelCreatorsAnnotator()

        # Act
        annotator.set_model_creators(document, creators)

        # Assert
        model = document.getModel()
        model_history = model.getModelHistory()
        model_creators = model_history.getListCreators()
        self.assertEqual(len(model_creators), 1)
        self.assertEqual(model_creators[0].getFamilyName(), "Doe")
        self.assertEqual(model_creators[0].getGivenName(), "John")
        self.assertEqual(model_creators[0].getOrganization(), "ACME PBK models")
        self.assertEqual(model_creators[0].getEmail(), "john.doe@acme-pbk.org")

if __name__ == '__main__':
    unittest.main()
