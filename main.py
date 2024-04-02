import aiohttp
import asyncio
import json
import sys
import logging
import names
from aiofile import AIOFile, LineReader
from aiopath import AsyncPath
import websockets
from websockets.exceptions import ConnectionClosedOK
from websockets import WebSocketServerProtocol
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

API_URL = "https://api.privatbank.ua/p24api/exchange_rates?date=01.12.2014"


async def fetch_currency(session, date):
    async with session.get(API_URL) as response:
        return await response.json()


async def get_exchange_rates(dates, currencies):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_currency(session, date) for date in dates]
        results = await asyncio.gather(*tasks)
        formatted_results = []
        for result in results:
            if "exchangeRate" in result:
                formatted_result = {}
                for currency in result["exchangeRate"]:
                    if currency["currency"] in currencies:
                        formatted_result[currency["currency"]] = {
                            "sale": currency["saleRateNB"],
                            "purchase": currency["purchaseRateNB"]
                        }
                formatted_results.append(formatted_result)
        return formatted_results


async def format_results(results):
    formatted_results = []
    for result in results:
        if "exchangeRate" in result:
            formatted_result = {}
            for currency in result["exchangeRate"]:
                if currency["currency"] in ["USD", "EUR"]:
                    formatted_result[currency["currency"]] = {
                        "sale": currency["saleRateNB"],
                        "purchase": currency["purchaseRateNB"]
                    }
            formatted_results.append(formatted_result)
    return formatted_results


async def main(num_days, currencies):
    dates = [(datetime.now() - timedelta(days=i)).strftime("%d.%m.%Y") for i in range(1, num_days + 1)]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(get_exchange_rates(dates, currencies))
    formatted_results = format_results(results)
    print(json.dumps(formatted_results, indent=2))


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.startswith("exchange"):
                try:
                    num_days = int(message.split(" ")[1])
                    currencies = ["USD", "EUR"]
                    results = await get_exchange_rates([datetime.now().strftime("%d.%m.%Y")], currencies)
                    formatted_results = format_results(results)
                    await ws.send(json.dumps(formatted_results, indent=2))
                    
                    # Logging to file
                    async with AIOFile("exchange_logs.txt", mode="a") as afp:
                        await afp.write(f"{ws.name}: {message}\n")
                    
                except (IndexError, ValueError):
                    await ws.send("Invalid command. Usage: exchange <num_days>")
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main_chat():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever
        await main(num_days, currencies)


if __name__ == '__main__':
    try:
        num_days = int(sys.argv[1])
        currencies = sys.argv[2].split(",")
    except (IndexError, ValueError):
        print("Usage: python main.py <num_days> <currencies>")
        sys.exit(1)

    if num_days > 10 or num_days <= 0:
        print("Error: Number of days should be between 1 and 10")
        sys.exit(1)

    asyncio.run(main_chat())
