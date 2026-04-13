---
title: And now for … Firefox 84 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/12/and-now-for-firefox-84/
author: Chris Mills
published: '2020-12-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As December ushers in the final curtain for this rather eventful year, there is time left for one more Firefox version to be given its wings. Firefox 84 includes some interesting new features including tab order inspection, complex selector support in `:not()`

, the `PerformancePaintTiming`

API, and more!

This blog post provides merely a set of highlights; for all the details, check out the following:

## DevTools gets tab order inspection

The Firefox Developer Tools have gotten a rather nice addition to the [Accessibility Inspector](https://wiki.developer.mozilla.org/en-US/docs/Tools/Accessibility_inspector) this time around — A “Show Tabbing Order” checkbox. When checked, this toggles a visual overlay showing the tabbing order or table items on the current page. This provides a high-level overview of how the page will be navigated using the tab key, which may highlight problems more effectively than simply tabbing through the elements.

![a web page with multiple tabbable items showing the tab order for those items visuallly](../../assets/f0d4fa5f7902651e.png)


## Web platform additions

Firefox 84 brings some new Gecko platform additions, the highlights of which are listed below.

### Complex selector support in :not()

The [ :not()](https://wiki.developer.mozilla.org/en-US/docs/Web/CSS/:not) pseudo-class is rather useful, allowing you to apply styles to elements that don’t match one or more selectors. For example, the following applies a blue background to all elements that aren’t paragraphs:

```
:not(p) {
background-color: blue;
}
```


However, it was of limited use until recently as it didn’t allow any kind of complex selectors to be negated. Firefox 84 adds support for this, so now you can do things like this:

```
:not(option:checked) {
color: #999;
}
```


This would set a different text color on `<select>`

options that are not currently selected.

### PerformancePaintTiming

The [ PerformancePaintTiming](https://developer.mozilla.org/en-US/docs/Web/API/PerformancePaintTiming) interface of the Paint Timing API provides timing information about “paint” (also called “render”) operations during web page construction, which is incredibly useful for developers wishing to develop their own performance tooling.

For example:

```
function showPaintTimings() {
if (window.performance) {
let performance = window.performance;
let performanceEntries = performance.getEntriesByType('paint');
performanceEntries.forEach( (performanceEntry, i, entries) => {
console.log("The time to " + performanceEntry.name + " was " + performanceEntry.startTime + " milliseconds.");
});
} else {
console.log('Performance timing isn\'t supported.');
}
}
```


Would output something like this in supporting browsers:

The time to first-paint was 2785.915 milliseconds. The time to first-contentful-paint was 2787.460 milliseconds.

### AppCache removal

[AppCache](https://developer.mozilla.org/en-US/docs/Web/HTML/Using_the_application_cache) was an attempt to create a solution for caching web app assets offline so the site could continue to be used without network connectivity. It seemed to be a good idea because it was really simple to use and could solve this very common problem easily. However, it made many assumptions about what you were trying to do and then broke horribly when your app didn’t follow those assumptions exactly.

Browser vendors have been planning its removal for quite some time, and as of Firefox 84, we have finally gotten rid of it for good. For creating offline app solutions, you should use the [Service Worker API](https://wiki.developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) instead.

## WebExtensions

Starting with Firefox 84, users will be able to [manage optional permissions](https://support.mozilla.org/kb/manage-optional-permissions-extensions) for installed add-ons through the Add-ons Manager.

![web extensions permissions dialog showing that you cna turn optional permissions on an off via the UI](../../assets/bbcdc9a6b9d0ea11.png)


We recommend that extensions using optional permissions listen for [ browser.permissions.onAdded](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/permissions/onAdded) and

[API events. This ensures the extension is aware of the user granting or revoking optional permissions.](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/permissions/onRemoved)

`browser.permissions.onRemoved`

Additionally, extension developers can now [zoom extension panels, popups, and sidebars](https://bugzilla.mozilla.org/show_bug.cgi?id=1634556) using `Ctrl` + scroll wheel (`Cmd` + scroll wheel on macOS).

We’ve also fixed an issue where [search engine changes weren’t being reset](https://bugzilla.mozilla.org/show_bug.cgi?id=1643858) under certain circumstances when an add-on was uninstalled.

## WebRender comes to Linux and Android

In our [previous Firefox release](https://hacks.mozilla.org/2020/11/firefox-83-is-upon-us/) we added support for our[ WebRender](https://hacks.mozilla.org/2017/10/the-whole-web-at-maximum-fps-how-webrender-gets-rid-of-jank/) rendering architecture to a number of new Windows and macOS versions. This time around we are pleased to add a subset of Linux and Android devices. In particular, we’ve enabled WebRender on:

- Gnome-, X11-, and GLX-based Linux devices.
- Android Mali-G GPU series phones (which represent approximately 27% of the Fenix release population).

We’re getting steadily closer to our dream of a 60fps web for everyone.

## Localhost improvements

Last but not least, we’d like to draw your attention to the fact that we’ve made some significant improvements to the way Firefox handles localhost URLs in version 84. Firefox now ensures that localhost URLs — such as *http://localhost/* and *http://dev.localhost/* — refer to the local host’s loopback interface (e.g. [ http://127.0.0.1](http://127.0.0.1)).

As a result, resources loaded from localhost are now assumed to have been delivered securely (see [Secure contexts](https://wiki.developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts)), and also will not be treated as [mixed content](https://wiki.developer.mozilla.org/en-US/docs/Web/Security/Mixed_content). This has a number of implications for simplifying local testing of different web features, especially for example those requiring secure contexts (like service workers).

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 12 comments

Stephan SokolowDecember 15th, 2020 at 12:48TyDecember 15th, 2020 at 18:15EamonDecember 16th, 2020 at 02:45zakiusDecember 16th, 2020 at 00:54Klaster_1December 17th, 2020 at 03:40AlDecember 16th, 2020 at 05:06EugeneDecember 16th, 2020 at 08:15MarkDecember 18th, 2020 at 02:00SimonDecember 18th, 2020 at 06:30Konstantinos LiakosDecember 18th, 2020 at 09:23SimonDecember 19th, 2020 at 03:04DenisJanuary 4th, 2021 at 09:16