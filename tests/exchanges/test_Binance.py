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


@pytest.fixture
def myWallet():
    return [
        {
            "symbol": "BTC",
            "price": 0.9,
            "bal": 1e-08,
            "balInDollar": 9.000000000000001e-09,
        },
        {"symbol": "USDT", "price": 0.9, "bal": 1.06009357, "balInDollar": 0.954084213},
        {"symbol": "ATOM", "price": 0.9, "bal": 37.17447, "balInDollar": 33.457023},
    ]


def test_isUsable_with_credentials(myValidBinance):
    assert myValidBinance.isUsable()


def test_isUsable_without_credentials(myInvalidBinance):
    assert not myInvalidBinance.isUsable()


def test_existInWallet(myValidBinance, myWallet):
    assert myValidBinance.existInWallet(myWallet, "BTC")
    assert not myValidBinance.existInWallet(myWallet, "LINK")


def test_getTokenInWallet(myValidBinance, myWallet):
    assert myValidBinance.getTokenInWallet(myWallet, "BTC") is not None
    assert myValidBinance.getTokenInWallet(myWallet, "LINK") is None


def test_getFuturesWallet(mocker, myValidBinance):
    with open("tests/mocks/binance_futures_account.json", "r") as mock_definition:
        futuresAccountMock = json.load(mock_definition)

    mocker.patch(
        "binance.client.Client.futures_account", return_value=futuresAccountMock
    )
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=0.9)

    assert myValidBinance.getFuturesWallet() == []


def test_getFuturesWallet_with_not_hideSmallBalance(mocker, myValidBinance):
    with open("tests/mocks/binance_futures_account.json", "r") as mock_definition:
        futuresAccountMock = json.load(mock_definition)

    mocker.patch(
        "binance.client.Client.futures_account", return_value=futuresAccountMock
    )
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=0.9)

    assert myValidBinance.getFuturesWallet(False) == [
        {"symbol": "USDT", "price": 0.9, "bal": 1.06009357, "balInDollar": 0.954084213}
    ]


def test_getWallet(mocker, myValidBinance):
    with open("tests/mocks/binance_get_account.json", "r") as mock_definition:
        spotAccountMock = json.load(mock_definition)

    with open("tests/mocks/binance_futures_account.json", "r") as mock_definition:
        futuresAccountMock = json.load(mock_definition)

    mocker.patch("binance.client.Client.get_account", return_value=spotAccountMock)
    mocker.patch(
        "binance.client.Client.futures_account", return_value=futuresAccountMock
    )
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=0.9)

    assert myValidBinance.getWallet() == [
        {"symbol": "ATOM", "price": 0.9, "bal": 37.17447, "balInDollar": 33.457023}
    ]


def test_getWallet_with_not_hideSmallBalance(mocker, myValidBinance):
    with open("tests/mocks/binance_get_account.json", "r") as mock_definition:
        spotAccountMock = json.load(mock_definition)

    with open("tests/mocks/binance_futures_account.json", "r") as mock_definition:
        futuresAccountMock = json.load(mock_definition)

    mocker.patch("binance.client.Client.get_account", return_value=spotAccountMock)
    mocker.patch(
        "binance.client.Client.futures_account", return_value=futuresAccountMock
    )
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=0.9)

    assert myValidBinance.getWallet(False) == [
        {
            "symbol": "BTC",
            "price": 0.9,
            "bal": 1e-08,
            "balInDollar": 9.000000000000001e-09,
        },
        {"symbol": "USDT", "price": 0.9, "bal": 1.06009357, "balInDollar": 0.954084213},
        {"symbol": "ATOM", "price": 0.9, "bal": 37.17447, "balInDollar": 33.457023},
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
