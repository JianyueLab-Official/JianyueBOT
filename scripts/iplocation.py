import requests

def iplocations(ipaddress):
    url = "https://api.iplocation.net/?ip="

    response = requests.get(url + ipaddress)
    data = response.json()

    try:
        if data["response_code"] == '200':
            result = {
                "ip": data["ip"],
                "ip_number": data["ip_number"],
                "ip_version": data["ip_version"], 
                "country_name": data["country_name"],
                "country_code2": data["country_code2"], 
                "isp": data["isp"],
                "response_code": data["response_code"], 
                "response_message": data["response_message"]
            }
            return result
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while processing the request: {e}")
        return None