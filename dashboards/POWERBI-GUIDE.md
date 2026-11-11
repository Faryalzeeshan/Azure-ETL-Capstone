# Power BI Dashboard — Build Guide

Build this in **Power BI Desktop** on your own computer, from the curated file:
`data/curated/sales_curated.csv` (300 rows, already cleaned — Kaggle Superstore public data, 2014–2017).

## Connect the data

1. Open Power BI Desktop.
2. **Get Data → Text/CSV** → pick `sales_curated.csv` → **Load**.
3. Check the columns: OrderID, OrderDate, Product, Category, Quantity,
   Price, Region, TotalAmount. OrderDate should be a Date type.

## One report page — 5 visuals

| # | Visual | Settings |
|---|---|---|
| 1 | **Card (KPI)** | Field: TotalAmount, set to **Sum**. Title: "Total Sales". Expected value: $77,903.06 |
| 2 | **Bar chart** | Axis: Product. Values: Sum of TotalAmount. Title: "Sales by Product" |
| 3 | **Line chart** | Axis: OrderDate (year level). Values: Sum of TotalAmount. Title: "Sales by Year" |
| 4 | **Slicer** | Field: Region. Title: "Filter by Region" |
| 5 | **Table** | Columns: Product, Category, Sum of TotalAmount. Sort by TotalAmount, largest first. Title: "Top Products" |

## Finish

- Add a report title at the top: "Retail Sales Dashboard_2014-2017".
- Give every visual a clear title (see above).
- Save the file as `dashboards/Retail_Sales_Dashboard.pbix`.
- Take a screenshot of the finished page for the GitHub repo and the report.

## What the dashboard should show

- Total sales of **$77,903.06** across 300 clean orders (2014–2017).
- Which products sell the most (bar chart).
- Whether sales rise or fall month by month (line chart).
- How each region compares (use the slicer to filter).
