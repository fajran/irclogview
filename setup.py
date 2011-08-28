from setuptools import setup, find_packages

packages = ['irclogview',
            'irclogview.management',
            'irclogview.management.commands']

setup(
    name = 'irclogview',
    version = '0.1',
    url = 'https://github.com/fajran/irclogview',
    license = 'AGPL 3.0',
    description = 'IRC Log viewer for Django',
    author = 'Fajran Iman Rusadi',
    packages = packages,
    install_requires = ['setuptools', 'django-picklefield']
)

