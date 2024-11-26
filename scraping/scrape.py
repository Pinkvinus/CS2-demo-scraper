import cloudscrape as cls
import random
import time
import csv
from datetime import datetime
from my_colors import mycolors

sleep_timer = (1,2)
site = "https://csstats.gg"
all_matches_url = "https://csstats.gg/match"
player_matches_filter = "?platforms=Valve&modes=Competitive~Premier#/matches"

csv_file_name = "cs_scrape_" + str(datetime.now()) + ".csv"

seen_ids = set()

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

    with open(csv_file_name, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile,)
        spamwriter.writerow([match_id, steamlink, map, server, avg_rank, type, team1_string, team2_string, cheater_names_str])

init_seen_ids("all_clean.csv")
html = cls.get_html(all_matches_url)
main_page_matches = cls.get_matches_from_all_matches(html)

for match in main_page_matches:
    print(f"{mycolors.HEADER}MATCH : {match} ======================={mycolors.ENDC}")

    url = all_matches_url+"/"+match
    print(f"url: {mycolors.OKBLUE}{url}{mycolors.ENDC}")

    phtml = cls.get_html(url)
    players = cls.get_players_from_match(phtml)

    for player in players:
        sleep()
        print(f"{mycolors.OKCYAN}{player}{mycolors.ENDC}")

        url = site+"/player/"+player[0]+player_matches_filter
        print(f"url: {mycolors.OKBLUE}{url}{mycolors.ENDC}")

        player_page_html = cls.get_html(url)
        player_matches = cls.get_matches_from_player(player_page_html)

        for pmatch_id in player_matches:

            if pmatch_id in seen_ids:
                print(f"{mycolors.WARNING}Match ({pmatch_id}) already seen. Skipping{mycolors.ENDC}")
                continue

            seen_ids.add(pmatch_id)

            sleep()

            url = site + "/match/" + pmatch_id
            print(f"url: {mycolors.OKBLUE}{url}{mycolors.ENDC}")

            pmatch_html = cls.get_html(url)

            pplayers = cls.get_players_from_match(pmatch_html)
            steamlink = cls.get_steam_link(cls.get_watch_demo_url(pmatch_html))
            match_info = cls.get_match_information(pmatch_html)

            append2file(pmatch_id,steamlink[0],match_info["map"],match_info["server"],str(match_info["rank"]), match_info["type"], pplayers)
    
    print("")
    sleep()