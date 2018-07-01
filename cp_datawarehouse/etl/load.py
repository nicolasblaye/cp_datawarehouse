"""
Load module provides functions to load data into various cp_datawarehouse tables
"""

import logging

import psycopg2
import psycopg2.extras

from cp_datawarehouse.config.base import config

LOGGER = logging.getLogger(__name__)
CONFIG = config()


def insert_users_list(users_list):
    """
    Insert into users database table the values given as CSV with header.
    :param list users_list: the CSV list INCLUDING HEADER ROW which is skipped during insertion
    """

    conn = psycopg2.connect(CONFIG["postgres_url"])

    with conn:
        cur = conn.cursor()

        LOGGER.info("Inserting {nb_rows} CSV row(s) in cp_datawarehouse.users table...".format(
            nb_rows=len(users_list) - 1  # Skip the first header row
        ))
        psycopg2.extras.execute_values(
            cur,
            "INSERT INTO cp_datawarehouse.users VALUES %s",
            # Skip the first header row
            users_list[1:]
        )
        LOGGER.info(cur.statusmessage)
        LOGGER.info(
            "Successfully inserted {nb_rows} CSV row(s) in cp_datawarehouse.users table".format(
                nb_rows=cur.rowcount
            ))


def insert_rides_dataframe(rides_df):
    insert_rides_list(rides_df.where((rides_df.notnull(rides_df)), None).values.tolist())


def insert_rides_list(rides_list):
    """
        Insert into rides database table the values given as CSV without headers.
        :param list rides_list: the CSV list without headers row
    """
    conn = psycopg2.connect(CONFIG["postgres_url"])

    with conn:
        cur = conn.cursor()

        LOGGER.info("Inserting {nb_rows} CSV row(s) in cp_datawarehouse.rides table...".format(
            nb_rows=len(rides_list) - 1  # Skip the first header row
        ))
        psycopg2.extras.execute_values(
            cur,
            "INSERT INTO cp_datawarehouse.rides VALUES %s",
            # Skip the first header row
            rides_list[1:]
        )
        LOGGER.info(cur.statusmessage)
        LOGGER.info(
            "Successfully inserted {nb_rows} CSV row(s) in cp_datawarehouse.rides table".format(
                nb_rows=cur.rowcount
            ))
