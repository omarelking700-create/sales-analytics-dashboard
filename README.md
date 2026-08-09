# OMARX Analytics

Professional Streamlit dashboard for sales, profit, profit margin and business insights.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Recommended Excel/CSV columns

- Product
- Date
- Price
- Cost
- Quantity

The dashboard automatically calculates:
- Total Sales = Price × Quantity
- Profit = (Price - Cost) × Quantity
- Profit Margin = Profit ÷ Total Sales × 100

You can also provide existing `Profit` or `Total Sales` columns.
