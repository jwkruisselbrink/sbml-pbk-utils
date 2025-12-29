
"""Data structures for specification of PBK model simulation scenarios.

This module defines data structures for specification of simulation
scenarios.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List

from .units import (
    AmountUnit,
    TimeUnit,
)

class SeriesType(str, Enum):
    """Enumeration of ways reference series are represented in files.

    TIMELINE -- continuous series that should be plotted as lines.
    CHECKPOINTS -- discrete series that should be plotted as markers.
    """
    TIMELINE = "timeline"
    CHECKPOINTS = "checkpoints"

@dataclass
class DosingEvent:
    """Specification of a dosing event.

    Attributes:
        type: dosing type (e.g., 'single_bolus', 'repeated_continuous').
        target: model variable to dose (compartment/species id).
        amount: dose amount (in scenario units).
        time: start time for the dose (in scenario time unit).
        duration: duration for continuous doses (optional).
        interval: repeat interval for repeated doses (optional).
        until: last time to apply repeated doses (optional).
    """
    type: str
    target: str
    amount: float
    time: float
    duration: float | None = None
    interval: float | None = None
    until: float | None = None

@dataclass
class InitialState:
    """Initial amount for a target variable in a scenario.

    Attributes:
        target: model variable id.
        amount: initial amount (in scenario amount unit).
    """
    target: str
    amount: float

@dataclass
class Output:
    """Configuration for an output series to be saved or plotted.

    Attributes:
        id: unique identifier used in files and plots.
        label: human-readable label for plots.
        output: model variable id to extract values from.
    """
    id: str
    label: str
    output: str

@dataclass
class ReferenceData:
    """Metadata describing external reference series to compare against.

    Attributes:
        id: identifier of the series column in the reference file.
        label: label used for plotting/legends.
        file_path: path to CSV containing the reference series.
        series_type: representation style (timeline or checkpoints).
        time_unit: time unit of the reference data.
        outputs: list of Output entries describing available series columns.
    """
    id: str
    label: str
    file_path: str
    series_type: SeriesType
    time_unit: TimeUnit
    outputs: List[Output]

@dataclass
class Scenario:
    """Defines a simulation scenario.

    Contains durations, outputs to record, initial states and dosing events
    as well as unit information for time and amount used in the scenario.
    """
    id: str
    label: str
    duration: int
    evaluation_resolution: int
    initial_states: List[InitialState] | None
    dosing_events: List[DosingEvent] | None
    outputs: List[Output]
    reference_data: List[ReferenceData] | None
    time_unit: TimeUnit
    amount_unit: AmountUnit

@dataclass
class ModelInstance:
    """Represents a concrete model file and optional parameterisation.

    Attributes:
        id: unique instance id used in filenames.
        label: display label for plots and legends.
        model_path: path to SBML model file.
        param_file: optional CSV with parameter values to load.
        target_mappings: optional mapping from scenario outputs to model ids.
    """
    id: str
    label: str
    model_path: str
    param_file: str | None = None
    target_mappings: Dict[str, str] | None = None

@dataclass
class SimulationConfig:
    """Top-level configuration for a set of simulation runs.

    Attributes:
        id: configuration id.
        label: human-readable label.
        scenarios: list of scenarios to run.
        model_instances: list of model instances to execute scenarios on.
    """
    id: str
    label: str
    scenarios: List[Scenario]
    model_instances: List[ModelInstance]

@dataclass
class EventSpec:
    """Event specification in form of roadrunner event assignment.

    Attributes:
        target: model variable to be assigned.
        trigger: boolean expression string that triggers the event.
        assignment: expression to assign when triggered.
    """
    target: str
    trigger: str
    assignment: str
