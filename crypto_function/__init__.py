import os
import json
import logging
import datetime
import requests
import mysql.connector
import azure.functions as func

logging.info("Importing libraries complete.")


def main(myTimer: func.TimerRequest) -> None:
    logging.info("Azure Function started.")

    # Get execution time
    # execution_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    logging.info(f"API key: {os.getenv("COINMARKETCAP_API_KEY")}")

    # Fetch Bitcoin price from CoinMarketCap API
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {"symbol": "BTC", "convert": "USD"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY"),
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    if "data" in data and "BTC" in data["data"]:
        logging.info("BTC data retrieved.")
        price = data["data"]["BTC"]["quote"]["USD"]["price"]
        last_updated_iso = data["data"]["BTC"]["quote"]["USD"][
            "last_updated"
        ]  # '2025-03-20T19:09:00.000Z'
        symbol = "BTC"
        hawkid = "colbert"

        logging.info(f"BTC Price: ${price:.2f} at {last_updated_iso}")

        # Convert ISO 8601 format to MySQL TIMESTAMP format
        last_updated = datetime.datetime.strptime(
            last_updated_iso, "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        # Connect to Azure MySQL Database
        try:
            conn = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DATABASE"),
                port=os.getenv("MYSQL_PORT"),
            )
            logging.info("database: %s", os.getenv("MYSQL_DATABASE"))
            logging.info("Connected to MySQL database.")

            cursor = conn.cursor()

            query = """
            INSERT INTO crypto_prices (readTime, hawkid, cryptocurrency, price, last_updated)
            VALUES (CURRENT_TIMESTAMP(), %s, %s, %s, %s)
            """
            cursor.execute(query, (hawkid, symbol, price, last_updated))

            conn.commit()

            logging.info("Data successfully inserted into MySQL.")

        except mysql.connector.Error as err:
            logging.error(f"Database error: {err}")

        finally:
            cursor.close()
            conn.close()

    else:
        logging.error("Failed to retrieve BTC price data.")
