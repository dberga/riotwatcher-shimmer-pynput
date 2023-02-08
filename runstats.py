import os
import pandas as pd
from parsers import read_csv, read_json
from parsers import df_filter_event_origin, df_filter_event_assist, df_filter_event_target
import argparse
from datetime import datetime
import scipy.stats as stats

if __name__ == "__main__": # test parsers
    root_dir = "Datos-Sesiones/"
    session_dirs = ["Viernes7-sesion1-6097099909/", "Viernes7-sesion2-6096523671/","Viernes28-sesion1-6127260054/","Viernes28-sesion2-6127261406/"]
    #### SESSION 1 - DATA FILES
    sync_files_session1 = [ # shimmer + lol
        root_dir+session_dirs[0]+"sincronizado/"+"merge_EUW1_6097099909_EnojaDitto_negro1_mod_shimmer.csv",
        root_dir+session_dirs[0]+"sincronizado/"+"merge_EUW1_6097099909_ivegotflow_naranja1_shimmer.csv",
        root_dir+session_dirs[0]+"sincronizado/"+"merge_EUW1_6097099909_LoxartAzul1_shimmer.csv",
        root_dir+session_dirs[0]+"sincronizado/"+"merge_EUW1_6097099909_Rogihrim6_verde1_shimmer.csv",
        root_dir+session_dirs[0]+"sincronizado/"+"merge_EUW1_6097099909_Taketagamer_amarillo1_mod_shimmer.csv",
    ]
    gamestats_file_session1 = root_dir+session_dirs[0]+"eventos/2022-10-07_EUW1_6097099909.csv"  # more data here
    playerinfo_session1 = [ # manually parsed from eventos/2022...
        {"name": "EnojaDitto","id": 3,"role": "JUNGLE","champion": "Shaco","summonerLevel":402,"teamId": 100,"win": False,"gameid":6097099909},
        {"name": "ivegotflow","id": 4,"role": "MIDDLE","champion": "Morgana","summonerLevel": 115,"teamId": 100,"win": False,"gameid":6097099909},
        {"name": "Loxart","id": 1,"role": "BOTTOM","champion": "Twitch","summonerLevel": 82,"teamId": 100,"win": False,"gameid":6097099909},
        {"name": "Rogihrim6","id": 2,"role": "TOP","champion": "Irelia","summonerLevel": 365,"teamId": 100,"win": False,"gameid":6097099909},
        {"name": "Taketagamer","id": 0,"role": "UTILITY","champion": "Ashe","summonerLevel": 13, "teamId": 100,"win": False,"gameid":6097099909},
    ]
    #### SESSION 2 - DATA FILES
    sync_files_session2 = [ # only shimmer data (no lol data [partida personalizado no en api])
        root_dir+session_dirs[1]+"EnojaDitto_negro2_shimmer.csv",
        root_dir+session_dirs[1]+"ivegotflow_naraja2_shimmer.csv",
        root_dir+session_dirs[1]+"Loxart_azul2_shimmer.csv",
        root_dir+session_dirs[1]+"Rogihrim6_verde2_shimmer.csv",
        root_dir+session_dirs[1]+"Taketatgamer_amarillo2_shimmer.csv",
    ]
    gamestats_file_session2 = None # no lol data for this one (custom game not in api)
    playerinfo_session2 = [ # copied from previous session
        {"name": "EnojaDitto","id": 3,"role": "JUNGLE","champion": "Unknown champ","summonerLevel":402,"teamId": 100,"win": True,"gameid": 6096523671},  
        {"name": "ivegotflow","id": 4,"role": "MIDDLE","champion": "Unknown champ","summonerLevel": 115,"teamId": 100,"win": True,"gameid": 6096523671}, 
        {"name": "Loxart","id": 1,"role": "BOTTOM","champion": "Unknown champ","summonerLevel": 82,"teamId": 100,"win": True,"gameid":6096523671}, 
        {"name": "Rogihrim6","id": 2,"role": "TOP","champion": "Unknown champ","summonerLevel": 365,"teamId": 100,"win": True,"gameid":6096523671}, 
        {"name": "Taketagamer","id": 0,"role": "UTILITY","champion": "Unknown champ","summonerLevel": 13, "teamId": 100,"win": True,"gameid":6096523671}, 
    ]
    #### SESSION 3 - DATA FILES
    sync_files_session3 = [ # shimmer + lol + pynput
        root_dir+session_dirs[2]+"sincronizado/"+"merge_EUW1_6127260054_4K Poppy.csv",
        root_dir+session_dirs[2]+"sincronizado/"+"merge_EUW1_6127260054_Darayitomck.csv",
        root_dir+session_dirs[2]+"sincronizado/"+"merge_EUW1_6127260054_Frank DeWitt.csv",
        root_dir+session_dirs[2]+"sincronizado/"+"merge_EUW1_6127260054_ivegotflow.csv",
        root_dir+session_dirs[2]+"sincronizado/"+"merge_EUW1_6127260054_PELO AVIONETA.csv",
    ]
    gamestats_file_session3 = root_dir+session_dirs[2]+"eventos/stats_2022-10-28_EUW1_6127260054.csv" # more data here
    playerinfo_session3 = [ # manually parsed from eventos/2022...
        {"name": "4K Poppy","id": 5,"role": "TOP","champion": "Kled","summonerLevel": 110,"teamId": 200,"win": True,"gameid": 6127260054},
        {"name": "Darayitomck","id": 7,"role": "MIDDLE","champion": "Veigar","summonerLevel": 153,"teamId": 200,"win": True,"gameid": 6127260054},
        {"name": "Frank DeWitt","id": 8,"role": "BOTTOM","champion": "Caitlyn","summonerLevel": 354,"teamId": 200,"win": True,"gameid": 6127260054},
        {"name": "ivegotflow","id": 9,"role": "UTILITY","champion": "Morgana","summonerLevel": 116, "teamId": 200,"win": True,"gameid": 6127260054},
        {"name": "PELO AVIONETA","id": 6,"role": "JUNGLE","champion": "Poppy","summonerLevel": 298,"teamId": 200,"win": True,"gameid": 6127260054}, 
    ]
    #### SESSION 4 - DATA FILES
    sync_files_session4 = [ # only pynput + lol
        root_dir+session_dirs[3]+"sincronizado/"+"merge_EUW1_6127261406_Rogihrim6.csv"
    ]
    playerinfo_session4 = [ # manually parsed from eventos/2022...
        {"name": "Rogihrim6","id": 6,"role": "TOP","champion": "Anivia","summonerLevel": 365,"teamId": 200,"win": False,"gameid": 6127261406},
    ]


    #### READ ALL DATA
    available_fields = ['timestamp', 'date', 'GSR_ohm', 'PPG_mv', 'GSR_raw', 'PPG_raw', 'event_type', 'event_origin', 'event_target', 'event_other_info', 'action', 'button', 'x', 'y', 'vertical_direction', 'horizontal_direction']
    available_info = ['name','id','role','champion','summonerLevel','teamId','win','gameid']
    all_players_df = []
    all_players_info = []
    for i,file in enumerate(sync_files_session1):
        playerdata,fields = read_csv(file,head_index=0)
        playerdf = pd.DataFrame.from_dict(playerdata)
        playerinfo = playerinfo_session1[i]

        # convert to float64
        playerdf['date'] = playerdf['date'].values.astype('datetime64[ns]')
        playerdf['timestamp'] = playerdf['date'].values.astype('float64') / 10 ** 6

        all_players_df.append(playerdf)
        all_players_info.append(playerinfo)
        
    for i,file in enumerate(sync_files_session2):
        playerdata,fields = read_csv(file,head_index=None)
        playerinfo = playerinfo_session2[i]
        
        # head index is None -> create that
        playerdata['timestamp'] = playerdata.pop(0)
        playerdata['GSR_ohm'] = playerdata.pop(1)
        playerdata['PPG_mv'] = playerdata.pop(2)
        playerdata['GSR_raw'] = playerdata.pop(3)
        playerdata['PPG_raw'] = playerdata.pop(4)
        
        playerdf = pd.DataFrame.from_dict(playerdata)
        
        #convert to float64
        playerdf['date'] = pd.to_datetime(playerdf['timestamp'], unit='s')
        playerdf['timestamp'] = playerdf['date'].values.astype('float64') / 10 ** 6
        # force float64 to GSR and PPG raw
        playerdf['GSR_raw'] = playerdf['GSR_raw'].values.astype("float64")
        playerdf['PPG_raw'] = playerdf['PPG_raw'].values.astype("float64")

        all_players_df.append(playerdf)
        all_players_info.append(playerinfo)
        
    for i,file in enumerate(sync_files_session3):
        playerdata,fields = read_csv(file,head_index=0)
        playerdf = pd.DataFrame.from_dict(playerdata)
        playerinfo = playerinfo_session3[i]

        # convert to float64
        playerdf['date'] = playerdf['date'].values.astype('datetime64[ns]')
        playerdf['timestamp'] = playerdf['date'].values.astype('float64') / 10 ** 6
        # force float64 to GSR and PPG raw
        #playerdf['GSR_raw'] = playerdf['GSR_raw'].values.astype("float64")
        #playerdf['PPG_raw'] = playerdf['PPG_raw'].values.astype("float64")

        all_players_df.append(playerdf)
        all_players_info.append(playerinfo)
        
    for i,file in enumerate(sync_files_session4):
        playerdata,fields = read_csv(file,head_index=0)
        playerdf = pd.DataFrame.from_dict(playerdata)
        playerinfo = playerinfo_session4[i]

        # convert to float64
        playerdf['date'] = playerdf['date'].values.astype('datetime64[ns]')
        playerdf['timestamp'] = playerdf['date'].values.astype('float64') / 10 ** 6
        # force float64 to GSR and PPG raw
        #playerdf['GSR_raw'] = playerdf['GSR_raw'].values.astype("float64")
        #playerdf['PPG_raw'] = playerdf['PPG_raw'].values.astype("float64")

        all_players_df.append(playerdf)
        all_players_info.append(playerinfo)

        # all data is stored in all_players_df (list of dataframes) and all_players_info (list of dicts)

    ##### DATA CLEANING AND CURATION
    # here make sure all players data have same fields
    for i,playerdf in enumerate(all_players_df):
        # add empty fields to players with non existing field
        for f,field in enumerate(available_fields):
            if field not in all_players_df[i]:
                all_players_df[i][field] = ''
        #sort according to available_fields
        all_players_df[i] = all_players_df[i][available_fields]

    # data cleaning and curation
    for i,playerdf in enumerate(all_players_df):
        # fill physiological data gaps with previous or next value when nan
        if 'GSR_ohm' in all_players_df[i] and 'PPG_mv' in all_players_df[i]:
            all_players_df[i]['GSR_ohm'] = all_players_df[i]['GSR_ohm'].fillna(method='ffill').fillna(method='bfill')
            all_players_df[i]['PPG_mv'] = all_players_df[i]['PPG_mv'].fillna(method='ffill').fillna(method='bfill')
            all_players_df[i]['GSR_raw'] = all_players_df[i]['GSR_raw'].fillna(method='ffill').fillna(method='bfill')
            all_players_df[i]['PPG_raw'] = all_players_df[i]['PPG_raw'].fillna(method='ffill').fillna(method='bfill')

    # add player info as columns
    for i,playerdf in enumerate(all_players_df):
        for key in available_info:
            all_players_df[i][key] = all_players_info[i][key]
            #all_players_df[i][key] = pd.Series([all_players_info[i][key] for x in range(len(all_players_df[i].index))])

    # replace event data by numbers
    available_events = [
        "CHAMPION_KILL", #1 = killing, 11 = being killed (death), 100 = assisting
        "CHAMPION_SPECIAL_KILL", #2 = special killing
        "ITEM_PURCHASED", #3
        "LEVEL_UP", #4
        "SKILL_LEVEL_UP", #5
        "WARD_PLACED", #6
        "BUILDING_KILL", #7
        "CHAMPION_TRANSFORM", #8
        "TURRET_PLATE_DESTROYED", #9
        "ELITE_MONSTER_KILL", # 10
        ]
    dict_event_window_size = {
    '1': 5000, 
    '2': 5000, #10000
    '3': 0,
    '4': 0,
    '5': 0,
    '6': 5000,
    '7': 5000, # 10000
    '8': 5000,
    '9': 5000,
    '10': 5000, # 10000
    '11': 5000, # 10000
    '100': 0,
    }
    pre_post_keys = [1000, 2000]
    list_events_5s = [key for key in list(dict_event_window_size.keys()) if dict_event_window_size[key]==5000]
    #list_events_10s = [key for key in list(dict_event_window_size.keys()) if dict_event_window_size[key]==10000]

    for i,playerdf in enumerate(all_players_df):
        all_players_df[i]['EVENTS'] = ''
        for e,event_type in enumerate(available_events):
            # set type of idx
            if event_type == "TURRET_PLATE_DESTROYED" or event_type == "BUILDING_KILL": 
                player_idx = str(all_players_info[i]['teamId'])
            else:
                player_idx = str(all_players_info[i]['id'])
            df_res_origin = df_filter_event_origin(all_players_df[i],event_type,player_idx)
            df_res_target = df_filter_event_target(all_players_df[i],event_type,player_idx)
            df_res_assist = df_filter_event_assist(all_players_df[i],event_type,player_idx)
            #print(f"{event_type}: origin:{df_res_origin.sum()},target:{df_res_target.sum()},assist:{df_res_assist.sum()}")

            all_players_df[i]['EVENTS'][df_res_origin[df_res_origin==True].index] = str(e+1)
            all_players_df[i]['EVENTS'][df_res_target[df_res_target==True].index] = str(e+1+10)
            all_players_df[i]['EVENTS'][df_res_assist[df_res_assist==True].index] = str(e+1+99)

    # create dataframes on txt for Eleonora
    out_folder = 'output/'
    os.makedirs(out_folder,exist_ok = True)

    all_players_gsr_raw = []
    all_players_ppg_raw = []
    for i,playerdf in enumerate(all_players_df):
        # calc session time and sampling rate
        session_time_sec = (playerdf['timestamp'].iloc[-1]-playerdf['timestamp'].iloc[0]) / 1000
        sampling_rate = float(playerdf.index.size) / session_time_sec

        # separate gsr and ppg as individual dataframes
        gsr_df = playerdf[['timestamp','GSR_raw', 'EVENTS']].copy()
        ppg_df = playerdf[['timestamp','PPG_raw', 'EVENTS']].copy()
        gsr_events = gsr_df[gsr_df['EVENTS'] != '']
        ppg_events = ppg_df[ppg_df['EVENTS'] != '']
        ### old (include all events)
        '''
        for index, row in gsr_events.iterrows():
            ttp = row['timestamp']
            event = row['EVENTS']
            gsr = row['GSR_raw']
            pre_post_time = dict_event_window_size[event]
            gsr_df = gsr_df.append({'timestamp': ttp-pre_post_time,'GSR_raw': gsr,'EVENTS': event+str(pre_post_keys[0])},ignore_index=True) # pre
            #gsr_df = gsr_df.append({'timestamp': ttp+pre_post_time,'GSR_raw': gsr,'EVENTS': event+str(pre_post_keys[1])},ignore_index=True) # post
            #gsr_df['EVENTS'].loc[index-1000] = gsr_df['EVENTS'][index]+str(1000) # pre
            #gsr_df['EVENTS'].loc[index+1000] = gsr_df['EVENTS'][index]+str(2000) # post
        for index, row in ppg_events.iterrows():
            ttp = row['timestamp']
            event = row['EVENTS']
            ppg = row['PPG_raw']
            pre_post_time = dict_event_window_size[event]
            ppg_df = ppg_df.append({'timestamp': ttp-pre_post_time,'PPG_raw': ppg,'EVENTS': event+str(pre_post_keys[0])},ignore_index=True) # pre
            #ppg_df = ppg_df.append({'timestamp': ttp+pre_post_time,'PPG_raw': ppg,'EVENTS': event+str(pre_post_keys[1])},ignore_index=True) # post
            #ppg_df['EVENTS'].loc[index-1000] = gsr_df['EVENTS'][index]+str(1000) # pre
            #ppg_df['EVENTS'].loc[index+1000] = gsr_df['EVENTS'][index]+str(2000) # post
        gsr_df = gsr_df.set_index('timestamp').sort_index(ascending=True)
        ppg_df = ppg_df.set_index('timestamp').sort_index(ascending=True)
        all_players_gsr_raw.append(gsr_df)
        all_players_ppg_raw.append(ppg_df)
        filename_gsr = "gsr_"+all_players_info[i]['name']+"_"+str(all_players_info[i]['gameid'])+'_'+str(all_players_info[i]['role'])+'_'+str(all_players_info[i]['summonerLevel'])+'_'+str(all_players_info[i]['win'])+".txt"
        filename_ppg = "ppg_"+all_players_info[i]['name']+"_"+str(all_players_info[i]['gameid'])+'_'+str(all_players_info[i]['role'])+'_'+str(all_players_info[i]['summonerLevel'])+'_'+str(all_players_info[i]['win'])+".txt"
        gsr_df.to_csv(out_folder+filename_gsr,sep=" ",header=False)
        ppg_df.to_csv(out_folder+filename_ppg,sep=" ",header=False)
        '''

        # filter 5s and 10s events
        gsr_events_5s = pd.DataFrame()
        ppg_events_5s = pd.DataFrame()
        #gsr_events_10s = pd.DataFrame()
        #ppg_events_10s = pd.DataFrame()
        for eventkey in list_events_5s:
            current_gsr_events_5s = gsr_df[gsr_df['EVENTS'] == eventkey]
            current_ppg_events_5s = ppg_df[ppg_df['EVENTS'] == eventkey]
            gsr_events_5s = pd.concat([gsr_events_5s,current_gsr_events_5s])
            ppg_events_5s = pd.concat([ppg_events_5s,current_ppg_events_5s])
        #for eventkey in list_events_10s:
        #    current_gsr_events_10s = gsr_df[gsr_df['EVENTS'] == eventkey]
        #    current_ppg_events_10s = ppg_df[ppg_df['EVENTS'] == eventkey]
        #    gsr_events_10s = pd.concat([gsr_events_10s,current_gsr_events_10s])
        #    ppg_events_10s = pd.concat([ppg_events_10s,current_ppg_events_10s])

        # clean dataframes events to start adding clean events
        gsr_5s = gsr_df
        gsr_5s['EVENTS'] = ''
        ppg_5s = ppg_df
        ppg_5s['EVENTS'] = ''
        #gsr_10s = gsr_df
        #gsr_10s['EVENTS'] = ''
        #ppg_10s = ppg_df
        #ppg_10s['EVENTS'] = ''

        # 5 sec events
        for index, row in gsr_events_5s.iterrows():
            gsr_5s = gsr_5s.append({'timestamp': row['timestamp'],'GSR_raw': row['GSR_raw'],'EVENTS': row['EVENTS']},ignore_index=True) # pre
            gsr_5s = gsr_5s.append({'timestamp': row['timestamp']-dict_event_window_size[row['EVENTS']],'GSR_raw': row['GSR_raw'],'EVENTS': row['EVENTS']+str(pre_post_keys[0])},ignore_index=True) # pre
        
        for index, row in ppg_events_5s.iterrows():
            ppg_5s = ppg_5s.append({'timestamp': row['timestamp'],'PPG_raw': row['PPG_raw'],'EVENTS': row['EVENTS']},ignore_index=True) # pre
            ppg_5s = ppg_5s.append({'timestamp': row['timestamp']-dict_event_window_size[row['EVENTS']],'PPG_raw': row['PPG_raw'],'EVENTS': row['EVENTS']+str(pre_post_keys[0])},ignore_index=True) # pre
        
        ## 10 sec events
        #for index, row in gsr_events_10s.iterrows():
        #    gsr_10s = gsr_10s.append({'timestamp': row['timestamp'],'GSR_raw': row['GSR_raw'],'EVENTS': row['EVENTS']},ignore_index=True) # pre
        #    gsr_10s = gsr_10s.append({'timestamp': row['timestamp']-dict_event_window_size[row['EVENTS']],'GSR_raw': row['GSR_raw'],'EVENTS': row['EVENTS']+str(pre_post_keys[0])},ignore_index=True) # pre
        #
        #for index, row in ppg_events_10s.iterrows():
        #    ppg_10s = ppg_10s.append({'timestamp': row['timestamp'],'PPG_raw': row['PPG_raw'],'EVENTS': row['EVENTS']},ignore_index=True) # pre
        #    ppg_10s = ppg_10s.append({'timestamp': row['timestamp']-dict_event_window_size[row['EVENTS']],'PPG_raw': row['PPG_raw'],'EVENTS': row['EVENTS']+str(pre_post_keys[0])},ignore_index=True) # pre
        
        # clean consecutive events (say the X1000 [pre] appears several times before the actual event X because other X events happen)
        filt_5s = gsr_5s[gsr_5s['EVENTS'] != '']['EVENTS']
        iffilt_5s = filt_5s.loc[filt_5s.shift() != filt_5s].index
        gsr_5s.iloc[iffilt_5s]['EVENTS'] = filt_5s

        filt_5s = ppg_5s[ppg_5s['EVENTS'] != '']['EVENTS']
        iffilt_5s = filt_5s.loc[filt_5s.shift() != filt_5s].index
        ppg_5s.iloc[iffilt_5s]['EVENTS'] = filt_5s
        
        #filt_10s = gsr_10s[gsr_10s['EVENTS'] != '']['EVENTS']
        #iffilt_10s = filt_10s.loc[filt_10s.shift() != filt_10s].index
        #gsr_10s.iloc[iffilt_10s]['EVENTS'] = filt_10s
        
        #filt_10s = ppg_10s[ppg_10s['EVENTS'] != '']['EVENTS']
        #iffilt_10s = filt_10s.loc[filt_10s.shift() != filt_10s].index
        #ppg_10s.iloc[iffilt_10s]['EVENTS'] = filt_10s

        # write files
        gsr_5s = gsr_5s.set_index('timestamp').sort_index(ascending=True)
        filename = f"gsr_events5sec_"+all_players_info[i]['name']+"_session"+str(all_players_info[i]['gameid'])+"_samplingrate(Hz)"+str(sampling_rate)+'_'+str(all_players_info[i]['role'])+'_'+str(all_players_info[i]['summonerLevel'])+'_'+str(all_players_info[i]['win'])+".txt"
        gsr_5s.to_csv(out_folder+filename,sep=" ",header=False)
        
        ppg_5s = ppg_5s.set_index('timestamp').sort_index(ascending=True)
        filename = f"ppg_events5sec_"+all_players_info[i]['name']+"_session"+str(all_players_info[i]['gameid'])+"_samplingrate(Hz)"+str(sampling_rate)+'_'+str(all_players_info[i]['role'])+'_'+str(all_players_info[i]['summonerLevel'])+'_'+str(all_players_info[i]['win'])+".txt"
        ppg_5s.to_csv(out_folder+filename,sep=" ",header=False)

        #gsr_10s = gsr_10s.set_index('timestamp').sort_index(ascending=True)
        #filename = f"gsr_events10sec_"+all_players_info[i]['name']+"_"+str(all_players_info[i]['gameid'])+'_'+str(all_players_info[i]['role'])+'_'+str(all_players_info[i]['summonerLevel'])+'_'+str(all_players_info[i]['win'])+".txt"
        #gsr_10s.to_csv(out_folder+filename,sep=" ",header=False)

        #ppg_10s = ppg_10s.set_index('timestamp').sort_index(ascending=True)
        #filename = f"ppg_events10sec_"+all_players_info[i]['name']+"_"+str(all_players_info[i]['gameid'])+'_'+str(all_players_info[i]['role'])+'_'+str(all_players_info[i]['summonerLevel'])+'_'+str(all_players_info[i]['win'])+".txt"
        #ppg_10s.to_csv(out_folder+filename,sep=" ",header=False)

    # remove unnecesary fields
    for i,playerdf in enumerate(all_players_df):
        del all_players_df[i]['event_type']
        del all_players_df[i]['event_origin']
        del all_players_df[i]['event_target']
        del all_players_df[i]['event_other_info']

        del all_players_df[i]['champion']
        del all_players_df[i]['id']
        del all_players_df[i]['teamId']

        del all_players_df[i]['vertical_direction']
        del all_players_df[i]['horizontal_direction']
        del all_players_df[i]['x']
        del all_players_df[i]['y']
    # concat all data to one unique file
    whole_df = pd.concat(all_players_df,axis=0).reset_index(drop=True)

    # clean name for each df
    for i,playerdf in enumerate(all_players_df):
        del all_players_df[i]['name']
        del all_players_df[i]['gameid']


    ##### WRITE CSV
    for i,playerdf in enumerate(all_players_df):
        session_time_sec = (playerdf['timestamp'].iloc[-1]-playerdf['timestamp'].iloc[0]) / 1000
        sampling_rate = float(playerdf.index.size) / session_time_sec
        playerdf['PPG_raw'] = playerdf['PPG_raw'].values.astype("str")
        filename = all_players_info[i]['name']+"_session"+str(all_players_info[i]['gameid'])+"_samplingrate(Hz)"+str(sampling_rate)+".csv"
        all_players_df[i].to_csv(out_folder+filename,sep=" ")

    whole_df.to_csv(out_folder+"whole.csv",sep=" ")
    