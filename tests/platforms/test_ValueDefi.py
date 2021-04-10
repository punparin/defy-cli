import pytest
from defy.PriceFinder import PriceFinder
from defy.platforms.ValueDefi import ValueDefi
import json
import responses
from configparser import ConfigParser


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


@responses.activate
def test_getWallet(mocker, myValueDefi, walletAddress):
    with open("tests/mocks/valuedefi_valuedefi_endpoint.json", "r") as mock_definition:
        mockReponse = json.load(mock_definition)

    config = ConfigParser()
    config.read("./config.ini")
    valuedefiEndpoint = config["DEFAULT"]["valuedefi_endpoint"]

    mocker.patch("defy.platforms.ValueDefi.ValueDefi.getTokenBalance", return_value=1)
    mocker.patch(
        "defy.platforms.ValueDefi.ValueDefi.getTokenPricePerShare", return_value=1.5
    )
    mocker.patch("defy.PriceFinder.PriceFinder.getTokenPrice", return_value=1)
    responses.add(responses.GET, valuedefiEndpoint, json=mockReponse, status=200)

    assert myValueDefi.getWallet(walletAddress) == [["Warden-BUSD", 1, 0.5, 3.0]]


def test_getWallet_with_not_hideSmallBalance(myValueDefi, walletAddress):
    assert myValueDefi.getWallet(walletAddress, False) == []


def test_displayWallet(capsys, myValueDefi):
    farms = [["Test1", 3.3333, 2.2222, 1.1111], ["Test2", 4.4444, 3.3333, 2.2222]]
    expectedFarms = "ValueDefi      Balance    Reward    Balance ($)\n-----------  ---------  --------  -------------\nTest1           3.3333    2.2222           1.11\nTest2           4.4444    3.3333           2.22 \n\n"

    myValueDefi.displayWallet(farms)
    captured = capsys.readouterr()

    assert captured.out == expectedFarms
