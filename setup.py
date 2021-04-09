import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "defy",
    version = "0.0.0",
    author = "Parin Kobboon",
    author_email = "punparin@gmail.com",
    description = "A command line tool to lookup balance on blockchain network",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/punparin/defy-cli",
    packages = setuptools.find_packages(),
    install_requires = [
        'click==7.1.2',
        'configparser==5.0.2',
        'requests==2.25.1',
        'tabulate==0.8.9',
        'web3==5.17.0',
        "python-binance==0.7.9",
        "pytest==6.2.3"
        ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': [
            'defy=defy.cli:cli',
        ],
    },
    python_requires = '>=3.6',
)