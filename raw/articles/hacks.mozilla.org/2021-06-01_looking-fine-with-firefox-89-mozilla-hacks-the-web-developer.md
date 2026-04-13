---
title: Looking fine with Firefox 89 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2021/06/looking-fine-with-firefox-89/
author: Chris Mills
published: '2021-06-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

While we’re sitting here feeling a bit frumpy after a year with reduced activity, Firefox 89 has smartened up and brings with it a slimmed down, slightly more minimalist interface.

Along with this new look, we get some great styling features including a [ force-colors](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors) feature for media queries and better control over how fonts are displayed. The long awaited

[top-level](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await#top-level-await)keyword for JavaScript modules is now enabled, as well as the

`await`

[interface, which is another addition to the performance suite of APIs: 89 really has been working out!](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceEventTiming)

`PerformanceEventTiming`

This blog post provides merely a set of highlights; for all the details, check out the following:

## forced-colors media feature

The `forced-colors`

CSS media feature detects if a user agent restricts the color palette used on a web page. For instance Windows has a *High Contrast* mode. If it’s turned on, using [ forced-colors: active](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors) within a CSS media query would apply the styles nested inside.

In this example we have a `.button`

class that declares a `box-shadow`

property, giving any HTML element using that class a nice drop-shadow.

If `forced-colors`

mode is active, this shadow would not be rendered, so instead we’re declaring a border to make up for the shadow loss:

```
.button {
border: 0;
padding: 10px;
box-shadow: -2px -2px 5px gray, 2px 2px 5px gray;
}
@media (forced-colors: active) {
.button {
/* Use a border instead, since box-shadow is forced to 'none' in forced-colors mode */
border: 2px ButtonText solid;
}
}
```


## Better control for displayed fonts

Firefox 89 brings with it the [ line-gap-override](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/line-gap-override),

[and](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/ascent-override)

`ascent-override`

[CSS properties. These allow developers more control over how fonts are displayed. The following snippet shows just how useful these properties are when using a local fallback font:](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/descent-override)

`descent-override`

```
@font-face {
font-family: web-font;
src: url("<https://example.com/font.woff>");
}
@font-face {
font-family: local-font;
src: local(Local Font);
ascent-override: 90%;
descent-override: 110%;
line-gap-override: 120%;
}
```


These new properties help to reduce layout shift when fonts are loading, as developers can better match the intricacies of a local font with a web font. They work alongside the [ size-adjust](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust) property which is currently behind a

[preference in Firefox 89](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Experimental_features#descriptor_size_adjust).

## Top-level await

If you’ve been writing JavaScript over the past few years you’ve more than likely become familiar with `async`

functions. Now the [ await keyword](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await#top-level-await), usually confined to use within an

`async`

function, has been given independence and allowed to go it alone. As long as it stays within [modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules#top_level_await)that is.

In short, this means JavaScript modules that have child modules using top level await wait for that child to execute before they themselves run. All while not blocking other child modules from loading.

Here is a very small example of a module using the >a href=”https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API”>Fetch API and specifying `await`

within the `export`

statement. Any modules that include this will wait for the fetch to resolve before running any code.

```
// fetch request
const colors = fetch('../data/colors.json')
.then(response => response.json());
export default await colors;
```


## PerformanceEventTiming

A new look can’t go unnoticed without mentioning performance. There’s a plethora of Performance APIs, which give developers granular power over their own bespoke performance tests. The [ PerformanceEventTiming](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceEventTiming) interface is now available in Firefox 89 and provides timing information for a whole array of events. It adds yet another extremely useful feature for developers by cleverly giving information about when a user-triggered event starts and when it ends. A very welcome addition to the new release.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.