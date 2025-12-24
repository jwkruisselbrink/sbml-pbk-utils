import unittest
import os
from parameterized import parameterized

from tests.helpers import create_console_logger
from tests.conf import TEST_OUTPUT_PATH, TEST_SCENARIOS_PATH
from sbmlpbkutils import run_config, load_config, plot_simulation_results

class ScenarioSimulationTests(unittest.TestCase):

    def setUp(self):
        self.out_path = os.path.join(TEST_OUTPUT_PATH, 'scenarios')
        os.makedirs(self.out_path, exist_ok=True)

    @parameterized.expand([
        ("oral.yaml")
    ])
    def test_simulation_scenarios(self, filename):
        # Get file path from filename
        file_path = os.path.join(TEST_SCENARIOS_PATH, filename)

        # Load config
        config = load_config(file_path)

        # Create output directory if it does not exist
        out_path = os.path.join(self.out_path, config.id)
        os.makedirs(out_path, exist_ok=True)

        # Run simulations
        logger = create_console_logger()
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


