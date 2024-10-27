import unittest
import uuid
import sys
import os
import logging
from pathlib import Path
from sbmlpbkutils import PbkModelValidator

sys.path.append('../sbmlpbkutils/')

__test_models_path__ = './tests/models/'
__test_outputs_path__ = './tests/__testoutputs__'

class PbkModelValidatorTests(unittest.TestCase):

    def create_file_logger(self, logfile: str) -> logging.Logger:
        logger = logging.getLogger(uuid.uuid4().hex)
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(logfile, 'w+')
        formatter = logging.Formatter('[%(levelname)s] - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    def setUp(self):
        from pathlib import Path
        Path(__test_outputs_path__).mkdir(parents=True, exist_ok=True)

    def test_validate_simple(self):
        sbml_file = os.path.join(__test_models_path__, 'simple.sbml')
        validator = PbkModelValidator()
        sbml_basename = os.path.basename(sbml_file)
        log_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.validation.log'))
        logger = self.create_file_logger(log_file)
        validator.validate(sbml_file, logger)

    def test_validate_simple_annotated(self):
        sbml_file = os.path.join(__test_models_path__, 'simple.annotated.sbml')
        validator = PbkModelValidator()
        sbml_basename = os.path.basename(sbml_file)
        log_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.validation.log'))
        logger = self.create_file_logger(log_file)
        validator.validate(sbml_file, logger)

if __name__ == '__main__':
    unittest.main()
