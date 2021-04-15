import click
from defy.Utilities import Utilities
from defy.Wallet import Wallet
from defy.PriceFinder import PriceFinder
from defy.exchanges.Binance import Binance
from defy.platforms.ValueDefi import ValueDefi
from defy.platforms.Fulcrum import Fulcrum

__author__ = "Parin Kobboon"


priceFinder = PriceFinder()

defyWallet = Wallet(priceFinder)
defyBinance = Binance(priceFinder)
defyValueDefi = ValueDefi(priceFinder)
defyFulcrum = Fulcrum(priceFinder)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command(
    "all", short_help="Lookup to all available wallet/platforms/exchanges balance"
)
@click.argument("address")
@click.option(
    "-hsb",
    "--hide-small-bal",
    "hideSmallBal",
    is_flag=True,
    default=False,
    help="`True` to hide small balance in wallet, default=false",
)
def all(address, hideSmallBal):
    walletBal = defyWallet.getWallet(address, hideSmallBal)
    binanceBal = defyBinance.getWallet(hideSmallBal)
    valueDefiBal = defyValueDefi.getWallet(address, hideSmallBal)
    fulcrumBal = defyFulcrum.getWallet(address, hideSmallBal)

    total = Utilities.getTotal(
        [
            {"bal": walletBal, "type": "wallet"},
            {"bal": binanceBal, "type": "binance"},
            {"bal": valueDefiBal, "type": "valuedefi"},
            {"bal": fulcrumBal, "type": "fulcrum"},
        ]
    )

    defyWallet.displayWallet(walletBal)
    defyBinance.displayWallet(binanceBal)
    defyFulcrum.displayWallet(fulcrumBal)
    defyValueDefi.displayWallet(valueDefiBal)

    Utilities.displayTotal(total)


@cli.command("wallet", short_help="Lookup to wallet balance")
@click.argument("address")
@click.option(
    "-hsb",
    "--hide-small-bal",
    "hideSmallBal",
    is_flag=True,
    default=False,
    help="`True` to hide small balance in wallet, default=false",
)
def wallet(address, hideSmallBal):
    walletBal = defyWallet.getWallet(address, hideSmallBal)

    total = Utilities.getTotal([{"bal": walletBal, "type": "wallet"}])

    defyWallet.displayWallet(walletBal)

    Utilities.displayTotal(total)


@cli.command("platform", short_help="Lookup to platforms balance")
@click.argument("address")
@click.option(
    "-hsb",
    "--hide-small-bal",
    "hideSmallBal",
    is_flag=True,
    default=False,
    help="`True` to hide small balance in wallet, default=false",
)
def platform(address, hideSmallBal):
    valueDefiBal = defyValueDefi.getWallet(address, hideSmallBal)
    fulcrumBal = defyFulcrum.getWallet(address, hideSmallBal)

    total = Utilities.getTotal(
        [
            {"bal": valueDefiBal, "type": "valuedefi"},
            {"bal": fulcrumBal, "type": "fulcrum"},
        ]
    )

    defyFulcrum.displayWallet(fulcrumBal)
    defyValueDefi.displayWallet(valueDefiBal)

    Utilities.displayTotal(total)


@cli.command("exchange", short_help="Lookup to exchanges balance")
@click.option(
    "-hsb",
    "--hide-small-bal",
    "hideSmallBal",
    is_flag=True,
    default=False,
    help="`True` to hide small balance in wallet, default=false",
)
def exchange(hideSmallBal):
    binanceBal = defyBinance.getWallet(hideSmallBal)

    total = Utilities.getTotal([{"bal": binanceBal, "type": "binance"}])

    defyBinance.displayWallet(binanceBal)

    Utilities.displayTotal(total)
