#!/usr/bin/env python3

import sys
import pandas as pd
import os
import glob


def wrangle_csv(backup_dir):
    csv_files = glob.glob(os.path.join(backup_dir, "*.csv"))
    if not csv_files:
        print("No CSV files found.")
        return

    for file in csv_files:
        try:
            df = pd.read_csv(file, na_values=[" ", ""])

            # Transformations
            df = df.fillna("NA")  # null values - > NA
            df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]  # standardize col names
            df["row_number"] = range(1, len(df) + 1)  # add row count

            df.to_csv(file, index=False)  # save back
            print(f"Wrangled {file}, rows: {len(df)}")

        except Exception as e:
            print(f"Error processing {file}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: wrangler.py <backup_dir>")
        sys.exit(1)

    wrangle_csv(sys.argv[1])

