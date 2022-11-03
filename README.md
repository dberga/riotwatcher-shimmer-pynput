# riotwatcher-shimmer-pynput

This is a repository for capturing live user data, either from EDA and HR (shimmer) or keyboard/mouse (pynput). All data can be synchronized by extracting riot League of Legends game events (lolwatcher.py) and later syncing this data with the shimmer/pynput one (sync_lol_shimmer.py).

## Installation

1. Install python >3.6 ([Python 3.10.6 for Windows 64 bit](https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe) and [Debian Linux](https://cloudcone.com/docs/article/how-to-install-python-3-10-on-debian-11/) ). Note for Windows case that you need to add the option "Add Python to PATH" in order to set the environment variable working for the console (cmd) terminal.

2. Install dependencies with:
```
pip3 install -r requirements.txt
```

## Usage (capturing EDA & HR data with Shimmer)

1.  Connect to your bluetooth shimmer device (usually Shimmer-XXXX). Note: Try to remove all shimmer-related bluetooth connections beforehand and reconnect the bluetooth device to avoid any process getting stuck.
2.  Run ```python3 Shimmer_with_view.py``` and set the summoner name (this must be the same as riot's summoner name to ease sync readout). 
3.  Shimmer data will be saved in ``assets/SUMMONERNAME_shimmer.csv`` after closing the view window (or with Ctrl+C). 
The shimmer fields are **timestamp, GSR_ohm, PPG_mv, GSR_raw, PPG_raw** 


## Usage (capturing pynput keyboard and mouse usage)
1. Go to ``pynput/`` folder and run ```python3 record.py``` and set the summoner name (this must be the same as riot's summoner name to ease sync readout).
2. Pynput data will be saved in ``pynput/data/SUMMONERNAME_pynput.txt`` after closing the process by holding Right Click more than 3 sec and then Pressing Esc. 
The pynput fields are **action,button,x,y,vertical_direction,horizontal_direction**. Note that Button.left and Button.right are the mouse clicks.

## Usage (obtaining League of Legends game events and syncing them with shimmer/pynput data)

1. Regenerate your riot api key [here](https://developer.riotgames.com/) after logging in
2. Obtain riotwatcher match data and events from a specific **SUMMONERNAME** and **MATCHID** by running (make sure to regenerate your **APIKEY**):
```
python3 lolwatcher.py --summoner_name "SUMMONERNAME" --api_key "APIKEY" --match_id MATCHID
```
This will export in ``assets/`` your ``REGION_MATCHID_match.json`` and ``REGION_MATCHID_timeline.json`` files.

3. Sync your pynput/shimmer data from:
```
python3 sync_lol_shimmer.py --shimmer_file "SUMMONERNAME_shimmer.csv" --shimmer_participantcode "SUMMONERNAME" --summoner_name "SUMMONERNAME" --api_key "APIKEY" --match_id MATCHID --pynput_file "SUMMONERNAME_pynput.txt"
```
This will export an events file in ``events_REGION_MATCHID.csv`` and stats file in ``DATE_REGION_MATCHID.csv`` inside ``assets``. The riot events fields are parsed as: **event_type, event_origin, event_target, event_other_info**.

The event origin is the summoner that does the event, and the event target is usually the victim or target. 
Event types are:
```
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
```
Note: Make sure to have your ``X_shimmer.csv`` and/or ``X_pynput.txt`` files ready inside ``assets``
**The final synced file will be uploaded with the name ``merge_REGION_MATCHID_SUMMONERNAME.csv`` and plots in ``plots/``**
