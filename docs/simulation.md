# Simulation

The `simulation` module provides utilities to configure and run PBK model simulation scenarios and to compare model outputs against reference data.

Simulation configurations are described in YAML files of which the structure is described below. Main functions are:
- `load_config`: load a YAML simulation configuration file and return a `SimulationConfig` object.
- `run_config`: execute all scenarios for all model instances and write per-instance CSV outputs to `out_path`.
- `plot_simulation_results`: generate PNG plots for each scenario/output and, when available, compare to reference data.

## Example of use

The code below shows how to load a simulation config provided in the file `simulations.yaml`, run the simulations, and generate output plots, saving the results to the specified output directory `out/simulations`.

```python
from sbmlpbkutils import load_config, run_config, plot_simulation_results
import logging

logger = logging.getLogger('pbk-sim')
logging.basicConfig(level=logging.INFO)

# Load simulation config
config = load_config('simulations.yaml')

# Run simulation config
run_config(config, out_path='out/simulations', force_recompute=False, logger=logger)

# Generate plots
plot_simulation_results(config, out_path='out/simulations')
```

## YAML simulation configuration structure

A simulation configuration YAML file follows a simple hierarchical layout. The sections below mirror the YAML structure and show the expected fields and typical usage.

- **id** *[string]*
  - Configuration identifier.
- **label** *[string]*
  - Human-readable configuration label.
- **model_instances** *[list]*
  - List of model instances to run. Each item is an object with:
    - **id** *[string | required]*
    - **label** *[string | required]*
    - **model_path** *[string | required]* - Path to the SBML model file.
    - **param_file** *[string | optional]* - Path to a CSV with parameter values.
    - **target_mappings** *[mapping | optional]* - Map scenario output ids to model variable ids (e.g. `AGut: AGut`). Useful when a scenario output id differs from the actual variable id in the SBML model.
- **scenarios** *[list]*
  - List of scenarios to execute. Each scenario is an object with:
    - **id** *[string | required]*
    - **label** *[string | required]*
    - **time_unit** *[enum | required]* - Time unit used by the scenario (e.g., `HOUR`, `DAY`).
    - **amount_unit** *[enum | required]* - Amount unit used by the scenario (e.g., `MICROGRAMS`, `MILLIGRAMS`).
    - **duration** *[number | required]* - Duration of the scenario in `time_unit`.
    - **evaluation_resolution** *[number | required]* - Sampling resolution (higher values produce finer time sampling). Controls output resolution; for example, `evaluation_resolution: 24` with `duration: 10` (and `time_unit: DAY`) produces hourly samples over 10 days.
    - **initial_states** *[list | optional]* - List of `{ target, amount }` objects to set initial amounts.
    - **parameters** *[mapping | optional]* - List of parameter mappings specific for the scenario (overrides model instance parametrisations). For example, the mapping `BW: 75` could be used to set model parameter `BW` to a value of 75 for specific scenarios.
    - **dosing_events** *[list | optional]* - List of dosing event objects. Each dosing event commonly includes:
      - **type** *[enum | required]* - Type of dosing event. Options are `single_bolus`, `repeated_bolus`, `single_continuous`, `repeated_continuous`.
      - **target** *[string | required]* - Model variable to dose.
      - **amount** *[number | required]* - Dose amount, in scenario amount unit.
      - **adjustment** *[string | optional]* - Multiplicative adjustment of the dosing amount using specified model variable. For example, use `adjustment: BW` to specify bodyweight adjusted doses.
      - **time** *[number | required]* - Start time of dosing event(s) (in scenario time unit).
      - **duration** *[number | optional]* - For continuous dosing, duration of dosing events (in scenario time unit).
      - **interval** *[number | optional]* - For repeated dosing, time interval between dosing events (in scenario time unit).
      - **until** *[number | optional]* - For repeated dosing: end time for repetition.
    - **outputs** *[list | required]* - List of `{ id, label, output }` objects that specify which model variables to record and their display labels.
    - **reference_data** *[list | optional]* - List of reference series to compare against. Each item includes:
      - **id** *[string | required]*
      - **label** *[string | required]*
      - **file_path** *[string | required]* - Path to CSV file.
      - **series_type** *[enum | required]* - Type of reference data. Options are `CHECKPOINTS` for sparse datapoints, or `TIMELINE` for (high resolution) timeseries. Controls whether data is plotted as scatter plot (for checkpoints) or line plot (for timeline).
      - **time_unit** *[enum | required]* - Time unit of the reference file.
      - **mappings** *[mapping | optional]* - Map scenario output ids to colums of the reference CSV file. For example, the mapping `ALiver: QLiver` maps the reference column `QLiver` to output `ALiver`.

## Example YAML simulation configuration

The code below shows an example YAML configuration file. It runs a single scenario `oral_repeated` for two model instances (`model_1` and `model_2`). The scenario is defined for `10` days with an `evaluation_resolution` of `24` (e.g. 24 samples per day, resulting in hourly sampling across the duration). A repeated bolus dose of amount `1` μg/kg BW is applied to the `AGut` target at time `0` and repeated every `1` day. The simulation records two outputs (`ABlood` and `ALiver`) for each instance. The results are compared to reference series stored in the file `example/reference_data.csv` (with fields `QBlood` and `QLiver` mapping to outputs `ABlood` and `ALiver`).

```yaml
id: oral
label: oral
model_instances:
  - id: model_1
    label: model 1
    model_path: examples/model_1.sbml
    param_file: examples/params_model_1.csv
    target_mappings:
      AGut: AGut
      ABlood: ABlood
  - id: model_2
    label: model 2
    model_path: examples/model_2.sbml
    param_file: examples/params_model_2.csv
    target_mappings:
      AGut: AGut
      ABlood: ABlood

scenarios:
  - id: oral_repeated
    label: Oral repeated dose
    time_unit: DAY
    amount_unit: MICROGRAMS
    duration: 10
    evaluation_resolution: 24
    parameters:
        BW: 70
    dosing_events:
      - type: repeated_bolus
        target: AGut
        amount: 1
        adjustment: BW
        time: 0
        interval: 1
    outputs:
      - id: ABlood
        label: Amount in blood
        output: ABlood
      - id: ALiver
        label: Amount in liver
        output: ALiver
    reference_data:
      - id: reference
        label: reference
        file_path: example/reference_data.csv
        series_type: TIMELINE
        time_unit: DAY
        mappings:
          ABlood: QBlood
          ALiver: QLiver
```

## Parametrisation CSV files

Model parametrisations can be provided as CSV files containing the following fields:

- **IdModelInstance** *[string | optional]* - Identification code of the model parametrisation. Required when the file contains multiple parametrisations.
- **Parameter** *[string | required]* - Identifier of the model parameter.
- **Value** *[number | required]* - Value of the model parameter.

These CSV files can be created manually, but you can also generate parametrisation templates (instances and parameter tables) from an SBML model using `ParametrisationsTemplateGenerator`. The generator returns a tuple `(instances_df, params_df)` which you can export to CSV. The resulting parameter CSV can be used as `param_file` in a `model_instances` entry of your simulation YAML.

```python
from sbmlpbkutils import ParametrisationsTemplateGenerator
from libsbml import readSBML

# Read model
doc = readSBML('model.sbml')

# Generate templates (optionally supply model_instance_ids)
instances_df, params_df = ParametrisationsTemplateGenerator().generate(
    doc.getModel(),
    use_defaults=True,
    include_element_name=True,
    model_instance_ids=['MODEL1_PARAM']
)
instances_df.to_csv('instances.csv', index=False)
params_df.to_csv('parameters.csv', index=False)
```

## Notes and dependencies

- Requires `tellurium` (RoadRunner) to run SBML simulations, `matplotlib` for plotting, `pandas` for CSV I/O and `pyyaml` for YAML parsing.
- Large simulations or many instances will write multiple CSV and PNG files. Using `force_recompute=False` to reuse previously generated results, or `force_recompute=True` to regenerate results.
