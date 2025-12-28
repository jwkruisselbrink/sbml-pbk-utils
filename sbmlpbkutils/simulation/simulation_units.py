from enum import Enum
import libsbml as ls

class TimeUnit(str, Enum):
    SECOND = "seconds"
    MINUTE = "minutes"
    HOUR = "hours"
    DAY = "days"

    def __str__(self) -> str:
        return self.value

class AmountUnit(str, Enum):
    MICROGRAMS = "ug"
    MILLIGRAMS = "mg"
    GRAMS = "g"
    MICROMOLES = "umol"
    MILLIMOLES = "mmol"
    MOLES = "mol"

    def __str__(self) -> str:
        return self.value

def get_model_time_unit(model: ls.Model) -> TimeUnit:
    """
    Extracts the model's time unit according to SBML rules:
    """

    unit_def_id = model.getTimeUnits()

    # Validate existence
    if not unit_def_id:
        raise Exception(f"Time unit not defined in model [{model.getId()}].")

    unit_def = model.getUnitDefinition(unit_def_id)
    if unit_def is None:
        raise Exception(
            f"Time unit [{unit_def_id}] referenced in model [{model.getId()}] does not exist."
        )

    # Check whether this is a time unit
    if unit_def.getNumUnits() != 1:
        raise Exception(
            f"Time unit definition [{unit_def_id}] in model [{model.getId()}] "
            f"contains multiple unit elements, cannot interpret."
        )

    u = unit_def.getUnit(0)
    if u.getKind() != ls.UNIT_KIND_SECOND:
        raise Exception(
            f"UnitDefinition [{unit_def_id}] in model [{model.getId()}] "
            f"is not a valid time unit (kind={ls.UnitKind_toString(u.getKind())})."
        )

    # Check unit exponent: should be 1
    exponent = u.getExponent()
    if exponent != 1:
        raise Exception(
            f"Time unit [{unit_def_id}] exponent {exponent} is not supported."
        )

    # Get scale and multiplier (time unit = multiplier * second * 10^scale)
    scale = u.getScale()
    multiplier = u.getMultiplier()

    # First: pure second-based based on multiplier and scale
    base_seconds = multiplier * (10 ** scale)

    # Interpret units
    # Minute:   60 seconds
    # Hour:     3600 seconds
    # Day:      86400 seconds

    # Use tolerance for float rounding
    eps = 1e-10

    if abs(base_seconds - 1) < eps:
        return TimeUnit.SECOND
    elif abs(base_seconds - 60) < eps:
        return TimeUnit.MINUTE
    elif abs(base_seconds - 3600) < eps:
        return TimeUnit.HOUR
    elif abs(base_seconds - 86400) < eps:
        return TimeUnit.DAY
    else:
        raise Exception(
            f"Time unit [{unit_def_id}] in model [{model.getId()}] "
            f"has unsupported time conversion: {base_seconds} seconds."
        )

def get_model_amount_unit(model: ls.Model) -> AmountUnit:
    """Determine the substance/amount unit from an SBML model and map it to
    :class:`AmountUnit`.

    Supports both mass-based (grams family) and amount-based (mole family)
    SBML units. Raises an :class:`Exception` when the unit definition cannot
    be mapped to a known :class:`AmountUnit`.
    """

    unit_def_id = model.getSubstanceUnits()

    if not unit_def_id:
        raise Exception(
            f"Substance (amount) unit not defined in model [{model.getId()}]."
        )

    unit_def = model.getUnitDefinition(unit_def_id)
    if unit_def is None:
        raise Exception(
            f"Substance unit [{unit_def_id}] referenced in model [{model.getId()}] does not exist."
        )

    if unit_def.getNumUnits() != 1:
        raise Exception(
            f"Substance unit definition [{unit_def_id}] in model [{model.getId()}] "
            f"has multiple unit elements; cannot interpret."
        )

    u = unit_def.getUnit(0)

    # Handle gram-based units
    if u.getKind() == ls.UNIT_KIND_GRAM:
        # Extract SBML unit information
        multiplier = u.getMultiplier()  # typical: 1
        scale = u.getScale()            # log10 factor
        exponent = u.getExponent()      # should be 1

        if exponent != 1:
            raise Exception(
                f"Amount unit [{unit_def_id}] exponent {exponent} is unsupported."
            )

        # Compute actual grams represented (unit = multiplier * 10^scale grams)
        base_grams = multiplier * (10 ** scale)

        eps = 1e-12

        # Map to enum
        if abs(base_grams - 1e-6) < eps:
            return AmountUnit.MICROGRAMS
        elif abs(base_grams - 1e-3) < eps:
            return AmountUnit.MILLIGRAMS
        elif abs(base_grams - 1) < eps:
            return AmountUnit.GRAMS
        else:
            raise Exception(
                f"Amount unit [{unit_def_id}] in model [{model.getId()}] "
                f"maps to unsupported mass: {base_grams} grams."
            )

    # Handle mole-based units
    if u.getKind() == ls.UNIT_KIND_MOLE:
        multiplier = u.getMultiplier()
        scale = u.getScale()
        exponent = u.getExponent()

        if exponent != 1:
            raise Exception(
                f"Amount unit [{unit_def_id}] exponent {exponent} is unsupported."
            )

        base_moles = multiplier * (10 ** scale)

        eps = 1e-12

        if abs(base_moles - 1e-6) < eps:
            return AmountUnit.MICROMOLES
        elif abs(base_moles - 1e-3) < eps:
            return AmountUnit.MILLIMOLES
        elif abs(base_moles - 1) < eps:
            return AmountUnit.MOLES

        raise Exception(
            f"Amount unit [{unit_def_id}] in model [{model.getId()}] "
            f"maps to unsupported amount: {base_moles} moles."
        )

    # If we reach here, the unit kind is not supported
    raise Exception(
        f"UnitDefinition [{unit_def_id}] in model [{model.getId()}] "
        f"is not a supported amount unit (kind={ls.UnitKind_toString(u.getKind())})."
    )

def get_model_time_unit_alignment_factor(
    model: ls.Model,
    target_unit: TimeUnit
) -> float:
    """
    Compute a conversion factor such that:

        time_in_target_units = time_in_model_units * factor

    The conversion is performed by converting both units to seconds.
    """

    # Resolve model time unit
    model_unit = get_model_time_unit(model)

    return get_time_unit_alignment_factor(model_unit, target_unit)

def get_time_unit_alignment_factor(
    source_unit: TimeUnit,
    target_unit: TimeUnit
) -> float:
    """
    Compute a conversion factor such that:

        time_in_target_units = source_time_unit * factor

    The conversion is performed by converting both units to seconds.
    """

    # Conversion map time unit to seconds
    map = {
        TimeUnit.SECOND: 1.0,
        TimeUnit.MINUTE: 60.0,
        TimeUnit.HOUR: 3600.0,
        TimeUnit.DAY: 86400.0,
    }

    if source_unit not in map:
        raise Exception(f"Unsupported model time unit: {source_unit}")

    if target_unit not in map:
        raise Exception(f"Unsupported target time unit: {target_unit}")

    model_seconds = map[source_unit]
    target_seconds = map[target_unit]
    return target_seconds / model_seconds

def get_amount_unit_alignment_factor(
    model: ls.Model,
    target_unit: AmountUnit,
    molar_mass: float | None = None
) -> float:
    """Compute a conversion factor such that::

        amount_in_target_units = amount_in_model_units * factor

    The conversion supports conversions within the same family (grams <-> grams,
    moles <-> moles) and cross-family conversions (grams <-> moles) which
    require a ``molar_mass`` argument (grams per mole).

    Parameters
    ----------
    model
        The SBML model from which the source amount unit is resolved.
    target_unit
        The desired target :class:`AmountUnit`.
    molar_mass
        Optional molar mass (grams per mole) required when converting between
        mass and amount families.
    """

    model_unit = get_model_amount_unit(model)

    mass_map = {
        AmountUnit.GRAMS: 1.0,
        AmountUnit.MILLIGRAMS: 1e-3,
        AmountUnit.MICROGRAMS: 1e-6,
    }
    mole_map = {
        AmountUnit.MOLES: 1.0,
        AmountUnit.MILLIMOLES: 1e-3,
        AmountUnit.MICROMOLES: 1e-6,
    }

    # Same family: mass -> mass
    if model_unit in mass_map and target_unit in mass_map:
        model_amount = mass_map[model_unit]
        target_amount = mass_map[target_unit]
        return model_amount / target_amount

    # Same family: mole -> mole
    if model_unit in mole_map and target_unit in mole_map:
        model_amount = mole_map[model_unit]
        target_amount = mole_map[target_unit]
        return model_amount / target_amount

    # Cross-family conversion requires molar_mass (grams per mole)
    if molar_mass is None:
        raise Exception("Cross-family amount/mass conversion requires molar mass (g/mol).")

    # model mass -> target mole
    if model_unit in mass_map and target_unit in mole_map:
        model_grams = mass_map[model_unit]
        # grams -> moles
        model_moles = model_grams / molar_mass
        target_mole_size = mole_map[target_unit]
        # 1 model unit equals model_moles / target_mole_size target units
        return model_moles / target_mole_size

    # model mole -> target mass
    if model_unit in mole_map and target_unit in mass_map:
        model_moles = mole_map[model_unit]
        model_grams = model_moles * molar_mass
        target_gram_size = mass_map[target_unit]
        return model_grams / target_gram_size

    raise Exception(f"Unsupported conversion from {model_unit} to {target_unit}")
