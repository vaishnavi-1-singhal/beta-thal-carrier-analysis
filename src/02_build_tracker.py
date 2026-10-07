"""
Step 2: Build the working variant tracker.

Input:  data/manual/hbb_variants_annotated.tsv
        (the manually annotated file from step 1 — must already have
        'Allele Frequency' and 'Status' columns filled in)
Output: data/processed/hbb_variants_tracker.tsv
"""

import os
import pandas as pd

IN_PATH = "data/manual/hbb_variants_annotated.tsv"
OUT_PATH = "data/processed/hbb_variants_tracker.tsv"


def main():
    data = pd.read_csv(IN_PATH, sep="\t")

    tracker = pd.DataFrame({
        "Variation ID": data["VariationID"],
        "Allele ID": data["AlleleID(s)"],
        "rsID": data["dbSNP ID"],
        "GRCh38 Location": data["GRCh38Location"],
        "Names": data["Name"],
        "Allele_Frequency": data["Allele Frequency"],
        "Mapping_Method": "",   # rsID / Coordinate / HGVS
        "Status": data["Status"],   # Pending / Done / NotFound
        "Notes": "",
    })

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    tracker.to_csv(OUT_PATH, sep="\t", index=False)
    print(f"Tracker written to: {OUT_PATH}")
    print(f"Total variants in tracker: {len(tracker)}")
    print(f"Variants with known allele frequency: {(tracker['Allele_Frequency'] > 0).sum()}")


if __name__ == "__main__":
    main()
