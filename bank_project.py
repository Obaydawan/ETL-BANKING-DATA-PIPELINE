# Code for ETL operations on Largest Banks data
# Importing the required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime

#LOG FUNCTION
def log_progress(message):
   
    timestamp_format = "%Y-%m-%d-%H:%M:%S"
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open("code_log.txt", "a") as f:
        f.write(f"{timestamp} : {message}\n")

#EXTRACT FUNCTION
def extract(url, table_attribs):
    page = requests.get(url).text
    data = BeautifulSoup(page, "html.parser")
    rows_data = []

    # To find the table containing market capitalization data
    tables = data.find_all("tbody")
    rows = tables[0].find_all("tr")

    for row in rows:
        # Skip header rows
        if row.find_all("th"):
            continue
        col = row.find_all("td")
        if len(col) > 2:
            a_tags = col[1].find_all("a")
            bank_name = a_tags[-1].get_text(strip=True) if a_tags else ""
            mc_val = col[2].get_text(strip=True).replace(",", "")
            if bank_name and mc_val:
                try:
                    data_dict = {
                        table_attribs[0]: bank_name,
                        table_attribs[1]: float(mc_val),
                    }
                    rows_data.append(data_dict)
                except Exception:
                    pass

    df = pd.DataFrame(rows_data, columns=table_attribs)
    # Get only top 10 banks
    df = df.head(10)
    return df

#TRANSFORM FUNCTION
def transform(df, csv_path):
     exchange_rates = pd.read_csv(csv_path)

    # Convert exchange rates to dictionary
    rates = exchange_rates.set_index("Currency").to_dict()["Rate"]

    # Ensure MC_USD_Billion is numeric
    df["MC_USD_Billion"] = pd.to_numeric(df["MC_USD_Billion"], errors="coerce")
    # Add new columns with converted values
    df["MC_GBP_Billion"] = round(df["MC_USD_Billion"] * rates["GBP"], 2)
    df["MC_EUR_Billion"] = round(df["MC_USD_Billion"] * rates["EUR"], 2)
    df["MC_INR_Billion"] = round(df["MC_USD_Billion"] * rates["INR"], 2)

    return df

#LOAD FUNCTION
def load_to_csv(df, output_path): 
    df.to_csv(output_path, index=False)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists="replace", index=False)

def run_query(query_statement, sql_connection):
    print(f"Query: {query_statement}")
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)

# Define required entities
url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
table_attribs = ["Name", "MC_USD_Billion"]
exchange_rate_csv = "exchange_rate.csv"
output_csv_path = "Largest_banks_data.csv"
db_name = "Banks.db"
table_name = "Largest_banks"
log_file = "code_log.txt"

# Initiate logging
log_progress("Preliminaries complete. Initiating ETL process")

# Call extract function
df = extract(url, table_attribs)
log_progress("Data extraction complete. Initiating Transformation process")

# Call transform function
df = transform(df, exchange_rate_csv)
log_progress("Data transformation complete. Initiating Loading process")

# Call load_to_csv function
load_to_csv(df, output_csv_path)
log_progress("Data saved to CSV file")

# Initiate SQLite3 connection
sql_connection = sqlite3.connect(db_name)
log_progress("SQL Connection initiated")

# Call load_to_db function
load_to_db(df, sql_connection, table_name)
log_progress("Data loaded to Database as a table, Executing queries")

# Call run_query function
query_statement = f"SELECT * FROM {table_name}"
run_query(query_statement, sql_connection)

query_statement = f"SELECT AVG(MC_GBP_Billion) FROM {table_name}"
run_query(query_statement, sql_connection)

query_statement = f"SELECT Name from {table_name} LIMIT 5"
run_query(query_statement, sql_connection)

log_progress("Process Complete")

# Close SQLite3 connection
sql_connection.close()
log_progress("Server Connection closed")
