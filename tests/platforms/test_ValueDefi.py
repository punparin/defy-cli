import pytest
from defy.PriceFinder import PriceFinder
from defy.platforms.ValueDefi import ValueDefi

@pytest.fixture
def myValueDefi():
    return ValueDefi(PriceFinder())

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

def test_getWallet(myValueDefi, walletAddress):
    assert myValueDefi.getWallet(walletAddress) == []

def test_getWallet_with_not_hideSmallBalance(myValueDefi, walletAddress):
    assert myValueDefi.getWallet(walletAddress, False) == [] 