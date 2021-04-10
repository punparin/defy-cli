import pytest
from defy.PriceFinder import PriceFinder
from defy.exchanges.Binance import Binance


@pytest.fixture
def myValidBinance():
    binance = Binance(PriceFinder())
    binance.binanceApiKey = "TEST"
    binance.binanceApiSecret = "TEST"
    return binance


@pytest.fixture
def myInvalidBinance():
    binance = Binance(PriceFinder())
    binance.binanceApiKey = None
    binance.binanceApiSecret = None
    return binance


def test_isUsable_with_credentials(myValidBinance):
    assert myValidBinance.isUsable()


def test_isUsable_without_credentials(myInvalidBinance):
    assert not myInvalidBinance.isUsable()


def test_getWallet(myInvalidBinance):
    assert myInvalidBinance.getWallet() == []


def test_displayWallet(capsys, myValidBinance):
    wallet = [["Test1", 3.3333, 2.2222, 1.1111], ["Test2", 4.4444, 3.3333, 2.2222]]
    expectedWallet = "Binance      Price    Balance    Balance ($)\n---------  -------  ---------  -------------\nTest1         3.33     2.2222           1.11\nTest2         4.44     3.3333           2.22 \n\n"

    myValidBinance.displayWallet(wallet)
    captured = capsys.readouterr()

    assert captured.out == expectedWallet
