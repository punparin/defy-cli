import pytest
import os
from configparser import ConfigParser
from web3 import Web3
from defy.Utilities import Utilities

@pytest.fixture
def myWeb3():
    config = ConfigParser(os.environ)
    config.read("config.ini")

    return Web3(Web3.HTTPProvider(config["DEFAULT"]["network_provider"]))

def test_formatBalance(myWeb3):
    assert Utilities.formatBalance(myWeb3, 10**18) == 1
    
def test_GetTotal():
    tabulateBalances = [
        [["Test1", 3, 2, 6], ["Test2", 4, 3, 12]],
        [["Test1", 3, 2, 6], ["Test2", 4, 3, 12]]
    ]
    assert Utilities.getTotal(tabulateBalances) == 36