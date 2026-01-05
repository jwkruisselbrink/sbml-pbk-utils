import unittest
import os
from parameterized import parameterized

import libsbml as ls
from tests.conf import TEST_MODELS_PATH, TEST_OUTPUT_PATH
from sbmlpbkutils import RenderMode, PbkModelReportGenerator

class PbkModelReportGeneratorTests(unittest.TestCase):

    def setUp(self):
        self.out_path = os.path.join(TEST_OUTPUT_PATH, 'report_generator_tests')
        os.makedirs(self.out_path, exist_ok=True)

    @parameterized.expand([
        (RenderMode.TEXT),
        (RenderMode.LATEX)
    ])
    def test_generate_report(self, render_mode: RenderMode):
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.annotated.sbml')
        document = ls.readSBML(sbml_file)
        generator = PbkModelReportGenerator(document)
        report_filename = f"simple_{render_mode}.md"
        out_file = os.path.join(self.out_path, report_filename)
        generator.create_md_report(out_file, math_render_mode = render_mode)

    @parameterized.expand([
        (RenderMode.TEXT),
        (RenderMode.LATEX)
    ])
    def test_get_odes_as_str(self, render_mode: RenderMode):
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.annotated.sbml')
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
    def test_get_transfer_equations_as_str(self, render_mode: RenderMode):
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.annotated.sbml')
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
    def test_get_assignment_rules_as_str(self, render_mode: RenderMode):
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple/simple.annotated.sbml')
        document = ls.readSBML(sbml_file)
        generator = PbkModelReportGenerator(document)
        result = generator.get_assignment_rules_as_str(render_mode)
        for key, val in result.items():
            print(f"{key}\t\t{val}\n")
        self.assertTrue(result)
        self.assertEqual(6, len(result))

    @parameterized.expand([
        (RenderMode.TEXT),
        (RenderMode.LATEX)
    ])
    def test_get_function_as_str(self, render_mode: RenderMode):
        sbml_file = os.path.join(TEST_MODELS_PATH, 'simple_lifetime/simple_lifetime.annotated.sbml')
        document = ls.readSBML(sbml_file)
        generator = PbkModelReportGenerator(document)
        result = generator.get_function_as_str(render_mode)
        for key, val in result.items():
            print(f"{key}\t\t{val}\n")
        self.assertTrue(result)
        self.assertEqual(1, len(result))

if __name__ == '__main__':
    unittest.main()
