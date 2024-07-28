#!/usr/bin/python3

import json
import requests
import platform
import sys
from datetime import datetime

version = "0.1.0pre"

if platform.system() == 'Windows':
    # make color codes show up on windows properly, this library is not required on other operating systems
    from colorama import just_fix_windows_console
    just_fix_windows_console()

# not using ccparser for colors everywhere for performance reasons
class colors:
    reset = '\033[0m'
    red = '\033[91m'
    aqua = '\033[96m'
    yellow = '\033[33m'
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

def playerlist():
    listfmt = "{display} | {user} | {uuid} | X:{xcoord}, Y:{ycoord}, Z:{zcoord}"
    request = json.loads(json.dumps(requests.get('http://api.retromc.org/api/v1/server/players').json()))

    print("\033[94mThere are \033[91m" + str(request["player_count"]) + "\033[94m out of a maximum \033[91m100\033[94m players online.\033[0m\n\nOutput format:")
    print("Rank and display name | Username | Player UUID | X coord | Y coord | Z coord\n")

    for i in range(0, request["player_count"]):
        print(listfmt.format(
            display = ccparser(request['players'][i]['display_name']),
            user = request['players'][i]['name'], 
            uuid = request['players'][i]['uuid'], 
            xcoord = str(round(request['players'][i]['x'], 1)),
            ycoord = str(round(request['players'][i]['y'], 1)),
            zcoord = str(round(request['players'][i]['z'], 1))
        ))

    input("\nPress any key to return to main menu.\n")
    main()

def chat():
    listfmt = "{display}: {message}"
    request = json.loads(json.dumps(requests.get('http://api.retromc.org/api/v1/server/chat').json()))

    print("\033[94mDisplaying recently sent messages. (does \033[91mNOT\033[94m display Discord messages)\033[0m")

    for i in range(0, len(request['messages'])): 
        print(listfmt.format(
            display = ccparser(request['messages'][i]['display_name']), 
            message = ccparser(request['messages'][i]['message'])
        ))

    input("\nPress any key to return to main menu.\n")
    main()

def villagelist():
    listfmt = "{name} | {owner} | {villageuuid}"
    request = json.loads(json.dumps(requests.get('http://api.retromc.org/api/v1/village/getVillageList').json()))

    print("Displaying list of all RetroMC villages.\n\nOutput format:")
    print("Village name | Village owner | Village UUID\n")

    for i in range(0, len(request['villages'])): 
        print(listfmt.format(
            name = request['villages'][i]['name'], 
            owner = uuidtousername(request['villages'][i]['owner']),
            villageuuid = request['villages'][i]['uuid']
        ))

    input("\nPress any key to return to main menu.\n")
    main()

def villagedetails():
    print("Enter the village name:")
    village = input("> ").lower()

    request = json.loads(json.dumps(requests.get('http://api.retromc.org/api/v1/village/getVillageList').json()))

    print("\033[94mDisplaying village info.\033[0m")

    for i in range(0, len(request['villages'])): 
        if request['villages'][i]['name'].lower() == village:
            villageuuid = request['villages'][i]['uuid']
            break
    else:
        print("Village not found")
        return

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

    input("\nPress any key to return to main menu.\n")
    main()

def playerstats():
    print("Enter the player name:")
    player = input("> ")

    try:
        playerusernamefixed = fixusernamecase(player)
    except KeyError:
        print("Error: This player does not exist")
        return

    playeruuid = usernametouuid(playerusernamefixed)

    request4 = json.loads(json.dumps(requests.get('https://statistics.johnymuffin.com/api/v1/getUser?serverID=0&uuid=' + playeruuid).json()))

    if "msg" in request4:
        print("Error: This player has not played on RetroMC")
        return

    request = json.loads(json.dumps(requests.get('https://statistics.retromc.org/api/online?username=' + playerusernamefixed).json()))

    print("\033[94mDisplaying player info.\033[0m")

    print("Name: " + playerusernamefixed)
    print("Player UUID: " + playeruuid)
    print("Rank: " + request4["groups"][0])
    print("Money: " + str(round(request4["money"], 2)) + "$\n")

    print("Playtime: " + str(round(request4["playTime"] / 60 / 60, 2)) + " hours")
    print("First join: " + unixtimetotime(request4["firstJoin"]))
    print("Last join: " + unixtimetotime(request4["lastJoin"]))
    print("Join count: " + str(request4["joinCount"]) + "\n")

    # TODO: implement more of these stats

    print("Trust level: " + str(request4["trustLevel"]))
    print("Trust score: " + str(round(request4["trustScore"], 2)))
    
    print("\nOnline: " + str(request["online"]))

    try:
        x = str(request["x"])
        y = str(request["y"])
        z = str(request["z"])

        print("Coordinates:")
        print("X: " + x + " Y: " + y + " Z: " + z)
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
    
    input("\nPress any key to return to main menu.")
    main()


def main():
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

            print("Welcome to " + c.aqua + "cstats v" + version + c.reset + "!")
            print("Type the " + c.aqua + "name of a function " + c.reset + "or its " + c.aqua + "numerical ID " + c.reset + "from the list below and press " + c.aqua + "ENTER\n" + c.reset)
            
            print(c.aqua + "1) "  + c.reset + "playerlist")
            print(c.aqua + "2) "  + c.reset + "chat")
            print(c.aqua + "3) "  + c.reset + "villagelist")
            print(c.aqua + "4) "  + c.reset + "villagedetails")
            print(c.aqua + "5) "  + c.reset + "playerstats (WIP)")
            print(c.aqua + "0) "  + c.reset + "exit")

            print("\nThis program is still a work in progress, report issues to SvGaming")

            choose = input("> ")

        if choose == "1" or choose == "playerlist":
            playerlist()
        elif choose == "2" or choose == "chat":
            chat()
        elif choose == "3" or choose == "villagelist":
            villagelist()
        elif choose == "4" or choose == "villagedetails":
            villagedetails()
        elif choose == "5" or choose == "playerstats":
            playerstats()
        elif choose == "0" or choose == "exit":
            sys.exit(0)
        else:
            print("Invalid option!")

if __name__ == '__main__':
    main()
