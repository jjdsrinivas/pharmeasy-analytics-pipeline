import sqlite3
import pandas as pd

conn = sqlite3.connect("pharmeasy.db")
q_left = "SELECT COUNT(*) FROM regions_master r LEFT JOIN orders_clean o ON r.region = o.region"
q_inner = "SELECT COUNT(*) FROM regions_master r INNER JOIN orders_clean o ON r.region = o.region"
print("LEFT JOIN count:", pd.read_sql_query(q_left, conn).iloc[0, 0])
print("INNER JOIN count:", pd.read_sql_query(q_inner, conn).iloc[0, 0])
conn.close()
