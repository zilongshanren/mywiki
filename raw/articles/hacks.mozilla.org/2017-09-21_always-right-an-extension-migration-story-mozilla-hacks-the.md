---
title: Always Right – An Extension Migration Story – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/09/always-right-a-webextension-migration-story/
author: Dietrich Ayala Posted; Web APIs
published: '2017-09-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

I’ve been building extensions for Firefox since 2005. I’ve integrated bookmark services (which got me a job at Mozilla!), fixed the default theme, enhanced the developer tools, tweaked Github, optimized performance, eased tagging, bookmarked all Etherpads, fixed Pocket and many other [terrible wonderful things](https://addons.mozilla.org/en-US/firefox/addon/quickfire/).

I’ve written XUL extensions, Jetpacks, Jetpacks (second kind), SDK add-ons and worked on the core of most of those as well. And now I’ve seen it all: Firefox has the [WebExtensions API](https://developer.mozilla.org/en-US/Add-ons/WebExtensions), a new extension format designed with a goal of browser extensibility without sacrificing performance and security.

In Firefox 57, the WebExtensions API will be the *only* supported extension format. So it’s time to move on. I can no longer frolic in the luxury of the insecure performance footgun APIs that the legacy extension formats allowed. It’s time to migrate the extensions I really just can’t live without.

I started with Always Right, one of the most important extensions for my daily browser use. I recorded this migration, complete with hiccups, missteps and compromises. Hopefully this will help you in your extension migration odyssey!

## I’m Always Right

[Always Right](https://addons.mozilla.org/en-us/firefox/addon/always-right/) is a simple Firefox extension which opens *all* new tabs immediately to the right of the current tab, regardless of how the tab is opened.

This is great for a couple of reasons:

- Tab opening behavior is predictable – it behaves the same 100% of the time. The default behavior in Firefox is determined by a number of factors, too complex to list here. Suffice it to say that changing Firefox’s default tab-opening behavior is like chasing hornets in a hurricane.
-
Related tabs are grouped. When I have a thought about something I’m busy doing, and want to start a new search or open a tab related to it, I open a new tab. This addon makes sure that tab is grouped with the current tabs. The default behavior opens that tab at the end of the tab strip, which results in two separate clusters of tabs related to the same task.


Conceptually, Always Right is a simple extension but ultimately required a complete rewrite in order to migrate to the new WebExtensions API format. The majority of the rewrite was painless and fast, but as is our bane as developers, the last few bits took the most time and were terribly frustrating.

## Migration Overview

The overall concept hasn’t changed: An extension built with the new APIs is still a zip file containing a manifest and all your code and asset files, just like every other extension format before it.

The major pieces of migration are:

- Renaming and migrating to the new manifest format.
- Rewrite the code to use the new WebExtensions APIs.
- Use the new
`web-ext`

CLI tool for packaging.

## Migrating the Manifest

The first step is to migrate your manifest file, beginning by renaming `package.json`

to `manifest.json`

.

Here’s an image that shows the differences between the old file and the new file:

![](../../assets/ec90853deeadabaa.png)


The most important change is to add the property `manifest_version`

and give it a value of `2`

. With the `manifest_version`

, `name`

and `version`

fields in place, you now have all the required properties for a valid extension. Everything else is optional.

However, since you’re updating an extension that already exists, you need to do a couple of other things.

- The
`id`

property is necessary in order for addons.mozilla.org (AMO) to match the new add-on with the old one. Remove the top-level`id`

field, and copy its value into the`applications/gecko/id`

field. -
If you used the

`main`

property, you’ll now specify your entry point file by the specific functionality, such as[background scripts](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/background),[content_scripts](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/content_scripts),[browser_actions (toolbar buttons)](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/browser_action),[page_actions](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/page_action)and[options_ui](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/options_ui). In my extension, I need to listen to tab events, so I used the background property to load a script. -
The

`permissions`

property is used, but differently. The value is now an array instead of an object, and any values you had are likely not supported anymore, and will need to be replaced. You can read about the supported permissions keys and values on the[manifest.json permissions page on MDN](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/permissions).

There are more optional fields not covered here. Read about the other fields in the [new manifest.json docs](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json), and for reference here are the old [package.json docs](https://developer.mozilla.org/en-US/Add-ons/SDK/Tools/package_json).

## Migrating the Functionality

The flow of Always Right is that it listens to an event that specifies that a new tab has been opened, and then modifies the index of that tab such that it is immediately to the right of the currently active tab.

I first moved my `/lib/main.js`

file to `/index.js`

and specified it as a background script in the `manifest.json`

file as noted above.

I then migrated the code in `/index.js`

from the old SDK tabs API to the [WebExtensions tabs API](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/tabs). The old SDK code used the [ tabs.open event](https://developer.mozilla.org/en-US/Add-ons/SDK/High-Level_APIs/tabs#open) and the new code uses the WebExtensions

[.](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/tabs/onCreated)

`tabs.onCreated`

eventFor example, this:

```
window.tabs.on('open', function(newTab) {
// do stuff
});
```


Turned into this:

```
browser.tabs.onCreated.addListener(function(newTab) {
// do stuff
});
```


A more interesting conversion was how to get access to the currently active tab.

In the SDK, you could simply access `window.tabs.activeTab`

, but in the new world of extensions you’ll need to do this:

```
browser.tabs.query({currentWindow: true, active: true}).then(function(tabs) {
// do stuff with the active tab
var activeTab = tabs[0];
});
```


Those were the main changes. Application logic and code flow stayed pretty much the same as before. However, since it’s a new API with different behaviors, a few things came up. I had to make the following adjustments:

- The WebExtensions API code initializes before the active tab is retrievable, so I needed to add checks for the active tab and no-op if it wasn’t available yet.
-
The SDK tabs API didn’t fire when the user reopened a previously-closed tab, but the WebExtensions API does. So I had to add checks to make sure that I didn’t relocate these tabs.

-
Another behavior change is that placing a tab adjacent to a pinned tab that’s not the last pinned tab puts it at the end of the tab strip, instead of just putting it at the end of the pinned tabs, like the SDK API did. So now I get all tabs and iterate over them until I find the last pinned tab, and place the tab there manually.


I also had to ship with some behavior that’s less than ideal and not fixable yet:

- The WebExtensions API executes
`tabs.onCreated`

listeners after the tab is added to the tab strip. This means that with Always Right, if you have a lot of tabs ([say, hundreds](https://metafluff.com/2017/07/21/i-am-a-tab-hoarder/)), you can actually see the tab added to the far end of the tabstrip and then whiz back over to the right of the active tab. It’s dizzying. -
Compounding the problem above, the tab strip scrolls to the new tab, so the currently active tab is scrolled out of view.


## Testing and Debugging

The new, improved developer workflow for testing in an existing profile is entirely different from the Firefox SDK.

To install your add-on for testing, open a new tab navigate to `about:debugging`

(see screenshot below). Click the *Load Temporary Add-on* button and select any file from your extension’s source directory. Your extension will be installed!

![about:debugging screenshot](../../assets/ae63c0957eedc0bd.png)


But what if you see an error there? What if the functionality is not working as expected? You can debug your extension using the Browser Toolbox. Read here how to configure and [open the toolbox](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Debugging#The_Browser_Toolbox).

Later in the development process I found the [web-ext CLI](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Getting_started_with_web-ext) which is great. Use [ web-ext run](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/web-ext_command_reference) like you would cfx/jpm. It opens in a temporary profile.

## Publishing

Once my changes were finished and tested, I relied on my new-found friend `web-ext`

and bundled a zip file with `web-ext build`

. The zip file is found in the `web-ext-artifacts`

subdirectory, named with the new version number. I uploaded the file the same as always on addons.mozilla.org, and the extension passed validation. I waited less than a day and my extension was reviewed and live!

VICTORY! Well, not total victory: Immediately the bugs came in. In a spectacular display of generous hearts, my users reported the bugs by giving the add-on 5 star reviews and commenting about the new version being broken. 😅

I’ve fixed most of the reported issues, so my users and I can now ride happily off into the sunset together.

Looking for help? There’s detailed documentation on migrating your add-ons on MDN, check out the [legacy extension porting page](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Porting_a_legacy_Firefox_add-on).

You can see the source code to this add-on in the [Always Right repo on Github](https://github.com/autonome/Always-Right). If you see any more bugs, let me know!

And if you’d like to try the extension out, you can install [Always Right from addons.mozilla.org](https://addons.mozilla.org/en-us/firefox/addon/always-right/).

## Participation

All code is a work in progress, and participating in the development process by reporting bugs is the easiest way to get things fixed. If you encounter bugs in the WebExtensions APIs, file them in the [WebExtensions components in Bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=Toolkit&component=WebExtensions%3A%20General).

The bugs I filed while migrating this extension:

-
[No easy way to test extension behavior across restarts](https://bugzilla.mozilla.org/show_bug.cgi?id=1389872), because I found bugs that only occured on Firefox startup, but development extensions are uninstalled at restart. -
– I found this issue while trying to figure out how many tabs it took to be able to make things slow enough to visually see new tabs being relocated in the tabstrip. My Tabcount add-on is`Tabs.onCreated`

and`onRemoved`

are evaluated at different times[here](https://addons.mozilla.org/en-US/firefox/addon/tabcount/). -
– this is the bug causing the visual relocation of tabs from the end of the tabstrip to the new location.`Tabs.onCreated`

evaluation is too late to modify index -
[Need a way to know whether a new tab is just a previously closed tab being restored](https://bugzilla.mozilla.org/show_bug.cgi?id=1364019)– this bug would really help any extensions doing things around where and how new tabs are opened. -
[Moving a tab to an index that is a pinned tab adds to end of tab strip instead of next valid index](https://bugzilla.mozilla.org/show_bug.cgi?id=1388276)– great opportunity for “do what i want” API design.

## 9 comments

wOxxOmSeptember 21st, 2017 at 08:31Dietrich AyalaSeptember 21st, 2017 at 17:21Dietrich AyalaSeptember 21st, 2017 at 17:28MarkSeptember 21st, 2017 at 11:13Dietrich AyalaSeptember 21st, 2017 at 17:23JackSeptember 21st, 2017 at 12:23Dietrich AyalaSeptember 21st, 2017 at 17:25steltenpowerOctober 3rd, 2017 at 15:10Dietrich AyalaOctober 3rd, 2017 at 21:25