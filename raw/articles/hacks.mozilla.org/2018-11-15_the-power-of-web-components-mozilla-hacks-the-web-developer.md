---
title: The Power of Web Components – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/11/the-power-of-web-components/
author: Sergi Mansilla
published: '2018-11-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![A video player with a corner folded over, revealing the code that powers it.](../../assets/10fe0ea0c34409fd.png)


## Background

Ever since the first animated DHTML cursor trails and “Site of the Week” badges graced the web, re-usable code has been a temptation for web developers. And ever since those heady days, integrating third-party UI into your site has been, well, a semi-brittle headache.

Using other people’s clever code has required buckets of boilerplate JavaScript or CSS conflicts involving the dreaded `!important`

. Things are a bit better in the world of React and other modern frameworks, but it’s a bit of a tall order to require the overhead of a full framework just to re-use a widget. HTML5 introduced a few new elements like [ <video>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video) and

[, which added some much-needed common UI widgets to the web platform. But adding new standard elements for every sufficiently common web UI pattern isn’t a sustainable option.](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date)

`<input type="date">`

In response, a handful of web standards were drafted. Each standard has some independent utility, but when used together, they enable something that was previously impossible to do natively, and tremendously difficult to fake: the capability to create user-defined HTML elements that can go in all the same places as traditional HTML. These elements can even hide their inner complexity from the site where they are used, much like a rich form control or video player.

## The standards evolve

As a group, the standards are known as [Web Components](https://developer.mozilla.org/en-US/docs/Web/Web_Components). In the year 2018 it’s easy to think of Web Components as old news. Indeed, early versions of the standards have been around in one form or another in Chrome since 2014, and polyfills have been clumsily filling the gaps in other browsers.

After some quality time in the standards committees, the Web Components standards were refined from their early form, now called version 0, to a more mature version 1 that is seeing implementation across all the major browsers. [Firefox 63](https://hacks.mozilla.org/2018/10/firefox-63-tricks-and-treats/) added support for two of the tent pole standards, Custom Elements and Shadow DOM, so I figured it’s time to take a closer look at how you can play HTML inventor!

Given that Web Components have been around for a while, there are lots of other resources available. This article is meant as a primer, introducing a range of new capabilities and resources. If you’d like to go deeper (and you definitely should), you’d do well to read more about Web Components on [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/Web_Components) and the [Google Developers](https://developers.google.com/web/fundamentals/web-components/) site.

Defining your own working HTML elements requires *new powers* the browser didn’t previously give developers. I’ll be calling out these previously-impossible bits in each section, as well as what other newer web technologies they draw upon.

## The `<template>`

element: a refresher

This first element isn’t quite as new as the others, as the need it addresses predates the Web Components effort. Sometimes you just need to store some HTML. Maybe it’s some markup you’ll need to duplicate multiple times, maybe it’s some UI you don’t need to create quite yet. The `<template>`

element takes HTML and parses it without adding the parsed [DOM](https://developer.mozilla.org/en-US/docs/Glossary/DOM) to the current document.

```
<template>
<h1>This won't display!</h1>
<script>alert("this won't alert!");</script>
</template>
```


Where does that parsed HTML go, if not to the document? It’s added to a “document fragment”, which is best understood as a thin wrapper that contains a portion of an HTML document. Document fragments dissolve when appended to other DOM, so they’re useful for holding a bunch of elements you want later, in a container you don’t need to keep.

“Well okay, now I have some DOM in a dissolving container, how do I use it when I need it?”

You could simply insert the template’s document fragment into the current document:

```
let template = document.querySelector('template');
document.body.appendChild(template.content);
```


This works just fine, except you just dissolved the document fragment! If you run the above code twice you’ll get an error, as the second time `template.content`

is gone. Instead, we want to make a copy of the fragment prior to inserting it:

```
document.body.appendChild(template.content.cloneNode(true));
```


The `cloneNode`

method does what it sounds like, and it takes an argument specifying whether to copy just the node itself or include all its children.

The template tag is ideal for any situation where you need to repeat an HTML structure. It particularly comes in handy when defining the inner structure of a component, and thus `<template>`

is inducted into the Web Components club.

#### New Powers:

- An element that holds HTML but doesn’t add it to the current document.

#### Review Topics:

[Document Fragments](https://developer.mozilla.org/en-US/docs/Web/API/DocumentFragment)[Duplicating DOM nodes](https://developer.mozilla.org/en-US/docs/Web/API/Node/cloneNode)using`cloneNode`


## Custom Elements

*Custom Elements* is the poster child for the Web Components standards. It does what it says on the tin – allowing developers to define their own custom HTML elements. Making this possible and pleasant builds fairly heavily on top of ES6’s class syntax, where the v0 syntax was much more cumbersome. If you’re familiar with [classes in JavaScript](https://hacks.mozilla.org/2015/07/es6-in-depth-classes/) or other languages, you can define classes that inherit from or “extend” other classes:

```
class MyClass extends BaseClass {
// class definition goes here
}
```


Well, what if we were to try this?

```
class MyElement extends HTMLElement {}
```


Until recently that would have been an error. Browsers didn’t allow the built-in `HTMLElement`

class or its subclasses to be extended. Custom Elements unlocks this restriction.

The browser knows that a `<p>`

tag maps to the `HTMLParagraphElement`

class, but how does it know what tag to map to a custom element class? In addition to extending built-in classes, there’s now a “Custom Element Registry” for declaring this mapping:

```
customElements.define('my-element', MyElement);
```


Now every `<my-element>`

on the page is associated with a new instance of `MyElement`

. The constructor for `MyElement`

will be run whenever the browser parses a `<my-element>`

tag.

What’s with that dash in the tag name? Well, the standards bodies want the freedom to create new HTML tags in the future, and that means that developers can’t just go creating an `<h7>`

or `<vr>`

tag. To avoid future conflicts, all custom elements must contain a dash, and standards bodies promise to never make a new HTML tag containing a dash. Collision avoided!

In addition to having your constructor called whenever your custom element is created, there are a number of additional “lifecycle” methods that are called on a custom element at various moments:

`connectedCallback`

is called when an element is appended to a document. This can happen more than once, e.g. if the element is moved or removed and re-added.`disconnectedCallback`

is the counterpart to`connectedCallback`

.`attributeChangeCallback`

fires when attributes from a whitelist are modified on the element.

A slightly richer example looks like this:

```
class GreetingElement extends HTMLElement {
constructor() {
super();
this._name = 'Stranger';
}
connectedCallback() {
this.addEventListener('click', e => alert(`Hello, ${this._name}!`));
}
attributeChangedCallback(attrName, oldValue, newValue) {
if (attrName === 'name') {
if (newValue) {
this._name = newValue;
} else {
this._name = 'Stranger';
}
}
}
}
GreetingElement.observedAttributes = ['name'];
customElements.define('hey-there', GreetingElement);
```


Using this on a page will look like the following:

```
<hey-there>Greeting</hey-there>
<hey-there name="Potch">Personalized Greeting</hey-there>
```


But what if you want to extend an existing HTML element? You definitely can and should, but using them within markup looks fairly different. Let’s say we want our greeting to be a button:

```
class GreetingElement extends HTMLButtonElement
```


We’ll also need to tell the registry we’re extending an existing tag:

```
customElements.define('hey-there', GreetingElement, { extends: 'button' });
```


Because we’re extending an existing tag, we actually use the existing tag instead of our custom tag name. We use the new special `is`

attribute to tell the browser what *kind* of button we’re using:

```
<button is="hey-there" name="World">Howdy</button>
```


It may seem a bit clunky at first, but assistive technologies and other scripts wouldn’t know our custom element is a kind of button without this special markup.

From here, all the classic web widget techniques apply. We can set up a bunch of event handlers, add custom styling, and even stamp out an inner structure using `<template>`

. People can use your custom element alongside their own code, via HTML templating, DOM calls, or even new-fangled frameworks, several of which support custom tag names in their virtual DOM implementations. Because the interface is the standard DOM interface, Custom Elements allows for truly portable widgets.

#### New Powers

- The ability to extend the built-in ‘HTMLElement’ class and its subclasses
- A custom element registry, available via
`customElements.define()`

- Special lifecycle callbacks for detecting element creation, insertion to the DOM, attribute changes, and more.

#### Review Topics

[ES6 Classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes), particularly[subclassing and the](https://hacks.mozilla.org/2015/08/es6-in-depth-subclassing/)`extends`

keyword

## Shadow DOM

We’ve made our friendly custom element, we’ve even thrown on some snazzy styling. We want to use it on all our sites, and share the code with others so they can use it on theirs. How do we prevent the nightmare of conflicts when our customized `<button>`

element runs face-first into the CSS of other sites? Shadow DOM provides a solution.

The Shadow DOM standard introduces the concept of a *shadow root*. Superficially, a shadow root has standard DOM methods, and can be appended to as if it was any other DOM node. Shadow roots shine in that their contents don’t appear to the document that contains their parent node:

```
// attachShadow creates a shadow root.
let shadow = div.attachShadow({ mode: 'open' });
let inner = document.createElement('b');
inner.appendChild(document.createTextNode('Hiding in the shadows'));
// shadow root supports the normal appendChild method.
shadow.appendChild(inner);
div.querySelector('b'); // empty
```


In the above example, the `<div>`

“contains” the `<b>`

and the `<b>`

is rendered to the page, but the traditional DOM methods can’t see it. Not only that, but the styles of the containing page can’t see it either. This means that styles outside of a shadow root can’t get in, and styles *inside* the shadow root don’t leak out. This boundary is **not** meant to be a security feature, as another script on the page could detect the shadow root’s creation, and if you have a reference to a shadow root, you can query it directly for its contents.

The contents of a shadow root are styled by adding a `<style>`

(or `<link>`

) to the root:

```
let style = document.createElement('style');
style.innerText = 'b { font-weight: bolder; color: red; }';
shadowRoot.appendChild(style);
let inner = document.createElement('b');
inner.innerHTML = "I'm bolder in the shadows";
shadowRoot.appendChild(inner);
```


Whew, we could really use a `<template>`

right about now! Either way, the `<b>`

will be affected by the stylesheet in the root, but any outer styles matching a `<b>`

tag will not.

What if a custom element has non-shadow content? We can make them play nicely together using a new special element called `<slot>`

:

```
<template>
Hello, <slot></slot>!
</template>
```


If that template is attached to a shadow root, then the following markup:

```
<hey-there>World</hey-there>
```


Will render as:

```
Hello, World!
```


This ability to composite shadow roots with non-shadow content allows you to make rich custom elements with complex inner structures that look simple to the outer environment. Slots are more powerful than I’ve shown here, with multiple slots and named slots and special CSS pseudo-classes to target slotted content. You’ll have to read more!

#### New Powers:

- A quasi-obscured DOM structure called a “shadow root”
- DOM APIs for creating and accessing shadow roots
- Scoped styles within shadow roots
- New CSS
[pseudo-classes](https://developer.mozilla.org/en-US/docs/Web/CSS/:host())for working with shadow roots and scoped styles [The](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_templates_and_slots)`<slot>`

element

## Putting it all together

Let’s make a fancy button! We’ll be creative and call the element `<fancy-button>`

. What makes it fancy? It will have a custom style, and it will also allow us to supply an icon and make that look snazzy as well. We’d like our button’s styles to stay fancy no matter what site you use them on, so we’re going to encapsulate the styles in a shadow root.

You can see the completed custom element in the interactive example below. Be sure to take a look at both the JS definition of the custom element and the HTML `<template>`

for the style and structure of the element.

## Conclusion

The standards that make up Web Components are built on the philosophy that by providing multiple low-level capabilities, people will combine them in ways that nobody expected at the time the specs were written. Custom Elements have already been used to make it easier to [build VR content on the web](https://aframe.io/), spawned [multiple](https://www.polymer-project.org/) [UI toolkits](https://vaadin.com/), and much more. Despite the long standardization process, the emerging promise of Web Components puts more power in the hand of creators. Now that the technology is available in browsers, the future of Web Components is in your hands. What will you build?

## 5 comments

TornikeNovember 15th, 2018 at 13:16PotchNovember 15th, 2018 at 14:37Feross AboukhadijehNovember 24th, 2018 at 17:33Da ScritchNovember 27th, 2018 at 06:23voracityNovember 30th, 2018 at 04:11