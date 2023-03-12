"""
TASK : Stadium Goods case test
AUTHOR: Bruna Lemberck
VERSION : 1.0
DESCRIPTION:
    This code defines functions to retrieve exchange rate of coutries currencies to euro and shoes data from two different APIs. 
    It also includes a function to merge the data and convert shoe prices to EUR. 
    Finally, it exports the merged data to CSV files and logs data retrieval and 
    processing status to a log file. The main function retrieves exchange rate data 
    and exports it to "result1.csv". It then retrieves shoes data, merges it with exchange
    rate data, converts shoe prices to EUR, and exports the merged data to "result2.csv". 
    It also create logs of the data retrieval and processing status to the file "logs".
    The log file and the two csv file results are saved in the 'output' folder.
"""

# imports
import requests
import pandas as pd
import io
import logging

# Logging config
logging.basicConfig(
    filename='output/logs.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

# Define EBC API URL parameters
protocol = 'https://'
entrypoint = 'sdw-wsrest.ecb.europa.eu/service/'
resource = 'data'
flowRef = 'EXR'
key = 'D..EUR.SP00.A'

def get_exchange_rate_data(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Get exchange rate data from the EBC API and return as a pandas DataFrame.
    """
    url = f'{protocol}{entrypoint}{resource}/{flowRef}/{key}'
    params = {'startPeriod': start_date, 'endPeriod': end_date}
    headers = {'Accept': 'text/csv'}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        logging.info(f'Successfully retrieved data from {url}')
        df = pd.read_csv(io.StringIO(response.text))
        logging.info(f'data fetched from ECB API: {df.columns}')
        df = df[['TIME_PERIOD', 'OBS_VALUE', 'CURRENCY']]
        df.rename(columns={'TIME_PERIOD': 'time_period', 'OBS_VALUE': 'exr_eur', 'CURRENCY': 'currency'}, inplace=True)
        df = df[['time_period', 'currency', 'exr_eur']].sort_values('currency')
        logging.info(f'EBC data after processing: {df.columns}')
        
        return df

    else:
        logging.error(f'Request to {url} failed with status code {response.status_code}')
        logging.info('\n--------------------------------------------------------------------------')
        return pd.DataFrame()


def get_shoes_data() -> pd.DataFrame:
    """
    Get product data from a fake e-commerce API for shoes category and return as a pandas DataFrame.
    """
    url = 'https://api.escuelajs.co/api/v1/categories/4/products'
    response = requests.get(url)

    if response.status_code == 200:
        logging.info(f'Successfully retrieved data from {url}')
        data = response.json()
        df = pd.DataFrame(data)
        logging.info(f'data fetched from Fake Ecommerce API: {df.columns}')
        df = df[['title', 'price']]
        df['currency'] = 'USD'
        logging.info(f'Fake ecommerce data after processing: {df.columns}')
        
        return df

    else:
        logging.error(f'Request to {url} failed with status code {response.status_code}')
        logging.info('\n--------------------------------------------------------------------------')
        return pd.DataFrame()


def merge_exchange_rate_and_shoes_data(exchange_rate_df: pd.DataFrame, shoes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge exchange rate and shoes data, convert price to EUR and return as a pandas DataFrame.
    """
    try:
        df = shoes_df.merge(exchange_rate_df, on='currency', how='left')
        logging.info(f'Joined data : {df.columns}')
        df['price_EUR'] = round(df['price'] / df['exr_eur'], 2)
        df.drop(['exr_eur', 'currency'], axis=1, inplace=True)
        df.rename(columns={'title': 'product_name', 'price': 'price_US', 'time_period': 'date_exr'}, inplace=True)
        df = df[['product_name', 'price_US', 'price_EUR', 'date_exr']]
        logging.info(f'Joined data after processing: {df.columns}')
        logging.info(f'Joined data shape after processing: {df.shape}')
        
    except Exception as e:
        logging.error(f'An error occurred during data merge: {str(e)}')
        df = pd.DataFrame()
    
    return df


def export_to_file(df: pd.DataFrame, file_name: str):
    """
    Export a pandas DataFrame to a CSV file.
    """
    try:
        df.to_csv('output/'+ file_name, index=False)

    except Exception as e:
        logging.error(f'An error occurred during csv file writing: {str(e)}')
        df = pd.DataFrame()


if __name__ == '__main__':
  
    # Set date range for exchange rate data
    start_date = '2023-02-09'
    end_date = '2023-02-10'

    # Get exchange rate data and export to result1.csv
    exchange_rate_df = get_exchange_rate_data(start_date, end_date)
    export_to_file(exchange_rate_df, 'result1.csv')

    # Get shoes data and merge with exchange rate data to get product prices in EUR
    shoes_df = get_shoes_data()
    shoes_eur_df = merge_exchange_rate_and_shoes_data(exchange_rate_df, shoes_df)

    # Export to result2.csv
    export_to_file(shoes_eur_df, 'result2.csv')

    # Results to logs
    logging.info(f'\nEBC Exchange Rate data fetch sample: \n{exchange_rate_df.head(6)}')
    logging.info(f'\nFinal result data sample: \n{shoes_eur_df.head(6)}')
    logging.info('\n--------------------------------------------------------------------------')
