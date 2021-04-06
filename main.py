import click
from Wallet import Wallet

__author__ = "Parin Kobboon"

@click.command()
@click.option("-a", "--address", type=str, required=True, help="Your wallet address")
@click.option("-hsb", "--hide-small-bal", "hideSmallBal", is_flag=True, default=False, help="`True` to hide small balance in wallet, default=false")
def cli(address, hideSmallBal):
    wallet.displayWallet(address, hideSmallBal)

if __name__ == '__main__':
    wallet = Wallet()
    cli()