"""
Multi‑Currency Cashflow Dashboard
================================

This script reads transaction data from multiple bank accounts in different
currencies, converts them into a base currency (EUR) and aggregates daily
cash positions. The output is written to an Excel file and can be used
to feed a dashboard tool like Power BI.

Dependencies:
    pandas, forex_python
"""

import argparse
from datetime import datetime
import pandas as pd

try:
    from forex_python.converter import CurrencyRates
except ImportError:
    CurrencyRates = None  # If forex_python is unavailable, conversion must be done manually


def load_transactions(csv_paths: list[str]) -> pd.DataFrame:
    """Load and concatenate transaction exports from multiple banks."""
    frames = []
    for path in csv_paths:
        df = pd.read_csv(path, parse_dates=['Date'])
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def convert_to_eur(row: pd.Series, fx: CurrencyRates) -> float:
    """Convert the amount into EUR using the given CurrencyRates object."""
    if row['Currency'] == 'EUR':
        return row['Amount']
    rate = fx.get_rate(row['Currency'], 'EUR', row['Date'].date())
    return round(row['Amount'] * rate, 2)


def build_cash_positions(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate net cash positions per day across accounts."""
    positions = df.groupby(['Date'])['Amount_EUR'].sum().reset_index()
    positions.rename(columns={'Amount_EUR': 'NetPositionEUR'}, inplace=True)
    return positions


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate multi‑currency cash positions into EUR.")
    parser.add_argument("--inputs", nargs='+', required=True, help="CSV files containing bank transactions with Date, Amount, Currency columns")
    parser.add_argument("--output", required=True, help="Excel file to write the dashboard source data")
    args = parser.parse_args()

    df = load_transactions(args.inputs)
    if CurrencyRates is None:
        raise RuntimeError("forex_python is required for FX conversion")
    fx = CurrencyRates()
    df['Amount_EUR'] = df.apply(lambda r: convert_to_eur(r, fx), axis=1)
    positions = build_cash_positions(df)
    with pd.ExcelWriter(args.output) as writer:
        df.to_excel(writer, sheet_name='Transactions', index=False)
        positions.to_excel(writer, sheet_name='CashPositions', index=False)
    print(f"Dashboard data saved to {args.output}")


if __name__ == '__main__':
    main()