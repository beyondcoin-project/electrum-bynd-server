Note
====

This code is now unmaintained. The replacement code for electrum
server is ElectrumX: https://github.com/kyuupichan/electrumx

How to run your own Electrum server
===================================

Abstract
--------

This document is an easy to follow guide to installing and running your own
Electrum server on Linux. It is structured as a series of steps you need to
follow, ordered in the most logical way. The next two sections describe some
conventions we use in this document and the hardware, software, and expertise
requirements.

The most up-to date version of this document is available at:

    https://github.com/pooler/electrum-ltc-server/blob/master/HOWTO.md

Conventions
-----------

In this document, lines starting with a hash sign (#) or a dollar sign ($)
contain commands. Commands starting with a hash should be run as root,
commands starting with a dollar should be run as a normal user (in this
document, we assume that user is called 'beyondcoin'). We also assume the
beyondcoin user has sudo rights, so we use `$ sudo command` when we need to.

Strings that are surrounded by "lower than" and "greater than" ( < and > )
should be replaced by the user with something appropriate. For example,
\<password\> should be replaced by a password. Do not confuse this
notation with shell redirection (`command < file` or `command > file`)!

Lines that lack hash or dollar signs are pastes from config files. They
should be copied verbatim or adapted without the indentation tab.

`apt-get install` commands are suggestions for required dependencies.
They conform to an Ubuntu 15.10 system but may well work with Debian
or other versions of Ubuntu.

Prerequisites
-------------

**Expertise.** You should be familiar with Linux command line and
standard Linux commands. You should have a basic understanding of git
and Python packages. You should have knowledge about how to install and
configure software on your Linux distribution. You should be able to
add commands to your distribution's startup scripts. If one of the
commands included in this document is not available or does not
perform the operation described here, you are expected to fix the
issue so you can continue following this howto.

**Software.** A recent Linux 64-bit distribution with the following software
installed: `python`, `easy_install`, `git`, standard C/C++
build chain. You will need root access in order to install other software or
Python libraries. Python 2.7 is the minimum supported version.

**Hardware.** The lightest setup is a pruning server with disk space
requirements of about 5 GB for the Electrum database (January 2017). However note that
you also need to run beyondcoind and keep a copy of the full blockchain,
which is roughly 7 GB (January 2017). Ideally you have a machine with 4 GB of RAM
and an equal amount of swap. If you have ~2 GB of RAM make sure you limit beyondcoind 
to 8 concurrent connections by disabling incoming connections. electrum-bynd-server may
bail-out on you from time to time with less than 2 GB of RAM, so you might have to 
monitor the process and restart it. You can tweak cache sizes in the config to an extend
but most RAM will be used to process blocks and catch-up on initial start.

CPU speed is less important than fast I/O speed. electrum-bynd-server makes use of one core 
only leaving spare cycles for beyondcoind. Fast single core CPU power helps for the initial 
block chain import. Any multi-core x86 CPU with CPU Mark / PassMark > 1500 will work
(see https://www.cpubenchmark.net/). An ideal setup in February 2016 has 4 GB+ RAM and
SSD for good i/o speed.

Instructions
------------

### Step 1. Create a user for running beyondcoind and Electrum server

This step is optional, but for better security and resource separation I
suggest you create a separate user just for running `beyondcoind` and Electrum.
We will also use the `~/bin` directory to keep locally installed files
(others might want to use `/usr/local/bin` instead). We will download source
code files to the `~/src` directory.

    $ sudo adduser beyondcoin --disabled-password
    $ sudo apt-get install git
    $ sudo su - beyondcoin
    $ mkdir ~/bin ~/src
    $ echo $PATH

If you don't see `/home/beyondcoin/bin` in the output, you should add this line
to your `.bashrc`, `.profile`, or `.bash_profile`, then logout and relogin:

    PATH="$HOME/bin:$PATH"
    $ exit

### Step 2. Download beyondcoind

We currently recommend beyondcoin core 0.16 stable.

If you prefer to compile beyondcoind yourself, here are some pointers for Ubuntu:

    $ sudo apt-get install automake make bsdmainutils g++ python-leveldb libboost-all-dev libssl-dev libdb++-dev pkg-config libevent-dev
    $ sudo su - beyondcoin
    $ cd ~/src && git clone https://github.com/beyondcoin-project/beyondcoin.git -b master
    $ cd beyondcoin
    $ git checkout v0.16
    $ ./autogen.sh
    $ ./configure --disable-wallet --without-miniupnpc
    $ make
    $ strip src/beyondcoind src/beyondcoin-cli src/beyondcoin-tx
    $ cp -a src/beyondcoind src/beyondcoin-cli src/beyondcoin-tx ~/bin

### Step 3. Configure and start beyondcoind

In order to allow Electrum to "talk" to `beyondcoind`, we need to set up an RPC
username and password for `beyondcoind`. We will then start `beyondcoind` and
wait for it to complete downloading the blockchain.

    $ mkdir ~/.beyondcoin
    $ $EDITOR ~/.beyondcoin/beyondcoin.conf

Write this in `beyondcoin.conf`:

    daemon=1
    txindex=1
    disablewallet=1

rpcuser / rpcpassword options are only needed for non-localhost connections.
you can consider setting maxconnections if you want to reduce beyondcoind bandwidth
(as stated above)

If you have an existing installation of beyondcoind and have not previously
set txindex=1 you need to reindex the blockchain by running

    $ beyondcoind -reindex

If you already have a freshly indexed copy of the blockchain with txindex start `beyondcoind`:

    $ beyondcoind

Allow some time to pass, so `beyondcoind` connects to the network and starts
downloading blocks. You can check its progress by running:

    $ beyondcoin-cli getinfo

Before starting the Electrum server your beyondcoind should have processed all
blocks and caught up to the current height of the network (not just the headers).
You should also set up your system to automatically start beyondcoind at boot
time, running as the 'beyondcoin' user. Check your system documentation to
find out the best way to do this.

### Step 4. Download and install Electrum server

We will download the latest git snapshot for Electrum to configure and install it:

    $ cd ~
    $ git clone https://github.com/beyondcoin-project/electrum-bynd-server.git
    $ cd electrum-bynd-server
    $ sudo apt-get install python-setuptools
    $ sudo ./configure
    $ sudo python setup.py install

See the INSTALL file for more information about the configure and install commands.

### Optional Step 5: Install Electrum dependencies manually

Electrum server depends on various standard Python libraries and leveldb. These will usually be
installed by calling `python setup.py install` above. They can be also be installed with your
package manager if you don't want to use the install routine.

    $ sudo apt-get install python-setuptools python-openssl python-leveldb libleveldb-dev
    $ sudo easy_install jsonrpclib irc plyvel

For the python irc module please note electrum-server currently only supports versions between 11 and 14.0. 
The setup.py takes care of installing a supported version but be aware of it when installing or upgrading
manually.

Regarding leveldb, see the steps in README.leveldb for further details, especially if your system
doesn't have the python-leveldb package or if plyvel installation fails.

leveldb should be at least version 1.9.0. Earlier version are believed to be buggy.

### Step 6. Select your limit

Electrum server uses leveldb to store transactions. You can choose
how many spent transactions per address you want to store on the server.
The default is 100, but there are also servers with 1000 or even 10000.
Few addresses have more than 10000 transactions. A limit this high
can be considered equivalent to a "full" server. Full servers previously
used abe to store the blockchain. The use of abe for electrum servers is now
deprecated.

The pruning server uses leveldb and keeps a smaller and
faster database by pruning spent transactions. It's a lot quicker to get up
and running and requires less maintenance and disk space than abe.

The section in the electrum server configuration file (see step 10) looks like this:

     [leveldb]
     path = /path/to/your/database
     # for each address, history will be pruned if it is longer than this limit
     pruning_limit = 100

### Step 7. Import blockchain into the database or download it

It's recommended that you fetch a pre-processed leveldb from the net.
The "configure" script above will offer you to download a database with pruning limit 100.

You can fetch recent copies of electrum leveldb databases with different pruning limits
and further instructions from the Electrum-BYND full archival server foundry at:
http://foundry.electrum-bynd.com/leveldb-dump/


Alternatively, if you have the time and nerve, you can import the blockchain yourself.

As of April 2014 it takes between one and two days to import 500k blocks, depending
on CPU speed, I/O speed, and your selected pruning limit.

It's considerably faster and strongly recommended to index in memory. You can use /dev/shm or
or create a tmpfs which will also use swap if you run out of memory:

    $ sudo mount -t tmpfs -o rw,nodev,nosuid,noatime,size=15000M,mode=0777 none /tmpfs

If you use tmpfs make sure you have enough RAM and swap to cover the size. If you only have 2 GB of
RAM but add 15 GB of swap from a file that's fine too; tmpfs is smart enough to swap out the least
used parts. It's fine to use a file on an SSD for swap in this case.

It's not recommended to do initial indexing of the database on a SSD because the indexing process
does at least 10 TB (!) of disk writes and puts considerable wear-and-tear on an SSD. It's a lot better
to use tmpfs and just swap out to disk when necessary.   

Databases have grown to roughly 5 GB as of February 2016. Leveldb prunes the database from time to time,
so it's not uncommon to see databases ~50% larger at times when it's writing a lot, especially when
indexing from the beginning.


### Step 8. Create a self-signed SSL cert

[Note: SSL certificates signed by a CA are supported by 2.0 clients.]

To run SSL / HTTPS you need to generate a self-signed certificate using openssl.
You could just comment out the SSL / HTTPS ports in the config and run
without, but this is not recommended.

Use the sample code below to create a self-signed cert with a recommended validity
of 5 years. You may supply any information for your sign request to identify your server.
They are not currently checked by the client except for the validity date.
When asked for a challenge password just leave it empty and press enter.

    $ openssl genrsa -des3 -passout pass:x -out server.pass.key 2048
    $ openssl rsa -passin pass:x -in server.pass.key -out server.key
    writing RSA key
    $ rm server.pass.key
    $ openssl req -new -key server.key -out server.csr
    ...
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:California
    Common Name (eg, YOUR name) []: electrum-server.tld
    ...
    A challenge password []:
    ...

    $ openssl x509 -req -days 1825 -in server.csr -signkey server.key -out server.crt

The server.crt file is your certificate suitable for the `ssl_certfile=` parameter and
server.key corresponds to `ssl_keyfile=` in your Electrum server config.

Starting with Electrum 1.9, the client will learn and locally cache the SSL certificate
for your server upon the first request to prevent man-in-the middle attacks for all
further connections.

If your certificate is lost or expires on the server side, you will need to run
your server with a different server name and a new certificate.
Therefore it's a good idea to make an offline backup copy of your certificate and key
in case you need to restore them.

### Step 9. Configure Electrum server

Electrum reads a config file (/etc/electrum-bynd.conf) when starting up. This
file includes the database setup, beyondcoind RPC setup, and a few other
options.

The "configure" script listed above will create a config file at /etc/electrum-bynd.conf
which you can edit to modify the settings.

Go through the config options and set them to your liking.
If you intend to run the server publicly have a look at README-IRC.md

### Step 10. Tweak your system for running electrum

Electrum server currently needs quite a few file handles to use leveldb. It also requires
file handles for each connection made to the server. It's good practice to increase the
open files limit to 128k.

The "configure" script will take care of this and ask you to create a user for running electrum-bynd-server.
If you're using the user `beyondcoin` to run electrum and have added it as shown in this document, run
the following code to add the limits to your /etc/security/limits.conf:

     echo "beyondcoin hard nofile 131072" >> /etc/security/limits.conf
     echo "beyondcoin soft nofile 131072" >> /etc/security/limits.conf

If you are on Debian > 8.0 Jessie or another distribution based on it, you also need to add these lines in /etc/pam.d/common-session and /etc/pam.d/common-session-noninteractive otherwise the limits in /etc/security/limits.conf will not work:

    echo "session required pam_limits.so" >> /etc/pam.d/common-session
    echo "session required pam_limits.so" >> /etc/pam.d/common-session-noninteractive

Check if the limits are changed either by logging with the user configured to run Electrum server as. Example:

    su - beyondcoin
    ulimit -n

Or if you use sudo and the user is added to sudoers group:

    sudo -u beyondcoin -i ulimit -n


Two more things for you to consider:

1. To increase privacy of transactions going through your server
   you may want to close beyondcoind for incoming connections and connect outbound only. Most servers do run
   full nodes with open incoming connections though.

2. Consider restarting beyondcoind (together with electrum-bynd-server) on a weekly basis to clear out unconfirmed
   transactions from the local the memory pool which did not propagate over the network.

### Step 11. (Finally!) Run Electrum server

The magic moment has come: you can now start your Electrum server as root (it will su to your unprivileged user):

    # electrum-bynd-server start

Note: If you want to run the server without installing it on your system, just run 'run_electrum_bynd_server" as the
unprivileged user.

You should see this in the log file:

    starting Electrum server

If your blockchain database is out of date Electrum Server will start updating it. You will see something similar to this in the log file:

    [09/02/2016-09:58:18] block 397319 (1727 197.37s) 0290aae5dc6395e2c60e8b2c9e48a7ee246cad7d0630d17dd5b54d70a41ffed7 (10.13tx/s, 139.78s/block) (eta 11.5 hours, 240 blocks)
    
The important pieces to you are at the end. In this example, the server has to calculate 240 more blocks, with an ETA of 11.5 hours. Multiple entries will appear below this one as the server catches back up to the latest block. During this time the server will not accept incoming connections from clients or connect to the IRC channel.

If you want to stop Electrum server, use the 'stop' command:

    # electrum-bynd-server stop


If your system supports it, you may add electrum-bynd-server to the /etc/init.d directory.
This will ensure that the server is started and stopped automatically, and that the database is closed
safely whenever your machine is rebooted.

    # ln -s `which electrum-bynd-server` /etc/init.d/electrum-bynd-server
    # update-rc.d electrum-bynd-server defaults

### Step 12. Test the Electrum server

We will assume you have a working Electrum client, a wallet, and some
transaction history. You should start the client and click on the green
checkmark (last button on the right of the status bar) to open the Server
selection window. If your server is public, you should see it in the list
and you can select it. If you server is private, you need to enter its IP
or hostname and the port. Press 'Ok' and the client will disconnect from the
current server and connect to your new Electrum server. You should see your
addresses and transactions history. You can see the number of blocks and
response time in the server selection window. You should send/receive some
beyondcoins to confirm that everything is working properly.
