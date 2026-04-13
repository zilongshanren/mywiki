---
title: The state of Web Components – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/06/the-state-of-web-components/
author: Wilson Page
published: '2015-06-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Web Components have been on developers’ radars for quite some time now. They were first introduced by [Alex Russell](http://twitter.com/slightlylate) at[ Fronteers Conference 2011](https://fronteers.nl/congres/2011/sessions/web-components-and-model-driven-views-alex-russell). The concept shook the community up and became the topic of many future talks and discussions.

In 2013 a Web Components-based framework called *Polymer* was released by *Google* to kick the tires of these new APIs, get community feedback and add some sugar and opinion.

By now, 4 years on, Web Components *should* be everywhere, but in reality *Chrome* is the only browser with ‘some version’ of Web Components. Even with polyfills it’s clear Web Components won’t be fully embraced by the community until the majority of browsers are on-board.

## Why has this taken so long?

To cut a long story short, vendors couldn’t agree.

Web Components were a *Google* effort and little negotiation was made with other browsers before shipping. Like most negotiations in life, parties that don’t feel involved lack enthusiasm and tend not to agree.

Web Components were an ambitious proposal. Initial APIs were high-level and complex to implement (albeit for good reasons), which only added to contention and disagreement between vendors.

*Google* pushed forward, they sought feedback, gained community buy-in; but in hindsight, before other vendors shipped, usability was blocked.

Polyfills meant theoretically Web Components could work on browsers that hadn’t yet implemented, but these have never been accepted as ‘suitable for production’.

Aside from all this, *Microsoft* haven’t been in a position to add many new DOM APIs due to the [ Edge](http://www.microsoft.com/en-us/windows/browser-for-doing) work (nearing completion). And

*Apple*, have been focusing on alternative features for

*Safari*.

## Custom Elements

Of all the Web Components technologies, Custom Elements have been the least contentious. There is general agreement on the value of being able to define how a piece of UI looks and behaves and being able to distribute that piece cross-browser and cross-framework.

### ‘Upgrade’

The term ‘upgrade’ refers to when an element transforms from a plain old `HTMLElement`

into a shiny custom element with its defined life-cycle and `prototype`

. Today, when elements are upgraded, their `createdCallback`

is called.

```
var proto = Object.create(HTMLElement.prototype);
proto.createdCallback = function() { ... };
document.registerElement('x-foo', { prototype: proto });
```


There are [five proposals](https://wiki.whatwg.org/wiki/Custom_Elements#Upgrading) so far from multiple vendors; two stand out as holding the most promise.

#### ‘Dmitry’

An evolved version of the `createdCallback`

pattern that works well with ES6 classes. The `createdCallback`

concept lives on, but sub-classing is more conventional.

```
class MyEl extends HTMLElement {
createdCallback() { ... }
}
document.registerElement("my-el", MyEl);
```


Like in today’s implementation, the custom element begins life as `HTMLUnknownElement`

then some time later the prototype is swapped (or ‘swizzled’) with the registered prototype and the `createdCallback`

is called.

The downside of this approach is that it’s different from how the platform itself behaves. Elements are ‘unknown’ at first, then transform into their final form at some point in the future, which can lead to developer confusion.

#### Synchronous constructor

The constructor registered by the developer is invoked by the parser at the point the custom element is created and inserted into the tree.

```
class MyEl extends HTMLElement {
constructor() { ... }
}
document.registerElement("my-el", MyEl);
```


Although this seems sensible, it means that any custom elements in the initial downloaded document will fail to upgrade if the scripts that contain their `registerElement`

definition are loaded asynchronously. This is not helpful heading into a world of asynchronous ES6 modules.

Additionally synchronous constructors come with [platform issues](https://lists.w3.org/Archives/Public/public-webapps/2015JanMar/0731.html) related to `.cloneNode()`

.

A direction is expected to be decided by vendors at a face-to-face meeting in July 2015.

### is=””

The `is`

attribute gives developers the ability to layer the behaviour of a custom element on top of a standard built-in element.

`<input type="text" is="my-text-input">`


#### Arguments for

- Allows extending the built-in features of a element that aren’t exposed as primitives (eg. accessibility characteristics,
`<form>`

controls,`<template>`

). - They give means to ‘progressively enhance’ an element, so that it remains functional without JavaScript.

#### Arguments against

- Syntax is confusing.
- It side-steps the underlying problem that we’re
[missing many key accessibility primitives](https://github.com/domenic/html-as-custom-elements/blob/master/docs/accessibility.md)in the platform. - It side-steps the underlying problem that we don’t have a way to properly extend built-in elements.
- Use-cases are limited; as soon as developers introduce Shadow DOM, they lose all built-in accessibility features.

#### Consensus

It is generally agreed that `is`

is a ‘wart’ on the Custom Elements spec. *Google has* already implemented `is`

and sees it as a stop-gap until lower-level primitives are exposed. Right now *Mozilla* and *Apple* would rather ship a Custom Elements V1 sooner and address this problem properly in a V2 without polluting the platform with ‘warts’.

[ HTML as Custom Elements](https://github.com/domenic/html-as-custom-elements) is a project by Domenic Denicola that attempts to rebuild built-in HTML elements with custom elements in an attempt to uncover DOM primitives the platform is missing.

## Shadow DOM

Shadow DOM yielded the most contention by far between vendors. So much so that features had to be split into a ‘V1’ and ‘V2’ agenda to help reach agreement quicker.

### Distribution

Distribution is the phase whereby children of a shadow host get visually ‘projected’ into slots inside the host’s Shadow DOM. This is the feature that enables your component to make use of content the user nests inside it.

#### Current API

The current API is fully declarative. Within the Shadow DOM you can use special `<content>`

elements to define where you want the host’s children to be visually inserted.

`<content select="header"></content>`


Both *Apple* and *Microsoft* pushed back on this approach due to concerns around complexity and performance.

#### A new Imperative API

Even at the [face-to-face meeting](https://www.w3.org/wiki/Webapps/WebComponentsApril2015Meeting), agreement couldn’t be made on a declarative API, so all vendors agreed to pursue an imperative solution.

All four vendors (*Microsoft*, *Google*, *Apple* and *Mozilla*) were tasked with specifying this new API before a July 2015 deadline. So far there have been [three suggestions](https://github.com/w3c/webcomponents/blob/gh-pages/proposals/Imperative-API-for-Node-Distribution-in-Shadow-DOM.md). The simplest of the three looks something like:

```
var shadow = host.createShadowRoot({
distribute: function(nodes) {
var slot = shadow.querySelector('content');
for (var i = 0; i < nodes.length; i++) {
slot.add(nodes[i]);
}
}
});
shadow.innerHTML = '<content></content>';
// Call initially ...
shadow.distribute();
// then hook up to MutationObserver
```


The main obstacle is:** timing**. If the children of the host node change and we redistribute when the `MutationObserver`

callback fires, asking for a layout property will return an incorrect result.

```
myHost.appendChild(someElement);
someElement.offsetTop; //=> old value
// distribute on mutation observer callback (async)
someElement.offsetTop; //=> new value
```


Calling offsetTop will perform a synchronous layout *before* distribution!

This might not seems like the end of the world, but scripts and browser internals often depend on the value of `offsetTop`

being correct to perform many different operations, such as: scrolling elements into view.

If these problems can’t be solved we may see a retreat back to discussions over a declarative API. This will either be in the form of the current `<content select>`

style, or the newly proposed [‘named slots’](https://github.com/w3c/webcomponents/blob/gh-pages/proposals/Slots-Proposal.md) API (from *Apple*).

#### A new Declarative API – ‘Named Slots’

The ‘named slots’ proposal is a simpler variation of the current ‘content select’ API, whereby the component user must explicitly label their content with the slot they wish it to be distributed to.

Shadow Root of <x-page>:

```
<slot name="header"></slot>
<slot></slot>
<slot name="footer"></slot>
<div>some shadow content</div>
```


Usage of <x-page>:

```
<x-page>
<header slot="header">header</header>
<footer slot="footer">footer</footer>
<h1>my page title</h1>
<p>my page content<p>
</x-page>
```


Composed/rendered tree (what the user sees):

```
<x-page>
<header slot="header">header</header>
<h1>my page title</h1>
<p>my page content<p>
<footer slot="footer">footer</footer>
<div>some shadow content</div>
</x-page>
```


The browser has looked at the direct children of the shadow host (`myXPage.children`

) and seen if any of them have a slot attribute that matches the name of a <slot> element in the host’s `shadowRoot`

.

When a match is found, the node is *visually* ‘distributed’ in place of the corresponding <slot> element. Any children left undistributed at the end of this matching process are distributed to a default (unamed) <slot> element (if one exists).

##### For:

- Distribution is more explicit, easier to understand, less ‘magic’.
- Distribution is simpler for the engine to compute.

##### Against:

- Doesn’t explain how built-in elements, like <select>, work.
- Decorating content with slot attributes is more work for the user.
- Less expressive.

### ‘closed’ vs. ‘open’

When a `shadowRoot`

is ‘closed’ the it cannot be accessed via `myHost.shadowRoot`

. This gives a component author *some* assurance that users won’t poke into implementation details, similar to how you can use closures to keep things private.

*Apple* felt strongly that this was an important feature that they would block on. They argued that implementation details should never be exposed to the outside world and that ‘closed’ mode would be a required feature when [‘isolated’ custom elements](https://github.com/w3c/webcomponents/wiki/Isolated-Imports-Proposal) became a thing.

*Google* on the other hand felt that ‘closed’ shadow roots would prevent some accessibility and component tooling use-cases. They argued that it’s impossible to accidentally stumble into a `shadowRoot`

and that if people want to they likely have a good reason. JS/DOM is open, let’s keep it that way.

At the [April meeting](https://www.w3.org/wiki/Webapps/WebComponentsApril2015Meeting) it became clear that to move forward, ‘mode’ needed to be a feature, but vendors were struggling to reach agreement on whether this should default to ‘open’ or ‘closed’. As a result, all agreed that for V1 ‘mode’ would be a required parameter, and thus wouldn’t need a specified default.

```
element.createShadowRoot({ mode: 'open' });
element.createShadowRoot({ mode: 'closed' });
```


### Shadow piercing combinators

A ‘piercing combinator’ is a special CSS ‘combinator’ that can target elements inside a shadow root from the outside world. An example is /deep/ later renamed to `>>>`

:

`.foo >>> div { color: red }`


When Web Components were first specified it was thought that these were required, but after looking at [how they were being used](https://github.com/KarstenB/csstransform/blob/master/bootstrap_deep.css) it seemed to only bring problems, making it too easy to break the style boundaries that make Web Components so appealing.

#### Performance

Style calculation can be incredibly fast inside a tightly scoped Shadow DOM if the engine doesn’t have to take into consideration any outside selectors or state. The very presence of piercing combinators forbids these kind of optimisations.

#### Alternatives

Dropping shadow piercing combinators doesn’t mean that users will never be able to customize the appearance of a component from the outside.

##### CSS custom-properties (variables)

In *Firefox OS* we’re using [CSS Custom Properties](http://dev.w3.org/csswg/css-variables/) to expose specific style properties that can be defined (or overridden) from the outside.

External (user):

```
x-foo { --x-foo-border-radius: 10px; }
```


Internal (author):

`.internal-part { border-radius: var(--x-foo-border-radius, 0); }`


##### Custom pseudo-elements

We have also seen interest expressed from several vendors in reintroducing the ability to define custom pseudo selectors that would expose given internal parts to be styled (similar to how we style parts of <input type=”range”> today).

`<span class="hljs-tag">x-foo</span><span class="hljs-pseudo">::my-internal-part</span> <span class="hljs-rules">{ <span class="hljs-rule"><span class="hljs-attribute">... }</span></span></span>`


This will likely be considered for a Shadow DOM V2 specification.

##### Mixins – @extend

There is [proposed specification](https://tabatkins.github.io/specs/css-extend-rule/) to bring [SASS’s @extend](http://sass-lang.com/documentation/file.SASS_REFERENCE.html#extend) behaviour to CSS. This would be a useful tool for component authors to allow users to provide a ‘bag’ of properties to apply to a specific internal part.

External (user):

```
<span class="hljs-class">.x-foo-part</span> <span class="hljs-rules">{
<span class="hljs-rule"><span class="hljs-attribute">background-color</span>:<span class="hljs-value"> red</span></span>;
<span class="hljs-rule"><span class="hljs-attribute">border-radius</span>:<span class="hljs-value"> <span class="hljs-number">4px</span></span></span>;
<span class="hljs-rule">}</span></span>
```


Internal (author):

```
<span class="hljs-class">.internal-part</span> <span class="hljs-rules">{
<span class="hljs-rule">@<span class="hljs-attribute">extend .x-foo-part;
}</span></span></span>
```


### Multiple shadow roots

*Why would I want more than one shadow root on the same element?*, I hear you ask. The answer is: **inheritance**.

Let’s imagine I’m writing an `<x-dialog>`

component. Within this component I write all the markup, styling, and interactions to give me an opening and closing dialog window.

```
<x-dialog>
<h1>My title</h1>
<p>Some details</p>
<button>Cancel</button>
<button>OK</button>
</x-dialog>
```


The shadow root pulls any user provided content into `div.inner`

via the `<content>`

insertion point.

```
<div class="outer">
<div class="inner">
<content></content>
</div>
</div>
```


I also want to create `<x-dialog-alert>`

that looks and behaves just like `<x-dialog>`

but with a more restricted API, a bit like `alert('foo')`

.

`<x-dialog-alert>foo</x-dialog-alert>`


```
var proto = Object.create(XDialog.prototype);
proto.createdCallback = function() {
XDialog.prototype.createdCallback.call(this);
this.createShadowRoot();
this.shadowRoot.innerHTML = templateString;
};
document.registerElement('x-dialog-alert', { prototype: proto });
```


The new component will have its own shadow root, but it’s designed to work *on top* of the parent class’s shadow root. The `<shadow>`

represents the ‘older’ shadow root and allows us to project content inside it.

```
<shadow>
<h1>Alert</h1>
<content></content>
<button>OK</button>
</shadow>
```


Once you get your head round multiple shadow roots, they become a powerful concept. The downside is they bring a lot of complexity and introduce a lot of edge cases.

#### Inheritance without multiple shadows

Inheritance is still possible without multiple shadow roots, but it involves manually mutating the super class’s shadow root.

```
var proto = Object.create(XDialog.prototype);
proto.createdCallback = function() {
XDialog.prototype.createdCallback.call(this);
var inner = this.shadowRoot.querySelector('.inner');
var h1 = document.createElement('h1');
h1.textContent = 'Alert';
inner.insertBefore(h1, inner.children[0]);
var button = document.createElement('button');
button.textContent = 'OK';
inner.appendChild(button);
...
};
document.registerElement('x-dialog-alert', { prototype: proto });
```


**The downsides of this approach are:**

- Not as elegant.
- Your sub-component is dependent on the implementation details of the super-component.
- This wouldn’t be possible if the super component’s shadow root was ‘closed’, as
`this.shadowRoot`

would be`undefined`

.

## HTML Imports

HTML Imports provide a way to import all assets defined in one `.html`

document, into the scope of another.

`<span class="tag"><link</span> <span class="atn">rel</span><span class="pun">=</span><span class="atv">"import"</span> <span class="atn">href</span><span class="pun">=</span><span class="atv">"/path/to/imports/stuff.html"</span><span class="tag">></span>`


As [previously stated,](https://hacks.mozilla.org/2014/12/mozilla-and-web-components/) *Mozilla* is not *currently* intending to implementing HTML Imports. This is in part because we’d like to see how ES6 modules pan out before shipping another way of importing external assets, and partly because we don’t feel they enable much that isn’t already possible.

We’ve been working with Web Components in *Firefox OS* for over a year and have found using existing module syntax (AMD or Common JS) to resolve a dependency tree, registering elements, loaded using a normal `<script>`

tag seems to be enough to get stuff done.

HTML Imports do lend themselves well to a simpler/more declarative workflow, such as the older [ <element>](https://github.com/MikeMitterer/DART-Sample-PolymerElementConsumer/blob/master/web/poly/components/CustomElements/workbench/HTMLElementElement.html) and

[registration syntax.](https://www.polymer-project.org/0.8/docs/migration.html#registration)

*Polymer’s*currentWith this simplicity has come [criticism](http://tjvantoll.com/2014/08/12/the-problem-with-using-html-imports-for-dependency-management/) from the community that Imports don’t offer enough control to be taken seriously as a dependency management solution.

Before the decision was made a few months ago, *Mozilla* had a working implementation behind a flag, but struggled through an incomplete specification.

### What will happen to them?

*Apple’s *[Isolated Custom Elements](https://github.com/w3c/webcomponents/wiki/Isolated-Imports-Proposal) proposal makes use of an HTML Imports style approach to provide custom elements with their own document scope;: Perhaps there’s a future there.

At *Mozilla* we want to explore how importing custom element definitions can align with upcoming ES6 module APIs. We’d be prepared to implement if/when they appear to enable developers to do stuff they can’t already do.

## To conclude

Web Components are a prime example of how difficult it is to get large features into the browser today. Every API added lives indefinitely and remains as an obstacle to the next.

Comparable to picking apart a huge knotted ball of string, adding a bit more, then tangling it back up again. This knot, our platform, grows ever larger and more complex.

Web Components have been in planning for over three years, but we’re optimistic **the end is near**. All major vendors are on board, enthusiastic, and investing significant time to help resolve the remaining issues.

**Let’s get ready to componentize the web!**

#### More

- Join the ongoing discussion on the
[public-webapps mailing list](https://lists.w3.org/Archives/Public/public-webapps/). - Keep an eye on the
[W3C Web Components Repo](https://github.com/w3c/webcomponents/). - Sign-up to the
[Web Components Weekly](http://webcomponentsweekly.me/)newsletter. - Play with Web Components in Firefox today by turning on ‘dom.webcomponents.enabled’ pref in about:config.

## About
[
Wilson Page ](http://wilsonpage.co.uk)

Front-end developer at Mozilla.

## 40 comments

Brian Di PalmaJune 9th, 2015 at 13:54cody lindleyJune 9th, 2015 at 15:43Paul van DamJune 10th, 2015 at 02:28Wilson PageJune 10th, 2015 at 02:46Wes JohnstonJune 10th, 2015 at 13:12Wilson PageJune 10th, 2015 at 03:01Wilson PageJune 10th, 2015 at 02:37Kevin LozandierJune 10th, 2015 at 11:16Kevin LozandierJune 10th, 2015 at 11:17Wilson PageJune 10th, 2015 at 11:27JoeJune 9th, 2015 at 14:39AngusJuly 6th, 2015 at 09:45Michael J. RyanJuly 8th, 2015 at 20:46Ron WaldonJune 9th, 2015 at 17:22Kevin LozandierJune 9th, 2015 at 17:45Sean HoganJune 9th, 2015 at 20:26SteveLeeJune 10th, 2015 at 03:38Kevin LozandierJune 15th, 2015 at 09:30SteveLeeJune 16th, 2015 at 02:58Kevin LozandierJune 15th, 2015 at 10:20Kevin LozandierJune 15th, 2015 at 10:25SteveLeeJune 16th, 2015 at 02:38Evan YouJune 10th, 2015 at 07:48Cameron SpearJune 10th, 2015 at 19:00Evan YouJune 15th, 2015 at 10:14ThadJune 11th, 2015 at 07:57Wilson PageJune 28th, 2015 at 21:20markgJune 11th, 2015 at 21:08Wilson PageJune 12th, 2015 at 00:38LukeJune 11th, 2015 at 22:50Stephen WilliamsJuly 9th, 2015 at 00:48Erik IsaksenJune 12th, 2015 at 13:32Wilson PageJune 15th, 2015 at 00:45Kristian GerardssonJune 15th, 2015 at 05:10Neil StansburyJune 16th, 2015 at 06:16Neil StansburyJune 16th, 2015 at 06:21Chris SandersJune 20th, 2015 at 12:03Jani TarvainenJuly 8th, 2015 at 19:59numanJuly 8th, 2015 at 21:04PaulJuly 9th, 2015 at 08:49