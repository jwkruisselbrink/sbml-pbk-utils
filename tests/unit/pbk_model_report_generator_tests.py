import unittest
import os

import libsbml as ls
from tests.conf import TEST_MODELS_PATH
from parameterized import parameterized
from sbmlpbkutils import RenderMode, PbkModelReportGenerator

class PbkModelReportGeneratorTests(unittest.TestCase):

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
