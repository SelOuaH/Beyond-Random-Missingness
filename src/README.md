# Source Code

This directory contains the experimental implementation accompanying the conference paper *Beyond Random Missingness: Evaluating Time-Series Imputation under Diverse Missingness Patterns in Beehive IoT Sensors*.

The implementation will be organised into four components:

- `preprocessing/` — Sensor data preparation, chronological partitioning, and standardisation.
- `missingness/` — Controlled generation of random, periodic, block, sensor-dropout, and mixed missingness.
- `imputation/` — Implementation and configuration of the six evaluated imputation methods: Linear Interpolation, LOCF, XGBoost, BRITS, SAITS, and CSDI.
- `evaluation/` — Missing-only reconstruction metrics, experiment aggregation, and statistical comparisons.

The original experimental scripts will be incorporated and verified against the methodology reported in the paper.

**Status:** Source-code organisation in progress.
