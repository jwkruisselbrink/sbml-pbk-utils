import libsbml as ls
import pandas as pd
from sbmlutils.report.mathml import astnode_to_latex

from . import PbkOntologyChecker
from . import PbkModelAnnotator
from . import TermDefinitions
from . import create_unit_string

class PbkModelInfosExtractor:

    def __init__(
        self,
        document: ls.SBMLDocument
    ):
        self.document = document
        self.model = self.document.getModel()
        self.terms_by_uri_lookup = self._init_terms_by_uri_lookup()
        self.onto_checker = PbkOntologyChecker()

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
        col_names = ["key", "value", "status", "message"]
        dt.append(["Model code", self.document.model.getMetaId()])
        dt.append(["Substance applicability domain"])
        dt.append(["Modelled species/orgamism(s)"])

        input_compartments = self.get_input_compartments()
        input_routes = set(input_compartments.values())
        input_routes_str = ' (' + str.join(", ", input_compartments.values()) + ')' if len(input_routes) > 0 else ""
        if len(input_routes) > 0:
            dt.append(["Input route(s)", f"{len(input_routes)}{input_routes_str}", "", ""])
        else:
            dt.append(["Input route(s)", "", "error", "No input routes detected."])

        if self.model.isSetTimeUnits():
            dt.append(["Time resolution", self._get_unit_string(self.model.getTimeUnits()), "", ""])
        else:
            dt.append(["Time resolution", "", "error", "Time unit missing."])

        if self.model.isSetSubstanceUnits():
            dt.append(["Amounts unit", self._get_unit_string(self.model.getSubstanceUnits()), "", ""])
        else:
            dt.append(["Amounts unit", "", "error", "Substance unit missing."])

        if self.model.isSetVolumeUnits():
            dt.append(["Volume unit", self._get_unit_string(self.model.getVolumeUnits()), "", ""])
        else:
            dt.append(["Volume unit", "", "error", "Volume unit missing."])

        dt.append(["Number of compartments", self.model.getNumCompartments(), "", ""])
        dt.append(["Number of species", self.model.getNumSpecies(), "", ""])

        internalParamsCount = 0
        externalParamsCount = 0
        for i in range(0, self.model.getNumParameters()):
            element = self.model.getParameter(i)
            if element.getConstant():
                externalParamsCount += 1
            else:
                internalParamsCount += 1

        dt.append(["Number of parameters", f'{self.model.getNumParameters()} ({externalParamsCount} external / {internalParamsCount} internal)'])

        result = pd.DataFrame(dt, columns=col_names)
        return result

    def get_compartment_infos(self):
        dt = []
        col_names = ["id", "name", "unit", "model qualifier", "status", "message"]
        for i in range(0, self.model.getNumCompartments()):
            element = self.model.getCompartment(i)
            bqm_is_class = self.get_pbko_class(element)
            status = "ok"
            messages = []
            unit = self._get_unit_string(element.getUnits())
            if not unit or unit == "":
                status = "error"
                messages.append("Unit not specified.")
            if not bqm_is_class:
                status = "error"
                messages.append("BQM_IS URI not specified.")
            dt.append(
                [
                    element.getId(),
                    element.getName(),
                    unit,
                    bqm_is_class.iri if bqm_is_class else '',
                    status,
                    " ".join(messages)
                ]
            )
        result = pd.DataFrame(dt, columns=col_names)
        return result

    def get_species_infos(self):
        dt = []
        col_names = ["id", "name", "unit", "model qualifier", "status", "message"]
        for i in range(0, self.model.getNumSpecies()):
            element = self.model.getSpecies(i)
            bqm_is_class = self.get_pbko_class(element)
            status = "ok"
            messages = []
            unit = self._get_unit_string(element.getUnits())
            if not unit or unit == "":
                status = "error"
                messages.append("Unit not specified.")
            if not bqm_is_class:
                status = "error"
                messages.append("BQM_IS URI not specified.")
            dt.append(
                [
                    element.getId(),
                    element.getName(),
                    unit,
                    bqm_is_class.iri if bqm_is_class else '',
                    status,
                    " ".join(messages)
                ]
            )
        result = pd.DataFrame(dt, columns=col_names)
        return result

    def get_parameter_infos(self):
        dt = []
        col_names = ["id", "name", "unit", "model qualifier", "status", "message"]
        for i in range(0, self.model.getNumParameters()):
            element = self.model.getParameter(i)
            bqm_is_class = self.get_pbko_class(element)
            status = "ok"
            messages = []
            unit = self._get_unit_string(element.getUnits())
            if not unit or unit == "":
                status = "error"
                messages.append("Unit not specified.")
            if not bqm_is_class:
                status = "error"
                messages.append("BQM_IS URI not specified.")
            dt.append(
                [
                    element.getId(),
                    element.getName(),
                    unit,
                    bqm_is_class.iri if bqm_is_class else '',
                    status,
                    " ".join(messages)
                ]
            )
        result = pd.DataFrame(dt, columns=col_names)
        return result

    # Get the differential equations
    def get_odes(self):
        # Get the list of species IDs
        species_ids = [species.getId() for species in self.model.getListOfSpecies()]

        # Initialize dictionaries to store the differential equations and reaction rates
        reaction_rates = {}

        # Iterate over the reactions in the model
        for i in range(self.model.getNumReactions()):
            reaction = self.model.getReaction(i)
            
            # Get the kinetic law associated with the reaction
            kinetic_law = reaction.getKineticLaw()
            if kinetic_law is None:
                continue

            # Get the reaction rate formula
            rate_formula = kinetic_law.getMath()

            # Iterate over the reactants and products of the reaction
            for j in range(reaction.getNumReactants()):
                reactant = reaction.getReactant(j)
                species_id = reactant.getSpecies()
                
                # Add the reaction rate to the dictionary
                if species_id in reaction_rates:
                    reaction_rates[species_id].append(f"- {astnode_to_latex(rate_formula)}")
                else:
                    reaction_rates[species_id] = [f"- {astnode_to_latex(rate_formula)}"]

            for j in range(reaction.getNumProducts()):
                product = reaction.getProduct(j)
                species_id = product.getSpecies()

                # Add the negative reaction rate to the dictionary
                if species_id in reaction_rates:
                    reaction_rates[species_id].append(astnode_to_latex(rate_formula))
                else:
                    reaction_rates[species_id] = [astnode_to_latex(rate_formula)]

        # Construct the differential equations for each species
        differential_equations = {}
        for species_id in species_ids:
            if species_id in reaction_rates:
                new_line = '\n'
                pref = f'{new_line}{" " * (len(species_id) + 8)}'
                equation = f"\\frac{{d[{self._math_print_element(species_id)}]}}{{dt}} = {f'{pref} + '.join(reaction_rates[species_id])}"
                differential_equations[species_id] = equation \
                    .replace("+ -", "-") \
                    .replace("·", "\cdot ")

        return differential_equations.items()

    def get_input_compartments(self):
        input_compartments = {}
        for i in range(0, self.model.getNumCompartments()):
            compartment = self.model.getCompartment(i)
            cv_terms = PbkModelAnnotator.get_cv_terms(compartment)
            for cv_term in cv_terms:
                lookup_key = f'{cv_term['qualifier']}#{cv_term['uri']}'
                if (lookup_key in self.terms_by_uri_lookup.keys()):
                    term_definition = self.terms_by_uri_lookup[lookup_key]
                    if ('exposure_route' in term_definition.keys()):
                        input_compartments.update({
                            compartment.getId() : term_definition['exposure_route'],
                        })
                        continue
        return input_compartments

    def get_input_species(self):
        input_compartments = self.get_input_compartments()
        input_species = {}
        for i in range(0, self.model.getNumSpecies()):
            element = self.model.getSpecies(i)
            species = self.model.getSpecies(i)
            compartment = element.getCompartment()
            if (compartment in input_compartments.keys()):
                input_species.update({
                    species.getId() : input_compartments[compartment]
                })
        return input_species

    def find_term_definition(self, element, element_type):
        """Tries to find a resource definition for the specified element."""
        element_id = element.getId()
        for index, value in enumerate(TermDefinitions):
            if value['element_type'] == element_type:
                if 'recommended_id' in value.keys() \
                    and element_id.lower() == value['recommended_id'].lower():
                    return value
                elif 'common_ids' in value.keys() \
                    and any(element_id.lower() == val.lower() for val in value['common_ids']):
                    return value
        return None

    def get_pbko_class(
        self,
        element: ls.SBase
    ):
        cv_terms = element.getCVTerms()
        if cv_terms is not None:
            for term in cv_terms:
                if term.getQualifierType() == ls.MODEL_QUALIFIER:
                    num_resources = term.getNumResources()
                    for j in range(num_resources):
                        iri = term.getResourceURI(j)
                        if self.onto_checker.check_in_pbpko(iri):
                            return self.onto_checker.get_class(iri)
        return None

    def _init_terms_by_uri_lookup(self):
        """Tries to find a resource definition for the specified element."""
        result = {}
        for value in TermDefinitions:
            if ('resources' in value.keys()):
                for resource in value['resources']:
                    result.update({
                        f'{resource['qualifier']}#{resource['URI']}': value
                    })
        return result

    def _math_print_element(self, id):
        return f"\\mathtt{{{id.replace('_', '-')}}}"

    def _get_unit_string(
        self,
        unit_id: ls.UnitDefinition
    ):
        """Tries to get the (UCUM) formated unit string of the specified element."""
        unit_def = self.model.getUnitDefinition(unit_id)
        if unit_def is not None:
            return create_unit_string(unit_def)
        return ""
