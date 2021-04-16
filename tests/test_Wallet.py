import pytest
from defy.PriceFinder import PriceFinder
from defy.Wallet import Wallet
import json
import responses
from configparser import ConfigParser
from tests.MockContext import *


@pytest.fixture
def myWallet(myPriceFinder):
    return Wallet(myPriceFinder)


@pytest.fixture
def walletAddress():
    return "0x683EdA55093092CF1D5365E6794597A3332A8FBc"


@pytest.fixture
def contractAddress():
    return "0xe9e7cea3dedca5984780bafc599bd69add087d56"


def test_getTokenBalance(myWallet, contractAddress, walletAddress):
    assert myWallet.getTokenBalance(contractAddress, walletAddress) == 0


def test_getTokenName(myWallet, contractAddress):
    assert myWallet.getTokenName(contractAddress) == "BUSD Token"


def test_getSymbol(myWallet, contractAddress):
    assert myWallet.getSymbol(contractAddress) == "BUSD"


@responses.activate
def test_getWalletTokens(mocker, myWallet, walletAddress):
    with open("tests/mocks/bscscan_transaction_endpoint.json", "r") as mock_definition:
        mockReponse = json.load(mock_definition)

    config = ConfigParser()
    config.read("./config.ini")
    transactionEndpoint = (
        config["DEFAULT"]["bscscan_transaction_endpoint"] + "&address=" + walletAddress
    )

    responses.add(responses.GET, transactionEndpoint, json=mockReponse, status=200)

    assert myWallet.getWalletTokens(walletAddress) == {
        "SXP": "0x47bead2563dcbf3bf2c9407fea4dc236faba485a"
    }


def test_getWallet(mocker, myWallet, walletAddress):
    mocker.patch(
        "defy.Wallet.Wallet.getWalletTokens",
        return_value={
            "Warden": "0x0feadcc3824e7f3c12f40e324a60c23ca51627fc",
            "ADA": "0x3ee2200efb3400fabb9aacf31297cbdd1d435d47",
        },
    )
    mocker.patch("defy.Wallet.Wallet.getTokenBalance", return_value=1)
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=0.1)

    assert myWallet.getWallet(walletAddress) == []


def test_getWallet_with_not_hideSmallBalance(mocker, myWallet, walletAddress):
    mocker.patch(
        "defy.Wallet.Wallet.getWalletTokens",
        return_value={
            "Warden": "0x0feadcc3824e7f3c12f40e324a60c23ca51627fc",
            "ADA": "0x3ee2200efb3400fabb9aacf31297cbdd1d435d47",
        },
    )
    mocker.patch("defy.Wallet.Wallet.getTokenBalance", return_value=1)
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=0.1)

    assert myWallet.getWallet(walletAddress, False) == [
        {"symbol": "Warden", "price": 0.1, "bal": 1, "balInDollar": 0.1},
        {"symbol": "ADA", "price": 0.1, "bal": 1, "balInDollar": 0.1},
    ]


def test_displayWallet(capsys, myWallet):
    wallet = [
        {"symbol": "Test1", "price": 3.3333, "bal": 2.2222, "balInDollar": 1.1111},
        {"symbol": "Test2", "price": 4.4444, "bal": 3.3333, "balInDollar": 2.2222},
    ]
    expectedKeywords = [
        "Wallet      Price    Balance    Balance ($)",
        "Test1        3.33     2.2222           1.11",
        "Test2        4.44     3.3333           2.22",
    ]

    myWallet.displayWallet(wallet)
    captured = capsys.readouterr()

    for keyword in expectedKeywords:
        assert keyword in captured.out
