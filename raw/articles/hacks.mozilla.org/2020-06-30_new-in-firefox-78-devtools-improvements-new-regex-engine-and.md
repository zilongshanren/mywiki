---
title: 'New in Firefox 78: DevTools improvements, new regex engine, and abundant web
  platform updates – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2020/06/new-in-firefox-78/
author: Florian Scholz
published: '2020-06-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A new stable Firefox version rolls out today, providing new features for web developers. A new regex engine, updates to the ECMAScript Intl API, new CSS selectors, enhanced support for WebAssembly, and many improvements to the Firefox Developer Tools await you.

This blog post provides merely a set of highlights; for all the details, check out the following:

## Developer tool improvements

### Source-mapped variables, now also in Logpoints

With our improvements over the [recent](https://hacks.mozilla.org/2019/05/faster-smarter-javascript-debugging-in-firefox/) [releases](https://hacks.mozilla.org/2020/06/new-in-firefox-77-devtool-improvements-and-web-platform-updates/), debugging your projects with source maps will feel more reliable and faster than ever. But there are more capabilities that we can squeeze out of source maps. Did you know that Firefox’s Debugger also maps variables back to their original name? This especially helps babel-compiled code with changed variable names and added helper variables. To use this feature, pause execution and enable the “Map” option in the Debugger’s “Scopes” pane.

As a hybrid between the worlds of the DevTools Console and Debugger, [Logpoints](https://developer.mozilla.org/en-US/docs/Tools/Debugger/Set_a_logpoint) make it easy to add console logs to live code–or any code, once you’ve added them to your toolbelt. New in Firefox 75, original variable names in Logpoints are mapped to the compiled scopes, so references will always work as expected.

To make mapping scopes work, ensure that your source maps are [correctly generated](https://sourcemaps.io/) and include enough data. In [Webpack](https://webpack.js.org/configuration/devtool/) this means avoid the “cheap” and “nosources” options for the “devtools” configuration.

### Promises and frameworks error logs get more detailed

Uncaught promise errors are critical in modern asynchronous JavaScript, and even more so in frameworks like [Angular](https://angular.io/). In Firefox 78, you can expect to see all details for thrown errors show up properly, including their name and stack:

The implementation of this functionality was only possible through the close collaboration between the [SpiderMonkey](https://twitter.com/SpiderMonkeyJS) engineering team and a contributor, [Tom Schuster](https://twitter.com/evilpies). We are investigating how to improve error logging further, so please [let us know](https://bugzilla.mozilla.org/enter_bug.cgi?product=DevTools&component=Console) if you have suggestions.

### Monitoring failed request issues

Failed or blocked network requests come in many varieties. Resources may be blocked by tracking protection, add-ons, CSP/CORS security configurations, or flaky connectivity, for example. A resilient web tries to gracefully recover from as many of these cases as possible automatically, and an improved Network monitor can help you with debugging them.

Firefox 78 provides detailed reports in the Network panel for requests blocked by [Enhanced Tracking Protection](https://support.mozilla.org/en-US/kb/enhanced-tracking-protection-firefox-desktop), [add-ons](https://addons.mozilla.org/en-US/firefox/search/?category=privacy-security&sort=recommended%2Cusers&type=extension), and [CORS](https://developer.mozilla.org/docs/Web/HTTP/CORS).

### Quality improvements

#### Faster DOM navigation in Inspector

Inspector now opens and navigates a lot faster than before, particularly on sites with many [CSS custom properties](https://developer.mozilla.org/docs/Web/CSS/Using_CSS_custom_properties). Some modern CSS frameworks were especially affected by slowdowns in the past. If you see other cases where Inspector isn’t as fast as expected, [please report a performance issue](https://developer.mozilla.org/docs/Mozilla/Performance/Reporting_a_Performance_Problem). We really appreciate your help in reporting performance issues so that we can keep improving.

#### Remotely navigate your Firefox for Android for debugging

[Remote debugging](https://developer.mozilla.org/docs/Tools/about:debugging#Setup_tab)’s new navigation elements make it more seamless to test your content for mobile with the forthcoming [new edition of Firefox for Android](https://play.google.com/store/apps/details?id=org.mozilla.fenix). After hooking up the phone via USB and connecting remote debugging to a tab, you can navigate and refresh pages from your desktop.

### Early-access DevTools features in Developer Edition

[Developer Edition](https://www.mozilla.org/firefox/developer/) is Firefox’s pre-release channel. You get early access to tooling and platform features. Its settings enable more functionality for developers by default. We like to bring new features quickly to Developer Edition to gather your feedback, including the following highlights.

#### Async stacks in Console & Debugger

We’ve built new functionality to better support async stacks in the Console and Debugger, extending stacks with information about the events, timers, and promises that lead the execution of a specific line of code. We have been improving asynchronous stacks for a while now, based on early feedback from developers using [Firefox DevEdition](https://www.mozilla.org/firefox/developer/). In Firefox 79, we expect to enable this feature across all release channels.

![Async stacks add promise execution for both Console and Debugger](../../assets/ab2ea499890841fa.png)


#### Console shows failed requests

Network requests with 4xx/5xx status codes now log as errors in the Console by default. To make them easier to understand, each entry can be expanded to view embedded network details.

## Web platform updates

### New CSS selectors :is and :where

Version 78 sees Firefox add support for the [ :is()](https://developer.mozilla.org/docs/Web/CSS/:is) and

[pseudo-classes, which allow you to present a list of selectors to the browser. The browser will then apply the rule to](https://developer.mozilla.org/docs/Web/CSS/:where)

`:where()`

*any*element that matches

*one*of those selectors. This can be useful for reducing repetition when writing a selector that matches a large number of different elements. For example:

```
header p, main p, footer p,
header ul, main ul, footer ul { … }
```


Can be cut down to

`:is(header, main, footer) :is(p, ul) { … }`


Note that `:is()`

is not particularly a new thing—it has been supported for a while in various browsers. Sometimes this has been with a prefix and the name any (e.g. `:-moz-any`

). Other browsers have used the name `:matches()`

. `:is()`

is the final standard name that the CSSWG agreed on.

`:is()`

and `:where()`

basically do the same thing, but what is the difference? Well, `:is()`

counts towards the specificity of the overall selector, taking the specificity of its most specific argument. However, `:where()`

has a specificity value of 0 — it was introduced to provide a solution to the problems found with :is() affecting specificity.

What if you want to add styling to a bunch of elements with `:is()`

, but then later on want to override those styles using a simple selector? You won’t be able to because class selectors have a higher specificity. This is a situation in which `:where()`

can help. See our [ :where() example](https://developer.mozilla.org/docs/Web/CSS/:where#Examples) for a good illustration.

### Styling forms with CSS :read-only and :read-write

At this point, HTML forms have a large number of pseudo-classes available to style inputs based on different states related to their validity — whether they are required or optional, whether their data is valid or invalid, and so on. You can find a lot more information in our [UI pseudo-classes article](https://developer.mozilla.org/docs/Learn/Forms/UI_pseudo-classes).

In this version, Firefox has enabled support for the non-prefixed versions of [ :read-only](https://developer.mozilla.org/docs/Web/CSS/:read-only) and

[. As their name suggests, they style elements based on whether their content is editable or not:](https://developer.mozilla.org/docs/Web/CSS/:read-write)

`:read-write`

```
input:read-only, textarea:read-only {
border: 0;
box-shadow: none;
background-color: white;
}
textarea:read-write {
box-shadow: inset 1px 1px 3px #ccc;
border-radius: 5px;
}
```


(*Note: Firefox has supported these pseudo-classes with a -moz- prefix for a long time now.*)

You should be aware that these pseudo-classes are not limited to form elements. You can use them to style any element based on whether it is editable or not, for example a `<p>`

element with or without `contenteditable`

set:

```
p:read-only {
background-color: red;
color: white;
}
p:read-write {
background-color: lime;
}
```


### New regex engine

Thanks to the [RegExp engine in SpiderMonkey](https://hacks.mozilla.org/2020/06/a-new-regexp-engine-in-spidermonkey/), Firefox now supports all new regular expression features introduced in ECMAScript 2018, including lookbehinds (positive and negative), the `dotAll`

flag, Unicode property escapes, and named capture groups.

Lookbehind and negative lookbehind [assertions](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Regular_Expressions/Assertions) make it possible to find patterns that are (or are not) preceded by another pattern. In this example, a negative lookbehind is used to match a number only if it is not preceded by a minus sign. A positive lookbehind would match values not preceded by a minus sign.

```
'1 2 -3 0 -5'.match(/(?<!-)\d+/g);
// → Array [ "1", "2", "0" ]
'1 2 -3 0 -5'.match(/(?<=-)\d+/g);
// → Array [ "3", "5" ]
```


[Unicode property escapes](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Regular_Expressions/Unicode_Property_Escapes) are written in the form `\p{…}`

and `\{…}`

. They can be used to match any decimal number in Unicode, for example. Here’s a unicode-aware version of `\d`

that matches any Unicode decimal number instead of just the ASCII numbers 0-9.

```
const regex = /^\p{Decimal_Number}+$/u;
```


[Named capture groups](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Regular_Expressions/Groups_and_Ranges) allow you to refer to a certain portion of a string that a regular expression matches, as in:

```
let re = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/u;
let result = re.exec('2020-06-30');
console.log(result.groups);
// → { year: "2020", month: "06", day: "30" }
```


### ECMAScript Intl API updates

Rules for formatting lists vary from language to language. Implementing your own proper list formatting is neither straightforward nor fast. Thanks to the new [ Intl.ListFormat](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/ListFormat) API, the JavaScript engine can now format lists for you:

```
const lf = new Intl.ListFormat('en');
lf.format(["apples", "pears", "bananas"]):
// → "apples, pears, and bananas"
const lfdis = new Intl.ListFormat('en', { type: 'disjunction' });
lfdis.format(["apples", "pears", "bananas"]):
// → "apples, pears, or bananas"
```


Enhanced language-sensitive number formatting as defined in the [Unified NumberFormat proposal](https://github.com/tc39/proposal-unified-intl-numberformat) is now fully implemented in Firefox. See the [ NumberFormat constructor](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat) documentation for the new options available.

### ParentNode.replaceChildren

Firefox now supports [ ParentNode.replaceChildren()](https://developer.mozilla.org/docs/Web/API/ParentNode/replaceChildren), which replaces the existing children of a

`Node`

with a specified new set of children. This is typically represented as a `NodeList`

, such as that returned by [.](https://developer.mozilla.org/docs/Web/API/ParentNode/querySelectorAll)

`Document.querySelectorAll()`

This method provides an elegant way to empty a node of children, if you call `replaceChildren()`

with no arguments. It also is a nice way to shift nodes from one element to another. For example, in this case, we use two buttons to transfer selected options from one `<select>`

box to another:

```
const noSelect = document.getElementById('no');
const yesSelect = document.getElementById('yes');
const noBtn = document.getElementById('to-no');
const yesBtn = document.getElementById('to-yes');
yesBtn.addEventListener('click', () => {
const selectedTransferOptions = document.querySelectorAll('#no option:checked');
const existingYesOptions = document.querySelectorAll('#yes option');
yesSelect.replaceChildren(...selectedTransferOptions, ...existingYesOptions);
});
noBtn.addEventListener('click', () => {
const selectedTransferOptions = document.querySelectorAll('#yes option:checked');
const existingNoOptions = document.querySelectorAll('#no option');
noSelect.replaceChildren(...selectedTransferOptions, ...existingNoOptions);
});
```


You can see the full example at [ ParentNode.replaceChildren()](https://developer.mozilla.org/docs/Web/API/ParentNode/replaceChildren).

### WebAssembly multi-value support

[Multi-value](https://github.com/WebAssembly/multi-value) is a proposed extension to core WebAssembly that enables functions to return many values, and enables instruction sequences to consume and produce multiple stack values. The article [Multi-Value All The Wasm!](https://hacks.mozilla.org/2019/11/multi-value-all-the-wasm/) explains what this means in greater detail.

### WebAssembly large integer support

WebAssembly now supports import and export of 64-bit integer function parameters (i64) using [ BigInt](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/BigInt) from JavaScript.

## WebExtensions

We’d like to highlight three changes to the WebExtensions API for this release:

- When using
, a filter that limits based on tab id or window id is now correctly applied. This is useful for add-ons that want to provide proxy functionality in just one window.`proxy.onRequest`

[Clicking within the context menu](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/menus/onClicked)from the “all tabs” dropdown now passes the appropriate tab object. In the past, the active tab was erroneously passed.- When using
[downloads.download](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/downloads/download)with the`saveAs`

option, the recently used directory is now remembered. While this data is not available to developers, it is very convenient to users.

## TLS 1.0 and 1.1 removal

Support for the[ Transport Layer Security](https://developer.mozilla.org/docs/Web/Security/Transport_Layer_Security) (TLS) protocol’s version 1.0 and 1.1, has been dropped from all browsers as of Firefox 78 and Chrome 84. Read [TLS 1.0 and 1.1 Removal Update](https://hacks.mozilla.org/2019/05/tls-1-0-and-1-1-removal-update/) for the previous announcement and what actions to take if you are affected.

## Firefox 78 is an ESR release

Firefox follows a rapid release schedule: every four weeks we release a new version of Firefox.

In addition to that, we provide a new [Extended Support Release (ESR)](https://www.mozilla.org/en-US/firefox/organizations/) for enterprise users once a year. Firefox 78 ESR includes all of the enhancements since the last ESR (Firefox 68), along with many new features to make your enterprise deployment easier.

A noteworthy feature: In previous ESR versions, [Service workers](https://developer.mozilla.org/docs/Web/API/Service_Worker_API) (and the [ Push API](https://developer.mozilla.org/docs/Web/API/Push_API)) were disabled. Firefox 78 is the first ESR release to support them. If your enterprise web application uses [AppCache](https://developer.mozilla.org/docs/Web/HTML/Using_the_application_cache) to provide offline support, you should migrate to these new APIs as soon as possible as AppCache will not be available in the next major ESR in 2021.

Firefox 78 is the last supported Firefox version for macOS users of OS X 10.9 Mavericks, OS X 10.10 Yosemite and OS X 10.11 El Capitan. These users will be moved to the Firefox ESR channel by an application update. For more details, see the [Mozilla support page](https://support.mozilla.org/en-US/kb/macos-users-esr).

See also the [release notes for Firefox for Enterprise 78](https://support.mozilla.org/en-US/kb/firefox-enterprise-78-release-notes).

## About
[
Florian Scholz ](https://developer.mozilla.org)

Florian is the Content Lead for MDN Web Docs, writes about Web platform technologies and researches browser compatibility data. He lives in Bremen, Germany.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.