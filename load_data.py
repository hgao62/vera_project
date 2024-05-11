"""Loading data from dataframe to mysql database"""
import logging
from MySQLdb import DatabaseError
from sqlalchemy import create_engine


logger = logging.getLogger(__name__)

# ENGINE = create_engine("mysql+mysqlconnector://airflow_user:airflow_pass@localhost/airflow_db")
# MySQL connection parameters
MYSQL_HOST = "localhost"
MYSQL_DATABASE = "airflow_db"
MYSQL_USER = "airflow_user"
MYSQL_PASSWORD = "airflow_pass"

# MySQL connection URL
MYSQL_CONNECTION_URL_LOCAL = (
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@"
    f"{MYSQL_HOST}/{MYSQL_DATABASE}"
)
MYSQL_CONNECTION_URL_DOCKER = "mysql://airflow_user:airflow_pass@mysql:3306/airflow_db"
# Create engine for MySQL
ENGINE = create_engine(MYSQL_CONNECTION_URL_DOCKER)


def save_df_to_db(dataframe, table_name, if_exists="append", dtype=None, engine=ENGINE):
    """Function to send a dataframe to SQL database.

    Args:
        df (pandas dataframe): DataFrame to be sent to the SQL database.
        table_name (str): Name of the table in the SQL database.
        if_exists (str, optional): Action to take if the table already exists in the SQL database.
                   Options: "fail", "replace", "append" (default: "append").
        dtype (_type_, optional): Dictionary of column names and data types to be used
                    when creating the table (default: None).
        engine (default to MYSQL_ENGINE): db engine type, in our project,
                    this could be sqlite or mysql

    Returns:
        None. This function logs a note in the log file to confirm that data
        has been sent to the SQL database.
    """
    try:
        logger.info(f"Connection detail is: {engine}")
        logger.info("Loading %s into database.", table_name)
        dataframe.to_sql(name=table_name, con=engine, if_exists=if_exists, dtype=dtype)
    except DatabaseError as exception:
        logger.exception(
            "Database error occurred while loading %s: %s", table_name, repr(exception)
        )
    except IOError as exception:
        logger.exception(
            "I/O error occurred while loading %s: %s", table_name, repr(exception)
        )
