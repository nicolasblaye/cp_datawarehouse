"""
Transform module provides functions to transform and clean data before further import into cp_datawarehouse tables
"""

import csv
import logging
import re
import io

import pandas as pd

LOGGER = logging.getLogger(__name__)


def clean_users_csv(users_csv, delimiter=','):
    """
    Clean user CSV file values replacing misspelled 'platinium' values into 'platinum'.
    :param list users_csv: the CSV object (path or StringIO) WHICH INCLUDES HEADER ROW
    :return: the cleaned csv as a Pandas dataframe
    """

    users_df = pd.read_csv(users_csv, delimiter=delimiter)
    LOGGER.info(
        "Successfully read {shape} CSV (row(s), column(s)) into dataframe".format(
            shape=users_df.shape
        ))

    users_df['loyalty_status_txt'].replace('platinium', 'platinum', inplace=True)

    return users_df


def clean_by_ile_de_france(users_csv, delimiter=","):
    zip_code_list = [75, 77, 78, 91, 92, 93, 94, 95]
    return clean_by_zip_code(users_csv, zip_code_list, delimiter)


def clean_by_zip_code(rides_csv, zip_code_list, delimiter=","):
    """
        Filter user CSV file by a list of zipcode.
        :param list rides_csv: the CSV object (path or StringIO) WHICH INCLUDES HEADER ROW
        :param list zip_code: the list of zip_code where the ride must be
        :return: the cleaned csv as a Pandas dataframe
        """
    rides_df = pd.read_csv(rides_csv, delimiter=delimiter)
    return rides_df[rides_df.apply(lambda x: is_in_zip_list(x, zip_code_list), axis=1)]


def is_in_zip_list(x, zipcode_list):
    from_zipcode = clean_digit_string(x['from_zipcode'])
    to_zipcode = clean_digit_string(x['to_zipcode'])

    from_condition = from_zipcode.isdigit() and int(int(from_zipcode)/1000) in zipcode_list
    to_condition = to_zipcode.isdigit() and int(int(to_zipcode)/1000) in zipcode_list

    return from_condition or to_condition

def clean_digit_string(x):
    x = str(x)
    if x.isdigit():
        return x
    else:
        x = re.sub("[^0-9]", "", x)
        x = x.strip()
        return x
