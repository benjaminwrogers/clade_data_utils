# Uses utility functions to output list of variants of interest.

import polars as pl
from utility.data_utility import *

variant_dat = pl.read_csv('data/metadata.tsv.zst', separator='\t', )

clean_dat = variant_prep(variant_dat)

variant_list = variants_to_model(clean_dat)

#print(variant_list)
# write the list to a text file

# Make sure target file is empty
open('variants_list.txt', 'w').close()

# Fill it with the variants of interest
with open('variants_list.txt', 'w') as outfile:
    outfile.write("\n".join(variant_list))