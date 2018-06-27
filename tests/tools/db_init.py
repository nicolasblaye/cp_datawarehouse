"""
Functions initializing cp_datawarehouse database
"""
import logging

import psycopg2

from cp_datawarehouse.config.base import config


CONFIG = config()
LOGGER = logging.getLogger(__name__)


def initialize_database(drop=False):
    """
    Create schema and tables in cp_datawarehouse database
    """

    conn = psycopg2.connect(CONFIG.get("postgres_url"))

    with open("cp_datawarehouse/db_models/create_table_users.sql", "r") as sql_file:
        sql_create_statement = sql_file.read()

    with conn:
        cur = conn.cursor()

        # Create master schema
        LOGGER.info('Creating schema cp_datawarehouse')
        cur.execute("CREATE SCHEMA IF NOT EXISTS cp_datawarehouse;")
        LOGGER.info('Schema cp_datawarehouse created successfully')

        # Create table 'users'
        LOGGER.info('Creating table cp_datawarehouse.users')
        if drop:
            cur.execute("DROP TABLE IF EXISTS cp_datawarehouse.users")
        cur.execute(sql_create_statement)
        LOGGER.info('Table cp_datawarehouse.users created successfully')
