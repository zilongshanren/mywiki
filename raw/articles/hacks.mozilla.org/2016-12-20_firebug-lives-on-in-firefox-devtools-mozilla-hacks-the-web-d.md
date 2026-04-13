---
title: Firebug lives on in Firefox DevTools – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/12/firebug-lives-on-in-firefox-devtools/
author: Soledad Penadés
published: '2016-12-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As you [might have heard already](https://blog.getfirebug.com/2016/02/08/merging-firebug-into-the-built-in-firefox-developer-tools/), Firebug has been discontinued as a separate Firefox add-on.

The reason for this huge change is [Electrolysis](https://wiki.mozilla.org/Electrolysis), Mozilla’s project name for a redesign of Firefox architecture to improve responsiveness, stability, and security. Electrolysis’s multiprocess architecture makes it possible for Firefox to run its user interface (things like the address bar, the tabs and menus) in one process while the content (websites) runs in other processes. With multiprocess architecture, if a website crashes, it doesn’t also crash the whole browser.

Unfortunately, Firebug wasn’t designed with multiprocess in mind, and making it work in this new scenario would have required an extremely difficult and costly rewrite. The [Firebug Working Group](https://getfirebug.com/wiki/index.php/Firebug_Working_Group) agreed they didn’t have enough resources to implement such a massive architectural change. Additionally, Firefox’s built-in developer tools have been gaining speed, so it made sense to base the next version of Firebug on these tools instead.

The decision was made that the next version of Firebug (codenamed *Firebug.next*) [would build on top of Firefox DevTools](https://hacks.mozilla.org/2014/12/firebug-3-multiprocess-firefox-e10s/), and Firebug would be merged into the built-in tools.

And perhaps most importantly, **we joined forces to build the best developer tools together**, rather than compete with each other. Many of Firebug’s core developers are on the DevTools team, including [Jan ‘Honza’ Odvarko](http://softwareishard.com/) and [Mike Ratcliffe](http://flailingmonkey.com/). Other Firebug Working Group members like [Sebastian Zartner](https://github.com/SebastianZ) and [Florent Fayolle](https://github.com/fflorent) are also active DevTools contributors.

A huge **thank you** to them for bringing their expertise in browser developer tooling to the project!

### In practical terms, what does it mean to merge Firebug into DevTools?

Several features have been absorbed: The [DOM panel](https://developer.mozilla.org/en-US/docs/Tools/DOM_Property_Viewer), [the Firebug theme](https://developer.mozilla.org/en-US/docs/Tools/Settings#Choose_DevTools_theme), [Server-side log messages](https://developer.mozilla.org/cs/docs/Tools/Web_Console/Console_messages#Server), the HTTP inspector (aka XHR Spy), and various popular add-ons like [FireQuery](https://addons.mozilla.org/en-us/firefox/addon/firequery/), [HAR export](http://www.softwareishard.com/blog/har-export-trigger/), and [PixelPerfect](https://addons.mozilla.org/en-US/firefox/addon/pixel-perfect/). Also, [over 40 bugs](https://mzl.la/2gNWrwz) were fixed to close the gap between DevTools and Firebug.

*For curious readers, a couple of articles on **hacks.mozilla.org** and on the **Firebug blog** go into more detail.*

If you are switching now from Firebug to Firefox DevTools, you will of course notice differences. This [migration guide](https://developer.mozilla.org/en-US/docs/Tools/Migrating_from_Firebug) can help you.

We understand that disruption is never really welcome, but we are working hard to ensure developers have the best possible tools, and sometimes this means we need to refocus and use resources wisely.

You can help: Tell us which features you need are missing. There are a few ways you can do this:

- Comment on
[this thread](https://groups.google.com/forum/#!topic/mozilla.dev.developer-tools/iGXTwn0xRaU)on[the Mozilla dev-developer-tools mailing list](https://lists.mozilla.org/listinfo/dev-developer-tools). - Share your feedback on
[this thread](https://groups.google.com/forum/#!topic/firebug/Q6eyvGt6hyI/discussion)on[the Firebug Google group](https://groups.google.com/forum/#!forum/firebug). - Or, post to
[this discussion thread on Twitter](https://twitter.com/FirefoxDevTools/status/800705364446629889).

We are already [tracking missing features on this bug](https://bugzilla.mozilla.org/show_bug.cgi?id=991806), and so far you have told us that the most important are these:

- Break on XHR (
[bug 821610](https://bugzilla.mozilla.org/show_bug.cgi?id=821610)) - Break on DOM mutations (
[bug 1004678](https://bugzilla.mozilla.org/show_bug.cgi?id=1004678)) - Better CSS auto-completion (like
[bug 1106336](https://bugzilla.mozilla.org/show_bug.cgi?id=1106336)and others) - Various console auto-complete improvements: (
[bug 1267140](https://bugzilla.mozilla.org/show_bug.cgi?id=1267140),[bug 1270015](https://bugzilla.mozilla.org/show_bug.cgi?id=1270015),[bug 672733](https://bugzilla.mozilla.org/show_bug.cgi?id=672733), and more) - An events sidebar panel: (
[bug 1226640](https://bugzilla.mozilla.org/show_bug.cgi?id=1226640)) - Live previewing changes made in the inspector (when changing attributes or editing as HTML:
[bug 815464](https://bugzilla.mozilla.org/show_bug.cgi?id=815464)) - Improvements to the way console log messages are displayed: (
[bug 1032855](https://bugzilla.mozilla.org/show_bug.cgi?id=1032855),[bug 1165010](https://bugzilla.mozilla.org/show_bug.cgi?id=1165010)and more) - Validating CSS values and selectors as you type: (
[bug 1227054](https://bugzilla.mozilla.org/show_bug.cgi?id=1227054)) - A DOM properties sidebar panel (
[bug 704094](https://bugzilla.mozilla.org/show_bug.cgi?id=704094)) - Font-size changes in the Firebug theme (
[bug 1319079](https://bugzilla.mozilla.org/show_bug.cgi?id=1319079)) - An option to add cookies: (
[bug 1231451](https://bugzilla.mozilla.org/show_bug.cgi?id=1231451)and[bug 1231452](https://bugzilla.mozilla.org/show_bug.cgi?id=1231452))

We thank you for your loyalty and hope you understand why we’ve made this difficult decision. The Firebug spirit lives on in all of the browser developer tools we build and use today.

*The Firefox DevTools and Firebug teams*

## About
[
Soledad Penadés ](https://soledadpenades.com)

Sole works at the Developer Tools team at Mozilla, helping people make amazing things on the Web, preferably real time. Find her on #devtools at irc.mozilla.org

## About
[
Jan Honza Odvarko ](http://www.softwareishard.com/)

Honza is working on Firefox Developer Tools

## About
[
Patrick Brosset ](http://patrickbrosset.com)

Patrick manages the DevTools engineering team at Mozilla

## 11 comments

Firefox UserDecember 20th, 2016 at 07:15Lawrence SanDecember 20th, 2016 at 09:55Mark Fischer, Jr.December 21st, 2016 at 08:32Lawrence SanDecember 23rd, 2016 at 10:36YepHepDecember 20th, 2016 at 11:03FlyingHailDecember 21st, 2016 at 03:49Castle SnowDecember 21st, 2016 at 01:21revyhDecember 21st, 2016 at 18:45Patrick BrossetJanuary 3rd, 2017 at 01:50EagleJanuary 6th, 2017 at 02:20Dan CallahanMarch 31st, 2017 at 14:24