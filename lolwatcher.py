from riotwatcher import LolWatcher, ApiError
import argparse
import pandas as pd
import requests
import os
import json
import time
from datetime import datetime
import pytz

def riotwatcher_get_instance(api_key = "RGAPI-8720b736-035a-44b6-85dd-78114bfdf2c8"):
    return LolWatcher(api_key)

def riotwatcher_get_summoner_data(lol_watcher, summoner_name = "bergoncio", my_region = "euw1"):
	try:
	    summoner_data = lol_watcher.summoner.by_name(my_region, summoner_name)
	except ApiError as err:
	    if err.response.status_code == 429:
	        print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
	        print('this retry-after is handled by default by the RiotWatcher library')
	        print('future requests wait until the retry-after time passes')
	    elif err.response.status_code == 404:
	        print('Summoner with that name not found.')
	    else:
	        raise
	return summoner_data

def riotwatcher_get_match_data(summoner_data, summoner = "bergoncio", my_region = "euw1", match_id = 'latest'):
    my_matches = lol_watcher.match.matchlist_by_puuid(my_region, summoner_data['puuid'])
    print(my_matches)
    if match_id == 'latest':
    	match_name = my_matches[0] # match id (last from matches)
    	match_data = lol_watcher.match.by_id(my_region, match_name)
    elif match_id in my_matches:
    	match_name = my_region.upper()+"_"+match_id
    	match_data = lol_watcher.match.by_id(my_region, match_name)
    elif match_id == "all":
    	match_data = []
    	match_name = []
    	for match in my_matches:
    		match_name.append(match)
    		match_data.append(lol_watcher.match.by_id(my_region, match))
    else:
    	try:
	    	match_name = my_region.upper()+"_"+match_id
	    	match_data = lol_watcher.match.by_id(my_region, match_name)
    	except:
    		print(f"Match {match_id} does not exist")	
    		exit()
    return match_name, match_data

def riotwatcher_get_match_names(summoner_data, summoner = "bergoncio", my_region = "euw1"):
	return lol_watcher.match.matchlist_by_puuid(my_region, summoner_data['puuid'])

def riotwatcher_match_statistics(match_data):
	participants = []
	for row in match_data['info']['participants']:
		participants_row = {}
		for key in list(row.keys()):
			participants_row[key] = row[key]
		participants.append(participants_row)
	return participants

def riotwatcher_get_match_timeline(match_id, my_region = "euw1"):
	try:
		last_timeline = lol_watcher.match.timeline_by_match(my_region,match_name)
	except requests.HTTPError as e:
		if e.response.status_code == 401:
			print("Unauthorized timeline data")
		if e.response.status_code != 404:  # no timeline data
			print("No timeline data")
			raise
		print(f"Timeline not found for {match_name}")
		last_timeline = {}  # indicate that no timeline data is present
	return last_timeline

def change_timezone(datetime, timezone = "GMT+0", from_timezone = "Europe/Madrid"):
	return pytz.timezone(from_timezone).localize(datetime).astimezone(pytz.timezone(timezone))

def riotwatcher_get_champ(match_data, summoner_name = "bergoncio"):
	for idx, participant in enumerate(match_data["info"]["participants"]):
		if participant["summonerName"] == summoner_name:
			return participant["championName"]
	return "Unknown"

def riotwatcher_get_match_date(match_data):
	timestamp = int(match_data["info"]["gameStartTimestamp"]*1e-3)
	dt = datetime.fromtimestamp(timestamp)
	dt = change_timezone(dt, "GMT+0", "Europe/Madrid")
	date = str(dt).replace(":","-")
	return date, timestamp

def riotwatcher_export_match_data(match_name, match_data, summoner_name = "bergoncio", output_folder = "assets"):
	with open(os.path.join(output_folder,match_name+"_match.json"), "w") as match_file:
		json.dump(match_data, match_file, indent=4)
	print(match_file.name)
	# set name csv_file
	date, timestamp = riotwatcher_get_match_date(match_data)
	champ = riotwatcher_get_champ(match_data, summoner_name)
	date = date.split(" ")[0] # remove time, keep date
	csv_file = f"{summoner_name}({champ})_{date}_{match_name}.csv"
	
	# export participant match statistics in csv
	participants = riotwatcher_match_statistics(match_data)
	df = pd.DataFrame(participants)
	df.to_csv(os.path.join(output_folder,csv_file))
	print(csv_file)

def riotwatcher_export_timeline(match_name, my_region = "euw1", output_folder = "assets"):	
	# Access Match timeline data (json)
	match_timeline = riotwatcher_get_match_timeline(match_name, my_region)
	with open(os.path.join(output_folder,match_name+"_timeline.json"), "w") as timeline_file:
		json.dump(match_timeline, timeline_file, indent=4)
	print(timeline_file.name)

if __name__ == "__main__": # test riotwatcher

	# arg params
	parser = argparse.ArgumentParser(description='LoL Spectator User info')
	parser.add_argument('--output_folder', type=str, default="assets")
	parser.add_argument('--region', type=str, default="euw1")
	parser.add_argument('--summoner_name', type=str, default="bergoncio")
	parser.add_argument('--api_key', type=str, default="RGAPI-8720b736-035a-44b6-85dd-78114bfdf2c8") # get it from https://developer.riotgames.com/
	parser.add_argument('--match_id', type=str, default='all') # get it clicking on match in game historial
	args = parser.parse_args()
	my_region = args.region
	summoner_name = args.summoner_name
	api_key = args.api_key
	output_folder = args.output_folder
	match_id = args.match_id
        os.makedirs(args.output_folder,exist_ok=True)

	# get instances
	lol_watcher = riotwatcher_get_instance(api_key)
	summoner_data = riotwatcher_get_summoner_data(lol_watcher, summoner_name, my_region)

	# Access Match data (json)
	match_name, match_data = riotwatcher_get_match_data(summoner_data, summoner_name, my_region, match_id)
	if match_id == "all":
		match_names = match_name
		match_datas = match_data
		for idx,_ in enumerate(match_names):
			match_name = match_names[idx]
			match_data = match_datas[idx]
			riotwatcher_export_match_data(match_name, match_data, summoner_name, output_folder)
			riotwatcher_export_timeline(match_name, my_region, output_folder)
	else:
		riotwatcher_export_match_data(match_name, match_data, summoner_name, output_folder)
		riotwatcher_export_timeline(match_name, my_region, output_folder)

	# For Riot's API, the 404 status code indicates that the requested data wasn't found and
	# should be expected to occur in normal operation, as in the case of a an
	# invalid summoner name, match ID, etc.
	#
	# The 429 status code indicates that the user has sent too many requests
	# in a given amount of time ("rate limiting").

	# OTHER DATA
	# all objects are returned (by default) as a dict
	# lets see if i got diamond yet (i probably didnt)
	my_ranked_stats = lol_watcher.league.by_summoner(my_region, summoner_data['id'])

	# First we get the latest version of the game from data dragon
	versions = lol_watcher.data_dragon.versions_for_region(my_region)
	champions_version = versions['n']['champion']

	# Lets get some champions
	current_champ_list = lol_watcher.data_dragon.champions(champions_version)



