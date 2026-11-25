# Data

This directory contains documentation and local storage conventions for the HOBOS/Schwartau beehive sensor observations used in the study *Beyond Random Missingness: Evaluating Time-Series Imputation under Diverse Missingness Patterns in Beehive IoT Sensors*.

## Data Source

The experiments use the publicly available [Bee Hive Metrics dataset](https://www.kaggle.com/datasets/se18m502/bee-hive-metrics), derived from the HOBOS/Schwartau monitoring project.

Three independent sensor series from 2018 are considered:

| Sensor | Period | Observations | Temporal resolution |
|---|---|---:|---|
| Temperature | 1 July–31 December 2018 | 4,416 | Hourly |
| Relative humidity | 15 May–31 December 2018 | 462 | 12-hourly |
| Hive weight | 1 August–31 December 2018 | 306 | 12-hourly |

## Directory Organisation

- `raw/` — Original sensor input files: `T_2018.csv`, `H_2018.csv`, and `W_2018.csv`.
- `processed/` — Selected sensor observations, chronological data partitions, and generated experimental datasets.

## Data Preparation

The original observations are processed using `src/preprocessing/00_prepare_new_data_portable.py`.

The preprocessing procedure preserves the original ground-truth measurements, parses timestamps using the day–month–year format, validates the selected observations, and partitions each series chronologically into training (70%), validation (15%), and testing (15%).

Artificial missingness is introduced subsequently, without replacing the retained ground-truth observations.

## Data Availability and Redistribution

The original dataset is maintained by its third-party provider. Researchers should obtain the source files from the referenced dataset repository and consult the applicable usage and redistribution terms.

Raw sensor observations are not included in this repository by default.
