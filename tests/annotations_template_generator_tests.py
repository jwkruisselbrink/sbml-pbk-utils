import unittest
import sys
import os
import libsbml as ls
from pathlib import Path
from sbmlpbkutils import AnnotationsTemplateGenerator
sys.path.append('../sbmlpbkutils/')

__test_outputs_path__ = './tests/__testoutputs__'

class AnnotationsTemplateGeneratorTests(unittest.TestCase):

    def setUp(self):
        from pathlib import Path
        Path(__test_outputs_path__).mkdir(parents=True, exist_ok=True)

    @classmethod
    def setUpClass(cls):
        cls.sbml_files = []
        files = os.listdir('./tests/models/')
        for file in files:
            if file.endswith('.sbml'):
                cls.sbml_files.append('./tests/models/' + file)

    def test_export_terms(self):
        infosExporter = AnnotationsTemplateGenerator()
        for sbml_file in self.sbml_files:
            document = ls.readSBML(sbml_file)
            model = document.getModel()
            df = infosExporter.generate(model)
            self.assertEqual(df.ndim, 2)
            sbml_basename = os.path.basename(sbml_file)
            csv_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.csv'))
            df.to_csv(csv_file, index=False)

if __name__ == '__main__':
    unittest.main()
