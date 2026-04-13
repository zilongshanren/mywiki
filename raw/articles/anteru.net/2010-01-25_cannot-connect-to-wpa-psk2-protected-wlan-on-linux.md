---
title: Cannot connect to WPA-PSK2 protected WLAN on Linux ...
url: https://anteru.net/blog/2010/cannot-connect-to-wpa-psk2-protected-wlan-on-linux
published: '2010-01-25'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

The title says it all. I had a machine here with a really old WLAN adapter (Realtek RTL-8185L on a PCMCIA card), and it wouldn’t connect to my local WLAN when using WPA-PSK2. I just checked that WLAN was working at all, and yes, it would connect without a pass-phrase, but with a key, it wouldn’t work. Each time, the authentication would simply fail due to a wrong password. The Linux was Ubuntu 9.10, but I guess it’ll be the same on other ones as well.

One weird issue was that the GNOME applet for entering the network key would refuse my 63 character key, and only let my type in 60 characters. Turns out that the problem is that for WPA-PSK, the key required to authenticate is not your pass-phrase, but generated from the pass-phrase and the SSID, and some drivers don’t do this transformation for you, so you have to help out by hand. That’s very easy, for instance by using [wpa_passphrase](http://linux.die.net/man/8/wpa_passphrase). This gives you the PSK, and on entering this one instead of the pass-phrase, everything worked right away. Woho!