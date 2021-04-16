import pytest
from defy.PriceFinder import PriceFinder
from defy.platforms.Fulcrum import Fulcrum
import json
import responses
from configparser import ConfigParser
from tests.MockContext import *


@pytest.fixture
def myFulcrum(myPriceFinder):
    return Fulcrum(myPriceFinder)


@pytest.fixture
def walletAddress():
    return "0x683EdA55093092CF1D5365E6794597A3332A8FBc"


@pytest.fixture
def contractAddress():
    return "0xacD39C8d46461bCa7D5Fb23eCD57A4CB0D31fAB5"


def test_getLoanTokenAddress(myFulcrum, contractAddress):
    assert (
        myFulcrum.getLoanTokenAddress(contractAddress)
        == "0xF8A0BF9cF54Bb92F17374d9e9A321E6a111a51bD"
    )


def test_getReward(myFulcrum, walletAddress):
    assert type(myFulcrum.getReward(walletAddress)) == list


def test_getSymbol(myFulcrum, contractAddress):
    assert myFulcrum.getSymbol(contractAddress) == "iLINK"


def test_getPoolInfos(myFulcrum):
    assert type(myFulcrum.getPoolInfos()) == list


def test_getWallet(mocker, myFulcrum, walletAddress):
    mocker.patch(
        "defy.platforms.Fulcrum.Fulcrum.getPoolInfos",
        return_value=[
            (
                "0x49646513609085f39D9e44b413c74530Ba6E2c0F",
                12500,
                6593849,
                278306568701334,
            ),
            (
                "0x7343b25c4953f4C57ED4D16c33cbEDEFAE9E8Eb9",
                12500,
                6593837,
                639244337442,
            ),
            (
                "0x949cc03E43C24A954BAa963A00bfC5ab146c6CE7",
                12500,
                6593869,
                1329019963679530,
            ),
            (
                "0xf326b42A237086F1De4E7D68F2d2456fC787bc01",
                12500,
                6593841,
                785712478028,
            ),
            (
                "0x97eBF27d40D306aD00bb2922E02c58264b295a95",
                12500,
                6593868,
                31930068812150232,
            ),
            (
                "0xA726F2a7B200b03beB41d1713e6158e0bdA8731F",
                75000,
                6593836,
                510472359357,
            ),
            (
                "0xEcd0aa12A453AE356Aba41f62483EDc35f2290ed",
                100000,
                6593881,
                8135218590011319,
            ),
            (
                "0xf8E026dC4C0860771f691EcFFBbdfe2fa51c77CF",
                12500,
                6593865,
                242803563053,
            ),
            (
                "0xacD39C8d46461bCa7D5Fb23eCD57A4CB0D31fAB5",
                12500,
                6593721,
                560846008470763,
            ),
        ],
    )
    mocker.patch(
        "web3.contract.ContractFunction.call",
        return_value=[
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [32650000000000000000, 4534765066782440000],
            [0, 0],
            [18780000000000000000, 4142765066782440000],
        ],
    )
    mocker.patch(
        "defy.platforms.Fulcrum.Fulcrum.getLoanTokenAddress",
        return_value="0xF8A0BF9cF54Bb92F17374d9e9A321E6a111a51bD",
    )
    mocker.patch(
        "defy.platforms.Fulcrum.Fulcrum.getReward",
        return_value=[0, 0, 0, 0, 0, 0, 0, 0, 4137620697064440000],
    )
    mocker.patch("defy.platforms.Fulcrum.Fulcrum.getSymbol", return_value="LINK")
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=0.01)

    assert myFulcrum.getWallet(walletAddress) == []


def test_getWallet_with_not_hideSmallBalance(mocker, myFulcrum, walletAddress):
    mocker.patch(
        "defy.platforms.Fulcrum.Fulcrum.getPoolInfos",
        return_value=[
            (
                "0x49646513609085f39D9e44b413c74530Ba6E2c0F",
                12500,
                6593849,
                278306568701334,
            ),
            (
                "0x7343b25c4953f4C57ED4D16c33cbEDEFAE9E8Eb9",
                12500,
                6593837,
                639244337442,
            ),
            (
                "0x949cc03E43C24A954BAa963A00bfC5ab146c6CE7",
                12500,
                6593869,
                1329019963679530,
            ),
            (
                "0xf326b42A237086F1De4E7D68F2d2456fC787bc01",
                12500,
                6593841,
                785712478028,
            ),
            (
                "0x97eBF27d40D306aD00bb2922E02c58264b295a95",
                12500,
                6593868,
                31930068812150232,
            ),
            (
                "0xA726F2a7B200b03beB41d1713e6158e0bdA8731F",
                75000,
                6593836,
                510472359357,
            ),
            (
                "0xEcd0aa12A453AE356Aba41f62483EDc35f2290ed",
                100000,
                6593881,
                8135218590011319,
            ),
            (
                "0xf8E026dC4C0860771f691EcFFBbdfe2fa51c77CF",
                12500,
                6593865,
                242803563053,
            ),
            (
                "0xacD39C8d46461bCa7D5Fb23eCD57A4CB0D31fAB5",
                12500,
                6593721,
                560846008470763,
            ),
        ],
    )
    mocker.patch(
        "web3.contract.ContractFunction.call",
        return_value=[
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [32650000000000000000, 4534765066782440000],
            [0, 0],
            [18780000000000000000, 4142765066782440000],
        ],
    )
    mocker.patch(
        "defy.platforms.Fulcrum.Fulcrum.getLoanTokenAddress",
        return_value="0xF8A0BF9cF54Bb92F17374d9e9A321E6a111a51bD",
    )
    mocker.patch(
        "defy.platforms.Fulcrum.Fulcrum.getReward",
        return_value=[0, 0, 0, 0, 0, 0, 0, 0, 4137620697064440000],
    )
    mocker.patch("defy.platforms.Fulcrum.Fulcrum.getSymbol", return_value="LINK")
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=0.1)

    assert myFulcrum.getWallet(walletAddress) == [
        {"symbol": "LINK", "deposit": 32.65, "reward": 0.0, "balInDollar": 3.265},
        {
            "symbol": "LINK",
            "deposit": 18.78,
            "reward": 4.13762069706444,
            "balInDollar": 2.291762069706444,
        },
    ]


def test_displayWallet(capsys, myFulcrum):
    farms = [
        {"symbol": "Test1", "deposit": 2.22, "reward": 0.4, "balInDollar": 7.02},
        {"symbol": "Test2", "deposit": 3.33, "reward": 0.7, "balInDollar": 14.36},
    ]
    expectedKeywords = [
        "Fulcrum      Deposit    Reward (BGOV)    Balance ($)",
        "Test1         2.2200           0.4000           7.02",
        "Test2         3.3300           0.7000          14.36",
    ]

    myFulcrum.displayWallet(farms)
    captured = capsys.readouterr()

    for keyword in expectedKeywords:
        assert keyword in captured.out
