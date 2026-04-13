---
title: 'Firefox 53: Quantum Compositor, Compact Themes, CSS Masks, and More – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2017/04/firefox-53-quantum-compositor-compact-themes-css-masks-and-more/
author: Dan Callahan
published: '2017-04-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 53, available today, includes the following key new features and enhancements.

### Quantum Compositor Process on Windows

One of the first pieces of [Project Quantum](https://medium.com/mozilla-tech/a-quantum-leap-for-the-web-a3b7174b3c12), the Compositor Process, has arrived on Windows. Compositors are responsible for flattening all of the various elements on a webpage into a single image to be drawn on the screen. Firefox can now run its compositor in a completely separate process from the main Firefox program, which means that Firefox will keep running even if the compositor crashes—it can simply restart it.

For more details on how this aspect of Project Quantum reduces crash rates for Firefox users, check out [Anthony Hughes’ blog post](https://ashughes.com/?p=426).

### Light and Dark Compact Themes

The “compact” themes that debuted with Firefox Developer Edition are now a standard feature of Firefox. Users can find light and dark variants of this space-saving, square-tabbed theme listed under the “Themes” menu in Customize mode.

### New WebExtension Features

WebExtensions are browser add-ons that are designed to work safely and efficiently in Firefox, Chrome, Opera, and Edge, while also supporting powerful features unique to Firefox.

In Firefox 53, WebExtensions gained compatibility with several pre-existing Chrome APIs:

- The
[browsingData](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/browsingData)API lets add-ons clear the browser’s cache, cookies, history, downloads, etc. For example, Firefox’s[Forget Button](https://support.mozilla.org/t5/Protect-your-privacy/Forget-button-quickly-delete-your-browsing-history-on-Firefox/ta-p/30515)could now be implemented as a WebExtension. - The
[identity](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/identity)API allows add-ons to request OAuth2 tokens with the consent of the user, making it easier to sign into services within an add-on. - The
[storage.sync](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/storage/sync)API allows add-ons to save user preferences to Firefox Sync, where it can be shared and synchronized between devices. - The
[webRequest.onBeforeRequest](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/webRequest/onBeforeRequest)API can now access the request body, in addition to headers. - The
[contextMenus](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/contextMenus)API now supports adding menus to browser actions and page actions.

Firefox 53 also supports the following unique APIs:

- Contextual Identities, the basis of the
[Containers experiment in Test Pilot](https://testpilot.firefox.com/experiments/containers), can now be created and managed via the[contextualIdentities](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/contextualIdentities)API. - Context menus can be created on tabs and password fields with the
[contextMenus](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/contextMenus)API. - CSS injected into pages with
[tabs.insertCSS](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/tabs/insertCSS)can specify if the new styles should be considered part of the author stylesheet or the user stylesheet, which exist at different levels in the[cascading order](https://developer.mozilla.org/en-US/docs/Web/CSS/Cascade#Cascading_order).

### New CSS Features: Positioned Masks and Flow-Root

Firefox 53 supports positioned [CSS Masks](https://drafts.fxtf.org/css-masking-1/#masking), which allow authors to partially or fully hide visual elements within a webpage. Masks work by overlaying images or other graphics (like linear gradients) that define which regions of an element should be visible, translucent, or transparent.

Masks can be configured to use either luminance or alpha values for occlusion. When the mode is set to luminance, white pixels in the mask correspond to fully visible pixels in the underlying element, while black pixels in the mask render that area completely transparent. The alpha mode simply uses the mask’s own opacity: transparent pixels in the mask cause transparent pixels in the element.

Many masking properties function similarly to the equivalent `background-*`

properties. For example, `mask-repeat`

works just like `background-repeat`

. To learn more about the available properties, see the [documentation on MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/mask).

The [specification](https://drafts.fxtf.org/css-masking-1/) also defines methods for clipping based on shapes and vector paths. Firefox 53 has partial support for clipping, and complete support is expected in Firefox 54.

Lastly, Firefox also supports the new `display: flow-root`

value, which achieves similar results to [clearfix](https://css-tricks.com/snippets/css/clear-fix/), but using a standard CSS value instead of pseudo-elements or other hacks.

### A Better Default Media Experience

Alongside [many other UI refinements](https://medium.com/@pastith/feeling-safer-online-with-firefox-b9fe13af6600) in Firefox 53, the default `<video>`

and `<audio>`

controls got a new, modern look:

~~Additionally, Firefox 53 includes brand new anti-annoyance technology: By default, HTML5 media will not autoplay until its tab is first activated. Try it by right-clicking on ~~[this link](https://www.youtube.com/watch?v=dQw4w9WgXcQ) and choosing “Open in New Tab.” Notice that the video doesn’t start until you change to that tab.

**Edit:** Autoplay blocking is scheduled for Firefox 54, not 53. Oops. ([Bug 1308154](https://bugzilla.mozilla.org/show_bug.cgi?id=1308154))

### 64-bit Everywhere

Windows users can now select between 32-bit and 64-bit Firefox during installation:

We’ve also removed support for 32-bit Firefox on macOS, and for processors older than Pentium 4 and Opteron on Linux.

### More Info

To find out more about Firefox 53, check out the general [Release Notes](https://www.mozilla.org/en-US/firefox/53.0/releasenotes/) as well as [Firefox 53 for Developers](https://developer.mozilla.org/en-US/Firefox/Releases/53) on MDN.

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 67 comments

JohnApril 19th, 2017 at 10:20Dan CallahanApril 19th, 2017 at 12:02GeorgeApril 19th, 2017 at 14:22TimApril 19th, 2017 at 19:56JoseApril 20th, 2017 at 00:45DDMay 10th, 2017 at 21:39PotchMay 11th, 2017 at 11:27jxnApril 19th, 2017 at 11:07michaelApril 19th, 2017 at 11:31FJApril 19th, 2017 at 11:34Dan CallahanApril 19th, 2017 at 15:15XadiqApril 20th, 2017 at 01:19samApril 24th, 2017 at 04:27Dan CallahanApril 24th, 2017 at 08:15ClaudioMApril 19th, 2017 at 12:04XerathusApril 19th, 2017 at 12:11Dan CallahanApril 19th, 2017 at 12:55minimalistApril 19th, 2017 at 13:22Dan CallahanApril 19th, 2017 at 15:34DanApril 19th, 2017 at 23:59Dan CallahanApril 20th, 2017 at 08:10DanApril 20th, 2017 at 21:53Ludwig StecherApril 19th, 2017 at 13:36Dan CallahanApril 20th, 2017 at 08:20JoseApril 20th, 2017 at 00:48Shady FlukeApril 20th, 2017 at 01:24Dan CallahanApril 20th, 2017 at 09:25FJApril 20th, 2017 at 05:35Dan CallahanApril 20th, 2017 at 09:29FJApril 20th, 2017 at 13:14FJApril 20th, 2017 at 13:42MakoSDVApril 20th, 2017 at 07:59Dan CallahanApril 20th, 2017 at 08:07Miles RaymondApril 20th, 2017 at 09:34grApril 20th, 2017 at 09:43Dan CallahanApril 20th, 2017 at 10:03ElijahApril 20th, 2017 at 09:48Dan CallahanApril 20th, 2017 at 10:01UbuntouristApril 20th, 2017 at 10:00Dan CallahanApril 20th, 2017 at 10:17AnthonyApril 20th, 2017 at 10:18Dan CallahanApril 20th, 2017 at 10:31Hermann HoorApril 20th, 2017 at 10:33Dan CallahanApril 20th, 2017 at 10:43DougApril 20th, 2017 at 12:55Dan CallahanApril 20th, 2017 at 13:12Francesco MigliettaApril 21st, 2017 at 02:42Dan CallahanApril 21st, 2017 at 13:03Sviat LohinauApril 21st, 2017 at 03:46eineApril 21st, 2017 at 08:19KentApril 21st, 2017 at 23:46Dan CallahanApril 24th, 2017 at 09:08MARILYNApril 26th, 2017 at 08:54Root777April 22nd, 2017 at 22:37Dan CallahanApril 24th, 2017 at 08:17DeRSApril 26th, 2017 at 02:05Dan CallahanApril 26th, 2017 at 12:50DeRSApril 26th, 2017 at 14:02Dan CallahanApril 28th, 2017 at 10:37DeRSApril 28th, 2017 at 16:39GraemeMay 7th, 2017 at 18:07Dan CallahanMay 8th, 2017 at 07:33jackApril 27th, 2017 at 16:08Dan CallahanApril 28th, 2017 at 10:38J DMay 3rd, 2017 at 04:08Dan CallahanMay 3rd, 2017 at 16:31Matt M.May 6th, 2017 at 19:33