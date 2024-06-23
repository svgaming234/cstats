#!/usr/bin/python3

import json
import requests
import platform
import sys

if platform.system() == 'Windows':
    # make color codes show up on windows properly
    from colorama import just_fix_windows_console
    just_fix_windows_console()

def colorcodeparser(s):
    # this is very jank feeling but it works i guess
    s = s.replace("&", "§")
    
    s = s.replace("§0", "\033[30m")
    s = s.replace("§1", "\033[34m")
    s = s.replace("§2", "\033[32m")
    s = s.replace("§3", "\033[36m")
    s = s.replace("§4", "\033[31m")
    s = s.replace("§5", "\033[35m")
    s = s.replace("§6", "\033[33m")
    s = s.replace("§7", "\033[37m")
    s = s.replace("§8", "\033[90m")
    s = s.replace("§9", "\033[94m")
    s = s.replace("§a", "\033[92m")
    s = s.replace("§b", "\033[96m")
    s = s.replace("§c", "\033[91m")
    s = s.replace("§d", "\033[95m")
    s = s.replace("§e", "\033[93m")
    s = s.replace("§f", "\033[97m")

    s = s + "\033[0m"    
    return s

def playerlist():
    listfmt = "{display} | {user} | {uuid} | X:{xcoord}, Y:{ycoord}, Z:{zcoord}"
    playerlist = json.loads(json.dumps(requests.get('http://api.retromc.org/api/v1/server/players').json()))

    print("\033[94mThere are \033[91m" + str(playerlist["player_count"]) + "\033[94m out of a maximum \033[91m100\033[94m players online.\033[0m")

    for i in range(0, playerlist["player_count"]):
        print(listfmt.format(
            display = colorcodeparser(playerlist['players'][i]['display_name']),
            user = playerlist['players'][i]['name'], 
            uuid = playerlist['players'][i]['uuid'], 
            xcoord = str(round(playerlist['players'][i]['x'], 1)),
            ycoord = str(round(playerlist['players'][i]['y'], 1)),
            zcoord = str(round(playerlist['players'][i]['z'], 1))
        ))

def chat():
    listfmt = "{display}: {message}"
    playerlist = json.loads(json.dumps(requests.get('http://api.retromc.org/api/v1/server/chat').json()))

    print("\033[94mDisplaying recently sent messages. (does NOT display Discord messages)\033[0m")

    for i in range(0, len(playerlist['messages'])): 
        print(listfmt.format(
            display = colorcodeparser(playerlist['messages'][i]['display_name']), 
            message = colorcodeparser(playerlist['messages'][i]['message'])
        ))

def villagelist():
    listfmt = "{name} | {owner}"
    playerlist = json.loads(json.dumps(requests.get('http://api.retromc.org/api/v1/village/getVillageList').json()))

    print("\033[94mDisplaying village list.\033[0m")

    for i in range(0, len(playerlist['villages'])): 
        ownerusernameapiurl = "https://sessionserver.mojang.com/session/minecraft/profile/" + playerlist['villages'][i]['owner']

        try:
            ownerusername = json.loads(json.dumps(requests.get(ownerusernameapiurl).json()))
        except:
            ownerusername = {'name':playerlist['villages'][i]['owner']}


        print(listfmt.format(
            name = colorcodeparser(playerlist['villages'][i]['name']), 
            owner = ownerusername['name']
        ))


def main():
    print("Welcome to cstats!")
    print("Press 1 to launch playerlist")
    print("Press 2 to launch chat")
    print("Press 3 to launch villagelist")
    print("This UI is temporary, it will be improved in the next releases")
    choose = input("> ")
    if choose == "1":
        playerlist()
    elif choose == "2":
        chat()
    elif choose == "3":
        villagelist()
    else:
        print("Invalid option!")
    

if __name__ == '__main__':
    main()
