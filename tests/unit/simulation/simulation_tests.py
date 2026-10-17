import logging
import os
import tempfile
import unittest

import pandas as pd

from tests.conf import TEST_MODELS_PATH
from sbmlpbkutils.simulation.definitions import (
    DosingEvent,
    EventSpec,
    ModelInstance,
    Output,
    Scenario,
)
from sbmlpbkutils.simulation.units import AmountUnit, TimeUnit
from sbmlpbkutils.simulation.simulation import (
    run_scenario,
    repeated_continuous,
    events_single_bolus,
    events_repeated_bolus,
    events_single_continuous,
    dosing_events_to_eventspecs,
    create_rr_events,
)

class RepeatedContinuousTests(unittest.TestCase):

    def test_basic_repeated_continuous(self):
        event = DosingEvent(
            type="repeated_continuous",
            target="X",
            amount=5.0,
            time=10.0,
            duration=2.0,
            interval=24.0,
        )
        specs = repeated_continuous(event, 1.0, 1.0, None)
        self.assertEqual(len(specs), 2)
        self.assertEqual(specs[0].target, "X")
        self.assertEqual(specs[0].trigger, "time >= 10.0 && time % 24.0 > 10.0")
        self.assertEqual(specs[0].assignment, "X + 5.0")
        self.assertEqual(specs[1].target, "X")
        self.assertEqual(specs[1].trigger, "time > 12.0 && time % 24.0 > 12.0")
        self.assertEqual(specs[1].assignment, "0")

    def test_repeated_continuous_with_until(self):
        event = DosingEvent(
            type="repeated_continuous",
            target="Y",
            amount=2.0,
            time=5.0,
            duration=1.5,
            interval=4.0,
            until=20.0,
        )
        specs = repeated_continuous(event, 1.0, 1.0, None)
        self.assertEqual(len(specs), 2)
        self.assertEqual(specs[0].trigger, "time >= 5.0 && time % 4.0 > 5.0 && time < 20.0")
        self.assertEqual(specs[1].trigger, "time > 6.5 && time % 4.0 > 6.5 && time <= 21.5")

    def test_repeated_continuous_with_target_mappings(self):
        event = DosingEvent(
            type="repeated_continuous",
            target="X",
            amount=3.0,
            time=0.0,
            duration=1.0,
            interval=5.0,
        )
        mappings = {"X": "comp_X"}
        specs = repeated_continuous(event, 1.0, 1.0, mappings)
        self.assertEqual(specs[0].target, "comp_X")
        self.assertEqual(specs[1].target, "comp_X")

    def test_repeated_continuous_with_adjustment(self):
        event = DosingEvent(
            type="repeated_continuous",
            target="X",
            amount=4.0,
            time=2.0,
            duration=3.0,
            interval=10.0,
            adjustment="BW",
        )
        specs = repeated_continuous(event, 1.0, 1.0, None)
        self.assertEqual(specs[0].assignment, "X + BW * 4.0")

    def test_repeated_continuous_with_adjustment_and_mappings(self):
        event = DosingEvent(
            type="repeated_continuous",
            target="X",
            amount=4.0,
            time=2.0,
            duration=3.0,
            interval=10.0,
            adjustment="BW",
        )
        mappings = {"X": "comp_X", "BW": "body_weight"}
        specs = repeated_continuous(event, 1.0, 1.0, mappings)
        self.assertEqual(specs[0].assignment, "comp_X + body_weight * 4.0")

    def test_repeated_continuous_with_unit_multipliers(self):
        event = DosingEvent(
            type="repeated_continuous",
            target="X",
            amount=1.0,
            time=1.0,
            duration=0.5,
            interval=2.0,
        )
        specs = repeated_continuous(event, 60.0, 1000.0, None)
        self.assertEqual(specs[0].trigger, "time >= 60.0 && time % 120.0 > 60.0")
        self.assertEqual(specs[1].trigger, "time > 90.0 && time % 120.0 > 90.0")
        self.assertEqual(specs[0].assignment, "X + 1000.0")

    def test_repeated_continuous_missing_duration_raises(self):
        event = DosingEvent(
            type="repeated_continuous",
            target="X",
            amount=1.0,
            time=0.0,
            interval=5.0,
        )
        with self.assertRaises(ValueError) as ctx:
            repeated_continuous(event, 1.0, 1.0, None)
        self.assertIn("duration", str(ctx.exception))

    def test_repeated_continuous_missing_interval_raises(self):
        event = DosingEvent(
            type="repeated_continuous",
            target="X",
            amount=1.0,
            time=0.0,
            duration=1.0,
        )
        with self.assertRaises(ValueError) as ctx:
            repeated_continuous(event, 1.0, 1.0, None)
        self.assertIn("interval", str(ctx.exception))

    def test_repeated_continuous_with_until_and_multipliers(self):
        event = DosingEvent(
            type="repeated_continuous",
            target="X",
            amount=1.0,
            time=1.0,
            duration=0.5,
            interval=2.0,
            until=10.0,
        )
        specs = repeated_continuous(event, 60.0, 1000.0, None)
        self.assertEqual(
            specs[0].trigger,
            "time >= 60.0 && time % 120.0 > 60.0 && time < 600.0"
        )
        self.assertEqual(
            specs[1].trigger,
            "time > 90.0 && time % 120.0 > 90.0 && time <= 630.0"
        )


class SingleBolusTests(unittest.TestCase):

    def test_basic_single_bolus(self):
        event = DosingEvent(
            type="single_bolus",
            target="X",
            amount=10.0,
            time=5.0,
        )
        specs = events_single_bolus(event, 1.0, 1.0, None)
        self.assertEqual(len(specs), 1)
        self.assertEqual(specs[0].target, "X")
        self.assertEqual(specs[0].trigger, "(time >= 5.0)")
        self.assertEqual(specs[0].assignment, "X + 10.0")

    def test_single_bolus_with_adjustment_and_mappings(self):
        event = DosingEvent(
            type="single_bolus",
            target="X",
            amount=5.0,
            time=2.0,
            adjustment="F",
        )
        mappings = {"X": "organ_X", "F": "bioavail"}
        specs = events_single_bolus(event, 1.0, 1.0, mappings)
        self.assertEqual(specs[0].target, "organ_X")
        self.assertEqual(specs[0].assignment, "organ_X + bioavail * 5.0")


class RepeatedBolusTests(unittest.TestCase):

    def test_basic_repeated_bolus(self):
        event = DosingEvent(
            type="repeated_bolus",
            target="X",
            amount=3.0,
            time=0.0,
            interval=6.0,
        )
        specs = events_repeated_bolus(event, 1.0, 1.0, None)
        self.assertEqual(len(specs), 1)
        self.assertEqual(specs[0].trigger, "time >= 0.0 && time % 6.0 == 0")

    def test_repeated_bolus_with_until(self):
        event = DosingEvent(
            type="repeated_bolus",
            target="X",
            amount=3.0,
            time=0.0,
            interval=6.0,
            until=24.0,
        )
        specs = events_repeated_bolus(event, 1.0, 1.0, None)
        self.assertEqual(specs[0].trigger, "time >= 0.0 && time % 6.0 == 0 && time < 24.0")

    def test_repeated_bolus_missing_interval_raises(self):
        event = DosingEvent(
            type="repeated_bolus",
            target="X",
            amount=1.0,
            time=0.0,
        )
        with self.assertRaises(ValueError) as ctx:
            events_repeated_bolus(event, 1.0, 1.0, None)
        self.assertIn("interval", str(ctx.exception))


class SingleContinuousTests(unittest.TestCase):

    def test_basic_single_continuous(self):
        event = DosingEvent(
            type="single_continuous",
            target="X",
            amount=2.0,
            time=5.0,
            duration=3.0,
        )
        specs = events_single_continuous(event, 1.0, 1.0, None)
        self.assertEqual(len(specs), 2)
        self.assertEqual(specs[0].trigger, "(time >= 5.0)")
        self.assertEqual(specs[0].assignment, "X + 2.0")
        self.assertEqual(specs[1].trigger, "(time >= 8.0)")
        self.assertEqual(specs[1].assignment, "0")

    def test_single_continuous_missing_duration_raises(self):
        event = DosingEvent(
            type="single_continuous",
            target="X",
            amount=1.0,
            time=0.0,
        )
        with self.assertRaises(ValueError) as ctx:
            events_single_continuous(event, 1.0, 1.0, None)
        self.assertIn("duration", str(ctx.exception))


class DosingEventDispatchTests(unittest.TestCase):

    def test_dispatch_repeated_continuous(self):
        event = DosingEvent(
            type="repeated_continuous",
            target="X",
            amount=1.0,
            time=0.0,
            duration=1.0,
            interval=4.0,
        )
        specs = dosing_events_to_eventspecs(event, 1.0, 1.0, None)
        self.assertEqual(len(specs), 2)

    def test_dispatch_single_bolus(self):
        event = DosingEvent(type="single_bolus", target="X", amount=1.0, time=0.0)
        specs = dosing_events_to_eventspecs(event, 1.0, 1.0, None)
        self.assertEqual(len(specs), 1)

    def test_dispatch_repeated_bolus(self):
        event = DosingEvent(
            type="repeated_bolus", target="X", amount=1.0, time=0.0, interval=4.0
        )
        specs = dosing_events_to_eventspecs(event, 1.0, 1.0, None)
        self.assertEqual(len(specs), 1)

    def test_dispatch_single_continuous(self):
        event = DosingEvent(
            type="single_continuous", target="X", amount=1.0, time=0.0, duration=2.0
        )
        specs = dosing_events_to_eventspecs(event, 1.0, 1.0, None)
        self.assertEqual(len(specs), 2)

    def test_dispatch_unknown_type_raises(self):
        event = DosingEvent(type="unknown", target="X", amount=1.0, time=0.0)
        with self.assertRaises(ValueError) as ctx:
            dosing_events_to_eventspecs(event, 1.0, 1.0, None)
        self.assertIn("Unknown dose_type", str(ctx.exception))


class CreateRREventsTests(unittest.TestCase):

    def test_multiple_events(self):
        events = [
            DosingEvent(
                type="single_bolus", target="X", amount=5.0, time=0.0
            ),
            DosingEvent(
                type="repeated_continuous",
                target="Y",
                amount=2.0,
                time=10.0,
                duration=1.0,
                interval=6.0,
            ),
        ]
        specs = create_rr_events(events, 1.0, 1.0, None)
        self.assertEqual(len(specs), 3)  # 1 bolus + 2 continuous event specs

    def test_empty_events(self):
        specs = create_rr_events([], 1.0, 1.0, None)
        self.assertEqual(specs, [])


class RunScenarioCustomOutputTests(unittest.TestCase):

    def _run(self, target_mappings, outputs, compute_stats=False):
        instance = ModelInstance(
            id="simple",
            label="simple",
            model_path=os.path.join(TEST_MODELS_PATH, "simple", "simple.annotated.sbml"),
            param_file=os.path.join(TEST_MODELS_PATH, "simple", "simple.params.csv"),
            target_mappings=target_mappings,
        )
        scenario = Scenario(
            id="custom",
            label="custom",
            duration=2,
            evaluation_resolution=4,
            initial_states=None,
            parameters=None,
            dosing_events=[
                DosingEvent(type="single_bolus", target="AGut", amount=1.0, time=0.0)
            ],
            outputs=[Output(id=o, output=o) for o in outputs],
            reference_data=None,
            time_unit=TimeUnit.DAY,
            amount_unit=AmountUnit.MICROGRAMS,
        )
        with tempfile.TemporaryDirectory() as tmp:
            out_file = os.path.join(tmp, "out.csv")
            run_scenario(
                instance, scenario, out_file, True, logging.getLogger(),
                compute_stats=compute_stats,
            )
            results = pd.read_csv(out_file)
            stats = (
                pd.read_csv(out_file.replace(".csv", "_stats.csv"))
                if compute_stats else None
            )
        return results, stats

    def test_expression_output_is_computed(self):
        results, _ = self._run(
            {"ATotal": "ABlood + ALiver + ARest + AGut + AUrine"},
            ["ABlood", "ALiver", "ARest", "AGut", "AUrine", "ATotal"],
        )
        expected = results[["ABlood", "ALiver", "ARest", "AGut", "AUrine"]].sum(axis=1)
        pd.testing.assert_series_equal(
            results["ATotal"], expected, check_names=False, atol=1e-9
        )

    def test_expression_operators(self):
        results, _ = self._run(
            {
                "Diff": "AGut - ABlood",
                "Prod": "2 * ABlood",
                "Ratio": "ABlood / (ABlood + ALiver + 1)",
            },
            ["AGut", "ABlood", "ALiver", "Diff", "Prod", "Ratio"],
        )
        pd.testing.assert_series_equal(
            results["Diff"], results["AGut"] - results["ABlood"],
            check_names=False, atol=1e-9,
        )
        pd.testing.assert_series_equal(
            results["Prod"], 2 * results["ABlood"], check_names=False, atol=1e-9
        )
        pd.testing.assert_series_equal(
            results["Ratio"],
            results["ABlood"] / (results["ABlood"] + results["ALiver"] + 1),
            check_names=False, atol=1e-9,
        )

    def test_plain_and_bracketed_mappings_still_selected(self):
        results, _ = self._run(
            {"CBlood": "[ABlood]"},
            ["ABlood", "CBlood"],
        )
        self.assertIn("[ABlood]", results.columns)
        self.assertNotIn("CBlood", results.columns)
        self.assertTrue((results["[ABlood]"] >= 0).all())
        self.assertGreater(results["[ABlood]"].max(), 0)

    def test_expression_output_included_in_stats(self):
        _, stats = self._run(
            {"ATotal": "ABlood + ALiver + ARest + AGut + AUrine"},
            ["ATotal"],
            compute_stats=True,
        )
        self.assertEqual(stats["output"].tolist(), ["ATotal"])
        self.assertAlmostEqual(stats["cmax"].iloc[0], 1.0, places=6)

    def test_null_mapping_is_skipped(self):
        results, _ = self._run({"Skipped": None}, ["ABlood", "Skipped"])
        self.assertIn("ABlood", results.columns)
        self.assertNotIn("Skipped", results.columns)


class EventSpecDataclassTests(unittest.TestCase):

    def test_event_spec_creation(self):
        spec = EventSpec(target="X", trigger="time >= 5.0", assignment="X + 10.0")
        self.assertEqual(spec.target, "X")
        self.assertEqual(spec.trigger, "time >= 5.0")
        self.assertEqual(spec.assignment, "X + 10.0")


if __name__ == '__main__':
    unittest.main()
