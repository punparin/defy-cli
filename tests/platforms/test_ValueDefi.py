import pytest
from defy.PriceFinder import PriceFinder
from defy.platforms.ValueDefi import ValueDefi
import json
import responses
from configparser import ConfigParser
from tests.MockContext import *


@pytest.fixture
def myValueDefi(myPriceFinder):
    return ValueDefi(myPriceFinder)


@pytest.fixture
def walletAddress():
    return "0x683EdA55093092CF1D5365E6794597A3332A8FBc"


@pytest.fixture
def contractAddress():
    return "0xdec50bf0e3c8522cee42a7c1754b9582143c7cb7"


def test_getTokenBalance(myValueDefi, contractAddress, walletAddress):
    assert myValueDefi.getTokenBalance(contractAddress, walletAddress) == 0


def test_getTokenPricePerShare(myValueDefi, contractAddress):
    assert type(myValueDefi.getTokenPricePerShare(contractAddress)) == float


@responses.activate
def test_getWallet(mocker, myValueDefi, walletAddress):
    with open("tests/mocks/valuedefi_endpoint.json", "r") as mock_definition:
        mockReponse = json.load(mock_definition)

    config = ConfigParser()
    config.read("./config.ini")
    valuedefiEndpoint = config["DEFAULT"]["valuedefi_endpoint"]

    mocker.patch("defy.platforms.ValueDefi.ValueDefi.getTokenBalance", return_value=1)
    mocker.patch(
        "defy.platforms.ValueDefi.ValueDefi.getTokenPricePerShare", return_value=1.5
    )
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=0.1)
    responses.add(responses.GET, valuedefiEndpoint, json=mockReponse, status=200)

    assert myValueDefi.getWallet(walletAddress) == []


@responses.activate
def test_getWallet_with_not_hideSmallBalance(mocker, myValueDefi, walletAddress):
    with open("tests/mocks/valuedefi_endpoint.json", "r") as mock_definition:
        mockReponse = json.load(mock_definition)

    config = ConfigParser()
    config.read("./config.ini")
    valuedefiEndpoint = config["DEFAULT"]["valuedefi_endpoint"]

    mocker.patch("defy.platforms.ValueDefi.ValueDefi.getTokenBalance", return_value=1)
    mocker.patch(
        "defy.platforms.ValueDefi.ValueDefi.getTokenPricePerShare", return_value=1.5
    )
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=10)
    responses.add(responses.GET, valuedefiEndpoint, json=mockReponse, status=200)

    assert myValueDefi.getWallet(walletAddress, False) == [
        {
            "pairSymbol": "Warden-BUSD",
            "deposit": 1,
            "reward": 0.5,
            "bal": 1.5,
            "balInDollar": 30.0,
        }
    ]


def test_displayWallet(capsys, myValueDefi):
    farms = [
        {
            "pairSymbol": "Test1",
            "deposit": 1.11,
            "reward": 2.22,
            "bal": 3.33,
            "balInDollar": 6.66,
        },
        {
            "pairSymbol": "Test2",
            "deposit": 5.55,
            "reward": 6.66,
            "bal": 12.21,
            "balInDollar": 24.42,
        },
    ]
    expectedKeywords = [
        "ValueDefi      Deposit    Reward    Balance    Balance ($)",
        "Test1           1.1100    2.2200       3.33           6.66",
        "Test2           5.5500    6.6600      12.21          24.42",
    ]

    myValueDefi.displayWallet(farms)
    captured = capsys.readouterr()

    for keyword in expectedKeywords:
        assert keyword in captured.out
