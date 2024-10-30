import pandas as pd
import requests

base_url = "http://localhost:5020/api"

def callApi():
    url = base_url + '/run'
    response = requests.request("GET", url)
    print(response)
    print(response.text)

callApi()