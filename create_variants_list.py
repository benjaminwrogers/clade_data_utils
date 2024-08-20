# Uses utility functions to output list of variants of interest.

import polars as pl
from utility.data_utility import variant_prep, variants_to_model
from urllib.request import urlretrieve


# Download latest data
url = "https://data.nextstrain.org/files/ncov/open/metadata.tsv.zst"
filename = "data/metadata.tsv.zst"

urlretrieve(url, filename)

# Read in data
variant_dat = pl.read_csv('data/metadata.tsv.zst', separator='\t', )

# Produce clean version of data with counts of clades
clean_dat = variant_prep(variant_dat)

# Produce list of variants above 1%, (or if more than 9 of these, the top 9 over the past 3 weeks)
variant_list = variants_to_model(clean_dat)

#print(variant_list)
# write the list to a text file

# Make sure target file is empty
open('variants_list.txt', 'w').close()

# Fill it with the variants of interest
with open('variants_list.txt', 'w') as outfile:
    outfile.write("\n".join(variant_list))