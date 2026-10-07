# Beta-Thalassemia Carrier Frequency & Disease Prevalence Estimation in South Asian Populations

## Overview

This project estimates the carrier frequency and disease prevalence of beta-thalassemia in South Asian populations, based on pathogenic and likely pathogenic variants in the *HBB* gene curated from ClinVar, using allele frequencies from the gnomAD South Asian (SAS) subpopulation.

Beta-thalassemia is an autosomal recessive blood disorder caused by mutations in *HBB*, and it disproportionately affects South Asian populations. This project applies the Hardy-Weinberg principle to publicly available variant data to produce a data-driven estimate of how common carriers and affected individuals are likely to be in this population.

## Data Sources

- **ClinVar** — pathogenic and likely pathogenic *HBB* variants associated with beta-thalassemia, including variant name, protein change, accession/variation ID, genomic location, variant type, molecular consequence, and germline classification.
- **gnomAD (South Asian / SAS subpopulation)** — allele frequency for each variant, matched to the corresponding ClinVar entry. Allele frequency is the key input to the Hardy-Weinberg calculation below.

> Note: exact ClinVar and gnomAD access/version dates should be filled in here for full reproducibility — see "How to Reproduce" below.

## Method

For each variant, allele frequency (**q**) from gnomAD SAS was used to estimate:

- **Carrier frequency** (heterozygotes): `2 × q × (1 − q)`
- **Disease frequency** (homozygotes/affected): `q²`

These per-variant estimates were summed across all variants with known allele frequency to produce an overall estimate, following the standard Hardy-Weinberg equilibrium model:

```
p + q = 1
p² + 2pq + q² = 1
```

where `p` is the frequency of the normal allele and `q` is the frequency of the pathogenic allele at a given variant site.

## Pipeline

```
data/
  raw/        <- original ClinVar export
  manual/     <- clean + manually annotated intermediate files
  processed/  <- final tracker and results
src/
  01_clean_clinvar.py
  02_build_tracker.py
  03_calculate_risk.py
```

1. **`src/01_clean_clinvar.py`** — loads the raw ClinVar export (`data/raw/clinvar_result.txt`), reports total variant count, and writes `data/manual/hbb_variants_clean.tsv`.
2. **Manual step (not scripted):** open `data/manual/hbb_variants_clean.tsv` and add two columns by hand — `Allele Frequency` (from gnomAD, South Asian/SAS subpopulation) and `Status` (Pending/Done/NotFound, tracking lookup progress per variant). Save the result as `data/manual/hbb_variants_annotated.tsv`. This step is manual because gnomAD frequency lookup for each variant was done one at a time rather than through a programmatic API call — a documented limitation, not an oversight.
3. **`src/02_build_tracker.py`** — reads the manually annotated file and restructures it into a clean working tracker (variant ID, allele ID, rsID, genomic location, name, allele frequency, mapping status, notes) at `data/processed/hbb_variants_tracker.tsv`.
4. **`src/03_calculate_risk.py`** — computes per-variant carrier and disease frequency, sums across all variants, prints the overall carrier frequency and disease prevalence, and writes full per-variant results to `data/processed/hbb_risk_analysis.tsv`.

Run in order, from the project root:
```bash
python src/01_clean_clinvar.py
# --- manual step here: annotate and save data/manual/hbb_variants_annotated.tsv ---
python src/02_build_tracker.py
python src/03_calculate_risk.py
```

## Results

| Metric | Value |
|---|---|
| Total *HBB* variants curated from ClinVar | 51 |
| Variants with known gnomAD SAS allele frequency | 12 (24%) |
| Estimated carrier frequency | ~1.95% (approx. 1 in 51) |
| Estimated disease prevalence | ~1 in 31,100 |

## Comparison to Published Literature

Published beta-thalassemia carrier rates in South Asia generally range from **~3% to 8%**, varying by country and region — for example, ~4.05% across pooled Indian schoolchildren studies (Delhi/Mumbai), an Indian average cited around 3.3% (with regional studies ranging from under 1% up to 17%), and a national Pakistani estimate of ~5–8% (with some local studies reporting substantially higher rates in specific districts).

This project's estimate (~1.95%) is **lower than the published range**, which is expected and discussed in Limitations below — it is a floor estimate built only from the variants with available gnomAD SAS frequency data, not a full population-level clinical estimate.

## Limitations

- **Ascertainment gap**: only 12 of 51 curated ClinVar *HBB* variants had a nonzero gnomAD SAS allele frequency. The remaining 39 variants (mostly large deletions and rare indels) are excluded from the calculation simply because they are too rare to appear in gnomAD, not because they are clinically insignificant. This means the estimate here is a **lower bound** — true carrier frequency and disease prevalence are likely higher.
- **Independence assumption**: this analysis sums `2pq` across variants as if each were an independent locus. In reality, all variants are alleles of the same gene (*HBB*), so an individual could be a compound heterozygote carrying two different pathogenic *HBB* variants. A more rigorous model would treat total pathogenic allele frequency at the *HBB* locus as `q_total = Σq_i` and apply Hardy-Weinberg once at the gene level, rather than summing per-variant heterozygote estimates independently.
- **Data source scope**: results reflect only variants classified as pathogenic/likely pathogenic in ClinVar at the time of access, and only frequencies available in gnomAD SAS; variants absent from either database are not represented.
- **No regional resolution**: gnomAD SAS aggregates multiple South Asian countries/ethnic groups, which have meaningfully different carrier rates (e.g., northern Pakistan vs. broader national estimates). This analysis cannot resolve sub-regional variation.

## How to Reproduce

```bash
git clone <repo-url>
cd beta-thal-carrier-analysis
pip install -r requirements.txt
python src/01_clean_clinvar.py
# manually annotate data/manual/hbb_variants_clean.tsv with gnomAD SAS
# allele frequencies and Status, save as data/manual/hbb_variants_annotated.tsv
python src/02_build_tracker.py
python src/03_calculate_risk.py
```

Raw data used:
- `data/raw/clinvar_result.txt` — ClinVar export (fill in access date)
- gnomAD SAS allele frequencies added by hand during the manual annotation step (fill in gnomAD version/date)

## Future Improvements

- Model compound heterozygosity explicitly using gene-level pathogenic allele frequency.
- Break down carrier frequency contribution by variant type (point mutation vs. indel vs. large deletion) and by ClinVar review status/confidence.
- Incorporate country- or ethnicity-level gnomAD subpopulation data where available, rather than aggregate SAS.
- Visualize allele frequency contribution per variant as a bar chart.
