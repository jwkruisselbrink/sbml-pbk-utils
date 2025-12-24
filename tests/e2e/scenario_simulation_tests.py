import unittest
import os
import logging
from parameterized import parameterized

from sbmlpbkutils import run_config, load_config, plot_simulation_results

__test_outputs_path__ = './tests/__testoutputs__'
__test_scenarios_path__ = './tests/resources/scenarios/'

class ScenarioSimulationTests(unittest.TestCase):

    @parameterized.expand([
        ("oral.yaml")
    ])
    def test_generate_report(self, filename):
        file_path = os.path.join(__test_scenarios_path__, filename)
        # Load config
        config = load_config(file_path)

        # Create output directory if it does not exist
        out_path = os.path.join(__test_outputs_path__, 'scenarios', config.id)

        # Ensure output path
        os.makedirs(out_path, exist_ok=True)

        # Run simulations
        logger = _create_console_logger()
        run_config(
            config = config,
            out_path = out_path,
            force_recompute = True,
            logger = logger
        )

        # Run simulations
        plot_simulation_results(
            config = config,
            out_path = out_path
        )

def _create_console_logger() -> logging.Logger:
    # Configure logger for formatted console output
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    if not logger.handlers:
        logger.addHandler(handler)
    return logger
