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
import configparser
import threading
from datetime import datetime
import urllib3.exceptions
import warnings

version = "v0.8.0"

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

def generateconfig(confoption):
    conf = configparser.ConfigParser()
    conf.optionxform = str

    try:
        conf.read(confpath + "config.ini")
    except configparser.MissingSectionHeaderError:
        pass

    try:
        conf["general"]
    except KeyError:
        conf["general"] = {}

    if confoption == "checkForUpdates":
        conf["general"]["checkForUpdates"] = "True"
    elif confoption == "changeWindowTitle":
        conf["general"]["changeWindowTitle"] = "True"
    elif confoption == "defaultSubMenu":
        conf["general"]["defaultSubMenu"] = "None"

    confini = open(confpath + "config.ini", "w")
    conf.write(confini)
    confini.close()

def generateallconfigs():
    generateconfig("checkForUpdates")
    generateconfig("changeWindowTitle")
    generateconfig("defaultSubMenu")

def readconfig(confcategory, confoption):
    global confvalues

    try:
        confvalues
    except NameError:
        confvalues = {}

    conf = configparser.ConfigParser()
    conf.optionxform = str
    try:
        conf.read(confpath + "config.ini")
    except configparser.MissingSectionHeaderError:
        cls()
        print(c.red + "ERROR: Missing section headers! The config file will be reset upon pressing ENTER." + c.reset)
        entertocontinue()
        pass

    try:
        confvalues[confoption] = conf.getboolean(confcategory, confoption)
    except (configparser.NoOptionError, configparser.NoSectionError):
        generateconfig(confoption)
        readconfig(confcategory, confoption)
    except ValueError:
        try:
            confvalues[confoption] = conf.get(confcategory, confoption)
        except ValueError:
            cls()
            print(c.red + "ERROR: Invalid data type for \"" + confoption + "\"! This option must be \"True\" or \"False\"!\nThis option will be reset automatically after you press ENTER." + c.reset)
            entertocontinue()
            generateconfig(confoption)
            readconfig(confcategory, confoption)

def readallconfigs():
    readconfig("general", "checkForUpdates")
    readconfig("general", "changeWindowTitle")
    readconfig("general", "defaultSubMenu")

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

def commaloop(value, separator = ", "):
    if value != 0:
        print(separator, end = "")

def randomquote():
    splashes = [
        "\"GUI soon(tm)\" - samcraft3",
        "\"fer\" - Krissofer",
        "\"chatGPT-free code!\" - samcraft3",
        "\";3\" - ospence5",
        "\"Up to 4 times more Notchcode\" - Krissofer",
        "\"Now with more Notchcode(tm)\" - SvGaming234",
        "\"Maybe RetroMC is the friends we met along the way?\" - Pittofer",
        "\"Jthings are Just better\" - Pittofer",
        "\"guh\" - SvGaming234",
        "\"Coming soon(TM) to theaters and computers near you!\" - Noggisoggi",
        "\"Together, we are RetroMC!\" - Noggisoggi",
        "\"true and real\" - Noggisoggi",
        "\"wb\" - Noggisoggi",
        "\"fer fer\" - Noggisoggi",
        "\"hmmmm\" - Noggisoggi",
        "\"https://wiki.retromc.org/\" - Noggisoggi",
        "\"Now with less Notchcode(TM)\" - Noggisoggi",
        "\"holy\" - Noggisoggi",
        "\"h\" - Noggisoggi",
        "\"how dee feller\" - Noggisoggi",
        "\".;,;.\" - Noggisoggi",
        "\"/vote day\" - Noggisoggi",
        "\"Brown bricks in Minecrap\" - Noggisoggi",
        "\"All hail Scout (not the TF2 one)\" - Noggisoggi",
        "\"Crystallitis and plasmoids? In *my* RetroMC? It's more likely than you think.\" - Noggisoggi",
        "\"Authenticated with uhhhhhh Nodes.\" - Noggisoggi",
        "\"oh god Scout's staring into my soul pleas send help us help you help us all\" - Noggisoggi",
        "\"instructions unclear; found red crystals on the back of head\" - Noggisoggi",
        "\"A certain VC is known to be one of the epicenters of brane rot..\" - Noggisoggi",
        "\"wb\" - Literally everyone on the server",
        "\"/home supersecretduplicationstashferfer\" - SvGaming234",
        "\"ÂÂÂÂÂÂÂÂÂÂÂÂ\" - The RMC player list API for no reason",
        "\"h\" - Ade1ie",
        "\"its ferfer not fer fer\" - SvGaming234",
        "\"the retromc\" - Noggisoggi",
        "\"You cannot afford to kill a Wild_Wolf\" - zavdav",
        "\"Is it C-stats, Cstats, or c-stats, cstats? That is the question.\" - Ade1ie",
        "\"its cstats ferfer\" - SvGaming234",
        "\"MOAR SPLASHES\" - zavdav",
        "\"ChestShopHistory\" - zavdav",
        "\"plugin.getFundamentalsLanguageConfig.getMessage(\"player_not_found_full\");\" - zavdav",
        "\"Is 42 the meaning of life?\" - Jaoheah",
        "\"Jaoheah was here on 10/31/2024 at 10:31 PM ET\" - Jaoheah",
        "\"blue and teal\" - Grassboii",
        "\"glue and seal\" - Grassboii",
        "\"double it and give it to the next person\" - Grassboii",
        "\"so real\" - Grassboii",
        "\"zuh?\" - Grassboii",
        "\"guh?\" - Grassboii",
        "\"free cake!\" - Grassboii",
        "\"/!\\ /!\\\" - Grassboii",
        "\"/kit food\" - Grassboii",
        "\"guys look, it's josh!\" - Grassboii",
        "\"test toast\" - Grassboii",
        "\"guhuhuhuh\" - Grassboii",
        "\"har har har har har har har har har har. har har har har, har har har har...\" - Grassboii",
        "\"plasmoid sighted\" - Grassboii",
        "\"boy dinner recipe: one (1) hot pocket, fifteen (15) doritos\" - Golden_MC",
        "\"svgaming234.github.io/cactus\" - SvGaming234",
        "\"ok\" - ScaryAdmin",
        "\"admin\" - bb771",
        "\"anyone wanna place a hit on someone\" - bb771"
    ]

    print(c.yellow + splashes[random.randint(0, len(splashes) - 1)] + c.reset)


def playerlist():
    request = json.loads(json.dumps(requests.get("https://api.retromc.org/api/v1/server/players").json()))

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
    rmcmenu()

def chat():
    listfmt = "{display}: {message}"
    request = json.loads(json.dumps(requests.get("https://api.retromc.org/api/v1/server/chat").json()))

    print("Displaying recently sent messages. (does " + c.aqua + "NOT" + c.reset + " display Discord messages)\n")

    for i in range(0, len(request["messages"])): 
        # remove Â from display names because the api puts them there for no reason
        displayname = removeweirda(request["messages"][i]["display_name"])

        print(listfmt.format(
            display = ccparser(displayname), 
            message = ccparser(request["messages"][i]["message"])
        ))

    entertocontinue()
    rmcmenu()

def villagelist():
    listfmt = "{name} | {owner} | {villageuuid}"
    request = json.loads(json.dumps(requests.get("https://api.retromc.org/api/v1/village/getVillageList").json()))

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
    rmcmenu()

def villagedetails():
    print("Enter the " + c.aqua + "village name" + c.reset + ":")
    village = input("> ").lower()

    if village == "exit" or village == "0":
        rmcmenu()

    request = json.loads(json.dumps(requests.get("https://api.retromc.org/api/v1/village/getVillageList").json()))

    print("\nDisplaying " + c.aqua + "village details" + c.reset + ".\n")

    for i in range(0, len(request["villages"])): 
        if request["villages"][i]["name"].lower() == village:
            villageuuid = request["villages"][i]["uuid"]
            break
    else:
        cls()
        print(c.red + "Error: Village not found." + c.reset)
        villagedetails()

    request2 = json.loads(json.dumps(requests.get("https://api.retromc.org/api/v1/village/getVillage?uuid=" + villageuuid).json()))
    
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
            commaloop(i)
            print(uuidtousername(request2["assistants"][i]), end="")
    else:
        print("No assistants", end="")

    print("\n\nMembers:")
    if len(request2["members"]) != 0:
        for i in range(0, len(request2["members"])):
            commaloop(i)
            print(uuidtousername(request2["members"][i]), end="")
    else:
        print("No members", end="")

    worldviewer = "\n\nView on world viewer:\nhttps://world.retromc.org/#/" + str(request2["spawn"]["x"])  + "/64/" + str(request2["spawn"]["z"]) +"/-3/"

    if request2["spawn"]["world"] == "retromc":
        worldviewer = worldviewer + "Overworld/overworldday"
    elif request2["spawn"]["world"] == "skylands":
        worldviewer = worldviewer + "Skylands/skylandsday"
    else:
        worldviewer = "\n\nView on world viewer:\nWorld viewer not available for this dimension!"
    
    print(worldviewer)

    print("\nView on J-Stats:\nhttps://statistics.retromc.org/village/" + str(request2["uuid"]))

    entertocontinue()
    rmcmenu()

def playerstats():
    print("Enter the " + c.aqua + "player name" + c.reset + ":")
    player = input("> ")

    if player == "exit" or player == "0":
        rmcmenu()

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

    novillages = False
    if request3["status"] == False and request3["message"] == "no villages for this user":
        novillages = True

    print("\nOwner of villages: ", end="")
    if novillages == True or len(request3["data"]["owner"]) == 0:
        print("None :(")
    else:
        print("")
        for i in range(len(request3["data"]["owner"])):
            print(request3["data"]["owner"][i]["village"] + " (" + request3["data"]["owner"][i]["village_uuid"] + ")")

    print("\nAssistant of villages: ", end="")
    if novillages == True or len(request3["data"]["assistant"]) == 0:
        print("None :(")
    else:
        print("")
        for i in range(len(request3["data"]["assistant"])):
            print(request3["data"]["assistant"][i]["village"] + " (" + request3["data"]["assistant"][i]["village_uuid"] + ")")

    print("\nMember of villages: ", end="")
    if novillages == True or len(request3["data"]["member"]) == 0:
        print("None :(")
    else:
        print("")
        for i in range(len(request3["data"]["member"])):
            print(request3["data"]["member"][i]["village"] + " (" + request3["data"]["member"][i]["village_uuid"] + ")")
    
    print("\nView on J-Stats:\nhttps://statistics.retromc.org/player/" + playeruuid)

    entertocontinue()
    rmcmenu()

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
        rmcmenu()
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

    print("Enter the " + c.aqua + "server IP" + c.reset + " (leave blank for " + c.aqua + "mc.retromc.org" + c.reset + "): ")
    ip = input("> ")

    if ip == "exit" or ip == "0":
        main()
    
    if ip == "":
        ip = "mc.retromc.org"
    
    timedout = False
    pingattempts = 5
    pingresultlist = []
    
    print("\nPinging " + ip + " " + c.aqua + str(pingattempts) + c.reset + " times:\n")

    for i in range(pingattempts):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)

        try:
            start_time = time.time()

            s.connect((ip, 25565))

            ping = time.time() - start_time
            pingresultlist.append(ping)
            print("Ping " + str(i + 1) + " to " + ip + ": " + c.aqua + str(round(ping * 1000, 2)) + c.reset + " ms")

            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except TimeoutError:
            print("Ping " + str(i + 1) + " to " + ip + ": " + c.red + "Timed out" + c.reset)
            timedout = True
        except socket.gaierror:
            cls()
            print(c.red + "Error: Unknown server hostname." + c.reset)
            serverping()

    try:
        print("\nAverage ping: " + c.aqua + str(round(sum(pingresultlist) / len(pingresultlist) * 1000, 2)) + c.reset + " ms")
    except ZeroDivisionError:
        print("\nAverage ping: " + c.red + "All pings timed out. Did you enter the right IP?" + c.reset)

    if timedout:
        print(c.yellow + "\nNOTE: When testing ping multiple times quickly in a row timeouts can start to appear.\nWait a bit and try again." + c.reset)
    
    entertocontinue()
    main()

def capes():
    print("Enter the " + c.aqua + "player name" + c.reset + ":")
    player = input("> ")

    if player == "exit" or player == "0":
        rmcmenu()

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
        rmcmenu()
    else:
        cls()
        print(c.red + "Error: This user is not wearing a BetaEvo cape." + c.reset)
        capes()

def loadingscreen(totalcount, current):
    cls()
    print("Loading server information... (" + c.aqua + str(round(current / totalcount * 100, 1)) + "%" + c.reset + ")")

def sortbycount(infoapi):
    return infoapi["count"]

def ltthread(stopevent, init = False):
    while True:
        if init == True:
            print("Loading server information...")

        if stopevent.is_set():
            break
        request = json.loads(json.dumps(requests.get("https://servers.legacyminecraft.com/api/getStats").json()))

        if init == True:
            totalrequests = request["totalServers"] + 2
            loadingscreen(totalrequests, 2)

        if stopevent.is_set():
            break
        request2 = json.loads(json.dumps(requests.get("https://servers.legacyminecraft.com/api/getGlobalHistory").json()))
        
        serverlist = []
        for i in range(len(request2["servers"])):
            if init == True:
                loadingscreen(totalrequests, i + 3)

            if stopevent.is_set():
                return
            request3 = json.loads(json.dumps(requests.get("https://servers.legacyminecraft.com/api/getPlayersOnline?id=" + str(request2["servers"][i]["id"])).json()))
            request3.update(request2["servers"][i])
            serverlist.append(request3)
        cls()
        serverlist.sort(key = sortbycount, reverse = True)

        print("Total current server count: " + str(request["totalServers"]))
        print("Total of unique user joins: " + str(request["totalUsers"]))
        print("Total users online: " + str(request["totalUsersOnline"]) + "\n")

        if stopevent.is_set():
            break
        for i in range(len(serverlist)):
            print(c.aqua + str(i + 1) + ") " + c.reset + serverlist[i]["name"] + 
            " (" + c.aqua + str(serverlist[i]["count"]) + c.reset + " players online)")

            print("UUID: " + c.aqua + serverlist[i]["uuid"] + c.reset
            + " (ID " + c.aqua + str(serverlist[i]["id"]) + c.reset + ")")

            print("Player list: ", end = "")

            if len(serverlist[i]["players"]) != 0:
                for j in range(len(serverlist[i]["players"])):
                    commaloop(j)
                    print(serverlist[i]["players"][j], end = "")
            else:
                print("No players online :(", end = "")
            
            print("\n")
        print("\nPress " + c.aqua + "ENTER" + c.reset + " to return to main menu.\n")
        if init == True:
            break


def legacytracker():
    stopevent = threading.Event()
    initthread = threading.Thread(target=ltthread, args=(stopevent,True,))
    initthread.start()
    initthread.join()

    loopthread = threading.Thread(target=ltthread, args=(stopevent,False,))
    loopthread.start()

    input()
    stopevent.set()
    loopthread.join()
    main()

def bmcplayerlist():
    # warning disabling required due to this api having a self signed certificate
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)
        request = json.loads(json.dumps(requests.get("https://betamc.org:8080/api/players", verify=False).json()))

    print("There are " + c.aqua + str(request["player_count"]) + c.reset + " out of a maximum " + c.aqua + str(request["max_players"]) + c.reset + " players online.\n\nOutput format:")
    print("Rank and display name | Username | Player UUID\nFirst join | Balance | Playtime\n")

    for i in range(0, request["player_count"]):
        stri = str(i)
        displayname = ccparser(request[stri]["display_name"])

        listfmt = "{display} | {user} | {uuid}\n{firstjoin} | ${balance} | {playtime}h\n"

        print(listfmt.format(
            display = displayname,
            user = request[stri]["username"], 
            uuid = request[stri]["uuid"],
            firstjoin = unixtimetotime(request[stri]["first_join"] / 1000),
            balance = round(request[stri]["balance"], 2),
            playtime = round(request[stri]["playtime"] / 1000 / 60 / 60, 1)
        ))

    entertocontinue()
    bmcmenu()

def asciilogo():
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

def about():
    print("About " + c.aqua + "cstats " + version + c.reset + ":")

    asciilogo()

    print("Unofficial command line based statistics program for RetroMC and BetaMC")

    print("\nCredits:")
    print(c.aqua + "SvGaming" + c.reset + " - Project lead")
    print(c.aqua + "Noggisoggi" + c.reset + " - Creator of player list script which cstats is based on")
    print(c.aqua + "JohnyMuffin" + c.reset + " - Creator of RetroMC and Legacy Tracker related APIs utilized by cstats")
    print(c.aqua + "zavdav" + c.reset + " - Tester, told me about the getUser API, gave ideas for improving the ping feature, creator of BetaMC APIs used by cstats")
    print(c.aqua + "Jaoheah" + c.reset + " - Switched the options around on the menu")

    print("\nGitHub repository: " + c.aqua + "https://github.com/svgaming234/cstats" + c.reset)
    print("Licensed under the MIT license. Read " + c.aqua + "https://github.com/svgaming234/cstats/blob/master/LICENSE" + c.reset + " for more info.")

    entertocontinue()
    main()

def resetcache():
    print("This option resets the UUID-Username cache located at " + c.aqua + confpath + "uuidusernamecache" + c.reset + ". Are you sure you want to reset it?\n")

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

def resetconfig():
    print("This option resets the configuration file located at " + c.aqua + confpath + "config.ini" + c.reset + ". Are you sure you want to reset it?")
    print(c.yellow + "NOTE: This option will also restart the program to make sure all changes are applied.\n" + c.reset)

    print(c.aqua + "1) " + c.reset + "yes")
    print(c.aqua + "0) " + c.reset + "no\n")

    choose = input("> ").lower()

    if choose == "1" or choose == "yes":
        cache = open(confpath + "config.ini", "w")
        cache.close()
        generateallconfigs()
        init()
    elif choose == "0" or choose == "no" or choose == "exit":
        return
    else:
        cls()
        print(c.red + "Error: Invalid option!" + c.reset)
        resetcache()


def options():
    print("Please select an " + c.aqua + "option.\n" + c.reset)

    print(c.aqua + "1) " + c.reset + "resetCache")
    print(c.aqua + "2) " + c.reset + "resetConfig")
    print(c.aqua + "0) " + c.reset + "exit\n")

    choose = input("> ").lower()

    if choose == "1" or choose == "resetcache":
        cls()
        resetcache()
        cls()
        options()
    if choose == "2" or choose == "resetconfig":
        cls()
        resetconfig()
        cls()
        options()
    elif choose == "0" or choose == "exit":
        main()
    else:
        cls()
        print(c.red + "Error: Invalid option!" + c.reset)
        options()

def init():
    generatefilestructure()
    readallconfigs()

    if confvalues["changeWindowTitle"] == True:
        setwindowtitle("cstats " + version)
    
    global latestversionstr
    latestversionstr = ""

    if confvalues["checkForUpdates"] == True:
        try:
            request = requests.head("https://github.com/svgaming234/cstats/releases/latest", allow_redirects=True, timeout = 3)
            latestversion = request.url.split("/")[-1]
        except requests.exceptions.Timeout:
            latestversionstr = c.red + "Failed to check for updates (timed out)! Please check your internet connection." + c.reset
        except requests.exceptions.ConnectionError:
            latestversionstr = c.red + "Failed to check for updates (connection error)! Please check your internet connection." + c.reset
        except:
            latestversionstr = c.red + "Failed to check for updates (unspecified error)! Please check your internet connection." + c.reset
            
        if version != latestversion:
            latestversionstr = c.yellow + "A new version is available! Please update to " + latestversion + c.reset

    main()

def rmcmenu():
    cls()

    while True:
        print(latestversionstr, end="")

        asciilogo()

        randomquote()

        print("Welcome to " + c.aqua + "cstats " + version + c.reset + "!")
        print("Type the " + c.aqua + "name of a function " + c.reset + "or its " + c.aqua + "numerical ID " + c.reset + "from the list below and press " + c.aqua + "ENTER\n" + c.reset)
        print(c.aqua + "RetroMC" + c.reset + " menu\n")

        print(c.aqua + "1) " + c.reset + "playerlist")
        print(c.aqua + "2) " + c.reset + "chat")
        print(c.aqua + "3) " + c.reset + "villagelist")
        print(c.aqua + "4) " + c.reset + "villagedetails")
        print(c.aqua + "5) " + c.reset + "playerstats")
        print(c.aqua + "6) " + c.reset + "leaderboard")
        print(c.aqua + "7) " + c.reset + "capes")
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
        elif choose == "0" or choose == "exit":
            main()
        else:
            cls()
            print(c.red + "Error: Invalid option!" + c.reset)

def bmcmenu():
    cls()

    while True:
        print(latestversionstr, end="")

        asciilogo()

        randomquote()

        print("Welcome to " + c.aqua + "cstats " + version + c.reset + "!")
        print("Type the " + c.aqua + "name of a function " + c.reset + "or its " + c.aqua + "numerical ID " + c.reset + "from the list below and press " + c.aqua + "ENTER\n" + c.reset)
        print(c.aqua + "BetaMC" + c.reset + " menu\n")

        print(c.aqua + "1) " + c.reset + "playerlist")
        print(c.aqua + "0) " + c.reset + "exit")

        print("\nThis program is still a work in progress, report issues to SvGaming")

        choose = input("> ").lower()

        if choose == "1" or choose == "playerlist":
            cls()
            bmcplayerlist()
        elif choose == "0" or choose == "exit":
            main()
        else:
            cls()
            print(c.red + "Error: Invalid option!" + c.reset)

def main():
    cls()
    global argused
    global confargused
    while True:
        try:
            argused
            confargused
        except NameError:
            argused = False
            confargused = False

        if len(sys.argv) > 1 and argused == False:
            choose = sys.argv[1]
            argused = True
        elif confvalues["defaultSubMenu"].lower() != "none" and argused == False and confargused == False:
            choose = confvalues["defaultSubMenu"]
            confargused = True
        elif argused == True:
            sys.exit(0)
        else:
            print(latestversionstr, end="")

            asciilogo()

            randomquote()

            print("Welcome to " + c.aqua + "cstats " + version + c.reset + "!")
            print("Type the " + c.aqua + "name of a function " + c.reset + "or its " + c.aqua + "numerical ID " + c.reset + "from the list below and press " + c.aqua + "ENTER\n" + c.reset)

            print(c.aqua + "Main" + c.reset + " menu, select a " + c.aqua + "server" + c.reset + " to view stats specific to it\n")

            print(c.aqua + "1) " + c.reset + "retromc")
            print(c.aqua + "2) " + c.reset + "betamc")
            print(c.aqua + "3) " + c.reset + "serverping")
            print(c.aqua + "4) " + c.reset + "legacytracker")
            print(c.aqua + "8) " + c.reset + "options")
            print(c.aqua + "9) " + c.reset + "about")
            print(c.aqua + "0) " + c.reset + "exit")

            print("\nThis program is still a work in progress, report issues to SvGaming")

            choose = input("> ").lower()

        if choose == "1" or choose == "retromc":
            rmcmenu()
            cls()
        elif choose == "2" or choose == "betamc":
            bmcmenu()
            cls()
        elif choose == "3" or choose == "serverping":
            cls()
            serverping()
        elif choose == "4" or choose == "legacytracker":
            cls()
            legacytracker()
        elif choose == "8" or choose == "options":
            cls()
            options()
        elif choose == "9" or choose == "about":
            cls()
            about()
        elif choose == "0" or choose == "exit":
            if confvalues["changeWindowTitle"] == True:
                setwindowtitle("")
            sys.exit(0)
        else:
            cls()
            print(c.red + "Error: Invalid option!" + c.reset)

if __name__ == "__main__":
    init()
