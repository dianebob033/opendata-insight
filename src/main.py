import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Configuration
# ----------------------------
INPUT_PATH = "data/raw/2023-income-limits.csv"
OUTPUT_PATH = "data/processed/clean_v1.csv"
FIG_DIR = "reports/figures"

# Use 4-person household columns for comparability
COLUMNS_TO_USE = [
    "County",
    "AMI",
    "ELI_4",
    "VLI_4",
    "LI_4",
    "MOD_4",
]


# ----------------------------
# Helpers
# ----------------------------
def ensure_dirs() -> None:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, usecols=COLUMNS_TO_USE)

    # Basic cleaning: ensure numeric columns are numeric
    numeric_cols = [c for c in df.columns if c != "County"]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    return df


def compute_ratios(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Avoid divide-by-zero
    df = df[df["AMI"].notna() & (df["AMI"] > 0)].copy()

    df["ELI_to_AMI"] = df["ELI_4"] / df["AMI"]
    df["LI_to_AMI"] = df["LI_4"] / df["AMI"]

    return df


def print_summary(df: pd.DataFrame) -> None:
    print("Rows:", len(df))
    print("Columns used:", df.columns.tolist())

    print("\nTop 5 counties by AMI:")
    print(df.sort_values("AMI", ascending=False).head(5)[["County", "AMI"]])

    print("\nBottom 5 counties by AMI:")
    print(df.sort_values("AMI", ascending=True).head(5)[["County", "AMI"]])

    ratios = df[["ELI_to_AMI", "LI_to_AMI"]].mean(numeric_only=True)
    print("\nAverage ratios:")
    print(ratios)


def plot_ami_distribution(df: pd.DataFrame) -> None:
    plt.figure(figsize=(8, 5))
    plt.hist(df["AMI"].dropna(), bins=20)
    plt.title("Distribution of AMI by County (4-Person Household)")
    plt.xlabel("AMI")
    plt.ylabel("Number of Counties")
    plt.tight_layout()

    out = os.path.join(FIG_DIR, "ami_distribution.png")
    plt.savefig(out, dpi=200)
    plt.close()


def _fit_line(x: np.ndarray, y: np.ndarray):
    """
    Returns (x_line, y_line, slope, intercept) for a simple linear fit.
    """
    mask = np.isfinite(x) & np.isfinite(y)
    x2, y2 = x[mask], y[mask]
    if len(x2) < 2:
        return None

    slope, intercept = np.polyfit(x2, y2, 1)
    x_line = np.linspace(x2.min(), x2.max(), 100)
    y_line = slope * x_line + intercept
    return x_line, y_line, slope, intercept


def plot_ratios_scatter(df: pd.DataFrame) -> None:
    """
    Scatter: AMI vs (ELI/AMI) and (LI/AMI)
    - Adds trend lines (linear fit)
    - Annotates the highest and lowest AMI counties
    """
    x = df["AMI"].to_numpy(dtype=float)
    y_eli = df["ELI_to_AMI"].to_numpy(dtype=float)
    y_li = df["LI_to_AMI"].to_numpy(dtype=float)

    plt.figure(figsize=(8, 5))
    plt.scatter(x, y_eli, label="ELI_4 / AMI")
    plt.scatter(x, y_li, label="LI_4 / AMI")

    # Trend lines
    fit_eli = _fit_line(x, y_eli)
    if fit_eli is not None:
        x_line, y_line, slope, intercept = fit_eli
        plt.plot(x_line, y_line, linewidth=2, label=f"ELI trend (slope={slope:.4g})")

    fit_li = _fit_line(x, y_li)
    if fit_li is not None:
        x_line, y_line, slope, intercept = fit_li
        plt.plot(x_line, y_line, linewidth=2, label=f"LI trend (slope={slope:.4g})")

    # Annotate extreme AMI counties (highest & lowest)
    hi = df["AMI"].idxmax()
    lo = df["AMI"].idxmin()

    for idx, tag in [(hi, "Highest AMI"), (lo, "Lowest AMI")]:
        row = df.loc[idx]
        county = str(row["County"])
        ami = float(row["AMI"])

        # Annotate near the LI ratio point (more visually separated)
        y_point = float(row["LI_to_AMI"]) if np.isfinite(row["LI_to_AMI"]) else float(row["ELI_to_AMI"])
        plt.annotate(
            f"{tag}: {county}",
            (ami, y_point),
            textcoords="offset points",
            xytext=(8, 8),
            ha="left",
            fontsize=9,
        )

    plt.title("Income Limit Ratios vs AMI (4-Person Household)")
    plt.xlabel("AMI")
    plt.ylabel("Ratio")
    plt.legend()
    plt.tight_layout()

    out = os.path.join(FIG_DIR, "eli_li_ratio_scatter.png")
    plt.savefig(out, dpi=200)
    plt.close()


def main() -> None:
    ensure_dirs()

    df = load_data(INPUT_PATH)
    df = compute_ratios(df)

    print_summary(df)

    # Save processed output
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved analysis output to: {OUTPUT_PATH}")

    # Figures
    plot_ami_distribution(df)
    plot_ratios_scatter(df)
    print(f"Saved figures to: {FIG_DIR}/")


if __name__ == "__main__":
    main()
