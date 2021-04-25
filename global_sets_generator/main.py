import configparser
import importlib
from global_sets_generator.utils.extractor import Extractor
from global_sets_generator.utils.transformer import Transformer

CLOUD_PROVIDER_SECTION = 'Cloud Providers'
IP_RANGES_SECTION = 'IP Ranges'

extractor_module = 'global_sets_generator.utils.extractor'
transformer_module = 'global_sets_generator.utils.transformer'


def str_to_instance(module_name: str, class_name: str):
    class_ = None
    try:
        module_ = importlib.import_module(module_name)
        try:
            class_ = getattr(module_, class_name)
        except AttributeError:
            pass  #todo error prints
    except ImportError:
        pass  #todo error prints
    if class_:
        return class_()
    return None


def get_url(conf: configparser.ConfigParser, cloud_provider: str)-> str:
    conf_entry = 'ip_ranges.url.{}'.format(cloud_provider.lower())
    return conf.get(IP_RANGES_SECTION, conf_entry)


def write_file(path: str, filename: str, data):
    pass


if __name__ == '__main__':
    # todo add error handling around config file
    config = configparser.ConfigParser()
    config.read("../config.txt")
    cloud_providers: str = config.get(CLOUD_PROVIDER_SECTION, 'cloud_provider_list')
    if cloud_providers and isinstance(cloud_providers, str):
        provider_list = cloud_providers.split(',')
        for cloud_provider in provider_list:
            source = get_url(config, cloud_provider)
            extractor: Extractor = str_to_instance(extractor_module, '{}Extractor'.format(cloud_provider))
            transformer: Transformer = str_to_instance(transformer_module, '{}Transformer'.format(cloud_provider))
            tmp = extractor.extract(source)
            write_file('', '', transformer.transform(extractor.extract(source)))
