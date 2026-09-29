import pandas as pd
import numpy as np

np.random.seed(42)
n_rows = 2159

regions = ['Hyderabad', 'Warangal', 'Visakhapatnam', 'Vijayawada', 'Guntur', 'Tirupati', 'Karimnagar', 'Nellore', 'Bengaluru']
categories = ['Vitamins', 'Pain Relief', 'Personal Care', 'Baby Care', 'First Aid', 'Devices']

dates = pd.date_range(start='2026-04-01', end='2026-06-30', periods=n_rows)

data = {
    'order_id': [f"ORD{str(i).zfill(6)}" for i in range(1, n_rows + 1)],
    'order_date': dates,
    'region': np.random.choice(regions, n_rows),
    'category': np.random.choice(categories, n_rows),
    'product': [f"Product_{np.random.randint(1, 20)}" for _ in range(n_rows)],
    'sales_inr': np.round(np.random.uniform(100, 5000, n_rows), 2),
    'profit_inr': np.round(np.random.uniform(10, 800, n_rows), 2)
}

df = pd.DataFrame(data)
# Add exact duplicates
df = pd.concat([df, df.iloc[:59]], ignore_index=True)
df.to_csv("pharmeasy_orders_raw.csv", index=False)
