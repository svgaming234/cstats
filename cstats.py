#!/usr/bin/python3

import json
import requests
import random
import platform
import sys
import subprocess
from datetime import datetime

version = "v0.1.0"

if platform.system() == 'Windows':
    # make color codes show up on windows properly, this library is not required on other operating systems
    from colorama import just_fix_windows_console
    just_fix_windows_console()

    def cls():
        subprocess.run(["cmd.exe", "/c", "cls"])
else:
    def cls():
        subprocess.run("clear")

# not using ccparser for colors everywhere for performance reasons
class colors:
    reset = '\033[0m'
    red = '\033[91m'
    aqua = '\033[96m'
    yellow = '\033[93m'
    white = '\033[39m'

c = colors()

def ccparser(s):
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

def unixtimetotime(unixtime):
    return datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')

def uuidtousername(uuid):
    mojangapiurl = "https://sessionserver.mojang.com/session/minecraft/profile/" + uuid

    cache = open("uuidusernamecache", "r+")
    content = cache.readlines()

    # this code is so janky and unreadable but it works somehow
    for l in content:
        if l.find(uuid) != -1:
            readline = content[content.index(l) - 1]
            return readline[:-1]
    else:
        try:
            request = json.loads(json.dumps(requests.get(mojangapiurl).json()))
            username = request["name"]
        except:
            username = uuid

        cache.write(username + "\n" + uuid + "\n")

    cache.close()

    return username

def usernametouuid(username):
    mojangapiurl = "https://api.mojang.com/users/profiles/minecraft/" + username

    request = json.loads(json.dumps(requests.get(mojangapiurl).json()))
    
    uuid = request["id"]
    uuidwithdashes = uuid[:8] + "-" + uuid[8:12] + "-" + uuid[12:16] + "-" + uuid[16:20] + "-" + uuid[20:]

    return uuidwithdashes

def fixusernamecase(username):
    mojangapiurl = "https://api.mojang.com/users/profiles/minecraft/" + username
    request = json.loads(json.dumps(requests.get(mojangapiurl).json()))

    usernamefixed = request["name"]
    return usernamefixed

def entertocontinue():
    input("\nPress " + c.aqua + "ENTER" + c.reset + " to return to main menu.\n")

def randomquote():
        randchoice = random.randint(1, 3)
        if randchoice == 1:
            print(c.yellow + "\"GUI soon(tm)\" - samcraft3" + c.reset)
        elif randchoice == 2:
            print(c.yellow + "\"fer\" - Krissofer" + c.reset)
        elif randchoice == 3:
            print(c.yellow + "\"chatGPT-free code!\" - samcraft3" + c.reset)
        else:
            print(c.red + "Error: random quote text picking failed" + c.reset)

def playerlist():
    listfmt = "{display} | {user} | {uuid} | X:{xcoord}, Y:{ycoord}, Z:{zcoord}"
    request = json.loads(json.dumps(requests.get('http://api.retromc.org/api/v1/server/players').json()))

    print("There are " + c.aqua + str(request["player_count"]) + c.reset + " out of a maximum " + c.aqua + str(request["max_players"]) + c.reset + " players online.\n\nOutput format:")
    print("Rank and display name | Username | Player UUID | X coord | Y coord | Z coord\n")

    for i in range(0, request["player_count"]):
        # remove Â from display names because the api puts them there for no reason
        displayname = request['players'][i]['display_name'].replace("Â", "")

        print(listfmt.format(
            display = ccparser(displayname),
            user = request['players'][i]['name'], 
            uuid = request['players'][i]['uuid'], 
            xcoord = str(round(request['players'][i]['x'], 1)),
            ycoord = str(round(request['players'][i]['y'], 1)),
            zcoord = str(round(request['players'][i]['z'], 1))
        ))

    entertocontinue()
    main()

def chat():
    listfmt = "{display}: {message}"
    request = json.loads(json.dumps(requests.get('http://api.retromc.org/api/v1/server/chat').json()))

    print("Displaying recently sent messages. (does " + c.aqua + "NOT" + c.reset + " display Discord messages)\n")

    for i in range(0, len(request['messages'])): 
        print(listfmt.format(
            display = ccparser(request['messages'][i]['display_name']), 
            message = ccparser(request['messages'][i]['message'])
        ))

    entertocontinue()
    main()

def villagelist():
    listfmt = "{name} | {owner} | {villageuuid}"
    request = json.loads(json.dumps(requests.get('http://api.retromc.org/api/v1/village/getVillageList').json()))

    print("Displaying list of " + c.aqua + "all" + c.reset + " RetroMC villages.\n\nOutput format:")
    print("Village name | Village owner | Village UUID\n")

    for i in range(0, len(request['villages'])): 
        print(listfmt.format(
            name = request['villages'][i]['name'], 
            owner = uuidtousername(request['villages'][i]['owner']),
            villageuuid = request['villages'][i]['uuid']
        ))

    entertocontinue()
    main()

def villagedetails():
    print("Enter the " + c.aqua + "village name" + c.reset + ":")
    village = input("> ").lower()

    if village == "exit" or village == "0":
        main()

    request = json.loads(json.dumps(requests.get('http://api.retromc.org/api/v1/village/getVillageList').json()))

    print("\nDisplaying " + c.aqua + "village details" + c.reset + ".\n")

    for i in range(0, len(request['villages'])): 
        if request['villages'][i]['name'].lower() == village:
            villageuuid = request['villages'][i]['uuid']
            break
    else:
        cls()
        print(c.red + "Error: Village not found." + c.reset)
        villagedetails()

    request2 = json.loads(json.dumps(requests.get('http://api.retromc.org/api/v1/village/getVillage?uuid=' + villageuuid).json()))
    
    print("Name: " + str(request2["name"]))
    print("Village UUID: " + str(request2["uuid"]))
    print("Owner: " + uuidtousername(request2['owner']))
    print("Location: X:" + str(request2["spawn"]["x"]) + ", Y:" + str(request2["spawn"]["y"]) + ", Z:" + str(request2["spawn"]["z"]) + " in world " + request2["spawn"]["world"])

    if request2['creationTime'] != 1640995200:
        print("Creation time: " + unixtimetotime(request2['creationTime']))
    else:
        print("Creation time: Unknown (likely lost in Towny > JVillage transfer)")
        
    print("Balance: " + str(round(request2["balance"], 2)))
    print("Claim count: " + str(request2["claims"]))
    print("Assistants: " + str(len(request2["assistants"])))
    print("Members: " + str(len(request2["members"])))

    print("\nVillage flags: ")
    print("Members can invite: " + str(request2["flags"]["MEMBERS_CAN_INVITE"]))
    print("Random can alter: " + str(request2["flags"]["RANDOM_CAN_ALTER"]))
    print("Mobs can spawn: " + str(request2["flags"]["MOBS_CAN_SPAWN"]))
    print("Assistant can withdraw: " + str(request2["flags"]["ASSISTANT_CAN_WITHDRAW"]))
    print("Mob spawner bypass: " + str(request2["flags"]["MOB_SPAWNER_BYPASS"]))

    print("\nAssistants:")
    if len(request2["assistants"]) != 0:    
        for i in range(0, len(request2["assistants"])):
            print(uuidtousername(request2["assistants"][i]), end="")
            if len(request2["assistants"]) - 1 != i:
                print(", ", end="")
    else:
        print("No assistants", end="")

    print("\n\nMembers:")
    if len(request2["members"]) != 0:
        for i in range(0, len(request2["members"])):
            print(uuidtousername(request2["members"][i]), end="")
            if len(request2["members"]) - 1 != i:
                print(", ", end="")
    else:
        print("No members", end="")

    # Add newline to the end of the members output
    print("")

    entertocontinue()
    main()

def playerstats():
    print("Enter the " + c.aqua + "player name" + c.reset + ":")
    player = input("> ")

    if player == "exit" or player == "0":
        main()

    try:
        playerusernamefixed = fixusernamecase(player)
    except KeyError:
        cls()
        print(c.red + "Error: A player going by this username does not exist." + c.reset)
        playerstats()

    playeruuid = usernametouuid(playerusernamefixed)

    request4 = json.loads(json.dumps(requests.get('https://statistics.johnymuffin.com/api/v1/getUser?serverID=0&uuid=' + playeruuid).json()))

    if "msg" in request4:
        cls()
        print(c.red + "Error: This player has not played on RetroMC." + c.reset)
        playerstats()

    request = json.loads(json.dumps(requests.get('https://statistics.retromc.org/api/online?username=' + playerusernamefixed).json()))

    print("\nDisplaying " + c.aqua + "player statistics" + c.reset + ".\n")

    print("Name: " + playerusernamefixed)
    print("Player UUID: " + playeruuid)

    if request4["groups"][0] == "wanderer":
        rank = ccparser("&8[&7Wanderer&8]")
    elif request4["groups"][0] == "citizen":
        rank = ccparser("&f[&aCitizen&f]")
    elif request4["groups"][0] == "trusted":
        rank = ccparser("&6[&aCitizen&6]")
    elif request4["groups"][0] == "diamondcitizen":
        rank = ccparser("&b[&aCitizen&b]")
    elif request4["groups"][0] == "hero":
        rank = ccparser("&f[&2Hero&f]")
    elif request4["groups"][0] == "legend":
        rank = ccparser("&f[&9Legend&f]")
    elif request4["groups"][0] == "mystic":
        rank = ccparser("&f[&bMystic&f]")
    elif request4["groups"][0] == "donator":
        rank = ccparser("&8[&cDonator&8]")
    elif request4["groups"][0] == "donator+":
        rank = ccparser("&8[&cDonator&4+&8]")
    elif request4["groups"][0] == "donatorplusplus":
        rank = ccparser("&8[&cDonator&4++&8]")
    elif request4["groups"][0] == "trooper":
        rank = ccparser("&d[trooper]")
    elif request4["groups"][0] == "helper":
        rank = ccparser("&f[&3Helper&f]")
    elif request4["groups"][0] == "trial":
        rank = ccparser("&f[&aTrial Helper&f]")
    elif request4["groups"][0] == "moderator":
        rank = ccparser("&f[&6Moderator&f]")
    elif request4["groups"][0] == "admin":
        rank = ccparser("&f[&4Admin&f]")
    elif request4["groups"][0] == "developer":
        rank = ccparser("&f[&cDeveloper&f]")
    else:
        rank = request4["groups"][0]

    print("Rank: " + rank)
    print("Money: " + str(round(request4["money"], 2)) + "$\n")

    print("Playtime: " + str(round(request4["playTime"] / 60 / 60, 2)) + " hours")
    print("First join: " + unixtimetotime(request4["firstJoin"]))
    print("Last join: " + unixtimetotime(request4["lastJoin"]))
    print("Join count: " + str(request4["joinCount"]) + "\n")

    print("Trust level: " + str(request4["trustLevel"]))
    print("Trust score: " + str(round(request4["trustScore"], 2)))

    print("Player deaths: " + str(request4["playerDeaths"]))
    print("Players killed: " + str(request4["playersKilled"]))
    print("Creatures killed: " + str(request4["creaturesKilled"]))

    print("\nDistance traveled: " + str(request4["metersTraveled"]) + " blocks")
    print("Blocks destroyed: " + str(request4["blocksDestroyed"]))
    print("Blocks placed: " + str(request4["blocksPlaced"]))
    print("Items dropped: " + str(request4["itemsDropped"]))
    
    print("\nOnline: " + str(request["online"]))

    try:
        x = str(request["x"])
        y = str(request["y"])
        z = str(request["z"])

        print("Coordinates:")
        print("X: " + x + ", Y: " + y + ", Z: " + z)
    except:
        print("Coordinates: Player is offline")

    request2 = json.loads(json.dumps(requests.get('https://statistics.retromc.org/api/bans?uuid=' + str(playeruuid)).json()))

    print("\nCurrently banned: " + str(request2["banned"]))
    
    if len(request2["bans"]) == 0:
        print("Ban history: Player has never been banned")
    else:
        print("Ban history:")
        for i in range(len(request2["bans"])):
            banreason = request2["bans"][i]["reason"]

            # remove trailing space on some ban reasons
            if banreason[len(banreason) - 1] == " ":
                banreason = banreason[:-1]

            print("\nBanned for \"" + banreason + "\" by " + request2["bans"][i]["admin"][0])

            print("Pardoned: " + str(request2["bans"][i]["pardoned"]) + ", Ban issue date: " + unixtimetotime(request2["bans"][i]["date"]))

    request3 = json.loads(json.dumps(requests.get('https://statistics.retromc.org/api/user_villages?uuid=' + str(playeruuid)).json()))

    print("\nOwner of villages: ", end="")
    if len(request3["data"]["owner"]) == 0:
        print("None :(")
    else:
        print("")
        for i in range(len(request3["data"]["owner"])):
            print(request3["data"]["owner"][i]["village"] + " (" + request3["data"]["owner"][i]["village_uuid"] + ")")

    print("\nAssistant of villages: ")
    if len(request3["data"]["assistant"]) == 0:
        print("None :(")
    else:
        for i in range(len(request3["data"]["assistant"])):
            print(request3["data"]["assistant"][i]["village"] + " (" + request3["data"]["assistant"][i]["village_uuid"] + ")")

    print("\nMember of villages: ")
    if len(request3["data"]["member"]) == 0:
        print("None :(")
    else:
        for i in range(len(request3["data"]["member"])):
            print(request3["data"]["member"][i]["village"] + " (" + request3["data"]["member"][i]["village_uuid"] + ")")
    
    entertocontinue()
    main()

def init():
    global latestversion
    request = requests.get("https://github.com/svgaming234/cstats/releases/latest")
    latestversion = request.url.split("/")[-1]

    main()

def main():
    cls()
    while(True):
        try:
            argused
        except NameError:
            argused = False
        if len(sys.argv) > 1 and argused == False:
            choose = sys.argv[1]
            argused = True
        else:
            cache = open("uuidusernamecache", "a")
            cache.close()

            if version != latestversion:
                print(c.yellow + "A new version is available! Please update to " + latestversion + c.reset)

            print('''
                      /88                 /88
                      | 88                | 88
  ''' + c.aqua + '''/8888888  ''' + c.reset + '''/8888888 /888888    /888888  /888888   /8888888
 ''' + c.aqua + '''/88_____/ ''' + c.reset + '''/88_____/|_  88_/   |____  88|_  88_/  /88_____/
''' + c.aqua + '''| 88      ''' + c.reset + '''|  888888   | 88      /8888888  | 88   |  888888 
''' + c.aqua + '''| 88       ''' + c.reset + '''\\____  88  | 88 /88 /88__  88  | 88 /88\\____  88
''' + c.aqua + '''|  8888888 ''' + c.reset + '''/8888888/  |  8888/|  8888888  |  8888//8888888/
 ''' + c.aqua + '''\\_______/''' + c.reset + '''|_______/    \\___/   \\_______/   \\___/ |_______/ 
''')

            randomquote()

            print("Welcome to " + c.aqua + "cstats " + version + c.reset + "!")
            print("Type the " + c.aqua + "name of a function " + c.reset + "or its " + c.aqua + "numerical ID " + c.reset + "from the list below and press " + c.aqua + "ENTER\n" + c.reset)
            
            print(c.aqua + "1) "  + c.reset + "playerlist")
            print(c.aqua + "2) "  + c.reset + "chat")
            print(c.aqua + "3) "  + c.reset + "villagelist")
            print(c.aqua + "4) "  + c.reset + "villagedetails")
            print(c.aqua + "5) "  + c.reset + "playerstats")
            print(c.aqua + "0) "  + c.reset + "exit")

            print("\nThis program is still a work in progress, report issues to SvGaming")

            choose = input("> ")

        if choose == "1" or choose == "playerlist":
            cls()
            playerlist()
        elif choose == "2" or choose == "chat":
            cls()
            chat()
        elif choose == "3" or choose == "villagelist":
            cls()
            villagelist()
        elif choose == "4" or choose == "villagedetails":
            cls()
            villagedetails()
        elif choose == "5" or choose == "playerstats":
            cls()
            playerstats()
        elif choose == "0" or choose == "exit":
            sys.exit(0)
        else:
            cls()
            print(c.red + "Error: Invalid option!" + c.reset)

if __name__ == '__main__':
    init()
