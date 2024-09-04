import pandas as pd

class ParametrisationsTemplateGenerator:

    def generate(self, model):
        dt = []
        for i in range(0,model.getNumParameters()):
            element = model.getParameter(i)
            if (element.getConstant()):
                dt.append([
                    element.getId(),
                    pd.NA,
                    ""
                ])

        terms = pd.DataFrame(
            dt,
            columns=["element_id", "value", "reference"]
        )
        return terms
