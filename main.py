import time 
import requests
import threading
from threading import Lock, Thread
from colorama import Fore, Style, init
import random 
from random import randrange
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import names
import email
from urllib.parse import unquote
from fp.fp import FreeProxy
import dotenv

startup = '''
    ("------------------------------------------------")
    ("Created by @antisaintt")
    ("------------------------------------------------")
'''
print(Fore.MAGENTA, startup)
time.sleep(1)

logo = ''' 
  /$$$$$$   /$$$$$$  /$$$$$$$$ /$$   /$$  /$$$$$$  /$$$$$$$$       /$$$$$$$  /$$     /$$        /$$$$$$  /$$   /$$ /$$$$$$$$ /$$$$$$
 /$$__  $$ /$$__  $$| $$_____/| $$$ | $$ /$$__  $$| $$_____/      | $$__  $$|  $$   /$$/       /$$__  $$| $$$ | $$|__  $$__/|_  $$_/
| $$  \__/| $$  \__/| $$      | $$$$| $$| $$  \__/| $$            | $$  \ $$ \  $$ /$$/       | $$  \ $$| $$$$| $$   | $$     | $$  
|  $$$$$$ |  $$$$$$ | $$$$$   | $$ $$ $$|  $$$$$$ | $$$$$         | $$$$$$$   \  $$$$/        | $$$$$$$$| $$ $$ $$   | $$     | $$  
 \____  $$ \____  $$| $$__/   | $$  $$$$ \____  $$| $$__/         | $$__  $$   \  $$/         | $$__  $$| $$  $$$$   | $$     | $$  
 /$$  \ $$ /$$  \ $$| $$      | $$\  $$$ /$$  \ $$| $$            | $$  \ $$    | $$          | $$  | $$| $$\  $$$   | $$     | $$  
|  $$$$$$/|  $$$$$$/| $$$$$$$$| $$ \  $$|  $$$$$$/| $$$$$$$$      | $$$$$$$/    | $$          | $$  | $$| $$ \  $$   | $$    /$$$$$$
 \______/  \______/ |________/|__/  \__/ \______/ |________/      |_______/     |__/          |__/  |__/|__/  \__/   |__/   |______/
                                                                                                                                    
'''

print(Fore.MAGENTA, logo)

with open('config.json') as json_data:
    config = json.load(json_data)

CONFIG = dotenv.dotenv_values()

catchall = config['catchall']
password = config['password']
url = config['url']
init(autoreset=True)

test1 = int(input("How many accounts would you like to make?: "))
threadMax = int(test1)

class logger:
    printLock = threading.Lock()

def create():
    #proxy
    proxy_no = 0
    proxyObject = FreeProxy(country_id=[CONFIG['LOCATION']], rand=True)
    proxy_list = CONFIG['PROXY'].split('%')
    proxy = {"http": f"http://{proxyObject.get()}"} if proxy_list[0] == "" else {"http": f"http://{proxy_list[proxy_no]}"}
    
    rand_fname = names.get_first_name()
    rand_lname = names.get_last_name()
    global email 
    email = (rand_fname + rand_lname + str('%40') + config['catchall'])
    emails = unquote(email)

    url = "https://www.ssense.com/en-ca/account/register"

    payload="email="+ email +"&password="+ password +"&confirmpassword="+ password +"&gender=Men&source=SSENSE_EN_SIGNUP"
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0',
    'content-type': 'application/x-www-form-urlencoded; charset=utf-8'
    }


    #REQUESTS MADE TO SSENSE
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxy)
    accmade = requests.request("POST", url, headers=headers, data=payload, proxies=proxy)
    account = (accmade.text)

    with logger.printLock:
            print(time.strftime("[%H:%M:%S]") + Fore.YELLOW + '[+] CREATING SESSION')
            print(time.strftime("[%H:%M:%S]") + Fore.GREEN + '[+] CREATING ACCOUNT')

    if account == '{}':
        with logger.printLock:
            print(time.strftime("[%H:%M:%S]") + Fore.GREEN+ '[+] ACCOUNT MADE')
            with open("accounts.txt", "a+") as f:
                f.write(emails + ':' + password + "\n")
                success_message()
                quit()
            
    else:
        with logger.printLock:
            print(time.strftime("[%H:%M:%S]") + Fore.RED + "[+] BLOCKED")

def thread():
    ask = input("Would you like to begin account generation? (y/n)")
    if ask == 'y':
        for i in range (threadMax):
            t = threading.Thread(target=create)
            t.start()
            t.join()
    else:
        quit() 

def success_message():
    webhook = DiscordWebhook(url)
    embed = DiscordEmbed(title='SUCCESSFULLY MADE ACCOUNT', color=65280)
    embed.set_footer(text='SSENSE ACCOUNT GEN BY ANTI', icon_url ='https://pbs.twimg.com/profile_images/1349092456986456069/kaSLUW-r_400x400.jpg')
    embed.set_timestamp()
    embed.add_embed_field(name='EMAIL', value="||"+ email +"||")
    embed.add_embed_field(name='PASSWORD', value='||'+ password +'||')
    webhook.add_embed(embed)
    response = webhook.execute()


thread()
create()
