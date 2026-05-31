"""Methods for running PBK model simulation scenarios.

This module provides methods for running PBK model simulation
scenarios, plot results and compare model outputs against
reference series.
"""

from logging import Logger
import os
import re
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
    DistributionParameter,
    InitialState,
    Output,
    ReferenceData,
    Scenario,
    ModelInstance,
    SimulationConfig,
    EventSpec
)

def _parse_param_value(value) -> float | DistributionParameter:
    """Convert a raw YAML parameter value into a float or DistributionParameter."""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dict):
        return DistributionParameter(
            distribution=value["distribution"],
            min=value.get("min", None),
            max=value.get("max", None),
            mu=value.get("mu", None),
            sigma=value.get("sigma", None),
            value=value.get("value", None),
        )
    raise TypeError(f"Unexpected parameter type: {type(value).__name__}")


def _parse_stan_distribution(dist_str: str) -> DistributionParameter:
    """Parse a Stan-notation distribution string.

    Accepted formats::

        uniform(min, max)
        lognormal(mu, sigma)
        normal(mu, sigma)
        constant(value)

    """
    dist_str = dist_str.strip()
    match = re.match(r'(\w+)\s*\(([^)]+)\)', dist_str)
    if not match:
        raise ValueError(f"Invalid Stan distribution string: {dist_str!r}")
    dist_name = match.group(1)
    try:
        args = [float(a.strip()) for a in match.group(2).split(',')]
    except ValueError as e:
        raise ValueError(
            f"Could not parse arguments in {dist_str!r}: {e}"
        ) from e

    if dist_name == "uniform":
        if len(args) != 2:
            raise ValueError(
                f"uniform requires 2 arguments, got {len(args)} in {dist_str!r}"
            )
        return DistributionParameter(distribution="uniform", min=args[0], max=args[1])
    elif dist_name == "lognormal":
        if len(args) != 2:
            raise ValueError(
                f"lognormal requires 2 arguments, got {len(args)} in {dist_str!r}"
            )
        return DistributionParameter(distribution="lognormal", mu=args[0], sigma=args[1])
    elif dist_name == "normal":
        if len(args) != 2:
            raise ValueError(
                f"normal requires 2 arguments, got {len(args)} in {dist_str!r}"
            )
        return DistributionParameter(distribution="normal", mu=args[0], sigma=args[1])
    elif dist_name == "constant":
        if len(args) != 1:
            raise ValueError(
                f"constant requires 1 argument, got {len(args)} in {dist_str!r}"
            )
        return DistributionParameter(distribution="constant", value=args[0])
    else:
        raise ValueError(f"Unknown distribution in {dist_str!r}: {dist_name}")


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
                    mappings = r['mappings']
                )
                reference_data.append(reference_series)

        raw_params = s['parameters'] if 'parameters' in s.keys() else None
        parameters = None
        if raw_params:
            parameters = {k: _parse_param_value(v) for k, v in raw_params.items()}

        scenarios.append(
            Scenario(
                id=s['id'],
                label=s['label'],
                duration=s['duration'],
                evaluation_resolution=s['evaluation_resolution'],
                initial_states=initial_states,
                parameters=parameters,
                dosing_events=dosing_events,
                outputs=outputs,
                reference_data=reference_data,
                time_unit=TimeUnit[s['time_unit']],
                amount_unit=AmountUnit[s['amount_unit']],
                molar_mass=s['molar_mass'] if 'molar_mass' in s.keys() else None,
                n_simulations=s.get('n_simulations', 1),
                use_distributions=s.get('use_distributions', False),
            )
        )

    return SimulationConfig(
        id=data['id'],
        label=data['label'],
        model_instances=model_instances,
        scenarios=scenarios
    )

def _sample_parameter(
    param_def: DistributionParameter,
    rng: np.random.Generator,
) -> float:
    """Sample a concrete value from a ``DistributionParameter``."""
    # Sample from variability distribution
    if param_def.distribution == "uniform":
        return rng.uniform(param_def.min, param_def.max)
    elif param_def.distribution == "lognormal":
        return rng.lognormal(param_def.mu, param_def.sigma)
    elif param_def.distribution == "normal":
        return rng.normal(param_def.mu, param_def.sigma)
    elif param_def.distribution == "constant":
        return param_def.value
    else:
        raise ValueError(f"Unknown distribution: {param_def.distribution}")


def run_config(
    config: SimulationConfig,
    out_path: str,
    force_recompute: bool,
    logger: Logger,
    random_seed: int | None = None,
):
    """Run all scenarios in a configuration for all model instances.

    For each scenario-instance pair a CSV output file named
    `{scenario.id}_{instance.id}.csv` is written into ``out_path``.

    When *random_seed* is provided, distribution-based parameters are
    sampled deterministically from that seed, ensuring reproducible runs.
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
                logger,
                random_seed=random_seed,
            )

def plot_simulation_results(
    config: SimulationConfig,
    out_path: str,
    plot_reference_comparison: bool = True,
    combine_outputs: bool = False,
    ncols_combined: int = 4,
    show_legend: bool = True
):
    """Generate plots for all scenarios in a configuration.

    Writes PNG files for each scenario and output variable into `out_path`.
    """
    for scenario in config.scenarios:
        # Plot combined instances scenario results
        plot_scenario_results(
            config.model_instances,
            scenario,
            out_path,
            combine_outputs,
            ncols_combined,
            show_legend
        )

        if plot_reference_comparison and scenario.reference_data:
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
    logger: Logger,
    random_seed: int | None = None,
):
    """Execute a single scenario for a model instance and save results.

    Loads the SBML model, applies initial states, dosing events and any
    parameter file, runs the simulation and writes a CSV with time and
    selected outputs.

    When *random_seed* is provided, distribution-based parameters are
    sampled deterministically from that seed.

    When ``scenario.n_simulations > 1`` the simulation is run multiple
    times with fresh samples from distribution-based parameters.  The
    output CSV contains an ``iteration`` column.
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
    amount_unit_multiplier = get_amount_unit_alignment_factor(ls_model, scenario.amount_unit, scenario.molar_mass)

    # Set initial amounts according to scenario (persists through reset)
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

    # If the scenario has dosing event definitions (set once, persist through reset)
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

    # Define the output selections
    output_selections = []
    for output in scenario.outputs:
        if instance.target_mappings is not None and output.id in instance.target_mappings.keys():
            mapped = instance.target_mappings[output.id]
            if mapped is None:
                continue
            output_selections.append(mapped)
        else:
            output_selections.append(output.id)
    selections = ['time'] + output_selections

    # Determine duration and steps
    duration = int(scenario.duration * time_unit_multiplier)
    evaluation_steps = int(scenario.evaluation_resolution * duration / time_unit_multiplier) + 1

    logger.info("- Time unit multiplier: %s", time_unit_multiplier)
    logger.info("- Amount unit multiplier: %s", amount_unit_multiplier)
    logger.info("- Duration: %s", duration)
    logger.info("- Steps: %s", evaluation_steps)

    n_sim = scenario.n_simulations
    use_stochastic = scenario.use_distributions and n_sim > 1
    rng = np.random.default_rng(random_seed)

    def _run_one(reset_first: bool = False) -> pd.DataFrame:
        """Run a single simulation and return a DataFrame with time + outputs."""
        if reset_first:
            rr_model.reset()

        # Apply instance parametrisation (re-samples distributions each iteration)
        if instance.param_file is not None:
            load_parametrisation(
                rr_model,
                instance.param_file,
                sample_distributions=use_stochastic,
                rng=rng,
            )

        # Apply scenario parameters
        if scenario.parameters:
            for param, value in scenario.parameters.items():
                if isinstance(value, DistributionParameter):
                    if use_stochastic:
                        value = _sample_parameter(value, rng)
                    else:
                        if value.value is None:
                            raise ValueError(
                                f"Distribution parameter '{param}' has no 'value' field. "
                                "Set a fixed 'value' for deterministic mode, or enable "
                                "distribution sampling (use_distributions=True) with "
                                "n_simulations > 1."
                            )
                        value = value.value
                if instance.target_mappings is not None and param in instance.target_mappings.keys():
                    target = instance.target_mappings[param]
                    if target is None:
                        continue
                else:
                    target = param
                rr_model[target] = value

        # Simulate
        results = rr_model.simulate(0, duration, evaluation_steps, selections)
        df = pd.DataFrame(results, columns=selections)
        df['time'] = df['time'].apply(lambda v: v / time_unit_multiplier)
        for col in output_selections:
            df[col] = df[col].apply(lambda v: v / amount_unit_multiplier)
        return df

    # Create output folder if not exists
    os.makedirs(os.path.dirname(out_file), exist_ok=True)

    if n_sim <= 1:
        # Single run (no reset needed — model was just loaded)
        df = _run_one(reset_first=False)
        df.to_csv(out_file, index=False)
    else:
        # Multi-iteration Monte Carlo
        all_dfs = []
        for iter_idx in range(n_sim):
            df = _run_one(reset_first=(iter_idx > 0))
            df['iteration'] = iter_idx
            all_dfs.append(df)
        combined = pd.concat(all_dfs, ignore_index=True)
        cols = ['iteration'] + [c for c in combined.columns if c != 'iteration']
        combined.to_csv(out_file, index=False, columns=cols)

def _resolve_output_mapping(target_mappings: Dict[str, str | None] | None, output_id: str) -> str | None:
    """Resolve output ID through target mappings, returning None if mapped to None."""
    if target_mappings is not None and output_id in target_mappings.keys():
        mapped = target_mappings[output_id]
        return mapped if mapped is not None else None
    return output_id


def load_parametrisation(model, filename, sample_distributions=False, rng=None):
    """Load parameter values from a CSV file into a roadrunner model.

    The CSV is expected to have columns ``Parameter`` and ``Value``.
    When ``sample_distributions=True`` and an optional ``Distribution``
    column is present with Stan notation (e.g. ``uniform(60, 80)``,
    ``lognormal(0.0, 0.2)``, ``constant(0.05)``), the parameter is sampled
    from that distribution.  Requires *rng* when sampling distributions.
    Otherwise the ``Value`` column is used as a fixed constant.
    """
    df = pd.read_csv(filename, skipinitialspace=True)
    has_dist = "Distribution" in df.columns
    for (_, row) in df.iterrows():
        param_name = str(row["Parameter"])
        use_dist = (
            sample_distributions
            and has_dist
            and pd.notna(row.get("Distribution"))
            and str(row["Distribution"]).strip()
        )
        if use_dist:
            dist_spec = _parse_stan_distribution(str(row["Distribution"]))
            if rng is None:
                raise ValueError(
                    "rng argument required when sampling distributions"
                )
            value = _sample_parameter(dist_spec, rng)
        else:
            value = float(row["Value"])
        model[param_name] = value

def plot_scenario_results(
    instances: list[ModelInstance],
    scenario: Scenario,
    out_path: str,
    combine_outputs: bool = False,
    ncols_combined: int = 4,
    show_legend: bool = True
) -> None:
    """Plot time series results for a scenario across model instances.

    Reads per-instance CSV results from `out_path` and writes PNG files for
    each configured `Output` in the scenario.
    """
    # Line and marker styles
    linestyles = ['-', '--', '-.', ':']
    markers = ['x', 'o', 's', '*', '^', 'v', 'p', '.']

    outputs = scenario.outputs
    n_outputs = len(outputs)
    scenario_label = scenario.label if scenario.label else scenario.id

    # Figure setup for combined mode
    if combine_outputs:
        nrows = int(np.ceil(n_outputs / ncols_combined))
        fig, axes = plt.subplots(
            nrows=nrows,
            ncols=ncols_combined,
            figsize=(4 * ncols_combined, 3 * nrows),
            squeeze=False
        )
    else:
        fig = None
        axes = None
        nrows = 0

    # Iterate over outputs
    for out_idx, output in enumerate(outputs):

        if combine_outputs and axes is not None:
            # Create subplot
            row = out_idx // ncols_combined
            col = out_idx % ncols_combined
            ax = axes[row][col]
        else:
            # Create figure
            _, ax = plt.subplots(figsize=(7, 5))

        # Loop over instance results and plot
        # Cycle through a small set of linestyles so multiple instances are
        # visually distinguishable even when colors are similar.
        for idx, instance in enumerate(instances):
            # Get instance scenario output file
            out_file = os.path.join(out_path, f"{scenario.id}_{instance.id}.csv")
            output_df = pd.read_csv(out_file, skipinitialspace=True)

            # Extract time and output variable from output
            output_id = _resolve_output_mapping(instance.target_mappings, output.id)
            if output_id is None:
                continue

            color = f'C{idx}'

            if 'iteration' in output_df.columns:
                # Multi-iteration: plot median + 5th-95th percentile band
                grouped = output_df.groupby('time')[output_id]
                times = grouped.mean().index.to_numpy(dtype=float)
                median_vals = grouped.median().to_numpy(dtype=float)
                lower_vals = grouped.quantile(0.05).to_numpy(dtype=float)
                upper_vals = grouped.quantile(0.95).to_numpy(dtype=float)
                ax.plot(times, median_vals, linewidth=1.5, color=color, label=instance.label)
                ax.fill_between(times, lower_vals, upper_vals, alpha=0.2, color=color)
            else:
                # Single run: plot the raw trace
                times = output_df['time'].to_numpy(dtype=float)
                values = output_df[output_id].to_numpy(dtype=float)
                linestyle = linestyles[idx % len(linestyles)]
                ax.plot(times, values, linewidth=1, linestyle=linestyle, label=instance.label)

        # Plot reference data/series
        if scenario.reference_data:
            for idx, item in enumerate(scenario.reference_data):
                time_unit_multiplier = get_time_unit_alignment_factor(
                    item.time_unit,
                    scenario.time_unit
                )

                if output.id in item.mappings.keys():
                    ref_id = item.mappings[output.id]

                    # Get instance scenario output file
                    reference_df = pd.read_csv(item.file_path, skipinitialspace=True)

                    # Extract time and output variable from output
                    times = reference_df['time'].apply(lambda v: v / time_unit_multiplier)
                    values = reference_df[ref_id].to_numpy(dtype=float)

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
        output_label = output.label if output.label else output.id
        ax.set_xlabel(f'Time ({str(scenario.time_unit)})', fontsize=12, fontweight='bold')
        ax.set_ylabel(output_label, fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

        if not combine_outputs:
            ax.set_title(f'{scenario_label} - {output_label}', fontsize=14)
            out_file = os.path.join(out_path, f"{scenario.id}_{output.id}.png")
            ax.legend()
            plt.tight_layout()
            plt.savefig(out_file)
            plt.close()
        else:
            ax.set_title(f'{output_label}', fontsize=14)
            if show_legend:
                ax.legend()

    # Clean up empty axes and save combined figure
    if combine_outputs and fig is not None and axes is not None:
        for idx in range(n_outputs, nrows * ncols_combined):
            fig.delaxes(axes[idx // ncols_combined][idx % ncols_combined])

        fig.suptitle(scenario_label, fontsize=14)
        fig.tight_layout(rect=(0, 0, 1, 0.96))
        fig.savefig(os.path.join(out_path, f"{scenario.id}_combined_results.png"))
        plt.close(fig)

def plot_scenario_differences(
    instances: list[ModelInstance],
    scenario: Scenario,
    out_path: str
) -> None:
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
                if output.id in item.mappings.keys():
                    ref_id = item.mappings[output.id]
                    ref_items.append((item, ref_id))

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
            output_id = _resolve_output_mapping(instance.target_mappings, output.id)
            if output_id is None:
                continue

            color = f'C{idx}'

            if 'iteration' in output_df.columns:
                grouped = output_df.groupby('time')[output_id]
                times = grouped.mean().index.to_numpy(dtype=float)
                median_vals = grouped.median().to_numpy(dtype=float)
                lower_vals = grouped.quantile(0.05).to_numpy(dtype=float)
                upper_vals = grouped.quantile(0.95).to_numpy(dtype=float)
                ax_series.plot(times, median_vals, linewidth=1.5, color=color, label=instance.label)
                ax_series.fill_between(times, lower_vals, upper_vals, alpha=0.2, color=color)
            else:
                times = output_df['time'].to_numpy(dtype=float)
                values = output_df[output_id].to_numpy(dtype=float)
                linestyle = linestyles[idx % len(linestyles)]
                ax_series.plot(times, values, linestyle=linestyle, linewidth=1, label=instance.label)

        # For each reference item, compute stats and plot reference points
        diffs_rows = []
        for r_idx, (item, series_id) in enumerate(ref_items):
            reference_df = pd.read_csv(item.file_path, skipinitialspace=True)

            # Align times using same approach as existing plotting
            time_unit_multiplier = get_time_unit_alignment_factor(item.time_unit, scenario.time_unit)
            ref_times = reference_df['time'].apply(lambda v: v / time_unit_multiplier).to_numpy(dtype=float)

            # Get reference series values
            ref_values = reference_df[series_id].to_numpy(dtype=float)

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
                output_id = _resolve_output_mapping(instance.target_mappings, output.id)
                if output_id is None:
                    continue

                if 'iteration' in output_df.columns:
                    # Use median across iterations as the representative model value
                    model_values = output_df.groupby('time')[output_id].median().to_numpy(dtype=float)
                    model_times = output_df.groupby('time')['time'].first().to_numpy(dtype=float)
                else:
                    model_times = output_df['time'].to_numpy(dtype=float)
                    model_values = output_df[output_id].to_numpy(dtype=float)

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
                        'reference_series': series_id,
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
        ax_series.set_ylabel(f'{output.label}')
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
    adjustment = None
    if event.adjustment is not None:
        if target_mappings is not None and event.adjustment in target_mappings.keys():
            adjustment = target_mappings[event.adjustment]
        else:
            adjustment = event.adjustment
    trigger = f"(time >= {time})"
    assignment = f"{target} + {adjustment} * {amount}" if adjustment else f"{target} + {amount}"
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
    adjustment = None
    if event.adjustment is not None:
        if target_mappings is not None and event.adjustment in target_mappings.keys():
            adjustment = target_mappings[event.adjustment]
        else:
            adjustment = event.adjustment
    trigger = (f"time >= {time} && time % {interval} == 0 && time < {until}"
        if until else f"time >= {time} && time % {interval} == 0"
    )
    assignment = f"{target} + {adjustment} * {amount}" if adjustment else f"{target} + {amount}"
    return [EventSpec(target, trigger, assignment)]

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
    adjustment = None
    if event.adjustment is not None:
        if target_mappings is not None and event.adjustment in target_mappings.keys():
            adjustment = target_mappings[event.adjustment]
        else:
            adjustment = event.adjustment
    assignment = f"{target} + {adjustment} * {amount}" if adjustment else f"{target} + {amount}"
    return [
        EventSpec(target, f"(time >= {time_start})", assignment),
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
    adjustment = None
    if event.adjustment is not None:
        if target_mappings is not None and event.adjustment in target_mappings.keys():
            adjustment = target_mappings[event.adjustment]
        else:
            adjustment = event.adjustment
    assignment = f"{target} + {adjustment} * {amount}" if adjustment else f"{target} + {amount}"
    return [
        EventSpec(
            target = target,
            trigger = (
                f"time >= {time_start} && time % {interval} > {time_start} && time < {until}"
                if until else f"time >= {time_start} && time % {interval} > {time_start}"
            ),
            assignment = assignment
        ),
        EventSpec(
            target = target,
            trigger = (
                f"time > {time_stop} && time % {interval} > {time_stop} && time <= {until + duration}"
                if until else f"time > {time_stop} && time % {interval} > {time_stop}"
            ),
            assignment = "0"
        )
    ]
