import glob
import unittest
import os
from pathlib import Path

import libsbml as ls
from sbmlpbkutils import PbkModelReportGenerator, RenderMode
from tests.conf import TEST_OUTPUT_PATH, TEST_MODELS_PATH

class ModelReportCreationTests(unittest.TestCase):

    def setUp(self):
        self.out_path = os.path.join(TEST_OUTPUT_PATH, 'reports')
        os.makedirs(self.out_path, exist_ok=True)

    def test_generate_report(self):
        # Load SBML file
        sbml_files = glob.glob(f'{TEST_MODELS_PATH}/**/*.sbml', recursive=True)
        for sbml_file in sbml_files:
            # Load SBML file
            document = ls.readSBML(sbml_file)

            # Create report
            sbml_basename = os.path.basename(sbml_file)
            report_file = os.path.join(self.out_path, Path(sbml_basename).with_suffix('.report.md'))
            generator = PbkModelReportGenerator(document)
            generator.create_md_report(report_file, math_render_mode = RenderMode.TEXT)

if __name__ == '__main__':
    unittest.main()
