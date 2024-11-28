from utils import scrape_utils as cls
import random
import time
import csv
from datetime import datetime
from utils.shell_colors import shell_colors as colors
import os

sleep_timer = (1,2)
site = "https://csstats.gg"
all_matches_url = "https://csstats.gg/match"
player_matches_filter = "?platforms=Valve&modes=Competitive~Premier#/matches"

seen_ids = set()

def write_old_data_to_new_file(old, new):
    with open(old, 'r') as oldfile:
        with open(new, 'w') as newfile:
            reader = csv.reader(oldfile)
            writer = csv.writer(newfile)
            
            for row in reader:
                writer.writerow(row)
    oldfile.close()
    newfile.close()

def get_newest_file_name():
    dir_list = os.listdir()
    filtered_list = [k for k in dir_list if 'cs_scrape_' in k]
    if len(filtered_list) > 0:
        filtered_list.sort(reverse=True)
        return filtered_list[0]
    return None

new_csv_file_name = "cs_scrape_" + str(datetime.now()) + ".csv"
existing_csv = get_newest_file_name()
if existing_csv is not None:
    write_old_data_to_new_file(existing_csv, new_csv_file_name)
else:
    with open(new_csv_file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ["match_id", "steamlink", "map", "server", "avg_rank", "type", "team1_string", "team2_string", "cheater_names_str"])
        writer.writeheader()
        csvfile.close()



def sleep():
    t = random.uniform(sleep_timer[0], sleep_timer[1])
    print(f"sleep for {t}")
    time.sleep(t)

def init_seen_ids(old_filename):

    with open(old_filename, 'r') as infile:
        reader = csv.reader(infile)
        
        for row in reader:
            if row[0] not in seen_ids:
                seen_ids.add(row[0])


def append2file(match_id:str, steamlink:str, map:str, server:str, avg_rank:str, type:str, playerinfo):
    seperator= "-"

    teamsize = int(len(playerinfo)/2)

    print(teamsize)

    cheater_names_str = ""
    team1_string = ""
    team2_string = ""

    for i in range(0,teamsize):
        player = playerinfo[i]
        team1_string = team1_string + player[0] + seperator

        if player[2] is True:
            cheater_names_str = cheater_names_str + player[1] + seperator

    for i in range(teamsize, len(playerinfo)):

        player = playerinfo[i]
        team2_string = team2_string + player[0] + seperator

        if player[2] is True:
            cheater_names_str = cheater_names_str + player[1] + seperator

    with open(new_csv_file_name, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile,)
        spamwriter.writerow([match_id, steamlink, map, server, avg_rank, type, team1_string, team2_string, cheater_names_str])

init_seen_ids(get_newest_file_name())
html = cls.get_html(all_matches_url)
main_page_matches = cls.get_matches_from_all_matches(html)

for match in main_page_matches:
    print(f"{colors.HEADER}MATCH : {match} ======================={colors.ENDC}")

    url = all_matches_url+"/"+match
    print(f"url: {colors.OKBLUE}{url}{colors.ENDC}")

    phtml = cls.get_html(url)
    players = cls.get_players_from_match(phtml)

    for player in players:
        sleep()
        print(f"{colors.OKCYAN}{player}{colors.ENDC}")

        url = site+"/player/"+player[0]+player_matches_filter
        print(f"url: {colors.OKBLUE}{url}{colors.ENDC}")

        player_page_html = cls.get_html(url)
        player_matches = cls.get_matches_from_player(player_page_html)

        for pmatch_id in player_matches:

            if pmatch_id in seen_ids:
                print(f"{colors.WARNING}Match ({pmatch_id}) already seen. Skipping{colors.ENDC}")
                continue

            seen_ids.add(pmatch_id)

            sleep()

            url = site + "/match/" + pmatch_id
            print(f"url: {colors.OKBLUE}{url}{colors.ENDC}")

            pmatch_html = cls.get_html(url)

            pplayers = cls.get_players_from_match(pmatch_html)
            steamlink = cls.get_steam_link(cls.get_watch_demo_url(pmatch_html))
            match_info = cls.get_match_information(pmatch_html)

            append2file(pmatch_id,steamlink[0],match_info["map"],match_info["server"],str(match_info["rank"]), match_info["type"], pplayers)
    
    print("")
    sleep()