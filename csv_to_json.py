#!/usr/bin/env python3
"""
CSV → JSON converter for Talent Hub style data.

Features
- Auto-detects array columns like `aiSpecialization[0]`, `aiTools[1]`, etc., and merges them into arrays.
- Keeps all other columns as-is.
- Attempts to coerce `yearsExperience` to int if present.
- Ignores blank/NaN array values.
- CLI usage with input/output paths.
"""

import argparse
import json
import math
import os
import re
from typing import Dict, List, Any

import pandas as pd


ARRAY_COL_PATTERN = re.compile(r"^(?P<base>[^\[]+)\[(?P<idx>\d+)\]$")


def is_nan(val: Any) -> bool:
    try:
        return val is None or (isinstance(val, float) and math.isnan(val))
    except Exception:
        return False


def normalize_value(val: Any) -> Any:
    """Convert NaN-like values to None; trim strings."""
    if is_nan(val):
        return None
    if isinstance(val, str):
        s = val.strip()
        return s if s != "" else None
    return val


def collect_array_fields(columns: List[str]) -> Dict[str, List[str]]:
    """
    Identify columns that follow the "<base>[index]" pattern and group them by base name.
    Returns: { base: [col1, col2, ...] } with column names sorted by index.
    """
    groups: Dict[str, List[tuple]] = {}
    for col in columns:
        m = ARRAY_COL_PATTERN.match(col)
        if m:
            base = m.group("base")
            idx = int(m.group("idx"))
            groups.setdefault(base, []).append((idx, col))

    # sort by index and return only names
    sorted_groups: Dict[str, List[str]] = {}
    for base, pairs in groups.items():
        pairs.sort(key=lambda x: x[0])
        sorted_groups[base] = [name for _, name in pairs]
    return sorted_groups


def row_to_record(row: pd.Series, array_groups: Dict[str, List[str]]) -> Dict[str, Any]:
    record: Dict[str, Any] = {}

    # First, process non-array columns
    array_cols = {c for cols in array_groups.values() for c in cols}
    for col in row.index:
        if col in array_cols:
            continue  # handled below
        val = normalize_value(row[col])
        record[col] = val

    # Attempt to coerce yearsExperience to int if present and safe
    if "yearsExperience" in record and record["yearsExperience"] is not None:
        try:
            record["yearsExperience"] = int(float(str(record["yearsExperience"])))
        except Exception:
            # leave as-is if not convertible
            pass

    # Now build arrays for each grouped base
    for base, cols in array_groups.items():
        arr: List[Any] = []
        for c in cols:
            v = normalize_value(row.get(c))
            if v is not None:
                arr.append(v)
        record[base] = arr

    return record


def convert_csv_to_json(input_csv: str, output_json: str) -> None:
    df = pd.read_csv(input_csv)

    # Identify array-style columns and build grouping
    array_groups = collect_array_fields(list(df.columns))

    # Convert rows
    records = [row_to_record(row, array_groups) for _, row in df.iterrows()]

    # Write JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)


def main():
    parser = argparse.ArgumentParser(description="Convert CSV with array-style columns to JSON.")
    parser.add_argument("input_csv", help="Path to the input CSV file.")
    parser.add_argument("output_json", nargs="?", help="Path to the output JSON file (default: <input>.json).")
    args = parser.parse_args()

    input_csv = args.input_csv
    output_json = args.output_json or os.path.splitext(input_csv)[0] + ".json"

    convert_csv_to_json(input_csv, output_json)
    print(f"✓ Wrote JSON to: {output_json}")


if __name__ == "__main__":
    main()
