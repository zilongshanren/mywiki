---
title: Firebug & DevTools Integration – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/10/firebug-devtools-integration/
author: Jan Honza Odvarko
published: '2015-10-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

You might have already heard about our effort to unify native Firefox Developer tools (DevTools) and Firebug. We’ve been working hard to port all favorite Firebug features into native DevTools, make them multi-process compatible, and available for remote debugging (i.e., [e10s](https://wiki.mozilla.org/Electrolysis) compatible). We’ve been also working hard to make the transition path from Firebug to DevTools as simple and smooth as possible. Yes, as we’ve mentioned before, we’re focused on developing one great tool for developers!

So, let’s see how it looks now.

The main goal of next-generation Firebug is to help users feel at home when working with native DevTools. This is where Firebug 3 (aka *Firebug.next*) comes in. Firebug 3 is not another developer tool, it is rather a thin layer built on top of DevTools, providing a new theme that makes DevTools look like Firebug. There are also a few additional features, that we’ll port into DevTools step by step.

*If you are missing any features (e.g. some of those you’ve been using in previous versions of Firebug), you should expect them to be part of DevTools in the future.*

## Firebug 3

Take a look at the screenshot below showing what DevTools look like if you [install Firebug 3](https://github.com/firebug/firebug.next/releases) (first beta). Does this look familiar?

![Firebug 3 (aka Firebug.next)](../../assets/2b172525e93c25a9.png)


*Firebug 3 (aka Firebug.next) isn’t distributed through AMO yet, so you might need to set the xpinstall.signatures.required preference (through about:config) to false.*

It’s the Firebug theme ported into DevTools to bring some UI and layout advantages. There is also the well-known Firebug start button in the Firefox toolbar, which represents the entry point to the developer toolbox.

See, the **Firebug Theme** option is currently active.

![Firebug Start Button](../../assets/871db7bcc4d0edda.png)


The process for entering your handy tools is exactly the same: you can either press the start button or the F12 key.

You might be a fan of the DOM panel used to inspect the document object model of the page you’re on. It isn’t supported natively (yet) and so, Firebug offers it to you.

![DOM panel](../../assets/2de62c27743e6382.png)


XHR previews in the Console panel (requested many times) are also supported.

![XHR Previews](../../assets/d695ce0c49901943.png)


Some of the most popular extensions have been re-implemented on top of DevTools. Not only does this keep popular features alive, these implementations also provide great examples of how you can make new extensions directly for DevTools. Firebug isn’t required to run these extensions.

*If you are an extension developer you might be interested in some examples and links to other resources helping to understand how to extend DevTools.*

Let’s see what extensions are available.

## FireQuery extension

[FireQuery](https://github.com/firebug/firequery/wiki) is a Firefox plugin for jQuery development built on top of DevTools in Firefox. [Firebug 3](https://github.com/firebug/firebug.next) isn’t required, but some of the screenshots below show DevTools with the Firebug theme activated (the other themes, Light and Dark, are also supported).

Elements with [jQuery data](http://api.jquery.com/data/) associated display a little envelope icon in the Console panel. You can inspect it by clicking on the icon. There is also a **jQuerify** button in the Console panel toolbar and you can use it to load jQuery into the current page.

![FireQuery extension](../../assets/94670ec3fb606131.png)


The Inspector panel also displays the envelope icon for elements with jQuery data. Clicking the icon opens a popup with details.

![FireQuery Inspector panel](../../assets/5cc258a38a2f5d6a.png)


- See the
[FireQuery home page](https://github.com/firebug/firequery/wiki). - Download the add-on from
[AMO](https://addons.mozilla.org/cs/firefox/addon/firequery/). - Try it out with this online
[test page](http://softwareishard.com/firequery/test1/).

## PixelPerfect extension

[Pixel Perfect](https://github.com/firebug/pixel-perfect/wiki) is a Firefox extension that allows web developers and designers to easily overlay a web composition with semi-transparent layers (images). These layers can then be used for per pixel comparison between the page and a layer.

There is a Pixel Perfect start button allowing quick access to this feature.

![PixelPerfect Start Button](../../assets/914aa2cc8fd28730.png)


And here is the final Pixel Perfect UI that you can open by clicking on the button above.

![PixelPerfect UI](../../assets/eb0bb613ff19a8e5.png)


- See the
[Pixel Perfect home page](https://github.com/firebug/pixel-perfect/wiki). - Download from
[AMO](https://addons.mozilla.org/en-US/firefox/addon/pixel-perfect/).

## HAR export

Support for exporting [HAR](https://en.wikipedia.org/wiki/.har) (the HTTP Archive format) from the Network panel is now a built-in feature and you don’t need an extension for it. All you need to do is select the Network panel (reload the page if necessary) and use two context menu actions:

- Copy All As HAR: copy collected data into the clipboard.
- Save All As HAR: save collected data into a file.

Exporting data from the Network panel is often automated (e.g. when testing web applications using Selenium). If you want to create a HAR file automatically for every loaded page you need to set the following preference (use about:config) to true:

`devtools.netmonitor.har.enableAutoExportToFile`


Some automated systems need more flexibility than just creating a HAR file after every page load. Sometimes you need to send data to a remote server, collect and export HAR between two specific user actions, etc. That’s why we’ve introduced a simple [HARExportTrigger](https://github.com/firebug/har-export-trigger) extension that improves automation by exporting HAR API into the page content. This allows you to use small script to trigger HAR at any time.

Here is an example script that gets HAR data from the Network panel:

```
var options = {
token: "test",
getData: true,
};
HAR.triggerExport(options).then(result => {
console.log(result.data);
});
```


- See
[HAR Export Trigger home page](http://www.softwareishard.com/blog/har-export-trigger/) - Download the add-on from
[AMO](https://addons.mozilla.org/en-US/firefox/addon/har-export-trigger/)

## Using `console.*`

APIs on the server

The Firebug community has implemented many extensions that allow developers to use `console.*`

APIs on the (HTTP) server side, so you can see your backend logs right in the browser. This feature is now natively supported in Firefox and you don’t need to install an additional extension.

All you need to do is enable logs coming from the server inside the Console panel.

![Server side logging](../../assets/c591549dcbe2d57d.png)


This feature supports an existing protocol (used in [Chrome Logger](https://craig.is/writing/chrome-logger)) that sends logs through HTTP headers to the client. Logs are consequently displayed in the Console panel as if they had been generated by JavaScript on the page. There are many server-side libraries that provide the appropriate server side API in various languages (NodeJS, Ruby, Python, PHP, .NET, Java, etc.)

Here is an [example](https://github.com/yannickcr/node-chromelogger) of server side logging:

```
var chromelogger = require('chromelogger');
var http = require('http');
var server = http.createServer();
server.on('request', chromelogger.middleware);
server.on('request', function(req, res) {
res.chrome.log('Hello from Node.js %s', process.version);
res.end();
});
server.listen(7357);
```


And here is what the server-side log looks like in the Console panel:

![Server log](../../assets/8c54e22fe68112ce.png)


## Final words

As I mentioned at the beginning of the article, we are trying to unify native Firefox Developer tools (DevTools) and Firebug since we believe that this is an effective strategy for delivering great tools for web developers. There is more yet to come, but this post should give you an overview of our plan and where we are heading. Stay tuned!

Please post feedback in the [Firebug group](https://groups.google.com/forum/#!topic/firebug/xrImQJdSi3I), thanks.

Jan ‘Honza’ Odvarko

## About
[
Jan Honza Odvarko ](http://www.softwareishard.com/)

Honza is working on Firefox Developer Tools

## 7 comments

ThomasOctober 28th, 2015 at 13:28Jan Honza OdvarkoOctober 28th, 2015 at 23:52Jeffrey JoseOctober 28th, 2015 at 21:43Sebastian ZartnerOctober 29th, 2015 at 04:51xpeteOctober 29th, 2015 at 18:12jeffNovember 2nd, 2015 at 12:12Jan Honza OdvarkoNovember 3rd, 2015 at 08:56