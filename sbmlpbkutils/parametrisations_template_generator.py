import pandas as pd
import libsbml as ls

from . import create_unit_string

class ParametrisationsTemplateGenerator:

    def generate(
        self,
        model: ls.Model,
        use_defaults: bool = True,
        include_element_name: bool = True
    ):
        dt = []
        for i in range(0,model.getNumParameters()):
            element = model.getParameter(i)
            if (element.getConstant()):
                unit_id = element.getUnits()
                if unit_id:
                    unit_definition = model.getUnitDefinition(unit_id)
                    unit_string = create_unit_string(unit_definition)
                else:
                    unit_string = ""
                row = [
                    element.getId(),
                    element.getValue() if use_defaults else "",
                    unit_string,
                    ""
                ]
                if include_element_name:
                    row.insert(3, element.getName())
                dt.append(row)

        colnames = ["element_id", "value", "unit", "reference"]
        if include_element_name:
            colnames.insert(3, "description")

        terms = pd.DataFrame(
            dt,
            columns=colnames
        )
        return terms
