---
title: Using the commandline network utilities from Emacs
url: https://www.masteringemacs.org/article/network-utilities-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Unbeknownst to many, Emacs comes with a full suite of wrappers around the common GNU network utilities.

Most of the utilities are just simple wrappers around their command-line equivalents, but in full technicolor; but some – like the `nslookup`

support – also adds full Emacs `comint`

support.

Another useful feature is the built-in `ffap`

support (it means *find file at point*) and it will try to determine if the point is – if used interactively with the net utils below – on a hostname or IP and default to that.

The net utils library were written with the GNU libraries in mind, so Windows users may find the support a bit lacking. But you can always download the Win32 ports.

Here’s a list of utilities Emacs supports; invoke with `M-x`

. You may have to configure them to your liking, and you can do that by invoking `M-x customize-group RET net-utils RET`

.

`ifconfig`

and`ipconfig`

Runs

`ifconfig`

or`ipconfig`

`iwconfig`

Runs the

`iwconfig`

tool`netstat`

Runs the

`netstat`

tool`arp`

Runs the

`arp`

tool`route`

Runs the

`route`

tool`traceroute`

Runs the

`traceroute`

tool`ping`

Runs

`ping`

, but on most systems it may run indefinitely; adjust`ping-program-options`

.`nslookup-host`

Runs

`nslookup`

in non-interactive mode.`nslookup`

Runs

`nslookup`

in interactive mode in Emacs as an inferior process`dns-lookup-host`

Look up the DNS information for an IP or host using

`host`

.`run-dig`

and`dig`

Invokes the

`dig`

in interactive mode as an inferior process`ftp`

Very simple wrapper around the commandline tool

`ftp`

. You are probably better off with TRAMP for all but low-level system administration.`smbclient`

and`smbclient-list-shares`

Runs

`smbclient`

as an inferior process or list a hosts’ shares.`finger`

Runs the

`finger`

tool`whois`

and`whois-reverse-lookup`

Runs the

`whois`

tool but tries to guess the correct WHOIS server. You may have to tweak`whois-server-tld`

and`whois-server-list`

or set`whois-guess-server`

to`nil`