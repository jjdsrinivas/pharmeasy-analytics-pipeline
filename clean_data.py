import pandas as pd

def build_cleaning_pipeline():
    df = pd.read_csv("pharmeasy_orders_raw.csv")
    df = df.drop_duplicates()
    if "region" in df.columns:
        df["region"] = df["region"].str.strip().str.title()
    df.to_csv("orders_clean.csv", index=False)
    return df

def validate_schema(df, required_columns):
    missing = [c for c in required_columns if c not in df.columns]
    return {"status": "validated" if not missing else "blocked_schema", "row_count": len(df), "missing_columns": missing}

if __name__ == "__main__":
    build_cleaning_pipeline()
