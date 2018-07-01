"""
test_load
"""
# pylint: disable=too-few-public-methods,line-too-long,invalid-name

import psycopg2

from cp_datawarehouse.config.base import config
from cp_datawarehouse.etl.load import (
    insert_users_list,
    insert_rides_list)
from tests.tools.db_init import initialize_database
import pandas as pd

CONFIG = config()


def test_insert_users_list():
    """
    Test INSERT of a dummy CSV into users database table
    """

    initialize_database(drop=True)

    users_list = [
        ('user_id', 'loyalty_status', 'loyalty_status_txt'),
        (1, 0, 'red'),
        (3, 3, 'platinum'),
        (4, 1, 'silver'),
        (2, 2, 'gold'),
    ]

    insert_users_list(users_list)

    conn = psycopg2.connect(CONFIG["postgres_url"])

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM cp_datawarehouse.users")
        result = cur.fetchall()

    # Skip CSV header first line
    assert result.sort() == users_list[1:].sort()


def test_insert_rides_list():
    """
    Test INSERT of a dummy CSV into rides database table
    """

    initialize_database(drop=True)

    rides_list = [
        ('ride_id', 'user_id', 'from_zipcode', 'to_zipcode', 'state', 'quote_date',
         'completed_date', 'price_nominal', 'loyalty_points_earned'),
        (1, 1, '75010', '75009', 'completed', '2018-04-09 10:31:43.52', '2018-04-09 10:31:43.52', 10, 1),
        (2, 1, '40000', '75001', 'completed', '2018-04-09 10:31:43.52', '2018-04-09 10:31:43.52', 10, 1),
        (3, 1, '34000', '30100', 'completed', '2018-04-09 10:31:43.52', '2018-04-09 10:31:43.52', 10, 1),
    ]

    insert_rides_list(rides_list)

    conn = psycopg2.connect(CONFIG["postgres_url"])

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM cp_datawarehouse.rides")
        result = cur.fetchall()

    # Skip CSV header first line
    assert result.sort() == rides_list[1:].sort()

def test_insert_rides_dataframe():
    """
        Test INSERT of a dataframe into rides database table
        """

    initialize_database(drop=True)

    rides_list = [
        ('ride_id', 'user_id', 'from_zipcode', 'to_zipcode', 'state', 'quote_date',
         'completed_date', 'price_nominal', 'loyalty_points_earned'),
        (1, 1, '75010', '75009', 'completed', '2018-04-09 10:31:43.52', '2018-04-09 10:31:43.52', 10, 1),
        (2, 1, '40000', '75001', 'completed', '2018-04-09 10:31:43.52', '2018-04-09 10:31:43.52', 10, 1),
        (3, 1, '34000', '30100', 'completed', '2018-04-09 10:31:43.52', '2018-04-09 10:31:43.52', 10, 1),
    ]

    string = "\n".join(["".join(i) for i in rides_list])

    insert_rides_list(pd.read_csv(string))

    conn = psycopg2.connect(CONFIG["postgres_url"])

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM cp_datawarehouse.rides")
        result = cur.fetchall()

    # Skip CSV header first line
    assert result.sort() == rides_list[1:].sort()
