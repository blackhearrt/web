import aiohttp
import asyncio
import json
import sys
from datetime import datetime, timedelta
API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="


async def fetch_currency(session, date):
    async with session.get(API_URL + date) as response:
        return await response.json()


async def get_exchange_rates(dates):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_currency(session, date) for date in dates]
        return await asyncio.gather(*tasks)


def format_results(results):
    formatted_results = []
    for result in results:
        formatted_result = {}
        for currency in result["exchangeRate"]:
            if currency["currency"] in ["USD", "EUR"]:
                formatted_result[currency["currency"]] = {
                    "sale": currency["saleRateNB"],
                    "purchase": currency["purchaseRateNB"]
                }
        formatted_results.append(formatted_result)
    return formatted_results


def main(num_days):
    dates = [(datetime.now() - timedelta(days=i)).strftime("%d.%m.%Y") for i in range(1, num_days + 1)]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(get_exchange_rates(dates))
    formatted_results = format_results(results)
    print(json.dumps(formatted_results, indent=2))


if __name__ == "__main__":
    try:
        num_days = int(sys.argv[1])
    except (IndexError, ValueError):
        print("Usage: python main.py <num_days>")
        sys.exit(1)
    
    if num_days > 10 or num_days <= 0:
        print("Error: Number of days should be between 1 and 10")
        sys.exit(1)

    main(num_days)
