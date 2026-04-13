---
title: Speed Up App Development with X-Tag and Web Components – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2013/05/speed-up-app-development-with-x-tag-and-web-components/
author: Daniel Buchner
published: '2013-05-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In the last few years we’ve witnessed an evolution in what ‘app’ means to both developers and consumers. The word app evokes the idea of a rich, task-oriented user experience with highly optimized user interface that responds to its environment and can be used on an array of common devices. In order to make development of rich app experiences easier, native platforms have generated many of their own controls and components that Just Work™.

For other native technology stacks, extensible components are all but assumed – not so much for the web. Soon, that all changes. We are on the verge of a declarative renaissance that will dramatically advance app development for the web platform, and Web Components will drive it.

X-Tag and Web Components offer features that obliterate the status quo for layout, UI, and widget development – here’s a few notable Web Component features:

- Create real custom elements the browser understands
- Stop the instantiation madness:
~~$$(‘button.super’).initSuperButton()~~ - Remove unmanageable HTML widget guts from your app’s view files
- Work with sharable components, based on standard technologies

## Meet the Web Components Family

Web Components is a group of W3C specifications, quickly moving toward standardization, that provide a robust HTML component model. You should not assume the following specs are implemented in your browser of choice. While these specifications are in various stages of implementation across browsers, you can use X-Tag (with either [Mozilla](https://github.com/mozilla/web-components/blob/master/src/document.register.js) or [Google’s](https://github.com/toolkitchen/CustomElements/tree/master) prollyfill) today to create custom elements that work well in recent version of Firefox, Chrome, Safari, and stock mobile browsers. X-Tag is a powerful sugar library primarily focused on wrapping and enhancing one of the draft-state Web Component specs: Custom Elements (document.register). We’ll get to X-Tag shortly – but for now, let’s quickly review the key features of each spec:

### Custom Elements

[Custom Elements](https://dvcs.w3.org/hg/webcomponents/raw-file/tip/spec/custom/index.html) provides you a way to create new elements for use in your environment. There are two ways to declare a new custom element, the imperative DOM API – document.register(), and the declarative HTML tag –

Here’s an example of what a custom element registration looks like in both the declarative and imperative styles:

```
document.register('x-foo', {
prototype: Object.create(HTMLElement.prototype, {
readyCallback: {
value: function(){
// do stuff here when your element is created
this.innerHTML = 'Barrrr me matey!';
}
},
bar: {
get: function() { return 'bar'; },
},
// add more properties to your custom prototype
// ...
})
});
```

```
```

### Shadow DOM

The [Shadow DOM](https://dvcs.w3.org/hg/webcomponents/raw-file/tip/spec/shadow/index.html) allows you to encapsulate structural and supporting elements within components. Elements within [shadow boundary](https://dvcs.w3.org/hg/webcomponents/raw-file/tip/spec/shadow/index.html#dfn-shadow-boundary).

### HTML Templates

[HTML Templates](https://dvcs.w3.org/hg/webcomponents/raw-file/tip/spec/templates/index.html) bring simple DOM templating and markup reuse to the web platform – which are often shimmed today using the [ HTMLScriptElement + DocumentFragment hack-pattern](http://stackoverflow.com/questions/4912586/explanation-of-script-type-text-template-script).


### HTML Imports

[HTML Imports](https://dvcs.w3.org/hg/webcomponents/raw-file/tip/spec/imports/index.html) are external HTML documents that contain declarative component definitions. HTML component documents can by imported using the `link`

element with the `rel`

attribute value `import`

. Imported resources may themselves contain additional sub-imports, which the browser then retrieves and performs automatic dependency resolution upon.

## Web Components + X-Tag = WINNING

Mozilla’s [X-Tag library](http://www.x-tags.org) enhances the imperative (JavaScript) route for creating custom elements. X-Tag’s primary interface is the `xtag.register()`

method – it wraps the soon-to-be standard `document.register()`

DOM API with features and functionality that make development of amazing custom elements effortless.

### Creating a Custom Element

Here’s a quick example of what registering a custom element looks like using X-Tag:

```
xtag.register('x-pirate', {
lifecycle: {
ready: function(){
this.innerHTML = '
```' +
'

Barrr me matey!' +
'

';
}
},
accessors: {
src: {
// X-Tag's attribute sugar relays any value passed to the src
// setter on to the src attribute of our and its
//

element (specified by CSS selector), and vice versa.
attribute: { selector: 'img' },
set: function(){
// When a 's src attribute/setter is changed, we
// stop everything to announce the arrival of a new pirate.
// Ex: doc.querySelector('x-pirate').src = 'pirate-2.png';
alert("There's a new captain on deck ye scurvy dogs!");
}
}
},
events: {
// This is an example of X-Tag's event and pseudo systems. The
// "tap" custom event handles the dance between click and touch,
// the ":delegate(img)" pseudo ensures our function is only
// called when tapping the

inside our .
'tap:delegate(blockquote > img)': function(){
alert("A pirate's life for me!");
}
}
});

### To the Democave Batman!

We’re actively working on a custom element UI toolkit and style pack that will make development of app interfaces a breeze. It’s still in very early stages, but we have a [few demos for you](http://ui.x-tags.org).

### Get the Code

Head over to [X-Tags.org](http://www.x-tags.org) and grab the code to develop custom elements of your own. After you get the hang of things, start contributing to our [open source effort](https://github.com/x-tag)!

## About Daniel Buchner

I'm a Product Manager at Mozilla and have an unhealthy love for building Open Web tech. I also dig economics, fast cars, classic rock and the Seattle Seahawks.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 5 comments

ericMay 14th, 2013 at 05:52Daniel BuchnerMay 14th, 2013 at 08:02CodespendMay 14th, 2013 at 11:05Robert Nyman [Editor]May 14th, 2013 at 15:34SimonMay 18th, 2013 at 00:18