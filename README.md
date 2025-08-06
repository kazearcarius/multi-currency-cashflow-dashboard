# Multi-Currency Cashflow Dashboard

A tool for consolidating cash balances and transactions across multiple bank accounts and currencies into a single EUR-based view. It ingests CSV exports or API feeds, converts each amount using European Central Bank FX rates, calculates daily net positions, and produces an Excel file ready for dashboarding.

## Features

- Read transactions from multiple banks (SEPA, SWIFT, digital banks) with date, amount and currency.
- Convert each transaction into EUR using forex-python and ECB rates.
- Aggregate daily inflows and outflows to compute net cash position.
- Output Excel workbook with transactions and cash position sheet.
- Designed to feed Power BI or other visualization tools.
