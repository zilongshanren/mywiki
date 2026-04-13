---
title: Using the new theming API in Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/12/using-the-new-theming-api-in-firefox/
author: Tim Nguyen
published: '2017-12-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

From powerful extensions like [Stratiform](https://lifehacker.com/5790059/stratiform-makes-tweaking-firefoxs-looks-really-simple) or [FT Deep Dark](http://stefrosselli.com/en/themes) to simple [lightweight themes](https://addons.mozilla.org/en-US/firefox/themes/), theming has been quite popular within Firefox. Now that Firefox Quantum (57) has launched with many performance improvements and a sparkling new interface, we want to bridge the gap with a new theming API that allows you to go beyond basic lightweight themes.

![](../../assets/f05933c0f08704a8.gif)

*Demo by John Gruen*

## What can you theme?

Before the launch of Quantum, lightweight themes had a limited set of properties that could be themed: you could only add a header image and set the frame text color and background color. The new theming API introduces some new properties. The full list [can be found on MDN](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/theme). A basic `Theme`

object looks like this:

```
{
"images": {
"theme_frame": ""
},
"colors": {
"frame": "tomato",
"tab_background_text": "white",
"toolbar": "#444",
"toolbar_text": "lightgray",
"toolbar_field": "black",
"toolbar_field_text": "white"
}
}
```


Here’s how the above theme is displayed:

Notice how the `images.theme_frame`

property is set to an empty string. This is because it is one of three mandatory properties: `images.theme_frame`

, `colors.frame`

and `colors.tab_background_text`

. (**Edit:** those properties are now optional in recent versions)

Finally, another improvement to lightweight themes is support for multiple header images, using the `images.additional_backgrounds`

field which takes an array of image paths. The alignments and tilings of these images is achieved using `properties.additional_backgrounds_alignment`

and `properties.additional_backgrounds_tiling`

, which take in an array of `background-position`

and `background-repeat`

values respectively. You can check out the MDN page for [an example](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/theme#Examples). You can use multiple backgrounds in order to display curtains on both sides of the browser UI, or as a way to add several thematic indicators (sports/weather/private browsing) in the UI.

Let’s say you would like to introduce a night mode to your theme. Dynamic themes allow you to do this. They have the full power of a normal browser extension. To use dynamic theming, you need to add the `theme`

[permission](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/permissions) to your manifest.

The `<a href="https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/theme/update">browser.theme.update()</a>`

method is at the core of this type of theming. It takes in a `Theme`

object as parameter. The method can be called anywhere in your background scripts.

For this example, let’s create an extension that switches the theme depending on whether it’s night or day. The first step is to create a function in your background script that switches your theme to the day theme or the night theme:

```
var currentTheme = '';
const themes = {
'day': {
images: {
theme_frame: 'sun.jpg',
},
colors: {
frame: '#CF723F',
tab_background_text: '#111',
}
},
'night': {
images: {
theme_frame: 'moon.jpg',
},
colors: {
frame: '#000',
tab_background_text: '#fff',
}
}
};
function setTheme(theme) {
if (currentTheme === theme) {
// No point in changing the theme if it has already been set.
return;
}
currentTheme = theme;
browser.theme.update(themes[theme]);
}
```


The above code defines two themes: the day theme and the night theme, the `setTheme`

function then uses `browser.theme.update()`

to set the theme.

The next step is now to use this `setTheme`

function and periodically check whether the extension should switch themes. You can do this using the alarms API. The code below checks periodically and sets the theme accordingly:

```
function checkTime() {
let date = new Date();
let hours = date.getHours();
// Will set the sun theme between 8am and 8pm.
if (hours > 8 && hours < 20) {
setTheme('day');
} else {
setTheme('night');
}
}
// On start up, check the time to see what theme to show.
checkTime();
// Set up an alarm to check this regularly.
browser.alarms.onAlarm.addListener(checkTime);
browser.alarms.create('checkTime', {periodInMinutes: 5});
```


That’s it for this example! The full example is available [on the webextension-examples github repository](https://github.com/mdn/webextensions-examples/tree/master/dynamic-theme).

Another method that’s not covered by the example is `<a href="https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/theme/reset">browser.theme.reset()</a>`

. This method simply resets the theme to the default browser theme.

## Per-window themes

The dynamic theming API is pretty powerful, but what if you need to apply a different theme for private windows or inactive windows? From Firefox 57 onwards, it is possible to specify a `windowId`

parameter to both `<a href="https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/theme/update">browser.theme.update()</a>`

and `<a href="https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/theme/reset">browser.theme.reset()</a>`

. The `windowId`

is the same ID returned by the [windows API](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/windows).

Let’s make a simple example that adds a dark theme to private windows and keeps other windows set to the default theme:

We start by defining the `themeWindow`

function:

```
function themeWindow(window) {
// Check if the window is in private browsing
if (window.incognito) {
browser.theme.update(window.id, {
colors: {
frame: "black",
tab_background_text: "white",
toolbar: "#333",
toolbar_text: "white"
}
});
}
// Reset to the default theme otherwise
else {
browser.theme.reset(window.id);
}
}
```


Once that’s done, we can wire this up with the [windows API](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/windows):

```
browser.windows.onCreated.addListener(themeWindow);
// Theme all currently open windows
browser.windows.getAll().then(wins => wins.forEach(themeWindow));
```


Pretty straightforward right? The full example can be found [here](https://github.com/mdn/webextensions-examples/tree/master/private-browsing-theme). Here is how the example looks:

Another add-on that makes use of these capabilities is the ![](../../assets/8400e560a245e596.png)


[Containers theme](https://addons.mozilla.org/en-US/firefox/addon/containers-theme/)by Jonathan Kingston, which sets the theme of each window to the container of its selected tab. The source code for this add-on can be found

[here](https://github.com/jonathanKingston/containers-theme).

The [VivaldiFox add-on](https://addons.mozilla.org/en-US/firefox/addon/vivaldifox/) also makes use of this capability to display different website themes across different windows:

From Firefox 58 onward, you can now obtain information about the current theme and watch for theme updates. Here’s why this matters:

This allows add-ons to integrate their user interface seamlessly with the user’s currently installed theme. An example of this would be matching your sidebar tabs colors with the colors from your current theme.

To do so, Firefox 58 provides [two new APIs](https://bugzilla.mozilla.org/show_bug.cgi?id=1349944): `<a href="https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/theme/getCurrent">browser.theme.getCurrent()</a>`

and `<a href="https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/theme/onUpdated">browser.theme.onUpdated</a>`

.

Here is a simple example that applies some of the current theme properties to the style of a [sidebar_action](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/sidebar_action):

```
function setSidebarStyle(theme) {
const myElement = document.getElementById("myElement");
// colors.frame and colors.accentcolor are aliases
if (theme.colors && (theme.colors.accentcolor || theme.colors.frame)) {
document.body.style.backgroundColor =
theme.colors.accentcolor || theme.colors.frame;
} else {
document.body.style.backgroundColor = "white";
}
if (theme.colors && theme.colors.toolbar) {
myElement.style.backgroundColor = theme.colors.toolbar;
} else {
myElement.style.backgroundColor = "#ebebeb";
}
if (theme.colors && theme.colors.toolbar_text) {
myElement.style.color = theme.colors.toolbar_text;
} else {
myElement.style.color = "black";
}
}
// Set the element style when the extension page loads
browser.theme.getCurrent().then(setSidebarStyle);
// Watch for theme updates
browser.theme.onUpdated.addListener(async ({ theme, windowId }) => {
const sidebarWindow = await browser.windows.getCurrent();
/*
Only update theme if it applies to the window the sidebar is in.
If a windowId is passed during an update, it means that the theme is applied to that specific window.
Otherwise, the theme is applied globally to all windows.
*/
if (!windowId || windowId == sidebarWindow.id) {
setSidebarStyle(theme);
}
});
```


The full example can be found [on Github](https://github.com/mdn/webextensions-examples/tree/master/theme-integrated-sidebar). As you can see in the screenshot below, the sidebar uses colors from the currently applied browser theme:

Another example is the ![](../../assets/e72b0bff5f650368.png)


[Tree Style Tab add-on](https://addons.mozilla.org/en-US/firefox/addon/tree-style-tab/)which makes

[use of these APIs](https://github.com/piroor/treestyletab/commit/c9f06a238cf557e59000a2290f99e27e0c93c326)to integrate its interface with the currently used theme. Here is a screencast of the add-on working together with VivaldiFox:

## What’s next?

There is more coming to this API! We plan to expand the set of supported properties and polish some rough edges around the way themes are applied. The tracking bug for the API [can be found on Bugzilla](https://bugzilla.mozilla.org/show_bug.cgi?id=themingapi).

In the meanwhile, we can’t wait to see what you will be able to do with the new theming API. Please let us know what improvements you would like to see.

Edit (July 21st 2019): Updated code samples to remove [deprecated theme properties](https://bugzilla.mozilla.org/show_bug.cgi?id=1472740)

## About Tim Nguyen

I work on web browsers.

## 17 comments

wDecember 4th, 2017 at 08:40CocorocoDecember 4th, 2017 at 09:17Tim NguyenDecember 4th, 2017 at 10:40CocorocoDecember 4th, 2017 at 11:01Christian KaindlDecember 5th, 2017 at 01:05MarcelDecember 4th, 2017 at 13:40WillDecember 4th, 2017 at 16:33Ken SaundersDecember 4th, 2017 at 13:52Tim NguyenDecember 4th, 2017 at 15:51Ken SaundersDecember 5th, 2017 at 14:47MaxDecember 5th, 2017 at 01:10GerdDecember 6th, 2017 at 00:46MauriDecember 5th, 2017 at 16:13Tim NguyenDecember 6th, 2017 at 00:52MattDecember 7th, 2017 at 11:43Tim NguyenDecember 7th, 2017 at 12:33StuDecember 10th, 2017 at 17:18