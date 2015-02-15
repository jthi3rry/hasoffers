import unittest
from tests import mocks
from hasoffers.api import Client, BrandClient, AffiliateClient


class TestBrandAPI(unittest.TestCase):

    def setUp(self):
        self.client = BrandClient("token", "id")

    def test_client(self):
        self.assertEqual("token", self.client.network_token)
        self.assertEqual("id", self.client.network_id)

    def test_backward_compatibility(self):
        self.assertIsInstance(Client("token", "id"), BrandClient)

    def test_auth_params(self):
        self.assertEqual({"NetworkToken": "token", "NetworkId": "id"}, self.client.get_auth_params())

    @mocks.patch_response(mocks.APPLICATION_FINDALLOFFERCATEGORIES_SUCCESS)
    def test_request(self, response_data):
        response = self.client.request("Application", "findAllOfferCategories",
                                       fields=["id", "name", "status"],
                                       sort={"name": "asc"})

        self.assertTrue(response.success)
        self.assertDictEqual(response_data, response.raw)
        self.assertEqual(response_data['request']['Target'], response.target)
        self.assertEqual(response_data['request']['Method'], response.method)
        self.assertEqual(response_data['request']['Version'], response.version)
        self.assertEqual(response_data['response']['status'], response.status)
        self.assertEqual(response_data['response']['errors'], response.errors)
        self.assertDictEqual(response_data['response']['data'], response.data)

    @mocks.patch_response(mocks.CONVERSION_FINDALL_SUCCESS)
    def test_request_with_filters(self, response_data):
        response = self.client.request("Conversion", "findAll",
                                       page="1",
                                       limit="100",
                                       fields=["id", "payout", "revenue"],
                                       sort={"datetime": "asc"},
                                       filters={
                                           "OR": {
                                               "advertiser_id": [444, 555],
                                               "revenue": {"GREATER_THAN_OR_EQUAL_TO": 100}
                                           },
                                           "user_agent": {"LIKE": "%AppleWebKit%"},
                                           "affiliate_id": 111
                                       })

        self.assertTrue(response.success)
        self.assertDictEqual(response_data, response.raw)
        self.assertEqual(response_data['request']['Target'], response.target)
        self.assertEqual(response_data['request']['Method'], response.method)
        self.assertEqual(response_data['request']['Version'], response.version)
        self.assertEqual(response_data['response']['status'], response.status)
        self.assertEqual(response_data['response']['errors'], response.errors)
        self.assertDictEqual(response_data['response']['data'], response.data)


class TestAffiliateAPI(unittest.TestCase):

    def setUp(self):
        self.client = AffiliateClient("key", "id")

    def test_client(self):
        self.assertEqual("key", self.client.api_key)
        self.assertEqual("id", self.client.network_id)

    def test_auth_params(self):
        self.assertEqual({"api_key": "key", "NetworkId": "id"}, self.client.get_auth_params())

    @mocks.patch_response(mocks.AFFILIATE_AFFILIATE_FINDBYID_SUCCESS)
    def test_request(self, response_data):
        response = self.client.request("Affiliate_Affiliate", "findById")

        self.assertTrue(response.success)
        self.assertDictEqual(response_data, response.raw)
        self.assertEqual(response_data['request']['Target'], response.target)
        self.assertEqual(response_data['request']['Method'], response.method)
        self.assertEqual(response_data['request']['Version'], response.version)
        self.assertEqual(response_data['response']['status'], response.status)
        self.assertEqual(response_data['response']['errors'], response.errors)
        self.assertDictEqual(response_data['response']['data'], response.data)
