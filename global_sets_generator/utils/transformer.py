import json

class TransformerException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Transformer:

    yaml_template: str = '''
apiVersion: projectcalico.org/v3
kind: GlobalNetworkSet
metadata:
  name: {}
  labels:
    cloud-provider: {}
    cloud-service: {}
spec:
  nets:
{}
---'''

    nets_template: str = '  - {}'

    def __init__(self):
        pass

    def _get_single_entry(self, service: str, ip_prefixes: list, cloud_provider: str)-> str:
        nets = '\n'.join([self.nets_template.format(net) for net in ip_prefixes])
        entry = self.yaml_template.format(service, cloud_provider, service, nets)
        return entry

    def transform(self, input: str) -> str:
        """
        :param input: Data to be transformed
        :return: Transformed data
        """
        return input


class AwsTransformer(Transformer):

    def __init__(self):
        super().__init__()

    def transform(self, input: str) -> str:
        """
        :param input: Data to be transformed
        :return: Transformed data
        """
        d = json.loads(input)
        service_nets_map = dict()
        for prefix in d['prefixes']:
            unformatted_service: str = prefix['service']
            # names in the YAML file will not have underscores or uppercase letters
            service = unformatted_service.replace('_', '-').lower()
            ip_prefix: str = prefix['ip_prefix']
            if service not in service_nets_map:
                service_nets_map[service] = list()
            service_nets_map[service].append(ip_prefix)
        transform_list = list()
        for s in service_nets_map.keys():
            transform_list.append(self._get_single_entry(s, service_nets_map[s], 'aws'))
        return ''.join(transform_list)


class AzureTransformer(Transformer):

    def __init__(self):
        super().__init__()

    def transform(self, input: str) -> str:
        """
        :param input: Data to be transformed
        :return: Transformed data
        """
        d = json.loads(input)
        transform_list = list()
        for v in d['values']:
            unformatted_service: str = v['name']
            # names in the YAML file will not have periods or uppercase letters
            service = unformatted_service.replace('.', '-').lower()
            properties = v['properties']
            entry = self._get_single_entry(service, properties['addressPrefixes'], 'azure')
            transform_list.append(entry)
        return  ''.join(transform_list)
