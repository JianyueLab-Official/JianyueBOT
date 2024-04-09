import requests


def cheapest(tld, order):
    url = "https://www.nazhumi.com/api/v1?"

    response = requests.get(url + "domain=" + str(tld) + "&order=" + str(order))
    data = response.json()

    try:
        if data["code"] == 100:
            result = {
                "domain": data["data"]["domain"],
                "order": data["data"]["order"],
                "reg_1": data["data"]["price"][0]["registrar"],
                "new_1": data["data"]["price"][0]["new"],
                "renew_1": data["data"]["price"][0]["renew"],
                "transfer_1": data["data"]["price"][0]["transfer"],
                "currency_1": data["data"]["price"][0]["currency"],
                "reg_web_1": data["data"]["price"][0]["registrarweb"],

                "reg_2": data["data"]["price"][1]["registrar"],
                "new_2": data["data"]["price"][1]["new"],
                "renew_2": data["data"]["price"][1]["renew"],
                "transfer_2": data["data"]["price"][1]["transfer"],
                "currency_2": data["data"]["price"][1]["currency"],
                "reg_web_2": data["data"]["price"][1]["registrarweb"],

                "reg_3": data["data"]["price"][2]["registrar"],
                "new_3": data["data"]["price"][2]["new"],
                "renew_3": data["data"]["price"][2]["renew"],
                "transfer_3": data["data"]["price"][2]["transfer"],
                "currency_3": data["data"]["price"][2]["currency"],
                "reg_web_3": data["data"]["price"][2]["registrarweb"],

                "reg_4": data["data"]["price"][3]["registrar"],
                "new_4": data["data"]["price"][3]["new"],
                "renew_4": data["data"]["price"][3]["renew"],
                "transfer_4": data["data"]["price"][3]["transfer"],
                "currency_4": data["data"]["price"][3]["currency"],
                "reg_web_4": data["data"]["price"][3]["registrarweb"],

                "reg_5": data["data"]["price"][4]["registrar"],
                "new_5": data["data"]["price"][4]["new"],
                "renew_5": data["data"]["price"][4]["renew"],
                "transfer_5": data["data"]["price"][4]["transfer"],
                "currency_5": data["data"]["price"][4]["currency"],
                "reg_web_5": data["data"]["price"][4]["registrarweb"],
            }
            return result
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while processing the request: {e}")
        return None


def registrar_search(registrar, order):
    url = "https://www.nazhumi.com/api/v1?"

    response = requests.get(url + "registrar=" + str(registrar) + "&order=" + str(order))
    data = response.json()

    try:
        if data["code"] == 100:
            result = {
                "reg": data["data"]["registrar"],
                "order": data["data"]["order"],
                "reg_web": data["data"]["registrarweb"],
                "domain_1": data["data"]["price"][0]["domain"],
                "new_1": data["data"]["price"][0]["new"],
                "renew_1": data["data"]["price"][0]["renew"],
                "transfer_1": data["data"]["price"][0]["transfer"],
                "currency_1": data["data"]["price"][0]["currency"],

                "domain_2": data["data"]["price"][1]["domain"],
                "new_2": data["data"]["price"][1]["new"],
                "renew_2": data["data"]["price"][1]["renew"],
                "transfer_2": data["data"]["price"][1]["transfer"],
                "currency_2": data["data"]["price"][1]["currency"],

                "new_3": data["data"]["price"][2]["new"],
                "renew_3": data["data"]["price"][2]["renew"],
                "transfer_3": data["data"]["price"][2]["transfer"],
                "currency_3": data["data"]["price"][2]["currency"],

                "domain_4": data["data"]["price"][3]["domain"],
                "new_4": data["data"]["price"][3]["new"],
                "renew_4": data["data"]["price"][3]["renew"],
                "transfer_4": data["data"]["price"][3]["transfer"],
                "currency_4": data["data"]["price"][3]["currency"],

                "domain_5": data["data"]["price"][4]["domain"],
                "new_5": data["data"]["price"][4]["new"],
                "renew_5": data["data"]["price"][4]["renew"],
                "transfer_5": data["data"]["pr aice"][4]["transfer"],
                "currency_5": data["data"]["price"][4]["currency"],
            }
            return result
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while processing the request: {e}")
        return None


def ipdetails(ipaddress):
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


def search_zipcode_jp(zipcode):
    url = "https://zipcloud.ibsnet.co.jp/api/search"
    params = {"zipcode": zipcode}

    response = requests.get(url, params=params)
    data = response.json()

    try:
        if data["status"] == 200:
            result = {
                "address1": data["results"][0]["address1"],
                "address2": data["results"][0]["address2"],
                "address3": data["results"][0]["address3"],
                "kana1": data["results"][0]["kana1"],
                "kana2": data["results"][0]["kana2"],
                "kana3": data["results"][0]["kana3"]
            }
            return result
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while processing the request: {e}")
        return None


def minecraftServer(server_type, server_ip):
    if server_type.value == 'java':
        response = requests.get("https://api.mcsrvstat.us/3/" + server_ip)
        data = response.json()

    elif server_type.value == 'bedrock':
        response = requests.get("https://api.mcsrvstat.us/bedrock/3/" + server_ip)
        data = response.json()

    else:
        return None

    if data["online"]:
        result = {
            "ip": data["ip"],
            "port": data["port"],
            "hostname": data["hostname"],
            "version": data["protocol"]["name"],
            "motd": data["motd"]["clean"],
            "ping": data["debug"]["ping"],
            "srv": data["debug"]["srv"],
            "player": data["players"]["online"],
            "maxPlayer": data["players"]["max"]
        }

        return result
