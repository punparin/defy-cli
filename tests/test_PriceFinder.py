import pytest
from defy.PriceFinder import PriceFinder


@pytest.fixture
def myPriceFinder():
    return PriceFinder()


def test_getTokenPrice(myPriceFinder):
    assert myPriceFinder.getTokenPrice("BUSD") == 1
