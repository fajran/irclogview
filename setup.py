from setuptools import setup, find_packages

packages = ['irclogview']

setup(
    name = 'irclogview',
    version = '0.1',
    url = 'https://github.com/fajran/irclogview',
    description = 'IRC Log viewer for Django',
    author = 'Fajran Iman Rusadi',
    packages = packages,
    install_requires = ['setuptools']
)

