import requests

__all__ = ['Response', 'Client', 'BrandClient', 'AffiliateClient']


class Response(object):

    def __init__(self, response):
        self.raw = response
        self.target = self.raw["request"]["Target"]
        self.method = self.raw["request"]["Method"]
        self.version = self.raw["request"]["Version"]
        self.format = self.raw["request"]["Format"]
        self.status = self.raw["response"]["status"]
        self.error_message = self.raw["response"]["errorMessage"]
        self.errors = self.raw["response"]["errors"]
        self.data = self.raw["response"]["data"]
        self.success = self.status > 0


class BaseClient(object):

    ENDPOINT = "https://api.hasoffers.com/v3/"

    def get_auth_params(self):  # pragma: nocover
        raise NotImplementedError()

    def _prepare_params(self, **kwargs):
        """
        Prepare params for the get request:
          * key[inner_key]=value (for dictionaries)
          * key[]=value (for lists and tuples)
          * key=value (for everything else)

        Dictionary values are prepared recursively when values are one of list, tuple or dict:
          * key[inner_key][] = value (for lists and tuples)
          * key[inner_key][inner_key2] = value (for dictionaries)

        :param kwargs: query string parameters
        :return dict: flat dictionary with keys prepared for the query string
        """
        params = {}
        for param, value in kwargs.items():
            if isinstance(value, dict):
                params.update(self._prepare_params(**{"{}[{}]".format(param, k): v for k, v in value.items()}))
            elif isinstance(value, (list, tuple)):
                params.update({"{}[]".format(param): value})
            else:
                params.update({param: value})
        return params

    def request(self, target, method, response_class=Response, verb='get', **kwargs):
        """
        Perform a call to the API endpoint

        :param target: hasoffer entity
        :param method: method performed on target
        :param response_class: response class wrapping the raw response
        :param verb: http method to use for the request
        :param kwargs: query string parameters
        :return: instance of response_class
        """
        params = self._prepare_params(**kwargs)
        params.update({"Method": method})
        params.update(self.get_auth_params())
        call = getattr(requests, verb.lower(), getattr(requests, 'get'))
        response = call("{}{}.json".format(self.ENDPOINT, target), params=params)
        return response_class(response.json())


class BrandClient(BaseClient):

    def __init__(self, network_token, network_id):
        """
        Constructor

        :param network_token: hasoffers network token
        :param network_id: hasoffers network id
        """
        self.network_token = network_token
        self.network_id = network_id

    def get_auth_params(self):
        return {"NetworkToken": self.network_token, "NetworkId": self.network_id}

# Backward compatibility
Client = BrandClient


class AffiliateClient(BaseClient):

    def __init__(self, api_key, network_id):
        """
        Constructor

        :param api_key: hasoffers affiliate api key
        :param network_id: hasoffers network id
        """
        self.api_key = api_key
        self.network_id = network_id

    def get_auth_params(self):
        return {"api_key": self.api_key, "NetworkId": self.network_id}
