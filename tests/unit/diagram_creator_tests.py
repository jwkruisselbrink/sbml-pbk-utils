import unittest
from unittest.mock import Mock, patch

from sbmlpbkutils.diagram_creator import DiagramCreator


class DiagramCreatorTests(unittest.TestCase):

    @patch('sbmlpbkutils.diagram_creator.shutil.which', return_value=None)
    @patch('sbmlpbkutils.diagram_creator.Digraph')
    def test_create_diagram_without_unflatten(self, digraph, which):
        creator = DiagramCreator()
        creator.get_graph_elements = Mock(return_value=({}, [], {}))

        creator.create_diagram(Mock(), 'diagram.svg')

        which.assert_called_once_with('unflatten')
        digraph.return_value.unflatten.assert_not_called()
        digraph.return_value.render.assert_called_once()

    @patch(
        'sbmlpbkutils.diagram_creator.shutil.which',
        return_value='/usr/bin/unflatten'
    )
    @patch('sbmlpbkutils.diagram_creator.Digraph')
    def test_create_diagram_with_unflatten(self, digraph, which):
        creator = DiagramCreator()
        creator.get_graph_elements = Mock(return_value=({}, [], {}))

        creator.create_diagram(Mock(), 'diagram.svg')

        which.assert_called_once_with('unflatten')
        digraph.return_value.unflatten.assert_called_once_with(stagger=3)
        digraph.return_value.unflatten.return_value.render.assert_called_once()


if __name__ == '__main__':
    unittest.main()
