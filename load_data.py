import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import logging

logger = logging.getLogger(__name__)

ENGINE = create_engine(f"mysql://Users/vera/Desktop/project_etl/vera_project/database/stock_db.db")
# MySQL connection parameters
MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'stockdata'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password123'

# MySQL connection URL
MYSQL_CONNECTION_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"

# Create engine for MySQL
ENGINE = create_engine(MYSQL_CONNECTION_URL)


def save_df_to_db(df, table_name, if_exists="append", dtype=None, engine=ENGINE):
    """Function to send a dataframe to SQL database.

    Args:
        df (pandas dataframe): DataFrame to be sent to the SQL database.
        table_name (str): Name of the table in the SQL database.
        if_exists (str, optional): Action to take if the table already exists in the SQL database.
                   Options: "fail", "replace", "append" (default: "append").
        dtype (_type_, optional): Dictionary of column names and data types to be used when creating the table (default: None).
        engine (default to MYSQL_ENGINE): db engine type, in our project, this could be sqlite or mysql

    Returns:
        None. This function logs a note in the log file to confirm that data has been sent to the SQL database.
    """
    try:
        logger.info(f'Loading {table_name} into database.')
        df.to_sql(name = table_name, con = engine, if_exists = if_exists, dtype = dtype) 
    except Exception as exception:
        logger.exception(f"inert into {table_name} failed due to :{repr(exception)}.")