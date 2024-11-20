import cloudscrape as cls
import random
import time


sleep_timer = (2,6)
site = "https://csstats.gg"
all_matches_url = "https://csstats.gg/match"
player_matches_filter = "?platforms=Valve&modes=Competitive~Premier#/matches"


def sleep():
    t = random.uniform(sleep_timer[0], sleep_timer[1])
    print(f"sleep for {t}")
    time.sleep(t)

html = cls.get_html(all_matches_url)
main_page_matches = cls.get_matches_from_all_matches(html)

for match in main_page_matches:
    print(f"MATCH : {match} =======================")

    url = all_matches_url+"/"+match
    print(f"url: {url}")

    phtml = cls.get_html(url)
    players = cls.get_players_from_match(phtml)

    for player in players:
        sleep()
        print(player)

        url = site+"/player/"+player[0]+player_matches_filter
        print(f"url: {url}")

        player_page_html = cls.get_html(url)
        player_matches = cls.get_matches_from_player(player_page_html)


        for pmatch_id in player_matches:

            sleep()

            url = site + "/match/" + pmatch_id
            print(url)

            pmatch_html = cls.get_html(url)
            pplayers = cls.get_players_from_match(pmatch_html)
            for pplayer in pplayers:
                print(pplayer)
    
    print("")
    sleep()