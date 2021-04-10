[![Upload Python Package](https://github.com/punparin/defy-cli/actions/workflows/python_publish.yaml/badge.svg)](https://github.com/punparin/defy-cli/actions/workflows/python_publish.yaml) [![Python Test](https://github.com/punparin/defy-cli/actions/workflows/python_test.yaml/badge.svg)](https://github.com/punparin/defy-cli/actions/workflows/python_test.yaml) [![codecov](https://codecov.io/gh/punparin/defy-cli/branch/main/graph/badge.svg?token=0LT1TMH2VZ)](https://codecov.io/gh/punparin/defy-cli) [![CodeQL](https://github.com/punparin/defy-cli/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/punparin/defy-cli/actions/workflows/codeql-analysis.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# DeFy CLI
> is a command line tool to lookup wallet and DeFi platforms balance on blockchain network


```sh-session
$ defy all 0x60226a096fdcc916xxxx1feb94f21096fdd9f2a1

Token      Price    Balance    Balance ($)
-------  -------  ---------  -------------
ACS        65.86     0.1560          10.28
ADA         1.21   260.1230         314.87
LINK       32.02    18.7821         601.48
AUTO     3568.35     0.0004           1.34
WATCH       1.19    21.1767          25.16

Binance      Price    Balance    Balance ($)
---------  -------  ---------  -------------
ATOM         20.31    37.1745         754.86

ValueDefi      Balance    Reward    Balance ($)
-----------  ---------  --------  -------------
Warden-BUSD   700.2664   72.4477        1289.95

Total Balance: $2348.17
```

Table of Contents
=================

   * [DeFy CLI](#defy-cli)
   * [Table of Contents](#table-of-contents)
      * [Prerequisite](#prerequisite)
      * [Installation](#installation)
      * [Support Platforms](#support-platforms)
      * [Support Exchanges](#support-exchanges)
      * [Support Networks](#support-networks)
      * [Commands](#commands)
         * [defy all [ADDRESS]](#defy-all-address)
         * [defy wallet [ADDRESS]](#defy-wallet-address)
         * [defy exchange](#defy-exchange)
         * [defy platform [ADDRESS]](#defy-platform-address)
      * [Known Issues](#known-issues)
         * [Timestamp for this request was 1000ms ahead of the server's time](#timestamp-for-this-request-was-1000ms-ahead-of-the-servers-time)

## Prerequisite
- (Optional) In case you would like to use Binance wallet lookup
  - [Binance API Key](https://www.binance.com/en-NG/support/faq/360002502072)
    `export binance_api_key=<BINANCE_API_KEY>`
  - [Binance API Secret](https://www.binance.com/en-NG/support/faq/360002502072)
    `export binance_api_secret=<BINANCE_API_SECRET>`

## Installation
```
$ pip install defy
```

## Support Platforms

| Platform  | Features | Support |
|-----------|----------|---------|
| ValueDefi | vSafe    |   ✅   |

## Support Exchanges

| Exchange  | Features | Support |
|-----------|----------|---------|
| Binance   | -        |   ✅    |

## Support Networks

| Network  | Support |
|-----------|---------|
| BSC Mainnet |  ✅   |

## Commands

* [`defy all [ADDRESS]`](#defy-all-address)
* [`defy wallet [ADDRESS]`](#defy-wallet-address)
* [`defy exchange`](#defy-exchange)
* [`defy platform [ADDRESS]`](#defy-platform-address)

### `defy all [ADDRESS]`
```
Usage: defy all [OPTIONS] ADDRESS

Options:
  -hsb, --hide-small-bal  `True` to hide small balance in wallet,
                          default=false

  -h, --help              Show this message and exit.
```

### `defy wallet [ADDRESS]`
```
Usage: defy wallet [OPTIONS] ADDRESS

Options:
  -hsb, --hide-small-bal  `True` to hide small balance in wallet,
                          default=false

  -h, --help              Show this message and exit.
```

### `defy exchange`
```
Usage: defy exchange [OPTIONS]

Options:
  -hsb, --hide-small-bal  `True` to hide small balance in wallet,
                          default=false

  -h, --help              Show this message and exit.
```

### `defy platform [ADDRESS]`
```
Usage: defy platform [OPTIONS] ADDRESS

Options:
  -hsb, --hide-small-bal  `True` to hide small balance in wallet,
                          default=false

  -h, --help              Show this message and exit.
```

## Known Issues

### Timestamp for this request was 1000ms ahead of the server's time

Run the following commands to resync machine's clock

> For Windows
```sh-session
$ net stop w32time
$ w32tm /unregister
$ net start w32time
$ w32tm /resync
```