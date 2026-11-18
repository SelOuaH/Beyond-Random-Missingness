# Beyond Random Missingness

**Time-Series Imputation under Realistic Missing-Data Scenarios**

Research materials for the conference study *Beyond Random Missingness: Evaluating Time-Series Imputation under Diverse Missingness Patterns in Beehive IoT Sensors* (manuscript title in the supplied version; update this line when the final proceedings title is confirmed).

This study benchmarks six missing-data imputation methods on temperature, relative-humidity and hive-weight observations from the HOBOS/Schwartau dataset. Models developed with random missingness are evaluated without adaptation on random, periodic, block, sensor-dropout and mixed missingness, to examine generalisation under changes in missingness structure.

> **Repository status:** Documentation scaffold. The original experimental scripts, results files, dependency lockfile and licensed source-data access instructions must be added and verified before this repository can be claimed to reproduce the paper end-to-end. No implementation is included in this scaffold.

## Research questions

- How does the temporal structure and rate of missingness affect imputation error?
- How well do models developed under random missingness generalise to structured losses?
- Do learned models systematically outperform inexpensive deterministic baselines on these sensor signals?

## Experimental design

| Element | Protocol |
|---|---|
| Source | HOBOS/Schwartau 2018, complete selected portions |
| Signals | Temperature, relative humidity, hive weight; independent univariate tasks |
| Splitting | Chronological training (70%), validation (15%), test (15%) |
| Missingness patterns | Random, periodic, block, sensor dropout, mixed |
| Test rates | 5%, 10%, 20%, 30%, 40%, 50% (requested) |
| Test missingness seeds | 42, 123, 2024 |
| Train/validation masking rates | 5%, 10%, 20%, 30% random missingness |
| Validation mask seeds | 31415, 27182, 16180 |
| Model training seeds | 42, 123, 2024, 3407, 5678 |
| Models | Linear interpolation, LOCF, XGBoost, BRITS, SAITS, CSDI |
| Metrics | MAE, RMSE, sMAPE, Tolerance Accuracy (TA) |
| Scoring | Only artificially removed test positions; originally observed values retained |

For each sensor, five missingness patterns × six rates × three test-mask seeds produce 90 test cases, or **270 fixed test series** across three sensors. Five training seeds for each trainable approach generate 1,350 per-model evaluation records; deterministic baselines generate 270 each. Training seeds and missingness seeds play different roles and must not be conflated.

The paper notes that structured masking may result in achieved missingness rates slightly different from their nominal requested rates. Retain both rates in results metadata.

## Methods

- **Linear interpolation:** Uses surrounding observations to reconstruct gaps.
- **LOCF:** Carries the latest available observation forwards, with boundary treatment as documented in the manuscript.
- **XGBoost:** Uses lagged readings, rolling statistics and timestamp-derived predictors.
- **BRITS:** Bidirectional recurrent imputation.
- **SAITS:** Self-attention-based imputation.
- **CSDI:** Conditional score-based diffusion imputation; five generated samples are averaged for point estimates.

For BRITS, SAITS and CSDI, temperature uses 336-observation windows with stride 168, while humidity and weight use 56-observation windows with stride 28. Model-specific settings must be taken from the verified experiment scripts rather than inferred from this summary.

## Headline findings from the supplied manuscript

| Sensor | Linear interpolation MAE | Best learned method | Best learned MAE |
|---|---:|---|---:|
| Temperature | 1.168 | SAITS | 1.794 |
| Relative humidity | 0.141 | SAITS | 1.960 |
| Hive weight | 140.753 | SAITS | 641.824 |

Results are mean values averaged over the evaluated missingness patterns and rates. Units follow the source measurement scale. Linear interpolation produced the lowest MAE in **85/90 (94.4%)** sensor–pattern–rate conditions, with LOCF best in four and SAITS in one. These findings apply to the selected locally smooth signals and should not be generalised to all IoT time series.

## Repository layout

```text
.
├── README.md
├── .gitignore
├── configs/                  # Verified experiment configuration files (to add)
├── data/README.md            # Source-data provenance and acquisition notes
├── docs/REPRODUCIBILITY.md   # Reproduction requirements and verification checklist
├── results/
│   ├── tables/               # Exported numerical results (to add)
│   └── figures/              # Generated figures (to add)
└── src/
    ├── preprocessing/        # Original preprocessing scripts (to add)
    ├── missingness/          # Original masking scripts (to add)
    ├── imputation/           # Original imputation scripts (to add)
    └── evaluation/           # Original evaluation scripts (to add)
```

## Reproducing the experiments

The reproducible execution commands cannot be documented faithfully until the original source scripts and software environment are available. See [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) for the required files and checks. Do not execute models using the test series for hyperparameter selection.

## Data provenance

The study uses selected complete periods of the publicly available HOBOS/Schwartau dataset. The original sensor observations are not redistributed in this scaffold. See [`data/README.md`](data/README.md) for acquisition and redistribution considerations.

## Citation

Please cite the conference paper when its final bibliographic details are available. A `CITATION.cff` file should be added once the publication title, venue, year and DOI have been verified. The manuscript title shown above may differ from the repository description or the final proceedings title.

## Authors

Seloua Haddaoui, Ikram Guelib, Soumya-Soundous Toumi, Salim Chikhi and Amel Zouari (as listed in the supplied manuscript).

## Licence

No licence has been selected for the code or this scaffold. The repository owner should choose and add a licence after verifying the rights for any third-party implementations and data.
