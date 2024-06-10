#!/usr/bin/python3

import json
import requests
import platform

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
            user = colorcodeparser(playerlist['players'][i]['name']), 
            uuid = colorcodeparser(playerlist['players'][i]['uuid']), 
            xcoord = colorcodeparser(str(playerlist['players'][i]['x'])),
            ycoord = colorcodeparser(str(playerlist['players'][i]['y'])),
            zcoord = colorcodeparser(str(playerlist['players'][i]['z']))
        ))

def chat():
    listfmt = "{display}: {message}"
    #param = {'startUnixTime': '1716850600'}
    playerlist = json.loads(json.dumps(requests.get('http://api.retromc.org/api/v1/server/chat').json()))

    print("\033[94mDisplaying recently sent messages. (does NOT display Discord messages)\033[0m")

    for i in range(0, len(playerlist['messages'])): 
        print(listfmt.format(
            display = colorcodeparser(playerlist['messages'][i]['display_name']), 
            message = colorcodeparser(playerlist['messages'][i]['message'])
        ))

def main():
    print("Welcome to cstats!")
    print("Press 1 to launch playerlist")
    print("Press 2 to launch chat")
    print("This UI is temporary, it will be improved in the next releases")
    choose = input("> ")
    if choose == "1":
        playerlist()
    elif choose == "2":
        chat()
    else:
        print("Invalid option!")
    

if __name__ == '__main__':
    main()
