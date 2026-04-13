---
title: 'Firefox 66: The Sound of Silence – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2019/03/firefox-66-the-sound-of-silence/
author: Dan Callahan
published: '2019-03-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 66 is out, and brings with it a host of great new features like screen sharing, scroll anchoring, autoplay blocking for audible media, and initial support for the Touch Bar on macOS.

These are just highlights. For complete information, see:

## Audible Autoplay Blocking

Starting with version 66, Firefox will [block audible autoplaying video and audio](https://hacks.mozilla.org/2019/02/firefox-66-to-block-automatically-playing-audible-video-and-audio/). This means media (audio and video) have to wait for user interaction before playing, unless the `muted`

property is set on the associated [HTMLMediaElement](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement). Blocking can be disabled on a case-by-case basis in the site information overlay:

Now ![Screenshot of the Site Information panel showing the 'Autoplay sound' permission](../../assets/cad4ac84fc691ea8.png)


*you*get to decide when to disturb

[the sound of silence](https://www.youtube.com/watch?v=NAEppFUWLfc)

[.](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

**Note:** We’re rolling out blocking gradually to ensure that it doesn’t break legitimate use cases. All Firefox users should have blocking enabled [within a few days](https://bugzilla.mozilla.org/1535667).


## Usability Improvements

### Scroll Anchoring

Firefox now implements [scroll anchoring](https://drafts.csswg.org/css-scroll-anchoring/), which prevents slow-loading content from suddenly appearing and pushing visible content off the page.

### Touch Bar

The Touch Bar on macOS is now supported, offering quick access to common browser features without having to learn keyboard shortcuts.

### Tab Search

Too many tabs? The overflow menu sports a new option to search through your open tabs and switch to the right one.

Astute users will note that clicking on “Search Tabs” focuses the Awesomebar and types a ![Screenshot of Firefox's tab overflow menu showing a new 'Search Tabs' options](../../assets/e370c9fcd53d001e.png)


`%`

sign in front of your query. Thus, while the menu entry makes tab search much more discoverable, you can actually achieve the same effect by focusing the Awesomebar and manually typing a `%`

sign or [other modifier](https://support.mozilla.org/en-US/kb/awesome-bar-search-firefox-bookmarks-history-tabs#w_changing-results-on-the-fly).

### Extension Shortcuts

Speaking of shortcuts, you can now manage and change all of the shortcuts set by extensions by visiting `about:addons`

and clicking “Manage Extension Shortcuts” under the gear icon on the Extensions overview page.![Screenshot of Firefox's new settings page to manage keyboard shortcuts added by extensions](../../assets/43adba844819fb92.png)


### Better Security Warnings

We’ve [completely redesigned Firefox’s security warnings](https://blog.mozilla.org/ux/2019/03/designing-better-security-warnings/) to better encourage safe browsing practices (i.e., don’t ignore the warnings!)

## Expanded CSS Features

Firefox is the first browser to support animating the CSS Grid `grid-template-rows`

and `grid-template-columns`

properties, as seen in the [video](https://www.youtube.com/watch?v=dC4W7t7JlHw) below.

We’re also the first browser to support the [ overflow-inline](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/overflow-inline) and

[media queries, which make it possible to apply styles based on whether (and how) overflowing content is available to the user. For example, a digital billboard might report](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/overflow-block)

`overflow-block`

`overflow-block: none`

, while an e-reader would match `overflow-block: paged`

.Furthermore, Firefox now supports:

- Optional
[case sensitivity](https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors#case-sensitive)for`[attr]`

selectors. - Unprefixed
`min-content`

and`max-content`

size keywords. [19 new shorthand logical properties](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/66#CSS)— these specify values relative to the current writing mode rather than the edges of the screen .

## New DOM APIs

The new [ getDisplayMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getDisplayMedia) API enables screen sharing on the Web similarly to how

[provides access to webcams. The resulting stream can be processed locally or shared over the network with WebRTC. See](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)

`getUserMedia`

[Using the Screen Capture API](https://developer.mozilla.org/en-US/docs/Web/API/Screen_Capture_API/Using_Screen_Capture)on MDN for more information.

![Screenshot of Firefox's screen sharing dialog](../../assets/66dc8912e5d35733.png)


![Screenshot of Firefox's screen sharing dialog](../../assets/66dc8912e5d35733.png)

Mozilla is using `getDisplayMedia`

in Bugzilla to allow people to [take and attach screenshots](https://twitter.com/BugzillaUX/status/1106203965497081856) to their bug reports, directly from inside the browser.

Also, starting with Firefox 66, `InputEvent`

now has a read-only property, `inputType`

. This distinguishes between many different types of edits that can happen inside an input field, for example `insertText`

versus `insertFromPaste`

. To learn more, check out the documentation (and live demo) [on MDN](https://developer.mozilla.org/en-US/docs/Web/API/InputEvent/inputType).

## Browser Internals

Lastly, we’ve made a few changes to how Firefox works under the hood:

- Local storage for browser extensions is now backed by IndexedDB, offering
[significant performance and memory improvements](https://blog.mozilla.org/addons/2019/02/15/extensions-in-firefox-66/), especially for users with many extensions installed. No developer-facing APIs were changed; this improvement is completely transparent and automatic for extension authors. - We’ve
[doubled Firefox’s default number of content processes](http://www.erahm.org/2019/03/13/doubling-the-number-of-content-processes-in-firefox/)from 4 to 8. We’ve managed to do this while keeping Firefox’s memory usage virtually unchanged thanks to Project Fission’s efforts to[reduce per-process overhead](https://wiki.mozilla.org/Project_Fission/Memory). - Firefox now supports
[Windows Hello for passwordless authentication](https://blog.mozilla.org/security/2019/03/19/passwordless-web-authentication-support-via-windows-hello/)online via[WebAuthn](https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API).

From all of us at Mozilla, thank you for choosing Firefox!

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 27 comments

Boris BosanoviciMarch 20th, 2019 at 15:00Dan CallahanMarch 21st, 2019 at 10:18GlennMarch 21st, 2019 at 13:11Dan CallahanMarch 21st, 2019 at 13:54GlennMarch 21st, 2019 at 14:43JerryMarch 21st, 2019 at 07:19jopMarch 21st, 2019 at 07:30Juan LanusMarch 21st, 2019 at 07:55Dan CallahanMarch 21st, 2019 at 10:11GregMarch 21st, 2019 at 15:59Dan CallahanMarch 22nd, 2019 at 14:38Sergey KuzmenkoMarch 22nd, 2019 at 02:23Dan CallahanMarch 22nd, 2019 at 14:40StagerMarch 23rd, 2019 at 13:34Dan CallahanMarch 23rd, 2019 at 13:51RumiMarch 25th, 2019 at 11:28Dan CallahanMarch 26th, 2019 at 15:14Rai42March 24th, 2019 at 06:16Dan CallahanMarch 24th, 2019 at 08:24Rai42March 24th, 2019 at 10:28Dan CallahanMarch 26th, 2019 at 14:48happysurfMarch 26th, 2019 at 00:52Dan CallahanMarch 26th, 2019 at 15:04LetsPlayNintendoITAMarch 31st, 2019 at 09:11Dan CallahanApril 1st, 2019 at 07:57LennyApril 3rd, 2019 at 22:23Dan CallahanApril 4th, 2019 at 08:00