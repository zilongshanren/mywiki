---
title: Fixing network after Ubuntu 19.04 to 19.10 upgrade
url: https://anteru.net/blog/2019/fixing-network-after-ubuntu-19-04-to-19-10-upgrade
published: '2019-10-26'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I updated my server from Ubuntu 19.04 to 19.10 recently, and ran into a rather curious issue: My virtual machines connected to the network bridge would continue to work fine, and I could connect to the host via SSH as well, but any kind of DNS lookup *on the host* would fail. I.e. you’d run `nslookup anteru.net`

and you’d get a `SERVFAIL`

response. After you manually restarted the resolver using `systemctl restart systemd-resolved`

, things would immediately work again on the host. I’ve been poking around without much luck and eventually turned to [askubuntu.com](https://askubuntu.com/questions/1183312/dns-resolve-stopped-working-after-19-10-update). That paid off big time – I did get the right hint there to solve my issue, which is: Migrate to [netplan](https://netplan.io)!

The original guide linked is a bit shy on how to do it properly and how we ended up here in the first place, so here’s the long version: Before Ubuntu 18.04, you’d manage your network using `/etc/network/interfaces`

and `ifupdown`

. Additionally, the DNS resolver was configured using `resolveconf`

. Since 18.04, Ubuntu server uses `systemd-networkd`

for network setup, and to ease the configuration, `netplan`

is used to create configuration files (and `systemd-resolved`

is taking care of resolving.) You’ll be wondering what this `netplan`

thing is good for: It’s a unified way to create configurations for both `systemd-networkd`

and `NetworkManager`

, the latter being most likely what you’re using on your desktop.

With that information at hand, our goal is clear – move to `systemd-networkd`

and `netplan`

manually. This is fairly simple now that we know what we’re doing. I’ll recommend using some kind of console access to do this, as I had the network disconnect me over SSH.

Let’s start by writing the `netplan`

configuration. This is pretty much a 1:1 port of your `/etc/network/interfaces`

file. What I needed was a bridge (there’s a simple example of how to use it) and I wanted to set the [forward delay parameter](https://netplan.io/reference#properties-for-device-type-bridges) on it. I stuffed this into `/etc/netplan/01-config.yaml`

:

```
network:
version: 2
renderer: networkd
ethernets:
eno1:
dhcp4: no
dhcp6: no
bridges:
br0:
interfaces: [eno1]
dhcp4: yes
dhcp6: yes
parameters:
forward-delay: 5
```


We’re nearly done here. After a quick `netplan try`

to make sure the config is valid, let’s run `netplan apply`

to generate the configuration files. From here on, the network should be configured correctly. The only remaining bit is to remove things we don’t need:

`apt remove --purge ifupdown resolveconf`

– no longer needed, and`--purge`

makes sure we remove all related configuration files.`systemctl stop NetworkManager && systemctl disable NetworkManager`

– we’re using`systemd-networkd`

, so no need for`NetworkManager`

to stick around.`rm /etc/network/interfaces`

just in case they’re still floating around

And that’s it – your server should be working again, without having to reinstall from scratch!