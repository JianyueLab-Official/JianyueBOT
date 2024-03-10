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
    
def registrar(registrar, order):
    url = "https://www.nazhumi.com/api/v1?"
    
    response = requests.get(url + "&order=" + str(order) + "&resgitrar=" + str(registrar))
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
                
                "domain_3": data["data"]["price"][2]["domain"],
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
                "transfer_5": data["data"]["price"][4]["transfer"],
                "currency_5": data["data"]["price"][4]["currency"],
            }
            return result
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while processing the request: {e}")
        return None