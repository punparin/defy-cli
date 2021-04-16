import pytest
from defy.PriceFinder import PriceFinder
from defy.platforms.AutoFarm import AutoFarm
import json
import responses
from configparser import ConfigParser
from tests.MockContext import *


@pytest.fixture
def myAutoFarm(myPriceFinder):
    return AutoFarm(myPriceFinder)


@pytest.fixture
def walletAddress():
    return "0x683EdA55093092CF1D5365E6794597A3332A8FBc"


@pytest.fixture
def farmId():
    return 6


def test_getTokenBalance(myAutoFarm, farmId, walletAddress):
    assert myAutoFarm.getTokenBalance(farmId, walletAddress) == 0


def test_getReward(myAutoFarm, farmId, walletAddress):
    assert myAutoFarm.getReward(farmId, walletAddress) == 0


@responses.activate
def test_getWallet(mocker, myAutoFarm, walletAddress):
    with open("tests/mocks/autofarm_endpoint.json", "r") as mock_definition:
        mockReponse = json.load(mock_definition)

    config = ConfigParser()
    config.read("./config.ini")
    autoFarmEndpoint = config["DEFAULT"]["autofarm_endpoint"]

    mocker.patch("defy.platforms.AutoFarm.AutoFarm.getTokenBalance", return_value=0.1)
    mocker.patch("defy.platforms.AutoFarm.AutoFarm.getReward", return_value=1)
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=0.3)

    responses.add(responses.GET, autoFarmEndpoint, json=mockReponse, status=200)

    assert myAutoFarm.getWallet(walletAddress) == []


@responses.activate
def test_getWallet_with_not_hideSmallBalance(mocker, myAutoFarm, walletAddress):
    with open("tests/mocks/autofarm_endpoint.json", "r") as mock_definition:
        mockReponse = json.load(mock_definition)

    config = ConfigParser()
    config.read("./config.ini")
    autoFarmEndpoint = config["DEFAULT"]["autofarm_endpoint"]

    mocker.patch("defy.platforms.AutoFarm.AutoFarm.getTokenBalance", return_value=0.1)
    mocker.patch("defy.platforms.AutoFarm.AutoFarm.getReward", return_value=1)
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=0.3)

    responses.add(responses.GET, autoFarmEndpoint, json=mockReponse, status=200)

    assert myAutoFarm.getWallet(walletAddress, False) == [
        {"symbol": "WBNB", "deposit": 0.1, "reward": 1, "balInDollar": 0.45},
        {"symbol": "BUSD", "deposit": 0.1, "reward": 1, "balInDollar": 0.3},
        {"symbol": "BTCB", "deposit": 0.1, "reward": 1, "balInDollar": 0.3},
        {"symbol": "ETH", "deposit": 0.1, "reward": 1, "balInDollar": 0.3},
        {"symbol": "LINK", "deposit": 0.1, "reward": 1, "balInDollar": 0.3},
        {"symbol": "WBNB-AUTO LP", "deposit": 0.1, "reward": 1, "balInDollar": 0.855},
    ]


def test_displayWallet(capsys, myAutoFarm):
    farms = [
        {"symbol": "WBNB", "deposit": 0.1, "reward": 1, "balInDollar": 0.45},
        {"symbol": "BUSD", "deposit": 0.1, "reward": 1, "balInDollar": 0.3},
    ]
    expectedKeywords = [
        "autofarm      Deposit    Reward (AUTO)    Balance ($)",
        "WBNB           0.1000                1           0.45",
        "BUSD           0.1000                1           0.30",
    ]

    myAutoFarm.displayWallet(farms)
    captured = capsys.readouterr()

    for keyword in expectedKeywords:
        assert keyword in captured.out
