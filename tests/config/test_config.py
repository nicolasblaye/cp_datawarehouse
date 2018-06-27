"""
test_config
"""

from cp_datawarehouse.config.base import config


def test_config_returns_configuration():
    """
    Test if config values are set
    """

    value = config()

    assert value["initialized"] is True
    assert value["postgres_url"]
