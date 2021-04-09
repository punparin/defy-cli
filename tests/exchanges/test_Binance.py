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