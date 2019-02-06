import requests
import json
import config
import time

def get_trans():
    lastTxnId = 0;
    while True:
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + config.qiwi_api_access_token
        parameters = {'rows': '10', 'operation': 'IN'}
        h = s.get('https://edge.qiwi.com/payment-history/v1/persons/{qiwi_login}/payments'.format(qiwi_login = config.qiwi_login), params = parameters)
        data = json.loads(h.text)


        for trans in data["data"]:
            if trans["txnId"] > lastTxnId:
                print (trans["status"] == "SUCCESS", trans["sum"]["amount"], trans["sum"]["currency"], trans["comment"])
                pass
            else:
                break
        lastTxnId = data["data"][0]["txnId"]
        time.sleep(3)
        print ("END DATA")

    return

get_trans()