---
title: 'Allar''s Dev Diary #5: Public LAN Port Scanner'
url: https://allarsblog.com/2010/05/04/allars-dev-diary-5-public-lan-port-scanner/
author: Michael Allar
published: '2010-05-04'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

Yup. Its a quick and dirty LAN port scanner. If you need one binded into UnrealScript, here you go, if not, move along.

With the binded DLL, you can scan your network for any open ports, given the port to hunt for.

If your game server is on port 7777 (which is what I use, you can set this by the ?port=7777 option on your servers command line or in your config files by Port=7777) and you do a lan scan on port 7777, it will find your server and store its IP address in an array of IPs that will also contain any other game servers on port 7777 on your same subnet mask.

Because it essentially is just a port scanner, it doesn't do anything fancy, and can create false positives if you have another service on the same port responding to udp communication.

Hopefully the included documentation within the code and the video below will be enough for you to use it.

I will be releasing more and more features for it when it becomes more and more refined and awesome.

**Download here. If you would like to link to these files, please link to this page and not the files directly.**

[download id="1"]

[download id="2"]