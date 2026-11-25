# -*- coding: utf-8 -*-
"""Prepare the selected 2018 HOBOS series and chronological data splits.

Read-only sources: training_Data/{T,H,W}_2018.csv (DD-MM-YY HH:MM).
Replaced outputs: training_Data/{Temperature,Humidity,Weight}.csv,
                  dataMissing/<sensor>/complete/*_complete.csv,
                  experiment_selected_2018/split_summary.csv.

Existing missingness masks and model results are NOT modified; regenerate
those separately after running this script.
"""

from pathlib import Path

import numpy as np
import pandas as pd



# Repository root
BASE = Path(__file__).resolve().parents[2]

# Original source data (read-only)
SOURCE_DIR = BASE / "data" / "raw"

# Generated data
NEW_BASE = BASE / "data" / "processed"
SELECTED_DIR = NEW_BASE / "selected"
DATA_DIR = NEW_BASE / "dataMissing"

# Sensor, raw filename, value column, first date, last date, sample count.
SENSORS = {
    "Temperature": ("T_2018.csv", "temperature", "2018-07-01", "2018-12-31", 4416),
    "Humidity": ("H_2018.csv", "humidity", "2018-05-15", "2018-12-31", 462),
    "Weight": ("W_2018.csv", "weight", "2018-08-01", "2018-12-31", 306),
}

RAW_DATE_FORMAT = "%d-%m-%y %H:%M"
OUTPUT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def prepare_sensor(raw_file, value_column, start, end, expected_count):
    """Parse dates explicitly and select the agreed period without imputation."""
    source = SOURCE_DIR / raw_file
    if not source.is_file():
        raise FileNotFoundError(f"Raw source not found: {source}")

    data = pd.read_csv(source)
    if list(data.columns) != ["timestamp", value_column]:
        raise ValueError(f"Unexpected columns in {source}: {list(data.columns)}")

    # CRITICAL: The original source uses day-month-year, not month-day-year.
    data["timestamp"] = pd.to_datetime(
        data["timestamp"], format=RAW_DATE_FORMAT, errors="raise"
    )
    data[value_column] = pd.to_numeric(data[value_column], errors="raise")

    end_exclusive = pd.Timestamp(end) + pd.Timedelta(days=1)
    selected = data.loc[
        (data["timestamp"] >= pd.Timestamp(start))
        & (data["timestamp"] < end_exclusive),
        ["timestamp", value_column],
    ].sort_values("timestamp").reset_index(drop=True)

    if len(selected) != expected_count:
        raise ValueError(
            f"{raw_file}: expected {expected_count} rows, found {len(selected)}"
        )
    if selected.isna().any().any():
        raise ValueError(f"{raw_file}: selected period contains missing values")
    if selected["timestamp"].duplicated().any():
        raise ValueError(f"{raw_file}: duplicate timestamps")
    if not np.isfinite(selected[value_column].to_numpy()).all():
        raise ValueError(f"{raw_file}: non-finite values")
    return selected


def main():
    # Validate all three raw sources BEFORE replacing any derived files.
    prepared = {
        sensor: prepare_sensor(*spec)
        for sensor, spec in SENSORS.items()
    }

    summary = []
    for sensor, selected in prepared.items():
        value_column = SENSORS[sensor][1]
        selected.to_csv(
            SOURCE_DIR / f"{sensor}.csv",
            index=False,
            date_format=OUTPUT_DATE_FORMAT,
        )  # Replaces the previous selected CSV; original raw CSV untouched.

        n = len(selected)
        train_end = int(n * 0.70)
        validation_end = int(n * 0.85)
        splits = {
            "train": selected.iloc[:train_end],
            "validation": selected.iloc[train_end:validation_end],
            "test": selected.iloc[validation_end:],
        }

        out_dir = DATA_DIR / sensor / "complete"
        out_dir.mkdir(parents=True, exist_ok=True)
        for split, part in splits.items():
            output = out_dir / f"{value_column}_{split}_complete.csv"
            part.to_csv(output, index=False, date_format=OUTPUT_DATE_FORMAT)
            summary.append({
                "Sensor": sensor,
                "Split": split,
                "N": len(part),
                "Start": part["timestamp"].min(),
                "End": part["timestamp"].max(),
            })

        print(
            f"{sensor}: selected={n}, train={len(splits['train'])}, "
            f"validation={len(splits['validation'])}, test={len(splits['test'])}"
        )

    pd.DataFrame(summary).to_csv(NEW_BASE / "split_summary.csv", index=False)
    print("\nDATA PREPARATION PASSED")
    print(f"Updated selected CSVs: {SOURCE_DIR}")
    print(f"Updated complete splits: {DATA_DIR}")
    print("Existing missingness masks and model results were not modified.")
    print("Regenerate the masks before any model evaluation.")


if __name__ == "__main__":
    main()
