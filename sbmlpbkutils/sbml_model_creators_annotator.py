import libsbml as ls
import yaml

class SbmlModelCreatorsAnnotator:

    def set_model_creators(
        self,
        document: ls.SBMLDocument,
        creators: dict
    ) -> None:
        """Sets the model creators in the SBML document based on the provided
        creators dictionary. The creators dictionary follows the structure of
        the citation file format (CFF). Overwrites existing model creators."""
        model = document.getModel()
        history = ls.ModelHistory()
        for record in creators:
            creator = ls.ModelCreator()
            if 'given-names' in record:
                creator.setGivenName(record['given-names'])
            if 'family-names' in record:
                creator.setFamilyName(record['family-names'])
            if 'affiliation' in record:
                creator.setOrganisation(record['affiliation'])
            if 'email' in record:
                creator.setEmail(record['email'])
            history.addCreator(creator)
        model.setModelHistory(history)

    def set_model_creators_from_cff(
        self,
        document: ls.SBMLDocument,
        cff_file: str
    ) -> None:
        """Sets the model creators in the SBML document based on the specified
        CFF file (citation file format). Overwrites existing model creators."""
        creators = self._read_cff_authors(cff_file)
        self.set_model_creators(document, creators)

    def _read_cff_authors(self, cff_file):
        """Reads in the authors from a cff file with the specified file path. """
        try:
            # Open and load the CFF file
            with open(cff_file, 'r', encoding='utf-8') as file:
                cff_data = yaml.safe_load(file)
            # Extract the list of creators from the 'authors' field
            creators = cff_data.get('authors', [])
        except FileNotFoundError:
            raise Exception("CFF file not found.")
        except yaml.YAMLError as e:
            raise Exception(f"Error reading CFF file: {e}")
        return creators
