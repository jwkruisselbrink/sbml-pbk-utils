"""Methods for running PBK model simulation scenarios.

This module provides methods for running PBK model simulation
scenarios, plot results and compare model outputs against
reference series.
"""

from logging import Logger
import os
from typing import Dict, List
import libsbml as ls
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tellurium as te
import yaml

from .units import (
    AmountUnit,
    TimeUnit,
    get_time_unit_alignment_factor,
    get_model_time_unit_alignment_factor,
    get_amount_unit_alignment_factor
)

from .definitions import (
    SeriesType,
    DosingEvent,
    InitialState,
    Output,
    ReferenceData,
    Scenario,
    ModelInstance,
    SimulationConfig,
    EventSpec
)

def load_config(path: str) -> SimulationConfig:
    """Load a YAML simulation configuration and return a SimulationConfig.

    The YAML should contain `model_instances` and `scenarios` sections that map
    onto the dataclasses defined in this module.
    """
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
    """Run all scenarios in a configuration for all model instances.

    For each scenario-instance pair a CSV output file named
    `{scenario.id}_{instance.id}.csv` is written into `out_path`.
    """
    for scenario in config.scenarios:
        for instance in config.model_instances:
            # Simulation output csv file
            logger.info("Running scenario %s for instance %s", scenario.id, instance.id)
            out_file = os.path.join(out_path, f"{scenario.id}_{instance.id}.csv")
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
    """Generate plots for all scenarios in a configuration.

    Writes PNG files for each scenario and output variable into `out_path`.
    """
    for scenario in config.scenarios:
        # Plot combined instances scenario results
        plot_scenario_results(
            config.model_instances,
            scenario,
            out_path
        )

        if scenario.reference_data:
            plot_scenario_differences(
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
    """Execute a single scenario for a model instance and save results.

    Loads the SBML model, applies initial states, dosing events and any
    parameter file, runs the simulation and writes a CSV with time and
    selected outputs.
    """
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

def load_parametrisation(model, filename):
    """Load parameter values from a CSV file into a roadrunner model.

    The CSV is expected to have columns `Parameter` and `Value`.
    """
    df = pd.read_csv(filename, skipinitialspace=True)
    df['Value'] = df['Value'].astype(float)
    for (_, row) in df.iterrows():
        model[str(row['Parameter'])] = row['Value']

def plot_scenario_results(
    instances: list[ModelInstance],
    scenario: Scenario,
    out_path: str
):
    """Plot time series results for a scenario across model instances.

    Reads per-instance CSV results from `out_path` and writes PNG files for
    each configured `Output` in the scenario.
    """
    # Line and marker styles
    linestyles = ['-', '--', '-.', ':']
    markers = ['x', 'o', 's', '*', '^', 'v', 'p', '.']

    # Iterate over outputs
    for output in scenario.outputs:
        # Create figure
        (_, ax) = plt.subplots(figsize=(7, 5))

        # Loop over instance results and plot
        # Cycle through a small set of linestyles so multiple instances are
        # visually distinguishable even when colors are similar.
        for idx, instance in enumerate(instances):
            # Get instance scenario output file
            out_file = os.path.join(out_path, f"{scenario.id}_{instance.id}.csv")
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
        out_file = os.path.join(out_path, f"{scenario.id}_{output.id}.png")
        plt.tight_layout()
        plt.legend()
        plt.savefig(out_file)
        plt.close()

def plot_scenario_differences(
    instances: list[ModelInstance],
    scenario: Scenario,
    out_path: str
):
    """Compare instance results with reference data and plot differences.

    For each output that has reference data, this function:
    - loads instance results and reference series,
    - aligns reference times to the scenario time unit,
    - interpolates model results to reference time points,
    - plots model series, reference points and a residual subplot, and
    - writes a PNG file named ``{scenario.id}_{output.id}_diff.png`` in ``out_path``.
    """

    linestyles = ['-', '--', '-.', ':']
    markers = ['x', 'o', 's', '*', '^', 'v', 'p', '.']

    for output in scenario.outputs:
        # Collect reference series items that include this output
        ref_items = []
        if scenario.reference_data:
            for item in scenario.reference_data:
                reference_series = [o for o in item.outputs if o.output == output.id]
                if reference_series:
                    ref_items.append((item, reference_series))

        if not ref_items:
            # No reference data for this output, skip
            continue

        # Create figure with two subplots: series and residuals at reference points
        (_, (ax_series, ax_resid)) = plt.subplots(
            nrows = 2,
            ncols = 1,
            figsize = (8, 8),
            gridspec_kw={"height_ratios": [3, 1]}
        )

        # Plot model instance series
        for idx, instance in enumerate(instances):
            out_file = os.path.join(out_path, f"{scenario.id}_{instance.id}.csv")
            output_df = pd.read_csv(out_file, skipinitialspace=True)
            times = output_df['time'].to_numpy(dtype=float)
            output_id = (instance.target_mappings.get(output.id, output.id)
                if instance.target_mappings is not None else output.id)
            values = output_df[output_id].to_numpy(dtype=float)
            linestyle = linestyles[idx % len(linestyles)]
            ax_series.plot(times, values, linestyle=linestyle, linewidth=1, label=instance.label)

        # For each reference item, compute stats and plot reference points
        diffs_rows = []
        for r_idx, (item, series_list) in enumerate(ref_items):
            reference_df = pd.read_csv(item.file_path, skipinitialspace=True)

            # Align times using same approach as existing plotting
            time_unit_multiplier = get_time_unit_alignment_factor(item.time_unit, scenario.time_unit)
            ref_times = reference_df['time'].apply(lambda v: v / time_unit_multiplier).to_numpy(dtype=float)

            for series in series_list:
                ref_values = reference_df[series.id].to_numpy(dtype=float)

                # Plot reference points
                if item.series_type == SeriesType.CHECKPOINTS:
                    # Plot points
                    ax_series.scatter(
                        ref_times,
                        ref_values,
                        marker=markers[r_idx % len(markers)],
                        label=f"{item.label}"
                    )
                else:
                    # Plot lines
                    linestyle = linestyles[(r_idx + len(scenario.outputs)) % len(linestyles)]
                    ax_series.plot(
                        ref_times,
                        ref_values,
                        linewidth=1,
                        linestyle=linestyle,
                        label=f"{item.label}"
                    )

                # Compute per-instance statistics at reference points
                for idx, instance in enumerate(instances):
                    out_file = os.path.join(out_path, f"{scenario.id}_{instance.id}.csv")
                    output_df = pd.read_csv(out_file, skipinitialspace=True)
                    model_times = output_df['time'].to_numpy(dtype=float)
                    model_values = output_df[instance.target_mappings.get(output.id, output.id) if instance.target_mappings is not None else output.id].to_numpy(dtype=float)

                    # interpolate model to reference times
                    interp_vals = np.interp(ref_times, model_times, model_values)

                    residuals = interp_vals - ref_values

                    # Add residual points to residual subplot
                    if item.series_type == SeriesType.CHECKPOINTS:
                        marker = markers[idx % len(markers)]
                        ax_resid.scatter(
                            ref_times,
                            residuals,
                            marker=marker,
                            s=20,
                            label=f"{instance.label}"
                        )
                    else:
                        # Plot lines
                        marker = markers[idx % len(markers)] if len(ref_times) < 15 else None
                        linestyle = linestyles[(idx + len(scenario.outputs)) % len(linestyles)]
                        ax_resid.plot(
                            ref_times,
                            residuals,
                            linewidth=1,
                            marker=marker,
                            linestyle=linestyle,
                            label=f"{instance.label}"
                        )

                    # Append detailed diffs for CSV
                    for t, mval, rval, res in zip(ref_times, interp_vals, ref_values, residuals):
                        abs_diff = abs(res)
                        rel_diff = (res / rval) if rval != 0 else float('nan')
                        diffs_rows.append({
                            'scenario': scenario.id,
                            'output': output.id,
                            'reference_label': item.label,
                            'reference_series': series.id,
                            'time': t,
                            'instance': instance.id,
                            'instance_label': instance.label,
                            'model_value': mval,
                            'ref_value': rval,
                            'residual': res,
                            'abs_diff': abs_diff,
                            'rel_diff': rel_diff
                        })

        # Layout and labels
        ax_series.set_xlabel(f'Time ({str(scenario.time_unit)})')
        ax_series.set_ylabel(f'{output.label} ({str(scenario.amount_unit)})')
        ax_series.set_title(f'{scenario.label} - {output.label} (model vs reference)')
        ax_series.grid(True, alpha=0.3, linestyle='--')
        ax_series.legend()

        ax_resid.set_xlabel(f'Time ({str(scenario.time_unit)})')
        ax_resid.set_ylabel('Residual (model - ref)')
        ax_resid.grid(True, alpha=0.3, linestyle='--')
        ax_resid.legend()

        out_file = os.path.join(out_path, f"{scenario.id}_{output.id}_diff.png")
        plt.tight_layout()
        plt.savefig(out_file)
        plt.close()

        # Write detailed diffs and summary CSVs
        if diffs_rows:
            diffs_df = pd.DataFrame(diffs_rows)
            diffs_csv = os.path.join(out_path, f"{scenario.id}_{output.id}_diffs.csv")
            diffs_df.to_csv(diffs_csv, index=False)

def create_rr_events(
    events: List[DosingEvent],
    time_unit_multiplier: float,
    amount_unit_multiplier: float,
    target_mappings: Dict[str, str] | None
) -> List[EventSpec]:
    """Convert a list of dosing events into EventSpec objects."""
    out: List[EventSpec] = []
    for e in events:
        out.extend(dosing_events_to_eventspecs(
            e,
            time_unit_multiplier,
            amount_unit_multiplier,
            target_mappings
        ))
    return out

def events_single_continuous(
    event: DosingEvent,
    time_unit_multiplier: float,
    amount_unit_multiplier: float,
    target_mappings: Dict[str, str] | None
) -> List[EventSpec]:
    """Create event specs for a single continuous dosing event.

    Returns a pair of events that start the infusion and stop it after
    the event duration. Raises if `duration` is not provided.
    """
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
    """Create event specs for a repeated continuous dosing schedule.

    Returns a list of event specs implementing repeated continuous dose pulses.
    """
    if event.duration is None:
        raise ValueError("duration is required for repeated continous dosing event")
    if event.interval is None:
        raise ValueError("interval is required for repeated continous dosing event")
    target = (target_mappings[event.target]
        if target_mappings is not None and event.target in target_mappings.keys()
        else event.target)
    time_start = time_unit_multiplier * event.time
    time_stop = time_unit_multiplier * (event.time + event.duration)
    interval = time_unit_multiplier * event.interval
    duration = time_unit_multiplier * event.duration
    until = time_unit_multiplier * event.until if event.until else None
    amount = amount_unit_multiplier * event.amount
    return [
        EventSpec(
            target = target,
            trigger = (
                f"time >= {time_start} && time % {interval} > 0 && time < {until}"
                if until else f"time >= {time_start} && time % {interval} > 0"
            ),
            assignment = f"{target} + {amount}"
        ),
        EventSpec(
            target = target,
            trigger = (
                f"time > {time_stop} && time % {interval} > {duration} && time <= {until + duration}"
                if until else f"time > {time_stop} && time % {interval} > {duration}"
            ),
            assignment = "0"
        )
    ]

def events_single_bolus(
    event: DosingEvent,
    time_unit_multiplier: float,
    amount_unit_multiplier: float,
    target_mappings: Dict[str, str] | None
) -> List[EventSpec]:
    """Create an event spec for a single bolus dose.

    Produces a single instantaneous event that adds `amount` to the target
    at the specified `time`.
    """
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
    """Create event specs for repeated bolus dosing.

    Returns a repeated bolus event spec that triggers on the configured repeat times.
    """
    if event.interval is None:
        raise ValueError("interval is required for repeated_bolus")
    target = (target_mappings[event.target]
        if target_mappings is not None and event.target in target_mappings.keys()
        else event.target)
    time = time_unit_multiplier * event.time
    interval = time_unit_multiplier * event.interval
    until = time_unit_multiplier * event.until if event.until else None
    amount = amount_unit_multiplier * event.amount
    trigger = (f"time >= {time} && time % {interval} == 0 && time < {until}"
        if until else f"time >= {time} && time % {interval} == 0"
    )
    assignment = f"{target} + {amount}"
    return [EventSpec(target, trigger, assignment)]

def dosing_events_to_eventspecs(
    event: DosingEvent,
    time_unit_multiplier: float,
    amount_unit_multiplier: float,
    target_mappings: Dict[str, str] | None
) -> List[EventSpec]:
    """Dispatch helper: convert a dosing event definition into EventSpec(s).

    Routes by `event.type` to the appropriate generator function.
    """
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
