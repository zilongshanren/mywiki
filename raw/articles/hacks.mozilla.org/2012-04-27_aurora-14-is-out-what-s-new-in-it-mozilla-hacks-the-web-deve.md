---
title: Aurora 14 is out! What's new in it? – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/04/aurora-14-is-out-whats-new-in-it/
author: Jean-Yves Perrier
published: '2012-04-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We have just released Firefox Aurora 14, which includes a number of improvements. If all goes well, these features should be released in 12 weeks as part of Firefox 14.

## Highlights

There are a few of things we’d like to shine some extra light on here:

[Native Fullscreen Support](http://www.apple.com/macosx/whats-new/full-screen.html)in Mac OS X 10.7 “Lion”: Firefox can now use the native full-screen mode and button. It animates and behaves properly in that[mode](https://bugzilla.mozilla.org/show_bug.cgi?id=639705), like any other well-integrated application.- Great news for gamers! The
[Pointer Lock API](https://developer.mozilla.org/en/API/Pointer_Lock_API), sometimes called the Mouse Lock API, lets games better control the mouse, by removing the pointer and letting the application capture and handle the mouse move coordinates directly. - The four default ways to search — using the search bar, the address bar, the contextual menu, or the home page, now all use the
[Google https search service](https://bugzilla.mozilla.org/show_bug.cgi?id=633773)in Aurora. This increase the security of your searches. - The dev tools now allow easily inspecting pseudo-classes states: when hovering over an element with the dev tools activated, the contextual menu now lists the different states of the element, like :hover, :active, and :focus. When selecting one of these items, the element is
*locked*in the associated state and can be inspected. That feature was[already there in Aurora 13](http://www.youtube.com/watch?feature=player_embedded&v=wuZB6JA4dCU), but the interface to access it is now very convenient!

![The menu allowing the pseudo-class state to be locked on an element](../../assets/21df1f93122c6c63.png)




## List of improvements

Here is a (more or less) complete list of the improvements.

### DevTools

- New keyboard shortcuts have been
[added](https://bugzilla.mozilla.org/show_bug.cgi?id=729960)to the[Source Editor JS module](https://developer.mozilla.org/en/JavaScript_code_modules/source-editor.jsm)(used by the Scratchpad or the Style Editor) to quickly jump to the code block start and end. - Still in the
[Source Editor module](https://developer.mozilla.org/en/JavaScript_code_modules/source-editor.jsm),[it is now possible](https://bugzilla.mozilla.org/show_bug.cgi?id=739192)to add or remove a comment on a line or the current selection with one keystroke. - Beside the new pseudo-class inspector, several improvements
[have been made](https://bugzilla.mozilla.org/show_bug.cgi?id=717916)to the infobar which has now an inspect button to the left and a node menu to the right (for example, it may be used to set the pseudo-class state on the node!)

### DOM

- The
[Pointer Lock API](https://developer.mozilla.org/en/API/Pointer_Lock_API)has been implemented. - A proposal for the replacement of
[MutationEvents](http://www.w3.org/TR/DOM-Level-3-Events/#events-MutationEvent), introduced in DOM Level 2 but deprecated in DOM Events Level 3, has[landed](https://bugzilla.mozilla.org/show_bug.cgi?id=641821), prefixed: instead of events, an[API allowing callbacks to be registered](http://dvcs.w3.org/hg/domcore/raw-file/tip/Overview.html#mutation-observers)has been crafted. - New, with added performance,
[DOM bindings](http://jstenback.wordpress.com/2012/04/11/new-dom-bindings/)for non-list objects have[landed](https://bugzilla.mozilla.org/show_bug.cgi?id=740069). Currently[XMLHttpRequest](https://developer.mozilla.org/en/DOM/XMLHttpRequest)is the only non-list object using them. These bindings are often called the “Paris DOM bindings” as they were designed in that city. - The
`<a title="SVGSVGElement DOM Element" href="https://developer.mozilla.org/en/DOM/SVGSVGElement">SVGSVGElement</a>`

has been[fixed](https://bugzilla.mozilla.org/show_bug.cgi?id=740811)to be a DOM[Element](https://developer.mozilla.org/en/DOM/element). `HTMLProgressElement`

, the DOM object associated with the`<a href="https://developer.mozilla.org/en/HTML/Element/progress"><progress></a>`

HTML element, was a`<a href="https://developer.mozilla.org/en/DOM/HTMLFormElement">HTMLFormElement</a>`

. This was incorrect and has been[fixed](https://bugzilla.mozilla.org/show_bug.cgi?id=686913). It is a simple`<a href="https://developer.mozilla.org/en/DOM/HTMLElement">HTMLElement</a>`

now.

### Plugins

- Optionally, if the
`plugins.click_to_play`

preference is enabled in`about:config`

,[plugins](https://developer.mozilla.org/En/Plugins)will require an extra click to activate and start “playing” content.[This mode improves the security of the browser](http://msujaws.wordpress.com/2012/04/11/opting-in-to-plugins-in-firefox/)and may be extended in the future to be activated by default in some cases. When on,[site-specific permissions can be set.](http://msujaws.wordpress.com/2012/04/20/site-specific-permissions-for-firefox-opt-in-plugins/)

### Layout

[CSS](https://developer.mozilla.org/en/CSS/text-transform)and`text-transform`

properties have been updated to match the spec and now handle`font-variant`

[the Dutch IJ digraph](http://firefoxnightly.tumblr.com/post/20267585898/css-text-transform-updated-for-the-dutch-language), the Turkic[dotless and dotted i](http://en.wikipedia.org/wiki/Dotted_and_dotless_I), and[the Greek sigma lowercase characters](http://firefoxnightly.tumblr.com/post/21224535375/css-text-transform-updated-for-a-weird-greek-case)correctly. This is big improvement for writing on the Web in these languages!- Related to
[CSS transforms](https://developer.mozilla.org/En/CSS/Using_CSS_transforms), the`skew()`

function has been removed from the spec, so support has been removed from Firefox as well. It wasn’t a real skew function which designs the linear[shear mapping](http://en.wikipedia.org/wiki/Shear_mapping)transform and its effect is still achievable using[the](https://developer.mozilla.org/en/CSS/transform-function#matrix%28%29).`matrix()`

function - Directly viewed images now have a textured background.
- The character maps (cmap) have been optimized.
[Fonts with identical character coverage now share them](https://bugzilla.mozilla.org/show_bug.cgi?id=710727). This lets Firefox use less memory, about 0.5 MB on a desktop system with few fonts, and up to 1.8MB or more on systems with a lot of fonts. The more fonts that are installed, the greater the savings. This was done as a part of the[MemShrink](https://wiki.mozilla.org/Performance/MemShrink)project. [SVG](https://developer.mozilla.org/en/SVG)performance has been significantly[improved](https://bugzilla.mozilla.org/show_bug.cgi?id=734079).

### User Interface

- The popup bubble containing a link URL that appears on the bottom of the page when hovering over a link
[is now longer](https://bugzilla.mozilla.org/show_bug.cgi?id=632634)when the URL doesn’t fit in it. - As part of the
[Australis theme evolution project](http://people.mozilla.com/~shorlander/ux-presentation/ux-presentation.html), the navigation bar buttons have been[modified](https://bugzilla.mozilla.org/show_bug.cgi?id=734373)(on Windows only). - The identity block has been
[redesigned](https://bugzilla.mozilla.org/show_bug.cgi?id=742419). The favicon has been changed to show an icon describing the connection used: - The page is served unencrypted (http).
![Nav bar with http (unencrypted)](../../assets/8bfc3738925967b1.png)

- The page is served encrypted (via https) but some of its content comes from unencrypted servers.

- The page and its content is served encrypted (and the server uses a CV certificate).
![Nav bar with https and CV certificate](../../assets/b6924b348dcbb277.png)

- The page and its content is served encrypted (and the server uses an EV certificate).


### Network

- At launch, tabs are no longer loaded in the background. Instead,
[they are now loaded when first selected](https://bugzilla.mozilla.org/show_bug.cgi?id=711193), which improves response during the start-up of Firefox. This has been done as a part of the[Snappy](https://wiki.mozilla.org/Performance/Snappy)project.

### Others

- Both the
[Internet Explorer](https://bugzilla.mozilla.org/show_bug.cgi?id=710895)and[Safari migrators](https://bugzilla.mozilla.org/show_bug.cgi?id=710259)have been rewritten in JavaScript. Using asynchronous I/O, they don’t block the browser when they run and it improves their maintainability. This has been done as part of the[Snappy](https://wiki.mozilla.org/Performance/Snappy)project. - On Linux, the
[$LANG system variable](https://bugzilla.mozilla.org/show_bug.cgi?id=746148)is now used when not able to locate a given dictionary in another way. Useful for system-wide installed dictionaries. - For add-ons writers, the
[js-ctypes](https://developer.mozilla.org/en/Mozilla/js-ctypes)library has been extended.*Variadic ctypes functions*— that is, support for functions with a variable number of arguments — have been[added](https://bugzilla.mozilla.org/show_bug.cgi?id=554790). [Several bugs](https://bugzilla.mozilla.org/show_bug.cgi?id=680721)in our WebGL implementation have been fixed (and workarounds for some common driver bugs added). We are close to WebGL 1.0.1 conformance, but[your help is still needed](http://blog.mozilla.org/bjacob/2012/04/21/webgl-1-0-1-conformance-testing-part-2/).- Extra flexibility has been added to the
[Garbage Collector](http://en.wikipedia.org/wiki/Garbage_collector_%28computing%29)(GC): it could previously be applied on a single compartment or on all compartments. Now[it can also be applied on a set of compartments](https://bugzilla.mozilla.org/show_bug.cgi?id=716142). This will let it be launched in more cases in the future, leading to a finer control of memory and of GC pauses.

Note: [pdf.js](http://blog.mozilla.org/labs/2011/10/video-what-is-pdf-js/) and the [new panel-based Download Manager](http://firefoxnightly.tumblr.com/post/21343114308/the-new-download-manager-panel-is-there-at), though they landed on Nightly, have not been lifted to Aurora 14 as they need further polishing. Similarly, support of [GStreamer](http://gstreamer.freedesktop.org/) for videos, though it landed [last week](https://bugzilla.mozilla.org/show_bug.cgi?id=422540), has not been activated yet.

## About Jean-Yves Perrier

Jean-Yves is a program manager in the Developer Outreach team at Mozilla. Previous he was an MDN Technical Writer specialized in Web platform technologies (HTML, CSS, APIs), and for several years the MDN Content Lead.

## 39 comments

JithinApril 27th, 2012 at 18:22Jean-Yves PerrierApril 28th, 2012 at 07:31BorisApril 27th, 2012 at 21:09Jean-Yves PerrierApril 28th, 2012 at 07:31StuartApril 27th, 2012 at 22:19Stuart RobsonApril 27th, 2012 at 23:34Jean-Yves PerrierApril 28th, 2012 at 08:05pdApril 28th, 2012 at 02:34Jean-Yves PerrierApril 28th, 2012 at 07:55Benoit JacobApril 28th, 2012 at 21:13Jean-Yves PerrierApril 28th, 2012 at 22:05NameApril 29th, 2012 at 09:19dargxApril 29th, 2012 at 09:26AndriyApril 30th, 2012 at 03:06FerdinandJuly 17th, 2012 at 14:15Benoit JacobApril 30th, 2012 at 05:04Simon B.May 1st, 2012 at 01:46Jean-Yves PerrierMay 1st, 2012 at 22:12AnonymousMay 1st, 2012 at 07:02Janet SwisherMay 2nd, 2012 at 11:53Vadim MakeevMay 1st, 2012 at 12:26Jean-Yves PerrierMay 1st, 2012 at 22:10Vadim MakeevMay 2nd, 2012 at 06:10Vadim MakeevMay 2nd, 2012 at 06:13Janet SwisherMay 2nd, 2012 at 11:55Vadim MakeevMay 3rd, 2012 at 09:15BobMay 1st, 2012 at 12:33Jean-Yves PerrierMay 1st, 2012 at 22:11pecinta tanaman obat indonesiaMay 5th, 2012 at 23:25AndriyMay 7th, 2012 at 02:50Jean-Yves PerrierMay 7th, 2012 at 02:57AndriyMay 7th, 2012 at 03:40Jean-Yves PerrierMay 7th, 2012 at 04:04AndriyMay 8th, 2012 at 13:26Gervase MarkhamMay 10th, 2012 at 05:10cjrclJuly 4th, 2012 at 23:52jackJuly 17th, 2012 at 09:33FerdinandJuly 17th, 2012 at 14:19ssamJuly 30th, 2012 at 06:14