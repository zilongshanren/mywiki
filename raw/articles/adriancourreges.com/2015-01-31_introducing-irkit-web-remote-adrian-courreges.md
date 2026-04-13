---
title: Introducing IRKit Web Remote - Adrian Courrèges
url: http://www.adriancourreges.com/blog/2015/01/31/introducing-irkit-web-remote/
author: Adrian Courrèges
published: '2015-01-31'
source_blog: Adrian Courrèges
source_site: http://www.adriancourreges.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/cf7bc9eaf1a8ca4d.png)


I [previously wrote](http://www.adriancourreges.com/blog/2015/01/24/irkit-setup-guide-for-android-ios-linux-mac-windows/) about the [IRKit device](http://getirkit.com/) and how to set it up from a basic webpage.

The setup guide was handy as a proof of concept, but I was still lacking a way to organize efficiently all the IR commands I recorded from various remote controls.

So here comes [IRKit Web Remote](http://www.adriancourreges.com/projects/irkit-web-remote/): a web-solution to control and dispatch commands from a web-browser.

I host it on a small Raspberry Pi so anybody in the family can just fire-up a browser on the phone, open the page and send commands.

Having everything centralized on the server is really useful when I need to add new commands: I simply update the web page on
the server and I don’t have to care about maintaining clients one by one, clients will get the latest features upon the next page reload.

A few features of IRKit Web Remote:

- supports sending one single command or a
*series*of command (with custom delays between each) - command buffer to avoid overloading IRKit, with current queue visual feedback. Queue is also cancellable.
- any size of screen supported thanks to the responsive design of Bootstrap
- can be exposed to the Internet (a script forward the POST request within the LAN)
- includes the interactive guide to do the initial setup of a new IRKit device
- easy to tune and adapt to your needs

The code [is on GitHub](https://github.com/acourreges/irkit-web-remote), feel free to grab it and play with it.