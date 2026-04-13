---
title: Firefox 69 — a tale of Resize Observer, microtasks, CSS, and DevTools – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/09/firefox-69-a-tale-of-resize-observer-microtasks-css-and-devtools/
author: Chris Mills
published: '2019-09-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

For our latest excellent adventure, we’ve gone and cooked up a new Firefox release. Version 69 features a number of nice new additions including [JavaScript public instance fields](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Class_fields#Public_fields), the [Resize Observer](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver) and [Microtask APIs](https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/queueMicrotask), CSS logical overflow properties (e.g. [ overflow-block](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-block)), and

[.](https://developer.mozilla.org/en-US/docs/Web/CSS/@supports#Testing_for_the_support_of_a_selector)

`@supports`

for selectorsWe will also look at highlights from the raft of new debugging features in the Firefox 69 DevTools, including console message grouping, event listener breakpoints, and text label checks.

This blog post provides merely a set of highlights; for all the details, check out the following:

## The new CSS

Firefox 69 supports a number of new CSS features; the most interesting are as follows.

### New logical properties for overflow

69 sees support for some new [logical properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Logical_Properties) — [ overflow-block](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-block) and

[— which control the overflow of an element’s content in the block or inline dimension respectively.](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-inline)

`overflow-inline`

These properties map to [ overflow-x](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-x) or

[, depending on the content’s](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-y)

`overflow-y`

[. Using these new logical properties instead of](https://developer.mozilla.org/en-US/docs/Web/CSS/writing-mode)

`writing-mode`

`overflow-x`

and `overflow-y`

makes your content easier to localize, especially when adapting it to languages using a different writing direction. They can also take the same values — `visible`

, `hidden`

, `scroll`

, `auto`

, etc.Note: Look at [Handling different text directions](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Handling_different_text_directions#Logical_properties_and_values) if you want to read up on these concepts.

### @supports for selectors

The [ @supports at-rule](https://developer.mozilla.org/en-US/docs/Web/CSS/@supports) has long been very useful for selectively applying CSS only when a browser supports a particular property, or doesn’t support it.

Recently this functionality has been extended so that you can apply CSS only if a particular selector is or isn’t supported. The syntax looks like this:

```
@supports selector(selector-to-test) {
/* insert rules here */
}
```


We are supporting this functionality by default in Firefox 69 onwards. Find some [usage examples here](https://developer.mozilla.org/en-US/docs/Web/CSS/@supports#Testing_for_the_support_of_a_selector).

## JavaScript gets public instance fields

The most interesting addition we’ve had to the JavaScript language in Firefox 69 is support for [public instance fields](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Class_fields#Public_fields) in JavaScript classes. This allows you to specify properties you want the class to have up front, making the code more logical and self-documenting, and the constructor cleaner. For example:

```
class Product {
name;
tax = 0.2;
basePrice = 0;
price;
constructor(name, basePrice) {
this.name = name;
this.basePrice = basePrice;
this.price = (basePrice * (1 + this.tax)).toFixed(2);
}
}
```


Notice that you can include default values if wished. The class can then be used as you’d expect:

```
let bakedBeans = new Product('Baked Beans', 0.59);
console.log(`${bakedBeans.name} cost $${bakedBeans.price}.`);
```


Private instance fields (which can’t be set or referenced outside the class definition) are very close to being supported in Firefox, and also look to be very useful. For example, we might want to hide the details of the tax and base price. Private fields are indicated by a hash symbol in front of the name:

```
#tax = 0.2;
#basePrice = 0;
```


## The wonder of WebAPIs

There are a couple of new WebAPIs enabled by default in Firefox 69. Let’s take a look.

### Resize Observer

Put simply, the [Resize Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Resize_Observer_API) allows you to easily observe and respond to changes in the size of an element’s content or border box. It provides a JavaScript solution to the often-discussed lack of [“element queries”](https://www.xanthir.com/b4PR0) in the web platform.

A simple trivial example might be something like the following ([resize-observer-border-radius.html](https://mdn.github.io/dom-examples/resize-observer/resize-observer-border-radius.html), [see the source also](https://github.com/mdn/dom-examples/blob/master/resize-observer/resize-observer-border-radius.html)), which adjusts the `border-radius`

of a `<div>`

as it gets smaller or bigger:

```
const resizeObserver = new ResizeObserver(entries => {
for (let entry of entries) {
if(entry.contentBoxSize) {
entry.target.style.borderRadius = Math.min(100, (entry.contentBoxSize.inlineSize/10) +
(entry.contentBoxSize.blockSize/10)) + 'px';
} else {
entry.target.style.borderRadius = Math.min(100, (entry.contentRect.width/10) +
(entry.contentRect.height/10)) + 'px';
}
}
});
resizeObserver.observe(document.querySelector('div'));
```


*“But you can just use border-radius with a percentage”*, I hear you cry. Well, sort of. But that quickly leads to ugly-looking elliptical corners, whereas the above solution gives you nice square corners that scale with the box size.

Another, slightly less trivial example is the following ([resize-observer-text.html](https://mdn.github.io/dom-examples/resize-observer/resize-observer-text.html) , [see the source also](https://github.com/mdn/dom-examples/blob/master/resize-observer/resize-observer-text.html)):

```
if(window.ResizeObserver) {
const h1Elem = document.querySelector('h1');
const pElem = document.querySelector('p');
const divElem = document.querySelector('body > div');
const slider = document.querySelector('input');
divElem.style.width = '600px';
slider.addEventListener('input', () => {
divElem.style.width = slider.value + 'px';
})
const resizeObserver = new ResizeObserver(entries => {
for (let entry of entries) {
if(entry.contentBoxSize) {
h1Elem.style.fontSize = Math.max(1.5, entry.contentBoxSize.inlineSize/200) + 'rem';
pElem.style.fontSize = Math.max(1, entry.contentBoxSize.inlineSize/600) + 'rem';
} else {
h1Elem.style.fontSize = Math.max(1.5, entry.contentRect.width/200) + 'rem';
pElem.style.fontSize = Math.max(1, entry.contentRect.width/600) + 'rem';
}
}
});
resizeObserver.observe(divElem);
}
```


Here we use the resize observer to change the `font-size`

of a header and paragraph as a slider’s value is changed, causing the containing `<div>`

to change its width. This shows that you can respond to changes in an element’s size, even if they have nothing to do with the viewport size changing.

So to summarise, Resize Observer opens up a wealth of new responsive design work that was difficult with CSS features alone. We’re even using it to implement a new [responsive version of our new DevTools JavaScript console](https://bugzilla.mozilla.org/show_bug.cgi?id=1523864)!.

### Microtasks

The Microtasks API provides a single method — `<a href="https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/queueMicrotask">queueMicrotask()</a>`

. This is a low-level method that enables us to directly schedule a callback on the microtask queue. This schedules code to be run immediately before control returns to the event loop so you are assured a reliable running order (using `setTimeout(() => {}, 0))`

for example can give unreliable results).

The syntax is as simple to use as other timing functions:

```
self.queueMicrotask(() => {
// function contents here
})
```


The use cases are subtle, but make sense when you read the [explainer section in the spec](https://html.spec.whatwg.org/multipage/timers-and-user-prompts.html#microtask-queuing). The biggest benefactors here are framework vendors, who like lower-level access to scheduling. Using this will reduce hacks and make frameworks more predictable cross-browser.

## Developer tools updates in 69

There are various interesting additions to the DevTools in 69, so be sure to go and check them out!

### Event breakpoints and async functions in the JS debugger

The [JavaScript debugger](https://developer.mozilla.org/en-US/docs/Tools/Debugger) has some cool new features for stepping through and examining code:

[Event listener breakpoints](https://developer.mozilla.org/en-US/docs/Tools/Debugger/Set_event_listener_breakpoints)- Stepping through of Async functions

### New remote debugging

In the new shiny `about:debugging`

page, you’ll find a grouping of options for remotely debugging devices, with more to follow in the future. In 69, we’ve enabled a new mechanism for allowing you to remotely debug other versions of Firefox, on the same machine or other machines on the same network (see *Network Location*).

### Console message grouping

In the console, we now group together similar error messages, with the aim of making the console tidier, spamming developers less, and making them more likely to pay attention to the messages. In turn, this can have a positive effect on security/privacy.

The new console message grouping looks like this, when in its initial closed state:

![](../../assets/95a14d02c0ed7dfb.png)


When you click the arrow to open the message list, it shows you all the individual messages that are grouped:

![](../../assets/655b28f52ff66c8e.png)


Initially the grouping occurs on CSP, CORS, and tracking protection errors, with more categories to follow in the future.

### Flex information in the picker infobar

Next up, we’ll have a look at the [Page inspector](https://wiki.developer.mozilla.org/en-US/docs/Tools/Page_Inspector). When using the picker, or hovering over an element in the HTML pane, the infobar for the element now shows when it is a flex container, item, or both.

![website nav menu with infobar pointing out that it is a flex item](../../assets/c799a0ac8e5d6b2e.png)


[See this page](https://wiki.developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_Flexbox_layouts#In_the_infobar) for more details.

### Text Label Checks in the Accessibility Inspector

A final great feature to mention is the new text label checks feature of the [Accessibility Inspector](https://developer.mozilla.org/en-US/docs/Tools/Accessibility_inspector).

![](../../assets/5239ff40e1ebe8ab.png)


When you choose *Check for issues > Text Labels* from the dropdown box at the top of the accessibility inspector, it marks all the nodes in the accessibility tree with a warning sign if it is missing a descriptive text label. The *Checks* pane on the right hand side then gives a description of the problem, along with a *Learn more* link that takes you to more detailed information available on MDN.

## WebExtensions updates

Last but not least, Let’s give a mention to WebExtensions! The main feature to make it into Firefox 69 is [User Scripts](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/userScripts) — these are a special kind of extension content script that, when registered, instruct the browser to insert the given scripts into pages that match the given URL patterns.

## See also

In this post we’ve reviewed the main web platform features added in Firefox 69. You can also read up on the main new features of the Firefox browser — see the [Firefox 69 Release Notes](https://www.mozilla.org/en-US/firefox/69.0/releasenotes/).

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 6 comments

tophfSeptember 3rd, 2019 at 09:03Chris MillsSeptember 3rd, 2019 at 09:21Tomas DaySeptember 5th, 2019 at 09:10intr0September 5th, 2019 at 09:48RayLokeSanSeptember 5th, 2019 at 13:10LukeSeptember 8th, 2019 at 20:55