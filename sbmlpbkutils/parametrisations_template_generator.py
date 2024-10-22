import pandas as pd
import libsbml as ls

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
                row = [
                    element.getId(),
                    element.getValue() if use_defaults else "",
                    element.getUnits(),
                    ""
                ]
                if include_element_name:
                    row.insert(2, element.getName())
                dt.append(row)

        colnames = ["element_id", "value", "unit", "reference"]
        if include_element_name:
            colnames.insert(2, "description")

        terms = pd.DataFrame(
            dt,
            columns=colnames
        )
        return terms
