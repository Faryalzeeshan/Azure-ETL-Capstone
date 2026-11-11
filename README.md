# Azure End-to-End ETL Capstone — Retail Sales

**Program:** Data Engineering / Diploma Program
**Weight:** 20% of final course grade
**Student:** Faryal Zeeshan
**Dataset:** Kaggle "Superstore Dataset Final" — first 300 rows in file order (Mar 2014 – Dec 2017, US regions, under 100 MB)

## What this project does

An end-to-end ETL pipeline in Microsoft Azure:

```
Data Source → Azure Blob (Raw) → Azure Data Factory → Transformation → Azure Blob (Curated) → Power BI
```

1. The raw sales file lands untouched in the **raw** Blob container.
2. Azure Data Factory pipeline **pl_ingest_curate** copies it and transforms it.
3. The cleaned file is written to the **curated** Blob container.
4. Power BI Desktop builds a dashboard from the curated file.

## Business question

Which products, categories, and regions drive sales, and how do sales trend year by year (2014–2017)?

## Dataset

| Item | Detail |
|---|---|
| Source file | `data/raw/sales_raw.csv` (original, never edited) |
| Rows | 300 orders |
| Columns | OrderID, OrderDate, Product, Category, Quantity, Price, Region |
| Size | Under 100 MB |
| Known quality issues | No nulls or invalid rows found in this 300-row slice. Dates arrive in one format (MM/DD/YYYY) and are standardised to ISO. Price is derived as Sales ÷ Quantity (discounted unit price — see Honest limits below). |

## Transformation (what the pipeline cleans)

1. **Remove null rows** — any row missing OrderDate, Quantity, or Price is dropped.
2. **Filter invalid records** — Quantity ≤ 0 or Price ≤ 0 is dropped.
3. **Standardize dates** — all OrderDate values converted to ISO format `YYYY-MM-DD`.
4. **Fix data types** — Quantity to integer, Price to decimal.
5. **Derived column** — `TotalAmount = Quantity × Price`.

The same logic is implemented twice, so it can be reviewed without Azure:
- In Azure: Mapping Data Flow `dfl_clean_sales` (see `pipelines/pl_ingest_curate.json`).
- Locally: `scripts/clean_sales.py` (same rules, same output).

## Validation (verified run)

| Check | Result |
|---|---|
| Rows in (raw) | 300 |
| Removed — nulls | 0 |
| Removed — invalid | 0 |
| Rows out (curated) | 300 |
| Total sales (curated) | $77,903.06 |
| Dates standardized | Yes — all `YYYY-MM-DD` |
| TotalAmount check | Quantity × Price on every row |

Pipeline run check (in Azure): open **Monitor** in Data Factory and confirm the
run status is **Succeeded**, then open the curated container and confirm
`sales_curated.csv` is present with 300 rows.

## Honest limits — tell the teacher these, don't hide them

1. **US data, 2014–2017, not 2026 and not Canadian.** The dashboard title is "Retail Sales Dashboard_2014-2017".
2. **Price is a derived discounted unit price.** The Superstore source stores the line total (Sales), not a unit price, and 174 of these 300 lines carry a discount. Price = Sales ÷ Quantity. Because of cent-rounding, the cleaned total ($77,903.06) sits $0.75 below the source Sales sum ($77,903.81) — a rounding effect, not lost data.
3. **The public file was already clean — 0 rows removed.** Validation found no nulls or invalid rows in this slice. The cleaning step still does real work (date standardising, type casts, derived TotalAmount, validation).
4. **First 300 rows in file order, not a time window.** Dates jump around (Mar 2014 – Dec 2017) because the source file isn't sorted by date.
5. **Source:** "Superstore Dataset Final" on Kaggle — https://www.kaggle.com/datasets/vivek468/superstore-dataset-final — reproduced with `public-option/map_superstore.py`. The earlier Muse-made sample data (300 in, 280 out, $23,631.06) is kept only as a backup in `data/sample-backup/` and is NOT the data in this project.

## Azure resources

| Resource | Name pattern |
|---|---|
| Resource Group | `rg-capstone-faryal` |
| Storage Account | Same region as the resource group |
| Blob containers | `raw`, `curated` |
| Data Factory | Same resource group |
| Pipeline | `pl_ingest_curate` |
| Trigger | On-demand (manual run; a daily trigger is optional) |

## Power BI dashboard

One report page, built in Power BI Desktop from `data/curated/sales_curated.csv`:

1. **KPI card** — Total Sales ($77,903.06)
2. **Bar chart** — Total Sales by Product
3. **Line chart** — Total Sales by Year (2014–2017)
4. **Slicer** — Region (or Category)
5. **Table** — Top products by TotalAmount

See `dashboards/POWERBI-GUIDE.md` for the step-by-step build.

## Cost control

- Small dataset (300 rows, under 100 MB).
- One pipeline, only a few runs.
- No always-on or expensive services (no VMs, no SQL Database, no Databricks).
- Free tier: Azure for Students ($100 credit, 12 months, no credit card).
- **Cleanup:** delete the resource group after submission/demo — this deletes
  the storage account, Data Factory, and all resources inside it at once.

## Folder structure

```
/azure-etl-capstone/
├── data/
│   ├── raw/                  # sales_raw.csv (original landing copy)
│   └── curated/              # sales_curated.csv (cleaned output)
├── pipelines/
│   └── pl_ingest_curate.json # Data Factory pipeline definition
├── scripts/
│   └── clean_sales.py        # same transformation logic, runnable locally
├── dashboards/
│   ├── POWERBI-GUIDE.md      # Power BI build steps
│   └── Retail_Sales_Dashboard.pbix  # built Nov 11, 2026 (on Faryal's laptop — upload this file)
├── public-option/             # how the Superstore swap was built (map_superstore.py)
└── data/sample-backup/        # earlier sample data, kept only as backup — NOT the project data
```

## How to run it (in Azure)

1. Create the resource group, storage account, and the `raw` / `curated` containers.
2. Upload `data/raw/sales_raw.csv` to the `raw` container.
3. Create the Data Factory, link it to the storage account, and create the raw + curated datasets.
4. Create/import the `pl_ingest_curate` pipeline and publish.
5. Run it in Debug (or Trigger), then check Monitor for **Succeeded**.
6. Open the curated container and verify `sales_curated.csv`.
7. Build the Power BI report from the curated file.
8. Take screenshots (resource group, containers, Monitor run, dashboard) for the report.
9. Delete the resource group after submission.
