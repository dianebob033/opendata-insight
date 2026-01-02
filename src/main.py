import matplotlib.pyplot as plt
import pandas as pd

# -----------------------------
# Configuration
# -----------------------------
INPUT_PATH = "data/raw/2023-income-limits.csv"
OUTPUT_PATH = "data/processed/clean_v1.csv"

COLUMNS_TO_USE = [
    "County",
    "AMI",
    "ELI_4",
    "VLI_4",
    "LI_4",
    "MOD_4",
]

# -----------------------------
# Data Loading
# -----------------------------
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, usecols=COLUMNS_TO_USE)

# -----------------------------
# Basic Analysis
# -----------------------------
def compute_ratios(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["ELI_to_AMI"] = df["ELI_4"] / df["AMI"]
    df["LI_to_AMI"] = df["LI_4"] / df["AMI"]

    return df

# -----------------------------
# Reporting
# -----------------------------
def print_summary(df: pd.DataFrame) -> None:
    print("\nTop 5 counties by AMI:")
    print(df.sort_values("AMI", ascending=False).head(5)[["County", "AMI"]])

    print("\nBottom 5 counties by AMI:")
    print(df.sort_values("AMI").head(5)[["County", "AMI"]])

    print("\nAverage ratios:")
    print(df[["ELI_to_AMI", "LI_to_AMI"]].mean())
    
def plot_ami_distribution(df: pd.DataFrame) -> None:
    plt.figure(figsize=(8, 5))
    plt.hist(df["AMI"], bins=20)
    plt.title("Distribution of AMI by County (4-Person Household)")
    plt.xlabel("AMI")
    plt.ylabel("Number of Counties")
    plt.tight_layout()
    plt.savefig("reports/figures/ami_distribution.png")
    plt.close()

# -----------------------------
# Main Pipeline
# -----------------------------
def main():
    df = load_data(INPUT_PATH)

    print("Rows:", len(df))
    print("Columns used:", df.columns.tolist())

    df = compute_ratios(df)

    print_summary(df)
    
    plot_ami_distribution(df)
    print("Saved figure: reports/figures/ami_distribution.png")

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved analysis output to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
