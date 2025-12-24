from typing import Dict, assert_never, cast

import libsbml as ls

from . import PbkOntologyChecker
from . import create_unit_string

class PbkModelInfosExtractor:

    def __init__(
        self,
        document: ls.SBMLDocument
    ):
        self.document = document
        self.model = self.document.getModel()
        self.onto_checker = PbkOntologyChecker()

    def get_model_info(self):
        pbk_model_infos_extractor = PbkModelInfosExtractor(self.document)
        input_compartments = pbk_model_infos_extractor.get_input_compartments()
        input_routes = set(input_compartments.values())
        time_unit = self.get_unit_string(self.model.getTimeUnits()) if self.model.isSetTimeUnits() else None
        amounts_unit = self.get_unit_string(self.model.getSubstanceUnits()) if self.model.isSetSubstanceUnits() else None
        volume_unit = self.get_unit_string(self.model.getVolumeUnits()) if self.model.isSetVolumeUnits() else None
        extent_unit = self.get_unit_string(self.model.getExtentUnits()) if self.model.isSetExtentUnits() else None
        num_internal_parameters = 0
        num_external_parameters = 0
        for i in range(0, self.model.getNumParameters()):
            element = self.model.getParameter(i)
            if element.getConstant():
                num_external_parameters += 1
            else:
                num_internal_parameters += 1
        result = ModelInfo(
            self.model.getMetaId(),
            self.model.getCVTerms(),
            pbk_model_infos_extractor.get_model_animal_species(),
            pbk_model_infos_extractor.get_model_chemicals(),
            input_routes,
            time_unit,
            amounts_unit,
            volume_unit,
            extent_unit,
            self.model.getNumCompartments(),
            self.model.getNumSpecies(),
            num_internal_parameters,
            num_external_parameters
        )
        return result

    def get_element_info(self, element: ls.SBase):
        match element.getTypeCode():
            case ls.SBML_COMPARTMENT:
                return self.get_compartment_info(cast(ls.Compartment, element))
            case ls.SBML_SPECIES:
                return self.get_species_info(cast(ls.Species, element))
            case ls.SBML_PARAMETER:
                return self.get_parameter_info(cast(ls.Parameter, element))
        return None

    def get_compartment_infos(self):
        element_infos = []
        for i in range(0, self.model.getNumCompartments()):
            element = self.model.getCompartment(i)
            info_record = self.get_compartment_info(element)
            element_infos.append(info_record)
        return element_infos

    def get_compartment_info(self, element: ls.Compartment):
        cv_terms = element.getCVTerms()
        info_record = ElementInfo(
            element.getId(),
            "compartment",
            element.getName(),
            self.get_unit_string(element.getUnits()),
            cv_terms,
            self.get_pbko_class(cv_terms)
        )
        return info_record

    def get_species_infos(self):
        element_infos = []
        for i in range(0, self.model.getNumSpecies()):
            element = self.model.getSpecies(i)
            info_record = self.get_species_info(element)
            element_infos.append(info_record)
        return element_infos

    def get_species_info(self, element: ls.Species):
        cv_terms = element.getCVTerms()
        info_record = SpeciesInfo(
            element.getId(),
            element.getName(),
            element.getCompartment(),
            self.get_unit_string(element.getUnits()),
            cv_terms,
            self.get_pbko_class(cv_terms),
            self.get_chebi_iri(cv_terms)
        )
        return info_record

    def get_parameter_infos(self):
        element_infos = []
        for i in range(0, self.model.getNumParameters()):
            element = self.model.getParameter(i)
            info_record = self.get_parameter_info(element)
            element_infos.append(info_record)
        return element_infos

    def get_parameter_info(self, element: ls.Parameter):
        cv_terms = element.getCVTerms()
        pbpko_bqm_is_class = self.get_pbko_class(cv_terms)
        chemical_specific = self.onto_checker.check_is_chemical_specific_parameter(pbpko_bqm_is_class.iri) \
            if pbpko_bqm_is_class is not None else False
        chebi_bqb_is_class = self.get_chebi_iri(cv_terms) \
            if chemical_specific else None
        info_record = ParameterInfo(
            element.getId(),
            element.getName(),
            self.get_unit_string(element.getUnits()),
            cv_terms,
            pbpko_bqm_is_class,
            chebi_bqb_is_class,
            element.getConstant(),
            chemical_specific
        )
        return info_record

    def get_unit_string(
        self,
        unit_id: str
    ):
        """Tries to get the (UCUM) formated unit string of the specified element."""
        if unit_id is None:
            return ""
        unit_def = self.model.getUnitDefinition(unit_id)
        if unit_def is None:
            return ""
        return create_unit_string(unit_def)

    def get_pbko_class(
        self,
        cv_terms: list[ls.CVTerm]
    ):
        if cv_terms is not None:
            for term in cv_terms:
                if term.getQualifierType() == ls.MODEL_QUALIFIER \
                    and term.getModelQualifierType() is ls.BQM_IS:
                    num_resources = term.getNumResources()
                    for j in range(num_resources):
                        iri = term.getResourceURI(j)
                        if self.onto_checker.check_in_pbpko(iri):
                            return self.onto_checker.get_pbpko_class(iri)
        return None

    def get_chebi_iri(
        self,
        cv_terms: list[ls.CVTerm]
    ) -> str | None:
        if cv_terms is not None:
            for term in cv_terms:
                if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER \
                    and term.getBiologicalQualifierType() is ls.BQB_IS:
                    num_resources = term.getNumResources()
                    for j in range(num_resources):
                        iri = term.getResourceURI(j)
                        if self.onto_checker.check_in_chebi(iri):
                            return self.onto_checker.get_chebi_class(iri)
        return None

    def get_model_animal_species(self):
        result = []
        cv_terms = self.model.getCVTerms()
        if cv_terms is not None:
            for term in cv_terms:
                if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER \
                    and term.getBiologicalQualifierType() == ls.BQB_HAS_TAXON:
                    num_resources = term.getNumResources()
                    for j in range(num_resources):
                        iri = term.getResourceURI(j)
                        taxon = self.onto_checker.get_ncbitaxon_class(iri)
                        if taxon is not None:
                            result.append(taxon)
        return result

    def get_model_chemicals(self):
        result = []
        cv_terms = self.model.getCVTerms()
        if cv_terms is not None:
            for term in cv_terms:
                if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER \
                    and term.getBiologicalQualifierType() == ls.BQB_HAS_PROPERTY:
                    num_resources = term.getNumResources()
                    for j in range(num_resources):
                        iri = term.getResourceURI(j)
                        chemical = self.onto_checker.get_chebi_class(iri)
                        if chemical is not None:
                            result.append(chemical)
        return result

    def get_input_compartments(self) -> Dict[str, str]:
        input_compartments = {}
        for i in range(0, self.model.getNumCompartments()):
            compartment = self.model.getCompartment(i)
            cv_terms = self.get_cv_terms_by_type(compartment)
            if ls.BQM_IS in cv_terms:
                for term in cv_terms[ls.BQM_IS]:
                    if self.onto_checker.check_is_oral_input_compartment(term):
                        input_compartments.update({
                            compartment.getId() : "oral",
                        })
                    elif self.onto_checker.check_is_dermal_input_compartment(term):
                        input_compartments.update({
                            compartment.getId() : "dermal",
                        })
                    elif self.onto_checker.check_is_inhalation_input_compartment(term):
                        input_compartments.update({
                            compartment.getId() : "inhalation",
                        })
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

    def get_cv_terms_by_type(
        self,
        element: ls.SBase
    ):
        lookup = {}
        cv_terms = element.getCVTerms()
        for term in cv_terms:
            num_resources = term.getNumResources()
            for j in range(num_resources):
                if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER:
                    qualifier_type = term.getBiologicalQualifierType()
                elif term.getQualifierType() == ls.MODEL_QUALIFIER:
                    qualifier_type = term.getModelQualifierType()
                else:
                    assert_never(qualifier_type)
                if qualifier_type not in lookup:
                    lookup[qualifier_type] = []
                lookup[qualifier_type].append(term.getResourceURI(j))
        return lookup

class ModelInfo():
    def __init__(
        self,
        code: str,
        cv_terms = [],
        ncbi_bqb_has_taxon_terms = [],
        chebi_bqb_has_property_terms = [],
        input_routes = [],
        time_unit: str | None = None,
        amounts_unit: str | None = None,
        volume_unit: str | None = None,
        extent_unit: str | None = None,
        num_compartments: int = 0,
        num_species: int = 0,
        num_internal_parameters: int = 0,
        num_external_parameters: int = 0
    ):
        self.id = id
        self.code = code
        self.cv_terms = cv_terms
        self.ncbi_bqb_has_taxon_terms = ncbi_bqb_has_taxon_terms
        self.chebi_bqb_has_property_terms = chebi_bqb_has_property_terms
        self.input_routes = input_routes
        self.time_unit = time_unit
        self.amounts_unit = amounts_unit
        self.volume_unit = volume_unit
        self.extent_unit = extent_unit
        self.num_compartments = num_compartments
        self.num_species = num_species
        self.num_internal_parameters = num_internal_parameters
        self.num_external_parameters = num_external_parameters
        self.num_parameters = self.num_internal_parameters + self.num_external_parameters

    def get_input_routes_string(self):
        return f'{len(self.input_routes)} (' + str.join(", ", self.input_routes) + ')' if len(self.input_routes) > 0 else ""

class ElementInfo():
    def __init__(
        self,
        element_id: str,
        element_type: str,
        name: str,
        unit: str,
        cv_terms = [],
        pbpko_bqm_is_class = None
    ):
        self.id = element_id
        self.type = element_type
        self.name = name
        self.unit = unit
        self.cv_terms = cv_terms
        self.pbpko_bqm_is_class = pbpko_bqm_is_class

    def has_cv_terms(self):
        if not self.cv_terms:
            return False
        else:
            return True

    def has_unit(self):
        if not self.unit or self.unit == "":
            return False
        else:
            return True

    def is_valid(self):
        return self.has_unit() and self.has_cv_terms()

class ParameterInfo(ElementInfo):
    def __init__(
        self,
        id: str,
        name: str,
        unit: str,
        cv_terms = [],
        pbpko_bqm_is_class = None,
        chebi_bqb_is_class = None,
        is_constant = False,
        is_chemical_specific = False
    ):
        ElementInfo.__init__(self, id, 'parameter', name, unit, cv_terms, pbpko_bqm_is_class)
        self.is_constant = is_constant
        self.is_chemical_specific = is_chemical_specific
        self.chebi_bqb_is_class = chebi_bqb_is_class

class SpeciesInfo(ElementInfo):
    def __init__(
        self,
        id: str,
        name: str,
        compartment_id: str,
        unit: str,
        cv_terms = [],
        pbpko_bqm_is_class = None,
        chebi_bqb_is_class = None
    ):
        ElementInfo.__init__(self, id, 'species', name, unit, cv_terms, pbpko_bqm_is_class)
        self.compartment_id = compartment_id
        self.chebi_bqb_is_class = chebi_bqb_is_class

