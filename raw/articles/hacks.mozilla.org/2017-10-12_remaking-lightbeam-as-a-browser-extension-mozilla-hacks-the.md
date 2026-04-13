---
title: Remaking Lightbeam as a browser extension – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/10/remaking-lightbeam-as-a-browser-extension/
author: Bianca Danforth
published: '2017-10-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Browser extensions: a new frontier

You may have heard of [browser extensions](https://developer.mozilla.org/en-US/Add-ons/WebExtensions) — perhaps you have even written one yourself. The technology for building extensions in Firefox has been modernized to support Web standards, and is one of the reasons why [Firefox Quantum](https://www.mozilla.org/firefox/quantum/) will be the fastest and most stable release yet.

Extensions built with the new [WebExtensions API](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API) are compatible with all modern browsers, which means you can write one code base that runs in multiple browsers, just as you would a website.

Today, I will talk about what I learned from writing my first extension using the WebExtensions API — namely what I believe to be the biggest conceptual difference (and one of the most common developer pitfalls) — between a browser extension and a traditional web application. I will illustrate with some practical examples and tips taken from my experience developing Lightbeam.

### What is Lightbeam?

[Lightbeam](https://github.com/mozilla/lightbeam-we) — previously a legacy add-on — is a privacy browser extension that visualizes the connections between the sites that you visit and third parties that may be tracking you. It works by listening for, capturing, storing and ultimately displaying requests made by each website as you browse the Web.

### What is a browser extension?

[Browser extensions](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/What_are_WebExtensions) allow you to write web applications that have browser superpowers using familiar front-end technologies.

Traditional web applications are limited by the browser [sandbox](https://en.wikipedia.org/wiki/Sandbox_(computer_security)): scripts can only run with the privileges of an individual web page, whereas browser extension scripts can run with some privileges of the browser. This is perhaps the biggest difference between browser extensions and traditional web applications. For example, if Lightbeam were a traditional web application, it would only be able to see its own requests; as a browser extension, however, it can see all requests made by all websites.

### The Pitfall

Our team didn’t fully appreciate this until we encountered it in the wild: we tried to include what is known as a [background script](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Anatomy_of_a_WebExtension#Background_scripts) for storage with a `<script>`

tag in our application’s `index.html`

document. In our case, we made the false assumption that we could fetch data from storage in this way to update our visualization page. In reality, we had accidentally loaded two instances of this storage script, one with the `<script>`

tag in the page showing the vizualization and one by including the same script in our browser extension’s [manifest](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json) file, and the two instances were not synched. As you can imagine, there were bugs, lots of bugs.

While MDN does try to explain how these scripts differ from each other, browser extensions can be somewhat complicated when coming from a web development background. Here we will discuss the practical implications in the hopes of sparing would-be browser extension developers this frustration!

### So what’s the difference between all these scripts?

There are two types of scripts unique to browser extensions: [content scripts](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Content_scripts) and [background scripts](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Anatomy_of_a_WebExtension#Background_scripts) that operate alongside the more familiar page scripts we all know and love.

**Content scripts**

Content scripts are loaded through the browser extension’s [manifest](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json) file or via the [ tabs](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/tabs) WebExtensions API with

`tabs.executeScript()`

.Since we don’t use content scripts in Lightbeam, here’s an example of how to load content scripts using the manifest file from another browser extension, [Codesy](https://github.com/codesy/widgets):

```
"content_scripts": [
{
"all_frames": false,
"js": [
"js/jquery-3.2.0.min.js",
"js/issue.js"
],
"matches": [
"*://*.github.com/*"
]
}
],
```


As you can see from the manifest, we ask to inject a specified set of content scripts (`jquery-3.2.0.min.js`

and `issue.js`

) into any document which `matches`

a set of URLs (any `github.com`

URL).

Content scripts run in the context of a particular web page — in other words, they execute when a tab with a matching URL loads, and they stop when that tab is closed.

Content scripts do not share the same origin as the extension’s pages and scripts. Instead they are loaded into a window using a sandbox mechanism and have permission to access and modify the DOM for most web pages loaded in a tab (a notable exception being about:* pages). It should be noted that since content scripts are isolated from the web page scripts, they do not have access to the same scope. As a result, content scripts use a ‘clean view’ of the DOM. This ensures that none of the built-in JavaScript methods the content scripts use are overwritten by any website’s page scripts.

Aside from being able to read the page’s DOM, Content scripts also have limited access to [WebExtensions APIs](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API).

Content scripts have many uses. For example, Codesy uses its `issue.js`

content script to insert an `<iframe>`

element into a GitHub page. This `<iframe>`

in turn loads a Codesy page with a form that users can fill out and submit to use the Codesy service. Content scripts can also inject script elements into the page’s DOM directly, as if the page had loaded the script itself – a common use case is to interact with events not available in the content script sandbox. Scripts injected into a page do NOT have access to browser WebExtensions APIs though (they are the same as any other scripts loaded by the web page).

**Background scripts versus extension page scripts**

Now that we’ve gotten content scripts out of the way, let’s talk about Lightbeam!

In Lightbeam, most of the content runs as a web page loaded from within the extension. The scripts in this page (which I will refer to as “extension page scripts” for lack of a better term) run the UI, including the visualization. This page is loaded in a tab when the user presses the Lightbeam icon in the browser toolbar, and runs until the the user closes the tab.

In addition to this page, we also use background scripts. Background scripts are automatically loaded when the extension is installed. In Lightbeam, background scripts capture, filter and store the request data used by Lightbeam’s visualization.

While both extension page scripts and background scripts have access to the WebExtensions APIs (they share the same `moz-extension://`

origin), they differ in many other respects.

*Inclusion*

Here’s how you include an extension page script in your browser extension:

```
<script src="js/lightbeam.js" type="text/javascript"></script>
```


In other words, extension page scripts for a browser extension are very similar to your average page script that runs in the context of a webpage. The notable difference is that extension page scripts have access to WebExtensions APIs.

By contrast, you can include a background script in your browser extension by adding it to the extension’s manifest file:

```
"background": {
"scripts": [
"js/store.js"
]
}
```


*Lifetime*

Extension page scripts run in the context of the application: they load when the extension page loads and persist until the extension page is closed.

By contrast, background scripts run in the browser context. They load when the extension is installed and persist until the extension is disabled or uninstalled, independent of the lifetime of any particular page or browser window.

*Scope*

Given these differing contexts and lifetimes, it may come as no surprise that extension page scripts and background scripts don’t share the same global scope. In other words, you can’t directly call a background script method from an extension page script, and vice versa. Thankfully there is a WebExtensions API for that!

### How to communicate between different kinds of scripts

We use asynchronous message passing via the [runtime](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/runtime) WebExtensions API to communicate between our extension page scripts and background scripts.

To illustrate this, let’s walk through every step in the process for Lightbeam’s ‘Reset Data’ feature.

At a high level, when the user clicks the ‘Reset Data’ button, all of Lightbeam’s data is deleted from storage and the application is reloaded to update the visualization in the UI.

In our `lightbeam.js`

extension page script, we:

- Add a
`click`

event handler to the reset button - When the reset button is clicked:
- Clear the data in storage
- Reload the page


```
// lightbeam.js
const resetData = document.getElementById('reset-data-button');
// 1. Add a ‘click’ event handler to the reset button
resetData.addEventListener('click', async () => {
// 2. When the reset button is clicked:
// 2.a. Reset the data in storage
await storeChild.reset();
// 2.b. Reload the page
window.location.reload();
});
```


`storeChild`

is another extension page script that passes a message to the `store`

background script to clear all our data. We will come back to `storeChild`

, but for the moment, let’s talk about what needs to happen in `store`

.

For `store`

to receive a message from any extension page script, it has to be listening for one, so let’s set up an `onMessage`

listener in `store`

using the `runtime`

WebExtensions API.

In our `store.js`

background script, we:

- Add an
`onMessage`

listener - When the message is received:
- Clear the data in storage


```
// store.js background script
// 1. Add an `onMessage` listener
browser.runtime.onMessage.addListener(async () => {
// 2. When the message is received
// 2.a. Clear the data in storage
await this.reset();
});
async reset() {
return await this.db.websites.clear();
},
```


Now that we have our `lightbeam.js`

extension page script and `store.js`

background script sorted out, let’s discuss where `storeChild`

comes in.

### Separation of Concerns

To recap, our Lightbeam extension page script listens for the `click`

event on the ‘Reset Data’ button, calls `storeChild.reset()`

and then reloads the application. `storeChild`

, is an extension page script that uses the `runtime`

WebExtensions API to send the “reset” message to the `store`

background script. You may be wondering why we can’t just communicate directly between `lightbeam.js`

and `store.js`

. The short answer is that, while we could, we want to adhere to the software design principle known as “separation of concerns”.

Basically, we want our Lightbeam extension page script, `lightbeam.js`

to only handle UI-related functionality. And, in the same way we want our `store.js`

background script to only handle storage functionality. (we, of course, *have* to use the background script for storage, so that the network data persists between sessions!). It would be wise then to set up an intermediary, `storeChild`

that takes on the separate concern of communicating between `lightbeam.js`

and `store.js`

.

Completing the chain for our ‘Reset Data’ feature, in `storeChild.js`

we need to forward the `reset`

call from `lightbeam.js`

to `store.js`

by sending a message to `store.js`

. Since `reset`

is only one of a number of potential methods we need to access from the `store.js`

background script, we configure `storeChild`

as a proxy object of `store`

.

### What is a proxy object?

One of the primary tasks performed by `storeChild.js`

is to call `store.js`

methods on behalf of the `lightbeam.js`

extension page script, such as `reset`

. In Lightbeam, `reset`

is only one of many `store.js`

methods that we want to be able to access from the extension page scripts. Rather than duplicate each method in `store.js`

inside of `storeChild.js`

, we might like to generalize these calls. This is where the idea of a [proxy object](https://rosettacode.org/wiki/Respond_to_an_unknown_method_call#JavaScript) comes in!

```
const storeChildObject = {
parentMessage(method, ...args) {
return browser.runtime.sendMessage({
type: 'storeCall',
method,
args
});
}
// ...other methods
};
const storeChild = new Proxy(storeChildObject, {
get(target, prop) {
if (target[prop] === undefined) {
return async function(...args) {
return await this.parentMessage(prop, ...args);
};
} else {
return target[prop];
}
}
});
```


A proxy object can be extremely useful for a browser extension, as it allows us to follow the software design principle: “Don’t Repeat Yourself”.

In Lightbeam’s case, `storeChild`

serves as a proxy object in the extension page context for `store`

. What this means is that when the `lightbeam.js`

extension page script needs to call a `store.js`

method, such as `store.reset`

–which it doesn’t have direct access to, it will instead call `storeChild.reset`

–which it does have direct access to. Instead of duplicating the `reset`

method in `storeChild`

, we set up a proxy object. Thus, if `storeChild`

doesn’t have a particular method, it will pass along that method call and any arguments to the `store`

via message passing.

### The `web-ext`

CLI

Now that we’ve talked about the most important and arguably most confusing browser extension concept and practical ways to apply this knowledge, I encourage you to write your own browser extension! Before you go, let me offer one final piece of advice.

You may already be familiar with live reloading development tools, in which case, you will be delighted to hear there is such a tool for browser extensions!

[ web-ext](https://github.com/mozilla/web-ext) is an extremely helpful browser extension CLI created and actively developed by Mozilla.

Among its many useful features, `web-ext`

lets you:

- Develop and test locally with live reloading.
- Specify which version of Firefox to run the browser extension in.
- Export your browser extension as an
[XPI](https://developer.mozilla.org/en-US/docs/Mozilla/XPI)when you’re ready to ship.

### Where do we go from here?

These are exciting times for the Web, and we expect browser extensions to become even more popular as they become ever more interoperable. Understanding these concepts and using these techniques and tools have really helped our team to create [the most modern Lightbeam yet](https://addons.mozilla.org/en-US/firefox/addon/lightbeam/), and we hope it helps you too!

### Acknowledgements

Thanks to Paul Theriault, Jonathan Kingston, Luke Crouch, and Princiya Sequeira for reviewing this post.

## About
[
Bianca Danforth ](http://biancadanforth.com)

Bianca is a web developer at Mozilla writing browser extensions to test new ideas and features for Firefox. Prior to building web applications, she built stepper motors and science exhibits. She just likes building stuff!

## 4 comments

Rafael EbronOctober 12th, 2017 at 11:32Bianca DanforthOctober 12th, 2017 at 20:11Ed MoOctober 15th, 2017 at 22:41soulrebelOctober 29th, 2017 at 19:54