"""
test_load
"""
# pylint: disable=too-few-public-methods,line-too-long,invalid-name

import psycopg2

from cp_datawarehouse.config.base import config
from cp_datawarehouse.etl.load import (
    insert_users_list,
)
from tests.tools.db_init import initialize_database


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
