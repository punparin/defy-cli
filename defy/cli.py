import click
from defy.Utilities import Utilities
from defy.Wallet import Wallet
from defy.PriceFinder import PriceFinder
from defy.platforms.ValueDefi import ValueDefi


__author__ = "Parin Kobboon"


priceFinder = PriceFinder()

wallet = Wallet(priceFinder)
valueDefi = ValueDefi(priceFinder)

@click.command()
@click.option("-a", "--address", type=str, required=True, help="Your wallet address")
@click.option("-hsb", "--hide-small-bal", "hideSmallBal", is_flag=True, default=False, help="`True` to hide small balance in wallet, default=false")
def cli(address, hideSmallBal):
    walletBal = wallet.getWallet(address, hideSmallBal)
    valueDefiBal = valueDefi.getPlatformFarms(address)

    total = Utilities.getTotal([walletBal, valueDefiBal])

    wallet.displayWallet(walletBal)
    valueDefi.displayPlatformFarms(valueDefiBal)
    Utilities.displayTotal(total)