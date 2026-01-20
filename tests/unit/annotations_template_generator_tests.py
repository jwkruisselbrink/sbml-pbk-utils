import unittest
import os
import libsbml as ls

from tests.conf import TEST_MODELS_PATH
from sbmlpbkutils import AnnotationsTemplateGenerator

class AnnotationsTemplateGeneratorTests(unittest.TestCase):

    def test_get_annotations_template(self):
        # Load SBML file
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.sbml')
        document = ls.readSBML(sbml_file)
        model = document.getModel()

        # Generate template
        generator = AnnotationsTemplateGenerator()
        df = generator.generate(model)

        # Check if template contains record for extent unit
        self.assertEqual(len(df.loc[df['element_id'] == 'extentUnits']), 1)

if __name__ == '__main__':
    unittest.main()
