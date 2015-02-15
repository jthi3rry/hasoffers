=========
HasOffers
=========

.. image:: https://pypip.in/version/hasoffers/badge.svg
    :target: https://pypi.python.org/pypi/hasoffers/

.. image:: https://pypip.in/format/hasoffers/badge.svg
    :target: https://pypi.python.org/pypi/hasoffers/

.. image:: https://travis-ci.org/OohlaLabs/hasoffers.svg?branch=master
    :target: https://travis-ci.org/OohlaLabs/hasoffers

.. image:: https://coveralls.io/repos/OohlaLabs/hasoffers/badge.png?branch=master
    :target: https://coveralls.io/r/OohlaLabs/hasoffers

.. image:: https://pypip.in/py_versions/hasoffers/badge.svg
    :target: https://pypi.python.org/pypi/hasoffers/

.. image:: https://pypip.in/license/hasoffers/badge.svg
    :target: https://pypi.python.org/pypi/hasoffers/

This package provides a Python low-level client for the `HasOffers <http://developers.hasoffers.com/>`_ API.


Installation
------------
::

    pip install hasoffers


Usage Examples
--------------

Instantiate a client with your network token and network id::


    from hasoffers import BrandClient

    client = BrandClient("networktoken", "networkid")

Or for the Affiliate API::

    from hasoffers import AffiliateClient

    client = AffiliateClient("api_key", "network_id")

The general usage to call an API method is ``client.request(target, method, **params)``.

For example, to retrieve all offer categories::


    response = client.request("Application", "findAllOfferCategories",
                              filters={
                                  "status": {"NOT_EQUAL": "deleted"}
                              })

    if response.success:
        # do something with
        response.data


Or to retrieve all conversions for an advertiser::


    response = client.request("Conversion", "findAll",
                              page=1,
                              limit=100,
                              filters={
                                  "advertiser_id": 444,
                              })

    if response.success:
        # do something with
        response.data


To use a combination of OR and AND in filters::


    # Find all conversions where (advertiser_id == 444 OR advertiser_id == 555 OR revenue >= 100) AND user_agent contains "AppleWebKit"
    response = client.request("Conversion", "findAll",
                              page=1,
                              limit=100,
                              filters={
                                  "OR": {
                                      "advertiser_id": [444, 555],
                                      "revenue": {
                                          "GREATER_THAN_OR_EQUAL_TO": 100
                                      }
                                  },
                                  "user_agent": {
                                      "LIKE": "%AppleWebKit%"
                                  }
                              })


Note that a special keyword argument called ``response_class`` can be passed to substitute the default response wrapper. For example::


    from hasoffers import Response


    class CustomResponse(Response):

        def next_page(self):
            return int(self.data.get('page')) + 1

        def has_more(self):
            return int(self.data.get('page')) < int(self.data.get('pageCount'))


    response = client.request("Conversion", "findAll",
                              limit=100,
                              page=1,
                              response_class=CustomResponse)


Running Tests
-------------
::

    tox


Contributions
-------------

All contributions and comments are welcome.

Change Log
----------

v0.2.0
~~~~~~
* Add support for Affiliate API. Thanks `jarradh <https://github.com/jarradh>`_

v0.1.1
~~~~~~
* Switch to Semantic Versioning
* Fix issue with parse_requirements for newer versions of pip (>=6.0.0)

v0.1
~~~~
* Initial
