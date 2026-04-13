---
title: Firebug 3 & Multiprocess Firefox (e10s) – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/12/firebug-3-multiprocess-firefox-e10s/
author: Jan Honza Odvarko
published: '2014-12-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Firebug 3 alpha** was [announced](https://blog.getfirebug.com/2014/11/10/firebug-3-next-generation-of-firebug/) couple of weeks ago. This version represents the next generation of Firebug built on top of Firefox native developer tools.

There are several reasons why having Firebug built on top of native developer tools in Firefox is an advantage — one of them is tight integration with the existing platform. This direction allows simple use of available platform components. This is important especially for upcoming multiprocess support in Firefox (also called Electrolysis or E10S).

From [wiki](https://wiki.mozilla.org/Electrolysis):


The goal of the Electrolysis project (“e10s” for short) is to run web content in a separate process from Firefox itself. The two major advantages of this model are security and performance.

The e10s project introduces a great leap ahead in terms of security and performance, as well as putting more emphasis on the internal architecture of add-ons. The main challenge (for many extensions) is solving communication problems between processes. The add-on’s code will run in a different process (browser chrome process) from web page content (page content process) — see the diagram below. Every time an extension needs to access the web page it must use one of the available inter-process communication channels (e.g. [message manager](https://developer.mozilla.org/en-US/docs/The_message_manager) or [remote debugging protocol](https://wiki.mozilla.org/Remote_Debugging_Protocol)). Direct access is no longer possible. This often means that many of the existing synchronous APIs will turn into asynchronous APIs.

Developer tools, including Firebug, deal with the content in many ways. Tools usually collect a large amount of (meta) data about the debugged page and present it to the user. Various CSS and DOM inspectors not only display internal content data, but also allow the user to edit them and see live changes. All these features require heavy interaction between a tool and the page content.

![](../../assets/428eb7268e7d4cf7.png)


So Firebug, built on top of the existing developer tools infrastructure that already ensures basic interaction with the debugged page, allows us to focus more on new features and user experience.

## Firebug Compatibility

**Firebug 2.0** is compatible with Firefox 30 – 36 and will support upcoming non-multiprocess browsers (as well as the recently announced [browser](https://hacks.mozilla.org/2014/11/mozilla-introduces-the-first-browser-built-for-developers-firefox-developer-edition/) for developers).

**Firebug 3.0** alpha (aka [Firebug.next](https://github.com/firebug/firebug.next)) is currently compatible with Firefox 35 – 36 and will support upcoming multiprocess (as well as non-multiprocess) browsers.

## Upgrade From Firebug 2

If you install Firebug 2 into a multiprocess (e10s) enabled browser, you’ll be prompted to upgrade to Firebug 3 or switch off the multiprocess support.

![](../../assets/1f086b344782f9fd.png)


Upgrade to Firebug 3 is definitely the recommended option. You might miss some features from Firebug 2 in Firebug 3 (it’s still in alpha phase) like Firebug extensions, but this is the right time to provide feedback and let us know what the priority features are for you.

You can follow us on [Twitter](https://twitter.com/firebugnews/) to be updated.

Leave a comment here or on the Firebug [newsgroup](https://groups.google.com/forum/#!forum/firebug).

Jan ‘Honza’ Odvarko

## About
[
Jan Honza Odvarko ](http://www.softwareishard.com/)

Honza is working on Firefox Developer Tools

## 6 comments

Jake ZieveDecember 4th, 2014 at 00:39Jan OdvarkoDecember 5th, 2014 at 14:13antDecember 4th, 2014 at 03:03Matt SmithDecember 4th, 2014 at 14:51Jan OdvarkoDecember 5th, 2014 at 14:19RiccardoDecember 5th, 2014 at 14:18