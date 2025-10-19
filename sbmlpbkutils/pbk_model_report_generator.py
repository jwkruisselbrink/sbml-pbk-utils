from enum import Enum
import libsbml as ls
import os
from pathlib import Path
import pandas as pd
from sbmlutils.report.mathml import astnode_to_latex

from sbmlpbkutils.diagram_creator import DiagramCreator, NamesDisplay

from . import PbkModelInfosExtractor
from . import create_unit_string

class RenderMode(Enum):
    TEXT = 1
    LATEX = 2

class PbkModelReportGenerator():

    def __init__(
        self,
        document: ls.SBMLDocument,
    ):
        self.document = document
        self.infos_extractor = PbkModelInfosExtractor(self.document)

    def create_md_report(
        self,
        output_file: str
    ):
        model = self.document.getModel()
        name = model.getName() if model.isSetName() else model.getId()

        # Open the file in write mode
        with open(output_file, mode="w", encoding="utf-8") as f:
            # Write the title
            f.write(f"# {name}\n\n")

            # Write the model overview table
            f.write("## Overview\n\n")
            table = self.get_model_overview()
            f.write(table.to_markdown(index=False))
            f.write("\n\n")

            # Generate and write the diagram
            f.write("## Diagram\n\n")
            diagram_file = Path(output_file).with_suffix('.svg')
            diagram_creator = DiagramCreator()
            diagram_creator.create_diagram(
                self.document,
                diagram_file,
                names_display=NamesDisplay.ELEMENT_IDS_AND_ONTO_IDS,
                draw_species=True,
                draw_reaction_ids=True
            )
            f.write(f"![Diagram]({diagram_file.name})")
            f.write("\n\n")

            # Write compartment infos table
            f.write("## Compartments\n\n")
            if (model.getNumCompartments() > 0):
                table = self.get_compartment_infos()
                f.write(table.to_markdown(index=False))
                f.write("\n\n")
            else:
                f.write("*no compartments defined in the model*\n\n")

            # Write compartment infos table
            f.write("## Species\n\n")
            if (model.getNumSpecies() > 0):
                table = self.get_species_infos()
                f.write(table.to_markdown(index=False))
                f.write("\n\n")
            else:
                f.write("*no species defined in the model*\n\n")

            # Write Transfer equations
            f.write("## Transfer equations\n\n")
            transfer_equations = list(self.get_transfer_equations_as_str(RenderMode.LATEX).values())
            table = pd.DataFrame({
                'id': [ x['id'] for x in transfer_equations ],
                'from': [ x['reactants'][0] for x in transfer_equations ],
                'to': [ x['products'][0] for x in transfer_equations ],
                'equation': [ f"${x['equation']}$" for x in transfer_equations ]
            })
            f.write(table.to_markdown(index=False))
            f.write("\n\n")

            # Write ODEs
            f.write("## ODEs\n\n")
            odes = self.get_odes_as_str(RenderMode.LATEX)
            for _, equation in odes.items():
                f.write(f"${equation}$\n\n")

            # Write rate rules
            rate_rules = self.get_rate_rules_as_str(RenderMode.LATEX)
            if (len(rate_rules) > 0):
                f.write("## Rate rules\n\n")
                for _, equation in rate_rules.items():
                    f.write(f"${equation}$\n\n")

            # Write assignment rules
            assignment_rules = self.get_assignment_rules_as_str(RenderMode.LATEX)
            if (len(assignment_rules) > 0):
                f.write("## Assignment rules\n\n")
                for _, equation in assignment_rules.items():
                    f.write(f"${equation}$\n\n")

            # Write assignment rules
            initial_assignments = self.get_initial_assigments_as_str(RenderMode.LATEX)
            if (len(initial_assignments) > 0):
                f.write("## Initial assignments\n\n")
                for _, equation in initial_assignments.items():
                    f.write(f"${equation}$\n\n")

            # Write functions
            function_defs = self.get_function_as_str(RenderMode.LATEX)
            if (len(function_defs) > 0):
                f.write("## Function definitions\n\n")
                for _, equation in function_defs.items():
                    f.write(f"${equation}$\n\n")

            # Write compartment infos table
            f.write("## Parameters\n\n")
            if (model.getNumParameters() > 0):
                table = self.get_parameter_infos()
                f.write(table.to_markdown(index=False))
                f.write("\n\n")
            else:
                f.write("*no parameters defined in the model*\n\n")

            # Write the model creators table
            f.write("## Creators\n\n")
            table = self.get_model_creators()
            if table is not None:
                f.write(table.to_markdown())
                f.write("\n\n")
            else:
                f.write("*not specified*\n\n")


    def get_model_creators(self) -> pd.DataFrame:
        dt = []
        col_names = ["first-name", "last-name", "affiliation", "email"]
        model = self.document.getModel()
        if model.isSetModelHistory():
            model_history = model.getModelHistory()
            if model_history.getNumCreators() > 0:
                model_creators = model_history.getListCreators()
                for creator in model_creators:
                    dt.append([
                        creator.getGivenName(),
                        creator.getFamilyName(),
                        creator.getOrganization(),
                        creator.getEmail()
                    ])
                result = pd.DataFrame(dt, columns=col_names)
                return result
        return None

    def get_model_overview(self) -> pd.DataFrame:
        dt = []
        col_names = ["key", "value"]
        model = self.document.getModel()

        animal_species = self.infos_extractor.get_model_animal_species()
        if len(animal_species) > 0:
            species = [x.iri for x in animal_species]
            dt.append(["Modelled species/orgamism(s)", ", ".join(species)])
        else:
            dt.append(["Modelled species/orgamism(s)", "*not specified*"])

        model_chemicals = self.infos_extractor.get_model_chemicals()
        if len(model_chemicals) > 0:
            chemicals = [x.iri for x in model_chemicals]
            dt.append(["Model chemical(s)", ", ".join(chemicals)])
        else:
            dt.append(["Model chemical(s)", "*not specified*"])

        input_compartments = self.infos_extractor.get_input_compartments()
        input_routes = set(input_compartments.values())
        input_routes_str = ' (' + str.join(", ", input_compartments.values()) + ')' if len(input_routes) > 0 else ""
        if len(input_routes) > 0:
            dt.append(["Input route(s)", f"{len(input_routes)}{input_routes_str}"])
        else:
            dt.append(["Input route(s)", "*no routes detected*"])

        if model.isSetTimeUnits():
            dt.append(["Time resolution", self._get_unit_string(model.getTimeUnits())])
        else:
            dt.append(["Time resolution", "*not specified*"])

        if model.isSetSubstanceUnits():
            dt.append(["Amounts unit", self._get_unit_string(model.getSubstanceUnits())])
        else:
            dt.append(["Amounts unit", "*not specified*"])

        if model.isSetVolumeUnits():
            dt.append(["Volume unit", self._get_unit_string(model.getVolumeUnits())])
        else:
            dt.append(["Volume unit", "*not specified*"])

        dt.append(["Number of compartments", model.getNumCompartments()])
        dt.append(["Number of species", model.getNumSpecies()])

        internal_params_count = 0
        external_params_count = 0
        for i in range(0, model.getNumParameters()):
            element = model.getParameter(i)
            if element.getConstant():
                external_params_count += 1
            else:
                internal_params_count += 1

        dt.append([
            "Number of parameters",
            f"{model.getNumParameters()} ({external_params_count} external / {internal_params_count} internal)"
        ])

        result = pd.DataFrame(dt, columns=col_names)
        return result

    def get_compartment_infos(self):
        dt = []
        col_names = ["id", "name", "unit", "model qualifier"]
        model = self.document.getModel()
        for i in range(0, model.getNumCompartments()):
            element = model.getCompartment(i)
            cv_terms = element.getCVTerms()
            bqm_is_class = self.infos_extractor.get_pbko_class(cv_terms)
            unit = self._get_unit_string(element.getUnits())
            name = element.getName()
            dt.append(
                [
                    element.getId(),
                    name if name else "*not specified*",
                    unit if unit else "*not specified*",
                    bqm_is_class.iri if bqm_is_class else "*not specified*",
                ]
            )
        result = pd.DataFrame(dt, columns=col_names)
        return result

    def get_species_infos(self):
        dt = []
        col_names = ["id", "name", "unit", "model qualifier"]
        model = self.document.getModel()
        for i in range(0, model.getNumSpecies()):
            element = model.getSpecies(i)
            cv_terms = element.getCVTerms()
            bqm_is_class = self.infos_extractor.get_pbko_class(cv_terms)
            unit = self._get_unit_string(element.getUnits())
            name = element.getName()
            dt.append(
                [
                    element.getId(),
                    name if name else "*not specified*",
                    unit if unit else "*not specified*",
                    bqm_is_class.iri if bqm_is_class else "*not specified*"
                ]
            )
        result = pd.DataFrame(dt, columns=col_names)
        return result

    def get_parameter_infos(self):
        model = self.document.getModel()
        dt = []
        col_names = ["id", "name", "unit", "model qualifier"]
        for i in range(0, model.getNumParameters()):
            element = model.getParameter(i)
            cv_terms = element.getCVTerms()
            bqm_is_class = self.infos_extractor.get_pbko_class(cv_terms)
            unit = self._get_unit_string(element.getUnits())
            name = element.getName()
            dt.append(
                [
                    element.getId(),
                    name if name else "*not specified*",
                    unit if unit else "*not specified*",
                    bqm_is_class.iri if bqm_is_class else "*not specified*"
                ]
            )
        result = pd.DataFrame(dt, columns=col_names)
        return result

    # Get the differential equations
    def get_odes_as_str(
        self,
        render_mode: RenderMode = RenderMode.TEXT
    ):
        model = self.document.getModel()

        # Get the list of species IDs
        species_ids = [species.getId() for species in model.getListOfSpecies()]

        # Initialize dictionaries to store the differential equations and reaction rates
        reaction_rates = {}

        # Iterate over the reactions in the model
        for i in range(model.getNumReactions()):
            reaction = model.getReaction(i)

            # Get the kinetic law associated with the reaction
            kinetic_law = reaction.getKineticLaw()
            if kinetic_law is None:
                continue

            # Get the reaction rate formula
            rate_formula = kinetic_law.getMath()

            # Iterate over the reactants
            for j in range(reaction.getNumReactants()):
                reactant = reaction.getReactant(j)
                species_id = reactant.getSpecies()
                
                # Add the negative reaction rate to the dictionary
                if species_id in reaction_rates:
                    reaction_rates[species_id].append(f"- {PbkModelReportGenerator._ast_node_to_str(rate_formula, render_mode)}")
                else:
                    reaction_rates[species_id] = [f"- {PbkModelReportGenerator._ast_node_to_str(rate_formula, render_mode)}"]

            # Iterate over the products
            for j in range(reaction.getNumProducts()):
                product = reaction.getProduct(j)
                species_id = product.getSpecies()

                # Add the reaction rate to the dictionary
                if species_id in reaction_rates:
                    reaction_rates[species_id].append(PbkModelReportGenerator._ast_node_to_str(rate_formula, render_mode))
                else:
                    reaction_rates[species_id] = [PbkModelReportGenerator._ast_node_to_str(rate_formula, render_mode)]

        # Construct the differential equations for each species
        differential_equations = {}
        for species_id in species_ids:
            if species_id in reaction_rates:
                new_line = '\n'
                pref = f'{new_line}{" " * (len(species_id) + 8)}'
                if render_mode == RenderMode.LATEX:
                    equation = f"\\frac{{d[{PbkModelReportGenerator._math_print_element(species_id)}]}}{{dt}} = {f'{pref} + '.join(reaction_rates[species_id])}"
                    equation = equation \
                        .replace("+ -", "-") \
                        .replace("·", "\\cdot ")
                else:
                    equation = f"d[{species_id}]/dt = {f'{pref} + '.join(reaction_rates[species_id])}"
                    equation = equation \
                        .replace("+ -", "-") \
                        .replace("·", "*")

                differential_equations[species_id] = equation

        return differential_equations

    def get_transfer_equations_as_str(
        self,
        render_mode: RenderMode = RenderMode.TEXT
    ):
        result = {}
        model = self.document.getModel()
        for reaction in model.getListOfReactions():
            products = []
            for product in reaction.getListOfProducts():
                products.append(product.getSpecies())
            reactants = []
            for reactant in reaction.getListOfReactants():
                reactants.append(reactant.getSpecies())

            eq = PbkModelReportGenerator._reaction_to_equation(reaction, render_mode)
            id_reaction = reaction.getId()
            result[id_reaction] = {
                'id': id_reaction,
                'equation': eq,
                'products': products,
                'reactants': reactants
            }
        return result

    def get_function_as_str(
        self,
        render_mode: RenderMode = RenderMode.TEXT
    ):
        model = self.document.getModel()
        result = {}
        for function in model.getListOfFunctionDefinitions():
            args = []
            for i in range(function.getNumArguments()):
                args.append(PbkModelReportGenerator._ast_node_to_str(function.getArgument(i), render_mode))
            eq = f'{function.getId()}({", ".join(args)}) = {PbkModelReportGenerator._ast_node_to_str(function.getMath(), render_mode)}'
            result[function.getId()] = eq
        return result

    def get_initial_assigments_as_str(
        self,
        render_mode: RenderMode = RenderMode.TEXT
    ):
        """Return a dict of initial assignments with their variable and rendered equation.
        Keyed by the target variable name.
        """
        result = {}
        model = self.document.getModel()

        for initial_assignment in model.getListOfInitialAssignments():
            variable = initial_assignment.getId()
            math = initial_assignment.getMath()
            equation = PbkModelReportGenerator._ast_node_to_str(math, render_mode)
            result[variable] = f'{variable} = {equation}'

        return result

    def get_assignment_rules_as_str(
        self,
        render_mode: RenderMode = RenderMode.TEXT
    ):
        """Return a dict of assignment rules with their variable and rendered equation.
        Keyed by the target variable name.
        """
        result = {}
        model = self.document.getModel()

        for rule in model.getListOfRules():
            is_assignment = (rule.getTypeCode() == ls.SBML_ASSIGNMENT_RULE)
            # Only consider assignment rules
            if not is_assignment:
                continue

            variable = rule.getVariable()
            math = rule.getMath()
            equation = PbkModelReportGenerator._ast_node_to_str(math, render_mode)
            result[variable] = f'{variable} = {equation}'

        return result

    def get_rate_rules_as_str(
        self,
        render_mode: RenderMode = RenderMode.TEXT
    ):
        """Return a dict of rate rules with their variable and rendered equation.
        Keyed by the target variable name.
        """
        result = {}
        model = self.document.getModel()

        for rule in model.getListOfRules():
            is_rate_rule = rule.getTypeCode() == ls.SBML_RATE_RULE
            # Only consider rate rules
            if not is_rate_rule:
                continue

            variable = rule.getVariable()
            math = rule.getMath()
            equation = PbkModelReportGenerator._ast_node_to_str(math, render_mode)
            if render_mode == RenderMode.LATEX:
                result[variable] = f'\\frac{{d{variable}}}{{dt}} = {equation}'
            else:
                result[variable] = f'd{variable}/dt = {equation}'

        return result

    @staticmethod
    def _reaction_to_equation(
        reaction: ls.Reaction,
        render_mode: RenderMode = RenderMode.TEXT
    ):
        kinetic_law = reaction.getKineticLaw()
        rate_formula = kinetic_law.getMath()
        equation = PbkModelReportGenerator._ast_node_to_str(rate_formula, render_mode)
        return equation

    @staticmethod
    def _ast_node_to_str(
        ast_node: ls.ASTNode,
        render_mode: RenderMode
    ):
        if render_mode == RenderMode.TEXT:
            return ls.formulaToString(ast_node).strip()
        elif render_mode == RenderMode.LATEX:
            return astnode_to_latex(ast_node).replace("·", "\\cdot ")

    @staticmethod
    def _math_print_element(element_id):
        return f"\\mathtt{{{element_id.replace('_', '-')}}}"

    def _get_unit_string(
        self,
        unit_id: ls.UnitDefinition
    ):
        """Tries to get the (UCUM) formated unit string of the specified element."""
        model = self.document.getModel()
        unit_def = model.getUnitDefinition(unit_id)
        if unit_def is not None:
            return create_unit_string(unit_def)
        return ""
