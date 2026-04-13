---
title: Docker, KVM and iptables
url: https://anteru.net/blog/2017/docker-kvm-iptables
published: '2017-09-09'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

A quick blog post as I’ve been recently setting up a server with [KVM](https://en.wikipedia.org/wiki/Kernel-based_Virtual_Machine) and [docker](http://docker.com/). If you’re using a bridge interface to have your VMs talk to your network, you might notice that after a docker installation, your VMs have suddenly no connection. So what is going on?

It turns out, docker adds a bunch of `iptables`

rules by default which prevent communication. These will interfere with an already existing bridge, and suddenly your VMs will report no network. There are two ways to solve it:

- Add a new rule for your bridge.
- Stop docker from adding iptables rules.

I’m assuming Ubuntu 17.04 for the commands below; they should be similar on any Debian based system.

## Solution 1: Add a new rule

In my case, my bridge is called `br0`

. docker changes the default for
`FORWARD`

from accept to drop, and adds a few exceptions for itself.
Adding a new forward rule for `br0`

will allow your bridge (and the
devices) behind it to get back into your network and not get dropped:

```
iptables -A FORWARD -i br0 -o br0 -j ACCEPT
```


Unfortunately, this won’t be persistent – you’ll need the `iptables-persistent`

package on Linux to make it persistent, plus some extra setup. It’s good for a quick test though! ([Source](https://forums.fedoraforum.org/showthread.php?t=312824))

## Solution 2: Stop docker

In my case, the server is not on the public internet, and I’ve got no need for the extra security. It turns out that the docker service adds the rules on startup, unless `--iptables=false`

is used. This can be either added to the default docker configuration, or, slightly cleaner in my opinion, to the `daemon.json`

configuration file (see the [documentation](https://docs.docker.com/engine/reference/commandline/dockerd/) for all options). Create a file `/etc/docker/daemon.json`

with the following contents:

```
{
"iptables" : false
}
```


That’ll stop docker from adding new rules, and everything will work as it did before.