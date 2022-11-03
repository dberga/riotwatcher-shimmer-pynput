import os
import pandas as pd
import json
import subprocess
import time
import shutil
from parsers import read_csv, read_json, plot_df
import argparse
from datetime import datetime

if __name__ == "__main__": # test parsers

	parser = argparse.ArgumentParser(description='Shimmer + LoL Spectator User info')
	## DATA FOLDER
	parser.add_argument('--input_folder', type=str, default="assets")
	
	## SHIMMER PARAMS
	parser.add_argument('--shimmer_file', type=str, default = "Alex2_shimmer.csv") # Shimmer (HD+EDA) file [csv]
	parser.add_argument('--shimmer_head_row', type=int, default=None) # None, 0, 1
	parser.add_argument('--shimmer_participantcode', type=str, default=None)
	## LOL PARAMS
	parser.add_argument('--timeline_file', type=str, default = "EUW1_5900827429_timeline.json") # LoL match timeline [json]
	parser.add_argument('--match_file', type=str, default = "EUW1_5900827429_match.json") # LoL match data [json]
	# lol (optional) params #
	parser.add_argument('--api_key', type=str, default="RGAPI-d167d546-c88f-48b1-8469-241a96e1b077") # get it from https://developer.riotgames.com/
	parser.add_argument('--region', type=str, default="euw1")
	parser.add_argument('--summoner_name', type=str, default="bergoncio")
	parser.add_argument('--match_id', type=str, default='latest')
	## PYNPUT PARAMS
	parser.add_argument('--pynput_file', type=str, default = None) # LoL match timeline [json]
	args = parser.parse_args()
	print(args)
	# ---------------------------------------------------------------
	# Checking input files
	input_shimmer = os.path.join(args.input_folder,args.shimmer_file)
	input_timeline = os.path.join(args.input_folder,args.timeline_file)
	input_match = os.path.join(args.input_folder,args.match_file)
	# checking shimmer file (csv) #
	if not os.path.exists(input_shimmer):
		shimmer_file = args.shimmer_file
		if not os.path.exists(input_shimmer) and not os.path.exists(shimmer_file) and args.shimmer_participantcode is not None:
			participant_code = args.shimmer_participantcode
			shimmer_file = participant_code+"_shimmer.csv"
			input_shimmer = os.path.join(args.input_folder,shimmer_file)
		if not os.path.exists(input_shimmer) and not os.path.exists(shimmer_file):
			participant_code = input(f"{input_shimmer} not found, please specify shimmer participant code (ShimmerLSL input tag): ")
			shimmer_file = participant_code+"_shimmer.csv"
			input_shimmer = os.path.join(args.input_folder,shimmer_file)
		if os.path.exists(shimmer_file): # read from current folder
			print(f"{input_shimmer} not found, reading {shimmer_file} from current folder")
			print(f"copying {shimmer_file} to {args.input_folder}")
			input_shimmer = os.path.join(args.input_folder,shimmer_file)
			shutil.copyfile(shimmer_file, input_shimmer)
		if not os.path.exists(input_shimmer):
			print(f"{input_shimmer} not found, exiting...")
	# checking League of Legends timeline file (json) #
	if not os.path.exists(input_timeline):
		timeline_file = args.timeline_file
		match_id = args.match_id
		if not os.path.exists(input_timeline) and not os.path.exists(timeline_file): # Prompt match id
			timeline_file = args.region.upper()+"_"+str(match_id)+"_timeline.json"
			input_timeline = os.path.join(args.input_folder,timeline_file)
			if not os.path.exists(input_timeline) and not os.path.exists(timeline_file) and args.match_id is 'latest': # Prompt match id
				match_id = input(f"{input_timeline} not found, please specify match id (LoL match history): ")
				timeline_file = args.region.upper()+"_"+str(match_id)+"_timeline.json"
				input_timeline = os.path.join(args.input_folder,timeline_file)
		if not os.path.exists(input_timeline) and not os.path.exists(timeline_file): # Running LOLWATCHER
			command = f"python lolwatcher.py --summoner_name {args.summoner_name} --api_key {args.api_key} --region {args.region} --match_id {match_id}"
			print(f"{input_timeline} not found, running subprocess")
			p = subprocess.Popen(['python', 'lolwatcher.py', '--summoner_name',args.summoner_name, '--api_key', args.api_key, '--region', args.region, '--match_id', match_id], shell = True)
			(output, err) = p.communicate()  
			p_status = p.wait()
			if not os.path.exists(input_timeline) and not os.path.exists(timeline_file):
				print(f"{input_timeline} not found, running {command} and waiting 10 sec")
				os.system(command)
				time.sleep(10)
		if os.path.exists(timeline_file): # read from current folder
			print(f"{input_timeline} not found, reading {timeline_file} from current folder")
			print(f"copying {timeline_file} to {args.input_folder}")
			input_timeline = os.path.join(args.input_folder,timeline_file)
			shutil.copyfile(timeline_file, input_timeline)
		if not os.path.exists(input_timeline):
			print(f"{input_timeline} not found, exiting...")
			exit()
	# Checking League of Legends match file (json)
	if not os.path.exists(input_match):
		match_file = args.match_file
		match_id = args.match_id
		if not os.path.exists(input_match) and not os.path.exists(match_file): # Prompt match id
			match_file = args.region.upper()+"_"+str(match_id)+"_match.json"
			input_match = os.path.join(args.input_folder,match_file)
			if not os.path.exists(input_match) and not os.path.exists(match_file) and args.match_id is 'latest': # Prompt match id
				match_id = input(f"{input_match} not found, please specify match id (LoL match history): ")
				match_file = args.region.upper()+"_"+str(match_id)+"_match.json"
				input_match = os.path.join(args.input_folder,match_file)
		if not os.path.exists(input_match) and not os.path.exists(match_file): # Running LOLWATCHER
			command = f"python lolwatcher.py --summoner_name {args.summoner_name} --api_key {args.api_key} --region {args.region} --match_id {match_id}"
			print(f"{input_match} not found, running subprocess")
			p = subprocess.Popen(['python', 'lolwatcher.py', '--summoner_name',args.summoner_name, '--api_key', args.api_key, '--region', args.region, '--match_id', match_id], shell = True)
			(output, err) = p.communicate()  
			p_status = p.wait()
			if not os.path.exists(input_match) and not os.path.exists(match_file):
				print(f"{input_match} not found, running {command} and waiting 10 sec")
				os.system(command)
				time.sleep(10)
		if os.path.exists(match_file): # read from current folder
			print(f"{input_match} not found, reading {match_file} from current folder")
			print(f"copying {match_file} to {args.input_folder}")
			input_match = os.path.join(args.input_folder,match_file)
			shutil.copyfile(timeline_file, input_match)
		if not os.path.exists(input_match):
			print(f"{input_match} not found, exiting...")
			exit()
	# ---------------------------------------------------------------
	# Building Shimmer list
	if os.path.exists(input_shimmer):
		print("Reading..."+input_shimmer)
		shimmer_data,shimmer_fields=read_csv(input_shimmer,head_index=args.shimmer_head_row)

		# reading fields properly (column names)
		if args.shimmer_head_row is None: # ShimmerLSL (bluetooth)
			shimmer_data['timestamp'] = shimmer_data.pop(0)
			shimmer_data['GSR_ohm'] = shimmer_data.pop(1)
			shimmer_data['PPG_mv'] = shimmer_data.pop(2)
			shimmer_data['GSR_raw'] = shimmer_data.pop(3)
			shimmer_data['PPG_raw'] = shimmer_data.pop(4)
		else: # Shimmer software-exported file (USB)
			# Replace Shimmer any timestamp key to timestamp (to merge)
			for key in list(shimmer_data.keys()):
				if "timestamp" in key.lower():
					shimmer_data["timestamp"] = shimmer_data.pop(key)

		# convert to pandas dataframe
		df_shimmer = pd.DataFrame.from_dict(shimmer_data)
		
		#erase first line
		if args.shimmer_head_row is not None:
			df_shimmer = df_shimmer.iloc[args.shimmer_head_row: , :]

		# transform timestamps to ms and get date
		'''
		df_shimmer['timestamp'] = df_shimmer['timestamp'].astype('float').astype('int64')
		##df_shimmer['timestamp'] = pd.Series(df_shimmer['timestamp']).str.replace(',', '').astype('int64') 
		df_shimmer = df_shimmer.astype({'timestamp':'int64'})
		#df_shimmer['unixtime'] = [datetime.fromtimestamp(x) for x in df_shimmer['timestamp']]
		'''
		df_shimmer['date'] = pd.to_datetime(df_shimmer['timestamp'], unit='s')
		df_shimmer['timestamp'] = df_shimmer['date'].values.astype('int64') // 10 ** 6

		# reorder columns, set timestamp and date at the beginning
		cols = list(df_shimmer.columns)
		if cols[-1] == 'date':
			cols = [cols[-1]] + cols[:-1]
		if cols[1] == 'timestamp':
			cols = [cols[1]] + [cols[0]] + cols[2:]
		df_shimmer = df_shimmer[cols]

	# ---------------------------------------------------------------
	# Retrieving lol data (character idx and team idx)
	print("Reading..."+input_match)
	match_data=read_json(input_match)
	for idx,participant in enumerate(match_data['info']['participants']):
		if participant['summonerName'] == args.summoner_name:
			player_idx = idx
			team_idx = participant['teamId']
			player_indposition = participant['individualPosition']
			player_lane = participant['lane']
			player_role = participant['role']
			player_teaposition = participant['teamPosition']
			player_winner = participant['win']
			break
	# ---------------------------------------------------------------
	# Building lol timeline list
	print("Reading..."+input_timeline)
	timeline_data=read_json(input_timeline)
	init_timestamp = timeline_data['info']['frames'][0]['events'][0]['realTimestamp']
	end_timestamp = timeline_data['info']['frames'][-1]['events'][-1]['realTimestamp']
	match_duration = timeline_data['info']['frames'][-1]['events'][-1]['timestamp']
	player_ids = timeline_data['metadata']['participants'][0:len(timeline_data['metadata']['participants'])]
	match_id = timeline_data['metadata']['matchId']
	frame_interval = timeline_data['info']['frameInterval']

	timeline_df_dict = {}
	timeline_df_dict["timestamp"] = []
	timeline_df_dict["event_type"] = []
	timeline_df_dict["event_origin"] = []
	timeline_df_dict["event_target"] = []
	timeline_df_dict["event_other_info"] = []
	filtered_events = ["CHAMPION_KILL", "CHAMPION_SPECIAL_KILL", "ITEM_PURCHASED", "LEVEL_UP", "SKILL_LEVEL_UP", "WARD_PLACED","BUILDING_KILL","CHAMPION_TRANSFORM","DRAGON_SOUL_GIVEN","ELITE_MONSTER_KILL","TURRET_PLATE_DESTROYED","PAUSE_END","GAME_END"]
	''' # all events
	"ASCENDED_EVENT",
	"BUILDING_KILL",
	"CAPTURE_POINT",
	"CHAMPION_KILL",
	"CHAMPION_SPECIAL_KILL",
	"CHAMPION_TRANSFORM",
	"DRAGON_SOUL_GIVEN",
	"ELITE_MONSTER_KILL",
	"GAME_END",
	"PAUSE_END",
	"PAUSE_START",
	"ITEM_DESTROYED",
	"ITEM_PURCHASED",
	"ITEM_SOLD",
	"ITEM_UNDO",
	"LEVEL_UP",
	"SKILL_LEVEL_UP",
	"TURRET_PLATE_DESTROYED",
	"WARD_KILL",
	"WARD_PLACED"
	'''
	for frame in range(len(timeline_data['info']['frames'])):
		frame_events = timeline_data['info']['frames'][frame]['events']
		event_type = ""
		event_timestamp = -1
		event_origin = ""
		event_target = ""
		event_other_info = ""
		for event in range(len(timeline_data['info']['frames'][frame]['events'])):
			event_type = frame_events[event]['type']
			event_timestamp = init_timestamp + frame_events[event]['timestamp']
			event_origin = ""
			event_target = ""
			event_other_info = ""
			if True: # event_type in filtered_events # set to True for no filtering
				### Champion / Building / Monster Kill Events
				if event_type == "CHAMPION_KILL" or event_type == "CHAMPION_SPECIAL_KILL": # CHAMPION_SPECIAL_KILL contains killType (KILL_MULTI, ACE) and/or multiKillLength
					event_origin = frame_events[event]['killerId']
					if "victimId" in frame_events[event]:
						event_target = frame_events[event]['victimId']
					if "assistingParticipantIds" in frame_events[event]:
						event_origin = [frame_events[event]['killerId'], frame_events[event]['assistingParticipantIds']]
					if "killType" in frame_events[event]:
						event_other_info = frame_events[event]['killType']
					if "multiKillLength" in frame_events[event]:
						event_other_info = [frame_events[event]['killType'],frame_events[event]['multiKillLength']]
				elif event_type == "BUILDING_KILL" or event_type == 'TURRET_PLATE_DESTROYED':
					event_origin = frame_events[event]['teamId']
					event_other_info = frame_events[event]['laneType']
				elif event_type == "ELITE_MONSTER_KILL":
					event_origin = frame_events[event]['killerId']
					event_target = frame_events[event]['monsterType']
				elif event_type == "DRAGON_SOUL_GIVEN":
					event_other_info = frame_events[event]['name']
					event_target = frame_events[event]['teamId']
				# Levelup / Transformation / Transformation events
				elif event_type == "CHAMPION_TRANSFORM":
					event_origin = frame_events[event]['participantId']
					event_other_info = frame_events[event]['transformType']
				elif event_type == "LEVEL_UP" or event_type == "ITEM_PURCHASED" or event_type == "SKILL_LEVEL_UP":
					event_origin = frame_events[event]['participantId']
				elif event_type == "WARD_PLACED":
					event_origin = frame_events[event]['creatorId']
				# Game start / end
				elif event_type == "PAUSE_END": # start
					event_other_info = frame_events[event]['timestamp']
					event_type = 'GAME_START' # rename start event
				elif event_type == "GAME_END": # end
					event_other_info = frame_events[event]['winningTeam']
				# append to one dict
				timeline_df_dict["timestamp"].append(event_timestamp)
				timeline_df_dict["event_type"].append(event_type)
				timeline_df_dict["event_origin"].append(event_origin)
				timeline_df_dict["event_target"].append(event_target)
				timeline_df_dict["event_other_info"].append(event_other_info)

	df_lol = pd.DataFrame.from_dict(timeline_df_dict)

	# transform timestamps to ms and get date
	'''
	df_lol['timestamp'] = df_lol['timestamp'].astype('float').astype('int64')
	#df_lol['timestamp'] = pd.Series(df_lol['timestamp']).str.replace(',', '').astype('int64') 
	df_lol = df_lol.astype({'timestamp':'int64'})
	df_lol['date'] = pd.to_datetime(df_lol['timestamp'], unit='ms')
	#df_lol['unixtime'] = [datetime.fromtimestamp(x) for x in df_lol['timestamp']]
	'''
	df_lol['date'] = pd.to_datetime(df_lol['timestamp'], unit='ms')
	df_lol['timestamp'] = df_lol['date'].values.astype('int64') // 10 ** 6

	# reorder cols
	cols = list(df_lol.columns)
	if cols[-1] == 'date':
		cols = [cols[-1]] + cols[:-1]
	if cols[1] == 'timestamp':
		cols = [cols[1]] + [cols[0]] + cols[2:]
	df_lol = df_lol[cols]

	# write csv
	df_lol.to_csv(os.path.join(args.input_folder,"events_"+match_id+".csv"))
	print("created ..."+os.path.join(args.input_folder,"events_"+match_id+".csv"))
	#----------------------------------------------------------------
	print("Getting pynput buttons")
	input_pynput = os.path.join(args.input_folder,args.pynput_file)
	if os.path.exists(input_pynput):
		pynput_data = read_json(input_pynput)
		df_pynput = pd.DataFrame.from_dict(pynput_data)
		df_pynput.rename(columns={'_time': "timestamp"}, inplace=True)

		df_pynput['date'] = pd.to_datetime(df_pynput['timestamp'], unit='s')
		df_pynput['timestamp'] = df_pynput['date'].values.astype('int64') // 10 ** 6
		
		# reorder cols
		cols = list(df_pynput.columns)
		if cols[-1] == 'date':
			cols = [cols[-1]] + cols[:-1]
		if cols[3] == 'timestamp':
			cols = [cols[3]] + cols[0:2] + cols[4:]
		df_pynput = df_pynput[cols]

		# write csv
		df_pynput.to_csv(os.path.join(args.input_folder,"pynput_"+args.summoner_name+"_"+match_id+".csv"))
		print("created ..."+os.path.join(args.input_folder,"pynput_"+args.summoner_name+"_"+match_id+".csv"))

	# ---------------------------------------------------------------
	print("Syncronizing dataframes upon timestamp")
	''' # set both indexes to timestamp before join
	df_lol = df_lol.set_index('timestamp')
	df_shimmer = df_shimmer.set_index('timestamp')
	'''
	''' # reduce ms precision to -2 digits and set unique timestamps
	df_lol['timestamp'] = df_lol['timestamp'].astype(str).str[:-2].astype('int64')
	df_shimmer['timestamp'] = df_shimmer['timestamp'].astype(str).str[:-2].astype('int64')
	df_lol = df_lol.drop_duplicates(subset=['timestamp'])
	df_shimmer = df_shimmer.drop_duplicates(subset=['timestamp'])
	'''
	# Merge dataframes (shimmer and df upon timestamp)
	if not os.path.exists(input_shimmer) and not os.path.exists(input_pynput):
		print("No data for shimmer nor pynput")
		exit()
	elif os.path.exists(input_shimmer) and not os.path.exists(input_pynput):
		df_merge = pd.merge(df_shimmer, df_lol, how='outer')
	elif os.path.exists(input_pynput) and not os.path.exists(input_shimmer):
		df_merge = pd.merge(df_pynput, df_lol, how='outer')
	elif os.path.exists(input_pynput) and os.path.exists(input_shimmer):
		df_merge = pd.merge(df_shimmer, df_lol, how='outer')
		df_merge = pd.merge(df_merge, df_pynput, how='outer')

	# sort values
	df_merge = df_merge.sort_values('timestamp')
	
	#filter from game start to game end
	timestamp_start = df_merge['timestamp'][df_merge['event_type'] == 'GAME_START'].tolist()[0]
	timestamp_end = df_merge['timestamp'][df_merge['event_type'] == 'GAME_END'].tolist()[0]
	df_merge = df_merge[(df_merge['timestamp']>=timestamp_start) & (df_merge['timestamp']<=timestamp_end)]

	# clean indexes setting it to timestamp
	df_merge = df_merge.set_index('timestamp')
	
	# Save files
	df_merge.to_csv(os.path.join(args.input_folder,"merge_"+match_id+"_"+args.summoner_name+".csv"))
	print("created ..."+os.path.join(args.input_folder,"merge_"+match_id+"_"+args.summoner_name+".csv"))
	
	# plot dfs
	if os.path.exists(input_shimmer):
		plot_df(df_merge, match_id, player_idx, team_idx, ['GSR_ohm','PPG_mv','GSR_raw','PPG_raw'])

	
	''' # use pd.concat for joining more than 2 dataframes at once
	df_concat = pd.concat([df_shimmer, df_lol])
	df_concat = df_concat.sort_values('timestamp')
	df_concat.to_csv(os.path.join(args.input_folder,"concat_"+match_id+"_"+os.path.basename(input_shimmer)))
	print("created ..."+os.path.join(args.input_folder,"concat_"+match_id+"_"+os.path.basename(input_shimmer)))
	'''

