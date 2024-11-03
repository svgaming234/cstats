#!/usr/bin/python3

import json
import requests
import random
import platform
import sys
import subprocess
import os
import errno
import socket
import time
from datetime import datetime

version = "v0.5.0"

def mkdir_p(newdir):
    try: 
        os.makedirs(newdir)
    except OSError as err:
        # reraise the error unless it's about an already existing directory 
        if err.errno != errno.EEXIST or not os.path.isdir(newdir): 
            raise

if platform.system() == "Windows":
    # make color codes show up on windows properly, this library is not required on other operating systems
    from colorama import just_fix_windows_console
    import ctypes
    just_fix_windows_console()

    if os.getenv("APPDATA"):
        confpath = os.getenv("APPDATA") + "\\cstats\\"
    else:
        confpath = "cstats-config\\"

    def setwindowtitle(title):
        ctypes.windll.kernel32.SetConsoleTitleW("cstats " + version)

    def cls():
        subprocess.run(["cmd.exe", "/c", "cls"])
else:
    if os.getenv("XDG_CONFIG_HOME"):
        confpath = os.getenv("XDG_CONFIG_HOME") + "/cstats/"
    elif os.getenv("HOME"):
        confpath = os.getenv("HOME") + "/.config/cstats/"
    else:
        confpath = "./cstats-config/"

    def setwindowtitle(title):
        print("\033]0;" + title + "\007")

    def cls():
        subprocess.run("clear")

# not using ccparser for colors everywhere for performance reasons
class colors:
    # cstats color scheme colors
    reset = "\033[0m"
    red = "\033[91m"
    aqua = "\033[96m"
    yellow = "\033[93m"
    white = "\033[39m"

    # mc colors
    mc0 = "\033[30m"
    mc1 = "\033[34m"
    mc2 = "\033[32m"
    mc3 = "\033[36m"
    mc4 = "\033[31m"
    mc5 = "\033[35m"
    mc6 = "\033[33m"
    mc7 = "\033[37m"
    mc8 = "\033[90m"
    mc9 = "\033[94m"
    mca = "\033[92m"
    mcb = "\033[96m"
    mcc = "\033[91m"
    mcd = "\033[95m"
    mce = "\033[93m"
    mcf = "\033[97m"

c = colors()

def generatefilestructure():
    mkdir_p(confpath)
    mkdir_p(confpath + "capes/")
    cache = open(confpath + "uuidusernamecache", "a")
    cache.close()

def ccparser(s):
    # this is very jank feeling but it works i guess
    s = s.replace("&", "§")
    
    s = s.replace("§0", c.mc0)
    s = s.replace("§1", c.mc1)
    s = s.replace("§2", c.mc2)
    s = s.replace("§3", c.mc3)
    s = s.replace("§4", c.mc4)
    s = s.replace("§5", c.mc5)
    s = s.replace("§6", c.mc6)
    s = s.replace("§7", c.mc7)
    s = s.replace("§8", c.mc8)
    s = s.replace("§9", c.mc9)
    s = s.replace("§a", c.mca)
    s = s.replace("§b", c.mcb)
    s = s.replace("§c", c.mcc)
    s = s.replace("§d", c.mcd)
    s = s.replace("§e", c.mce)
    s = s.replace("§f", c.mcf)

    s = s + c.reset
    return s

def unixtimetotime(unixtime):
    return datetime.fromtimestamp(unixtime).strftime("%Y-%m-%d %H:%M:%S")

def uuidtousername(uuid):
    mojangapiurl = "https://sessionserver.mojang.com/session/minecraft/profile/" + uuid

    cache = open(confpath + "uuidusernamecache", "r+")
    content = cache.readlines()

    # this code is so janky and unreadable but it works somehow
    for i in content:
        if i.find(uuid) != -1:
            readline = content[content.index(i) - 1]
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

def entertocontinue(message = "\nPress " + c.aqua + "ENTER" + c.reset + " to return to main menu.\n"):
    input(message)

def removeweirda(strold):
    # remove Â from display names because the api puts them there for no reason
    strnew = strold.replace("Â", "")
    return strnew

def randomquote():
        randchoice = random.randint(1, 41)
        if randchoice == 1:
            print(c.yellow + "\"GUI soon(tm)\" - samcraft3" + c.reset)
        elif randchoice == 2:
            print(c.yellow + "\"fer\" - Krissofer" + c.reset)
        elif randchoice == 3:
            print(c.yellow + "\"chatGPT-free code!\" - samcraft3" + c.reset)
        elif randchoice == 4:
            print(c.yellow + "\";3\" - ospence5" + c.reset)
        elif randchoice == 5:
            print(c.yellow + "\"Up to 4 times more Notchcode\" - Krissofer" + c.reset)
        elif randchoice == 6:
            print(c.yellow + "\"Now with more Notchcode(tm)\" - SvGaming234" + c.reset)
        elif randchoice == 7:
            print(c.yellow + "\"Maybe RetroMC is the friends we met along the way?\" - Pittofer" + c.reset)
        elif randchoice == 8:
            print(c.yellow + "\"Jthings are Just better\" - Pittofer" + c.reset)
        elif randchoice == 9:
            print(c.yellow + "\"guh\" - SvGaming234" + c.reset)
        elif randchoice == 10:
            print(c.yellow + "\"Coming soon(TM) to theaters and computers near you!\" - Noggisoggi" + c.reset)
        elif randchoice == 11:
            print(c.yellow + "\"Together, we are RetroMC!\" - Noggisoggi" + c.reset)
        elif randchoice == 12:
            print(c.yellow + "\"true and real\" - Noggisoggi" + c.reset)
        elif randchoice == 13:
            print(c.yellow + "\"wb\" - Noggisoggi" + c.reset)
        elif randchoice == 14:
            print(c.yellow + "\"fer fer\" - Noggisoggi" + c.reset)
        elif randchoice == 15:
            print(c.yellow + "\"hmmmm\" - Noggisoggi" + c.reset)
        elif randchoice == 16:
            print(c.yellow + "\"https://wiki.retromc.org/\" - Noggisoggi" + c.reset)
        elif randchoice == 17:
            print(c.yellow + "\"Now with less Notchcode(TM)\" - Noggisoggi" + c.reset)
        elif randchoice == 18:
            print(c.yellow + "\"holy\" - Noggisoggi" + c.reset)
        elif randchoice == 19:
            print(c.yellow + "\"h\" - Noggisoggi" + c.reset)
        elif randchoice == 20:
            print(c.yellow + "\"how dee feller\" - Noggisoggi" + c.reset)
        elif randchoice == 21:
            print(c.yellow + "\".;,;.\" - Noggisoggi" + c.reset)
        elif randchoice == 22:
            print(c.yellow + "\"/vote day\" - Noggisoggi" + c.reset)
        elif randchoice == 23:
            print(c.yellow + "\"Brown bricks in Minecrap\" - Noggisoggi" + c.reset)
        elif randchoice == 24:
            print(c.yellow + "\"All hail Scout (not the TF2 one)\" - Noggisoggi" + c.reset)
        elif randchoice == 25:
            print(c.yellow + "\"Crystallitis and plasmoids? In *my* RetroMC? It's more likely than you think.\" - Noggisoggi" + c.reset)
        elif randchoice == 26:
            print(c.yellow + "\"Authenticated with uhhhhhh Nodes.\" - Noggisoggi" + c.reset)
        elif randchoice == 27:
            print(c.yellow + "\"oh god Scout's staring into my soul pleas send help us help you help us all\" - Noggisoggi" + c.reset)
        elif randchoice == 28:
            print(c.yellow + "\"instructions unclear; found red crystals on the back of head\" - Noggisoggi" + c.reset)
        elif randchoice == 29:
            print(c.yellow + "\"A certain VC is known to be one of the epicenters of brane rot..\" - Noggisoggi" + c.reset)
        elif randchoice == 30:
            print(c.yellow + "\"wb\" - Literally everyone on the server" + c.reset)
        elif randchoice == 31:
            print(c.yellow + "\"/home supersecretduplicationstashferfer\" - SvGaming234" + c.reset)
        elif randchoice == 32:
            print(c.yellow + "\"ÂÂÂÂÂÂÂÂÂÂÂÂ\" - The RMC player list API for no reason" + c.reset)
        elif randchoice == 33:
            print(c.yellow + "\"h\" - Ade1ie" + c.reset)
        elif randchoice == 34:
            print(c.yellow + "\"its ferfer not fer fer\" - SvGaming234" + c.reset)
        elif randchoice == 35:
            print(c.yellow + "\"the retromc\" - Noggisoggi" + c.reset)
        elif randchoice == 36:
            print(c.yellow + "\"You cannot afford to kill a Wild_Wolf\" - zavdav" + c.reset)
        elif randchoice == 37:
            print(c.yellow + "\"Is it C-stats, Cstats, or c-stats, cstats? That is the question.\" - Ade1ie" + c.reset)
        elif randchoice == 38:
            print(c.yellow + "\"its cstats ferfer\" - SvGaming234" + c.reset)
        elif randchoice == 39:
            print(c.yellow + "\"MOAR SPLASHES\" - zavdav" + c.reset)
        elif randchoice == 40:
            print(c.yellow + "\"ChestShopHistory\" - zavdav" + c.reset)
        elif randchoice == 41:
            print(c.yellow + "\"plugin.getFundamentalsLanguageConfig.getMessage(\"player_not_found_full\");\" - zavdav" + c.reset)
        elif randchoice == 42:
            print(c.yellow + "\"Is 42 the meaning of life?\" - Jaoheah" + c.reset)
        elif randchoice == 43:
            print(c.yellow + "\"Jaoheah was here on 10/31/2024 at 10:31 PM ET\" - Jaoheah" + c.reset)    
        else:
            print(c.red + "Error: random quote text picking failed" + c.reset)

def playerlist():
    request = json.loads(json.dumps(requests.get("http://api.retromc.org/api/v1/server/players").json()))

    print("There are " + c.aqua + str(request["player_count"]) + c.reset + " out of a maximum " + c.aqua + str(request["max_players"]) + c.reset + " players online.\n\nOutput format:")
    print("Rank and display name | Username | Player UUID | X coord | Y coord | Z coord\n")

    for i in range(0, request["player_count"]):
        # remove Â from display names because the api puts them there for no reason
        displayname = removeweirda(request["players"][i]["display_name"])

        if request["players"][i]["x"] == 0 and request["players"][i]["y"] == 0 and request["players"][i]["z"] == 0:
            listfmt = "{display} | {user} | {uuid} | Coordinates: Unknown, player is in vanish"

            print(listfmt.format(
                display = ccparser(displayname),
                user = request["players"][i]["name"], 
                uuid = request["players"][i]["uuid"]
            ))
        else:
            listfmt = "{display} | {user} | {uuid} | X:{xcoord}, Y:{ycoord}, Z:{zcoord}"

            print(listfmt.format(
                display = ccparser(displayname),
                user = request["players"][i]["name"], 
                uuid = request["players"][i]["uuid"], 
                xcoord = str(round(request["players"][i]["x"], 1)),
                ycoord = str(round(request["players"][i]["y"], 1)),
                zcoord = str(round(request["players"][i]["z"], 1))
            ))

    entertocontinue()
    main()

def chat():
    listfmt = "{display}: {message}"
    request = json.loads(json.dumps(requests.get("http://api.retromc.org/api/v1/server/chat").json()))

    print("Displaying recently sent messages. (does " + c.aqua + "NOT" + c.reset + " display Discord messages)\n")

    for i in range(0, len(request["messages"])): 
        # remove Â from display names because the api puts them there for no reason
        displayname = removeweirda(request["messages"][i]["display_name"])

        print(listfmt.format(
            display = ccparser(displayname), 
            message = ccparser(request["messages"][i]["message"])
        ))

    entertocontinue()
    main()

def villagelist():
    listfmt = "{name} | {owner} | {villageuuid}"
    request = json.loads(json.dumps(requests.get("http://api.retromc.org/api/v1/village/getVillageList").json()))

    print("Displaying list of " + c.aqua + "all" + c.reset + " RetroMC villages.\n\nOutput format:")
    print("Village name | Village owner | Village UUID\n")

    totalcount = len(request["villages"])
    print("Total village count: " + str(totalcount) + "\n")

    for i in range(0, totalcount): 
        print(listfmt.format(
            name = request["villages"][i]["name"], 
            owner = uuidtousername(request["villages"][i]["owner"]),
            villageuuid = request["villages"][i]["uuid"]
        ))

    print("\nTotal village count: " + str(totalcount))

    entertocontinue()
    main()

def villagedetails():
    print("Enter the " + c.aqua + "village name" + c.reset + ":")
    village = input("> ").lower()

    if village == "exit" or village == "0":
        main()

    request = json.loads(json.dumps(requests.get("http://api.retromc.org/api/v1/village/getVillageList").json()))

    print("\nDisplaying " + c.aqua + "village details" + c.reset + ".\n")

    for i in range(0, len(request["villages"])): 
        if request["villages"][i]["name"].lower() == village:
            villageuuid = request["villages"][i]["uuid"]
            break
    else:
        cls()
        print(c.red + "Error: Village not found." + c.reset)
        villagedetails()

    request2 = json.loads(json.dumps(requests.get("http://api.retromc.org/api/v1/village/getVillage?uuid=" + villageuuid).json()))
    
    print("Name: " + str(request2["name"]))
    print("Village UUID: " + str(request2["uuid"]))
    print("Owner: " + uuidtousername(request2["owner"]))
    print("Location: X:" + str(request2["spawn"]["x"]) + ", Y:" + str(request2["spawn"]["y"]) + ", Z:" + str(request2["spawn"]["z"]) + " in world " + request2["spawn"]["world"])

    if request2["creationTime"] != 1640995200:
        print("Creation time: " + unixtimetotime(request2["creationTime"]))
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

    print("\n\nView on world viewer:\nhttps://world.retromc.org/#/"
     + str(request2["spawn"]["x"])  + "/64/" + str(request2["spawn"]["z"]) +"/-3/")

    print("\nView on J-Stats:\nhttps://j-stats.xyz/village/" + str(request2["uuid"]))

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

    request4 = json.loads(json.dumps(requests.get("https://statistics.johnymuffin.com/api/v1/getUser?serverID=0&uuid=" + playeruuid).json()))

    if "msg" in request4:
        cls()
        print(c.red + "Error: This player has not played on RetroMC." + c.reset)
        playerstats()

    request = json.loads(json.dumps(requests.get("https://statistics.retromc.org/api/online?username=" + playerusernamefixed).json()))

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
        if request["x"] == 0 and request["y"] == 0 and request["z"] == 0:
            print("Coordinates: Unknown, player is in vanish")
        else:
            x = str(request["x"])
            y = str(request["y"])
            z = str(request["z"])

            print("Coordinates: X: " + x + ", Y: " + y + ", Z: " + z)
    except:
        print("Coordinates: Player is offline")

    request2 = json.loads(json.dumps(requests.get("https://statistics.retromc.org/api/bans?uuid=" + str(playeruuid)).json()))

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

    request3 = json.loads(json.dumps(requests.get("https://statistics.retromc.org/api/user_villages?uuid=" + str(playeruuid)).json()))

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
    
    print("\nView on J-Stats:\nhttps://j-stats.xyz/player/" + playeruuid)

    entertocontinue()
    main()

def leaderboard():
    print("Please select a " + c.aqua + "statistic type " + c.reset + "to view its leaderboard.\n")

    print(c.aqua + "1) " + c.reset + "blocksPlaced")
    print(c.aqua + "2) " + c.reset + "blocksDestroyed")
    print(c.aqua + "3) " + c.reset + "metersTraveled")
    print(c.aqua + "4) " + c.reset + "itemsDropped")
    print(c.aqua + "5) " + c.reset + "playerDeaths")
    print(c.aqua + "6) " + c.reset + "playersKilled")
    print(c.aqua + "7) " + c.reset + "creaturesKilled")
    print(c.aqua + "8) " + c.reset + "joinCount")
    print(c.aqua + "9) " + c.reset + "playTime")
    print(c.aqua + "10) " + c.reset + "trustLevel")
    print(c.aqua + "11) " + c.reset + "trustScore")
    print(c.aqua + "12) " + c.reset + "money")
    print(c.aqua + "0) " + c.reset + "exit\n")

    choose = input("> ").lower()

    dataprefix = ""
    datasuffix = ""

    if choose == "1" or choose == "blocksplaced":
        cls()
        stattype = "blocksPlaced"
        datasuffix = " blocks"
    elif choose == "2" or choose == "blocksdestroyed":
        cls()
        stattype = "blocksDestroyed"
        datasuffix = " blocks"
    elif choose == "3" or choose == "meterstraveled":
        cls()
        stattype = "metersTraveled"
        datasuffix = " meters"
    elif choose == "4" or choose == "itemsdropped":
        cls()
        stattype = "itemsDropped"
        datasuffix = " items"
    elif choose == "5" or choose == "playerdeaths":
        cls()
        stattype = "playerDeaths"
        datasuffix = " deaths"
    elif choose == "6" or choose == "playerskilled":
        cls()
        stattype = "playersKilled"
        datasuffix = " kills"
    elif choose == "7" or choose == "creatureskilled":
        cls()
        stattype = "creaturesKilled"
        datasuffix = " kills"
    elif choose == "8" or choose == "joincount":
        cls()
        stattype = "joinCount"
        datasuffix = " joins"
    elif choose == "9" or choose == "playtime":
        cls()
        stattype = "playTime"
    elif choose == "10" or choose == "trustlevel":
        cls()
        stattype = "trustLevel"
        dataprefix = "Level "
    elif choose == "11" or choose == "trustscore":
        cls()
        stattype = "trustScore"
        dataprefix = "Score "
    elif choose == "12" or choose == "money":
        cls()
        stattype = "money"
        dataprefix = "$"
    elif choose == "0" or choose == "exit":
        main()
    else:
        cls()
        print(c.red + "Error: Invalid statistic type!" + c.reset)
        leaderboard()

    request = json.loads(json.dumps(requests.get("https://statistics.retromc.org/api/leaderboard?type=" + stattype).json()))

    print("Leaderboard for " + c.aqua + stattype + c.reset + ":")

    if stattype == "playTime":
        for i in range(len(request["data"])):
            print(str(i + 1) + ". " + request["data"][i]["username"] + " = " + str(round(request["data"][i][stattype] / 60 / 60, 2)) + " hours (" + str(round(request["data"][i][stattype] / 60, 2)) + " minutes)")
    else:
        for i in range(len(request["data"])):
            print(str(i + 1) + ". " + request["data"][i]["username"] + " = "  + dataprefix + str(request["data"][i][stattype]) + datasuffix)

    entertocontinue("\nPress " + c.aqua + "ENTER" + c.reset + " to return to leaderboard menu.\n")
    cls()
    leaderboard()

def serverping():
    print(c.yellow + "WARNING: This feature has very questionable accuracy." + c.reset)
    
    timedout = False
    pingattempts = 5
    pingresultlist = []
    
    print("\nPinging RetroMC " + c.aqua + str(pingattempts) + c.reset + " times:\n")

    for i in range(pingattempts):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)

        try:
            start_time = time.time()

            s.connect(("mc.retromc.org", 25565))

            ping = time.time() - start_time
            pingresultlist.append(ping)
            print("Ping " + str(i + 1) + " to mc.retromc.org: " + c.aqua + str(round(ping * 1000, 2)) + c.reset + " ms")

            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except TimeoutError:
            print("Ping " + str(i + 1) + " to mc.retromc.org: " + c.red + "Timed out" + c.reset)
            timedout = True

    print("\nAverage ping: " + c.aqua + str(round(sum(pingresultlist) / len(pingresultlist) * 1000, 2)) + c.reset + " ms")

    if timedout:
        print(c.yellow + "NOTE: When testing ping multiple times quickly in a row timeouts start to appear.\nWait a bit and try again." + c.reset)
    
    entertocontinue()
    main()

def capes():
    print("Enter the " + c.aqua + "player name" + c.reset + ":")
    player = input("> ")

    if player == "exit" or player == "0":
        main()

    try:
        playerusernamefixed = fixusernamecase(player)
    except KeyError:
        cls()
        print(c.red + "Error: A player going by this username does not exist." + c.reset)
        capes()

    playeruuid = usernametouuid(playerusernamefixed)

    request = requests.get("https://capes.johnymuffin.com/getCape.php?username=" + playerusernamefixed)

    if request.status_code == 200:
        print("Name: " + playerusernamefixed)
        print("Player UUID: " + playeruuid)
        print("\nBetaEvo cape: " + c.aqua + "Yes" + c.reset)

        if platform.system() == "Windows":
            capepath = confpath + "capes\\" + playerusernamefixed + "_cape.png"
        else:
            capepath = confpath + "capes/" + playerusernamefixed + "_cape.png"

        image = open(capepath, "wb")
        image.write(request.content)
        image.close()

        print("\nCape has been saved to " + c.aqua + capepath + c.reset)

        entertocontinue()
        main()
    else:
        cls()
        print(c.red + "Error: This user is not wearing a BetaEvo cape." + c.reset)
        capes()

def about():
    print("About " + c.aqua + "cstats " + version + c.reset + ":")

    print("\nCredits:")
    print(c.aqua + "SvGaming" + c.reset + " - Project lead")
    print(c.aqua + "Noggisoggi" + c.reset + " - Creator of player list script which cstats is based on")
    print(c.aqua + "JohnyMuffin" + c.reset + " - Creator of APIs utilized by cstats")
    print(c.aqua + "zavdav" + c.reset + " - Lead tester, told me about the getUser API, gave ideas for improving the ping feature")
    print(c.aqua + "Jaoheah" + c.reset + " - Switched the options around on the menu")

    print("\nGitHub repository: " + c.aqua + "https://github.com/svgaming234/cstats" + c.reset)
    print("Licensed under the MIT license. Read " + c.aqua + "https://github.com/svgaming234/cstats/blob/master/LICENSE" + c.reset + " for more info.")

    entertocontinue()
    main()

def resetcache():
    print("This option resets the UUID-Username cache located at " + c.aqua + confpath + c.reset + ". Are you sure you want to reset it?\n")

    print(c.aqua + "1) " + c.reset + "yes")
    print(c.aqua + "0) " + c.reset + "no\n")

    choose = input("> ").lower()

    if choose == "1" or choose == "yes":
        cache = open(confpath + "uuidusernamecache", "w")
        cache.close()
    elif choose == "0" or choose == "no" or choose == "exit":
        return
    else:
        cls()
        print(c.red + "Error: Invalid option!" + c.reset)
        resetcache()


def options():
    print("Please select an " + c.aqua + "option.\n" + c.reset)

    print(c.aqua + "1) " + c.reset + "resetCache")
    print(c.aqua + "0) " + c.reset + "exit\n")

    choose = input("> ").lower()

    if choose == "1" or choose == "resetcache":
        cls()
        resetcache()
        cls()
        options()
    elif choose == "0" or choose == "exit":
        main()
    else:
        cls()
        print(c.red + "Error: Invalid option!" + c.reset)
        options()

def init():
    setwindowtitle("cstats " + version)

    global latestversion

    try:
        request = requests.get("https://github.com/svgaming234/cstats/releases/latest")
        latestversion = request.url.split("/")[-1]
    except:
        latestversion = "Error"
    
    generatefilestructure()

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
            if latestversion == "Error":
                print(c.red + "Failed to check for updates! Please check your internet connection." + c.reset)
            elif version != latestversion:
                print(c.yellow + "A new version is available! Please update to " + latestversion + c.reset)

            print("""
                      /88                 /88
                      | 88                | 88
  """ + c.aqua + """/8888888  """ + c.reset + """/8888888 /888888    /888888  /888888   /8888888
 """ + c.aqua + """/88_____/ """ + c.reset + """/88_____/|_  88_/   |____  88|_  88_/  /88_____/
""" + c.aqua + """| 88      """ + c.reset + """|  888888   | 88      /8888888  | 88   |  888888 
""" + c.aqua + """| 88       """ + c.reset + """\\____  88  | 88 /88 /88__  88  | 88 /88\\____  88
""" + c.aqua + """|  8888888 """ + c.reset + """/8888888/  |  8888/|  8888888  |  8888//8888888/
 """ + c.aqua + """\\_______/""" + c.reset + """|_______/    \\___/   \\_______/   \\___/ |_______/ 
""")

            randomquote()

            print("Welcome to " + c.aqua + "cstats " + version + c.reset + "!")
            print("Type the " + c.aqua + "name of a function " + c.reset + "or its " + c.aqua + "numerical ID " + c.reset + "from the list below and press " + c.aqua + "ENTER\n" + c.reset)
            
            print(c.aqua + "1) " + c.reset + "playerlist")
            print(c.aqua + "2) " + c.reset + "chat")
            print(c.aqua + "3) " + c.reset + "villagelist")
            print(c.aqua + "4) " + c.reset + "villagedetails")
            print(c.aqua + "5) " + c.reset + "playerstats")
            print(c.aqua + "6) " + c.reset + "leaderboard")
            print(c.aqua + "7) " + c.reset + "capes")
            print(c.aqua + "8) " + c.reset + "serverping")
            print(c.aqua + "9) " + c.reset + "options")
            print(c.aqua + "10) " + c.reset + "about")
            print(c.aqua + "0) " + c.reset + "exit")

            print("\nThis program is still a work in progress, report issues to SvGaming")

            choose = input("> ").lower()

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
        elif choose == "6" or choose == "leaderboard":
            cls()
            leaderboard()
        elif choose == "7" or choose == "capes":
            cls()
            capes()
        elif choose == "8" or choose == "serverping":
            cls()
            serverping()
        elif choose == "9" or choose == "options":
            cls()
            options()
        elif choose == "10" or choose == "about":
            cls()
            about()
        elif choose == "0" or choose == "exit":
            setwindowtitle("")
            sys.exit(0)
        else:
            cls()
            print(c.red + "Error: Invalid option!" + c.reset)

if __name__ == "__main__":
    init()
