---
title: 'Firefox 67: Dark Mode CSS, WebRender, and more – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2019/05/firefox-67-dark-mode-css-webrender/
author: Dan Callahan
published: '2019-05-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 67 is available today, bringing a faster and better [JavaScript debugger](https://hacks.mozilla.org/2019/05/faster-smarter-javascript-debugging-in-firefox/), support for CSS [ prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme) media queries, and the initial debut of

[WebRender](https://hacks.mozilla.org/2017/10/the-whole-web-at-maximum-fps-how-webrender-gets-rid-of-jank/)in stable Firefox.

These are just the highlights. For complete information, see:

**CSS Color Scheme Queries**

New in Firefox 67, the [ prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme) media feature allows sites to adapt their styles to match a user’s preference for dark or light color schemes, a choice that’s begun to appear in operating systems like

[Windows](https://blogs.windows.com/windowsexperience/2019/04/01/windows-10-tip-dark-theme-in-file-explorer/),

[macOS](https://developer.apple.com/design/human-interface-guidelines/macos/visual-design/dark-mode/)and

[Android](https://www.theverge.com/2019/5/7/18530599/google-android-q-features-hands-on-dark-mode-gestures-accessibility-io-2019). As an example of what this looks like in the real world,

[Bugzilla](https://bugzilla.mozilla.org/show_bug.cgi?id=188761)uses

`prefers-color-scheme`

to trigger a [brand new dark theme](https://twitter.com/BugzillaUX/status/1112516874531540992)if the user has set that preference.

The `prefers-color-scheme`

media feature is currently supported in Firefox and Safari, with support in Chrome expected [later this year](https://twitter.com/tomayac/status/1121661549242773505).

Additionally, the [ revert](https://developer.mozilla.org/en-US/docs/Web/CSS/revert) keyword is now supported, making it possible to revert one or more CSS property values back to their original values specified by the user agent’s default styles (or by a custom user stylesheet if one is set). Defined in

[Cascading and Inheritance Level 4](https://drafts.csswg.org/css-cascade/#default),

`revert`

is also supported by Safari.**WebRender’s Stable Debut**

Nearly four years ago we started work on a [new rendering architecture](https://hacks.mozilla.org/2017/10/the-whole-web-at-maximum-fps-how-webrender-gets-rid-of-jank/) for Firefox with the goal of better utilizing modern graphics hardware. Today, we’re beginning to [gradually enable](https://bugzilla.mozilla.org/show_bug.cgi?id=1541488) WebRender for users on Windows 10 with qualified hardware. This marks the first time that WebRender has been enabled outside of Nightly and Beta builds of Firefox, and we hope to expand the supported platforms in future releases.

You can read more about WebRender in [The whole web at maximum FPS: How WebRender gets rid of jank](https://hacks.mozilla.org/2017/10/the-whole-web-at-maximum-fps-how-webrender-gets-rid-of-jank/).

**More Capable DevTools**

Firefox 67 and 68 [Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) bring enormous improvements to Firefox’s JavaScript Debugger. Discover faster load times, amazing support for source maps, more predictable breakpoints, brand new logpoints, and much more.

We’ve collected the Debugger improvements in their own article: [ Faster, Smarter JavaScript Debugging in Firefox DevTools](https://hacks.mozilla.org/2019/05/faster-smarter-javascript-debugging-in-firefox/).

In addition to the Debugger, the Web Console saw numerous updates, including [greater keyboard accessibility](https://bugzilla.mozilla.org/show_bug.cgi?id=1424159) and support for importing modules into the current page.

We’ve also [removed or deprecated](https://developer.mozilla.org/en-US/docs/Tools/Deprecated_tools) a few seldom-used and experimental tools, including the Canvas Debugger, Shader Editor, Web Audio Inspector, and WebIDE.

**Browser Features**

**Side-by-Side Profiles**

Firefox now defaults to using [different profiles for each installed version](https://blog.nightly.mozilla.org/2019/01/14/moving-to-a-profile-per-install-architecture/), making it easier than ever to run multiple copies of Firefox side-by-side.

![The macOS dock showing Firefox, Firefox Developer Edition, and Firefox Nightly all running simultaneously](../../assets/a28ed995bce52280.png)


In addition, the browser will warn you if you try to open a newer profile with an older version of Firefox, as such mismatches can occasionally lead to data loss. This protection can be bypassed with the new `-allow-downgrade`

command line argument.

**Enhanced Privacy Controls**

Firefox 67 better protects your privacy online with new Content Blocking options to avoid known cryptominers and fingerprinters.

You also have more control over your extensions, which can be ![Screenshot of the new Content Blocking options: Cryptominer and Fingerprinter blocking](../../assets/33e444c1b3380d09.png)


[prevented from running in private browsing windows](https://support.mozilla.org/en-US/kb/extensions-private-browsing).

![Screenshot of uBlock Origin's settings with a banner reading "Allowed in Private Windows"](../../assets/49f8256648109af4.png)

`about:addons`

.

**Easier Access to Firefox Accounts and Saved Passwords**

We’re working hard to make Firefox Accounts more useful and discoverable this year, starting with a new [default icon](https://blog.mozilla.org/services/2019/04/16/making-firefox-accounts-more-transparent-in-firefox/) in the browser toolbar.

The new icon indicates whether or not you’re signed into a Firefox Account, and makes it easy to perform actions like sending tabs to other devices or manually triggering a sync. Like other toolbar buttons, you can freely move or hide the Firefox Account button according to your preferences.

Check out the [many improvements to Firefox’s built-in password manager](https://matthew.noorenberghe.com/blog/2019/05/password-manager-improvements-firefox-67), including quicker access to your list of saved credentials. You can either click on the new “Logins and Passwords” item in the main menu, or the new “View Saved Logins” button in the login autocomplete popup.

This can be especially useful if you need to look up or edit a login outside of the normal autofill workflow. And, if you use Firefox Sync, you can access your saved passwords with the [Firefox Lockbox](https://lockbox.firefox.com/) app for Android or iOS.

**Web Platform Features**

**Support for legacy FIDO U2F APIs**

We’ve enabled [legacy FIDO U2F support](https://blog.mozilla.org/security/2019/04/04/shipping-fido-u2f-api-support-in-firefox/) to improve backwards compatibility with sites that have not yet upgraded to its standards-based successor, [WebAuthn](https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API).

These APIs make it possible for websites to authenticate users with strong, hardware-backed authentication mechanisms like [USB security keys](https://en.wikipedia.org/wiki/Universal_2nd_Factor) or [Windows Hello](https://blog.mozilla.org/security/2019/03/19/passwordless-web-authentication-support-via-windows-hello/).

**AV1 on Windows, Linux, and macOS**

Firefox now supports AV1, a [next-generation video codec](https://research.mozilla.org/av1-media-codecs/), on all major desktop platforms. Also, playback on those platforms is now powered by [dav1d](https://code.videolan.org/videolan/dav1d), a [faster and more efficient](http://www.jbkempf.com/blog/post/2018/First-release-of-dav1d) AV1 decoder developed by the VideoLAN and FFmpeg communities.

**JavaScript: **`String.prototype.matchAll()`

and Dynamic Imports

`String.prototype.matchAll()`

and Dynamic ImportsFirefox joins Chrome in supporting the [ matchAll()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/matchAll) String prototype method, which takes a regular expression and returns an iterator of all matching text, including capturing groups.

The [ import()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import) function can now be used to dynamically load JavaScript modules, similarly to how the static import statement works. Now it’s possible to load modules conditionally or in response to user actions, though such imports are harder to reason about for build tools that use static analysis for optimizations like

[tree shaking](https://developer.mozilla.org/en-US/docs/Glossary/Tree_shaking).

**And more awaits!**

This release includes plenty of other fixes and enhancements not covered here, and lots more to come. So what are you waiting for? [Download Firefox 67](https://www.mozilla.org/firefox/new/) today and let us know what you think!

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 20 comments

rugkMay 21st, 2019 at 09:45Wellington Torrejais da SIlvaMay 21st, 2019 at 13:33PhilippeVayMay 22nd, 2019 at 08:33Dan CallahanMay 25th, 2019 at 03:31Brian KussMay 23rd, 2019 at 05:03Dan CallahanMay 25th, 2019 at 03:33J RedheadMay 23rd, 2019 at 18:07Dan CallahanMay 24th, 2019 at 02:33J RedheadMay 26th, 2019 at 00:42John AMay 23rd, 2019 at 22:24Dan CallahanMay 24th, 2019 at 03:18MohamedMay 24th, 2019 at 00:34Dan CallahanMay 24th, 2019 at 02:49Giovanni BarrantesMay 24th, 2019 at 08:56Dan CallahanMay 25th, 2019 at 03:41ShawnMay 26th, 2019 at 03:48Dan CallahanMay 28th, 2019 at 04:01A_AjrMay 26th, 2019 at 07:51Dan CallahanMay 28th, 2019 at 04:00AnthonyMay 26th, 2019 at 09:43