import unittest
import sys
import os
import libsbml as ls
from pathlib import Path

from sbmlpbkutils import PbkReportGenerator

sys.path.append('../sbmlpbkutils/')

__test_models_path__ = './tests/models/'
__test_outputs_path__ = './tests/__testoutputs__'

class PbkPbkReportGeneratorTests(unittest.TestCase):

    def setUp(self):
        from pathlib import Path
        Path(__test_outputs_path__).mkdir(parents=True, exist_ok=True)

    def test_generate_report(self):
        files = ['simple.sbml', 'simple.annotated.sbml']
        for file in files:
            sbml_file = os.path.join(__test_models_path__, file)
            document = ls.readSBML(sbml_file)
            sbml_basename = os.path.basename(sbml_file)
            report_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.report.md'))
            report_generator = PbkReportGenerator()
            report_generator.create_report(document, report_file)

if __name__ == '__main__':
    unittest.main()
