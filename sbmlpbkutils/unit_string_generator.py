import libsbml as ls

si_prefix_string = {
    3: 'k',
    2: 'h',
    1: 'da',
    0: '',
    -1: 'd',
    -2: 'c',
    -3: 'm',
    -6: 'u',
    -9: 'n',
    -12: 'p',
}

si_prefix_strings_ext = {
    3: 'kilo',
    2: 'hecto',
    1: 'deca',
    0: '',
    -1: 'deci',
    -2: 'centi',
    -3: 'milli',
    -6: 'micro',
    -9: 'nano',
    -12: 'pico',
}

base_unit_strings = {
    ls.UNIT_KIND_DIMENSIONLESS: '',
    ls.UNIT_KIND_SECOND: 's',
    ls.UNIT_KIND_GRAM: 'g',
    ls.UNIT_KIND_LITER: 'L',
    ls.UNIT_KIND_LITRE: 'L',
    ls.UNIT_KIND_METER: 'm',
    ls.UNIT_KIND_METRE: 'm',
    ls.UNIT_KIND_MOLE: 'mol'
}

base_unit_strings_ext = {
    ls.UNIT_KIND_DIMENSIONLESS: '',
    ls.UNIT_KIND_SECOND: 'second',
    ls.UNIT_KIND_GRAM: 'gram',
    ls.UNIT_KIND_LITER: 'liter',
    ls.UNIT_KIND_LITRE: 'liter',
    ls.UNIT_KIND_METER: 'meter',
    ls.UNIT_KIND_METRE: 'meter',
    ls.UNIT_KIND_MOLE: 'mole'
}

class UnitStringGenerator:

    def create_unit_string(
        self,
        unit: ls.UnitDefinition,
        ext: bool = False
    ) -> str:
        unit_string_parts = []
        for i in range(unit.getNumUnits()):
            unit_part = unit.getUnit(i)
            unit_part_string = self.create_unit_part_string(unit_part, ext, i == 0)
            if unit_part_string:
                unit_string_parts.append(unit_part_string)
        result = ''.join(unit_string_parts) if unit_string_parts else 'dimensionless'
        return result

    def create_unit_part_string(
        self,
        u: ls.Unit,
        ext: bool = False,
        is_first: bool = False,
    ) -> str:
        kind = u.getKind()
        scale = u.getScale()
        exponent = u.getExponentAsDouble()
        multiplier = u.getMultiplier()
        if kind == ls.UNIT_KIND_SECOND:
            match multiplier:
                case 60:
                    base_unit_str = 'min'
                    multiplier = 1
                case 3600:
                    base_unit_str = 'h'
                    multiplier = 1
                case 86400:
                    base_unit_str = 'd'
                    multiplier = 1
                case 31557600:
                    base_unit_str = 'y'
                    multiplier = 1
                case _:
                    base_unit_str = 's'
        else:
            base_unit_str = base_unit_strings_ext.get(kind) if ext else base_unit_strings.get(kind)

        scale_str = si_prefix_strings_ext.get(scale) if ext else si_prefix_string.get(scale)
        if exponent >= 0:
            if is_first:
                operator_str = ''
            else:
                operator_str = '.'
        else:
            operator_str = '/'
            exponent = -exponent
        exponent_str = f"^{exponent:g}" if exponent != 1 else ''
        multiplier_str = f"{multiplier}." if multiplier != 1 else ''
        ucum_unit = f"{operator_str}{multiplier_str}{scale_str}{base_unit_str}{exponent_str}"
        return ucum_unit
