import pytest
from defy.PriceFinder import PriceFinder
from defy.exchanges.Binance import Binance
import json
import responses
from configparser import ConfigParser
from tests.MockContext import *


@pytest.fixture
def myValidBinance(myPriceFinder):
    binance = Binance(myPriceFinder)
    binance.binanceApiKey = "TEST"
    binance.binanceApiSecret = "TEST"
    return binance


@pytest.fixture
def myInvalidBinance(myPriceFinder):
    binance = Binance(myPriceFinder)
    binance.binanceApiKey = None
    binance.binanceApiSecret = None
    return binance


def test_isUsable_with_credentials(myValidBinance):
    assert myValidBinance.isUsable()


def test_isUsable_without_credentials(myInvalidBinance):
    assert not myInvalidBinance.isUsable()


def test_getWallet(mocker, myValidBinance):
    with open("tests/mocks/binance_get_account.json", "r") as mock_definition:
        mock = json.load(mock_definition)

    mocker.patch("binance.client.Client.get_account", return_value=mock)
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=1)
    assert myValidBinance.getWallet() == [
        {"symbol": "ATOM", "price": 1, "bal": 37.17447000, "balInDollar": 37.17447000}
    ]


def test_displayWallet(capsys, myValidBinance):
    wallet = [
        {"symbol": "Test1", "price": 3.3333, "bal": 2.2222, "balInDollar": 1.1111},
        {"symbol": "Test2", "price": 4.4444, "bal": 3.3333, "balInDollar": 2.2222},
    ]
    expectedKeywords = [
        "Binance      Price    Balance    Balance ($)",
        "Test1         3.33     2.2222           1.11",
        "Test2         4.44     3.3333           2.22",
    ]

    myValidBinance.displayWallet(wallet)
    captured = capsys.readouterr()

    for keyword in expectedKeywords:
        assert keyword in captured.out
