import pandas as pd
import libsbml as ls

from . import create_unit_string

class ParametrisationsTemplateGenerator:

    def generate(
        self,
        model: ls.Model,
        use_defaults: bool = True,
        include_element_name: bool = True,
        model_instance_ids: list[str] = None
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        model_instance_ids = model_instance_ids if model_instance_ids else [f'{model.getId()}_PARAM']
        instances = self.generate_instances_df(
            model,
            model_instance_ids = model_instance_ids
        )
        params = self.generate_parameters_df(
            model,
            use_defaults = use_defaults,
            include_element_name = include_element_name,
            model_instance_ids = model_instance_ids
        )
        return (instances, params)

    def generate_instances_df(
        self,
        model: ls.Model,
        model_instance_ids: list[str] = None
    ):
        model_instance_ids = model_instance_ids if model_instance_ids else [f'{model.getId()}_PARAM']
        dt = []
        for i, model_instance_id in enumerate(model_instance_ids):
            row = [
                model_instance_id,
                model.getId(),
                "",
                "",
                ""
            ]
            dt.append(row)

        colnames = ["idModelInstance", "idModelDefinition", "Species", "Substances", "Reference"]
        df = pd.DataFrame(dt, columns = colnames)
        return df

    def generate_parameters_df(
        self,
        model: ls.Model,
        use_defaults: bool = True,
        include_element_name: bool = True,
        model_instance_ids: list[str] = None
    ):
        dt = []
        model_instance_ids = model_instance_ids if model_instance_ids else [f'{model.getId()}_PARAM']
        for _, model_instance_id in enumerate(model_instance_ids):
            for j in range(0,model.getNumParameters()):
                element = model.getParameter(j)
                if (element.getConstant()):
                    unit_id = element.getUnits()
                    if unit_id:
                        unit_definition = model.getUnitDefinition(unit_id)
                        unit_string = create_unit_string(unit_definition)
                    else:
                        unit_string = ""
                    row = [
                        model_instance_id,
                        element.getId(),
                        element.getValue() if use_defaults else "",
                        unit_string,
                        ""
                    ]
                    if include_element_name:
                        row.insert(4, element.getName())
                    dt.append(row)

        colnames = ["idModelInstance", "Parameter", "Value", "Unit", "Reference"]
        if include_element_name:
            colnames.insert(4, "Description")

        df = pd.DataFrame(dt, columns = colnames)
        return df
