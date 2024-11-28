from csgo.sharecode import decode
import csv
import subprocess

steamlink = "steam://rungame/730/76561202255233023/+csgo_download_match%20CSGO-38jZH-2shwO-Pj2A7-x5qsy-fqbNE"

def steamlink_to_sharecode(url:str):
    return url.split("%20")[1]

def sharecode_to_outcomeid(share_code):
    return decode(share_code)["outcomeid"]

def steamlink_to_outcomeid(url:str):
    return sharecode_to_outcomeid(steamlink_to_sharecode(url))

def is_match_downloaded(url:str, path:str):
    """
        parameters: 
            - steam link with match sharing code. Ex: \"steam://rungame/730/76561202255233023/+csgo_download_match%20CSGO-xxxxx-xxxxx-xxxxx-xxxxx-xxxxx\"
            - Download folder: path to the folder where the demofiles are stored.
        returns
            - bool: True if match corresponding to the steamlink was found in the download folder. False if not.
    """
    outcome_id = sharecode_to_outcomeid(url)
    #TODO

def check_duplicate_outcomeids(filepath):
    """
        Parameters: File path to a csv file that needs to be checked for duplicate outcomeid values
        Returns: 
    """
    # Track seen IDs to filter duplicates
    seen_ids = set()
    duplicate_ids = set()

    with open(filepath, 'r') as infile:
        reader = csv.reader(infile)
        #header = next(reader)
        
        for row in reader:
            outcome_id = steamlink_to_outcomeid(row[1])

            #print(f"{outcome_id}")
            if outcome_id in seen_ids:
                print(f"Outcome ID duplicate: {outcome_id}")
                duplicate_ids.add(row[1])
                continue

            seen_ids.add(row[1])

    if len(duplicate_ids) != 0:
        print("Duplicates found")
    else:
        print("No duplicates have been seen")

    return duplicate_ids
        
print(check_duplicate_outcomeids("cs_scrape_2024-11-27 09:27:45.128459.csv"))

subprocess.run(["ls","-a"]) 