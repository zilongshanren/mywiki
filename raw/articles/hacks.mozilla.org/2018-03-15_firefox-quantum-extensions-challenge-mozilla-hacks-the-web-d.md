---
title: Firefox Quantum Extensions Challenge – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/03/firefox-quantum-extensions-challenge/
author: Mike Conca Posted
published: '2018-03-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox users love using [extensions](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/What_are_WebExtensions) to personalize their browsing experience. Now, it’s easier than ever for developers with working knowledge of JavaScript, HTML, and CSS to create extensions for Firefox using the [WebExtensions API](https://developer.mozilla.org/en-US/Add-ons/WebExtensions) . New and improved WebExtensions APIs land with each new Firefox release, giving developers the freedom to create new features and fine-tune their extensions.

You’re invited to use your skill, savvy, and creativity to create great new extensions for the [Firefox Quantum Extensions Challenge](https://extensionschallenge.com) . Between **March 15 and April 15, 2018**, use [Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) to create extensions that make full use of [available WebExtensions APIs](https://developer.mozilla.org/Add-ons/WebExtensions/Browser_support_for_JavaScript_APIs) for one of the prize categories. (Legacy extensions that have been updated to WebExtensions APIs, or Chrome extensions that have been ported to Firefox on or after January 1, 2018, are also eligible for this challenge.)

A [panel of judges](https://extensionschallenge.com/#judges) will select three to four finalists in each category, and the community will be invited to vote for the winners. We’ll announce the winners with the release of [Firefox 60](https://developer.mozilla.org/en-US/Firefox/Releases/60) in May 2018. Winners in each category will receive an iPad Pro and promotion of their extensions to Firefox users. Runners-up will receive a $250 USD Amazon gift card.

## Categories

### Best in Tab Management & Organization

Firefox users love customizing their browser tabs. Create the next generation of user-friendly extensions to style, organize, and manage tabs.

### Best Dynamic Themes

With the new [theme API](https://developer.mozilla.org/Add-ons/WebExtensions/API/theme), developers can create beautiful and responsive [dynamic themes](https://developer.mozilla.org/en-US/Add-ons/Themes/Theme_concepts#Dynamic_themes) to customize Firefox’s appearance and make them interactive. We’re looking for a dynamite combination of aesthetics and utility.

### Best in Games & Entertainment

Extensions aren’t just for improving productivity — they’re also great for adding whimsy and fun to your day. We’re looking for high-performing, original ideas that will bring delight to Firefox users.

## New & Improved APIs

So many new WebExtensions APIs have landed in the last few Firefox releases, and Firefox 60 will add even more. Let’s start with themes.

The current Theme API supports nearly [20 different visual elements](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/theme) that developers can customize. In Firefox 60, the list will grow to include the following items now in development:

- tab_line – Set the color of the
[tab line](https://bugzilla.mozilla.org/show_bug.cgi?id=1439734)shown at the top of the active tab - tab_selected – Set the
[background color of the selected tab](https://bugzilla.mozilla.org/show_bug.cgi?id=1434476) - tab_loading – Set the color of the
[tab loading indicator](https://bugzilla.mozilla.org/show_bug.cgi?id=1426686) - popup – Set the background color of the
[Firefox popup](https://bugzilla.mozilla.org/show_bug.cgi?id=1417880)(arrow panel) - popup_text – Set the text color of the
[Firefox popup](https://bugzilla.mozilla.org/show_bug.cgi?id=1417880)(arrow panel) - popup_border – Set the border color of the
[Firefox popup](https://bugzilla.mozilla.org/show_bug.cgi?id=1417880)(arrow panel)

But remember, your goal isn’t just to come up with a nice looking set of UI elements. Wow us with an extension that uses the [Theme API](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/theme) to dynamically modify UI elements in order to create something that is visually stunning and equally useful.

For tabs, several new API have been added, including:

- browserSettings.openBookmarksInNewTabs() for controlling the options to
[open bookmarks in new tabs](https://bugzilla.mozilla.org/show_bug.cgi?id=1420974). - browserSettings.openSearchResultsInNewTabs() so extensions can
[open search results in new tabs](https://bugzilla.mozilla.org/show_bug.cgi?id=1420969). [tabs.captureTab()](https://bugzilla.mozilla.org/show_bug.cgi?id=1427463). This is very similar to[tabs.captureVisibleTab()](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/tabs/captureVisibleTab), but allows you to capture any tab (specified by ID) instead of just the active tab.- Calling
[tabs.create()](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/tabs/create)without a windowId will now[target only non-popup windows](https://bugzilla.mozilla.org/show_bug.cgi?id=1415913). [Tabs.query()](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/tabs/query)now does[pattern matching on the title](https://bugzilla.mozilla.org/show_bug.cgi?id=1334782).

The [contextualIdentities](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/contextualIdentities) API is not new, but it is unique to Firefox and may provide developers with some interesting tools for separating online identities. The same goes for the [sidebar](https://developer.mozilla.org/Add-ons/WebExtensions/API/sidebarAction) API, another unique feature of Firefox that allows developers to get creative with alternate user interface models.

## Get Started

- Visit the
[challenge site](https://extensionschallenge.com)for more information and to submit your extension - Download
[Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) - Want help building your extension? Check out
[these resources](https://extensionschallenge.com/#resources). - Upload your new (or newly ported) extension from the
[Add-on Developer Hub](https://addons.mozilla.org/developers/) - Fill out the
[submission form](https://goo.gl/forms/U4ReAbu8qPsFtMPF3)to enter the challenge - Check out the Web Extensions
[MDN web docs](https://developer.mozilla.org/Add-ons/WebExtensions)for tools and documentation

Winners will be notified by the end of April 2018 and will be announced with the release of Firefox 60 in May 2018.

Good luck!

## About Mike Conca

Mike Conca is the Group Product Manager for the Firefox Web Platform, leading the product team responsible for the core web technologies in Firefox including JavaScript, DOM Web API, WebAssembly, storage, layout, media, and graphics.

## 2 comments

bcMarch 17th, 2018 at 09:06Caitlin NeimanMarch 20th, 2018 at 15:49