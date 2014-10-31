import unittest
from tests import mocks
from hasoffers.api import Client


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = Client("token", "id")

    def test_client(self):
        self.assertEqual("token", self.client.network_token)
        self.assertEqual("id", self.client.network_id)

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
