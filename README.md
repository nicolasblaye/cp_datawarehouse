# Overview

__datawarehouse__ is a Python project to create a PostgreSQL database `cp_datawarehouse` and import  _Chauffeur Privé_ data inside.

The data sources for each table are located inside the `raw_data/` directory as CSV files.


# _Chauffeur Privé_ Data Description

## Users Table
| column | definition |
| --- | ------- |
| `user_id` | *unique user id, primary key* |
| `loyalty_status` | *user loyalty status stored as integer: 0 = red, 1 = silver, 2 = gold, 3 = platinum* |
| `loyalty_status_txt` | *user loyalty status stored as text: red, silver, gold, platinum* |


## Rides Table
| column | definition |
| --- | ------- |
| `ride_id` | *unique ride id, primary key* |
| `user_id` | *user id* |
| `from_zipcode` | *zip code of the ride start location* |
| `to_zipcode` | *zip code of the ride end location* |
| `state` | *state of the ride: completed, not_completed: whether the ride was completed or not (for whatever possible reason)* |
| `quote_date` | *local date when the user sees the price of a ride in his app before ordering it* |
| `completed_date` | *local date when the ride is actually completed successfully* |
| `price_nominal` | *price of the ride* |
| `loyalty_points_earned` | *loyalty points awarded by the ride if elligible (=payed with real money, without discount or loyalty points). Only completed rides are eligibles.* |


# Setup

Go to the project top directory:
```bash
$ cd datawarehouse/
```

## Install PostgreSQL Docker Container

[Install `docker-compose`](https://docs.docker.com/compose/install)


Create and start the docker container named `postgres-dw` with `PostgreSQL`:
```bash
$ docker-compose up -d postgres-dw
```

Check if the container is up:
```bash
$ docker-compose ps

           Name                          Command              State            Ports          
---------------------------------------------------------------------------------------------
datawarehouse_postgres-dw_1   docker-entrypoint.sh postgres   Up      0.0.0.0:65432->5432/tcp
```

## Run tests

A docker container named `python-test` has been set up with Python Pandas, which can connect to the `postgres-dw` container above and run unit tests with [pytest](https://docs.pytest.org/en/latest/).

Run Python tests (keep the `--build` option to force rebuild if you modify the code and test it again):
```bash
$ docker-compose up --build  python-test
```

All tests should pass successfully:
```bash
Building python-test
Step 1/1 : FROM python:3.6.3-onbuild
...
...
python-test_1  | ============================= test session starts ==============================
python-test_1  | platform linux -- Python 3.6.3, pytest-3.6.1, py-1.5.3, pluggy-0.6.0
python-test_1  | rootdir: /usr/src/app, inifile:
python-test_1  | collected 3 items
python-test_1  | 
python-test_1  | tests/config/test_config.py .                                            [ 33%]
python-test_1  | tests/etl/test_load.py .                                                 [ 66%]
python-test_1  | tests/etl/test_transform.py .                                            [100%]
python-test_1  | 
python-test_1  | =========================== 3 passed in 0.39 seconds ===========================
datawarehouse_python-test_1 exited with code 0
```


## (Clean up all resources)
Once you are done with the technical test, you can remove all docker containers with:
```bash
$ docker-compose down
```


# Exercises

## Data transform and load

1. Explore all files in the `datawarehouse/` project top directory and try to understand them.
2. Based on `raw_data/rides.csv` input values, write a Python function in `datawarehouse/etl/transform.py` to clean rides by keeping only the rides in the **_Île-de-France_** region.
3. Write a Python function to load data from a Pandas dataframe into a `cp_datawarehouse.rides` PostgreSQL table.
4. Write tests for every function and run them with `pytest` to make sure they pass successfully.


## Python Pandas

From the `raw_data/*.csv` CSV files, answer the following questions using the Python Pandas library:
1. Write a function which returns a dataframe listing all the users, with the following columns:
* user_id
* loyalty_status
* loyalty_status_txt
* daily_date: date of ride day
* nb_rides: number of completed rides made by the user for the given day
* total_price: total ride price spent by the user for the given day
2. Write a function which returns a dataframe listing the average basket per day. The average basket is the average completed ride price for a given period of time.
3. Write a function which returns a dataframe listing the 5 days with the lowest number of completed rides, ordered chronologically.
4. Create a chart plotting the number of completed rides per week for each loyalty status.


## SQL

Write the equivalent SQL queries answering the first three previous Pandas questions (ignore the chart question).


## How to answer

1. In the `datawarehouse/` project directory, feel free to create or update all files/directories that you might think of.
2. Send us back your updated project as a zip/tar.gz archive or push it to [GitHub](https://github.com/), [Bitbucket](https://bitbucket.org/), etc. and send us the repository address.
