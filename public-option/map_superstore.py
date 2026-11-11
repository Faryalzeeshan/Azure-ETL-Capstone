"""
map_superstore.py — build the public-dataset swap option for the capstone.

Reads the public Superstore source file (Kaggle "Superstore Dataset Final",
vivek468 — downloaded from its public GitHub mirror, see PUBLIC-OPTION-README.md)
and writes a 300-row raw file in the project's 7-column schema:

  OrderID, OrderDate, Product, Category, Quantity, Price, Region

Mapping (exact, reproducible):
  - Rows used: the FIRST 300 data rows of the source file, in file order.
    No cherry-picking; anyone re-running this gets the same 300 rows.
  - OrderID    <- Order ID          (e.g. CA-2016-152156)
  - OrderDate  <- Order Date        (kept as MM/DD/YYYY, the source format)
  - Product    <- Product Name
  - Category   <- Category
  - Quantity   <- Quantity
  - Price      <- round(Sales / Quantity, 2)  — derived unit price (see note)
  - Region     <- Region

NOTE on Price: the Superstore file stores the line total (Sales), not a unit
price, and 174 of these 300 lines carry a discount, so Sales is the
discounted line total. Price here is therefore the DISCOUNTED unit price,
Sales / Quantity rounded to cents. Because of that rounding, the cleaned
total (Quantity x Price summed) is $77,903.06, which is $0.75 below the
source Sales sum of $77,903.81. That 75-cent gap is a rounding effect of
the derivation, not lost data, and the README for this option says so.

Run from the capstone folder:
    python3 public-option/map_superstore.py
It expects the downloaded source at /tmp/superstore.csv (see README).
"""
import csv

SOURCE = "/tmp/superstore.csv"
OUT = "public-option/sales_raw_public.csv"
N_ROWS = 300


def main():
    with open(SOURCE, newline="", encoding="latin-1") as f:
        rows = list(csv.DictReader(f))[:N_ROWS]

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "OrderID", "OrderDate", "Product", "Category",
            "Quantity", "Price", "Region"])
        w.writeheader()
        for r in rows:
            qty = int(r["Quantity"])
            price = round(float(r["Sales"]) / qty, 2)
            w.writerow({
                "OrderID": r["Order ID"],
                "OrderDate": r["Order Date"],
                "Product": r["Product Name"],
                "Category": r["Category"],
                "Quantity": qty,
                "Price": f"{price:.2f}",
                "Region": r["Region"],
            })

    print(f"Rows written: {len(rows)} -> {OUT}")


if __name__ == "__main__":
    main()
