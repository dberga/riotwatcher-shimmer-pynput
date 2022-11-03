import pandas as pd
import json
import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def read_csv(csv_path,head_index=1,sep_token=','):
    dict_captured_data = pd.read_csv(csv_path,sep=sep_token,header=head_index).to_dict()
    list_fields = dict_captured_data.keys()
    return dict_captured_data, list_fields

def read_json(json_path):
	with open(json_path, 'r') as f:
  		data = json.load(f)  		
	return data

def df_filter_event_origin(dataframe, event_type = "CHAMPION_KILL", player_idx = 0):
	df_origins = dataframe[dataframe['event_type']==event_type]['event_origin']
	df_player_events = df_origins==player_idx
	for index, event_origin in df_origins.iteritems():
		if type(event_origin) == type(list()):
			if event_origin[0] == player_idx:
				df_player_events[index] = True
		elif type(event_origin) == type(int()):
			if event_origin == player_idx:
				df_player_events[index] = True
	return df_player_events

def df_filter_event_assist(dataframe, event_type = "CHAMPION_KILL", player_idx = 0):
	df_origins = dataframe[dataframe['event_type']==event_type]['event_origin']
	df_player_events = df_origins==-1
	for index, event_origin in df_origins.iteritems():
		if type(event_origin) == type(list()):
			if player_idx in event_origin[1]:
				df_player_events[index] = True
		elif type(event_origin) == type(int()):
			if event_origin == player_idx:
				df_player_events[index] = False
	return df_player_events

def df_filter_event_target(dataframe, event_type = "CHAMPION_KILL", player_idx = 0):
	df_targets = dataframe[dataframe['event_type']==event_type]['event_target']
	df_player_events = df_targets==player_idx
	return df_player_events

def plot_df(df_merge, match_name = "temp", player_idx = 0, team_idx = 100, fields = ['GSR_ohm','PPG_mv','GSR_raw','PPG_raw'], limits = {'GSR_ohm': [120, 480],'PPG_mv': [0, 2800], 'GSR_raw': [17900, 36100],'PPG_raw': [0, 3800]}):
	for fidx,field in enumerate(fields):
		print(f"plotting {field} for {match_name} player {player_idx}")
		df_player_kills = df_filter_event_origin(df_merge, "CHAMPION_KILL", player_idx )
		df_player_deaths = df_filter_event_target(df_merge, "CHAMPION_KILL", player_idx )
		df_player_assists = df_filter_event_assist(df_merge, "CHAMPION_KILL", player_idx )
		df_player_special_kills = df_filter_event_origin(df_merge, "CHAMPION_SPECIAL_KILL", player_idx )
		df_player_building_kills = df_filter_event_origin(df_merge, "BUILDING_KILL", team_idx )
		df_player_elitemonster_kills = df_filter_event_origin(df_merge, "ELITE_MONSTER_KILL", player_idx )
		timestamps_events = {
			"CHAMPION_KILL": {"color": 'g', "timestamps": df_player_kills[df_player_kills==True].index},
			"CHAMPION_DEATH": {"color": 'r', "timestamps": df_player_deaths[df_player_deaths==True].index},
			"CHAMPION_KILL_ASSIST": {"color": 'b', "timestamps": df_player_assists[df_player_assists==True].index},
			"CHAMPION_SPECIAL_KILL": {"color": 'c', "timestamps": df_player_special_kills[df_player_special_kills==True].index},
			"BUILDING_KILL": {"color": 'y', "timestamps": df_player_building_kills[df_player_building_kills==True].index},
			"ELITE_MONSTER_KILL": {"color": 'm', "timestamps": df_player_elitemonster_kills[df_player_elitemonster_kills==True].index},
		}
		#df_merge['time']=pd.to_datetime(df_merge['date']).dt.time.to_string()
		#df_merge['time']=df_merge['time'].str.slice(27,35)
		df_merge['time'] = pd.to_datetime(df_merge.index, unit='ms').astype(str).str.slice(11,19)
		####df_merge.loc[df_player_kills[df_player_kills==True].index,field] = field_trigger_vals[fidx]
		## PLOT	
		fig = plt.figure(figsize=(25,7.5))
		plt.plot(df_merge.index,df_merge[field], color='k')
		#plt.rcParams["figure.figsize"] = (30,5)
		#fig.subtitle("player="+str(player_idx))
		for event_type in timestamps_events.keys():
			for timestamp in timestamps_events[event_type]["timestamps"]:
				plt.axvline(x = timestamp, color = timestamps_events[event_type]["color"], label = event_type)
		plt.xticks(df_merge.index,df_merge['time'], rotation=45)
		plt.locator_params(axis='x', nbins=30)
		plt.xlabel('time (h:m:s)')
		#plt.xlabel('timestamp (ms)')
		plt.ylabel(field)
		plt.ylim([df_merge[field].min(),df_merge[field].max()])
		#if field in limits:
		#	plt.ylim(limits[field])
		custom_legend_lines = [Line2D([0], [0], color='g', lw=4),Line2D([0], [0], color='r', lw=4),Line2D([0], [0], color='b', lw=4), Line2D([0], [0], color='c', lw=4), Line2D([0], [0], color='y', lw=4),Line2D([0], [0], color='m', lw=4)]
		plt.legend(custom_legend_lines, list(timestamps_events.keys()))
		plt.savefig(f"assets/{player_idx}_{field}_{match_name}.png")
		plt.clf()
if __name__ == "__main__": # test parsers
	sample_path="assets/SkillShot_David_22022022.csv"
	shimmer_data,shimmer_fields=read_csv(sample_path)
	print(shimmer_fields)
	print(shimmer_data)

	sample_path="assets/mereurecat11_Session1_blue_Calibrated_PC_128hz.csv"
	shimmer_data,shimmer_fields=read_csv(sample_path)
	print(shimmer_fields)
	print(shimmer_data)

	sample_path="assets/match.json"
	match_data=read_json(sample_path)
	###Main Fields:
	print(match_data['metadata']['matchId']) # unique match id
	print(match_data['metadata']['participants'][0:9]) # player ids, 5 for each team (0:4),(5:9)
	print(match_data['info']['gameCreation']) # game creation time (lobby)
	print(match_data['info']['gameDuration']) # game duration (total)
	print(match_data['info']['gameStartTimestamp']) # actual game start 
	print(match_data['info']['teams'][0:1]) # both team stats (0),(1)
	print(match_data['info']['participants'][0:9]) # stats of players, 5 for each team (0:4),(5:9)

	sample_path="assets/timeline.json"
	timeline_data=read_json(sample_path)
	###Main Fields:
	print(timeline_data['metadata']['matchId']) # unique match id
	print(timeline_data['metadata']['participants'][0:9]) # player ids, 5 for each team (0:4),(5:9)
	print(timeline_data['info']['frameInterval']) # frame interval (captures are every N frameInterval)
	print(len(timeline_data['info']['frames'])) # total captured frame instances
	print(timeline_data['info']['frames'][0]['timestamp']) # frame 0 timestamp
	print(timeline_data['info']['frames'][0]['events'][0]['realTimestamp']) # initial real time timestamp
	print(timeline_data['info']['frames'][5]['events']) # all events from that phase
	print(timeline_data['info']['frames'][5]['events'][0]['type']) # event type
	# for each event type, we have different fields
	if timeline_data['info']['frames'][5]['events'][0]['type'] == "CHAMPION_KILL":
		print(timeline_data['info']['frames'][5]['events'][0]['victimId'])
		print(timeline_data['info']['frames'][5]['events'][0]['killerId'])
		print(timeline_data['info']['frames'][5]['events'][0]['assistingParticipantIds'])
	elif timeline_data['info']['frames'][5]['events'][0]['type'] == "LEVEL_UP" or timeline_data['info']['frames'][5]['events'][0]['type'] == "ITEM_PURCHASED" or timeline_data['info']['frames'][5]['events'][0]['type'] == "SKILL_LEVEL_UP":
		print(timeline_data['info']['frames'][5]['events'][0]['participantId']) # event participant
	elif timeline_data['info']['frames'][5]['events'][0]['type'] == "WARD_PLACED":
		print(timeline_data['info']['frames'][5]['events'][0]['creatorId'])

	print(sample_path)

	
