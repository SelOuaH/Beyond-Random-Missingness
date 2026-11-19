# Data Preprocessing

This directory contains the preprocessing scripts for the HOBOS/Schwartau beehive sensor dataset used in the ICMSCT 2026 time-series imputation benchmark.

## Preprocessing Protocol

Three sensor streams are processed independently:

| Sensor | Selected period (2018) | Observations | Sampling resolution |
|---|---|---:|---|
| Temperature | 1 July – 31 December | 4,416 | Hourly |
| Relative humidity | 15 May – 31 December | 462 | 12-hourly |
| Hive weight | 1 August – 31 December | 306 | 12-hourly |

Each complete sensor series is chronologically partitioned into 70% training, 15% validation, and 15% testing.

| Sensor | Training | Validation | Test |
|---|---:|---:|---:|
| Temperature | 3,091 | 662 | 663 |
| Relative humidity | 323 | 69 | 70 |
| Hive weight | 214 | 46 | 46 |

The original observed values are retained as ground truth, while artificially masked copies are generated separately for model development and evaluation.

For trainable deep-learning methods, standardisation parameters are estimated exclusively from finite observations in the corresponding incomplete training series. Validation and test data are transformed using the same parameters, and predictions are returned to the original measurement scale before evaluation.

## Implementation Status

The original preprocessing scripts and verified execution commands will be added to this directory.

No replacement preprocessing implementation is provided at this stage.
