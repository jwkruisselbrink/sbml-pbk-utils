import unittest
import sys
import os
from pathlib import Path

import libsbml as ls
from parameterized import parameterized
from sbmlpbkutils import DiagramCreator
from sbmlpbkutils.diagram_creator import NamesDisplay

sys.path.append('../sbmlpbkutils/')

__test_models_path__ = './tests/models/'
__test_outputs_path__ = './tests/__testoutputs__'

class DiagramCreatorTests(unittest.TestCase):

    def setUp(self):
        Path(__test_outputs_path__).mkdir(parents=True, exist_ok=True)

    @parameterized.expand([
        ("simple.annotated.sbml", False, False),
        ("simple.annotated.sbml", True, False),
        ("simple.annotated.sbml", False, False),
        ("simple.annotated.sbml", True, True),
        ("euromix.annotated.sbml", True, True),
    ])
    def test_generate_report(
        self,
        file,
        draw_species,
        draw_reaction_ids
    ):
        sbml_file = os.path.join(__test_models_path__, file)
        document = ls.readSBML(sbml_file)
        for names_display in NamesDisplay:
            param_str = f"_names-{int(names_display)}_sp-{int(draw_species)}_rc-{int(draw_reaction_ids)}"
            sbml_basename = os.path.basename(sbml_file)
            output_filename = f'{Path(sbml_basename).stem}_{param_str}.diagram.svg'
            output_file = os.path.join(__test_outputs_path__, output_filename)
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
