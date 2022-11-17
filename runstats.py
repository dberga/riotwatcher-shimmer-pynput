import os
import pandas as pd
from parsers import read_csv, read_json
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
        {"name": "EnojaDitto","id": 3,"role": "JUNGLE","champion": "Unknown champ","summonerLevel":402,"teamId": 100,"win": True,"gameid": 6096523671,"shimmer":True,"riot":False,"pynput":False},  
        {"name": "ivegotflow","id": 4,"role": "MIDDLE","champion": "Unknown champ","summonerLevel": 115,"teamId": 100,"win": True,"gameid": 6096523671,"shimmer":True,"riot":False,"pynput":False}, 
        {"name": "Loxart","id": 1,"role": "BOTTOM","champion": "Unknown champ","summonerLevel": 82,"teamId": 100,"win": True,"gameid":6096523671,"shimmer":True,"riot":False,"pynput":False}, 
        {"name": "Rogihrim6","id": 2,"role": "TOP","champion": "Unknown champ","summonerLevel": 365,"teamId": 100,"win": True,"gameid":6096523671,"shimmer":True,"riot":False,"pynput":False}, 
        {"name": "Taketagamer","id": 0,"role": "UTILITY","champion": "Unknown champ","summonerLevel": 13, "teamId": 100,"win": True,"gameid":6096523671,"shimmer":True,"riot":False,"pynput":False}, 
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
        {"name": "PELO AVIONETA","id": 6,"role": "JUNGLE","champion": "Poppy","summonerLevel": 298,"teamId": 200,"win": True,"gameid": 6127260054,"shimmer":True,"riot":True,"pynput":True}, 
        {"name": "Darayitomck","id": 7,"role": "MIDDLE","champion": "Veigar","summonerLevel": 153,"teamId": 200,"win": True,"gameid": 6127260054,"shimmer":True,"riot":True,"pynput":True},
        {"name": "Frank DeWitt","id": 8,"role": "BOTTOM","champion": "Caitlyn","summonerLevel": 354,"teamId": 200,"win": True,"gameid": 6127260054,"shimmer":True,"riot":True,"pynput":True},
        {"name": "ivegotflow","id": 9,"role": "UTILITY","champion": "Morgana","summonerLevel": 116, "teamId": 200,"win": True,"gameid": 6127260054,"shimmer":True,"riot":True,"pynput":True},
    ]
    #### SESSION 4 - DATA FILES
    sync_files_session4 = [ # only pynput + lol
        root_dir+session_dirs[3]+"sincronizado/"+"merge_EUW1_6127261406_Rogihrim6.csv"
    ]
    playerinfo_session4 = [ # manually parsed from eventos/2022...
        {"name": "Rogihrim6","id": 6,"role": "TOP","champion": "Anivia","summonerLevel": 365,"teamId": 200,"win": False,"gameid": 6127261406,"shimmer":False,"riot":True,"pynput":True},
    ]
    #### READ ALL DATA
    all_players_data = []
    all_players_df = []
    all_players_info = []
    for i,file in enumerate(sync_files_session1):
        playerdata,fields = read_csv(file,head_index=0)
        playerdf = pd.DataFrame.from_dict(playerdata).fillna(method='ffill').fillna(method='bfill')
        playerinfo = playerinfo_session1[i]
        
        all_players_data.append(playerdata)
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
        
        playerdf = pd.DataFrame.from_dict(playerdata).fillna(method='ffill').fillna(method='bfill')
        
        #transform date
        playerdf['date'] = pd.to_datetime(playerdf['timestamp'], unit='s')
        playerdf['timestamp'] = playerdf['date'].values.astype('int64') // 10 ** 6
        
        all_players_data.append(playerdata)
        all_players_df.append(playerdf)
        all_players_info.append(playerinfo)
        
    for i,file in enumerate(sync_files_session3):
        playerdata,fields = read_csv(file,head_index=0)
        playerdf = pd.DataFrame.from_dict(playerdata).fillna(method='ffill').fillna(method='bfill')
        playerinfo = playerinfo_session3[i]
        
        all_players_data.append(playerdata)
        all_players_df.append(playerdf)
        all_players_info.append(playerinfo)
        
    for i,file in enumerate(sync_files_session4):
        playerdata,fields = read_csv(file,head_index=0)
        playerdf = pd.DataFrame.from_dict(playerdata).fillna(method='ffill').fillna(method='bfill')
        playerinfo = playerinfo_session4[i]
        
        all_players_data.append(playerdata)
        all_players_df.append(playerdf)
        all_players_info.append(playerinfo)
    
    # all data is stored in all_players_data (list of dicts), all_players_df (list of  dataframes) and all_players_info (list of dicts)
    ##### STATS
    
    # one-way anova (differences)
    print("-----GSR_ohm comparison between players in all sessions. ANOVA:")
    fvalue, pvalue = stats.f_oneway(all_players_df[0]['GSR_ohm'], all_players_df[1]['GSR_ohm'], all_players_df[2]['GSR_ohm'], all_players_df[3]['GSR_ohm'], all_players_df[4]['GSR_ohm'],all_players_df[5]['GSR_ohm'], all_players_df[6]['GSR_ohm'], all_players_df[7]['GSR_ohm'], all_players_df[8]['GSR_ohm'], all_players_df[9]['GSR_ohm'],all_players_df[10]['GSR_ohm'], all_players_df[12]['GSR_ohm'], all_players_df[13]['GSR_ohm'], all_players_df[14]['GSR_ohm'])
    print(f"GSR_ohm difference between participants: F={fvalue}, p={pvalue}")
    
    print("-----PPG_mv comparison between players in all sessions. ANOVA:")
    fvalue, pvalue = stats.f_oneway(all_players_df[0]['PPG_mv'], all_players_df[1]['PPG_mv'], all_players_df[2]['PPG_mv'], all_players_df[3]['PPG_mv'], all_players_df[4]['PPG_mv'],all_players_df[5]['PPG_mv'], all_players_df[6]['PPG_mv'], all_players_df[7]['PPG_mv'], all_players_df[8]['PPG_mv'], all_players_df[9]['PPG_mv'],all_players_df[10]['PPG_mv'], all_players_df[12]['PPG_mv'], all_players_df[13]['PPG_mv'], all_players_df[14]['PPG_mv'])
    print(f"PPG_mv difference between participants: F={fvalue}, p={pvalue}")
    
    print("-----GSR_ohm comparison between players in same session. ANOVA:")
    fvalue, pvalue = stats.f_oneway(all_players_df[0]['GSR_ohm'], all_players_df[1]['GSR_ohm'], all_players_df[2]['GSR_ohm'], all_players_df[3]['GSR_ohm'], all_players_df[4]['GSR_ohm'])
    print(f"*1st session* GSR_ohm difference between participants: F={fvalue}, p={pvalue}")
    fvalue, pvalue = stats.f_oneway(all_players_df[5]['GSR_ohm'], all_players_df[6]['GSR_ohm'], all_players_df[7]['GSR_ohm'], all_players_df[8]['GSR_ohm'], all_players_df[9]['GSR_ohm'])
    print(f"*2nd session* GSR_ohm difference between participants: F={fvalue}, p={pvalue}")
    fvalue, pvalue = stats.f_oneway(all_players_df[10]['GSR_ohm'], all_players_df[12]['GSR_ohm'], all_players_df[13]['GSR_ohm'], all_players_df[14]['GSR_ohm']) # all_players_df[11] sensor was not working
    print(f"*3rd session* GSR_ohm difference between participants: F={fvalue}, p={pvalue}")
    print("*4th session* No GSR_ohm data") # all_players_df[15]  sensor was not working
    
    print("-----PPG_mv comparison between players in same session. ANOVA:")
    fvalue, pvalue = stats.f_oneway(all_players_df[0]['PPG_mv'], all_players_df[1]['PPG_mv'], all_players_df[2]['PPG_mv'], all_players_df[3]['PPG_mv'], all_players_df[4]['PPG_mv'])
    print(f"*1st session* PPG_mv difference between participants: F={fvalue}, p={pvalue}")
    fvalue, pvalue = stats.f_oneway(all_players_df[5]['PPG_mv'], all_players_df[6]['PPG_mv'], all_players_df[7]['PPG_mv'], all_players_df[8]['PPG_mv'], all_players_df[9]['PPG_mv'])
    print(f"*2nd session* PPG_mv difference between participants: F={fvalue}, p={pvalue}")
    fvalue, pvalue = stats.f_oneway(all_players_df[10]['PPG_mv'], all_players_df[12]['PPG_mv'], all_players_df[13]['PPG_mv'], all_players_df[14]['PPG_mv']) # all_players_df[11] sensor was not working
    print(f"*3rd session* PPG_mv difference between participants: F={fvalue}, p={pvalue}")
    print("*4th session* No PPG_mv data") # all_players_df[15] sensor was not working
    
    # correlations / anticorrelations
    print("-----GSR_ohm and PPG_mv correlation for all players (all players data concatenated in 1 column)")
    all_gsr_ohm = pd.concat([all_players_df[0]['GSR_ohm'], all_players_df[1]['PPG_mv'], all_players_df[2]['GSR_ohm'], all_players_df[3]['GSR_ohm'], all_players_df[4]['GSR_ohm'],all_players_df[5]['GSR_ohm'], all_players_df[6]['GSR_ohm'], all_players_df[7]['GSR_ohm'], all_players_df[8]['GSR_ohm'], all_players_df[9]['GSR_ohm'],all_players_df[10]['GSR_ohm'], all_players_df[12]['GSR_ohm'], all_players_df[13]['GSR_ohm'], all_players_df[14]['GSR_ohm']], axis=0)
    all_ppg_mv = pd.concat([all_players_df[0]['PPG_mv'], all_players_df[1]['PPG_mv'], all_players_df[2]['PPG_mv'], all_players_df[3]['PPG_mv'], all_players_df[4]['PPG_mv'],all_players_df[5]['PPG_mv'], all_players_df[6]['PPG_mv'], all_players_df[7]['PPG_mv'], all_players_df[8]['PPG_mv'], all_players_df[9]['PPG_mv'],all_players_df[10]['PPG_mv'], all_players_df[12]['PPG_mv'], all_players_df[13]['PPG_mv'], all_players_df[14]['PPG_mv']], axis=0)
    rho,pvalue = stats.pearsonr(all_ppg_mv,all_gsr_ohm)
    print(f"correlation between GSR_ohm and PPG_mv for all players: rho={rho}, p={pvalue}")
    
    print("-----GSR_ohm and PPG_mv correlation for each individual player. PEARSON:")
    rho,pvalue = stats.pearsonr(all_players_df[0]['PPG_mv'],all_players_df[0]['GSR_ohm'])
    print(f"*1st session* {all_players_info[0]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    rho,pvalue = stats.pearsonr(all_players_df[1]['PPG_mv'],all_players_df[1]['GSR_ohm'])
    print(f"*1st session* {all_players_info[1]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    rho,pvalue = stats.pearsonr(all_players_df[2]['PPG_mv'],all_players_df[2]['GSR_ohm'])
    print(f"*1st session* {all_players_info[2]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    rho,pvalue = stats.pearsonr(all_players_df[3]['PPG_mv'],all_players_df[3]['GSR_ohm'])
    print(f"*1st session* {all_players_info[3]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    rho,pvalue = stats.pearsonr(all_players_df[4]['PPG_mv'],all_players_df[4]['GSR_ohm'])
    print(f"*1st session* {all_players_info[4]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    
    rho,pvalue = stats.pearsonr(all_players_df[5]['PPG_mv'],all_players_df[5]['GSR_ohm'])
    print(f"*2nd session* {all_players_info[5]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    rho,pvalue = stats.pearsonr(all_players_df[6]['PPG_mv'],all_players_df[6]['GSR_ohm'])
    print(f"*2nd session* {all_players_info[6]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    rho,pvalue = stats.pearsonr(all_players_df[7]['PPG_mv'],all_players_df[7]['GSR_ohm'])
    print(f"*2nd session* {all_players_info[7]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    rho,pvalue = stats.pearsonr(all_players_df[8]['PPG_mv'],all_players_df[8]['GSR_ohm'])
    print(f"*2nd session* {all_players_info[8]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    rho,pvalue = stats.pearsonr(all_players_df[9]['PPG_mv'],all_players_df[9]['GSR_ohm'])
    print(f"*2nd session* {all_players_info[9]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    
    rho,pvalue = stats.pearsonr(all_players_df[10]['PPG_mv'],all_players_df[10]['GSR_ohm'])
    print(f"*3rd session* {all_players_info[10]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    rho,pvalue = stats.pearsonr(all_players_df[12]['PPG_mv'],all_players_df[12]['GSR_ohm'])
    print(f"*3rd session* {all_players_info[12]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    rho,pvalue = stats.pearsonr(all_players_df[13]['PPG_mv'],all_players_df[13]['GSR_ohm'])
    print(f"*3rd session* {all_players_info[13]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    rho,pvalue = stats.pearsonr(all_players_df[14]['PPG_mv'],all_players_df[14]['GSR_ohm'])
    print(f"*3rd session* {all_players_info[14]['champion']} correlation between GSR_ohm and PPG_mv: rho={rho}, p={pvalue}")
    
    print(f"*4th session* {all_players_info[15]['champion']} has no GSR_ohm nor PPG_mv data")
    
    # to do: split GSR_ohm measurement in 2 or 3 parts (30 or 20 min) and make differences between
    # to do: split GSR_ohm measurement in 2 or 3 parts and make differences between
    # to do: filter GSR_ohm and PPG_mv event time (30 sec before and 30 after an event in which all_players_info[X]['id'] appears as event_origin or event_target) for each specific player
    # to do: set click (Button.left or Button.right) as '0' and Q,W,A,S,D,1,2,3,4,5,6,7,8,9,0 as '1' in key dataframes
        # then calculate absolute differences and correlations between keys and clicks
        # then calculate absolute differences and correlations between keys and GSR_ohm
        # then calculate absolute differences and correlations between keys and PPG_mv
        # then calculate absolute differences and correlations between clicks and GSR_ohm
        # then calculate absolute differences and correlations between clicks and PPG_mv
    #to do: filter keys and clicks event time (30 sec before and 30 after an event in which all_players_info[X]['id'] appears as event_origin or event_target) for each specific player
    #to do: filter data from roles in all_players_info[X]['role'] and then make statistics
    