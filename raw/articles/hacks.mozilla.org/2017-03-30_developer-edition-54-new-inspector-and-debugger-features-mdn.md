---
title: 'Developer Edition 54: New inspector and debugger features, MDN help in the
  netmonitor, and more – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2017/03/developer-edition-54-new-inspector-and-debugger-features/
author: Patrick Brosset
published: '2017-03-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We didn’t have a chance to blog when Firefox Developer Edition 53 came out, so now that [54 is out too](https://www.mozilla.org/en-US/firefox/developer/), let’s discover what new features and bugs fixes made it into these new releases.

There is a lot to cover so we will get right to it.

## Inspector

The inspector now fully supports [CSS color level 4](https://drafts.csswg.org/css-color/), which means that new color syntax like `hsl(120deg 100% 50%)`

is recognized in the CSS Rules panel.

People love our screenshot feature. In Developer Edition 53 we added a setting that, when turned on, will copy screenshots to your clipboard directly, so you can paste those images directly in other applications.

Firebug users used to be able to copy the full CSS path of any node in the inspector. This feature has now also been added to Firefox DevTools, as demonstrated here:

When nodes are collapsed in the inspector, it’s not possible to know whether they have children or not. A visual hint is displayed between the opening and closing tags as shown below:

![Indicator between opening and closing tags in the inspector to show children exist](../../assets/ecbab80524fa1aaf.png)


A lot of work was done to make the inspector faster and more reliable. In particular, the DOM tree now initializes with the `DOMContentLoaded`

event.

The [CSS Grid inspector](https://hacks.mozilla.org/2016/12/css-grid-and-grid-highlighter-now-in-firefox-developer-edition/), that can be toggled from the CSS rules panel, is now displayed for cases like `display:inline-grid`

or `display:grid !important`

.

Asynchronous Panning and Zooming ([APZ for short](https://hacks.mozilla.org/2016/02/smoother-scrolling-in-firefox-46-with-apz/)) is the technology in Firefox that makes scrolling long pages super fast and smooth. Now, all the overlays that the inspector displays on web pages (like the box-model or the CSS grid lines) also benefit from it and scroll smoothly with the page.

In some situations, it may be hard to know that part of a property is overridden in a CSS rule. For instance, when only a longhand part of a shorthand property (e.g. margin-bottom in margin) gets overridden, the CSS rules panel didn’t show this unless you expand the shorthand property. This has changed, and the CSS rules panel now looks like this:

![When only a part of a shorthand property is overridden](../../assets/4cffa033d837afd8.png)


Right-clicking on an attribute in the inspector now gives you a menu item that lets you copy attribute values. (This is in addition to editing, adding, and deleting, which were already available.):

![Copying attribute values in the inspector](../../assets/e40d2aa93a2cb802.png)


## Debugger

Our awesome [new debugger front-end](https://github.com/firefox-devtools/debugger.html) (available to our Nightly and Developer Edition users for now) gained a ton of new features in Firefox 54.

You can now add watch expressions in the right sidebar, which will be evaluated when you pause:

![](../../assets/99036f2439b949da.png)


A lot of the UI state is saved between sessions now: Opened tabs, whether the sidebar is collapsed, the selected source, whether you want to pause on exceptions, etc., making it easier and much more intuitive to start debugging again.

The debugger now also supports collapsing the layout to a vertical mode when there isn’t enough space:

![](../../assets/b10544b854db3c45.gif)


Code search is also much improved: Outlines are shown around matches, the total number of results is also displayed in the search bar, and a brand new function search option is now available:

![](../../assets/6f0bcfa770940545.png)


The pretty-printing feature has been implemented, so you can now make those minified files much easier to read. Pretty-printing a source file opens the pretty version in another tab:

![](../../assets/4b5679498be54cb2.gif)


Finally, hovering over a variable in the source now pops-up a preview tooltip for this variable, and lets you see its value:

![](../../assets/6b1fb5124044dffe.gif)


## Storage

First a reminder: If you don’t see the Storage panel in DevTools, you’ll need to [enable it first in the settings panel](https://developer.mozilla.org/en-US/docs/Tools/Settings#Default_Firefox_Developer_Tools). (We will soon be working on a new way to open new tools.)

![](../../assets/98bd3c834782a3e6.gif)


In the cookies section, multiple cookies with the same name are now shown correctly.

Local data stored by Web Extensions are now also displayed in the storage panel.

The IndexedDB storage type can now be seen in a new column. You can learn more about [storage types on MDN](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Browser_storage_limits_and_eviction_criteria).

![](../../assets/518222682e19bc37.png)


Last, but definitely not least, the storage panel is now a lot faster when your Firefox browser profile has a lot of IndexedDB data in it.

## Network Monitor

You might know that we spent a lot of last year migrating our tools away from XUL markup and Firefox-only JavaScript to standard HTML, CSS and JavaScript. ([I blogged about this in January](https://hacks.mozilla.org/2017/01/devtools-what-you-need-to-know/)). Well, I’m really pleased to report that the Network Monitor is now part of that revamped tool set. It should be much easier to [work on the panel](http://firefox-dev.tools/?easy&tool=network) if you have some HTML, CSS, and React experience.

We have also added some MDN documentation goodness in the Network Monitor. In particular, both HTTP status codes and HTTP response headers get `[Learn More]`

links that will open relevant documentation pages on MDN:

![](../../assets/fe37498c920b7383.gif)


There is now a new “transferred” size in the monitor’s toolbar that indicates how much data was really transferred over the wire (useful when data is compressed). As before, clicking on this label brings up the performance summary view, but now this view also includes the transferred size:

![](../../assets/1506633fdb63b926.png)


## Responsive Design Mode

The dimension controls have been moved above the viewport so they’re easier to see and use:

![](../../assets/3f7d15a2c1811e6a.png)


We also added the ability for users to enter their own custom devices to the list of pre-defined devices:

![](../../assets/7f8038647a4e74e6.gif)


## JSON Viewer

The JSON Viewer has been around on our [Nightly](https://nightly.mozilla.org/) and [Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) channels for a while.

With Firefox 53, we enabled it on all channels. This means that if you run the standard release of Firefox, very soon JSON responses in tabs will be much easier to read and explore:

![](../../assets/70b35f6658e02a0e.png)


The JSON Viewer is now displayed for files with the `application/manifest+json`

mime-type.

## New Web Extensions API for DevTools

[WebExtensions ](https://developer.mozilla.org/en-US/Add-ons/WebExtensions) are Firefox’s new way to write extensions for the browser that are compatible to a large extent with Google Chrome and Opera.

Firefox now supports new DevTools-related WebExtensions APIs, which means that Chrome DevTools extensions are going to start working with Firefox too!

In particular, it is now possible to create [new DevTools panels](https://github.com/firefox-devtools/extension-examples/tree/master/devtools-panel) with the `devtools.panels.create`

API, or even [execute code in the content window](https://github.com/firefox-devtools/extension-examples/tree/master/console) with the `devtools.inspectedWindow.eval`

API.

We created a GitHub repository that provides [examples of how to build WebExtensions using the DevTools API](https://github.com/firefox-devtools/extension-examples).

## Right-to-Left Layout Improvements

Many [RTL (right-to-left)](https://developer.mozilla.org/en-US/docs/Web/CSS/direction) improvements were made in these last couple of releases.

The settings panel now fully supports RTL, the computed styles panel in the inspector also works better with RTL, the JSONViewer now supports it, the DOM panel also received some RTL love, and finally RTL support also came to the font panel in the inspector.

## More Bug Fixes

The Firebug theme received a variety of fixes and now works much better for our Mac and Linux users (in particular font-size, some padding, breadcrumbs, and various colors were fixed).

The icon for the new Responsive Design Mode in the toolbar was changed. It was confusingly similar to the docking icon, and is now easier to find:

Finally, all the buttons shown in the toolbar now display the corresponding keyboard shortcuts on hover!

![](../../assets/683daf9f3cdf9066.gif)


## Thank You!

Many volunteer contributors have helped fix bugs and implement new features in these releases, so warm thank yous to all (in no particular order)!:

- Kimberly Pennington
- Yann Gravrand
- Tomer Cohen
- Micah Tigley
- Jaideep Bhoosreddy
- Tooru Fujisawa
- Thomas Dräbing
- Adrien Enault
- Iulian Radu
- Ruturaj Vartak
- Rahul Chaudhary
- Oliver Scheiwiller
- Tim Nguyen
- Bao Quan
- Nick Fox
- Eduardo Bouças
- Leonardo Couto
- Kerem Kat
- Ken Lee
- Cosm
- Jarda Snajdr
- Florian Apolloner
- Fabien Casters
- Deepjyoti Mondal
- Dalimil Hajek
- Nicolas Chevobbe
- Taylor Alexander Brown
- Michael Brennan
- André Bargull
- Sébastien Blin
- Ajay Krishna
- Ahmed Towkir

You can see [the full list of bugs](https://mzl.la/2mee2io) if you’re interested.

As always, let us know what you think about this. You can add a comment right here, [file a bug](https://bugzilla.mozilla.org/enter_bug.cgi?product=Firefox&component=Developer%20Tools) if you notice something wrong, or [discuss new ideas or ask for help](https://discourse.mozilla-community.org/c/devtools) on our Discourse forum.

## About
[
Patrick Brosset ](http://patrickbrosset.com)

Patrick manages the DevTools engineering team at Mozilla

## 14 comments

maxmMarch 30th, 2017 at 08:29Patrick BrossetMarch 30th, 2017 at 08:36maxmMarch 30th, 2017 at 09:10WillMarch 30th, 2017 at 13:39Patrick BrossetMarch 31st, 2017 at 00:34vflashMarch 30th, 2017 at 13:48AlbertApril 6th, 2017 at 00:34SachinMarch 30th, 2017 at 10:30WillMarch 30th, 2017 at 13:39duc4231March 30th, 2017 at 20:21drumpf400March 31st, 2017 at 06:21LukeMarch 31st, 2017 at 18:21Patrick BrossetApril 3rd, 2017 at 00:50Wellington TorrejaisApril 3rd, 2017 at 04:31