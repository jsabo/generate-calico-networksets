from urllib.request import Request, urlopen
import ssl
import subprocess


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
        encoding = 'utf-8'
        # todo error handling
        context = ssl._create_unverified_context()
        # todo do proper TLS certificate verification https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
        req = Request(source, headers={'User-Agent': 'Mozilla/5.0'})
        contents: bytes = urlopen(req, context=context).read()
        return contents.decode(encoding)


class AwsExtractor(Extractor):

    def __init__(self):
        super().__init__()

    def extract(self, source: str)-> str:
        return super().extract(source)


class AzureExtractor(Extractor):

    def __init__(self):
        super().__init__()

    def extract(self, source: str)-> str:
        encoding = 'utf-8'
        bashCommand = "curl -sS {} | egrep -o 'https://download.*?\.json' | uniq".format(source)
        output = subprocess.check_output(['bash', '-c', bashCommand])
        download_url = output.decode(encoding).strip()
        contents: str = super().extract(download_url).replace('\r\n', '\n')
        return contents