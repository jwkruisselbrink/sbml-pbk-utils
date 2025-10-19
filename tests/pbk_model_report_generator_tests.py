import unittest
import sys
import os
from pathlib import Path

import libsbml as ls
from parameterized import parameterized
from sbmlpbkutils import RenderMode, PbkModelReportGenerator

sys.path.append('../sbmlpbkutils/')

__test_models_path__ = './tests/models/'
__test_outputs_path__ = './tests/__testoutputs__'

class PbkModelReportGeneratorTests(unittest.TestCase):

    def setUp(self):
        Path(__test_outputs_path__).mkdir(parents=True, exist_ok=True)

    @parameterized.expand([
        ("simple.sbml"),
        ("simple.annotated.sbml"),
        ("simple_lifetime.annotated.sbml"),
        ("euromix.annotated.sbml")
    ])
    def test_generate_report(self, file):
        sbml_file = os.path.join(__test_models_path__, file)
        document = ls.readSBML(sbml_file)
        sbml_basename = os.path.basename(sbml_file)
        report_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.report.md'))
        generator = PbkModelReportGenerator(document)
        generator.create_md_report(report_file)

    @parameterized.expand([
        (RenderMode.TEXT),
        (RenderMode.LATEX)
    ])
    def test_get_odes_as_str(self, render_mode):
        sbml_file = os.path.join(__test_models_path__, 'simple.annotated.sbml')
        document = ls.readSBML(sbml_file)
        generator = PbkModelReportGenerator(document)
        result = generator.get_odes_as_str(render_mode)
        for key, val in result.items():
            print(f"{key}\t\t{val}\n")
        self.assertTrue(result)

    @parameterized.expand([
        (RenderMode.TEXT),
        (RenderMode.LATEX)
    ])
    def test_get_transfer_equations_as_str(self, render_mode):
        sbml_file = os.path.join(__test_models_path__, 'simple.annotated.sbml')
        document = ls.readSBML(sbml_file)
        generator = PbkModelReportGenerator(document)
        result = generator.get_transfer_equations_as_str(render_mode)
        for _, val in result.items():
            print(f"{val['id']}: {val['products'][0]}\t <= \t{val['equation']}\n")
        self.assertTrue(result)

    @parameterized.expand([
        (RenderMode.TEXT),
        (RenderMode.LATEX)
    ])
    def test_get_assignment_rules_as_str(self, render_mode):
        sbml_file = os.path.join(__test_models_path__, 'simple.annotated.sbml')
        document = ls.readSBML(sbml_file)
        generator = PbkModelReportGenerator(document)
        result = generator.get_assignment_rules_as_str(render_mode)
        for key, val in result.items():
            print(f"{key}\t\t{val}\n")
        self.assertTrue(result)

    @parameterized.expand([
        (RenderMode.TEXT),
        (RenderMode.LATEX)
    ])
    def test_get_function_as_str(self, render_mode):
        sbml_file = os.path.join(__test_models_path__, 'euromix.annotated.sbml')
        document = ls.readSBML(sbml_file)
        generator = PbkModelReportGenerator(document)
        result = generator.get_function_as_str(render_mode)
        for key, val in result.items():
            print(f"{key}\t\t{val}\n")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
