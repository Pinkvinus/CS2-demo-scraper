from csgo.sharecode import decode

steam_url="steam://rungame/730/76561202255233023/+csgo_download_match%20CSGO-O7LXF-6jxDY-cM3eu-OBqCV-7FFdH"
steam_url="steam://rungame/730/76561202255233023/+csgo_download_match%20CSGO-O7LXF-6jxDY-cM3eu-OBqCV-7FFdH"

filename="match730_003720612134233571706_1582537776_182.dem"

# Your match sharing code
#share_code = "CSGO-O7LXF-6jxDY-cM3eu-OBqCV-7FFdH"
share_code = "CSGO-uKSea-7zaRF-TWAf9-9wT6t-FsFiJ"
filename="match730_003720617515827593527_1414147351_187"

# Decode the sharing code
decoded = decode(share_code)

# Extract relevant data
match_id = decoded["matchid"]
outcome_id = decoded["outcomeid"]
token_id = decoded["token"]

# Display decoded information
print("Match ID:", match_id)
print("Outcome ID:", outcome_id)
print("Token ID:", token_id)

from datetime import datetime

# Example value
value = 1414147351
print(datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S'))