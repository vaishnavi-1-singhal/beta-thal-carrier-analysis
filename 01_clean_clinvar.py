"""
Step 1: Load the raw ClinVar export and do basic cleaning.

Input:  data/raw/clinvar_result.txt       (raw ClinVar export)
Output: data/manual/hbb_variants_clean.tsv

After this script runs, there is a MANUAL step before step 2:
open data/manual/hbb_variants_clean.tsv and add two columns by hand:
  - "Allele Frequency"  (from gnomAD, South Asian / SAS subpopulation)
  - "Status"            (Pending / Done / NotFound, tracking lookup progress)
Save the result as data/manual/hbb_variants_annotated.tsv
"""

import os
import pandas as pd

RAW_PATH = "data/raw/clinvar_result.txt"
OUT_PATH = "data/manual/hbb_variants_clean.tsv"


def main():
    data = pd.read_csv(RAW_PATH, sep="\t")
    print(f"Total variants loaded: {len(data)}")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    data.to_csv(OUT_PATH, sep="\t", index=False)
    print(f"Cleaned file written to: {OUT_PATH}")
    print()
    print("NEXT STEP (manual, not scripted):")
    print("  Add 'Allele Frequency' (gnomAD SAS) and 'Status' columns by hand,")
    print("  then save as data/manual/hbb_variants_annotated.tsv")


if __name__ == "__main__":
    main()
