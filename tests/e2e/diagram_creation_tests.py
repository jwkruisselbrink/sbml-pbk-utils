import unittest
import os
from pathlib import Path
from parameterized import parameterized

import libsbml as ls
from tests.conf import TEST_OUTPUT_PATH, TEST_MODELS_PATH
from sbmlpbkutils import DiagramCreator
from sbmlpbkutils.diagram_creator import NamesDisplay

class DiagramCreationTests(unittest.TestCase):

    def setUp(self):
        self.out_path = os.path.join(TEST_OUTPUT_PATH, 'diagrams')
        os.makedirs(self.out_path, exist_ok=True)

    @parameterized.expand([
        ("simple/simple.annotated.sbml", False, False),
        ("simple/simple.annotated.sbml", True, False),
        ("simple/simple.annotated.sbml", False, False),
        ("simple/simple.annotated.sbml", True, True),
        ("euromix/euromix.annotated.sbml", True, True),
    ])
    def test_generate_report(
        self,
        file,
        draw_species,
        draw_reaction_ids
    ):
        # Load SBML file
        sbml_file = os.path.join(TEST_MODELS_PATH, file)
        document = ls.readSBML(sbml_file)

        # Iterate over rendering options
        sbml_basename = os.path.basename(sbml_file)
        for names_display in NamesDisplay:
            param_str = f"_names-{int(names_display)}_sp-{int(draw_species)}_rc-{int(draw_reaction_ids)}"
            output_filename = f'{Path(sbml_basename).stem}_{param_str}.diagram.svg'
            output_file = os.path.join(self.out_path, output_filename)
            generator = DiagramCreator()
            generator.create_diagram(
                document,
                output_file,
                names_display=names_display,
                draw_species=draw_species,
                draw_reaction_ids=draw_reaction_ids
            )

if __name__ == '__main__':
    unittest.main()
