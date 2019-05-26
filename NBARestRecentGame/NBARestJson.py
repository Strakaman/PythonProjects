import requests
import json
import os
import time

SEC_IN_A_DAY = 86400
SEC_IN_A_WEEK = 604800
PLAYER_CACHE_PATH = "playerFile.json"
TEAMS_CACHE_PATH = "teamsFile.json"



def rest_update_player_list():
    p_list_response = requests.get('http://data.nba.net/prod/v1/2018/players.json')
    player_list = json.loads(p_list_response.content)["league"]["standard"]
    player_dict = {}
    for player in player_list:
        id = player["personId"]
        player_dict[id] = {}
        player_dict[id]["name"] = player["firstName"] + " " + player["lastName"]
        player_dict[id]["pos"] = player["pos"]
    player_file = open(PLAYER_CACHE_PATH, 'w')
    json.dump(player_dict, player_file, sort_keys=True, indent=4)
    return player_dict

def rest_update_teams_list():
    t_list_response = requests.get('http://data.nba.net/prod/v1/2018/teams.json')
    teams_list = json.loads(t_list_response.content)["league"]["standard"]
    teams_dict = {}
    for team in teams_list:
        teamId = team["teamId"]
        teams_dict[teamId] = {}
        teams_dict[teamId]["tricode"] = team["tricode"]
        teams_dict[teamId]["name"] = team["fullName"]
    teams_file = open(TEAMS_CACHE_PATH, 'w')
    json.dump(teams_dict, teams_file, sort_keys=True, indent=4)
    return teams_dict

def get_player_list():
    exists = os.path.isfile(PLAYER_CACHE_PATH)
    if exists:
        currTime = (time.time())
        fileTime = os.path.getmtime(PLAYER_CACHE_PATH)
        diff = currTime - fileTime
        print("Seconds since last player list pull: " + str(diff))
        if  (int(diff) < SEC_IN_A_DAY):
            print("No need for new file. Reading local file")
            return json.loads(open(PLAYER_CACHE_PATH,"rt").read())
    #file either didn't exist or is too old to be reliable
    print("new file needed lets get it")
    return rest_update_player_list()

def get_team_list():
    exists = os.path.isfile(TEAMS_CACHE_PATH)
    if exists:
        currTime = (time.time())
        fileTime = os.path.getmtime(TEAMS_CACHE_PATH)
        diff = currTime - fileTime
        print("Seconds since last teams list pull: " + str(diff))
        if  (int(diff) < SEC_IN_A_DAY):
            print("No need for new file. Reading local file")
            return json.loads(open(TEAMS_CACHE_PATH,"rt").read())
    #file either didn't exist or is too old to be reliable
    print("new file needed lets get it")
    return rest_update_teams_list()

def formatted_team_score(t_dict, team):
    resString = t_dict[team["teamId"]]["tricode"] + " " + team["score"]
    if team["isWinner"]:
        return  resString + " W"
    else:
        return  resString + " L"

def analyze_game_result(g_data):
    home_team = g_data["basicGameData"]["hTeam"]
    visi_team = g_data["basicGameData"]["vTeam"]
    if int(visi_team["score"]) > int(home_team["score"]):
        visi_team["isWinner"] = True
        home_team["isWinner"] = False
    else:
        home_team["isWinner"] = True
        visi_team["isWinner"] = False
    home_team["players"] = []
    visi_team["players"] = []
    for player in g_data["stats"]["activePlayers"]:
        if player["teamId"] == home_team["teamId"]:
            home_team["players"].append(player)
        else:
            visi_team["players"].append(player)

def formatted_player_score(team, player_index):
    if player_index < len(team["players"]):
        currPlayer = team["players"][player_index]
        return p_dictionary[currPlayer["personId"]]["name"].ljust(25) + " " + currPlayer["points"].ljust(6)
    return ""

def print_game_results(g_data):
    print("\n" + "-"*33 +"Game Results" + "-"*33)
    delimiter = "      |       "
    print(" "*15+formatted_team_score(t_dictionary,g_data["basicGameData"]["hTeam"])+" "*8+delimiter + " "*15+formatted_team_score(t_dictionary,g_data["basicGameData"]["vTeam"]))
    #hrange = len(g_data["hTeam"]["players"])
    #if len(g_data["vTeam"]["players"]) > range:
    length = max(len(g_data["basicGameData"]["hTeam"]["players"]),len(g_data["basicGameData"]["vTeam"]["players"]))
    print("Name".ljust(25) +" Points"+delimiter+"Name".ljust(25) +" Points")
    for i in range(length):
        print(formatted_player_score(g_data["basicGameData"]["hTeam"],i) + delimiter + formatted_player_score(g_data["basicGameData"]["vTeam"],i))
    print()



def get_game_result():
    response = requests.get('http://data.nba.net/prod/v1/20190525/0041800306_boxscore.json')
    if not response.ok:
        print(
            "Error, could not reach NBA Stats Page. NBA Stats server may be down or there is no connection to internet")
        return
    gameData = json.loads(response.content)
    analyze_game_result(gameData)  # analyze data to determine winners and build team list
    print("Date: " + gameData["basicGameData"]["startDateEastern"])
    print("Lead Changes: " + gameData["stats"]["leadChanges"])
    print("Quick Nugget: " + gameData["basicGameData"]["nugget"]["text"])
    # print(response.content.decode('UTF-8'))
    # print(response.status_code)
    print_game_results(gameData)

p_dictionary = get_player_list() #player dictionary
t_dictionary = get_team_list() #team dictionary
get_game_result()
#print(t_dictionary)
#print(p_dictionary)




