from setuptools import setup

setup(
    name="electrum-bynd-server",
    version="1.0",
    scripts=['run_electrum_bynd_server.py','electrum-bynd-server'],
    install_requires=['plyvel','jsonrpclib', 'irc >= 11, <=14.0'],
    package_dir={
        'electrumbyndserver':'src'
        },
    py_modules=[
        'electrumbyndserver.__init__',
        'electrumbyndserver.utils',
        'electrumbyndserver.storage',
        'electrumbyndserver.deserialize',
        'electrumbyndserver.networks',
        'electrumbyndserver.blockchain_processor',
        'electrumbyndserver.server_processor',
        'electrumbyndserver.processor',
        'electrumbyndserver.version',
        'electrumbyndserver.ircthread',
        'electrumbyndserver.stratum_tcp'
    ],
    description="Beyondcoin Electrum Server",
    author="Thomas Voegtlin",
    author_email="thomasv@electrum.org",
    license="MIT Licence",
    url="https://github.com/beyondcoin-project/electrum-bynd-server/",
    long_description="""Server for the Electrum Lightweight Beyondcoin Wallet"""
)
