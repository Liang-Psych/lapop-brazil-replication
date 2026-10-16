# Replication materials and erratum: Chinese development finance and Brazilian attitudes toward China

Xu, L. (2025). *The Impact of Chinese Development Finance on Brazilian Public Attitudes Toward China*. Master's thesis, China Agricultural University / Escola Superior de Agricultura "Luiz de Queiroz" (ESALQ), University of São Paulo (joint degree).

> **Erratum.** The dependent variable in the thesis was interpreted in the opposite direction of its coding. After correction there is no robust evidence that Chinese development finance projects are associated with Brazilians' trust in the Chinese government. See [`ERRATUM.md`](ERRATUM.md) for the full erratum in Chinese and English.

## What is in this repository

| Path | Content |
|---|---|
| `ERRATUM.md` | Erratum (Chinese and English): the error, its cause, affected sections with page numbers, corrected results and conclusions |
| `ANALYSIS_PLAN.md` | Analysis plan for the extended corrected analyses, committed before they were run; deviation log; results summary |
| `lapop_12.R` … `lapop_23.R`, `re_ana.R`, `efa.R`, `censobr.R` | Original thesis scripts, unchanged |
| `re_ana_corrected.R`, `pixi.toml` | Corrected analysis in R |
| `re_ana_corrected_py.py` | The same corrected analysis in Python (pyfixest) |
| `replicate_thesis_tables.py` | Replicates thesis Tables 2–6 and their corrected-direction versions |
| `build_plan_data.py`, `run_plan_v1.py` | Data construction and estimation for the pre-specified extended analyses |
| `check_dashboard.py` | Compares the raw data with LAPOP's official online dashboard |
| `results/` | Aggregate results (regression tables and coefficients only; no respondent-level data) |
| `brazil_aid.gpkg` | AidData Geospatial Global Chinese Development Finance Dataset v3.0, Brazil subset |
| `PIB_2010-2021.xlsx` | IBGE municipal GDP |
| `municipios.csv`, `estados.csv` | Municipal seat coordinates (kelvins/municipios-brasileiros) |

## Data not included: AmericasBarometer (LAPOP)

LAPOP's terms of use do not allow its data files to be passed to third parties, so the survey data are **not** included in this repository, and neither are files derived from them at the respondent level. To replicate:

1. Register and download the Brazil country files for 2012, 2014, 2017, 2019, 2021 and 2023 from the [LAPOP data repository](https://www.vanderbilt.edu/lapop/raw-data.php).
2. Save them in the repository root as `Brazil_2012.dta`, `Brazil_2014.dta`, `Brazil_2017.dta`, `Brazil_2019.dta`, `Brazil_2021.dta` and `Brazil_2023.dta`.
3. Run the original wave scripts `lapop_12.R` … `lapop_23.R` (they use `geobr`, which downloads municipal boundaries) and export each wave as `bra_lapop_YY.txt`, as in the first lines of `re_ana.R`.
4. Run the corrected analyses:
   - R: `pixi run corrected`
   - Python: `python re_ana_corrected_py.py`, `python replicate_thesis_tables.py`, `python build_plan_data.py`, then `python run_plan_v1.py` (requires `pyfixest`, `geopandas`, `statsmodels`, `wildboottest`, `openpyxl`)

## Licences and attribution

- Code: MIT licence (see `LICENSE`).
- AidData's dataset is licensed under the Open Data Commons Attribution Licence (ODC-By); geospatial data derived from OpenStreetMap are licensed under the Open Database Licence (ODbL). Source: [aiddata/gcdf-geospatial-data](https://github.com/aiddata/gcdf-geospatial-data).
- Municipal GDP: Instituto Brasileiro de Geografia e Estatística (IBGE).
- Municipal coordinates: [kelvins/municipios-brasileiros](https://github.com/kelvins/municipios-brasileiros) (MIT), sourced from IBGE.
- AmericasBarometer data: LAPOP Lab, Vanderbilt University, [www.vanderbilt.edu/lapop](https://www.vanderbilt.edu/lapop). Not redistributed here.

## Contact

Liang Xu · questions about the erratum or replication can be raised in this repository's issue tracker.

## Version history

The commit history of this repository is carried over from the author's original working repository, with the LAPOP survey files and respondent-level derived files removed from every commit. Commit dates are unchanged; commit hashes differ from the original repository. In particular:

| Commit | Date (UTC+8) | Content |
|---|---|---|
| `0e38d44` | 2026-10-12 11:28 | Analysis plan v1.0 committed, before the extended analyses were run |
| `0490a0e` | 2026-10-12 11:34 | Extended analyses run; results and deviation log added |

The original repository, including the uncorrected thesis analysis as first published, is retained privately by the author.
