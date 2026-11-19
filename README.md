# Beyond Random Missingness

**Time-Series Imputation under Realistic Missing-Data Scenarios**

Official research repository for the conference paper:

**Beyond Random Missingness: Evaluating Time-Series Imputation under Diverse Missingness Patterns in Beehive IoT Sensors**

This study investigates the robustness and generalisation of time-series imputation methods under heterogeneous missing-data scenarios in Internet of Things (IoT) sensor streams.

Using real-world temperature, relative-humidity, and hive-weight observations from the HOBOS/Schwartau dataset, we benchmark six imputation methods under five missingness patterns and six missingness rates.

The central objective is to examine whether models developed under random missingness can reliably reconstruct observations affected by structured and prolonged data losses.

## Research Contributions

The study provides:

1. **Cross-missingness benchmarking:** A controlled evaluation covering random, periodic, block, sensor-dropout, and mixed missingness.
2. **Generalisation assessment:** Trainable models are developed exclusively under random missingness and evaluated without adaptation across five missingness patterns.
3. **Comparative evaluation:** Six imputation techniques are assessed under a common experimental protocol using chronological data partitioning, repeated training, and missing-only evaluation.
4. **Statistical comparison:** Friedman and Holm-corrected Wilcoxon signed-rank tests are used to examine differences in reconstruction performance.

## Dataset

Experiments use selected complete periods from the publicly available [HOBOS/Schwartau beehive dataset](https://www.kaggle.com/datasets/se18m502/bee-hive-metrics).

Three sensor variables are considered independently:

| Sensor | Observation period (2018) | Samples | Resolution |
|---|---|---:|---|
| Temperature | 1 July – 31 December | 4,416 | Hourly |
| Relative humidity | 15 May – 31 December | 462 | 12-hourly |
| Hive weight | 1 August – 31 December | 306 | 12-hourly |

Each series is chronologically divided into:

- Training: 70%
- Validation: 15%
- Testing: 15%

Complete observations are retained as ground truth, and artificial missingness is introduced to evaluate reconstruction accuracy.

## Experimental Protocol

### Missingness Scenarios

Five missingness patterns are considered:

| Pattern | Description |
|---|---|
| Random | Independently selected missing observations |
| Periodic | Missing observations distributed at regular intervals |
| Block | Multiple contiguous missing-data intervals |
| Sensor dropout | A single extended consecutive data loss |
| Mixed | Combination of approximately 40% random, 30% block, and 30% periodic missingness |

The evaluation covers six nominal missingness rates:

**5%, 10%, 20%, 30%, 40%, and 50%.**

### Training, Validation and Testing

| Dataset partition | Missingness patterns | Rates (%) | Purpose |
|---|---|---|---|
| Training | Random | 5, 10, 20, 30 | Model development |
| Validation | Random | 5, 10, 20, 30 | Hyperparameter selection |
| Test | Random, periodic, block, sensor dropout, mixed | 5, 10, 20, 30, 40, 50 | Final evaluation |

Three missingness seeds are used for the test benchmark: `42`, `123`, and `2024`.

Validation masks use three independent seeds: `31415`, `27182`, and `16180`.

Five independent model-training seeds are used for trainable methods: `42`, `123`, `2024`, `3407`, and `5678`.

The fixed test benchmark contains:

**3 sensors × 5 patterns × 6 rates × 3 missingness seeds = 270 test datasets.**

Trainable methods produce 1,350 evaluation records per method, reflecting the five training seeds.

Periodic masks are deterministic and consequently identical across missingness seeds at the same rate.

### Compared Imputation Methods

Six methods representing different methodological families are evaluated:

| Method | Category |
|---|---|
| Linear Interpolation | Deterministic temporal interpolation |
| LOCF | Last Observation Carried Forward |
| XGBoost | Gradient-boosted regression |
| BRITS | Bidirectional recurrent imputation |
| SAITS | Self-attention-based imputation |
| CSDI | Conditional score-based diffusion imputation |

Models are tuned independently for temperature, humidity, and weight using validation Mean Absolute Error (MAE).

For BRITS, SAITS, and CSDI, overlapping sequences are constructed using:

- Temperature: window length 336, stride 168.
- Humidity and weight: window length 56, stride 28.

The selected configurations are retained during final cross-missingness evaluation.

No hyperparameters are selected using the test benchmark.

## Evaluation Metrics

Performance is evaluated exclusively at artificially removed positions using:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Symmetric Mean Absolute Percentage Error (sMAPE)
- Tolerance Accuracy (TA)

Tolerance Accuracy uses sensor-specific tolerances derived exclusively from the complete training data.

MAE and RMSE are the primary reconstruction-error measures. Tolerance Accuracy provides supplementary information but may exhibit saturation for some sensor variables.

## Principal Results

The table summarises overall performance averaged across missingness patterns, rates, and experimental repetitions where applicable.

| Sensor | Method | MAE | RMSE | sMAPE (%) | TA |
|---|---|---:|---:|---:|---:|
| Temperature | Linear Interpolation | **1.452** | **1.898** | **10.208** | **0.895** |
| Temperature | Best learned: XGBoost | 2.168 | 2.848 | 15.280 | 0.766 |
| Humidity | Linear Interpolation | **0.112** | **0.168** | **0.113** | **1.000** |
| Humidity | Best learned: SAITS | 1.923 | 2.108 | 1.954 | 0.998 |
| Weight | Linear Interpolation | **138.693** | **172.164** | **0.211** | **1.000** |
| Weight | Best learned: SAITS | 418.500 | 471.227 | 0.635 | 1.000 |

### Key Findings

Linear interpolation achieved the lowest overall MAE, RMSE, and sMAPE across all three sensors.

It uniquely achieved the lowest mean MAE in **80 of 90 sensor–pattern–rate conditions (88.9%)**. LOCF achieved the lowest mean MAE in eight conditions, XGBoost in one, and one additional condition resulted in a tie between linear interpolation and LOCF.

Among learned methods:

- XGBoost performed best on temperature and achieved the only learned-method condition-level win, under 5% block missingness.
- SAITS achieved the lowest overall MAE among learned methods for humidity and weight.
- Sensor dropout generally caused greater reconstruction difficulty than random and periodic missingness.

These findings indicate that increased model complexity does not necessarily improve reconstruction accuracy for locally smooth IoT sensor signals.

The conclusions are specific to the examined univariate sensor streams, single deployment, and experimental protocol.

## Statistical Analysis

Exploratory statistical comparisons were performed using:

- Friedman tests across the six imputation methods.
- Kendall's coefficient of concordance.
- Pairwise Wilcoxon signed-rank tests with Holm correction.

The analyses identified significant performance differences between methods across the evaluated conditions.

Because the comparisons are based on dependent conditions from the same dataset, statistical significance should be interpreted as within-benchmark evidence rather than proof of generalisability across independent deployments.

## Repository Structure

The repository is being organised as follows:

```text
Beyond-Random-Missingness/
├── README.md
├── .gitignore
├── requirements.txt
├── CITATION.cff
├── configs/
├── data/
│   └── README.md
├── docs/
│   └── REPRODUCIBILITY.md
├── src/
│   ├── preprocessing/
│   ├── missingness/
│   ├── imputation/
│   └── evaluation/
└── results/
    ├── tables/
    └── figures/
```

The structure above represents the intended organisation. Source code, configurations, results and supporting files will be added as the repository is completed.

## Reproducibility and Code Availability

The experimental implementation, missingness-generation procedures, hyperparameter configurations and evaluation scripts are being prepared for public release.

The final repository will document the execution environment, dataset preparation procedure, model configurations, random seeds and commands required to reproduce the reported results.

Until the original experimental scripts and dependencies are incorporated and verified, the repository should be considered a work in progress rather than a validated end-to-end reproduction package.

## Data Availability

The original sensor data are publicly accessible through the [Bee Hive Metrics dataset on Kaggle](https://www.kaggle.com/datasets/se18m502/bee-hive-metrics).

Data acquisition and preprocessing instructions will be provided separately. Redistribution of third-party data remains subject to the original dataset's applicable terms.

## Citation

If you use the experimental methodology or results, please cite:

Haddaoui, S., Guelib, I., Toumi, S.-S., Chikhi, S., and Zouari, A. *Beyond Random Missingness: Evaluating Time-Series Imputation under Diverse Missingness Patterns in Beehive IoT Sensors.*

Final proceedings details and the DOI will be added when available.

## Authors

- Seloua Haddaoui
- Ikram Guelib
- Soumya-Soundous Toumi
- Salim Chikhi
- Amel Zouari

MISC Laboratory and NTIC Faculty, University of Abdelhamid Mehri – Constantine 2, Algeria.

## Licence

The repository licence will be specified after verification of the rights associated with the original implementation and any third-party components.
