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
        "Binance         Price    Balance    Balance ($)",
        "TEST BINANCE        1    37.1745          37.17",
        "Binance Futures        Position     PNL    ROE %    Balance ($)",
        "TEST BINANCEFUTURES        0.90  0.0300     3.33           0.93",
        "autofarm         Deposit    Reward (AUTO)    Balance ($)",
        "TEST AUTOFARM     2.5237           0.0021        7354.72",
        "Fulcrum         Deposit    Reward (BGOV)    Balance ($)",
        "TEST FULCRUM     2.2200           0.4000           7.02",
        "ValueDefi         Deposit    Reward    Balance    Balance ($)",
        "TEST VALUEDEFI     1.1100    2.2200       3.33           6.66",
        "Total Balance: $7406.60",
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
                "symbol": "TEST BINANCE",
                "price": 1,
                "bal": 37.17447000,
                "balInDollar": 37.17447000,
            }
        ],
    )
    mocker.patch(
        "defy.exchanges.BinanceFutures.BinanceFutures.getWallet",
        return_value=[
            {
                "symbol": "TEST BINANCEFUTURES",
                "pos": 0.9,
                "pnl": 0.03,
                "roe": 3.3333333333333335,
                "balInDollar": 0.93,
            }
        ],
    )
    mocker.patch(
        "defy.platforms.AutoFarm.AutoFarm.getWallet",
        return_value=[
            {
                "symbol": "TEST AUTOFARM",
                "deposit": 2.5237,
                "reward": 0.0021,
                "balInDollar": 7354.72,
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

    result = runner.invoke(all, [walletAddress])  # noqa: F405
    print(result.output)
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
        "autofarm         Deposit    Reward (AUTO)    Balance ($)",
        "TEST AUTOFARM     2.5237           0.0021        7354.72",
        "Fulcrum         Deposit    Reward (BGOV)    Balance ($)",
        "TEST FULCRUM     2.2200           0.4000           7.02",
        "ValueDefi         Deposit    Reward    Balance    Balance ($)",
        "TEST VALUEDEFI     1.1100    2.2200       3.33           6.66",
        "Total Balance: $7368.40",
    ]

    mocker.patch(
        "defy.platforms.AutoFarm.AutoFarm.getWallet",
        return_value=[
            {
                "symbol": "TEST AUTOFARM",
                "deposit": 2.5237,
                "reward": 0.0021,
                "balInDollar": 7354.72,
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

    result = runner.invoke(platform, [walletAddress])  # noqa: F405

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output


def test_valuedefi(mocker, walletAddress):
    runner = CliRunner()
    expectedKeywords = [
        "ValueDefi         Deposit    Reward    Balance    Balance ($)",
        "TEST VALUEDEFI     1.1100    2.2200       3.33           6.66",
        "Total Balance: $6.66",
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

    result = runner.invoke(valuedefi, [walletAddress])  # noqa: F405

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output


def test_fulcrum(mocker, walletAddress):
    runner = CliRunner()
    expectedKeywords = [
        "Fulcrum         Deposit    Reward (BGOV)    Balance ($)",
        "TEST FULCRUM     2.2200           0.4000           7.02",
        "Total Balance: $7.02",
    ]

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

    result = runner.invoke(fulcrum, [walletAddress])  # noqa: F405

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output


def test_autofarm(mocker, walletAddress):
    runner = CliRunner()
    expectedKeywords = [
        "autofarm         Deposit    Reward (AUTO)    Balance ($)",
        "TEST AUTOFARM     2.5237           0.0021        7354.72",
        "Total Balance: $7354.72",
    ]

    mocker.patch(
        "defy.platforms.AutoFarm.AutoFarm.getWallet",
        return_value=[
            {
                "symbol": "TEST AUTOFARM",
                "deposit": 2.5237,
                "reward": 0.0021,
                "balInDollar": 7354.72,
            }
        ],
    )

    result = runner.invoke(autofarm, [walletAddress])  # noqa: F405

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output


def test_exchange(mocker):
    runner = CliRunner()
    expectedKeywords = [
        "Binance         Price    Balance    Balance ($)",
        "TEST BINANCE        1    37.1745          37.17",
        "Binance Futures        Position     PNL    ROE %    Balance ($)",
        "TEST BINANCEFUTURES        0.90  0.0300     3.33           0.93",
        "Total Balance: $38.10",
    ]

    mocker.patch(
        "defy.exchanges.Binance.Binance.getWallet",
        return_value=[
            {
                "symbol": "TEST BINANCE",
                "price": 1,
                "bal": 37.17447000,
                "balInDollar": 37.17447000,
            }
        ],
    )
    mocker.patch(
        "defy.exchanges.BinanceFutures.BinanceFutures.getWallet",
        return_value=[
            {
                "symbol": "TEST BINANCEFUTURES",
                "pos": 0.9,
                "pnl": 0.03,
                "roe": 3.3333333333333335,
                "balInDollar": 0.93,
            }
        ],
    )

    result = runner.invoke(exchange)  # noqa: F405

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output


def test_binance(mocker):
    runner = CliRunner()
    expectedKeywords = [
        "Binance         Price    Balance    Balance ($)",
        "TEST BINANCE        1    37.1745          37.17",
        "Binance Futures        Position     PNL    ROE %    Balance ($)",
        "TEST BINANCEFUTURES        0.90  0.0300     3.33           0.93",
        "Total Balance: $38.10",
    ]

    mocker.patch(
        "defy.exchanges.Binance.Binance.getWallet",
        return_value=[
            {
                "symbol": "TEST BINANCE",
                "price": 1,
                "bal": 37.17447000,
                "balInDollar": 37.17447000,
            }
        ],
    )
    mocker.patch(
        "defy.exchanges.BinanceFutures.BinanceFutures.getWallet",
        return_value=[
            {
                "symbol": "TEST BINANCEFUTURES",
                "pos": 0.9,
                "pnl": 0.03,
                "roe": 3.3333333333333335,
                "balInDollar": 0.93,
            }
        ],
    )

    result = runner.invoke(binance)  # noqa: F405

    assert result.exit_code == 0
    for keyword in expectedKeywords:
        assert keyword in result.output
