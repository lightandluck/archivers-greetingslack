import websocket
import json
import requests
import urllib
import os
import logging

logging.basicConfig(level=logging.DEBUG,
        stream=sys.stdout)

# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###VARIABLES THAT YOU NEED TO SET MANUALLY IF NOT ON HEROKU#####
try:
        MESSAGE = os.environ['WELCOME-MESSAGE']
        TOKEN = os.environ['SLACK-TOKEN']
        UNFURL = os.environ['UNFURL-LINKS']
except:
        MESSAGE = 'Manually set the Message if youre not running through heroku or have not set vars in ENV'
        TOKEN = 'Manually set the API Token if youre not running through heroku or have not set vars in ENV'
        UNFURL = 'FALSE'
###############################################################

def is_team_join(msg):
    return msg['type'] == "team_join"

def is_debug_channel_join(msg):
    return msg['type'] == "channel_joined" and msg['channel']['name'] == 'greetingslack'

def parse_join(message):
    m = json.loads(message)
    if is_team_join(m) or is_debug_channel_join(m):
        x = requests.get("https://slack.com/api/im.open?token="+TOKEN+"&user="+m["user"]["id"])
        print(x)
        x = x.json()
        print(x)
        x = x["channel"]["id"]
        print(x)
        if (UNFURL.lower() == "false"):
          xx = requests.post("https://slack.com/api/chat.postMessage?token="+TOKEN+"&channel="+x+"&text="+urllib.quote(MESSAGE)+"&parse=full&as_user=true&unfurl_links=false")
          print(xx)
        else:
          xx = requests.post("https://slack.com/api/chat.postMessage?token="+TOKEN+"&channel="+x+"&text="+urllib.quote(MESSAGE)+"&parse=full&as_user=true")
          print(xx)
        logging.debug('\033[91m' + "HELLO SENT" + m["user"]["id"] + '\033[0m')

#Connects to Slacks and initiates socket handshake
def start_rtm():
    r = requests.get("https://slack.com/api/rtm.start?token="+TOKEN, verify=False)
    r = r.json()
    logging.debug(r)
    r = r["url"]
    return r

def on_message(ws, message):
    parse_join(message)

def on_error(ws, error):
    logging.error("SOME ERROR HAS HAPPENED:" + error)

def on_close(ws):
    logging.info('\033[91m'+"Connection Closed"+'\033[0m')

def on_open(ws):
    logging.info("Connection Started - Auto Greeting new joiners to the network")


if __name__ == "__main__":
    r = start_rtm()
    ws = websocket.WebSocketApp(r, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.run_forever()

