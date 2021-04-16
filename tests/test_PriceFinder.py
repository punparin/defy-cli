import pytest
from defy.PriceFinder import PriceFinder
import json
import responses
from configparser import ConfigParser
from tests.MockContext import *


def test_getTokenPrice(myPriceFinder):
    assert myPriceFinder.getTokenPrice("TEST") == 1
