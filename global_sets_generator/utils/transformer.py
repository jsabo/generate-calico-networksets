class TransformerException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Transformer:

    def __init__(self):
        pass

    def transform(self, input: str) -> str:
        """
        :param input: Data to be transformed
        :return: Transformed data
        """
        return ""


class AwsTransformer(Transformer):

    def __init__(self):
        super().__init__()

    def transform(self, input: str) -> str:
        """
        :param input: Data to be transformed
        :return: Transformed data
        """
        return ""


class AzureTransformer(Transformer):

    def __init__(self):
        super().__init__()

    def transform(self, input: str) -> str:
        """
        :param input: Data to be transformed
        :return: Transformed data
        """
        return ""