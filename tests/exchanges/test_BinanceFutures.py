import pytest
from defy.PriceFinder import PriceFinder
from defy.exchanges.BinanceFutures import BinanceFutures
import json
import responses
from configparser import ConfigParser
from tests.MockContext import *


@pytest.fixture
def myValidBinanceFutures(myPriceFinder):
    binanceFutures = BinanceFutures(myPriceFinder)
    binanceFutures.binanceApiKey = "TEST"
    binanceFutures.binanceApiSecret = "TEST"
    return binanceFutures


@pytest.fixture
def myInvalidBinanceFutures(myPriceFinder):
    binanceFutures = BinanceFutures(myPriceFinder)
    binanceFutures.binanceApiKey = None
    binanceFutures.binanceApiSecret = None
    return binanceFutures


def test_isUsable_with_credentials(myValidBinanceFutures):
    assert myValidBinanceFutures.isUsable()


def test_isUsable_without_credentials(myInvalidBinanceFutures):
    assert not myInvalidBinanceFutures.isUsable()


def test_getWallet(mocker, myValidBinanceFutures):
    with open("tests/mocks/binance_futures_account.json", "r") as mock_definition:
        futuresAccountMock = json.load(mock_definition)

    mocker.patch(
        "binance.client.Client.futures_account", return_value=futuresAccountMock
    )

    assert myValidBinanceFutures.getWallet() == []


def test_getWallet_with_not_hideSmallBalance(mocker, myValidBinanceFutures):
    with open("tests/mocks/binance_futures_account.json", "r") as mock_definition:
        futuresAccountMock = json.load(mock_definition)

    mocker.patch(
        "binance.client.Client.futures_account", return_value=futuresAccountMock
    )

    assert myValidBinanceFutures.getWallet(False) == [
        {
            "symbol": "LUNAUSDT",
            "pos": 0.9,
            "pnl": 0.03,
            "roe": 3.3333333333333335,
            "balInDollar": 0.93,
        }
    ]


def test_displayWallet(capsys, myValidBinanceFutures):
    wallet = [
        {
            "symbol": "TEST1USDT",
            "pos": 0.9,
            "pnl": 0.03,
            "roe": 3.3333333333333335,
            "balInDollar": 0.93,
        }
    ]
    expectedKeywords = [
        "Binance Futures      Position     PNL    ROE %    Balance ($)",
        "TEST1USDT                0.90  0.0300     3.33           0.93",
    ]

    myValidBinanceFutures.displayWallet(wallet)
    captured = capsys.readouterr()

    for keyword in expectedKeywords:
        assert keyword in captured.out
