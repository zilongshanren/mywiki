---
title: A Fabulous February Firefox — 86! – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2021/02/a-fabulous-february-firefox-86/
author: Chris Mills
published: '2021-02-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Looking into the near distance, we can see the end of February loitering on the horizon, threatening to give way to March at any moment. To keep you engaged until then, we’d like to introduce you to Firefox 86. The new version features some interesting and fun new goodies including support for the `Intl.DisplayNames`

object, the `:autofill`

pseudo-class, and a much better `<iframe>`

inspection feature in DevTools.

This blog post provides merely a set of highlights; for all the details, check out the following:

## Better <iframe> inspection

The Firefox [web console](https://developer.mozilla.org/en-US/docs/Tools/Web_Console) used to include a `cd()`

helper command that enabled developers to change the DevTools’ context to inspect a specific `<iframe>`

present on the page. This helper has been removed in favor of the iframe context picker, which is much easier to use.

When inspecting a page with `<iframe>`

s present, the DevTools will show the iframe context picker button.

![Firefox devtools, showing the select iframe dropdown menu, a list of the iframes on the page that can be selected from](../../assets/47684dfa63107e62.png)


When pressed, it will display a drop-down menu listing all the URLs of content embedded in the page inside `<iframe>`

s. Choose one of these, and the inspector, console, debugger, and all other developer tools will then target that `<iframe>`

, essentially behaving as if the rest of the page does not exist.

## :autofill

The [ :autofill](https://developer.mozilla.org/en-US/docs/Web/CSS/:autofill) CSS pseudo-class matches when an

`<input>`

element has had its value auto-filled by the browser. The class stops matching as soon as the user edits the field.For example:

```
input:-webkit-autofill {
border: 3px solid blue;
}
input:autofill {
border: 3px solid blue;
}
```


Firefox 86 supports the unprefixed version with the -webkit-prefixed version also supported as an alias. Most other browsers just support the prefixed version, so you should provide both for maximum browser support.

## Intl.DisplayNames

The [ Intl.DisplayNames](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DisplayNames) built-in object has been enabled by default in Firefox 86. This enables the consistent translation of language, region, and script display names. A simple example looks like so:

```
// Get English currency code display names
let currencyNames = new Intl.DisplayNames(['en'], {type: 'currency'});
// Get currency names
currencyNames.of('USD'); // "US Dollar"
currencyNames.of('EUR'); // "Euro"
```


## Nightly preview — image-set()

The [ image-set()](https://developer.mozilla.org/en-US/docs/Web/CSS/image-set()) CSS function lets the browser pick the most appropriate CSS image from a provided set. This is useful for implementing responsive images in CSS, respecting the fact that resolution and bandwidth differ by device and network access.

The syntax looks like so:

```
background-image: image-set("cat.png" 1x,
"cat-2x.png" 2x,
"cat-print.png" 600dpi);
```


Given the set of options, the browser will choose the most appropriate one for the current device’s resolution — users of lower-resolution devices will appreciate not having to download a large hi-res image that they don’t need, which users of more modern devices will be happy to receive a sharper, crisper image that looks better on their device.

## WebExtensions

As part of our work on Manifest V3, we have landed an experimental base content security policy (CSP) behind a preference in Firefox 86. The new CSP disallows remote code execution. This restriction only applies to extensions using [ manifest_version 3](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/manifest_version), which is not currently supported in Firefox (currently, only

`manifest_version`

2 is supported).If you would like to test the new CSP for extension pages and content scripts, you must change your extension’s `manifest_version`

to 3 and set `extensions.manifestv3.enabled`

to `true`

in `about:config`

. Because this is a highly experimental and evolving feature, we want developers to be aware that extensions that work with the new CSP may break as more changes are implemented.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 3 comments

DennisFebruary 23rd, 2021 at 18:32Chris MillsFebruary 23rd, 2021 at 23:46stefan brownMarch 6th, 2021 at 01:14