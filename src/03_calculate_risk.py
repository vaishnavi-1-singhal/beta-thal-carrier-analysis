"""
Step 3: Calculate carrier frequency and disease prevalence.

Applies Hardy-Weinberg equilibrium to each variant's allele frequency:
  Carrier frequency (heterozygotes) = 2 * q * (1 - q)
  Disease frequency (homozygotes)   = q^2
and sums across all variants with known allele frequency.

Input:  data/processed/hbb_variants_tracker.tsv
Output: data/processed/hbb_risk_analysis.tsv (full per-variant results)
        + printed summary totals
"""

import pandas as pd

IN_PATH = "data/processed/hbb_variants_tracker.tsv"
OUT_PATH = "data/processed/hbb_risk_analysis.tsv"


def main():
    calc_data = pd.read_csv(IN_PATH, sep="\t")

    calc_data["Carrier_Frequency"] = (
        2 * calc_data["Allele_Frequency"] * (1 - calc_data["Allele_Frequency"])
    )
    calc_data["Disease_Frequency"] = calc_data["Allele_Frequency"] ** 2

    total_carrier = calc_data["Carrier_Frequency"].sum()
    total_disease = calc_data["Disease_Frequency"].sum()

    print(f"Carrier frequency: {total_carrier:.6f}  (1 in {1/total_carrier:.0f})")
    print(f"Disease prevalence: {total_disease:.8f}  (1 in {1/total_disease:.0f})")

    calc_data.to_csv(OUT_PATH, sep="\t", index=False)
    print(f"\nFull per-variant results written to: {OUT_PATH}")


if __name__ == "__main__":
    main()
