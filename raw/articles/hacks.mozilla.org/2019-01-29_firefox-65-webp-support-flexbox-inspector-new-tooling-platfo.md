---
title: 'Firefox 65: WebP support, Flexbox Inspector, new tooling & platform updates
  – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2019/01/firefox-65-webp-flexbox-inspector-new-tooling/
author: Chris Mills
published: '2019-01-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Well now, there’s no better way to usher out the first month of the year than with a great new Firefox release. It’s winter for many of us, but that means more at-home time to install Firefox version 65, and check out some of the great new browser and web platform features we’ve included within. Unless you’d rather be donning your heavy coat and heading outside to grit the driveway, that is (or going to the beach, in the case of some of our Australian chums).

## A good day for DevTools

Firefox 65 features several notable DevTools improvements. The highlights are as follows:

### CSS Flexbox Inspector

At Mozilla, we believe that new features of the web platform are often [best understood](https://www.chenhuijing.com/blog/devtools-for-understanding-modern-layout-techniques/) with the help of intuitive, visual tools. That’s why our DevTools team has spent the last few years getting feedback from the field, and prioritizing innovative new tooling to allow web devs and designers to inspect, edit, understand, and tinker with UI features. This drive led to the release of the [CSS Grid Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_grid_layouts), [Font Editor](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Edit_fonts), and [Shape Path Editor](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Edit_CSS_shapes).

Firefox 65 sees these features joined by a new friend — the [CSS Flexbox Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_Flexbox_layouts) — which allows you to easily visualize where your flex containers and items are sitting on the page and how much free space is available between them, what each flex item’s default and final size is, how much they are being shrunk or grown, and more.

### Changes panel

When you’re done tweaking your site’s interface using these tools, our new Changes panel tracks and summarizes all of the CSS modifications you’ve made during the current session, so you can work out what you did to fix a particular issue, and can copy and paste your fixes back out to your code editor.

### Advanced color contrast ratio

We have also added an advanced color contrast ratio display. When using the [Accessibility Inspector’s](https://developer.mozilla.org/en-US/docs/Tools/Accessibility_inspector) accessibility picker, hovering over the text content of an element displays its color contrast ratio, even if its background is complex (for example a gradient or detailed image), in which case it shows a range of color contrast values, along with a [WCAG rating](https://www.w3.org/WAI/standards-guidelines/wcag/).

### JavaScript debugging improvements

Firefox 65 also features some nifty JavaScript debugging improvements:

- When displaying stack traces (e.g. in console logs or with the
[JavaScript debugger](https://developer.mozilla.org/en-US/docs/Tools/Debugger)), calls to framework methods are identified and collapsed by default, making it easier to home in on your code. - In the same fashion as native terminals, you can now use reverse search to find entries in your JavaScript console history (F9 (Windows/Linux) or Ctrl + R (macOS) and type a search term, followed by Ctrl + R/Ctrl + S to toggle through results).
- The JavaScript console’s
`$0`

shortcut (references the currently inspected element on the page) now has autocomplete available, so for example you could type`$0.te`

to get a suggestion of`$0.textContent`

to reference text content.

### Find out more

- You can find about these features in more detail and read about other incremental improvements in the
[DevTools section of Firefox 65 for developers](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/65#Developer_tools). - If you’d like to know more about how the Firefox DevTools are created, check out Victoria Wang’s
[Designing the Flexbox Inspector](https://hacks.mozilla.org/2019/01/designing-the-flexbox-inspector/)post.

## CSS platform improvements

A number of CSS features have been added to Gecko in 65. The highlights are described below.

### CSS environment variables

[CSS environment variables](https://developer.mozilla.org/en-US/docs/Web/CSS/env) are now supported, accessed via `env()`

in stylesheets. These variables are usable in any part of a property value or descriptor, and are scoped globally to a particular document, whereas custom properties are scoped to the element(s) they are declared on. These were initially provided by the iOS browser to allow developers to place their content in a safe area of the viewport, i.e., away from the area covered by the notch.

```
body {
padding:
env(safe-area-inset-top, 20px)
env(safe-area-inset-right, 20px)
env(safe-area-inset-bottom, 20px)
env(safe-area-inset-left, 20px);
}
```


### steps() animation timing function

We’ve added the [ steps() CSS animation timing function](https://developer.mozilla.org/en-US/docs/Web/CSS/timing-function#The_steps()_class_of_timing_functions), along with the related

`jump-*`

keywords. This allows you to easily create animations that jump in a series of equidistant steps, rather than a smooth animation.As an example, we might previously have added a smooth animation to a DOM node like this:

```
.smooth {
animation: move-across 2s infinite alternate linear;
}
```


Now we can make the animation jump in 5 equal steps, like this:

```
.stepped {
animation: move-across 2s infinite alternate steps(5, jump-end);
}
```


**Note**: The `steps()`

function was previously called `frames()`

, but some details changed, and the [CSS Working Group](https://www.w3.org/Style/CSS/members) decided to rename it to something less confusing.

### break-* properties

New [ break-before](https://developer.mozilla.org/en-US/docs/Web/CSS/break-before),

[, and](https://developer.mozilla.org/en-US/docs/Web/CSS/break-after)

`break-after`

[CSS properties have been added, and the now-legacy](https://developer.mozilla.org/en-US/docs/Web/CSS/break-inside)

`break-inside`

`page-break-*`

properties have been aliased to them. These properties are part of the [CSS Fragmentation](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Fragmentation)spec, and set how page, column, or region breaks should behave before, after, or inside a generated box.

For example, to stop a page break occurring inside a list or paragraph:

```
ol, ul, p {
break-inside: avoid;
}
```


## JavaScript/APIs

Firefox 65 brings many updates to JavaScript/APIs.

### Readable streams

[Readable streams](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Using_readable_streams) are now enabled by default, allowing developers to process data chunk by chunk as it arrives over the network, e.g. from a [ fetch() request](https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/fetch).

You can find a number of [ ReadableStream demos on GitHub](https://github.com/mdn/dom-examples/tree/master/streams).

### Relative time formats

The [ Intl.RelativeTimeFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RelativeTimeFormat) constructor allows you to output strings describing localized relative times, for easier human-readable time references in web apps.

A couple of examples, to sate your appetite:

```
let rtf1 = new Intl.RelativeTimeFormat('en', { style: 'narrow' });
console.log(rtf1.format(2, 'day')); // expected output: "in 2 days"
let rtf2 = new Intl.RelativeTimeFormat('es', { style: 'narrow' });
console.log(rtf2.format(2, 'day')); // expected output: "dentro de 2 días"
```


### Storage Access API

The [Storage Access API](https://developer.mozilla.org/en-US/docs/Web/API/Storage_Access_API) has been enabled by default, providing a mechanism for embedded, cross-origin content to request access to client-side storage mechanisms it would normally only have access to in a first-party context. This API features a couple of simple methods, [ hasStorageAccess()](https://developer.mozilla.org/en-US/docs/Web/API/Document/hasStorageAccess) and

[, which respectively check and request storage access. For example:](https://developer.mozilla.org/en-US/docs/Web/API/Document/requestStorageAccess)

`requestStorageAccess()`

```
document.requestStorageAccess().then(
() => { console.log('access granted') },
() => { console.log('access denied') }
);
```


### Other honorable mentions

- The
`globalThis`

keyword has been added, for[accessing the global object](https://github.com/tc39/proposal-global)in whatever context you are in. This avoids needing to use a mix of`window`

,`self`

,`global`

, or`this`

, depending on where a script is executing (e.g. a webpage, a worker, or Node.js). - The
object’s`FetchEvent`

`replacesClientId`

and`resultingClientId`

properties are now implemented — allowing you to monitor the origin and destination of a navigation. - You can now set a referrer policy on scripts applied to your documents (e.g. via a
)`referrerpolicy`

attribute on`<script>`

elements - Lastly, to avoid popup spam,
may now only be called once per user interaction event.`Window.open()`


## Media: Support for WebP and AV1, and other improvements

At long last, Firefox 65 now supports the [WebP image format](https://developers.google.com/speed/webp/). WebP offers both lossless and lossy compression modes, and typically produces files that are 25-34% smaller than equivalent JPEGs or PNGs with the same image quality. Smaller files mean faster page loads and better performance, so this is obviously a good thing.

Not all browsers support WebP. You can use the [ <picture> element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture) in your HTML to offer both WebP and traditional image formats, leaving the final choice to the user’s browser. You can also detect WebP support on the server-side and serve images as appropriate, as supported browsers send an Accept: image/webp header when requesting images.

Images are great, but what about video? Mozilla, along with industry partners, has been developing the next-generation [AV1 video codec](https://research.mozilla.org/av1-media-codecs/), which is now supported in Firefox 65 for Windows. AV1 is nearly twice as efficient as H.264 in terms of compression, and, unlike H.264, it’s completely open and royalty-free. Support for other operating systems will be enabled in future releases.

### Other additions

- The
[MediaRecorder](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder)`pause`

and`resume`

events are finally supported in Firefox, as of version 65. - For developers creating WebGL content, Firefox 65 supports the
[BPTC](https://www.khronos.org/registry/webgl/extensions/EXT_texture_compression_bptc/)and[RGTC](https://www.khronos.org/registry/webgl/extensions/EXT_texture_compression_rgtc/)texture compression extensions.

## Firefox Internals

We’ve also updated several aspects of Firefox itself:

- Support for
[Handoff](https://support.apple.com/en-us/HT204681#handoff)between iOS and macOS devices is now available. - Preferences for content blocking have been completely redesigned to give people greater and more obvious control over how Firefox protects them from third-party tracking.
- The
`about:performance`

dashboard now reports the memory used by tabs and extensions. [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)have been implemented over HTTP/2.- Lastly, for Windows administrators, Firefox is now available as an MSI package in addition to a traditional self-extracting EXE.

## WebExtensions improvements

We’ve added some useful WebExtensions API features too!

- The
[Tabs API](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs)now allows extensions to control which tab gets focused when the current tab is closed. You can read more about the motivation for this feature on[Piro’s blog](https://piro.sakura.ne.jp/latest/blosxom/mozilla/xul/2018-12-03_successor-tabs-api-en.htm), where he discusses it in the context of his[Tree Style Tab](https://addons.mozilla.org/en-US/firefox/addon/tree-style-tab/)extension.

## Interoperability

The web often contains conflicting, non-standard, or under-specified markup, and it’s up to us to ensure that pages which work in other browsers also work in Firefox.

To that end, Firefox 65:

- supports even more values of the non-standard
CSS property.`-webkit-appearance`

- behaves the same as other browsers when encountering the
CSS property in nested, shadow, or content editable contexts.`user-select`

- clears the content of
s when the`<iframe>`

`src`

attribute is removed, matching the behavior of Safari and Chrome.

## Further Reading

- For more details on the added features mentioned above, plus other minor additions, see
[Firefox 65 for Developers](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/65)on MDN, and the official[Firefox 65 Release Notes](https://www.mozilla.org/en-US/firefox/65.0/releasenotes/). - You may also be interested in the
[Firefox 65 Site Compatibility](https://www.fxsitecompat.com/en-CA/versions/65/)notes.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 7 comments

ChristophJanuary 30th, 2019 at 00:07PAUL MILESJanuary 31st, 2019 at 07:45DenialJanuary 31st, 2019 at 08:11ClémentJanuary 31st, 2019 at 08:48lyn adkinsFebruary 1st, 2019 at 01:17Josef RennerFebruary 1st, 2019 at 08:46Chris MillsFebruary 1st, 2019 at 12:49