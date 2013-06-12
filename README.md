logster-parsers
===============

Log file parsers for etsy's logster.


Overview
--------
Logster is a project for following log files and extracting useful data from them.  This project contains log file parsers for logster that provide the ability to handle new types of log file format.

Prerequisites
-------------
* The `logtail` program (see logster project for details)


Installation
------------
Clone the `parsers` directory into the _site-packages_ directory of your local Python 2.6+ installation or virtualenv, or anywhere where logster's `sys.path` can see it.


```
# Basic invocation - print dnsmasq DHCP statistics
$ logster --output=stdout parsers.dnsmasq.DHCP /var/log/syslog
> 1371007459 discover 0
> 1371007459 offer 0
> 1371007459 request 0
> 1371007459 ack 0
> 1371007459 nack 0

# More advanced - send them to Graphite
$ logster --output=graphite --graphite-host=graphite:2003 parsers.dnsmasq.DHCP /var/log/syslog

# ...or generate Graphite-formatted metrics on STDOUT
$ logster --output=stdout parsers.dnsmasq.DHCP /var/log/syslog | awk '{print $2 " " $3 " " $1}'
> discover 0 1371007488
> offer 0 1371007488
> request 0 1371007488
> ack 0 1371007488
> nack 0 1371007488

# ...with a prefix
logster -p services.dnsmasq.dhcp.dhcp --output=stdout parsers.dnsmasq.DHCP /var/log/syslog | awk '{print $2 " " $3 " " $1}'
> services.dnsmasq.dhcp.dhcp_discover 0 1371007511
> services.dnsmasq.dhcp.dhcp_offer 0 1371007511
> services.dnsmasq.dhcp.dhcp_request 0 1371007511
> services.dnsmasq.dhcp.dhcp_ack 0 1371007511
> services.dnsmasq.dhcp.dhcp_nack 0 1371007511


# ...then pipe it to Graphite for fun, profit
$ logster -p services.dnsmasq.dhcp.dhcp --output=stdout parsers.dnsmasq.DHCP /var/log/syslog | awk '{print $2 " " $3 " " $1}' | nc graphite 2003

```

See Also
--------
* Etsy's Logster Project: https://github.com/etsy/logster
