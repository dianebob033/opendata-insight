import pandas as pd

def main():
    input_path = "data/raw/2023-income-limits.csv"
    output_path = "data/processed/clean.csv"

    df = pd.read_csv(input_path)

    print("Rows:", len(df))
    print("Columns:", df.columns.tolist())
    print("\nMissing values:\n", df.isna().sum())

    df.to_csv(output_path, index=False)
    print(f"\nSaved cleaned data to: {output_path}")

if __name__ == "__main__":
    main()
