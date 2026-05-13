import typing
import os
from pathlib import Path
from enum import IntEnum
import libsbml as ls
from graphviz import Digraph

from sbmlpbkutils import PbkModelInfosExtractor

class NamesDisplay(IntEnum):
    NONE = 0
    ELEMENT_IDS = 1
    ELEMENT_NAMES = 2
    ELEMENT_IDS_AND_ONTO_IDS = 3
    ELEMENT_NAMES_AND_ONTO_IDS = 4
    ONTO_LABELS_AND_IDS = 5

SPECIES_CHEBI_COLORS = [
    'gold',
    'mediumspringgreen',
    'lightcoral',
    'lightskyblue',
    'plum',
    'khaki',
    'lightsalmon',
    'paleturquoise',
    'mediumaquamarine',
    'thistle',
]

class DiagramCreator:

    @staticmethod
    def _get_species_chebi_color_map(species):
        chebi_to_color = {}
        color_index = 0
        for sp_info in species.values():
            chebi_class = sp_info.chebi_bqb_is_class
            if chebi_class not in chebi_to_color:
                if chebi_class is None:
                    chebi_to_color[chebi_class] = 'gold'
                else:
                    chebi_to_color[chebi_class] = SPECIES_CHEBI_COLORS[
                        color_index % len(SPECIES_CHEBI_COLORS)
                    ]
                    color_index += 1
        return chebi_to_color

    def create_diagram(
        self,
        document: ls.SBMLDocument,
        output_file: typing.Union[os.PathLike, str, None],
        names_display: NamesDisplay = NamesDisplay.ELEMENT_IDS,
        draw_species: bool = True,
        draw_reaction_ids: bool = True
    ):
        # Parse the SBML file
        draw_compartment_edges = not draw_species
        species, reactions, compartments = self.get_graph_elements(
            document,
            draw_compartment_edges
        )

        chebi_color_map = self._get_species_chebi_color_map(species)

        dot = Digraph(
            format="svg",
            node_attr={'fontname': 'Arial'}
        )
        dot.attr(size="7,4")
        dot.attr(ratio="fill")

        # Create compartments as subgraphs
        for comp_id, comp_info in compartments.items():

            # Determine compartment label
            comp_label = self.get_element_label(names_display, comp_id, comp_info)

            if draw_species:
                with dot.subgraph(name=f'cluster_{comp_id}') as subgraph:
                    subgraph.attr(
                        label=comp_label,
                        shape='box',
                        style='filled,rounded',
                        fillcolor='lightblue',
                        color='black',
                        href=f'#compartment-{comp_id}',
                        fontname='Arial'
                    )
                    for sp_id, species_info in species.items():
                        if species_info.compartment_id == comp_id:
                            sp_label = self.get_element_label(names_display, sp_id, species_info)
                            sp_color = chebi_color_map[species_info.chebi_bqb_is_class]
                            subgraph.node(
                                sp_id,
                                label=sp_label,
                                shape='box',
                                style='filled,rounded',
                                fillcolor=sp_color,
                                color='black',
                                href=f'#species-{sp_id}'
                            )
            else:
                dot.node(
                    comp_id,
                    label=comp_label,
                    shape='box',
                    style='filled,rounded',
                    fillcolor='lightblue',
                    color='black',
                    href=f'#compartment-{comp_id}'
                )

        # Create edges for reactions
        for (id, source, target) in reactions:
            dot.edge(
                source,
                target,
                label=id if draw_reaction_ids else None
            )

        # Save and render the diagram
        dot = dot.unflatten(stagger=3)
        dot.render(
            outfile=output_file,
            engine='dot',
            filename=Path(output_file).with_suffix('.dot').name if output_file else None,
            directory=Path(output_file).parent if output_file else None,
            view=False
        )

    def get_element_label(self, names_display, element_id, element_info):
        comp_label = ' '
        if names_display in {
                NamesDisplay.ELEMENT_IDS,
                NamesDisplay.ELEMENT_IDS_AND_ONTO_IDS
            }:
            comp_label = element_id
        elif names_display in {
                NamesDisplay.ELEMENT_NAMES,
                NamesDisplay.ELEMENT_NAMES_AND_ONTO_IDS
            }:
            comp_label = element_info.name if element_info.name else element_id

        onto_label = element_info.pbpko_bqm_is_class.name.replace('_', ':') \
                if element_info.pbpko_bqm_is_class else '-'
        if names_display == NamesDisplay.ELEMENT_IDS_AND_ONTO_IDS:
            comp_label = comp_label + f"\n[{onto_label}]"
        elif names_display == NamesDisplay.ELEMENT_NAMES_AND_ONTO_IDS:
            comp_label = comp_label + f"\n[{onto_label}]"
        elif names_display == NamesDisplay.ONTO_LABELS_AND_IDS:
            comp_label = element_info.pbpko_bqm_is_class.label[0] \
                    if element_info.pbpko_bqm_is_class else element_id
            comp_label = comp_label + f"\n[{onto_label}]"

        return comp_label

    def get_graph_elements(
        self,
        document: ls.SBMLDocument,
        draw_compartment_edges: bool = False
    ):
        model = document.getModel()
        infos_exporter = PbkModelInfosExtractor(document)

        # Extract compartments
        compartments = {
            comp.getId(): infos_exporter.get_compartment_info(comp)
            for comp in model.getListOfCompartments()
        }

        # Extract species
        species = {
            sp.getId(): infos_exporter.get_species_info(sp)
            for sp in model.getListOfSpecies()
        }

        # Extract reactions
        reactions = []
        if draw_compartment_edges:
            for reaction in model.getListOfReactions():
                for reactant in reaction.getListOfReactants():
                    reactant_species_id = reactant.getSpecies()
                    reactant_compartment = species[reactant_species_id].compartment_id
                    for product in reaction.getListOfProducts():
                        product_species_id = product.getSpecies()
                        product_compartment = species[product_species_id].compartment_id
                        reactions.append((reaction.getId(), reactant_compartment, product_compartment))
        else:
            for reaction in model.getListOfReactions():
                for reactant in reaction.getListOfReactants():
                    for product in reaction.getListOfProducts():
                        reactions.append((reaction.getId(), reactant.getSpecies(), product.getSpecies()))

        return species, reactions, compartments
