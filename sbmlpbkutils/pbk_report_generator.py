import libsbml as ls

from . import PbkModelInfosExtractor

class PbkReportGenerator:

    def create_report(
        self,
        document: ls.SBMLDocument,
        output_file: str
    ):
        model = document.getModel()
        name = model.getName() if model.isSetName() else model.getId()
        infos_extractor = PbkModelInfosExtractor(document)

        # Open the file in write mode
        with open(output_file, "w") as f:
            # Write the title
            f.write(f"# {name}\n\n")

            # Write the model creators table
            f.write("## Creators\n\n")
            table = infos_extractor.get_model_creators()
            if table is not None:
                f.write(table.to_markdown())
                f.write("\n\n")
            else:
                f.write("Model creators not specified\n\n")

            # Write the model overview table
            f.write("## Overview\n\n")
            table = infos_extractor.get_model_overview()
            f.write(table.to_markdown())
            f.write("\n\n")

            # Write compartment infos table
            f.write("## Compartments\n\n")
            table = infos_extractor.get_compartment_infos()
            f.write(table.to_markdown())
            f.write("\n\n")

            # Write compartment infos table
            f.write("## Species\n\n")
            table = infos_extractor.get_species_infos()
            f.write(table.to_markdown())
            f.write("\n\n")

            # Write compartment infos table
            f.write("## Parameters\n\n")
            table = infos_extractor.get_parameter_infos()
            f.write(table.to_markdown())
            f.write("\n\n")

            # Write compartment infos table
            f.write("## ODEs\n\n")
            odes = infos_extractor.get_odes()
            for species_id, equation in odes:
                f.write(f"${equation}$\n\n")
            f.write("\n\n")
