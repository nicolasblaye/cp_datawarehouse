"""
config
"""
import os

def config():
    """
    Returns the configuration from environment variables

    :return: The configuration dictionnary
    :rtype: dict
    :example: config() returns { "initialized": True }
    """

    config_dict = {
        "initialized": True,
        "postgres_url": os.environ.get('POSTGRES_URL', 'postgresql://postgres:@localhost:65432/cp_datawarehouse'),
    }

    return config_dict
