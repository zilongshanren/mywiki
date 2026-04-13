---
title: Announcing the prototype Firefox OS Simulator – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/11/announcing-the-prototype-firefox-os-simulator/
author: Luca Greco
published: '2012-11-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Firefox OS](http://mozilla.org/firefoxos/) (and the [Boot2Gecko (B2G)](https://wiki.mozilla.org/B2G) project on which it is based) has been written about extensively on Hacks already, but the brief summary is that Mozilla is building a mobile phone operating system where the whole user interface is built on web technology (HTML, CSS and JavaScript). Part of the magic in making that happen is that we’re giving the web platform [new superpowers](https://wiki.mozilla.org/WebAPI) that enable it to access more device capabilities and data sources. Using the web as a basis for apps means that you can build a single app that works on many platforms and with a lot more freedom as a developer.

## Getting Started

If you’re thinking “that all sounds great, but how do I get started?”, you can check out Luca Greco’s detailed [“Hacking Firefox OS”](https://hacks.mozilla.org/2012/11/hacking-firefox-os/) article. In this article, I’m going to cover some of the specifics of working with the Firefox OS Simulator, which Luca mentions in his article.

The Firefox OS Simulator was introduced [in a Hacks post last month as r2d2b2g](https://hacks.mozilla.org/2012/10/r2d2b2g-an-experimental-prototype-firefox-os-test-environment/), a prototype Firefox add-on that makes it really easy to install B2G on your Windows, Mac or Linux computer. B2G is undergoing heavy development, and the Firefox OS Simulator makes it easy to stay up-to-date (the 1.0 release will automatically update… for now, it’s a simple install that doesn’t require restarting Firefox).

We’re angling for a “1.0” release of the Simulator soon. Our main goal with 1.0 is to make it easy to run B2G and install apps that you’re working on into it, and we’re a good way toward that goal right now. You can try out the Simulator right now by [downloading it from Myk’s r2d2b2g page](http://people.mozilla.org/~myk/r2d2b2g/).

## The Simulator Manager

To get going with the Simulator, you’re first going to open up the “Simulator Manager”. The Manager lets you control the Simulator and manages the apps that you have installed into it. Start up the Manager by selecting “Firefox OS Simulator” from the Web Developer menu, or using the `firefoxos manager`

command [from the Developer Toolbar’s command line](https://hacks.mozilla.org/2012/08/new-firefox-command-line-helps-you-develop-faster/).

Here’s what the Simulator Manager looks like:

On the left, you’ll find some navigation controls including a switch that lets you start and stop the Simulator. You can also start and stop the Simulator using the ![](https://hacks.mozilla.org/wp-content/uploads/2012/11/Firefox-OS-Simulator-Manager-2-500x299.png)


`firefoxos start`

and `firefoxos stop`

commands in the Developer Toolbar. The “Console” checkbox allows you to start up with an Error Console window so that you can spot errors that might arise while you’re working on your apps.## Working with your apps

In the screenshot above, you’ll see that I’ve already installed a couple of apps. You can add apps by providing a URL to a site (with autocompletion based on your open tabs) or, even better, a URL to a [manifest](https://marketplace.mozilla.org/developers/docs/manifests) (so that the app can have a proper icon and such). You’ll need a manifest file anyhow to submit to the [Firefox Marketplace](https://marketplace.mozilla.org/), so you might as well start out with that early on.

You can also locate a manifest file on your local computer so that you can create a [packaged app](https://developer.mozilla.org/en-US/docs/Apps/Packaged_apps) (no web server required!).

In the screenshot above, you’ll see that I installed James Long’s [Weather Me](http://jlongster.github.com/weatherme/) app straight from GitHub and Fred Wenzel’s Serpent game from a local clone of its [git repository](https://github.com/fwenzel/serpent/). I’ll note that I did have to tweak the manifest for Serpent a little bit, because it was set up to deploy to GitHub rather than from its local directory. Changing just a couple of fields was all it took and then it worked great!

With those set up, I clicked the switch that says “Stopped” to fire up the Simulator. Then, I unlocked it with a swipe of the mouse, and swiped left on the home screen to get to my apps:

As you can see, the Weather Me and Serpent apps are installed and ready for testing! One feature I’d like to point out is the home button at the bottom of the Simulator. You can press the “Home” key on your keyboard to do the same function, but it’s nice having an on-screen button to mimic the physical button a phone would have.![](../../assets/3ffc990394d62612.png)


While hacking away on these apps, if I make changes I just have to follow some simple rules to see my changes. Hosted apps follow the usual rules for website caching and for [working with appcache](https://developer.mozilla.org/en-US/docs/HTML/Using_the_application_cache) (which you should!). You can update packaged apps just by clicking the Update button in the dashboard. The Simulator is updated, restarted and your app is brought into view right away.

Once you’re done working with an app, you can remove it from the manager, which will also remove it from the Simulator (though you made need to restart your Simulator to see the icon disappear).

The Firefox OS Simulator is the easiest way to try out Firefox OS apps today and to verify how they’ll look before [submitting them to the Marketplace](https://marketplace.mozilla.org/developers/docs/mkt_submission).

## How the Simulator works

The Firefox OS Simulator is different from some mobile environment simulations in that it doesn’t create a virtual computer. Instead, it is actually [B2G Desktop](https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Using_the_B2G_desktop_client), a version of the Boot2Gecko project that is built for desktop operating systems. This allows the Simulator to run very quickly and with minimal startup time on your computer.

## Get it today!

Though we’re still cleaning things up for a 1.0 release, you can [install it today](https://addons.mozilla.org/firefox/addon/firefox-os-simulator/), give it a try, and [let us know if you run into any problems](https://github.com/mozilla/r2d2b2g/issues?state=open).

## 31 comments

Bob PelersonNovember 15th, 2012 at 18:14Kevin DangoorNovember 15th, 2012 at 19:01Myk MelezNovember 16th, 2012 at 10:40AlexandreNovember 16th, 2012 at 04:23Aaron K.November 16th, 2012 at 05:59Kevin DangoorNovember 16th, 2012 at 06:10JeffreyNovember 16th, 2012 at 06:45SokratisNovember 16th, 2012 at 06:39Kevin DangoorNovember 16th, 2012 at 06:41Ken SaundersNovember 16th, 2012 at 08:35AdamNovember 18th, 2012 at 15:24Kevin DangoorNovember 18th, 2012 at 18:48MarvinNovember 19th, 2012 at 06:26AlastairNovember 19th, 2012 at 09:05Kevin DangoorNovember 19th, 2012 at 09:14shimmyNovember 20th, 2012 at 17:37Kevin DangoorNovember 20th, 2012 at 19:29James ParsonNovember 22nd, 2012 at 03:21Kevin DangoorNovember 26th, 2012 at 09:25Miguel Angel Ivars MasNovember 27th, 2012 at 07:15Jim CloughleyDecember 2nd, 2012 at 18:56Kevin DangoorDecember 2nd, 2012 at 19:29FitoschidoDecember 17th, 2012 at 06:54Robert NymanDecember 18th, 2012 at 01:44viswaprasathDecember 23rd, 2012 at 03:52shimmyDecember 27th, 2012 at 17:02M S RishikeshJanuary 3rd, 2013 at 10:20Phoenix FireJanuary 10th, 2013 at 08:57JanetJanuary 29th, 2013 at 12:51Robert Nyman [Editor]January 30th, 2013 at 02:09HardikApril 11th, 2013 at 04:40