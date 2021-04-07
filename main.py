import click
from Utilities import *
from Wallet import Wallet
from PriceFinder import PriceFinder
from platforms.ValueDefi import ValueDefi

__author__ = "Parin Kobboon"

@click.command()
@click.option("-a", "--address", type=str, required=True, help="Your wallet address")
@click.option("-hsb", "--hide-small-bal", "hideSmallBal", is_flag=True, default=False, help="`True` to hide small balance in wallet, default=false")
def cli(address, hideSmallBal):
    walletBal = wallet.getWallet(address, hideSmallBal)
    valueDefiBal = valueDefi.getPlatformFarms(address)

    total = getTotal([walletBal, valueDefiBal])

    wallet.displayWallet(walletBal)
    valueDefi.displayPlatformFarms(valueDefiBal)
    displayTotal(total)

if __name__ == '__main__':
    priceFinder = PriceFinder()

    wallet = Wallet(priceFinder)
    valueDefi = ValueDefi(priceFinder)

    cli()