# US economic data API: GDP, inflation, jobs, interest rates, the yield curve, Fed decisions and trade

Get official US economic data with one request each: GDP, consumer prices and inflation by category, jobs and unemployment, weekly jobless claims, Treasury yields and the yield curve, Federal Reserve rate decisions, mortgage and corporate bond rates, trade by country and product, and gas prices. Every example is one request to the [DataPorium](https://dataporium.tech) REST API, shown in Python and curl.

## Quick start

```bash
pip install git+https://github.com/DataPorium/dataporium-python.git
export DATAPORIUM_API_KEY="YOUR_API_KEY"
```

```python
from dataporium import DataPorium, to_frame

dp = DataPorium()   # reads DATAPORIUM_API_KEY
answer = dp.economic_metrics(economic_metrics="GDP")
print(to_frame(answer).head())
```

Or run any example below from this repository:

```bash
git clone https://github.com/DataPorium/us-economic-data-api.git
cd us-economic-data-api
pip install -r requirements.txt
python examples.py           # list the examples
python examples.py gdp     # run one
python examples.py gdp --csv out.csv
```

## What you can get

| Question | Example | Endpoint |
|---|---|---|
| US GDP | [`gdp`](#gdp) | `GET /economic-metrics` |
| Unemployment rate | [`unemployment-rate`](#unemployment-rate) | `GET /economic-metrics` |
| Nonfarm payrolls | [`payrolls`](#payrolls) | `GET /economic-metrics` |
| Consumer price index (CPI) | [`cpi`](#cpi) | `GET /economic-metrics` |
| Recession probability | [`recession-probability`](#recession-probability) | `GET /economic-metrics` |
| Which prices are rising fastest: 25 categories, newest month | [`inflation-by-category`](#inflation-by-category) | `GET /inflation-categories` |
| Shelter and rent inflation since 2020 | [`rent-inflation-history`](#rent-inflation-history) | `GET /inflation-categories` |
| The next Federal Reserve meetings and the current target range | [`fed-next-meeting`](#fed-next-meeting) | `GET /fed-decisions` |
| Every Fed rate cut since 2019 | [`fed-cuts`](#fed-cuts) | `GET /fed-decisions` |
| The Treasury yield curve today, a month ago and a year ago | [`yield-curve`](#yield-curve) | `GET /treasury-yields/curve` |
| 2-year and 10-year Treasury yields, monthly since 2000 | [`treasury-yields`](#treasury-yields) | `GET /treasury-yields` |
| 30-year fixed mortgage rate | [`mortgage-rate`](#mortgage-rate) | `GET /economic-metrics` |
| High-grade corporate bond yields and their spread over Treasuries | [`corporate-bonds`](#corporate-bonds) | `GET /corporate-bond-yields` |
| Weekly unemployment claims, US | [`jobless-claims`](#jobless-claims) | `GET /layoffs/official/claims` |
| States ranked by unemployment, newest month | [`state-unemployment`](#state-unemployment) | `GET /local-jobs` |
| Official layoffs and discharges (JOLTS) | [`layoffs-rate`](#layoffs-rate) | `GET /layoffs/official/jolts` |
| Largest US trade deficits by country, last 12 months | [`trade-deficits`](#trade-deficits) | `GET /us-trade/summary` |
| Monthly trade with China since 2024 | [`trade-china`](#trade-china) | `GET /us-trade` |
| Release dates of consumer price index (CPI) reports | [`economic-calendar`](#economic-calendar) | `GET /market-calendar` |
| Gas prices in the states of the weekly survey, newest week | [`gas-prices`](#gas-prices) | `GET /gas-prices` |

## Headline indicators

<a id="gdp"></a>
### US GDP

```python
dp.economic_metrics(economic_metrics="GDP")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/economic-metrics?economic_metrics=GDP"
```

Newest first, as `{date, value}`. The same request gives every series below by name.

<a id="unemployment-rate"></a>
### Unemployment rate

```python
dp.economic_metrics(economic_metrics="unemployment_Rate")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/economic-metrics?economic_metrics=unemployment_Rate"
```

<a id="payrolls"></a>
### Nonfarm payrolls

```python
dp.economic_metrics(economic_metrics="total_Non_farm_Payroll")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/economic-metrics?economic_metrics=total_Non_farm_Payroll"
```

<a id="cpi"></a>
### Consumer price index (CPI)

```python
dp.economic_metrics(economic_metrics="CPI")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/economic-metrics?economic_metrics=CPI"
```

<a id="recession-probability"></a>
### Recession probability

```python
dp.economic_metrics(economic_metrics="smoothed_US_Recession_Probabilities")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/economic-metrics?economic_metrics=smoothed_US_Recession_Probabilities"
```

## Inflation

<a id="inflation-by-category"></a>
### Which prices are rising fastest: 25 categories, newest month

```python
dp.inflation_categories(latest=True, sort="yoy_pct", order="desc")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/inflation-categories?latest=true&sort=yoy_pct&order=desc"
```

Gasoline, electricity, rent, shelter, groceries, restaurants, used cars, car insurance, airline fares, medical care and more, with 12-month and 1-month changes.

<a id="rent-inflation-history"></a>
### Shelter and rent inflation since 2020

```python
dp.inflation_categories(category="shelter,rent", month_from="2020-01", sort="month", order="asc", limit=500)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/inflation-categories?category=shelter,rent&month_from=2020-01&sort=month&order=asc&limit=500"
```

## Interest rates

<a id="fed-next-meeting"></a>
### The next Federal Reserve meetings and the current target range

```python
dp.fed_decisions(status="upcoming", order="asc")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/fed-decisions?status=upcoming&order=asc"
```

The answer also has `current_target`, `next_meeting` and `last_decision`.

<a id="fed-cuts"></a>
### Every Fed rate cut since 2019

```python
dp.fed_decisions(decision="cut", date_from="2019-01-01", order="asc")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/fed-decisions?decision=cut&date_from=2019-01-01&order=asc"
```

<a id="yield-curve"></a>
### The Treasury yield curve today, a month ago and a year ago

```python
dp.treasury_yields_curve(compare="1m,1y")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/treasury-yields/curve?compare=1m,1y"
```

With the 10-year minus 2-year and 10-year minus 3-month spreads and whether the curve is inverted.

<a id="treasury-yields"></a>
### 2-year and 10-year Treasury yields, monthly since 2000

```python
dp.treasury_yields(maturity="2y,10y", date_from="2000-01-01", frequency="monthly", order="asc", limit=1000)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/treasury-yields?maturity=2y,10y&date_from=2000-01-01&frequency=monthly&order=asc&limit=1000"
```

12 maturities from 1 month to 30 years, daily from 1990.

<a id="mortgage-rate"></a>
### 30-year fixed mortgage rate

```python
dp.economic_metrics(economic_metrics="30Year_Fixed_Rate_Mortgage_Average")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/economic-metrics?economic_metrics=30Year_Fixed_Rate_Mortgage_Average"
```

<a id="corporate-bonds"></a>
### High-grade corporate bond yields and their spread over Treasuries

```python
dp.corporate_bond_yields(month_from="2020-01", order="asc")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/corporate-bond-yields?month_from=2020-01&order=asc"
```

## Jobs

<a id="jobless-claims"></a>
### Weekly unemployment claims, US

```python
dp.layoffs_official_claims(state="US", date_from="2026-01-01")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/layoffs/official/claims?state=US&date_from=2026-01-01"
```

Every state too: `state=CA,TX`.

<a id="state-unemployment"></a>
### States ranked by unemployment, newest month

```python
dp.local_jobs(area_type="state", latest=True, sort="unemployment_rate", order="desc", limit=60)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/local-jobs?area_type=state&latest=true&sort=unemployment_rate&order=desc&limit=60"
```

Also metro areas, counties and cities of 25,000 people or more.

<a id="layoffs-rate"></a>
### Official layoffs and discharges (JOLTS)

```python
dp.layoffs_official_jolts(area="US", latest=True)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/layoffs/official/jolts?area=US&latest=true"
```

## Trade and prices

<a id="trade-deficits"></a>
### Largest US trade deficits by country, last 12 months

```python
dp.us_trade_summary(dimension="country", period="last_12_months", sort="balance", order="asc", limit=10)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/us-trade/summary?dimension=country&period=last_12_months&sort=balance&order=asc&limit=10"
```

<a id="trade-china"></a>
### Monthly trade with China since 2024

```python
dp.us_trade(dimension="country", code="5700", month_from="2024-01", order="asc")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/us-trade?dimension=country&code=5700&month_from=2024-01&order=asc"
```

Country codes: 5700 China, 1220 Canada, 2010 Mexico. `dimension=product` gives product groups.

<a id="economic-calendar"></a>
### Release dates of consumer price index (CPI) reports

```python
dp.market_calendar(event_name="CPI YY")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/market-calendar?event_name=CPI%20YY"
```

Event names are written as in the calendar, for example `CPI YY` (CPI, change from a year earlier). Each row has the date, time, previous value and `country`.

<a id="gas-prices"></a>
### Gas prices in the states of the weekly survey, newest week

```python
dp.gas_prices(area_type="state", product="regular", latest=True, sort="price_usd", order="desc")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/gas-prices?area_type=state&product=regular&latest=true&sort=price_usd&order=desc"
```

## Answers

Every answer is JSON. Many are a list of rows; paged answers hold their rows under `rows` with `total`, `limit` and `offset`. `to_frame(answer)` in the Python library finds the rows and returns a pandas DataFrame. Each endpoint and all of its parameters are described in the [API documentation](https://dataporium.tech/api-docs), and `print(dp.describe("<method>"))` shows them in Python.

## Use it in Claude, ChatGPT or Cursor

The same data is in the [DataPorium MCP server](https://github.com/DataPorium/dataporium-mcp), so Claude, ChatGPT or Cursor can answer questions like "How have mortgage rates and the 10-year yield moved this year?" from the official numbers.

## Ready-made scripts

- [yield-curve-inversion-tracker](https://github.com/DataPorium/yield-curve-inversion-tracker): spreads, every inversion since 1990 and a chart
- [inflation-by-category](https://github.com/DataPorium/inflation-by-category): rank the categories and chart them
- [layoffs-tracker](https://github.com/DataPorium/layoffs-tracker): layoffs by company, state and industry

## Get an API key

Sign up at [dataporium.tech](https://dataporium.tech/pricing) and subscribe to the Premium plan; the key is in your account settings. It works for the REST API (600 requests per minute) and the MCP server. Send it in the `apikey` header, as above; a `?apikey=` query parameter also works, but a key in a URL can end up in logs. Keep the key out of code you commit or share.

## More

- Python library: [dataporium-python](https://github.com/DataPorium/dataporium-python)
- JavaScript and TypeScript library: [dataporium-js](https://github.com/DataPorium/dataporium-js)
- Examples in curl, R, Google Sheets and Excel: [financial-data-api](https://github.com/DataPorium/financial-data-api)
- AI assistants: [dataporium-mcp](https://github.com/DataPorium/dataporium-mcp)
- API documentation: <https://dataporium.tech/api-docs>

## License

The code in this repository is released under the [MIT License](LICENSE). Use of the API and its data is governed by the DataPorium [Terms of Use](https://dataporium.tech/terms-of-use). Data is for information only and is not investment advice.
