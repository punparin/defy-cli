import pytest
from defy.PriceFinder import PriceFinder
import json
import responses
from configparser import ConfigParser


@pytest.fixture
@responses.activate
def myPriceFinder():
    with open("tests/mocks/pricefinder_pancake_endpoint.json", "r") as mock_definition:
        mockReponse = json.load(mock_definition)

    config = ConfigParser()
    config.read("./config.ini")
    pancakeEndpoint = config["DEFAULT"]["pancake_endpoint"]

    responses.add(responses.GET, pancakeEndpoint, json=mockReponse, status=200)

    return PriceFinder()


def test_getTokenPrice(myPriceFinder):
    assert myPriceFinder.getTokenPrice("TEST") == 1
