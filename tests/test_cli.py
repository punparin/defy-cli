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
        "Binance          Price    Balance    Balance ($)",
        "TEST EXCHANGE        1    37.1745          37.17",
        "Total Balance: $43.93",
    ]

    mocker.patch(
        "defy.Wallet.Wallet.getWallet", return_value=[["TEST WALLET", 0.1, 1, 0.1]]
    )
    mocker.patch(
        "defy.platforms.ValueDefi.ValueDefi.getWallet",
        return_value=[["TEST VALUEDEFI", 1.11, 2.22, 3.33, 6.66]],
    )
    mocker.patch(
        "defy.exchanges.Binance.Binance.getWallet",
        return_value=[["TEST EXCHANGE", 1, 37.17447000, 37.17447000]],
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
        "defy.Wallet.Wallet.getWallet", return_value=[["TEST WALLET", 0.1, 1, 0.1]]
    )

    result = runner.invoke(wallet, [walletAddress])  # noqa: F405

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output


def test_platform(mocker, walletAddress):
    runner = CliRunner()
    expectedKeywords = [
        "ValueDefi         Deposit    Reward    Balance    Balance ($)",
        "TEST VALUEDEFI     1.1100    2.2200       3.33           6.66",
        "Total Balance: $6.66",
    ]

    mocker.patch(
        "defy.platforms.ValueDefi.ValueDefi.getWallet",
        return_value=[["TEST VALUEDEFI", 1.11, 2.22, 3.33, 6.66]],
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
        return_value=[["TEST EXCHANGE", 1, 37.17447000, 37.17447000]],
    )

    result = runner.invoke(exchange)  # noqa: F405

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output
