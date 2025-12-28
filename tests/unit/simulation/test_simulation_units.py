import unittest

import libsbml as ls

from sbmlpbkutils.simulation import simulation_units as su

class SimulationUnitsTests(unittest.TestCase):

    def _new_model_with_unit(
        self,
        unit_id: str,
        kind: int,
        multiplier: float,
        scale: int = 0,
        exponent: int = 1
    ):
        doc = ls.SBMLDocument()
        model = doc.createModel()
        ud = model.createUnitDefinition()
        ud.setId(unit_id)
        u = ud.createUnit()
        u.setKind(kind)
        u.setMultiplier(multiplier)
        u.setScale(scale)
        u.setExponent(exponent)
        model.setSubstanceUnits(unit_id)
        return model

    def test_get_model_amount_unit_grams(self):
        model = self._new_model_with_unit('mg', ls.UNIT_KIND_GRAM, 1e-3)
        self.assertEqual(su.get_model_amount_unit(model), su.AmountUnit.MILLIGRAMS)

    def test_get_model_amount_unit_moles(self):
        model = self._new_model_with_unit('umol', ls.UNIT_KIND_MOLE, 1e-6)
        self.assertEqual(su.get_model_amount_unit(model), su.AmountUnit.MICROMOLES)

    def test_amount_alignment_same_family_mass(self):
        model = self._new_model_with_unit('g', ls.UNIT_KIND_GRAM, 1.0)
        factor = su.get_amount_unit_alignment_factor(model, su.AmountUnit.MILLIGRAMS)
        self.assertAlmostEqual(factor, 1000.0)

    def test_amount_alignment_same_family_mole(self):
        model = self._new_model_with_unit('mol', ls.UNIT_KIND_MOLE, 1.0)
        factor = su.get_amount_unit_alignment_factor(model, su.AmountUnit.MILLIMOLES)
        self.assertAlmostEqual(factor, 1000.0)

    def test_cross_family_grams_to_millimoles_with_molar_mass(self):
        model = self._new_model_with_unit('g', ls.UNIT_KIND_GRAM, 1.0)
        # molar mass of glucose ~ 180 g/mol
        factor = su.get_amount_unit_alignment_factor(model, su.AmountUnit.MILLIMOLES, molar_mass=180.0)
        # 1 g -> 1/180 mol -> 5.555... mmol (1000/180)
        self.assertAlmostEqual(factor, 1000.0/180.0, places=6)

    def test_cross_family_requires_molar_mass(self):
        model = self._new_model_with_unit('g', ls.UNIT_KIND_GRAM, 1.0)
        with self.assertRaises(Exception):
            su.get_amount_unit_alignment_factor(model, su.AmountUnit.MOLES)


if __name__ == '__main__':
    unittest.main()
