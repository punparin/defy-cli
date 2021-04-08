[![Upload Python Package](https://github.com/punparin/defy-cli/actions/workflows/python_publish.yaml/badge.svg)](https://github.com/punparin/defy-cli/actions/workflows/python_publish.yaml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# DeFy CLI
is a command line tool to lookup wallet and DeFi platforms balance on blockchain network

<!-- toc -->

## Usage
```sh-session
$ py main.py --address 0x60226a096fdcc916xxxx1feb94f21096fdd9f2a1

Token      Price    Balance    Balance ($)
-------  -------  ---------  -------------
ACS        57.08     0.1560           8.91
ADA         1.19   260.1230         308.72
LINK       31.48    18.7821         591.24
AUTO     3461.64     0.0004           1.30
WATCH       1.08    21.1767          22.81 

ValueDefi Farm      Balance    Reward    Balance ($)
----------------  ---------  --------  -------------
Warden-BUSD        700.2664   57.2355        1415.19

Total Balance: $2348.17
```

## Prerequisite
- [BscScan API Key](https://bscscan.com/myapikey)
  `export bscscan_api_key=<API_KEY>`

## Installation
`pip install defy`

## Support Platforms

| Platform  | Features | Support |
|-----------|----------|---------|
| DefiValue | vSafe    |   ✅   |

## Support Networks

| Network  | Support |
|-----------|---------|
| BSC Mainnet |  ✅   |

## Commands

### `defy --address <ADDRESS>`

```
USAGE
  $ defy

OPTIONS
  -a,   --address <ADDRESS>   wallet address
  -h,   --help                show help menu
  -hsb, --hide-small-bal      hide token which has small balance
```