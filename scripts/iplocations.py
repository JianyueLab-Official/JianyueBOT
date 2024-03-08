import requests

def iplocations(ipaddress):
    url = "http://ip-api.com/json/"

    response = requests.get(url + ipaddress)
    data = response.json()

    try:
        if data["status"] == "success":
            result = {
                "query": data["query"],
                "country": data["country"],
                "city": data["city"],
                "zip": data["zip"], 
                "isp": data["isp"],
                "org": data["org"],
                "timezone": data["timezone"], 
                "as": data["as"]
            }
            return result
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while processing the request: {e}")
        return None