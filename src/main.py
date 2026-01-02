import pandas as pd

def main():
    df = pd.read_csv("data/raw/2023-income-limits.csv")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print("\nMissing values:\n", df.isna().sum())

    df.to_csv("data/processed/clean.csv", index=False)

if __name__ == "__main__":
    main()
