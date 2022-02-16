# Libraries to interact with computer
import webbrowser
from win10toast_click import ToastNotifier 

# Library for delay
import time

# API interaction
import requests
import json

# Enviroment files
from dotenv import load_dotenv
import os

def make_request(api_key, symbols_str):
    """
    Description: Function to make request to the Yahoo Finnance API,  
    Input: api_key - Valid Key to make requests 
           symbols_str - 3 symbols of market in a string devided by comma.
    Output: Tuple of the 3 symbols requested, the "regularMarketChangePercent" metric.
    """
    url = "https://yfapi.net/v6/finance/quote"
    querystring = {"symbols":symbols_str}
    headers = {
        'x-api-key': api_key
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    vals = json.loads(response.text)
    vals = vals["quoteResponse"]["result"]
    return (vals[0]["regularMarketChangePercent"], vals[1]["regularMarketChangePercent"], vals[2]["regularMarketChangePercent"])

def open_url():
    """
    Description: This function will open the "https://smartrader.io/" page in the browser
    """
    url = "https://smartrader.io/"
    try: 
        webbrowser.open_new(url)
    except: 
        print('No se pudo encontrar la url')
        
if __name__ == "__main__":
    # Access to enviroment variables
    load_dotenv()
    symbols = "^N225,^GDAXI,NDAQ"
    api_key = os.getenv("API_KEY")
    
    #Initialize the notifier
    toaster = ToastNotifier()
    # Request to the Finnance API.
    old_price_N225, old_price_GDAXI, old_price_NDAQ = make_request(api_key, symbols)
    
    # Intializing notification message.
    notification_string = ""
    time.sleep(10)
    
    # Loop to chaeck values and send in case of change.
    while True:
        
        # Extracting new values makin a request to the finnance API.
        new_price_N225, new_price_GDAXI, new_price_NDAQ = make_request(api_key, symbols)
        
        if abs(old_price_N225 - new_price_N225) > .5:
            notification_string += "\nN225\n"
            old_price_N225 = new_price_N225 
            
        if abs(old_price_GDAXI -  new_price_GDAXI) > .5:
            notification_string += "\nGDAXI\n"
            old_price_GDAXI = new_price_GDAXI
            
        if abs(old_price_NDAQ -  new_price_NDAQ) > .5:
            notification_string += "\nNDAQ\n"
            old_price_NDAQ = new_price_NDAQ
    
        # In case there is any change, send the notification to user.
        if notification_string != "": 
            
            
            toaster.show_toast(
                "smarttrader.io",
                "The stock of: " + notification_string + " has changed.", 
                icon_path=None, 
                duration=5, 
                threaded=True, 
                callback_on_click=open_url 
                )
            # Reset the notification string. 
            notification_string = ""
        time.sleep(30)