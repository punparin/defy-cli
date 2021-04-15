from click.testing import CliRunner
from defy.cli import *
import pytest


@pytest.fixture
def walletAddress():
    return "0x683EdA55093092CF1D5365E6794597A3332A8FBc"


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli)  # noqa: F405

    assert result.exit_code == 0
    assert "Usage: cli [OPTIONS] COMMAND [ARGS]" in result.output


def test_all(mocker, walletAddress):
    runner = CliRunner()
    expectedKeywords = [
        "Wallet         Price    Balance    Balance ($)",
        "TEST WALLET     0.10          1           0.10",
        "ValueDefi         Deposit    Reward    Balance    Balance ($)",
        "TEST VALUEDEFI     1.1100    2.2200       3.33           6.66",
        "Fulcrum         Deposit    Reward (BGOV)    Balance ($)",
        "TEST FULCRUM     2.2200           0.4000           7.02",
        "Binance          Price    Balance    Balance ($)",
        "TEST EXCHANGE        1    37.1745          37.17",
        "Total Balance: $50.95",
    ]

    mocker.patch(
        "defy.Wallet.Wallet.getWallet",
        return_value=[
            {"symbol": "TEST WALLET", "price": 0.1, "bal": 1, "balInDollar": 0.1}
        ],
    )
    mocker.patch(
        "defy.exchanges.Binance.Binance.getWallet",
        return_value=[
            {
                "symbol": "TEST EXCHANGE",
                "price": 1,
                "bal": 37.17447000,
                "balInDollar": 37.17447000,
            }
        ],
    )
    mocker.patch(
        "defy.platforms.ValueDefi.ValueDefi.getWallet",
        return_value=[
            {
                "pairSymbol": "TEST VALUEDEFI",
                "deposit": 1.11,
                "reward": 2.22,
                "bal": 3.33,
                "balInDollar": 6.66,
            }
        ],
    )
    mocker.patch(
        "defy.platforms.Fulcrum.Fulcrum.getWallet",
        return_value=[
            {
                "symbol": "TEST FULCRUM",
                "deposit": 2.22,
                "reward": 0.4,
                "balInDollar": 7.02,
            }
        ],
    )

    result = runner.invoke(all, [walletAddress])  # noqa: F405

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output


def test_wallet(mocker, walletAddress):
    runner = CliRunner()
    expectedKeywords = [
        "Wallet         Price    Balance    Balance ($)",
        "TEST WALLET     0.10          1           0.10",
        "Total Balance: $0.10",
    ]

    mocker.patch(
        "defy.Wallet.Wallet.getWallet",
        return_value=[
            {"symbol": "TEST WALLET", "price": 0.1, "bal": 1, "balInDollar": 0.1}
        ],
    )

    result = runner.invoke(wallet, [walletAddress])  # noqa: F405

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output


def test_platform(mocker, walletAddress):
    runner = CliRunner()
    expectedKeywords = [
        "Fulcrum         Deposit    Reward (BGOV)    Balance ($)",
        "TEST FULCRUM     2.2200           0.4000           7.02",
        "ValueDefi         Deposit    Reward    Balance    Balance ($)",
        "TEST VALUEDEFI     1.1100    2.2200       3.33           6.66",
        "Total Balance: $13.68",
    ]

    mocker.patch(
        "defy.platforms.ValueDefi.ValueDefi.getWallet",
        return_value=[
            {
                "pairSymbol": "TEST VALUEDEFI",
                "deposit": 1.11,
                "reward": 2.22,
                "bal": 3.33,
                "balInDollar": 6.66,
            }
        ],
    )
    mocker.patch(
        "defy.platforms.Fulcrum.Fulcrum.getWallet",
        return_value=[
            {
                "symbol": "TEST FULCRUM",
                "deposit": 2.22,
                "reward": 0.4,
                "balInDollar": 7.02,
            }
        ],
    )

    result = runner.invoke(platform, [walletAddress])  # noqa: F405

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output


def test_exchange(mocker):
    runner = CliRunner()
    expectedKeywords = [
        "Binance          Price    Balance    Balance ($)",
        "TEST EXCHANGE        1    37.1745          37.17",
        "Total Balance: $37.17",
    ]

    mocker.patch(
        "defy.exchanges.Binance.Binance.getWallet",
        return_value=[
            {
                "symbol": "TEST EXCHANGE",
                "price": 1,
                "bal": 37.17447000,
                "balInDollar": 37.17447000,
            }
        ],
    )

    result = runner.invoke(exchange)  # noqa: F405

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output
