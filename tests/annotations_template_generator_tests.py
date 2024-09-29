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

    def test_generate_no_fill(self):
        infosExporter = AnnotationsTemplateGenerator()
        for sbml_file in self.sbml_files:
            document = ls.readSBML(sbml_file)
            model = document.getModel()
            df = infosExporter.generate(model, False)
            self.assertEqual(df.ndim, 2)
            sbml_basename = os.path.basename(sbml_file)
            stem = Path(sbml_basename).stem
            csv_file = os.path.join(__test_outputs_path__, f'{stem}_no_fill.csv')
            df.to_csv(csv_file, index=False)

    def test_generate_try_fill(self):
        infosExporter = AnnotationsTemplateGenerator()
        for sbml_file in self.sbml_files:
            document = ls.readSBML(sbml_file)
            model = document.getModel()
            df = infosExporter.generate(model, True)
            self.assertEqual(df.ndim, 2)
            sbml_basename = os.path.basename(sbml_file)
            stem = Path(sbml_basename).stem
            csv_file = os.path.join(__test_outputs_path__, f'{stem}_try_fill.csv')
            df.to_csv(csv_file, index=False)

if __name__ == '__main__':
    unittest.main()
