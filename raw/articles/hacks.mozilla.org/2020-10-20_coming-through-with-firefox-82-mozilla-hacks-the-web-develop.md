---
title: Coming through with Firefox 82 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/10/coming-through-with-firefox-82/
author: Chris Mills
published: '2020-10-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As October ushers in the tail-end of the year, we are pushing Firefox 82 out the door. This time around we finally enable support for the Media Session API, provide some new CSS pseudo-selector behaviours, close some security loopholes involving the `Window.name`

property, and provide inspection for server-sent events in our developer tools.

This blog post provides merely a set of highlights; for all the details, check out the following:

## Inspecting server-sent events

[Server-sent events](https://developer.mozilla.org/docs/Web/API/Server-sent_events) allow for an inversion of the traditional client-initiated web request model, with a server sending new data to a web page at any time by pushing messages. In this release we’ve added the ability to inspect server-sent events and their message contents using the [Network Monitor](https://developer.mozilla.org/docs/Tools/Network_Monitor).

You can go to the Network Monitor, select the file that is sending the server-sent events, and view the received messages in the *Response* tab on the right-hand panel.

![](../../assets/216f8a7d98fefb6b.png)


For more information, check out our [Inspecting server-sent events](https://developer.mozilla.org/docs/Tools/Network_Monitor/Inspecting_server-sent_events) guide.

## Web platform updates

Now let’s look at the web platform additions we’ve got in store in 82.

### Media Session API

The [Media Session API](https://developer.mozilla.org/docs/Web/API/Media_Session_API) enables two main sets of functionality:

- First of all, it provides a way to customize media notifications. It does this by providing metadata for display by the operating system for the media your web app is playing.
- Second, it provides event handlers that the browser can use to access platform media keys such as hardware keys found on keyboards, headsets, remote controls, and software keys found in notification areas and on lock screens of mobile devices. So you can seamlessly control web-provided media via your device, even when not looking at the web page.

The code below provides an overview of both of these in action:

```
if ('mediaSession' in navigator) {
navigator.mediaSession.metadata = new MediaMetadata({
title: 'Unforgettable',
artist: 'Nat King Cole',
album: 'The Ultimate Collection (Remastered)',
artwork: [
{ src: 'https://dummyimage.com/96x96', sizes: '96x96', type: 'image/png' },
{ src: 'https://dummyimage.com/128x128', sizes: '128x128', type: 'image/png' },
{ src: 'https://dummyimage.com/192x192', sizes: '192x192', type: 'image/png' },
{ src: 'https://dummyimage.com/256x256', sizes: '256x256', type: 'image/png' },
{ src: 'https://dummyimage.com/384x384', sizes: '384x384', type: 'image/png' },
{ src: 'https://dummyimage.com/512x512', sizes: '512x512', type: 'image/png' },
]
});
navigator.mediaSession.setActionHandler('play', function() { /* Code excerpted. */ });
navigator.mediaSession.setActionHandler('pause', function() { /* Code excerpted. */ });
navigator.mediaSession.setActionHandler('seekbackward', function() { /* Code excerpted. */ });
navigator.mediaSession.setActionHandler('seekforward', function() { /* Code excerpted. */ });
navigator.mediaSession.setActionHandler('previoustrack', function() { /* Code excerpted. */ });
navigator.mediaSession.setActionHandler('nexttrack', function() { /* Code excerpted. */ });
}
```


Let’s consider what this could look like to a web user — say they are playing music through a web app like Spotify or YouTube. With the first block of code above we can provide metadata for the currently playing track that can be displayed on a system notification, on a lock screen, etc.

The second block of code illustrates that we can set special action handlers, which work the same way as event handlers but fire when the equivalent action is performed at the OS-level. This could include for example when a keyboard play button is pressed, or a skip button is pressed on a mobile lock screen.

The aim is to allow users to know what’s playing and to control it, without needing to open the specific web page that launched it.

### What’s in a Window.name?

This [ Window.name](https://developer.mozilla.org/docs/Web/API/Window/name) property is used to get or set the name of the window’s current browsing context — this is used primarily for setting targets for hyperlinks and forms. Previously one issue was that, when a page from a different domain was loaded into the same tab, it could access any information stored in

`Window.name`

, which could create a security problem if that information was sensitive.To close this hole, Firefox 82 and other modern browsers will reset `Window.name`

to an empty string if a tab loads a page from a different domain, and restore the name if the original page is reloaded (e.g. by selecting the “back” button).

This could potentially surface some issues — historically `Window.name`

has also been used in some frameworks for providing cross-domain messaging (e.g. [ SessionVars](http://www.thomasfrank.se/sessionvars.html) and Dojo’s

[) as a more secure alternative to JSONP. This is not the intended purpose of](https://www.sitepen.com/blog/2008/07/22/windowname-transport/)

`dojox.io.windowName`

`Window.name`

, however, and there are safer/better ways of sharing information between windows, such as [.](https://developer.mozilla.org/docs/Web/API/Window/postMessage)

`Window.postMessage()`

### CSS highlights

We’ve got a couple of interesting CSS additions in Firefox 82.

To start with, we’ve introduced the standard [ ::file-selector-button](https://developer.mozilla.org/docs/Web/CSS/::file-selector-button) pseudo-element, which allows you to select and style the file selection button inside

[elements.](https://developer.mozilla.org/docs/Web/HTML/Element/input/file)

`<input type=”file”>`

So something like this is now possible:

```
input[type=file]::file-selector-button {
border: 2px solid #6c5ce7;
padding: .2em .4em;
border-radius: .2em;
background-color: #a29bfe;
transition: 1s;
}
input[type=file]::file-selector-button:hover {
background-color: #81ecec;
border: 2px solid #00cec9;
}
```


Note that this was previously handled by the proprietary `::-webkit-file-upload-button`

pseudo, but all browsers should hopefully be following suit soon enough.

We also wanted to mention that the `:is()`

and `:where()`

pseudo-classes have been updated so that their error handling is more forgiving — a single invalid selector in the provided list of selectors will no longer make the whole rule invalid. It will just be ignored, and the rule will apply to all the valid selectors present.

## WebExtensions

Starting with Firefox 82, language packs will be updated in tandem with Firefox updates. Users with an active language pack will no longer have to deal with the hassle of defaulting back to English while the language pack update is pending delivery.

Take a look at the [Add-ons Blog](https://blog.mozilla.org/addons/2020/10/07/extensions-in-firefox-82/) for more updates to the WebExtensions API in Firefox 82!

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 2 comments

DziadOctober 20th, 2020 at 09:03Christopher DawkinsOctober 21st, 2020 at 03:40