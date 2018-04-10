================================================================================
openvpn-status-zabbix - Parse OpenVPN status logs in Python for Zabbix with LLD
================================================================================


What is this?
*************
``openvpn-status-zabbix`` provides an executable called ``openvpn-client-lld``.

Installation
************
*on most UNIX-like systems, you'll probably need to run the following
`install` commands as root or by using sudo*

**from source**

::

  pip install git+http://github.com/verdel/openvpn-status-zabbix

**or**

::

  git clone git://github.com/verdel/openvpn-status-zabbix.git
  cd openvpn-status-zabbix
  python setup.py install

as a result, the ``openvpn-client-lld`` executable will be installed into a
system ``bin`` directory

Usage
-----
::

    openvpn-client-lld --help
    usage: openvpn-client-lld [-h] (-l | -m) [-i ID] -f FILE

    Openvpn client zabbix exporter

    optional arguments:
      -h, --help            show this help message and exit
      -l, --lld             export information for Zabbix LLD
      -m, --metric          export metric information by openvpn user id
      -i ID, --id ID        openvpn user id
      -f FILE, --file FILE  input file with openvpn status
