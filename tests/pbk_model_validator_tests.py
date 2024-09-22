import unittest
import sys
import os
import logging
import libsbml as ls
from pathlib import Path
from sbmlpbkutils import PbkModelValidator

sys.path.append('../sbmlpbkutils/')

__test_outputs_path__ = './tests/__testoutputs__'

class PbkModelValidatorTests(unittest.TestCase):

    def create_file_logger(self, logfile) -> logging.Logger:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(logfile)
        logger.addHandler(fh)
        return logger

    def setUp(self):
        from pathlib import Path
        Path(__test_outputs_path__).mkdir(parents=True, exist_ok=True)

    @classmethod
    def setUpClass(cls):
        cls.sbml_files = []
        files = os.listdir('./tests/models/')
        for file in files:
            if file.endswith('.sbml'):
                cls.sbml_files.append('./tests/models/' + file)

    def test_validate(self):
        validator = PbkModelValidator()
        for sbml_file in self.sbml_files:
            sbml_basename = os.path.basename(sbml_file)
            log_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.log'))
            logger = self.create_file_logger(log_file)
            validator.validate(sbml_file, logger)

if __name__ == '__main__':
    unittest.main()