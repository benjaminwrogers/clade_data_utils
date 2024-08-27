# Uses utility functions to output list of variants of interest.

import polars as pl
from utility.data_utility import data_prep, clades_to_model
from urllib.request import urlretrieve
import json
from datetime import date


# Download latest data
url = "https://data.nextstrain.org/files/ncov/open/metadata.tsv.zst"
filename = "data/metadata.tsv.zst"

urlretrieve(url, filename)

# Read in data
clade_dat = pl.read_csv('data/metadata.tsv.zst', separator='\t', )

# Produce clean version of data with counts of clades
clean_dat = data_prep(clade_dat)

# Produce list of variants above 1%, (or if more than 9 of these, the top 9 over the past 3 weeks)
clade_list_today = clades_to_model(clean_dat)

# Load existing json file, if it exists, so we can append to it
try:
    with open('clade_list.json', 'r') as f:
        clade_history = json.load(f)
except FileNotFoundError:
    clade_history = []

# Get today's date
today = date.today().strftime("%Y-%m-%d")

# Check if today's date already exists in the data
for entry in clade_history:
    if entry["date"] == today:
        # If it exists, replace the entry
        entry["clades"] = clade_list_today
        break
else:
    # If it doesn't exist, append a new entry
    clade_history.append({"date": today, "clades": clade_list_today})

# Write the updated data to the JSON file
with open('clade_list.json', 'w') as f:
    json.dump(clade_history, f, indent=4)


