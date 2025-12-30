
# SBML model validation

The `PbkModelValidator` class provides functionality for validating SBML PBK model implementations against the [FAIR PBK standard](https://fair-pbk.github.io/fair-pbk-standard/specification/) specification. It performs a range of automated checks at the model, element, and unit levels to help identify missing annotations, structural issues, and inconsistencies that may affect model interoperability and reuse.

## Example

The following example shows how to run the validation on an annotated SBML PBK model file `model.sbml` and print the results to the console using a console logger:

```python
import logging
from sbmlpbkutils import PbkModelValidator

logger = logging.getLogger('pbk-validator')
logging.basicConfig(level=logging.INFO)
PbkModelValidator().validate('model.sbml', logger)
```

To write the validation results to a file instead, use a file logger.

