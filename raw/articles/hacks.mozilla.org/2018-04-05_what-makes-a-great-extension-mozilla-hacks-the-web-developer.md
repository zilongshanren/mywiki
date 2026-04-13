---
title: What Makes a Great Extension? – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/04/what-makes-a-great-extension/
author: Dustin Driver
published: '2018-04-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We’re in the middle of our [Firefox Quantum Extensions Challenge](https://extensionschallenge.com) and we’ve been asking ourselves: What makes a great extension?

Great extensions add functionality and fun to Firefox, but there’s more to it than that. They’re easy to use, easy to understand, and easy to find. If you’re building one, here are some simple steps to help it shine.

## Make It Dynamic

Firefox 57 added [dynamic themes](https://hacks.mozilla.org/2017/12/using-the-new-theming-api-in-firefox/). What does that mean? They’re just like standard themes that change the look and feel of Firefox, but they can change over time. Create new themes for daytime, nighttime, private browsing, and all your favorite things.

Mozilla developer advocate Potch created a wonderful video explaining how dynamic themes work in Firefox:

## Make It Fun

Browsing the web is fun, but it can be downright hilarious with an awesome extension. Firefox extensions support JavaScript, which means you can create and integrate full-featured games into the browser. [Tab Invaders](https://addons.mozilla.org/en-US/firefox/addon/tab-invaders/?src=search) is a fun example. This remake of the arcade classic Space Invaders lets users blast open tabs into oblivion. It’s a cathartic way to clear your browsing history and start anew.

But you don’t have to build a full-fledged game to have fun. [Tabby Cat](https://addons.mozilla.org/en-US/firefox/addon/tabby-cat-friend) adds an interactive cartoon cat to every new tab. The cats nap, meow, and even let you pet them. Oh, and the cats can wear hats.

## Make It Functional

A fantastic extension helps users do everyday tasks faster and more easily. [RememBear](https://addons.mozilla.org/en-US/firefox/addon/remembear-app/), from the makers of TunnelBear, remembers usernames and passwords (securely) and can generate new strong passwords. [Tree Style Tab](https://addons.mozilla.org/en-US/firefox/addon/tree-style-tab/) lets users order tabs in a collapsible tree structure instead of the traditional tab structure. The [Grammarly extension](https://addons.mozilla.org/en-US/firefox/addon/grammarly-1) integrates the entire Grammarly suite of writing and editing tools in any browser window. Excellent extensions deliver functionality. Think about ways to make browsing the web faster, easier, and more secure when you’re building your extension.

## Make It Firefox

The Firefox UI is built on the [Photon Design System](https://design.firefox.com/photon/welcome.html). A good extension will fit seamlessly into the UI design language and seem to be a native part of the browser. Guidelines for typography, [color](https://design.firefox.com/photon/visuals/color.html), [layout](https://design.firefox.com/photon/visuals/grid.html), and [iconography](https://design.firefox.com/photon/visuals/iconography.html) are available to help you integrate your extension with the Firefox browser. Try to keep edgy or unique design elements apart from the main Firefox UI elements and stick to the Photon system when possible.

## Make It Clear

When you upload an extension to addons.mozilla.org (the Firefox add-ons site), pay close attention to its listing information. A clear, easy-to-read description and well-designed screenshots are key. The [Notebook Web Clipper](https://addons.mozilla.org/en-US/firefox/addon/notebook_web_clipper/) extension is a good example of an easy-to-read page with detailed descriptions and clear screenshots. Users know exactly what the extension does and how to use it. Make it easy for users to get started with your extension.

## Make It Fresh

Firefox 60, now available in [Firefox Beta](https://www.mozilla.org/firefox/channel/desktop/), includes a host of brand-new APIs [that let you do even more with your extensions](https://blog.mozilla.org/addons/2018/04/02/extensions-firefox-60/). We’ve cracked open a cask of theme properties that let you control more parts of the Firefox browser than ever before, including `tab color`

, toolbar icon color, frame color, and button colors.

The tabs API now supports a [ tabs.captureTab method](https://developer.mozilla.org/Add-ons/WebExtensions/API/tabs/captureTab) that can be passed a

`tabId`

to capture the visible area of the specified tab. There are also new or improved APIs for proxies, network extensions, keyboard shortcuts, and messages.For a full breakdown of all the new improvements to extension APIs in Firefox 60, check out Firefox engineer [Mike Conca](https://blog.mozilla.org/addons/author/mconcamozilla-com/)’s [excellent post on the Mozilla Add-ons Blog](https://blog.mozilla.org/addons/2018/04/02/extensions-firefox-60/).

## Submit Your Extension Today

The Quantum Extensions Challenge is running until April 15, 2018. Visit [the Challenge homepage](https://extensionschallenge.com) for rules, requirements, tips, tricks, and more. Prizes will be awarded to the top extensions in three categories: Games & Entertainment, Dynamic Themes, and Tab Manager/Organizer. Winners will be awarded an Apple iPad Pro 10.5” Wifi 256GB and be featured on [addons.mozilla.org](https://addons.mozilla.org). Runners up in each category will receive a $250 USD Amazon gift card. Enter today and keep making awesome extensions!

## About Dustin Driver

Journalist, tech writer, and video producer helping Mozilla keep the Web open and accessible for everyone.