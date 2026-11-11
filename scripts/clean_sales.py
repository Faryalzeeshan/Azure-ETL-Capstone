"""
clean_sales.py — transformation step for the Azure ETL capstone.

Reads the raw retail sales file (data/raw/sales_raw.csv) and writes the
cleaned file (data/curated/sales_curated.csv).

Transformations applied:
  1. Drop rows with a missing OrderDate, Quantity, or Price (null handling).
  2. Drop invalid rows: Quantity <= 0 or Price <= 0.
  3. Standardize OrderDate to ISO format YYYY-MM-DD
     (raw file mixes YYYY-MM-DD, MM/DD/YYYY, and DD-MM-YYYY).
  4. Cast Quantity to int and Price to float (type changes).
  5. Add derived column: TotalAmount = Quantity * Price.

This script mirrors what the Azure Data Factory Mapping Data Flow does in
the cloud pipeline (pl_ingest_curate). It is kept in the repo so the
transformation logic is reviewable and reproducible without Azure.
"""

import csv
from datetime import datetime

RAW_PATH = "data/raw/sales_raw.csv"
CURATED_PATH = "data/curated/sales_curated.csv"

DATE_FORMATS = ("%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y")


def parse_date(value):
    """Try each known raw format; return ISO date string or None."""
    value = value.strip()
    if not value:
        return None
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def main():
    with open(RAW_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    total_in = len(rows)
    removed_nulls = 0
    removed_invalid = 0
    cleaned = []

    for row in rows:
        order_date = parse_date(row["OrderDate"])
        qty_raw = row["Quantity"].strip()
        price_raw = row["Price"].strip()

        # 1. Null handling
        if order_date is None or qty_raw == "" or price_raw == "":
            removed_nulls += 1
            continue

        qty = int(qty_raw)
        price = float(price_raw)

        # 2. Invalid records
        if qty <= 0 or price <= 0:
            removed_invalid += 1
            continue

        # 3-5. Standardized date, typed values, derived column
        cleaned.append({
            "OrderID": row["OrderID"],
            "OrderDate": order_date,
            "Product": row["Product"],
            "Category": row["Category"],
            "Quantity": qty,
            "Price": f"{price:.2f}",
            "Region": row["Region"],
            "TotalAmount": f"{qty * price:.2f}",
        })

    with open(CURATED_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(cleaned[0].keys()))
        writer.writeheader()
        writer.writerows(cleaned)

    print(f"Rows in:            {total_in}")
    print(f"Removed (nulls):    {removed_nulls}")
    print(f"Removed (invalid):  {removed_invalid}")
    print(f"Rows out:           {len(cleaned)}")
    print(f"Total sales:        ${sum(float(r['TotalAmount']) for r in cleaned):,.2f}")


if __name__ == "__main__":
    main()
