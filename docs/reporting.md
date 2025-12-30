# Model reporting

The `PbkModelReportGenerator` class produces a Markdown report for an SBML PBK model. The report contains a model overview, compartments, species, transfer equations, ODEs, rules and parameters and includes a rendered SVG diagram of the model.

The class expects an `libsbml.SBMLDocument` object and writes a Markdown file (and an SVG diagram with the same base name) when calling `create_md_report`.

## Example of use

The following code example shows how to generate a report for the SBML PBK model `model.sbml` to generate the Markdown report file `model-report.md` (and accompanying diagram SVG file `model-report.svg`)).

```python
from libsbml import readSBML
from sbmlpbkutils import PbkModelReportGenerator

# Read SBML document
doc = readSBML('model.sbml')

# Create a Markdown report
PbkModelReportGenerator(doc).create_md_report('model-report.md')
```

## Notes and dependencies

- Diagrams require the `graphviz` Python package and the Graphviz system executable (`dot`).
- The report uses LaTeX-formatted math (wrapped in `$...$`) for equations. Ensure the host or renderer you use supports math rendering (GitHub Pages with MathJax, MkDocs with a math plugin, or local viewing with a Markdown viewer that supports math).
