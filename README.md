[![Upload Python Package](https://github.com/punparin/defy-cli/actions/workflows/python_publish.yaml/badge.svg)](https://github.com/punparin/defy-cli/actions/workflows/python_publish.yaml) [![Python Test](https://github.com/punparin/defy-cli/actions/workflows/python_test.yaml/badge.svg)](https://github.com/punparin/defy-cli/actions/workflows/python_test.yaml) [![codecov](https://codecov.io/gh/punparin/defy-cli/branch/main/graph/badge.svg?token=0LT1TMH2VZ)](https://codecov.io/gh/punparin/defy-cli) [![CodeQL](https://github.com/punparin/defy-cli/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/punparin/defy-cli/actions/workflows/codeql-analysis.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# DeFy CLI
> is a command line tool to lookup wallet and DeFi platforms balance on blockchain network


```sh-session
$ defy all 0x60226a096fdcc916xxxx1feb94f21096fdd9f2a1

Wallet      Price    Balance    Balance ($)
--------  -------  ---------  -------------
Warden       0.67   134.2319          89.95
ADA          1.21   260.1230         315.08
LINK        32.80    18.7821         616.00

Binance      Price    Balance    Balance ($)
---------  -------  ---------  -------------
ATOM         21.05    37.1745         782.70

Binance Futures      Position       PNL    ROE %    Balance ($)
-----------------  ----------  --------  -------  -------------
LUNAUSDT               148.25   32.8795    22.18         181.13

autofarm        Deposit    Reward (AUTO)    Balance ($)
------------  ---------  ---------------  -------------
WBNB-AUTO LP     2.5237           0.0022        7218.35

Fulcrum      Deposit    Reward (BGOV)    Balance ($)
---------  ---------  ---------------  -------------
LINK         18.7800           4.2001         759.39

ValueDefi      Deposit    Reward    Balance    Balance ($)
-----------  ---------  --------  ---------  -------------
Warden-BUSD   980.7301  140.9000    1121.63        1873.24

Total Balance: $11835.84
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
         * [defy binance](#defy-binance)
         * [defy platform [ADDRESS]](#defy-platform-address)
         * [defy valuedefi [ADDRESS]](#defy-valuedefi-address)
         * [defy fulcrum [ADDRESS]](#defy-fulcrum-address)
         * [defy autofarm [ADDRESS]](#defy-autofarm-address)
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

| Platform       | Features | Support |
|----------------|----------|---------|
| autofarm       | Vaults   |   ✅    |
| Fulcrum (BSC)  | Farm     |   ✅    |
| ValueDefi      | vSafe    |   ✅    |

## Support Exchanges

| Exchange  | Features          | Support |
|-----------|-------------------|---------|
| Binance   | Fiat and Spot     |   ✅    |
|           | USDⓈ-M Futures   |   ✅    |

## Support Networks

| Network  | Support |
|-----------|---------|
| BSC Mainnet |  ✅   |

## Commands

* [`defy all [ADDRESS]`](#defy-all-address)
* [`defy wallet [ADDRESS]`](#defy-wallet-address)
* [`defy exchange`](#defy-exchange)
* [`defy binance`](#defy-binance)
* [`defy platform [ADDRESS]`](#defy-platform-address)
* [`defy valuedefi [ADDRESS]`](#defy-valuedefi-address)
* [`defy fulcrum [ADDRESS]`](#defy-fulcrum-address)
* [`defy autofarm [ADDRESS]`](#defy-autofarm-address)

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

### `defy binance`
```
Usage: defy binance [OPTIONS]

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

### `defy valuedefi [ADDRESS]`
```
Usage: defy valuedefi [OPTIONS] ADDRESS

Options:
  -hsb, --hide-small-bal  `True` to hide small balance in wallet,
                          default=false

  -h, --help              Show this message and exit.
```

### `defy fulcrum [ADDRESS]`
```
Usage: defy fulcrum [OPTIONS] ADDRESS

Options:
  -hsb, --hide-small-bal  `True` to hide small balance in wallet,
                          default=false

  -h, --help              Show this message and exit.
```

### `defy autofarm [ADDRESS]`
```
Usage: defy autofarm [OPTIONS] ADDRESS

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
$ w32tm /register
$ net start w32time
$ w32tm /resync
```