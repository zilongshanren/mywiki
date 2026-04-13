---
title: Handling click-to-activate plugins using JavaScript – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2013/11/handling-click-to-activate-plugins-using-javascript/
author: Chris Mills
published: '2013-11-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

From Firefox 26 onwards — and in the case of insecure Flash/Java in older Firefox versions — [most plugins will not be automatically activated](https://blog.mozilla.org/futurereleases/2013/09/24/plugin-activation-in-firefox/). We therefore can no longer plugins starting immediately after they have been inserted into the page. This article covers JavaScript techniques we can employ to handle plugins, making it less likely that affected sites will break.

## Using a script to determine if a plugin is installed

To detect if a plugin is actually installed, we can query [ navigator.mimeTypes](https://developer.mozilla.org/docs/Web/API/NavigatorPlugins.mimeTypes) for the plugin MIME type we intend to use, to differentiate between plugins that are not installed and those that are click-to-activate. For example:

```
function isJavaAvailable() {
return 'application/x-java-applet' in navigator.mimeTypes;
}
```

Note: Do not iterate through `<a href="https://developer.mozilla.org/docs/Web/API/NavigatorPlugins.mimeTypes">navigator.mimeTypes</a>`

or `<a href="https://developer.mozilla.org/docs/Web/API/NavigatorPlugins.plugins">navigator.plugins</a>`

, as enumeration may well be removed as a privacy measure in a future version of Firefox.

## Using a script callback to determine when a plugin is activated

The next thing to be careful of is scripting plugins immediately after instances are created on the page, to avoid breakage due to the plugin not being properly loaded. The plugin should make a call into JavaScript after it is created, using `<a href="https://developer.mozilla.org/docs/Gecko_Plugin_API_Reference/Scripting_plugins">NPRuntime</a>`

scripting:

```
function pluginCreated() {
document.getElementById('myPlugin').callPluginMethod();
}
```

```
```

Note that the “callback” parameter (or something equivalent) must be implemented by your plugin. This can be done in Flash using the `flash.external.ExternalInterface`

API, or in Java using the `netscape.javascript`

package.

## Using properties on the plugin to determine when it activated

When using a plugin that doesn’t allow us to specify callbacks and we can’t modify it, an alternative technique is to test for properties that the plugin should have, using code constructs like so:

```
```Waiting for the plugin to activate!


```
window.onload = function () {
if (document.getElementById('myPlugin').myProperty !== undefined) {
document.getElementById('myNotification').style.display = 'none';
document.getElementById('myPlugin').callPluginMethod();
} else {
console.log("Plugin not activated yet.");
setTimeout(checkPlugin, 500);
}
}
```

## Making plugins visible on the page

When a site wants the user to enable a plugin, the primary indicator is that the plugin is visible on the page, for example:

![Screenshot of the silverlight plugin activation on the Netflix website.](https://mdn.mozillademos.org/files/6305/silverlight-CtA.png)


If a page creates a plugin that is very small or completely hidden, the only visual indication to the user is the small icon in the Firefox location bar. Even if the plugin element will eventually be hidden, pages should create the plugin element visible on the page, and then resize or hide it only after the user has activated the plugin. This can be done in a similar fashion to the callback technique we showed above:

```
function pluginCreated() {
// We don't need to see the plugin, so hide it by resizing
var plugin = document.getElementById('myPlugin');
plugin.height = 0;
plugin.width = 0;
plugin.callPluginMethod();
}
```

```
```

**Note:** For more basic information on how plugins operate in Firefox, read [Why do I have to click to activate plugins?](https://support.mozilla.org/en-US/kb/why-do-i-have-click-activate-plugins) on support.mozilla.org.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.