import libsbml
from graphviz import Digraph


def load_sbml_model(file_path):
    """Load an SBML file and return the model."""
    reader = libsbml.SBMLReader()
    document = reader.readSBML(file_path)
    if document.getNumErrors() > 0:
        raise Exception("Errors occurred while reading the SBML file.")
    return document.getModel()


def extract_grouped_network_data(model):
    """
    Extract reactions and group species by compartment for visualization.
    """
    compartments = {}
    edges = []

    # Process compartments
    for compartment in model.getListOfCompartments():
        compartments[compartment.getId()] = {
            "name": compartment.getName() if compartment.isSetName() else compartment.getId(),
            "species": [],
        }
    
    # Process species and assign them to compartments
    for species in model.getListOfSpecies():
        species_id = species.getId()
        compartment_id = species.getCompartment()
        if compartment_id in compartments:
            compartments[compartment_id]["species"].append(species_id)
    
    # Process reactions to establish relationships between compartments
    for reaction in model.getListOfReactions():
        reactant_compartments = set()
        product_compartments = set()
        
        # Identify compartments of reactants
        for reactant in reaction.getListOfReactants():
            species_id = reactant.getSpecies()
            for compartment_id, data in compartments.items():
                if species_id in data["species"]:
                    reactant_compartments.add(compartment_id)
        
        # Identify compartments of products
        for product in reaction.getListOfProducts():
            species_id = product.getSpecies()
            for compartment_id, data in compartments.items():
                if species_id in data["species"]:
                    product_compartments.add(compartment_id)
        
        # Create edges between compartments
        for reactant_compartment in reactant_compartments:
            for product_compartment in product_compartments:
                edges.append((reactant_compartment, product_compartment))
    
    return compartments, edges


def plot_grouped_network_graphviz(compartments, edges, output_file="sbml_diagram"):
    """
    Plot the network graph using Graphviz, grouping species by compartments.
    """
    dot = Digraph(format="png")  # Change format as needed (e.g., pdf, svg)

    # Add nodes for compartments using square shapes
    for compartment_id, data in compartments.items():
        label = f"{data['name']}\\n({len(data['species'])} species)"
        dot.node(compartment_id, label=label, shape="box", style="filled", color="lightblue", fontsize="10")

    # Add edges between compartments
    for source, target in edges:
        dot.edge(source, target, color="black", arrowhead="normal")

    # Save and render the diagram
    dot.render(output_file, view=True)
    print(f"Graph saved as {output_file}.png")


# Main function to load SBML, process data, and plot
def main(sbml_file, output_file="sbml_diagram"):
    model = load_sbml_model(sbml_file)
    compartments, edges = extract_grouped_network_data(model)
    plot_grouped_network_graphviz(compartments, edges, output_file)

# Example Usage
if __name__ == "__main__":
    sbml_file = "./tests/models/simple.annotated.sbml"  # Replace with your SBML file path
    main(sbml_file)
