# Binance_data
websockets,MS SQL,async,spread


Class OrderBookTree-The class holds all the global variables to be used in the functions . async def start(self) – Calls the websockets and while it has connection call the function each_order_update_format

async def each_order_update_format(self, data) – Parses the data received. Saves it into format [Bid,Ask]. Checks if there is a 10th value and if its volume is greater than 0 and calculates the spread. Checks if the Best_One_second_Bid is LOWER than the new order book bid and if so it takes the new value. The opposite is done for the ASK. If this is the first encounter it sets the Best_One_second_Bid and Best_One_second_Ask it takes the first order book values. Calculates the midpoint (Best Ask - Best Bid)/2). This one second value is stored in Each_second_midpoint series. async def. Then it removes the first element of the array and adds, after 1 iteration a new one . That way the moving average is shifting by 1 and it maintains a size of 60. I believe this is O(1) due to constant series size.

async def spread_bid_ask(self, parsed_data): Calculates the spread between the BID and ASK.

async def save_to_database(self, bid_ask_pair): Saves the data pair into a database. If one doesn’t exist it will create on the level of the project FOR EACH STOCK, DERIVATIVE, FUTURE any ( SYMBOL) . def close_connection(self): Closes the connection to the database. async def orderbooks(symbols): Initializes the symbols taken. One or many.
