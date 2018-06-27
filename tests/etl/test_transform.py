"""
test_load
"""
# pylint: disable=too-few-public-methods,line-too-long,invalid-name

import io

from pandas import DataFrame
from pandas.testing import assert_frame_equal

from cp_datawarehouse.etl.transform import (
    clean_users_csv, clean_digit_string,
    clean_by_zip_code, clean_by_ile_de_france)


def test_clean_users_csv():
    """
    Test the cleaning of users CSV data:
    * should replace misspelled "platinium" values with "platinum"
    """

    users_csv = io.StringIO('user_id,loyalty_status,loyalty_status_txt\n1,0,red\n2,1,silver\n3,2,gold\n4,3,platinium\n5,3,platinum')

    clean_users_df = clean_users_csv(users_csv)

    assert_frame_equal(
        clean_users_df.sort_index(axis=1),
        DataFrame({
            'user_id' : [1, 2, 3, 4, 5],
            'loyalty_status' : [0, 1, 2, 3, 3],
            'loyalty_status_txt' : ['red', 'silver', 'gold', 'platinum', 'platinum'],
        }).sort_index(axis=1),
        check_names=True
    )

def test_clean_digit():
    digit = "75001"
    cedex_digit = "CEDEX 92300"
    char = "Paris"

    assert(clean_digit_string(digit) == "75001")
    assert(clean_digit_string(cedex_digit) == "92300")
    assert(clean_digit_string(char) == "")

def test_clean_by_zip_code():
    rides_csv = io.StringIO(
        'ride_id,user_id,from_zipcode,to_zipcode,state,quote_date,completed_date,price_nominal,loyalty_points_earned\n'
        + '1,1,75010,75009,completed,today,today,10,1\n'
        + '2,1,40000,75001,completed,today,today,10,1\n'
        + '3,1,34000,30100,completed,today,today,10,1\n'
    )

    clean_rides = clean_by_zip_code(rides_csv, [75])

    assert_frame_equal(
        clean_rides.sort_index(axis=1),
        DataFrame({
            'ride_id': [1,2],
            'user_id': [1,1],
            'from_zipcode': [75010, 40000],
            'to_zipcode': [75009, 75001],
            'state': ['completed', 'completed'],
            'quote_date': ['today', 'today'],
            'completed_date': ['today', 'today'],
            'price_nominal': [10, 10],
            'loyalty_points_earned': [1, 1],
        }).sort_index(axis=1),
        check_names=True
    )

def test_clean_idf():
    rides_csv = io.StringIO(
        'ride_id,user_id,from_zipcode,to_zipcode,state,quote_date,completed_date,price_nominal,loyalty_points_earned\n'
        + '1,1,75010,75009,completed,today,today,10,1\n'
        + '2,1,40000,75001,completed,today,today,10,1\n'
        + '4,1,CEDEX 92000,95342,completed,today,today,10,1\n'
        + '5,1,mad,77230,completed,today,today,10,1\n'
        + '3,1,34000,30100,completed,today,today,10,1\n'
    )

    clean_rides = clean_by_ile_de_france(rides_csv)

    clean_rides_results = DataFrame(
        {'ride_id': [1, 2, 4, 5], 'user_id': [1, 1, 1, 1], 'from_zipcode': ['75010', '40000', 'CEDEX 92000', 'mad'],
         'to_zipcode': [75009, 75001, 95342, 77230], 'state': ['completed', 'completed', 'completed', 'completed'],
         'quote_date': ['today', 'today', 'today', 'today'], 'completed_date': ['today', 'today', 'today', 'today'],
         'price_nominal': [10, 10, 10, 10], 'loyalty_points_earned': [1, 1, 1, 1], })
    assert_frame_equal(
        clean_rides.sort_index(axis=1),
        clean_rides_results.sort_index(axis=1),
        check_names=True
    )
