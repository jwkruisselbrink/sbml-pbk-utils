from enum import Enum
from dataclasses import dataclass
from logging import Logger
import os
from typing import Dict, List
import libsbml as ls
import matplotlib.pyplot as plt
import pandas as pd
import tellurium as te
import yaml

from .simulation_units import (
    AmountUnit,
    TimeUnit,
    get_model_time_unit_alignment_factor,
    get_time_unit_alignment_factor,
    get_amount_unit_alignment_factor
)

class SeriesType(str, Enum):
    TIMELINE = "timeline"
    CHECKPOINTS = "checkpoints"

@dataclass
class DosingEvent:
    type: str
    target: str
    amount: float
    time: float
    duration: float | None = None
    interval: float | None = None
    until: float | None = None

@dataclass
class InitialState:
    target: str
    amount: float

@dataclass
class Output:
    id: str
    label: str
    output: str

@dataclass
class ReferenceData:
    id: str
    label: str
    file_path: str
    series_type: SeriesType
    time_unit: TimeUnit
    outputs: List[Output]

@dataclass
class Scenario:
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
    id: str
    label: str
    model_path: str
    param_file: str | None = None
    target_mappings: Dict[str, str] | None = None

@dataclass
class SimulationConfig:
    id: str
    label: str
    scenarios: List[Scenario]
    model_instances: List[ModelInstance]

@dataclass
class EventSpec:
    target: str
    trigger: str
    assignment: str

def events_single_continuous(
    event: DosingEvent,
    time_unit_multiplier: float,
    amount_unit_multiplier: float,
    target_mappings: Dict[str, str] | None
) -> List[EventSpec]:
    if event.duration is None:
        raise ValueError("duration is required for single continous dosing event")
    target = target_mappings[event.target] \
        if target_mappings is not None and event.target in target_mappings.keys() \
        else event.target
    time_start = time_unit_multiplier * event.time
    time_stop = time_unit_multiplier * (event.time + event.duration)
    amount = amount_unit_multiplier * event.amount
    return [
        EventSpec(target, f"(time >= {time_start})", f"{target} + {amount}"),
        EventSpec(target, f"(time >= {time_stop})", "0")
    ]

def repeated_continuous(
    event: DosingEvent,
    time_unit_multiplier: float,
    amount_unit_multiplier: float,
    target_mappings: Dict[str, str] | None
) -> List[EventSpec]:
    if event.duration is None:
        raise ValueError("duration is required for repeated continous dosing event")
    if event.until is None:
        raise ValueError("until is required for repeated continous dosing event")
    if event.interval is None:
        raise ValueError("interval is required for repeated continous dosing event")
    target = target_mappings[event.target] \
        if target_mappings is not None and event.target in target_mappings.keys() \
        else event.target
    time_start = time_unit_multiplier * event.time
    time_stop = time_unit_multiplier * (event.time + event.duration)
    interval = time_unit_multiplier * event.interval
    duration = time_unit_multiplier * event.duration
    until = time_unit_multiplier * event.until
    amount = amount_unit_multiplier * event.amount
    return [
        EventSpec(
            target = target,
            trigger = f"time >= {time_start} && time % {interval} > 0 && time < {until}",
            assignment = f"{target} + {amount}"
        ),
        EventSpec(
            target = target,
            trigger = f"time > {time_stop} && time % {interval} > {duration} && time <= {until} + {duration}",
            assignment = "0"
        )
    ]

def events_single_bolus(
    event: DosingEvent,
    time_unit_multiplier: float,
    amount_unit_multiplier: float,
    target_mappings: Dict[str, str] | None
) -> List[EventSpec]:
    target = target_mappings[event.target] \
        if target_mappings is not None and event.target in target_mappings.keys() \
        else event.target
    time = time_unit_multiplier * event.time
    amount = amount_unit_multiplier * event.amount
    trigger = f"(time >= {time})"
    assignment = f"{target} + {amount}"
    return [EventSpec(target, trigger, assignment)]

def events_repeated_bolus(
    event: DosingEvent,
    time_unit_multiplier: float,
    amount_unit_multiplier: float,
    target_mappings: Dict[str, str] | None
) -> List[EventSpec]:
    if event.interval is None:
        raise ValueError("interval is required for repeated_bolus")
    if event.until is None:
        raise ValueError("until is required for repeated_bolus")
    target = target_mappings[event.target] \
        if target_mappings is not None and event.target in target_mappings.keys() \
        else event.target
    time = time_unit_multiplier * event.time
    interval = time_unit_multiplier * event.interval
    until = time_unit_multiplier * event.until
    amount = amount_unit_multiplier * event.amount
    trigger = f"time >= {time} && time % {interval} == 0 && time < {until}"
    assignment = f"{target} + {amount}"
    return [EventSpec(target, trigger, assignment)]

def dosing_events_to_eventspecs(
    event: DosingEvent,
    time_unit_multiplier: float,
    amount_unit_multiplier: float,
    target_mappings: Dict[str, str] | None
) -> List[EventSpec]:
    if event.type == "single_bolus":
        return events_single_bolus(
            event,
            time_unit_multiplier,
            amount_unit_multiplier,
            target_mappings
        )
    elif event.type == "repeated_bolus":
        return events_repeated_bolus(
            event,
            time_unit_multiplier,
            amount_unit_multiplier,
            target_mappings
        )
    elif event.type == "single_continuous":
        return events_single_continuous(
            event,
            time_unit_multiplier,
            amount_unit_multiplier,
            target_mappings
        )
    elif event.type == "repeated_continuous":
        return repeated_continuous(
            event,
            time_unit_multiplier,
            amount_unit_multiplier,
            target_mappings
        )
    else:
        raise ValueError(f"Unknown dose_type: {event.type}")

def load_config(path: str) -> SimulationConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    model_instances = [
        ModelInstance(**mi)
        for mi in data["model_instances"]
    ]

    scenarios = []
    for s in data["scenarios"]:
        dosing_events = ([DosingEvent(**e) for e in s["dosing_events"]]
            if "dosing_events" in s.keys() else None)
        initial_states = ([InitialState(**e) for e in s["initial_states"]]
            if "initial_states" in s.keys() else None)
        outputs = [Output(**c) for c in s["outputs"]]
        reference_data = []
        if 'reference_data' in s.keys():
            for r in s['reference_data']:
                reference_series = ReferenceData(
                    id = r['id'],
                    label = r['label'],
                    file_path = r['file_path'],
                    series_type = SeriesType[r['series_type']],
                    time_unit = TimeUnit[r['time_unit']],
                    outputs = [Output(**c) for c in r['outputs']]
                )
                reference_data.append(reference_series)

        scenarios.append(
            Scenario(
                id=s["id"],
                label=s["label"],
                duration=s["duration"],
                evaluation_resolution=s["evaluation_resolution"],
                initial_states=initial_states,
                dosing_events=dosing_events,
                outputs=outputs,
                reference_data=reference_data,
                time_unit=TimeUnit[s["time_unit"]],
                amount_unit=AmountUnit[s["amount_unit"]],
            )
        )

    return SimulationConfig(
        id=data["id"],
        label=data["label"],
        model_instances=model_instances,
        scenarios=scenarios
    )

def run_config(
    config: SimulationConfig,
    out_path: str,
    force_recompute: bool,
    logger: Logger
):
    for scenario in config.scenarios:
        for instance in config.model_instances:
            # Simulation output csv file
            logger.info("Running scenario %s for instance %s", scenario.id, instance.id)
            out_file = os.path.join(out_path, f"{scenario.id}-{instance.id}.csv")
            run_scenario(
                instance,
                scenario,
                out_file,
                force_recompute,
                logger
            )

def plot_simulation_results(
    config: SimulationConfig,
    out_path: str
):
    for scenario in config.scenarios:
        # Plot combined instances scenario results
        plot_scenario_results(
            config.model_instances,
            scenario,
            out_path
        )

def run_scenario(
    instance: ModelInstance,
    scenario: Scenario,
    out_file: str,
    force_recompute: bool,
    logger: Logger
):
    # Skip if output already available and no forced recalculation
    if os.path.exists(out_file) and not force_recompute:
        logger.info("Skipping scenario %s: results already available", scenario.id)
        return

    # Load the model
    sbml_file = instance.model_path
    ls_document = ls.readSBML(sbml_file)
    ls_model = ls_document.getModel()
    rr_model = te.loadSBMLModel(sbml_file)

    # Simulation time and amount unit alignment
    time_unit_multiplier = get_model_time_unit_alignment_factor(ls_model, scenario.time_unit)
    amount_unit_multiplier = get_amount_unit_alignment_factor(ls_model, scenario.amount_unit)

    # Set initial amounts according to scenario
    if scenario.initial_states is not None:
        for item in scenario.initial_states:
            target = (instance.target_mappings[item.target]
                if instance.target_mappings is not None
                    and item.target in instance.target_mappings.keys()
                else item.target
            )
            amount = amount_unit_multiplier * item.amount
            logger.info(f"- Initial amount in {target}: {amount}")
            rr_model.setInitAmount(target, amount)

    # If the scenario has dosing event definitions
    if scenario.dosing_events is not None:

        # Get events from scenario
        event_specs = create_rr_events(
            scenario.dosing_events,
            time_unit_multiplier,
            amount_unit_multiplier,
            instance.target_mappings
        )

        # Set events
        event_count = 0
        for ev in event_specs:
            event_count += 1
            eid = f"ev_{event_count}"
            rr_model.addEvent(eid, False, ev.trigger, False)
            rr_model.addEventAssignment(eid, ev.target, ev.assignment, False)
        rr_model.regenerateModel(True, True)

    # Set instance parametrisation
    if instance.param_file is not None:
        load_parametrisation(rr_model, instance.param_file)

    # Define the output selections
    output_selections = set(
        instance.target_mappings.get(output.id, output.id)
            if instance.target_mappings is not None else output.id
        for output in scenario.outputs
    )
    selections = ['time'] + list(output_selections)

    # Determine duration and steps
    duration = int(scenario.duration * time_unit_multiplier)
    evaluation_steps = int(scenario.evaluation_resolution * duration / time_unit_multiplier) + 1

    logger.info("- Time unit multiplier: %s", time_unit_multiplier)
    logger.info("- Amount unit multiplier: %s", amount_unit_multiplier)
    logger.info("- Duration: %s", duration)
    logger.info("- Steps: %s", evaluation_steps)

    # Simulate the PBPK model
    results = rr_model.simulate(0, duration, evaluation_steps, selections)

    # Create output folder if not exists
    os.makedirs(os.path.dirname(out_file), exist_ok=True)

    # Write results file
    df = pd.DataFrame(results, columns=selections)

    # Align output times and amounts to target units
    df['time'] = df['time'].apply(lambda v: v / time_unit_multiplier)
    for output in output_selections:
        df[output] = df[output].apply(lambda v: v / amount_unit_multiplier)
    df.to_csv(out_file, index=False)

def plot_scenario_results(
    instances: list[ModelInstance],
    scenario: Scenario,
    out_path: str
):
    # Line and marker styles
    linestyles = ['-', '--', '-.', ':']
    markers = ['x', 'o', 's', '*', '^', 'v', 'p', '.']

    # Iterate over outputs
    for output in scenario.outputs:
        # Create figure
        fig, ax = plt.subplots(figsize=(7, 5))

        # Loop over instance results and plot
        # Cycle through a small set of linestyles so multiple instances are
        # visually distinguishable even when colors are similar.
        for idx, instance in enumerate(instances):
            # Get instance scenario output file
            out_file = os.path.join(out_path, f"{scenario.id}-{instance.id}.csv")
            output_df = pd.read_csv(out_file, skipinitialspace=True)

            # Extract time and output variable from output
            times = output_df['time'].to_numpy(dtype=float)
            output_id = instance.target_mappings.get(output.id, output.id) \
                if instance.target_mappings is not None else output.id
            values = output_df[output_id].to_numpy(dtype=float)

            # Plot time series
            linestyle = linestyles[idx % len(linestyles)]
            ax.plot(times, values, linewidth=1, linestyle=linestyle, label=instance.label)

        # Plot reference data/series
        if scenario.reference_data:
            for idx, item in enumerate(scenario.reference_data):
                reference_series = [o for o in item.outputs if o.output == output.id]
                time_unit_multiplier = get_time_unit_alignment_factor(
                    item.time_unit,
                    scenario.time_unit
                )
                for series in reference_series:
                    # Get instance scenario output file
                    reference_df = pd.read_csv(item.file_path, skipinitialspace=True)

                    # Extract time and output variable from output
                    times = reference_df['time'].apply(lambda v: v / time_unit_multiplier)
                    values = reference_df[series.id].to_numpy(dtype=float)

                    if item.series_type == SeriesType.CHECKPOINTS:
                        # Plot points
                        marker = markers[idx % len(linestyles)]
                        ax.scatter(times, values, marker=marker, label=item.label)
                    else:
                        # Plot lines
                        linestyle = linestyles[(idx + len(scenario.outputs)) % len(linestyles)]
                        ax.plot(
                            times,
                            values,
                            linewidth=1,
                            linestyle=linestyle,
                            label=item.label
                        )

        # Set plot layout
        ax.set_xlabel(f'Time ({str(scenario.time_unit)})', fontsize=12, fontweight='bold')
        ax.set_ylabel(f'{output.label} ({str(scenario.amount_unit)})', fontsize=12, fontweight='bold')
        ax.set_title(f'{scenario.label} - {output.label}', fontsize=14)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

        # Set output file
        out_file = os.path.join(out_path, f"{scenario.id}-{output.id}.png")
        plt.tight_layout()
        plt.legend()
        plt.savefig(out_file)
        plt.close()

def create_rr_events(
    events: List[DosingEvent],
    time_unit_multiplier: float,
    amount_unit_multiplier: float,
    target_mappings: Dict[str, str] | None
) -> List[EventSpec]:
    out: List[EventSpec] = []
    for e in events:
        out.extend(dosing_events_to_eventspecs(
            e,
            time_unit_multiplier,
            amount_unit_multiplier,
            target_mappings
        ))
    return out

def load_parametrisation(model, filename):
    df = pd.read_csv(filename, skipinitialspace=True)
    df['Value'] = df['Value'].astype(float)
    for index, row in df.iterrows():
        model[str(row['Parameter'])] = row['Value']
