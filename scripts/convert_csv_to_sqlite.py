import argparse
import sqlite3
import pandas as pd
from pathlib import Path

def convert(csv_path, db_path, table_name):
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    print(f"Reading {csv_path} ...")
    df = pd.read_csv(csv_file)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    print(f"Rows: {len(df):,}  |  Columns: {len(df.columns)}")
    print(f"Writing to {db_path} (table: {table_name}) ...")
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Done! '{db_path}' is ready.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("db_path")
    parser.add_argument("--table-name", default="data")
    args = parser.parse_args()
    convert(args.csv_path, args.db_path, args.table_name)
