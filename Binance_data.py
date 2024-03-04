import asyncio
import websockets
import pandas as pd
import pyodbc
import json

class OrderBookSaver:
    def __init__(self, symbol):
        self.symbol = symbol
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=(local);DATABASE=Binance_data;Trusted_Connection=yes;')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        table_exists_query = f"SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{self.symbol}_order_book'"
        table_exists = self.cursor.execute(table_exists_query).fetchone()

        if not table_exists:
            create_table_query = f"""
                CREATE TABLE {self.symbol}_order_book (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    bid_price FLOAT,
                    ask_price FLOAT
                )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()

    def save_to_database(self, bid_ask_pair):
        self.cursor.execute(f"INSERT INTO {self.symbol}_order_book (bid_price, ask_price) VALUES (?, ?)", bid_ask_pair)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

class TreeNode:
    def __init__(self, price, volume):
        self.price = price
        self.volume = volume
        self.left = None
        self.right = None

class OrderBookUpdater:
    def __init__(self, symbol, order_saver):
        self.symbol = symbol
        self.order_saver = order_saver
        self.highest_bid = None
        self.lowest_ask = None

    async def update(self, data):
        parsed_data = json.loads(data)
        print("Parsed data:", parsed_data)
        if "b" in parsed_data and "a" in parsed_data:
            if parsed_data["b"]:
                self.update_highest_bid(parsed_data["b"])
            if parsed_data["a"]:
                self.update_lowest_ask(parsed_data["a"])
            await self.save_to_database()

    def update_highest_bid(self, bids):
        valid_bids = [(float(order[0]), float(order[1])) for order in bids if float(order[1]) > 0]
        if valid_bids:
            self.highest_bid = max(valid_bids, key=lambda x: x[0])

    def update_lowest_ask(self, asks):
        valid_asks = [(float(order[0]), float(order[1])) for order in asks if float(order[1]) > 0]
        if valid_asks:
            self.lowest_ask = min(valid_asks, key=lambda x: x[0])

    async def save_to_database(self):
        bid_price = self.highest_bid[0] if self.highest_bid else None
        ask_price = self.lowest_ask[0] if self.lowest_ask else None
        print("Saving bid/ask prices:", bid_price, ask_price)
        bid_ask_pair = [bid_price, ask_price]
        self.order_saver.save_to_database(bid_ask_pair)

class OrderBookAnalyzer:
    def __init__(self):
        self.spread = []
        self.counter = 0
        self.midpoints = []

    async def analyze(self, data, updater):
        parsed_data = json.loads(data)
        if self.counter % 10 == 0:
            await self.calculate_spread(parsed_data)
        await self.calculate_midpoint(updater)
        self.counter += 1

    async def calculate_spread(self, parsed_data):
        if (len(parsed_data["b"]) >= 10 and float(parsed_data["b"][9][1]) > 0) and \
           (len(parsed_data["a"]) >= 10 and float(parsed_data["a"][9][1]) > 0):
            bid_price = float(parsed_data["b"][9][0])
            ask_price = float(parsed_data["a"][9][0])
            self.spread.append(ask_price - bid_price)
            print("Spread", self.spread)

    async def calculate_midpoint(self, updater):
        if self.counter % 10 == 0:
            bid_price = updater.highest_bid[0] if updater.highest_bid else 0.0
            ask_price = updater.lowest_ask[0] if updater.lowest_ask else 0.0
            midpoint = (bid_price + ask_price) / 2
            self.midpoints.append(midpoint)
            

async def start_order_book(symbol):
    Lower_case = symbol.lower()
    url = f"wss://stream.binance.com:9443/ws/{Lower_case}@depth@100ms"
    async with websockets.connect(url) as websocket:
        order_saver = OrderBookSaver(symbol)
        updater = OrderBookUpdater(symbol, order_saver)
        analyzer = OrderBookAnalyzer()
        while True:
            data = await websocket.recv()
            await updater.update(data)
            await analyzer.analyze(data, updater)

async def orderbooks(symbols):
    tasks = [start_order_book(symbol) for symbol in symbols]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    symbols = ["BTCUSDT"]
    asyncio.run(orderbooks(symbols))