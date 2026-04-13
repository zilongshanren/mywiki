---
title: Enabling SSL in your local network
url: https://anteru.net/blog/2020/enabling-ssl-in-your-local-network
published: '2020-05-17'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

If you’re running a network, you’re probably having quite a few services which would love to default to SSL and present you with self-signed certificates. Sure, with enough persistance it possible to become your own certificate authority and push your local certificate to all devices in your local network to get proper SSL working. There is however a much better way: What if you can use a proper SSL certificate in your local network? Turns out, for the cost of a domain, you can do exactly that. In this blog post, we’ll take a look at how.

Please keep in mind that local network here can be your company network as well. Of course if all you have in your network is one lone printer, then feel free to skip this post :) But if you have a network with several machines, and Wi-Fi, it makes sense to add another protection layer (more so as an attacker can spend basically infinite time trying to hack your Wi-Fi). Various large companies moved or a moving to a zero trust environment, in which being on the network does not grant you any additional privileges (see for instance [Google’s BeyondCorp](https://en.wikipedia.org/wiki/BeyondCorp)).

## Prerequisites

This setup requires a few prerequisites – and while you can do it differently, here’s my recommendation:

- First, you need a domain from a DNS provider who supports changing DNS entries via an API. If you have no idea where to start, check the list of DNS providers supported by
[lexicon](https://github.com/AnalogJ/lexicon) - You need a local DHCP server which can set a local network domain. If in doubt, you can use
[Pi-hole](https://pi-hole.net) - You need a server which can call the DNS API once in a while. This server
*does*not have to be reachable from the internet. A Raspberry Pi running in your local network will do fine (and you can run Pi-hole on it.)

## What we’re going to do

With that setup in place, this is what we’re going to do:

- We’ll get a Let’s Encrypt wildcard certificate for our domain
- We’ll put all devices in our local network into that domain
- We’ll distribute the certificate to all servers/services that need it

How does this work? It’s fairly easy: If you own the domain `home.cloud`

, and you obtain a certificate for `*.home.cloud`

, then your browser will accept that certificate as long as the URL resolves correctly. Meaning: If you have a server named `icarus`

, and you can reach it via `icarus.home.cloud`

, then it’s covered by a `*.home.cloud`

certificate. There’s no need for the server to be reachable from the internet or that URL to resolve to any host from *outside* of your network. Specifically, `icarus.home.cloud`

does not have to be reachable *from* the internet, and it does not have to be a public DNS name.

Armed with this knowledge, the steps are fairly easy. In this example, I’ll assume the domain you obtained is called `home.cloud`

. First, we need to get a [Let’s Encrypt](https://letsencrypt.org/) wildcard certificate for it. That’s fairly easy if you can manipulate the DNS using an API, as a wildcard certificate only requires you to put a new [TXT record](https://en.wikipedia.org/wiki/TXT_record) and have it there for a few seconds.

To simplify setting up a cron job, I’m going to use [dehydrated](https://dehydrated.io/) – it comes as a package on Debian/Ubuntu, so it’s literally trivial to set up. In my case, my DNS provider is not supported by `lexicon`

, so I had to write my own script for it – don’t be surprised I’m using a custom script name. The way `dehydrated`

works is that it expects a bash script with hooks. Copy `/usr/share/doc/dehydrated/examples/hook.sh`

to `/etc/dehydrated/hook.sh`

, and edit the first two hook functions as following:

```
#!/usr/bin/env bash
export DNS_AUTH_TOKEN="you can set env variables"
export DNS_ZONE_ID="as needed, as only root can see this"
deploy_challenge() {
local DOMAIN="${1}" TOKEN_FILENAME="${2}" TOKEN_VALUE="${3}" TLD_DOMAIN=$(tld_domain $DOMAIN)
dns-helper.py create ${TLD_DOMAIN} TXT --name="_acme-challenge" --content="$TOKEN_VALUE"
}
clean_challenge() {
local DOMAIN="${1}" TOKEN_FILENAME="${2}" TOKEN_VALUE="${3}" TLD_DOMAIN=$(tld_domain $DOMAIN)
dns-helper.py delete ${TLD_DOMAIN} TXT --name="_acme-challenge"
}
# ... rest of the original hook.sh
```


`dns-helper.py`

is my own script; I’ve kept the command line syntax compatible with `lexicon`

, which is probably what you want to use. We only care about two hooks here: The one to create the challenge (which requires us to put a `TXT`

record), and the cleanup. Feel free to fill the remaining ones with some logging so you know if this worked or not!

With this in place, you need to actually hook this up. First, we need to register the domain. Add this to `/etc/dehydrated/domains.txt`

:

```
*.home.cloud > star_home_cloud
```


In `/etc/dehydrated/config`

, there should be an entry `DOMAINS_TXT`

pointing to that file, if not, add it. Ok, nearly done, the last this we need to do is to register our hooks. On Debian based systems, use `/etc/dehydrated/conf.d/01-config.sh`

for that. In my case, it contains:

```
HOOK=/etc/dehydrated/hook.sh
CHALLENGETYPE="dns-01"
CONTACT_EMAIL=secret@example.org
```


The next thing you need is a cron job to run this. For now you can start `dehydrated`

directly from the console, for a cron job you’ll want to use `dehydrated -c`

. Your cert will then show up in `/var/lib/dehydrated/certs/star_home_cloud/`

. There will be two files: `fullchain.pem`

and `privkey.pem`

. Those are the certificates you’re looking for, which you can now distribute to whatever service in your network needs one!

Of course your machines must be reachable under `hostname.home.cloud`

for this to work. If you’re using Pi-hole, this is easy to do: In your settings, under `DHCP`

, set the `Pi-hole domain name`

to `home.cloud`

. That should do the trick! Make sure you can ping the desired endpoint using the fully qualified name, i.e. if you want to talk to `icarus`

, you’d try to ping `icarus.home.cloud`

.

## Example use

In this blog post, we’ll use it for [cockpit](https://cockpit-project.org/) and [dovecot](https://www.dovecot.org/). Unlike NGINX, which expects a private/public key in separate files (so you can copy them directly), cockpit requires everything to be in one file in `/etc/cockpit/ws-certs/`

. In my case, I run a cron job which simply does `cat /var/lib/dehydrated/certs/star_home_cloud/* > /etc/cockpit/ws-certs.d/1-letsencrypt.cert`

. For dovecot the configuration is trivial – you can simply symlink `privkey.pem`

to `/etc/dovecot/private/dovecot.key`

and `fullchain.pem`

to `/etc/dovecot/private/dovecot.pem`

, and you’re all set.

And with that, cockpit is happy, and I have SSL working at home without having to deal with self-signed certificates and having to convince all devices at home to accept it. Hope this guide is helpful for you as well!