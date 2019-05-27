import requests
import json
import os
import datetime

SEC_IN_A_DAY = 86400
PLAYER_CACHE_PATH = "playerFile.json"
TEAMS_CACHE_PATH = "teamsFile.json"
#CALENDAR_CACHE_PATH = "calendarFile.json"
CURR_TIME = ""
ACTIVE_SEASON_YEAR = ""

'''Uses Rest to get the player roster for the year. Caches local json file.'''
def rest_update_player_list():
    p_list_response = requests.get('http://data.nba.net/prod/v1/' + ACTIVE_SEASON_YEAR + '/players.json')
    if not p_list_response.ok:
        print(
            "Error, could not reach NBA Stats Page. NBA Stats server may be down or there is no connection to internet")
        return {}
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

'''Uses Rest to get list of nba teams for the year. Caches local json file'''
def rest_update_teams_list():
    t_list_response = requests.get('http://data.nba.net/prod/v1/' + ACTIVE_SEASON_YEAR +'/teams.json')
    if not t_list_response.ok:
        print(
            "Error, could not reach NBA Stats Page. NBA Stats server may be down or there is no connection to internet")
        return {}
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

'''def rest_update_calendar():
    t_list_response = requests.get('http://data.nba.net/prod/v2/calendar.json')
    result_calendar = json.loads(t_list_response.content)
    calendar_file = open(CALENDAR_CACHE_PATH, 'w')
    json.dump(result_calendar, calendar_file, sort_keys=True, indent=4)
    return result_calendar'''

'''Returns player roster. Compares timestamp of local cache to current time in an effort to reduce number of rest queries needed.'''
def get_player_list():
    exists = os.path.isfile(PLAYER_CACHE_PATH)
    if exists:
        fileTime = os.path.getmtime(PLAYER_CACHE_PATH)
        diff = CURR_TIME.now().timestamp() - fileTime
        if  (int(diff) < SEC_IN_A_DAY):
            print("No need for new roster file. Reading local file")
            return json.loads(open(PLAYER_CACHE_PATH,"rt").read())
    #file either didn't exist or is too old to be reliable
    print("New NBA Roster file needed lets get it")
    return rest_update_player_list()

'''Returns list of nba teams. Compares timestamp of local cache to current time in an effort to reduce number of rest queries needed.'''
def get_team_list():
    exists = os.path.isfile(TEAMS_CACHE_PATH)
    if exists:
        fileTime = os.path.getmtime(TEAMS_CACHE_PATH)
        diff = CURR_TIME.now().timestamp() - fileTime
        if  (int(diff) < SEC_IN_A_DAY):
            print("No need for new team list file. Reading local file")
            return json.loads(open(TEAMS_CACHE_PATH,"rt").read())
    #file either didn't exist or is too old to be reliable
    print("New NBA teams list needed lets get it")
    return rest_update_teams_list()

'''def get_nba_calendar():
    exists = os.path.isfile(CALENDAR_CACHE_PATH)
    if exists:
        fileTime = os.path.getmtime(CALENDAR_CACHE_PATH)
        diff = CURR_TIME - fileTime
        print("Seconds since last calendar pull: " + str(diff))
        if  (int(diff) < SEC_IN_A_DAY):
            print("No need for new calendar. Reading local file")
            return json.loads(open(CALENDAR_CACHE_PATH,"rt").read())
    #file either didn't exist or is too old to be reliable
    print("New calendar needed lets get it")
    return rest_update_calendar()'''

'''Formats the score in a way that associates it with a team nad tells you who won'''
def formatted_team_score(t_dict, team):
    resString = t_dict[team["teamId"]]["tricode"] + " " + team["score"]
    if team["isWinner"]:
        return  resString + " W"
    else:
        return  resString + " L"

'''Adds some extra data to the box score dictionary that would make it easier to interpret the game.
I.e. who won and which player was on which team'''
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

'''Formats the player data (name and score) in a way that's easy to read (left justified and padded)'''
def formatted_player_score(team, player_index):
    if player_index < len(team["players"]):
        currPlayer = team["players"][player_index]
        return p_dictionary[currPlayer["personId"]]["name"].ljust(25) + " " + currPlayer["points"].ljust(6)
    return ""

'''Prints the results of the games and calls formatting functions to do so'''
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

'''Uses Rest to get the box score and print out the results'''
def get_game_result(date,gameID):
    response = requests.get('http://data.nba.net/prod/v1/' + date + '/' + gameID +'_boxscore.json')
    if not response.ok:
        print(
            "Error, could not reach NBA Stats Page. NBA Stats server may be down or there is no connection to internet")
        return
    gameData = json.loads(response.content)
    analyze_game_result(gameData)  # analyze data to determine winners and build team list
    print("\nDate: " + gameData["basicGameData"]["startDateEastern"])
    print("Lead Changes: " + gameData["stats"]["leadChanges"])
    print("Quick Nugget: " + gameData["basicGameData"]["nugget"]["text"])
    # print(response.content.decode('UTF-8'))
    # print(response.status_code)
    print_game_results(gameData)

'''Imperfect logic to figure out which year to query since 
the nba season is the second half of one year and the first half of the following year.
 NBA season typically starts in october around the third Tuesday.'''
def get_nba_year():
    now = CURR_TIME.now()
    yearToUse = now.year
    if now.month >10:
        return yearToUse
    elif now.month == 10 and now.day > 21:
        return yearToUse
    else:
        return yearToUse-1

'''Looks as the list of the games in reverse order, obtains the most recent date of a completed or in progress game,
and then gets the box score for every game that day'''
def get_most_recent_games():
    response = requests.get('http://data.nba.net/prod/v2/' + ACTIVE_SEASON_YEAR +'/schedule.json')
    if not response.ok:
        print(
            "Error, could not reach NBA Stats Page. NBA Stats server may be down or there is no connection to internet")
        return
    schedule = json.loads(response.content)
    gamesR = reversed(schedule["league"]["standard"])
    dateOfRecentGame = ""
    for game in gamesR:
        if game["statusNum"] > 2: #used to check for ==3 but i think a val of 2 means 'in progress' so lets test that theory
            if dateOfRecentGame is "" or dateOfRecentGame==game["startDateEastern"]:
                dateOfRecentGame = str(game["startDateEastern"]) #in case it's still "", set it
                get_game_result(dateOfRecentGame,game["gameId"])
                continue
            else:
                print("Finished getting all of the games for that date")
                break

'''Main Code'''
print("Omari's NBA Game Tracker v1.0")
CURR_TIME = datetime.datetime
ACTIVE_SEASON_YEAR = str(get_nba_year())

p_dictionary = get_player_list() #player dictionary
t_dictionary = get_team_list() #team dictionary
#calendar = get_nba_calendar() #unneeded, use different rest call
get_most_recent_games()

input("Press Enter key to exit...")
#print(t_dictionary)
#print(p_dictionary)




