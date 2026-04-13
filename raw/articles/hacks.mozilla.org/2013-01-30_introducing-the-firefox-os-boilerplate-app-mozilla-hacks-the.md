---
title: Introducing the Firefox OS Boilerplate App – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/01/introducing-the-firefox-os-boilerplate-app/
author: Robert Nyman
published: '2013-01-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When coming to a new platform or context, it’s always good to get a peek at some code and examples how to make things work. With [Firefox OS](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS) and app development, it’s just the web with a few additions.

Before here at Mozilla Hacks, we’ve covered a few ways to get started with building apps for Firefox OS:

## My experiences

Lately I’ve been fortunate enough to give and take part in a number of workshops around Firefox OS, to see developers trying to build things for it, port their existing web apps and much more.

This has been a fantastic learning lesson for me, and it’s been crucial to see where people might need pointers, help or examples!

## The Firefox OS Boilerplate App

This led to me creating the [Firefox OS Boilerplate App](https://github.com/robnyman/Firefox-OS-Boilerplate-App). As the name implies, it’s there to provide you with the most basic features to get started with building an app from scratch, or tools to port your existing web app.

The idea is also to avoid any dependency on external libraries or resources, but rather be self-contained.

It contains:

- An install button, offering you to install it as a hosted app
[Web Activities](https://hacks.mozilla.org/2013/01/introducing-web-activities/)– lots of examples and use cases[WebAPIs](https://wiki.mozilla.org/WebAPI)in action- Offline support (disabled by default)
- Packaged apps – install your app as a ZIP file

![](../../assets/51372b4607e83eee.png)


It’s available on GitHub:

## How to use it

The easiest way to get started, installing it and testing the various features, is to navigate to the [Firefox OS Boilerplate App](http://robnyman.github.com/Firefox-OS-Boilerplate-App/) in the web browser on a Firefox OS device or in the [Firefox OS Simulator](https://hacks.mozilla.org/2012/12/firefox-os-simulator-1-0-is-here/).

Alternatively, install it in the Firefox OS Simulator Dashboard by providing either of these URLs:

[http://robnyman.github.com/Firefox-OS-Boilerplate-App/](http://robnyman.github.com/Firefox-OS-Boilerplate-App/)[http://robnyman.github.com/Firefox-OS-Boilerplate-App/manifest.webapp](http://robnyman.github.com/Firefox-OS-Boilerplate-App/manifest.webapp)

## Running it locally

Once you’re ready to get started developing, [download the code](https://github.com/robnyman/Firefox-OS-Boilerplate-App) and run it on a web server, or point out your local version of the Firefox OS Boilerplate App in the Firefox OS Simulator.

Note: make sure that the paths in the [manifest file](https://github.com/robnyman/Firefox-OS-Boilerplate-App/blob/gh-pages/manifest.webapp) are valid on your localhost – bear in mind that these paths are relative to the root of the web site they are being served at.

Also make sure to configure your server to send the manifest file with the right `Content-type`

: `application/x-web-app-manifest+json`

.

This is, for instance, easy to set up in an [.htaccess file](http://en.wikipedia.org/wiki/Htaccess) in Apache:

```
AddType application/x-web-app-manifest+json .webapp
```

## Offline support

I’ve provided an [.appcache file](https://github.com/robnyman/Firefox-OS-Boilerplate-App/blob/gh-pages/manifest.appcache) for enabling offline support (it’s disabled by default).

To enable offline capabilities, just add this to the [index.html file](https://github.com/robnyman/Firefox-OS-Boilerplate-App/blob/gh-pages/index.html):

```
```

Please make sure to do your homework before enabling offline support, to avoid possible initial issues:

Remember that the `.appcache`

file has to be served as a `text/cache-manifest`

file:

```
AddType text/cache-manifest .appcache
```

## Packaged apps

When you develop web apps, by default they are being delivered from a server, thus needing online connectivity or offline support to be enabled, to work as expected.

You do have another option, though, which is [packaged apps](https://developer.mozilla.org/en-US/docs/Apps/Packaged_apps). Basically, what this is, is putting all the files of your app into a ZIP file, making them available directly on the device itself.

Packaged apps can also request an elevated access to certain WebAPIs in Firefox OS that aren’t available to hosted apps (we’ll go more into the differences in a later post here on Mozilla Hacks).

There are a couple of files included in the Firefox Boilerplate OS App to help you get started, if you are interested in this.

To create and install a packaged app, you need to go through a few steps:

- ZIP all app content (not containing folder), including regular manifest
- Create a
[mini manifest (the package.manifest file)](https://github.com/robnyman/Firefox-OS-Boilerplate-App/blob/gh-pages/package.webapp)and make sure the “package_path” is absolute to where the ZIP is located - Developer name and info
*has*to match between mini manifest and the regular one in the ZIP file - Have an
`installPackage`

call in JavaScript pointing to the mini manifest (instead of the regular`install`

one) – this is shown in comments in the[base.js file](https://github.com/robnyman/Firefox-OS-Boilerplate-App/blob/gh-pages/js/base.js) - Turn on Developer Mode in the Firefox OS Simulator (Settings > Device Information > More Information > Developer > Developer mode)
- Add type property (e.g.
`"type" : "privileged"`

) in the manifest if you want access to certain APIs

## Work in progress

The Firefox OS Boilerplate App is a work in progress, meaning that it’s likely to change over time. I believe, however, that it gives you a good head start and look into what’s possible with web apps in Firefox OS.

Hope you like it, and please let me know what you think!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 36 comments

Rodolfo De NadaiJanuary 30th, 2013 at 02:57Robert Nyman [Editor]January 30th, 2013 at 03:02mpmediaJanuary 30th, 2013 at 03:13Robert Nyman [Editor]January 30th, 2013 at 03:46zalunJanuary 30th, 2013 at 03:24Robert Nyman [Editor]January 30th, 2013 at 03:46rgJanuary 30th, 2013 at 04:01Robert Nyman [Editor]January 30th, 2013 at 04:58Fernando BrianoJanuary 30th, 2013 at 04:39Robert Nyman [Editor]January 30th, 2013 at 04:41Jaydson GomesJanuary 30th, 2013 at 06:10Robert Nyman [Editor]January 30th, 2013 at 07:34Joshua OlsJanuary 30th, 2013 at 06:18Robert Nyman [Editor]January 30th, 2013 at 07:38Peter BengtssonJanuary 30th, 2013 at 09:54Robert Nyman [Editor]January 30th, 2013 at 10:48Peter BengtssonJanuary 30th, 2013 at 17:31Robert Nyman [Editor]January 31st, 2013 at 02:27Rob HudsonJanuary 30th, 2013 at 21:20Robert Nyman [Editor]January 31st, 2013 at 02:27Tin Aung LinnFebruary 1st, 2013 at 03:10Robert Nyman [Editor]February 1st, 2013 at 04:17zalunFebruary 4th, 2013 at 04:46Rob HudsonFebruary 4th, 2013 at 10:51Robert Nyman [Editor]February 4th, 2013 at 13:18Maël LavaultFebruary 5th, 2013 at 05:46Robert Nyman [Editor]February 5th, 2013 at 07:23Robert Nyman [Editor]February 4th, 2013 at 13:16JulienWFebruary 4th, 2013 at 06:29Robert Nyman [Editor]February 4th, 2013 at 13:24Julien WajsbergFebruary 5th, 2013 at 00:12Julien WajsbergFebruary 5th, 2013 at 00:14Robert Nyman [Editor]February 5th, 2013 at 02:00Robert Nyman [Editor]February 5th, 2013 at 02:00Fernando JiménezFebruary 4th, 2013 at 14:51Robert Nyman [Editor]February 4th, 2013 at 14:54