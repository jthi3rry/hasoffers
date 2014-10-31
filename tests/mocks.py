import functools
import json
import responses

def patch_response(response_dict):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            responses.start()
            responses.add(**response_dict)
            result = f(response_data=json.loads(response_dict["body"]), *args, **kwargs)
            responses.stop()
            responses.reset()
            return result
        return wrapper
    return decorator


APPLICATION_FINDALLOFFERCATEGORIES_SUCCESS = {
    "method": responses.GET,
    "match_querystring": True,
    "url": "https://api.hasoffers.com/v3/Application.json?Method=findAllOfferCategories&NetworkToken=token&NetworkId=id&sort%5Bname%5D=asc&fields%5B%5D=id&fields%5B%5D=name&fields%5B%5D=status",
    "status": 200,
    "content_type": "application/json",
    "body": """{
                "request": {
                    "Format": "json",
                    "Method": "findAllOfferCategories",
                    "NetworkId": "id",
                    "NetworkToken": "token",
                    "Service": "HasOffers",
                    "Target": "Application",
                    "Version": "3",
                    "fields": ["id", "name", "status"],
                    "sort": {"name": "asc"}
                },
                "response": {
                    "data": {
                        "2": {
                            "OfferCategory": {
                                "id": "2",
                                "name": "Category1",
                                "status": "active"
                            }
                        },
                        "4": {
                            "OfferCategory": {
                                "id": "4",
                                "name": "Category2",
                                "status": "deleted"
                            }
                        }
                    },
                    "errorMessage": null,
                    "errors": [],
                    "httpStatus": 200,
                    "status": 1
                }
               }""",
}


CONVERSION_FINDALL_SUCCESS = {
    "method": responses.GET,
    "match_querystring": True,
    "url": "https://api.hasoffers.com/v3/Conversion.json?Method=findAll&NetworkToken=token&NetworkId=id&sort%5Bdatetime%5D=asc&filters%5Baffiliate_id%5D=111&filters%5Buser_agent%5D%5BLIKE%5D=%25AppleWebKit%25&filters%5BOR%5D%5Badvertiser_id%5D%5B%5D=444&filters%5BOR%5D%5Badvertiser_id%5D%5B%5D=555&filters%5BOR%5D%5Brevenue%5D%5BGREATER_THAN_OR_EQUAL_TO%5D=100&limit=100&fields%5B%5D=id&fields%5B%5D=payout&fields%5B%5D=revenue&page=1",
    "status": 200,
    "content_type": "application/json",
    "body": """{
                "request": {
                    "Format": "json",
                    "Method": "findAll",
                    "NetworkId": "id",
                    "NetworkToken": "token",
                    "Service": "HasOffers",
                    "Target": "Conversion",
                    "Version": "3",
                    "fields": ["id", "payout", "revenue"],
                    "filters": {
                        "OR": {
                            "advertiser_id": ["444", "555"],
                            "revenue": {"GREATER_THAN_OR_EQUAL_TO": "100"}
                        },
                        "user_agent": {"LIKE": "%AppleWebKit%"},
                        "affiliate_id": "111"
                    },
                    "limit": "100",
                    "page": "1",
                    "sort": {"datetime": "asc"}
                },
                "response": {
                    "data": {
                        "count": 10,
                        "current": 0,
                        "data": {
                            "1230": {"Conversion": {"id": "1230", "payout": "80.00000", "revenue": "100.00000"}},
                            "1231": {"Conversion": {"id": "1231", "payout": "80.00000", "revenue": "100.00000"}},
                            "1232": {"Conversion": {"id": "1232", "payout": "80.00000", "revenue": "100.00000"}},
                            "1233": {"Conversion": {"id": "1233", "payout": "80.00000", "revenue": "100.00000"}},
                            "1234": {"Conversion": {"id": "1234", "payout": "80.00000", "revenue": "100.00000"}},
                            "1235": {"Conversion": {"id": "1235", "payout": "80.00000", "revenue": "100.00000"}},
                            "1236": {"Conversion": {"id": "1236", "payout": "80.00000", "revenue": "100.00000"}},
                            "1237": {"Conversion": {"id": "1237", "payout": "80.00000", "revenue": "100.00000"}},
                            "1238": {"Conversion": {"id": "1238", "payout": "80.00000", "revenue": "100.00000"}},
                            "1239": {"Conversion": {"id": "1239", "payout": "80.00000", "revenue": "100.00000"}}
                        },
                        "page": "1",
                        "pageCount": 1
                    },
                    "errorMessage": null,
                    "errors": [],
                    "httpStatus": 200,
                    "status": 1
                }
            }""",
}
