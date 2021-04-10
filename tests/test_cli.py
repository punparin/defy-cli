from click.testing import CliRunner
from defy.cli import *
import pytest


@pytest.fixture
def walletAddress():
    return "0x683EdA55093092CF1D5365E6794597A3332A8FBc"


def test_all(walletAddress):
    runner = CliRunner()
    result = runner.invoke(all, [walletAddress])
    expectedKeywords = [
        "Wallet",
        "ValueDefi",
        "Binance",
        "Reward",
        "Price",
        "Balance",
        "Balance ($)",
        "Total Balance: $",
    ]

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output


def test_wallet(walletAddress):
    runner = CliRunner()
    result = runner.invoke(wallet, [walletAddress])  # noqa: F405
    expectedKeywords = ["Wallet", "Price", "Balance", "Balance ($)", "Total Balance: $"]

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output


def test_platform(walletAddress):
    runner = CliRunner()
    result = runner.invoke(platform, [walletAddress])  # noqa: F405
    expectedKeywords = [
        "ValueDefi",
        "Balance",
        "Reward",
        "Balance ($)",
        "Total Balance: $",
    ]

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output


def test_exchange():
    runner = CliRunner()
    result = runner.invoke(exchange)  # noqa: F405
    expectedKeywords = [
        "Binance",
        "Price",
        "Balance",
        "Balance ($)",
        "Total Balance: $",
    ]

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output
