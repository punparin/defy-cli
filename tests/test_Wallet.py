import pytest
from defy.PriceFinder import PriceFinder
from defy.Wallet import Wallet

@pytest.fixture
def myWallet():
    return Wallet(PriceFinder())

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

def test_getWalletTokens(myWallet, walletAddress):
    assert myWallet.getWalletTokens(walletAddress) == {}

def test_getWallet(myWallet, walletAddress):
    assert myWallet.getWallet(walletAddress) == []

def test_getWallet_with_not_hideSmallBalance(myWallet, walletAddress):
    assert myWallet.getWallet(walletAddress, False) == [] 