import time, requests, asyncio
from telegram import Bot

# Replace with your Telegram bot token and channel ID
token_telegram_bot = "6602062815:AAH0CK-fNuL00ojz8_UX9zP5f66MQ013h94"
id_canal_telegram = -4023725807

tokens_names = [
    ["0x2170Ed0880ac9A755fd29B2688956BD959F933F8", "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"],
    ["0x2170Ed0880ac9A755fd29B2688956BD959F933F8", "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"]    #<----- Here is an example use
]  # Format: [ [100 BEST TOKENS], [100 NEW TOKENS] ]

last_tokens = [[], []]  # Record of tokens from the last 15 minutes, same format as tokens_names

# Replace with the desired threshold percentage for change
seuil_pourcentage = 10

max_requests_limit = 300  # Max requests per minute

# Set the candle period in minutes (15 minutes)
periode_bougies_minutes = 15

bot_telegram = Bot(token=token_telegram_bot)

async def start():
    await bot_telegram.send_message(chat_id=id_canal_telegram, text="Bot Started Working Made By div_yt on Discord")

async def notifier_telegram(message):
    await bot_telegram.send_message(chat_id=id_canal_telegram, text=message)

async def verify_pair_changes():
    # Check for price, volume, and market cap changes over 15 minutes candles
    requests_count = 0
    requests_start = time.time()
    url = "https://api.dexscreener.io/latest/dex/tokens/"  # Replace with the actual API endpoint
    for indx, name in enumerate(tokens_names):
        for token in name:

            if requests_start <= max_requests_limit:
                time_left = time.time() - requests_start
                if time_left >= 60:
                    requests_count = 0
                    requests_start = time.time()
                else:
                    loop.run_until_complete(asyncio.sleep(time_left))

            response = requests.get(url + str(token))
            requests_count += 1
            if response.status_code == 200:
                data = response.json()["pairs"][0]
                if last_tokens != [[], []]:
                    for last_token in last_tokens:
                        for last_tokn in last_token:
                            if last_tokn["baseToken"]["address"] == data["baseToken"]["address"]:
                                last_price = float(last_tokn["priceNative"])
                                new_price = float(data["priceNative"])

                                last_volume = float(last_tokn["volume"]["m5"])
                                new_volume = float(data["volume"]["m5"])

                                last_fdv = float(last_tokn["fdv"])
                                new_fdv = float(data["fdv"])

                                if abs((new_price - last_price) / last_price) * 100 >= seuil_pourcentage or \
                                        abs((new_volume - last_volume) / last_volume) * 100 >= seuil_pourcentage or \
                                        abs((new_fdv - last_fdv) / last_fdv) * 100 >= seuil_pourcentage:
                                    message = f"The Token {data['pairAddress']} has a change:\n" \
                                              f"Price Change (15min): {(new_price - last_price) / last_price * 100}%\n" \
                                              f"Volume Change (15min): {(new_volume - last_volume) / last_volume * 100}%\n" \
                                              f"Market Cap Change: {(new_fdv - last_fdv) / last_fdv * 100}%"
                                    print(message)
                                    await notifier_telegram(message)
                else:
                    last_tokens[indx].append(data)

# Run the program every 15 minutes
loop = asyncio.get_event_loop()
loop.run_until_complete(start())
while True:
    print("Doing Verifications")
    loop.run_until_complete(verify_pair_changes())
    # Wait for 15 minutes before the next execution
    loop.run_until_complete(asyncio.sleep(periode_bougies_minutes * 60))
