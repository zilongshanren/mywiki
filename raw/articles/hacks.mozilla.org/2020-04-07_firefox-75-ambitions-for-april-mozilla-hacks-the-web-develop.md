---
title: 'Firefox 75: Ambitions for April – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2020/04/firefox-75-ambitions-for-april/
author: Chris Mills
published: '2020-04-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Even in these times of isolation, our engineering teams have adapted, kept focused, and worked hard to bring you another exciting new edition of Firefox. On the developer tools side, you’ll find instant evaluation in the console, event breakpoints for WebSockets, and many other things besides. On the web platform side, new additions include HTML lazy loading for images, the CSS `min()`

, `max()`

, and `clamp()`

functions, public static class fields, and additions to Web Animations API support.

As always, read on for the highlights, or find the full list of additions in the following articles:

## Developer tools additions

Let’s start by reviewing the most interesting Developer Tools additions for 75.

### Instant evaluation for console expressions

Evaluating expressions in the [Console](https://developer.mozilla.org/docs/Tools/Web_Console) is a rapid way to explore your application state, query the DOM, or just try out JavaScript APIs. It’s now easier to prototype longer code with [Firefox’s multi-line Console mode](https://developer.mozilla.org/docs/Tools/Web_Console/The_command_line_interpreter#Multi-line_mode), which becomes ever friendlier and more IDE-like to use.

The new *Instant evaluation* previews the results of the current expression as you type, similar to editors like [Quokka.js](https://quokkajs.com/). As long as expressions typed into the Web Console are side-effect free, their results will be previewed while you type.

A lot of polish went into making the preview as seamless as possible. Elements for DOM nodes in results are highlighted. The in-code autocomplete recommends methods and properties based on the result type. Also, you can preview errors to help you fix expressions faster.

### Better inspection & measuring

#### Area measuring is now resizable

Using the optional [area measurement tool](https://developer.mozilla.org/docs/Tools/Measure_a_portion_of_the_page) in DevTools you can quickly draw rectangles over your page to measure the height, width, and diagonal length of specific areas. You can enable the tool in the settings, under “Available Toolbox Buttons”. Thanks to [Sebastian Zartner [:sebo]](https://github.com/SebastianZ), these rectangles now have resize-handles, so you can adjust them precisely.

#### Use XPath to find DOM elements

[XPath queries](https://developer.mozilla.org/docs/Web/XPath) are commonly used in automation tools to tell software which elements to look for and interact with. Thanks again to sebo, you can now use XPath in the [Inspector’s HTML search](https://developer.mozilla.org/docs/Tools/Page_Inspector/How_to/Examine_and_edit_HTML#XPath_search) for DOM elements. This makes it easier to test expressions and fine-tune queries on real sites.

### Event breakpoints for WebSockets

[WebSocket inspection](https://hacks.mozilla.org/2019/10/firefoxs-new-websocket-inspector/) features have improved in every recent DevTools release. This time there’s a nice addition to debugging, thanks to a contribution from the talented [Chujun Lu](https://bugzilla.mozilla.org/user_profile?user_id=632471).

You now have the option to either pause or log when WebSocket event handlers are executed. Use the newly-added [Event Listener Breakpoints](https://developer.mozilla.org/docs/Tools/Debugger/Set_event_listener_breakpoints) in the Debugger. When you select the Log option, event data and the handler that’s been executed will be logged, but execution will not pause.

In other WebSocket Inspector news, the message filter now supports regular expressions, thanks to long-time contributor [Outvi V](https://bugzilla.mozilla.org/user_profile?user_id=603026).

### Network additions

A lot of quality and performance work went into the Network panel for Firefox 75. This release marks major improvements for how fast simultaneous quick-firing requests are rendered without taxing your CPU.

On the interface side, contributor [Florens Verschelde](https://fvsch.com/) drove the proposal and design for adding borders between columns to aid readability. Note how the design is more consistent with the overall look of the DevTools. Filter buttons are also more legible, with improved contrast between states, thanks to contributor [Vitalii](https://bugzilla.mozilla.org/user_profile?user_id=657068).

The Request Blocking panel helps you test how resilient your site is when matched requests fail. It now allows wildcard patterns with “*”. Thanks to [Duncan Dean](https://bugzilla.mozilla.org/user_profile?user_id=472694) for that contribution.

### Early-access DevTools features in Developer Edition

[Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) is Firefox’s pre-release channel. It provides early access to tooling and platform features. Its settings also enable more functionality for developers by default. We like to bring new features quickly to Developer Edition to gather your feedback, including the following highlights.

#### Async Stack Traces for Debugger & Console

Modern JavaScript code depends heavily upon stacking [ async/await](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/async_function) on top of other

[async operations](https://developer.mozilla.org/docs/Learn/JavaScript/Asynchronous)like events, promises, and timeouts. Thanks to better integration with the JavaScript engine, async execution is now captured to provide a more complete picture.

Async call stacks in the Debugger let you step through events, timeouts, and promise-based function calls that are executed over time. In the Console, async stacks make it easier to find the root causes of errors.

## Web platform updates

Let’s explore what Firefox 75 provides in terms of web platform updates.

### HTML lazy loading for images

[Lazy loading](https://developer.mozilla.org/docs/Web/Performance/Lazy_loading) is a common strategy to improve performance by identifying resources as non-blocking (non-critical) and loading them only when needed, rather than loading them all immediately. Images are one of the most common assets to be lazy-loaded in web apps.

To make lazy loading images easier, we have introduced support for the load attribute on the HTML [ <img>](https://developer.mozilla.org/docs/Web/HTML/Element/img) element. Setting the value to

*lazy*will instruct the browser to defer loading of images that are off-screen until the user scrolls near them. The only other possible value is

*eager*, which is the default value as you’d expect.

`<img src="image.jpg" loading="lazy" alt="..." />`


You can determine if a given image has finished loading by examining the value of its boolean `complete`

property.

Note: The `load`

event fires when the eagerly-loaded content has all been loaded. At that time, it’s possible (or even likely) that there may be lazily-loaded images within the visual viewport that have yet to load.

Note: Chrome has also implemented experimental support for lazy loading of [ <iframe>](https://developer.mozilla.org/docs/Web/HTML/Element/iframe) content, but this is not in a standard yet; we are waiting until it has been standardized.

### CSS `min()`

, `max()`

, and `clamp()`


Some exciting new CSS additions this month! We have added support for three very useful CSS functions that are closely-related to each other but have different purposes:

— accepts one or more possible values or calculations to choose from, and ensures that the value used in all situations will be the smallest of the possibilities. In effect, this provides a range of values for responsive designs, along with a maximum allowed value.`min()`

— accepts one or more possible values or calculations to choose from, and ensures that the value used in all situations will be the largest of the possibilities. In effect, this provides a range of values for responsive designs, along with a minimum allowed value.`max()`

— accepts three values or calculations: a minimum, preferred, and a maximum. The minimum or maximum will be used if the computed value falls below the minimum or above the maximum. The preferred value will be used if the computed value falls between the two. This allows the property value to adapt to changes in the element or page it is assigned to, while remaining between the minimum and maximum values.`clamp()`


These functions are very useful for responsive design, and can save a lot of time and code doing things that you might previously have done using a combination of [ min-width](https://developer.mozilla.org/docs/Web/CSS/min-width),

[, and](https://developer.mozilla.org/docs/Web/CSS/width)

`width`

[, multiple](https://developer.mozilla.org/docs/Web/CSS/max-width)

`max-width`

[media queries](https://developer.mozilla.org/docs/Web/CSS/Media_Queries), or even

[JavaScript](https://developer.mozilla.org/docs/Web/javascript).

#### CSS `min()`

, `max()`

, and `clamp()`

in action

Let’s study the following example:

```
html {
font-family: sans-serif;
}
body {
margin: 0 auto;
width: min(1000px, calc(70% + 100px));
}
h1 {
letter-spacing: 2px;
font-size: clamp(1.8rem, 2.5vw, 2.8rem)
}
p {
line-height: 1.5;
font-size: max(1.2rem, 1.2vw);
}
```


Here, we’ve got the body width set to `min(1000px, calc(70% + 100px))`

, which means that in wider viewports the body content will be `1000px`

wide. In narrower viewports, the body content will be `70%`

of the viewport width plus `100px`

(up until this calculation’s result becomes `1000px`

or more)!

The top level heading’s font-size is set to `clamp(1.8rem, 2.5vw, 2.8rem)`

. Thus, it will be a minimum of `1.8rem`

, and a maximum of `2.8rem`

. In between those values, the ideal value of `2.5vw`

will kick in, so you will see the header text grow and shrink at viewport widths where `2.5vw`

is computed as larger than `1.8rem`

, but smaller than `2.8rem`

.

The paragraph font-size is set to `max(1.2rem, 1.2vw)`

, meaning that it will be a minimum of `1.2rem`

. But it will start to grow at the point that `1.2vw`

’s computed value is larger than `1.2rem`

s’ computed value.

You can see this in action in our [ min(), max(), clamp() simple example](https://mdn.github.io/css-examples/min-max-clamp/).



### JavaScript language features

There have been a few interesting JavaScript additions in 75.

First of all, we’ve now got [public static class fields](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Classes/Class_fields#Public_static_fields). These are useful when you want a field to exist only once per class, not on every class instance you create. This is particularly relevant for cache, fixed-configuration, or any other data you don’t need to replicate across instances. The basic syntax looks like so:

```
class ClassWithStaticField {
static staticField = 'static field'
}
console.log(ClassWithStaticField.staticField)
// expected output: "static field"
```


Next up, we’ve got another boost to internationalization (i18n) functionality with the addition of [ Intl.Locale](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Locale), a standard built-in constructor that represents a Unicode locale identifier. For example, you could create a Korean locale object like so:

```
const korean = new Intl.Locale('ko', {
script: 'Kore', region: 'KR', hourCycle: 'h24', calendar: 'gregory'
});
```


And then return properties of the object as you’d expect:

```
console.log(korean.hourCycle, japanese.hourCycle);
// expected output: "h24" "h12"
```


### Form additions

We’ve got a couple of useful form-specific API additions in Firefox 75:

- The
interface has a new method,`HTMLFormElement`

. Unlike the old (and still available)`requestSubmit()`

method,`submit()`

`requestSubmit()`

acts as if a specified submit button has been clicked, rather than just sending the form data to the recipient. Thus theevent is delivered and the form is checked for validity prior to the data being submitted.`submit`

- The
event is now represented by an object of type`submit`

rather than a simple`SubmitEvent`

.`Event`

`SubmitEvent`

includes a newproperty, which returns the`submitter`

that was invoked to trigger the form submission. With this event, you can have a single handler for submit events that can discern which of multiple submit buttons or links was used to submit the form.`Element`


### Web Animations API enhancements

In 75, we’ve added a number of new Web Animations API features, making this spec even more interesting and useful.

#### Implicit to/from keyframes

From now on, you are able to set a beginning or end state for an animation only (i.e., a single keyframe). The browser will then infer the other end of the animation if it is able to. For example, consider [this simple animation](https://mdn.github.io/dom-examples/web-animations-api/implicit-keyframes.html) — the keyframe object looks like so:

```
let rotate360 = [
{ transform: 'rotate(360deg)' }
];
```


We have only specified the end state of the animation, and the beginning state is implied.

#### Automatically removing filling animations

It is possible to trigger a large number of animations on the same element. If they are indefinite (i.e., forwards-filling), this can result in a huge animations list, which could create a memory leak. For this reason, we’ve implemented the part of the Web Animations spec that automatically removes overriding forward filling animations, unless the developer explicitly specifies to keep them.

You can see this in action in our simple [replace indefinite animations demo](https://mdn.github.io/dom-examples/web-animations-api/replace-indefinite-animations.html). The related JavaScript features are as follows:

`animation.commitStyles()`

— run this method to commit the end styling state of an animation to the element being animated, even after that animation has been removed. It will cause the end styling state to be written to the element being animated, in the form of properties inside a style attribute.`animation.onremove`

— allows you to run an event handler that fires when the animation is removed (i.e., put into an active replace state).`animation.persist()`

— when you explicitly want animations to be retained, then invoke`persist()`

.`animation.replaceState`

— returns the replace state of the animation. This will be`active`

if the animation has been removed, or`persisted`

if`persist()`

has been invoked.

#### Timelines

The [ Animation.timeline](https://developer.mozilla.org/docs/Web/API/Animation/timeline) getter,

[,](https://developer.mozilla.org/docs/Web/API/Document/timeline)

`Document.timeline`

[, and](https://developer.mozilla.org/docs/Web/API/DocumentTimeline)

`DocumentTimeline`

[features are now enabled by default, meaning that you can now access your animation’s timeline information. This feature is invaluable for returning time values for synchronization purposes.](https://developer.mozilla.org/docs/Web/API/AnimationTimeline)

`AnimationTimeline`

By default, the animation’s timeline and the document’s timeline are the same.

#### Getting active animations

Last but not least, the [ Document.getAnimations()](https://developer.mozilla.org/docs/Web/API/Document/getAnimations) and

[methods are now enabled by default. Respectively, these allow you to return an array of all the active animations on an entire document, or on a specific element.](https://developer.mozilla.org/docs/Web/API/Element/getAnimations)

`Element.getAnimations()`

### ARIA annotations

In Firefox 75 (on Linux and Windows), you’ll see the addition of support for a set of new accessibility features collectively known as ARIA annotations, which are set to be published in the upcoming WAI-ARIA version 1.3 specification. These features make it possible to create accessible annotations within web documents. Typical use cases include edit suggestions (i.e., an addition and/or deletion in an editable document), and comments (e.g. an editorial comment related to a part of a document under review).

There is no screenreader support available for ARIA Annotations yet, but soon we’ll be able to make use of these new roles and other attributes. For examples and more support details, read [ARIA Annotations](https://developer.mozilla.org/docs/Web/Accessibility/ARIA/Annotations) on MDN.

## Browser extensions

Two new [ browserSettings](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/browserSettings) have been added to the

[WebExtensions API](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions):

[to zoom the text on a page and](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/browserSettings/zoomFullPage)

`zoomFullPage`

[, which determines if zoom applies to only the active tab or all tabs of the same site.](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/browserSettings/zoomSiteSpecific)

`zoomSiteSpecific`

## Summary

So there you have it. We’ve packed Firefox 75 with interesting new features; check them out, and have fun playing! As always, feel free to give feedback and ask questions in the comments.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 7 comments

OrenApril 7th, 2020 at 08:43RuturajApril 8th, 2020 at 02:38voracityApril 8th, 2020 at 06:21EvilSparkApril 8th, 2020 at 14:43AliApril 9th, 2020 at 03:51Łukasz LeśkoApril 11th, 2020 at 04:42ZumDeWaldApril 16th, 2020 at 07:13