import requests, json
from pprint import pprint
from collections import defaultdict
from thefuzz import fuzz
import pandas as pd

base_url = 'https://fantasy.premierleague.com/api/' 
highest_score = 0
high_scorer_map = defaultdict(list)
gw_results = []
points_map = [10,8,7,6,5,4,3,2,1,0,-1]

def generateResults():
    
    team_data = pd.read_excel("Fpl_gw3.xlsx")
    for index, team in team_data.iterrows():
        generateScoresByLeague(team["League_id"], team["Cap"], team["Sub"])
    
    #Sort the results and print the points.
    gw_results.sort(reverse=True)
    print("\nGame Week results")
    for index, element  in enumerate(gw_results):
        points, team = element[0], element[1]
        print("Team: " + team + " | GW Points: " + str(points) + " | League Points: " + str(points_map[index]))

    #Calculate Top Scorers:
    print("\nTop scorers for this week")
    for player, team in high_scorer_map[highest_score]:
        print("Player: " + player + " from : " + team + " scored: " + str(highest_score)) 


def getPlayerPointsByGW(playerId):
    api_url = f"{base_url}entry/{playerId}/history/"
    r = requests.get(api_url)
    data = r.json()
    current_data = data["current"]
    gw_data = current_data[-1]
    transfer_cost = gw_data["event_transfers_cost"]
    gw_points = gw_data["points"]
    return int(gw_points) - int(transfer_cost)

def generateScoresByLeague(league_id, cap, sub):
    global highest_score 
    league_api_url = f"{base_url}leagues-classic/{league_id}/standings/"
    r = requests.get(league_api_url)
    data = r.json()
    league_name = data["league"]["name"]
    print("Getting results for league : " + league_name + " league_id : " + str(league_id) + " cap: " + cap + ", sub: " + sub)
    total_points = 0
    if 'results' in data["standings"]:
        for result in data["standings"]["results"]:
            playerId, player_name = result["entry"], result["player_name"]
            gw_points = getPlayerPointsByGW(playerId)
            highest_score = max(highest_score, gw_points)
            high_scorer_map[gw_points].append((player_name, league_name))
            if cap == player_name or fuzz.ratio(player_name.lower(), cap) > 70:
                print("Cap id: " + str(playerId) + " Points scored by cap "+ player_name + " : " + str(gw_points))
                total_points +=  gw_points * 2
            elif sub == player_name or fuzz.ratio(player_name.lower(), sub) > 70:
                print("Sub id: " + str(playerId) + " Points scored by sub "+ player_name + " : " + str(gw_points))
                total_points += gw_points * 0.5
            else:
                total_points += gw_points
    gw_results.append((total_points, league_name))

generateResults()