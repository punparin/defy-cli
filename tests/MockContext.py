import pytest
from defy.PriceFinder import PriceFinder
import json
import responses
from configparser import ConfigParser


@pytest.fixture
@responses.activate
def myPriceFinder(mocker):
    with open("tests/mocks/pancake_price_endpoint.json", "r") as mock_definition:
        pancakePriceMockReponse = json.load(mock_definition)
    with open("tests/mocks/oneinch_chain_56_endpoint.json", "r") as mock_definition:
        oneInchChain56MockReponse = json.load(mock_definition)
    with open("tests/mocks/oneinch_price_endpoint.json", "r") as mock_definition:
        oneInchPriceMockReponse = json.load(mock_definition)

    config = ConfigParser()
    config.read("./config.ini")
    pancakePriceEndpoint = config["DEFAULT"]["pancake_price_endpoint"]
    oneInchChain56Endpoint = config["DEFAULT"]["oneinch_chain_56_endpoint"]
    oneInchPriceEndpoint = config["DEFAULT"]["oneinch_price_endpoint"]

    mocker.patch("defy.PriceFinder.PriceFinder.getBNBPrice", return_value=555.55)

    responses.add(
        responses.GET, pancakePriceEndpoint, json=pancakePriceMockReponse, status=200
    )
    responses.add(
        responses.GET,
        oneInchChain56Endpoint,
        json=oneInchChain56MockReponse,
        status=200,
    )
    responses.add(
        responses.GET, oneInchPriceEndpoint, json=oneInchPriceMockReponse, status=200
    )

    return PriceFinder()
