import sqlite3
import pandas as pd

def build_database():
    conn = sqlite3.connect("pharmeasy.db")
    regions = pd.DataFrame({'region': ['Hyderabad', 'Warangal', 'Visakhapatnam', 'Vijayawada', 'Guntur', 'Tirupati', 'Karimnagar', 'Nellore', 'Bengaluru', 'Kurnool']})
    regions.to_sql("regions_master", conn, if_exists="replace", index=False)
    df = pd.read_csv("orders_clean.csv")
    df.to_sql("orders_clean", conn, if_exists="replace", index=False)
    conn.close()

if __name__ == "__main__":
    build_database()
