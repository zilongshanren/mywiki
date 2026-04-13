---
title: 'Firefox Quantum Developer Edition: the fastest Firefox ever with Photon UI
  and better tooling – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2017/09/firefox-quantum-developer-edition-fastest-firefox-ever/
author: Dan Callahan
published: '2017-09-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox Quantum is now available in [Developer Edition](https://mozilla.org/firefox/developer), and this Firefox is *fast*.

As a reader of the Hacks blog, you may be familiar with [Project Quantum](https://medium.com/mozilla-tech/a-quantum-leap-for-the-web-a3b7174b3c12), our attempt to refactor, redesign, replace, and modernize the very core of Firefox. We’ve shipped many incremental improvements to Firefox in the past, but this release marks the first milestone where we believe Firefox fundamentally *feels* like a newer, better browser.

To celebrate, we gave Developer Edition a brand new logo:

Why does this feel like a brand new browser? Read on!![](../../assets/089646db62071db9.png)


## Firefox Quantum: Towards a next-gen browser

Developer Edition now includes “Quantum CSS,” an [entirely new CSS engine](https://hacks.mozilla.org/2017/08/inside-a-super-fast-css-engine-quantum-css-aka-stylo/) written in [Rust](https://www.rust-lang.org) and based on the [Servo](https://servo.org/) parallel browser engine project. Additionally, the “Quantum Flow” team tracked down and [fixed 369 performance bugs](https://ehsanakhgari.org/blog/2017-09-21/quantum-flow-engineering-newsletter-25) in Firefox, with a special focus on responsiveness and UI interactions. Lastly, the “Quantum DOM” project began overhauling how Firefox prioritizes work, responding more quickly to events like user input while delaying less urgent computations until the browser is idle.

The result? Compared to Firefox six months ago, **today’s Developer Edition is twice as fast** on benchmarks like [Speedometer 2.0](https://mozilla.github.io/arewefastyet-speedometer/2.0/) that simulate the real-world performance of modern web applications.

Furthermore, Firefox is 64-bit and multi-process by default, and Firefox’s ![](../../assets/b13b751fe5a4aadd.png)


[unique architecture](https://medium.com/mozilla-tech/the-search-for-the-goldilocks-browser-and-why-firefox-may-be-just-right-for-you-1f520506aa35)allows it to take advantage of modern, multi-core processors while still respecting your available RAM. Meanwhile, the “Quantum Compositor” project

[significantly reduced](https://blog.mozilla.org/blog/2017/04/19/first-big-bytes-project-quantum/)crashes caused by buggy graphics drivers.

## Photon: Firefox’s new UI

To complement Quantum, the Photon team rebuilt Firefox’s interface to be faster and more modern:

You’ll hear more about Photon in November, but highlights include redesigned menus, square tabs, and a new “Library” button that acts as a single place for your bookmarks, downloads, history, etc. By default, Photon combines the search and URL bars into a single widget, but the old style is only a preference away.

The “Activity Stream” project redesigned the New Tab Page to feature highlights from your recent history and bookmarks, as well as recommendations from Pocket. Of course, each of these content blocks are optional, and [add-ons can completely replace the new tab page](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/chrome_url_overrides) to create entirely different experiences.

We also refreshed form handling in Firefox, adding a brand new autofill feature and implementing built-in widgets for `<input type=date>`

and `<input type=time>`

elements.

Lastly, Firefox’s preferences were completely redesigned and are now searchable.

## DevTools in 57: Redesigned and better than ever

Firefox Quantum: Developer Edition also includes a ton of refined, redesigned, and brand new developer tools.

- The Console, Debugger, and Network tabs are now implemented using standard web technologies, including React and Redux, as part of our “devtools.html” effort.
- The Inspector gained tons of new features for working with CSS Grid, CSS Variables, toggling classes on elements, etc.
- The Console now supports grouping messages and expanding / inspecting objects in-line.
- The Debugger offers completely new ways to search, navigate, and debug projects.

And that’s not all. To read in greater depth about what’s new in Firefox Developer Tools, check out [Developer Edition Devtools Update](https://hacks.mozilla.org/2017/09/developer-edition-devtools-update-now-with-photon-ui).


## Project Quantum: There’s more to come

Today’s release is* *a major milestone in Project Quantum, but we’re not done. Future releases of Firefox will include [Quantum Render](https://wiki.mozilla.org/Platform/GFX/Quantum_Render), a brand new, GPU-optimized rendering pipeline based on Servo’s [WebRender](https://mozillagfx.wordpress.com/2017/09/21/introduction-to-webrender-part-1-browsers-today/) project, and [Quantum DOM](https://wiki.mozilla.org/Quantum/DOM) Scheduler, a new technique that ensures that tabs in the background can’t slow down your active tabs.

[Try out Developer Edition](https://mozilla.org/firefox/developer) today, or [sign up](https://www.mozilla.org/firefox/quantum) to get notified when Firefox Quantum is released to mainline Firefox. Either way, stay tuned to the Hacks blog to learn more about Project Quantum!

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 59 comments

mikeSeptember 26th, 2017 at 08:19Dan CallahanSeptember 26th, 2017 at 11:39Ivan AugustoSeptember 26th, 2017 at 09:09RoyiSeptember 26th, 2017 at 09:50zakiusSeptember 26th, 2017 at 10:50Dan CallahanSeptember 26th, 2017 at 11:38zakiusSeptember 26th, 2017 at 13:05zakiusSeptember 27th, 2017 at 07:22YFSeptember 26th, 2017 at 12:41AshoksinhSeptember 26th, 2017 at 17:58PiyushSeptember 26th, 2017 at 19:59Dan CallahanOctober 2nd, 2017 at 11:50nooneSeptember 27th, 2017 at 01:12Dan CallahanOctober 2nd, 2017 at 13:35SYSMACOctober 3rd, 2017 at 03:42JBSeptember 27th, 2017 at 03:15AekSeptember 27th, 2017 at 03:33SergeySeptember 27th, 2017 at 12:01Harald KirschnerOctober 9th, 2017 at 20:50JeanJSeptember 27th, 2017 at 14:28Dan CallahanOctober 2nd, 2017 at 13:41JulieSeptember 27th, 2017 at 15:02Dan CallahanOctober 2nd, 2017 at 13:43CraigSeptember 28th, 2017 at 05:18Dan CallahanOctober 2nd, 2017 at 13:46Mikey PeeSeptember 28th, 2017 at 12:31Wellington Torrejais da SilvaSeptember 28th, 2017 at 12:42TomSeptember 28th, 2017 at 13:05Alexandre LeducSeptember 28th, 2017 at 13:57Harald KirschnerOctober 9th, 2017 at 20:57AssSeptember 29th, 2017 at 09:24Dan CallahanOctober 2nd, 2017 at 14:00Chris CohierSeptember 29th, 2017 at 12:08Dan CallahanOctober 2nd, 2017 at 14:04KimiSeptember 29th, 2017 at 20:58Dan CallahanOctober 2nd, 2017 at 14:05Artur HaurylkevichSeptember 30th, 2017 at 07:09Dan CallahanOctober 2nd, 2017 at 14:06WesOctober 1st, 2017 at 02:30Dan CallahanOctober 2nd, 2017 at 11:21DaleOctober 1st, 2017 at 11:37Dan CallahanOctober 2nd, 2017 at 11:21ChuckOctober 2nd, 2017 at 14:00Dan CallahanOctober 2nd, 2017 at 14:23MikeOctober 3rd, 2017 at 06:39Marcin W. DąbrowskiOctober 6th, 2017 at 10:05Dan CallahanOctober 7th, 2017 at 11:39SladiOctober 13th, 2017 at 11:55CuongtvOctober 6th, 2017 at 20:24Dan CallahanOctober 7th, 2017 at 11:21CuongtvOctober 8th, 2017 at 20:14PhilippOctober 7th, 2017 at 07:16Dan CallahanOctober 7th, 2017 at 11:25daler5150October 8th, 2017 at 01:34KarenOctober 8th, 2017 at 18:17shellyOctober 9th, 2017 at 05:37DreamwebsOctober 10th, 2017 at 01:34Siamak AlaviOctober 11th, 2017 at 23:59LukeOctober 13th, 2017 at 07:16