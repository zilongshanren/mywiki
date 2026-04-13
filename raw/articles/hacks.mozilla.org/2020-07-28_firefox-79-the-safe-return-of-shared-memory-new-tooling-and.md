---
title: 'Firefox 79: The safe return of shared memory, new tooling, and platform updates
  – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2020/07/firefox-79/
author: Florian Scholz
published: '2020-07-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A new stable version of Firefox brings July to a close with the return of shared memory! Firefox 79 also offers a new Promise method, more secure `target=_blank`

links, logical assignment operators, and other updates of interest to web developers.

This blog post provides merely a set of highlights; for all the details, check out the following:

## New in Developer Tools

First, we look at the new additions to the Firefox DevTools in version 79.

### JavaScript logging and debugging capabilities

#### Async stack traces everywhere

Modern JavaScript depends on promises, async/await, events, and timeouts to orchestrate complex scheduling between your code, libraries, and the browser. And yet, it can be challenging to debug async code to understand control and data flow. Operations are broken up over time. Async stack traces solve this by combining the live synchronous part of the stack with the part that is captured and asynchronous.

Now you can enjoy detailed async execution chains in the Firefox JavaScript Debugger’s call stack, Console errors, and Network initiators.

To make this work, the JavaScript engine captures the stack when a promise is allocated or when some async operation begins. Then the captured stack is appended to any new stacks captured.

#### Better debugging for erroneous network responses

Failing server requests can lead to a cascade of errors. Previously, you had to switch between the Console and Network panels to debug, or enable the *XHR/Requests* filters in the Console. With Firefox 79, the Console shows network requests with 4xx/5xx error status codes by default. In addition, the request/response details can be expanded to inspect the full details. These are also available in the Network Inspector.

*Tip:* To further debug, retry, or verify server-side changes, use the “Resend Request” context-menu option. It’s available in both the Console and Network panels. You can send a new request with the same parameters and headers. The additional “Edit and Resend” option is only available in the Network panel. It opens an editor to tweak the request before sending it.

#### Debugger highlights errors in code

Many debugging sessions start by jumping from a logged JavaScript error to the Debugger. To make this flow easier, errors are now highlighted in their corresponding source location in the Debugger. Furthermore, relevant details are shown on hover, in the context of the code, and paused variable state.

We’d like to say thanks to core contributor [Stepan Stava](https://bugzilla.mozilla.org/user_profile?user_id=652974), who is already building this feature out, further blurring the line between logging and debugging.

#### Restart frame in Call Stack

When you restart frames from the Debugger, the call stack moves the execution pointer to the top of the function. With the caveat that the state of variables is not reset, this allows time-traveling within the current call stack.

“Restart Frame” is now available as a context-menu option in the Debugger’s call stack. Again, we have [Stepan Stava](https://bugzilla.mozilla.org/user_profile?user_id=652974) to thank for this addition, which Debugger users will recognize from Chrome and VS Code.

#### Faster JavaScript debugging

Performance improvements in this release speed up debugging, particularly for projects with large files. We also fixed a bottleneck that affected eval-heavy code patterns, which will now just work.

### Inspector updates

#### Better source map references for SCSS and CSS-in-JS

We’ve improved source map handling across all panels, so that opening SCSS and CSS-in-JS sources from the Inspector now works more reliably. You can quickly jump from the rules definitions in the Inspector side panel to the original file in the [Style Editor](https://developer.mozilla.org/en-US/docs/Tools/Style_Editor).

#### New Inspect accessibility properties context menu

The [Accessibility Inspector](https://developer.mozilla.org/en-US/docs/Tools/Accessibility_inspector) is now always available in the browser context menu. allows you can open the element in the Accessibility panel directly, to inspect [ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA) properties and run audits.

### More tooling updates

- The “Disable Cache” option in the Network panel now also deactivates
[CORS preflight request](https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request)caching. This makes it easier to iterate on your[web security](https://developer.mozilla.org/en-US/docs/Web/Security)settings. - Contributor
[KC](https://bugzilla.mozilla.org/user_profile?user_id=657869)aligned the styling for blocked requests shown in Console with their appearance in the Network panel. [Richard Sherman](https://github.com/richorrichard)extended the reach of tooltips, which now describe the type and value for previewed object values across Console and Debugger.- To consolidate sidebar tabs,
[Farooq AR](https://farooqar.github.io/)moved Network’s WebSocket “Messages” tab into the “Response” tab. - Debugger’s references to “blackbox” were renamed “ignore”, to align wording with other tools and make it more inclusive. Thanks to
[Richard Sherman](https://github.com/richorrichard)for this update too!

## Web platform updates

### Implicit `rel=noopener`

with `target=_blank`

links

To prevent the DOM property [ window.opener](https://developer.mozilla.org/docs/Web/API/Window/opener) from being abused by untrusted third-party sites, Firefox 79 now automatically sets

`rel=noopener`

for all links that contain `target=_blank`

. Previously, you had to set `rel=noopener`

manually to make `window.opener = null`

for every link that uses `target=_blank`

. In case you need `window.opener`

, explicitly enable it using `rel=opener`

.### SharedArrayBuffer returns

At the start of 2018, [Shared Memory](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer) and high-resolution timers were effectively [disabled](https://blog.mozilla.org/security/2018/01/03/mitigations-landing-new-class-timing-attack/) in light of [Spectre](https://en.wikipedia.org/wiki/Spectre_(security_vulnerability)). In 2020, a new, more secure approach has been standardized to re-enable shared memory. As a baseline requirement, your document needs to be in a secure context. For top-level documents, you must set two headers to cross-origin isolate your document:

set to`Cross-Origin-Opener-Policy`

`same-origin`

.set to`Cross-Origin-Embedder-Policy`

`require-corp`

.

To check if cross-origin isolation has been successful, you can test against the [ crossOriginIsolated](https://developer.mozilla.org/docs/Web/API/WindowOrWorkerGlobalScope/crossOriginIsolated) property available to window and worker contexts:

```
if (crossOriginIsolated) {
// use postMessage and SharedArrayBuffer
} else {
// Do something else
}
```


Read more in the post [Safely reviving shared memory.](https://hacks.mozilla.org/2020/07/safely-reviving-shared-memory/)

### Promise.any support

The new [ Promise.any()](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise/any) method takes an iterable of

[objects and, as soon as one of the promises in the iterable fulfills, returns a single promise resolving to the value from that promise. Essentially, this method is the opposite of](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise)

`Promise`

[. Additionally,](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise/all)

`Promise.all()`

`Promise.any()`

is different from [. What matters is the order in which a promise is fulfilled, as opposed to which promise settles first.](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise/race)

`Promise.race()`

If all of the promises given are rejected, a new error class called [ AggregateError](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/AggregateError) is returned. In addition, it indicates the reason for the rejection(s).

```
const promise1 = Promise.reject(0);
const promise2 = new Promise((resolve) => setTimeout(resolve, 100, 'quick'));
const promise3 = new Promise((resolve) => setTimeout(resolve, 500, 'slow'));
const promises = [promise1, promise2, promise3];
Promise.any(promises).then((value) => console.log(value));
// quick wins
```


### Logical assignment operators

JavaScript supports a variety of [assignment operators](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Expressions_and_Operators#Assignment) already. The [Logical Assignment Operator Proposal](https://github.com/tc39/proposal-logical-assignment) specifies three new logical operators that are now enabled by default in Firefox:

`??=`

—[Logical nullish assignment](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Logical_nullish_assignment).`&&=`

—[Logical AND assignment](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Logical_AND_assignment).`||=`

— and,[Logical OR assignment](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Logical_OR_assignment).

These new logical assignment operators have the same short-circuit behavior that the existing [logical operations](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Expressions_and_Operators#Logical_operators) implement already. Assignment only happens if the logical operation would evaluate the right-hand side.

For example, if the “lyrics” element is empty, set the `innerHTML`

to a default value:

`document.getElementById('lyrics').innerHTML ||= '<i>No lyrics.</i>'`


Here the short-circuit is especially beneficial, since the element will not be updated unnecessarily. Moreover, it won’t cause unwanted side-effects such as additional parsing or rendering work, or loss of focus.

### Weakly held references

In JavaScript, references between objects are generally 1-1: if you have a reference to one object so that it cannot be garbage collected, then none of the objects it references can be collected either. This changed with the addition of [ WeakMap](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/WeakMap) and

[in ES2015, where you now need to have a reference to both the](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/WeakSet)

`WeakSet`

`WeakMap`

and a key in order to prevent the corresponding value from being collected.Since that time, JavaScript has not provided a more advanced API for creating weakly held references, until now. The [WeakRef proposal](https://github.com/tc39/proposal-weakrefs) adds this capability. Now Firefox supports the [ WeakRef](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/WeakRef) and

[objects.](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/FinalizationRegistry)

`FinalizationRegistry`

Hop over to the MDN docs for [example usage](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/WeakRef#Examples) of `WeakRef`

. Garbage collectors are complicated, so make sure you also read [this note of caution](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/WeakRef#Avoid_where_possible) before using WeakRefs.

### WebAssembly

Firefox 79 includes new WebAssembly functionality:

- First off, seven new built-in operations are provided for
[bulk memory operations](https://developer.mozilla.org/docs/WebAssembly/Understanding_the_text_format#Bulk_memory_operations). For example, copying and initializing allow WebAssembly to model native functions such as`memcpy`

and`memmove`

in a more efficient, performant way. - The
[reference-types proposal](https://github.com/WebAssembly/reference-types)is now supported. It provides a new type,`externref`

, which can hold any JavaScript value, for example strings, DOM references, or objects. Thedocumentation includes guidance for taking advantage of`wasm-bindgen`

`externref`

from Rust. - With the return of SharedArrayBuffer objects, we’re now also able to support
[WebAssembly threads](https://developer.mozilla.org/docs/WebAssembly/Understanding_the_text_format#WebAssembly_threads). Thus, it is now possible for WebAssembly Memory objects to be shared across multiple WebAssembly instances running in separate Web Workers. The outcome? Very fast communication between Workers, as well as significant performance gains in web applications.

## WebExtensions updates

Starting with Firefox 79, developers of tab management extensions can improve the perceived performance when users switch tabs. The new [ tabs.warmup()](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/warmup) function will prepare the tab to be displayed. Developers can use this function, when they anticipate a tab switch, e.g. when hovering over a button or link.

If you’re an extension developer and your extensions sync items across multiple devices, be aware that we ported [ storage.sync area](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/storage/sync) to a Rust-based implementation. Extension data that had been stored locally in existing profiles will automatically migrate the first time an installed extension tries to access

`storage.sync`

data in Firefox 79. As a quick note, the new implementation enforces client-side quota limits. You should estimate how much data your extension stores locally and test how your extension behaves once the data limit is exceeded. Check out [this post](https://blog.mozilla.org/addons/2020/07/09/changes-to-storage-sync-in-firefox-79/)for testing instructions and more information about this change.

Take a look at the [Add-ons Blog](https://blog.mozilla.org/addons/) for more updates to the WebExtensions API in Firefox 79!

## Summary

As always, feel free to share constructive feedback and ask questions in the comments. And thanks for keeping your [Firefox up to date](https://www.mozilla.org/en-US/firefox/new/)!

## About
[
Florian Scholz ](https://developer.mozilla.org)

Florian is the Content Lead for MDN Web Docs, writes about Web platform technologies and researches browser compatibility data. He lives in Bremen, Germany.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.

## One comment

MATTEO MEDICIAugust 2nd, 2020 at 12:54