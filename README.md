# api-data-ingestion-transformation
Fetching data from two different APIs , transforming and joining them for bulding a Business report

## About the code

This is a Python script that retrieves exchange rate data from **[ECB API](https://sdw-wsrest.ecb.europa.eu/help/)** and product data from a **[Fake Ecommerce API](https://fakeapi.platzi.com/en/rest/introduction)**, transforms and merges the data and converts the products in shoe category prices from USD to EUR. The merged data is then exported to CSV files and the logs data retrieval and processing status are stored in a log file.

The script defines three functions:

- **get_exchange_rate_data()** retrieves exchange rate data from an ECB API, processes the data and returns it as a Pandas DataFrame.
- **get_shoes_data()** retrieves product data from a fake e-commerce API for the shoes category, processes the data and returns it as a Pandas DataFrame.
- **merge_exchange_rate_and_shoes_data()** merges the exchange rate and shoes data, converts the price to EUR and returns the merged data as a Pandas DataFrame.

The script also defines a function **export_to_file()** to export a Pandas DataFrame to a CSV file.

The main section of the script retrieves the exchange rate data, exports it to "result1.csv", retrieves the shoes data, merges it with the exchange rate data, converts shoe prices to EUR, and exports the merged data to "result2.csv". The script logs data retrieval and processing status to the file "logs". The log file and the two CSV file results are saved in the **'output' folder**.

## About the files
There are 5 files for this solution:

- **dev.ipynb** : Development notebook, used to create and test the logic.
- **main.py** : Refactored code, to be used in production, with logging information.
- **output/logs.log** : Logging file,  that allows developers to keep track of the behavior of the code and identify errors or potential issues, with timestamp of each step. In the end, a sample of each of the two results is shown.
- **output/result1.csv** : Stores the result of the data fetch from EBC API exchange rate (exr) for 'February 9-10, 2023', pulling data for all daily currencies against the Euro.
- **output/result2.csv** :  Stores the final result, that includes all of the products of shoes category from Fake Ecommerce API, their price in USD, and the newly calculated price in EUR for each exchange rate date pulled from the EBC API.
