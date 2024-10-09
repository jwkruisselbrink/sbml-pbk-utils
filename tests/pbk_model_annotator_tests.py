import unittest
import sys
import os
import logging
import libsbml as ls
from pathlib import Path
from sbmlpbkutils import PbkModelValidator
from sbmlpbkutils.pbk_model_annotator import PbkModelAnnotator

sys.path.append('../sbmlpbkutils/')

__test_outputs_path__ = './tests/__testoutputs__'

class PbkModelAnnotatorTests(unittest.TestCase):

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
            if file.endswith('.sbml') and not file.endswith('annotated.sbml'):
                cls.sbml_files.append('./tests/models/' + file)

    def test_annotate(self):
        annotator = PbkModelAnnotator()
        for sbml_file in self.sbml_files:
            sbml_basename = os.path.basename(sbml_file)
            annotations_file = Path(sbml_file).with_suffix('.annotations.csv')
            print(annotations_file)
            log_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.annotation.log'))
            out_file = os.path.join(__test_outputs_path__, Path(sbml_basename).with_suffix('.annotated.sbml'))
            logger = self.create_file_logger(log_file)
            annotator.annotate(sbml_file, annotations_file, out_file, logger)

if __name__ == '__main__':
    unittest.main()
