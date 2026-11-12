"""US economic data API: GDP, inflation, jobs, interest rates, the yield curve, Fed decisions and trade

Runnable examples: each one is a single request to the DataPorium API.

    python examples.py                      # list the examples
    python examples.py gdp
    python examples.py gdp --csv out.csv
    python examples.py gdp --json       # the raw answer

Needs a DataPorium API key in the DATAPORIUM_API_KEY environment variable.
"""
from __future__ import annotations

import argparse
import json
import sys

from dataporium import DataPorium, to_frame

# name: (question, method, parameters, key of the rows inside the answer)
EXAMPLES = {
    'gdp': ('US GDP', 'economic_metrics', {'economic_metrics': 'GDP'}, None),
    'unemployment-rate': ('Unemployment rate', 'economic_metrics', {'economic_metrics': 'unemployment_Rate'}, None),
    'payrolls': ('Nonfarm payrolls', 'economic_metrics', {'economic_metrics': 'total_Non_farm_Payroll'}, None),
    'cpi': ('Consumer price index (CPI)', 'economic_metrics', {'economic_metrics': 'CPI'}, None),
    'recession-probability': ('Recession probability', 'economic_metrics', {'economic_metrics': 'smoothed_US_Recession_Probabilities'}, None),
    'inflation-by-category': ('Which prices are rising fastest: 25 categories, newest month', 'inflation_categories', {'latest': True, 'sort': 'yoy_pct', 'order': 'desc'}, None),
    'rent-inflation-history': ('Shelter and rent inflation since 2020', 'inflation_categories', {'category': 'shelter,rent', 'month_from': '2020-01', 'sort': 'month', 'order': 'asc', 'limit': 500}, None),
    'fed-next-meeting': ('The next Federal Reserve meetings and the current target range', 'fed_decisions', {'status': 'upcoming', 'order': 'asc'}, None),
    'fed-cuts': ('Every Fed rate cut since 2019', 'fed_decisions', {'decision': 'cut', 'date_from': '2019-01-01', 'order': 'asc'}, None),
    'yield-curve': ('The Treasury yield curve today, a month ago and a year ago', 'treasury_yields_curve', {'compare': '1m,1y'}, None),
    'treasury-yields': ('2-year and 10-year Treasury yields, monthly since 2000', 'treasury_yields', {'maturity': '2y,10y', 'date_from': '2000-01-01', 'frequency': 'monthly', 'order': 'asc', 'limit': 1000}, None),
    'mortgage-rate': ('30-year fixed mortgage rate', 'economic_metrics', {'economic_metrics': '30Year_Fixed_Rate_Mortgage_Average'}, None),
    'corporate-bonds': ('High-grade corporate bond yields and their spread over Treasuries', 'corporate_bond_yields', {'month_from': '2020-01', 'order': 'asc'}, None),
    'jobless-claims': ('Weekly unemployment claims, US', 'layoffs_official_claims', {'state': 'US', 'date_from': '2026-01-01'}, None),
    'state-unemployment': ('States ranked by unemployment, newest month', 'local_jobs', {'area_type': 'state', 'latest': True, 'sort': 'unemployment_rate', 'order': 'desc', 'limit': 60}, None),
    'layoffs-rate': ('Official layoffs and discharges (JOLTS)', 'layoffs_official_jolts', {'area': 'US', 'latest': True}, None),
    'trade-deficits': ('Largest US trade deficits by country, last 12 months', 'us_trade_summary', {'dimension': 'country', 'period': 'last_12_months', 'sort': 'balance', 'order': 'asc', 'limit': 10}, None),
    'trade-china': ('Monthly trade with China since 2024', 'us_trade', {'dimension': 'country', 'code': '5700', 'month_from': '2024-01', 'order': 'asc'}, None),
    'economic-calendar': ('Release dates of consumer price index (CPI) reports', 'market_calendar', {'event_name': 'CPI YY'}, None),
    'gas-prices': ('Gas prices in the states of the weekly survey, newest week', 'gas_prices', {'area_type': 'state', 'product': 'regular', 'latest': True, 'sort': 'price_usd', 'order': 'desc'}, None),
}


def rows(answer, key=None):
    """The answer as a DataFrame, or None when it has no table in it."""
    try:
        frame = to_frame(answer, key=key)
    except (KeyError, TypeError):
        return None
    return frame if len(frame) > 1 else None  # one record reads better as JSON


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("example", nargs="?", help="Name of the example; leave out to list them")
    parser.add_argument("--csv", help="Save the rows to this CSV file")
    parser.add_argument("--json", action="store_true", help="Print the raw JSON answer")
    parser.add_argument("--rows", type=int, default=20, help="Rows to print (default 20)")
    args = parser.parse_args(argv)

    if not args.example:
        width = max(len(name) for name in EXAMPLES)
        for name, (question, *_rest) in EXAMPLES.items():
            print(f"{name:<{width}}  {question}")
        return 0
    if args.example not in EXAMPLES:
        parser.error(f"unknown example {args.example!r}; run without arguments to list them")

    question, method, params, key = EXAMPLES[args.example]
    print(f"{question}\n  dp.{method}({', '.join(f'{k}={v!r}' for k, v in params.items())})\n")
    answer = DataPorium().call(method, **params)

    frame = None if args.json else rows(answer, key)
    if frame is None:
        print(json.dumps(answer, indent=2, default=str)[:20000])
    else:
        print(frame.head(args.rows).to_string(max_colwidth=40))
        print(f"\n{len(frame)} rows")
    if args.csv:
        if frame is None:
            frame = rows(answer, key)
        if frame is None:
            print("This answer has no table to save.", file=sys.stderr)
            return 1
        frame.to_csv(args.csv, index=False)
        print(f"Saved {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
