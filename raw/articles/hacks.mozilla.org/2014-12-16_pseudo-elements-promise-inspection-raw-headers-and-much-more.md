---
title: Pseudo elements, promise inspection, raw headers, and much more – Firefox Developer
  Edition 36 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/12/pseudo-elements-promise-inspection-raw-headers-and-much-more-firefox-developer-edition-36/
author: Brian Grinstead
published: '2014-12-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 36 was just uplifted to the Developer Edition channel, so let’s take a look at the most important Developer Tools changes in this release. We will also cover some changes from Firefox 35 since it was released shortly before the initial [Developer Edition announcement](https://hacks.mozilla.org/2014/11/mozilla-introduces-the-first-browser-built-for-developers-firefox-developer-edition). There is a lot to talk about, so let’s get right to it.

## Inspector

You can now inspect ::before and ::after pseudo elements. They behave like other elements in the markup tree and inspector sidebars. (35, [development notes]( http://bugzil.la/920141))

There is a new “Show DOM Properties” context menu item in the markup tree. (35, [development notes](http://bugzil.la/992679), [documentation about this feature](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector#Element_popup_menu_2) on MDN)

The box model highlighter now works on remote targets, so there is a full-featured highlighter even when working with pages on Firefox for Android or apps on Firefox OS. (36, [development notes](http://bugzil.la/985597), and [technical documentation](https://wiki.mozilla.org/DevTools/Highlighter) for building your own custom highlighter)

Shadow DOM content is now visible in the markup tree; note that you will need to set dom.webcomponents.enabled to true to test this feature (36, [development notes](http://bugzil.la/1079185), and see [bug 1053898](http://bugzil.la/1053898) for more work in this space).

We borrowed a useful feature from Firebug and are now allowing more paste options when right clicking a node in the markup tree. (36, [development notes](http://bugzil.la/1095521), [documentation about this feature](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector#Element_popup_menu_2) on MDN)

Some more changes to the Inspector included in Firefox 35 & 36:

- Deleting a node now selects the previous sibling instead of the parent (36,
[development notes](http://bugzil.la/1094622)) - There is higher contrast for the currently hovered node in the markup view (36,
[development notes](http://bugzil.la/1102084)) - Hover over a CSS selector in the computed view to highlight all the nodes that match that selector on the page. (35,
[development notes](http://bugzil.la/1059360))

## Debugger / Console

[DOM Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) are now inspectable. You can inspect the promises state and value at any moment. (36, [development notes](http://bugzil.la/1033153))

The debugger now recognizes and works with eval’ed sources. (36, [development notes](http://bugzil.la/905700))

Eval’ed sources support the `//# sourceURL=path.js`

syntax, which will make them appear as a normal file in the debugger and in stack traces reported by `Error.prototype.stack`

. See this post: [http://fitzgeraldnick.com/weblog/59/](http://fitzgeraldnick.com/weblog/59/) for much more information. (36, [development notes](http://bugzil.la/1107541), [more development notes](http://bugzil.la/583083))

Console statements now include the column number they originated from. (36, [development notes](http://bugzil.la/684096))

## WebIDE

You are now able to connect to Firefox for Android from the WebIDE. See documentation for [debugging firefox for android](https://developer.mozilla.org/en-US/docs/Tools/Remote_Debugging/Debugging_Firefox_for_Android_with_WebIDE) on MDN. (36, [development notes](http://bugzil.la/982890)).

We also made some changes to improve the user experience in the WebIDE:

- Bring up developer tools by default when I select a runtime app / tab (35,
[development notes](http://bugzil.la/1055279)) - Re-select project on connect if last project is runtime app (35,
[development notes](http://bugzil.la/1055666)) - Auto-select and connect to last used runtime if available (35,
[development notes](http://bugzil.la/1045660)) - Font resizing (36,
[development notes](http://bugzil.la/1027817)) - You can now adding a hosted app project by entering the base URL (eg: “http://example.com”) instead of requiring the full path to the manifest.webapp file (35,
[development notes](http://bugzil.la/913711))

## Network Monitor

We added a plain request/response headers view to make it easier to view and copy the raw headers on a request. (35, [development notes](http://bugzil.la/859133))

Here is a list of all the [bugs resolved for Firefox 35](http://mzl.la/1oltPdy) and all the [bugs resolved for Firefox 36](http://mzl.la/1tS0R2i).

Do you have feedback, bug reports, feature requests, or questions? As always, you can comment here, [add/vote for ideas on UserVoice](http://mzl.la/devtools) or get in touch with the team at [@FirefoxDevTools on Twitter](https://twitter.com/FirefoxDevTools).

## 3 comments

MarkDecember 16th, 2014 at 13:43Brian GrinsteadDecember 18th, 2014 at 22:31FlimmJanuary 15th, 2015 at 03:14