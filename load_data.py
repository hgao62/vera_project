import pandas as pd
import sqlite3
from sqlalchemy import create_engine

ENGINE = create_engine(f"sqlite:///<path on your local drive>.db")

def save_df_to_db(df, table_name, if_exists="append", dtype=None, engine=MYSQL_ENGINE):
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
    df.to_sql(name = table_name, con = ENGINE, if_exists = if_exists, dtype = dtype)


    