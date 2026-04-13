---
title: Firefox 73 is upon us – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/02/firefox-73-is-upon-us/
author: Chris Mills
published: '2020-02-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Another month, another new browser release! Today we’ve released Firefox 73, with useful additions that include CSS and JavaScript updates, and numerous DevTools improvements.

Read on for the highlights. To find the full list of additions, check out the following links:

**Note**: Until recently, this post mentioned the new form method [ requestSubmit()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/requestSubmit) being enabled in Firefox 73. It has come to light that

`requestSubmit()`

is in fact currently behind a flag, and targetted for a release in Firefox 75. Apologies for the error. *(Updated Friday, 14 February.)*

## Web platform language features

Our latest Firefox offers a fair share of new web platform additions; let’s review the highlights now.

We’ve added to [CSS logical properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Logical_Properties), with [ overscroll-behavior-block](https://developer.mozilla.org/en-US/docs/Web/CSS/overscroll-behavior-block) and

[.](https://developer.mozilla.org/en-US/docs/Web/CSS/overscroll-behavior-inline)

`overscroll-behavior-inline`

These new properties provide a logical alternative to [ overscroll-behavior-x](https://developer.mozilla.org/en-US/docs/Web/CSS/overscroll-behavior-x) and

[, which allow you to control the browser’s behavior when the boundary of a scrolling area is reached.](https://developer.mozilla.org/en-US/docs/Web/CSS/overscroll-behavior-y)

`overscroll-behavior-y`

The `yearName`

and `relatedYear`

fields are now available in the [ DateTimeFormat.prototype.formatToParts()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DateTimeFormat/formatToParts) method. This enables useful formatting options for CJK (Chinese, Japanese, Korean) calendars.

## DevTools updates

There are several interesting DevTools updates in this release. Upcoming features can be previewed now in [Firefox DevEdition](https://www.mozilla.org/firefox/developer/).

We continually survey DevTools users for input, often from our [@FirefoxDevTools](https://twitter.com/FirefoxDevTools/) Twitter account. Many useful updates come about as a result. For example, thanks to [your feedback](https://twitter.com/FirefoxDevTools/status/1205200368210104320) on one of those surveys, it is [now possible](https://bugzilla.mozilla.org/show_bug.cgi?id=1602152) to copy cleaner CSS snippets out of the [Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector)’s [Changes panel](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_and_edit_CSS#Track_changes). The `+`

and `-`

signs in the output are no longer part of the copied text.

### Solid & Fast

The DevTools engineering work for this release focused on pushing performace forward. We made the process of collecting fast-firing requests in the [Network](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor) panel [ a lot more lightweight](https://twitter.com/FirefoxDevTools/status/1204625601627213825), which made the UI snappier. In the same vein, large source-mapped scripts now [load much, much faster](https://bugzilla.mozilla.org/show_bug.cgi?id=1598180#c6) in the [Debugger](https://developer.mozilla.org/en-US/docs/Tools/Debugger) and cause less strain on the [Console](https://developer.mozilla.org/en-US/docs/Tools/Web_Console) as well.

Loading the right sources in the Debugger is not straightforward when the DevTools are opened on a loaded page. In fact, modern browsers are too good at purging original files when they are parsed, rendered, or executed, and no longer needed. Firefox 73 makes script loading a lot more reliable and ensures you get the right file to debug.

### Smarter Console

Console script authoring and logging gained some quality of life improvements. To date, [CORS network errors](https://wiki.developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors) have been shown as warnings, making them too easy to overlook when resources could not load. Now they are correctly reported as errors, not warnings, to give them the visibility they deserve.

Variables declared in the expression [will now](https://bugzilla.mozilla.org/show_bug.cgi?id=1604411) be included in the autocomplete. This change makes it easier to author longer snippets in the [multi-line editor](https://developer.mozilla.org/en-US/docs/Tools/Web_Console/The_command_line_interpreter#Multi-line_mode). Furthermore, the DevTools setting for auto-closing brackets is now working in the Console as well, bringing you closer to the experience of authoring in an IDE.

Did you know that [console logs can be styled](https://developer.mozilla.org/en-US/docs/Web/API/Console#Styling_console_output) using backgrounds? For even more variety, you can add images, using data-uris. This feature is now [working in Firefox](https://bugzilla.mozilla.org/show_bug.cgi?id=1579663), so don’t hesitate to get creative. For example, we tried this in one of our Fetch examples:

```
console.log('There has been a problem with your fetch operation: %c' +
e.message, 'color: red; padding: 2px 2px 2px 20px; background: yellow 3px no-repeat
url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAACXBIWXMAAA
7EAAAOxAGVKw4bAAAApUlEQVQoz5WSwQ3DIBAE50wEEkWkABdBT+bhNqwoldBHJF58kzryIp+zgwiK5JX2w+
2xdwugMMZ4IAIZeCszELX2hYhcgQIkEQnOOe+c8yISgAQU1Rw3F2BdlmWig56tQNmdIpA68Qbcu6akWrJat7
gp27EDkCdgttY+uoaX8oBq5gsDiMgToNY6Kv+OZIzxfZT7SP+W3oZLj2JtHUaxnnu4s1/jA4NbNZ3AI9YEA
AAAAElFTkSuQmCC);');
```


And got the following result:

![styled console message with yellow highlighter effect](../../assets/08ea64e283a30b1d.png)


We’d like to thank Firefox DevTools contributor Edward Billington for the data-uri support!

We now show arguments by default. We believe this makes logging JavaScript functions a bit more intuitive.

And finally for this section, when you perform a text or regex search in the Console, you can negate a search item by prefixing it with ‘-’ (i.e. return results **not** including this term).

### WebSocket Inspector improvements

The WebSocket inspector that [shipped in Firefox 71](https://hacks.mozilla.org/2019/10/firefoxs-new-websocket-inspector/) now nicely prints [WAMP](https://wamp-proto.org/)-formatted messages (in JSON, MsgPack, and CBOR flavors).

You won’t needlessly wait for updates, as the Inspector now also indicates when a WebSocket connection is closed.

A big thanks to contributor Elad Zelingher for implementing the WAMP support, and to saihemanth9019 for the WebSocket closed indicator!

## New (power-)user features

We wanted to mention a couple of nice power user *Preferences* features dropping in Firefox 73.

First of all, the *General* tab in *Preferences* now has a *Zoom* tool. You can use this feature to set the magnification level applied to all pages you load. You can also specify whether all page contents should be enlarged, or only text. We know this is a hugely popular feature because of the number of extensions that offer this functionality. Selective zoom as a native feature is a huge boon to users.

The * DNS over HTTPS* control in the

*Network Settings*tab includes a new provider option,

*NextDNS*. Previously, Cloudflare was the only available option.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 19 comments

Virendra kumarFebruary 11th, 2020 at 09:10Ceremy JorbynFebruary 11th, 2020 at 18:14Michael M.February 12th, 2020 at 01:49Michael JonesFebruary 12th, 2020 at 05:06Jon PaddockFebruary 17th, 2020 at 22:41Michael JonesFebruary 12th, 2020 at 05:15Trevor BaairdFebruary 12th, 2020 at 07:49Chris MillsFebruary 12th, 2020 at 08:04Trevor BairdFebruary 13th, 2020 at 01:01Annika SFebruary 14th, 2020 at 10:43CHARLES BARTHOLOMEWFebruary 12th, 2020 at 13:57EddyFebruary 12th, 2020 at 18:47Tim RoweFebruary 13th, 2020 at 04:01YanFebruary 13th, 2020 at 08:14GregFebruary 13th, 2020 at 13:57GregFebruary 13th, 2020 at 14:13BFebruary 15th, 2020 at 03:44GregFebruary 16th, 2020 at 17:17User # 1,484,654,981March 4th, 2020 at 12:26