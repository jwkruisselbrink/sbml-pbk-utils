import libsbml as ls
import pandas as pd
from sbmlutils.report.mathml import astnode_to_latex
from enum import Enum

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
        with open(output_file, "w") as f:
            # Write the title
            f.write(f"# {name}\n\n")

            # Write the model creators table
            f.write("## Creators\n\n")
            table = self.get_model_creators()
            if table is not None:
                f.write(table.to_markdown())
                f.write("\n\n")
            else:
                f.write("*not specified*\n\n")

            # Write the model overview table
            f.write("## Overview\n\n")
            table = self.get_model_overview()
            f.write(table.to_markdown(index=False))
            f.write("\n\n")

            # Write compartment infos table
            f.write("## Compartments\n\n")
            table = self.get_compartment_infos()
            f.write(table.to_markdown(index=False))
            f.write("\n\n")

            # Write compartment infos table
            f.write("## Species\n\n")
            table = self.get_species_infos()
            f.write(table.to_markdown(index=False))
            f.write("\n\n")

            # Write compartment infos table
            f.write("## Parameters\n\n")
            table = self.get_parameter_infos()
            f.write(table.to_markdown(index=False))
            f.write("\n\n")

            # Write ODEs
            f.write("## ODEs\n\n")
            odes = self.get_odes_as_str(RenderMode.LATEX)
            for species_id, equation in odes.items():
                f.write(f"${equation}$\n\n")
            f.write("\n\n")

            function_defs = self.get_function_as_str(RenderMode.LATEX)
            for fct_id, equation in function_defs.items():
                f.write(f"${equation}$\n\n")
            f.write("\n\n")

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

            function_defs = self.get_function_as_str(RenderMode.LATEX)
            for fct_id, equation in function_defs.items():
                f.write(f"${equation}$\n\n")
            f.write("\n\n")

    def get_model_creators(self) -> pd.DataFrame:
        dt = []
        col_names = ["first-name", "last-name", "affiliation", "email"]
        model = self.document.getModel()
        if model.isSetModelHistory():
            model_history = model.getModelHistory()
            if (model_history.getNumCreators() > 0):
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
        if (len(animal_species) > 0):
            species = [x.iri for x in animal_species]
            dt.append(["Modelled species/orgamism(s)", ", ".join(species)])
        else:
            dt.append(["Modelled species/orgamism(s)", "*not specified*"])

        model_chemicals = self.infos_extractor.get_model_chemicals()
        if (len(model_chemicals) > 0):
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

        internalParamsCount = 0
        externalParamsCount = 0
        for i in range(0, model.getNumParameters()):
            element = model.getParameter(i)
            if element.getConstant():
                externalParamsCount += 1
            else:
                internalParamsCount += 1

        dt.append(["Number of parameters", f'{model.getNumParameters()} ({externalParamsCount} external / {internalParamsCount} internal)'])

        result = pd.DataFrame(dt, columns=col_names)
        return result

    def get_compartment_infos(self):
        dt = []
        col_names = ["id", "name", "unit", "model qualifier"]
        model = self.document.getModel()
        for i in range(0, model.getNumCompartments()):
            element = model.getCompartment(i)
            bqm_is_class = self.infos_extractor.get_pbko_class(element)
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
            bqm_is_class = self.infos_extractor.get_pbko_class(element)
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
            bqm_is_class = self.infos_extractor.get_pbko_class(element)
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
                equation = f"\\frac{{d[{PbkModelReportGenerator._math_print_element(species_id)}]}}{{dt}} = {f'{pref} + '.join(reaction_rates[species_id])}"
                differential_equations[species_id] = equation \
                    .replace("+ -", "-") \
                    .replace("·", "\cdot ")

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
            idReaction = reaction.getId()
            result[idReaction] = {
                'id': idReaction,
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
        if (render_mode == RenderMode.TEXT):
            return ls.formulaToString(ast_node).strip()
        elif (render_mode == RenderMode.LATEX):
            return astnode_to_latex(ast_node).replace("·", "\cdot ")

    @staticmethod
    def _math_print_element(id):
        return f"\\mathtt{{{id.replace('_', '-')}}}"

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
