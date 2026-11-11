# Public-dataset swap option — ready, NOT applied

**Status: APPLIED Nov 11, 2026 — Faryal picked the Superstore public data and built the Power BI dashboard from it (300 rows, $77,903.06, 2014–2017).** The main project files (README, Power BI guide, DATACAMP-PLAN, `data/raw/` and `data/curated/`) now use this public data. The earlier sample data (300 in, 280 out, $23,631.06) is kept only as a backup in `data/sample-backup/`.

## Why this exists

The brief asks for a **public** dataset (Kaggle, an API, or open data).
The current raw file is Muse-created sample data. Faryal was asked on
Nov 5 which she wants: keep the sample, or swap in a real public dataset.
This folder is the swap, already built and verified, so the choice is
concrete instead of abstract.

## Source (real, public, citable)

- **Dataset:** "Superstore Dataset Final" on Kaggle —
  https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
- **File used:** `Sample-Superstore.csv`, 9,994 retail order lines, the
  classic Kaggle retail dataset (also mirrored in the public GitHub repo
  dheerajsk26/AWS_Superstore_DataEngineering_Project).
- **Rows used:** the **first 300 data rows in file order** — no
  cherry-picking. Anyone can reproduce this with
  `map_superstore.py` in this folder.
- **What it is:** real US superstore order lines (Furniture, Office
  Supplies, Technology), 2014–2017, US regions (Central, East, South,
  West). 274 different products in these 300 rows.

## How it maps to the project schema

| Project column | Superstore column | Note |
|---|---|---|
| OrderID | Order ID | e.g. `CA-2016-152156` |
| OrderDate | Order Date | Kept as `MM/DD/YYYY`, the source format; cleaning standardises it to ISO |
| Product | Product Name | |
| Category | Category | Furniture / Office Supplies / Technology |
| Quantity | Quantity | |
| Price | **derived: `round(Sales / Quantity, 2)`** | See the honest limit below |
| Region | Region | US regions, not Canadian provinces |

## Verified numbers (same cleaning script, same rules)

| Check | Sample file (current) | Public option (this folder) |
|---|---|---|
| Rows in (raw) | 300 | **300** |
| Removed — nulls | 13 | **0** |
| Removed — invalid | 7 | **0** |
| Rows out (curated) | 280 | **300** |
| Total sales (curated) | $23,631.06 | **$77,903.06** |
| Dates standardised | Yes, all `YYYY-MM-DD` | **Yes, all `YYYY-MM-DD`** |
| TotalAmount = Quantity × Price | Every row | **Every row (checked, 0 mismatches)** |
| Date range | Jan–Oct 2026 | **Mar 2014 – Dec 2017** |
| Top product | — | Lexmark MX611dhe Monochrome Laser Printer, $11,219.93 |
| Sales by category | — | Technology $32,667.02 · Furniture $28,126.36 · Office Supplies $17,110.42 |

Files in this folder: `sales_raw_public.csv` (300 rows),
`sales_curated_public.csv` (300 rows), `map_superstore.py` (reproduces
the raw file from the downloaded source).

## Honest limits — tell the teacher these, don't hide them

1. **US data, 2014–2017, not 2026 and not Canadian.** The dashboard
   title "Retail Sales Dashboard — 2026" would be wrong; it becomes
   "Retail Sales Dashboard — 2014–2017".
2. **Price is a derived discounted unit price.** The Superstore file
   stores the line total (Sales), not a unit price, and 174 of these
   300 lines carry a discount. So Price = Sales ÷ Quantity is the
   *discounted* unit price. Because of cent-rounding, the cleaned total
   ($77,903.06) sits **$0.75 below** the source Sales sum ($77,903.81).
   That 75¢ is a rounding effect of the derivation, not lost data.
3. **The public file was already clean — 0 rows removed.** The cleaning
   step still does real work (date standardising, type casts, derived
   TotalAmount, validation), but the "removed rows" story disappears.
   The honest line for the teacher: "validation found no nulls or
   invalid rows in this slice."
4. **Dates come in one format only** (`MM/DD/YYYY`), so the
   three-format date story in the current README goes away. The date
   step still standardises to ISO.
5. **First 300 rows in file order, not a time window.** The dates jump
   around (Mar 2014 – Dec 2017) because the file isn't sorted by date.

## If she picks the swap — exact checklist (nothing else changes)

1. Replace `data/raw/sales_raw.csv` with
   `public-option/sales_raw_public.csv` (rename to `sales_raw.csv`).
2. Replace `data/curated/sales_curated.csv` with
   `public-option/sales_curated_public.csv`.
3. README: dataset section → "Kaggle Superstore Dataset Final, first
   300 rows, 2014–2017, US regions"; validation table → 300 in, 0
   removed, 300 out, $77,903.06; known-issues line → single date
   format, no nulls/invalid found.
4. Power BI guide: "280 rows" → "300 rows"; expected KPI value
   $23,631.06 → **$77,903.06**; report title "2026" → "2014–2017".
5. Pipeline JSON (`pl_ingest_curate.json`): **no change** — column
   names are identical, so the Data Factory mapping still fits.
6. The 30-second teacher answer stays the same shape; only the
   dataset sentence changes: "public Kaggle Superstore data, first 300
   rows."

## If she keeps the sample

Delete or ignore this folder. The README already says "public-style
retail sales data" — she should be ready to tell her teacher plainly
that the file is sample data built for the project, if he asks where it
came from.
