import pytest
import os
from configparser import ConfigParser
from web3 import Web3
from defy.Utilities import Utilities


@pytest.fixture
def myWeb3():
    config = ConfigParser(os.environ)
    config.read("config.ini")

    return Web3(Web3.HTTPProvider(config["DEFAULT"]["network_provider"]))


def test_formatBalance(myWeb3):
    assert Utilities.formatBalance(myWeb3, 10 ** 18) == 1


def test_GetTotal():
    tabulateBalances = [
        [
            {
                "pairSymbol": "TEST1/TEST2",
                "deposit": 1,
                "reward": 1,
                "bal": 1,
                "balInDollar": 6,
            }
        ],
        [
            {"symbol": "TEST", "price": 4, "bal": 3, "balInDollar": 12},
            {"symbol": "TEST", "price": 2, "bal": 1, "balInDollar": 2},
        ],
    ]
    assert Utilities.getTotal(tabulateBalances) == 20


def test_displayTotal(capsys):
    Utilities.displayTotal(11.111111)
    captured = capsys.readouterr()
    assert captured.out == "Total Balance: $11.11\n"
