---
title: Changing XP from retail to OEM ...
url: https://anteru.net/blog/2010/changing-xp-from-retail-to-oem
published: '2010-01-18'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Just recently I had to fix a PC with Windows XP. It turned out that the installed version was not “genuine”. Du’h, someone helpful re-installed Windows on the machine, but instead of using the original OEM which came with the PC, he installed a retail XP with some key which was obviously invalid. I tried to change the product key to the valid one on the notebook (the one on the Windows sticker with the nice hologram), but the [normal way to change keys](http://support.microsoft.com/kb/328874) refused it. Bummer. Called Microsoft, and it turned out that it’s an OEM key and the current Windows is not OEM (if you want to check, go to the control panel, system. If your system id is <....>-OEM, you’re on OEM)

Ok, so I had to change the XP version from retail to OEM, and then change the key somehow. Turns out that changing the XP version requires a reinstall – at least that’s what I was told by the Windows activation hotline operator. However, there is a different way, by using [a tool from Microsoft to change the product key](http://windows.microsoft.com/en-US/windows/help/genuine/product-key#T1=tab03). Guess what, this tool was able to change the product key **and** the product version at the same time. Voilà , I had finally an OEM windows with a valid key, and could go ahead to install *lots* of updates as well as other tools that require a valid key like the pretty decent [security essentials](https://support.microsoft.com/en-us/help/14210/security-essentials-download).

Machine is half-way fixed again; and I still wonder why computer science graduates are supposed to be good at troubleshooting Windows issues … and I’m always amazed how much crap people tend to install on their machines. Some good advice: If you install some stuff off the web, and you don’t use it/know what it is any more, remove it! And please try to keep your updates on; the machine in question had Firefox 2 and Adobe Reader 8, as well as a 4 year-old antivirus program. That’s basically a sure way to become a victim of some exploit.

So much for now, next week we’ll take a look at stupid WLAN drivers on Linux and WPA-PSK keys getting refused.

**Update**: 2014-10-27: Updated the tool link, thanks to Costi for reporting!

**Update**: 2017-09-09: Updated the link to Microsoft Security essentials, thanks to Jeff for reporting!