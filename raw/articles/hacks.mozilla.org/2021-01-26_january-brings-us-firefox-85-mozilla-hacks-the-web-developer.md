---
title: January brings us Firefox 85 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2021/01/january-brings-us-firefox-85/
author: Chris Mills
published: '2021-01-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

To wrap up January, we are proud to bring you the release of Firefox 85. In this version we are bringing you support for the `:focus-visible`

pseudo-class in CSS and associated devtools, `<link rel="preload">`

, and the complete removal of Flash support from Firefox. We’d also like to invite you to preview two exciting new JavaScript features in the current Firefox Nightly — top-level `await`

and relative indexing via the `.at()`

method. Have fun!

This blog post provides merely a set of highlights; for all the details, check out the following:

## :focus-visible

The [ :focus-visible](https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible) pseudo-class, previously supported in Firefox via the proprietary

`:-moz-focusring`

pseudo-class, allows the developer to apply styling to elements in cases where browsers use heuristics to determine that focus should be made evident on the element.The most obvious case is when you use the keyboard to focus an element such as a button or link. There are often cases where designers will want to get rid of the ugly focus-ring, commonly achieved using something like `:focus { outline: none }`

, but this causes problems for keyboard users, for whom the focus-ring is an essential accessibility aid.

`:focus-visible`

allows you to apply a focus-ring alternative style only when the element is focused using the keyboard, and not when it is clicked.

For example, this HTML:

```
<p><button>Test button</button></p>
<p><input type="text" value="Test input"></p>
<p><a href="#">Test link</a></p>
```


Could be styled like this:

```
/* remove the default focus outline only on browsers that support :focus-visible */
a:not(:focus-visible), button:not(:focus-visible), button:not(:focus-visible) {
outline: none;
}
/* Add a strong indication on browsers that support :focus-visible */
a:focus-visible, button:focus-visible, input:focus-visible {
outline: 4px dashed orange;
}
```


And as another nice addition, the Firefox DevTools’ Page Inspector now allows you to toggle `:focus-visible`

styles in its Rules View. See [Viewing common pseudo-classes](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_and_edit_CSS#viewing_common_pseudo-classes) for more details.

## Preload

After a couple of false starts in previous versions, we are now proud to announce support for [ <link rel="preload">](https://developer.mozilla.org/en-US/docs/Web/HTML/Link_types/preload), which allows developers to instruct the browser to preemptively fetch and cache high-importance resources ahead of time. This ensures they are available earlier and are less likely to block page rendering, improving performance.

This done by including `rel="preload"`

on your link element, and an as attribute containing the type of resource that is being preloaded, for example:

```
<link rel="preload" href="style.css" as="style">
<link rel="preload" href="main.js" as="script">
```


You can also include a type attribute containing the MIME type of the resource, so a browser can quickly see what resources are on offer, and ignore ones that it doesn’t support:

```
<link rel="preload" href="video.mp4" as="video" type="video/mp4">
<link rel="preload" href="image.webp" as="image" type="image/webp">
```


See [Preloading content with rel=”preload”](https://developer.mozilla.org/en-US/docs/Web/HTML/Preloading_content) for more information.

## The Flash is dead, long live the Flash

Firefox 85 sees the complete removal of Flash support from the browser, with no means to turn it back on. This is a coordinated effort across browsers, and as our [plugin roadmap](https://developer.mozilla.org/en-US/docs/Plugins/Roadmap) shows, it has been on the cards for a long time.

For some like myself — who have many nostalgic memories of the early days of the web, and all the creativity, innovation, and just plain fun that Flash brought us — this is a bittersweet day. It is sad to say goodbye to it, but at the same time the advantages of doing so are clear. Rest well, dear Flash.

## Nightly previews

There are a couple of upcoming additions to Gecko that are currently available only in our [Nightly Preview](https://www.mozilla.org/en-US/firefox/channel/desktop/#nightly). We thought you’d like to get a chance to test them early and give us feedback, so please let us know what you think in the comments below!

### Top-level await

[ async/await](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Async_await) has been around for a while now, and is proving popular with JavaScript developers because it allows us to write promise-based async code more cleanly and logically. This following trivial example illustrates the idea of using the


[inside an](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await)

`await`

keyword[async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)to turn a returned value into a resolved promise.

```
async function hello() {
return greeting = await Promise.resolve("Hello");
};
hello().then(alert);
```


The trouble here is that await was originally only allowed inside async functions, and not in the global scope. The experimental [top-level await proposal](https://github.com/tc39/proposal-top-level-await) addresses this, by allowing global awaits. This has many advantages in situations like wanting to await the loading of modules in your JS application. Check out the proposal for some useful examples.

### What’re you pointing at() ?

Currently an ECMAScript stage 3 draft proposal, the relative indexing method `.at()`

has been added to [ Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/at),

[, and](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/at)

`String`

[instances to provide an easy way of returning specific index values in a relative manner. You can use a positive index to count forwards from position 0, or a negative value to count backwards from the highest index position.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/at)

`TypedArray`

Try these, for example:

```
let myString = 'Hello, how are you?';
myString.at(4);
myString.at(-3);
let myArray = [0, 10, 35, 70, 100, 300];
myArray.at(1);
myArray.at(-2);
```


## WebExtensions

Last but not least, let’s look at what has changed in our WebExtensions implementation in Fx 85.

- It is now possible to
[disable a homepage and new tab override](https://bugzilla.mozilla.org/show_bug.cgi?id=1595858)for an extension without disabling the extension. Special thanks to Erica Wright for getting this done. - The “Undo Close Tabs” feature now does the right thing if an extension
[just closed multiple tabs](https://bugzilla.mozilla.org/show_bug.cgi?id=1650956). - The
is now available on Firefox for Android.`browsingData`

API - Certain errors triggered when an extension
[changes a permission to optional](https://bugzilla.mozilla.org/show_bug.cgi?id=1637059)during an update have been fixed. - When the devtools permission is revoked and then granted, extension pages are now
[automatically enabled in the toolbox](https://bugzilla.mozilla.org/show_bug.cgi?id=1671579).

And finally, we want to remind you about upcoming site isolation changes with [Project Fission](https://wiki.mozilla.org/Project_Fission). As we [previously mentioned](https://blog.mozilla.org/addons/2020/10/07/extensions-in-firefox-82/#fission), the `drawWindow()`

method is being deprecated as part of this work. If you use this API, we recommend that you switch to using the [ captureTab()](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/captureTab) method instead.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 3 comments

StigJanuary 26th, 2021 at 10:35ItielFebruary 1st, 2021 at 05:34Chris MillsFebruary 1st, 2021 at 06:33