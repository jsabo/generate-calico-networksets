class ExtractorException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Extractor:

    def __init__(self):
        pass

    def extract(self, source: str)-> str:
        """
        Reads a set of ip range sets from a pre-configured source. The source may have access protocols and specific
        data validation needs that should be implemented here
        :param source: the source from which to extract
        :return: the data extracted in string format
        """
        pass


class AwsExtractor(Extractor):

    def __init__(self):
        super().__init__()

    def extract(self)-> str:
        pass


class AzureExtractor(Extractor):

    def __init__(self):
        super().__init__()

    def extract(self)-> str:
        pass
