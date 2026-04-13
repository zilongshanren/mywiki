---
title: Firefox 61 – Quantum of Solstice – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/06/firefox-61-quantum-of-solstice/
author: Sergi Mansilla
published: '2018-06-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Summertime 1, and the browser is speedy! Firefox 61 is now available, and with it come new performance improvements that make the fox faster than ever! Let’s take a short tour of the highlights:

### Parallel CSS Parsing

![a road sign that says "parallel parsing only"](../../assets/aca81b7b6614e084.png)

[mjfmjfmjf on flickr](https://www.flickr.com/photos/mjfmjfmjf/15931280059)

[Quantum CSS](https://hacks.mozilla.org/2017/08/inside-a-super-fast-css-engine-quantum-css-aka-stylo/) boosted our style system by calculating computed styles in parallel. Firefox 61 adds even more power to Quantum CSS by also parallelizing the parsing step! The extra horsepower pays real dividends on sites with large stylesheets and complex layouts.

### Retained Display Lists

One of the final steps before a page is painted onto the screen is building a list of everything that is going to be drawn, from lowest z-order to highest (“back to front”). In Firefox, this is called the *display list*, and it’s the final chance to determine what’s on screen before painting begins. The display list contains backgrounds, borders, box shadows, text, everything that’s about to be pixels on the screen.

Historically, the entire display list was computed prior to every new paint. This meant that if a 60fps animation was running, the display list would be computed 60 times a second. For complex pages, this gets to be costly and can lead to reduced script execution budget and, in severe cases, dropped frames. Firefox 61 enables “retained” display lists, which, as the name would suggest, are retained from paint to paint. If only a small amount of the page has changed, the renderer may only have to recompute a small portion of the display list. With retained display lists enabled, the graphics team has observed a near 40% reduction in dropped frames due to list building! We’ve decided to pass those savings on to you, and are enabling the initial work in Firefox 61.

You can dive deeper into display lists in [Matt Woodrow’s recent post](https://hacks.mozilla.org/2018/06/retained-display-lists/) here on Hacks.

Pretty snazzy stuff, but there’s more than just engine improvements! Here are few other new things to check out in this release:

## Accessibility Inspector

A great website is one that works for everyone! The web platform has accessibility features baked right in that let users with assistive technologies make use of web content. Just as the JS engine can see and interact with a tree of elements on a page, there is a separate “accessibility tree” that is available to assistive technologies so they can better describe and understand the structure and UI of a website. Firefox 61 ships with an Accessibility Inspector that lets developers view the computed accessibility tree and better understand which aspects of their site are friendly to assistive technologies and spot areas where accessible markup is needed. Useful for spotting poorly-labeled buttons and for debugging advanced interactions annotated with [ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA).

You can learn more about how to use the Accessibility Inspector in [Marco Zehe’s introductory blog post](https://www.marcozehe.de/2018/04/11/introducing-the-accessibility-inspector-in-the-firefox-developer-tools/).

## Speaking of DevTools…

- The tabs for each panel are now draggable, so you can put your most-used tools where you want them!
- No need to open Responsive Design Mode to enable simulated network throttling – it’s now also available from the top menu of the Network pane.
- See a custom property in the Inspector? Hover to see its value. While typing css, custom properties autocomplete, including color swatches when the value is a color.

## Tab Management

One of the most popular uses of browser extensions is to help users better ~~hoard~~ manage their open tabs. Firefox 61 ships with new extension APIs to help power users use tabs more powerfully! Extensions with the `tabs`

permission can now [hide](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/tabs/hide) and [restore](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/tabs/show) tabs on the browser’s tab bar. The hidden tabs are still loaded, they’re simply not shown. Extensions for productivity and organization can now swap out groups of tabs based on task or context. Firefox also includes an always-available menu that lists all open tabs regardless of their hidden state.

## Wrapping Up

Curious about everything that’s new or changed in Firefox 61? You can view the [Release Notes](https://www.mozilla.org/en-US/firefox/61.0/releasenotes/) or see the full platform changelog on [MDN Web Docs](https://developer.mozilla.org/en-US/Firefox/Releases/61).

Have A Great Summer!

1. In the Northern hemisphere, that is. I mean, I hope the Southern hemisphere has a great summer too- it’s just a ways off.

## 2 comments

RoyiJune 27th, 2018 at 04:02nassoJune 28th, 2018 at 13:46