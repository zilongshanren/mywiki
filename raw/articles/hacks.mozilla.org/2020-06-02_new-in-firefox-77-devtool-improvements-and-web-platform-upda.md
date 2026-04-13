---
title: 'New in Firefox 77: DevTool improvements and web platform updates – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2020/06/new-in-firefox-77-devtool-improvements-and-web-platform-updates/
author: Florian Scholz
published: '2020-06-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Note: This post is also available in: 简体中文 (Chinese (Simplified)), 繁體中文 (Chinese (Traditional)), and Español (Spanish).*

A new stable Firefox version is rolling out. Version 77 comes with a few new features for web developers.

This blog post provides merely a set of highlights; for all the details, check out the following:

## Developer tools improvements

Let’s start by reviewing the most interesting Developer Tools improvements and additions for 77. If you like to see more of the work in progress to give feedback, get [Firefox DevEdition](https://www.mozilla.org/firefox/developer/) for early access.

### Faster, leaner JavaScript debugging

Large web apps can provide a challenge for DevTools as bundling, live reloading, and dependencies need to be handled fast and correctly. With 77, Firefox’s Debugger learned a few more tricks, so you can focus on debugging.

After we improved debugging performance over many releases, we did run out of actionable, high-impact bugs. So to find the last remaining bottlenecks, we have been actively reaching out to our community. Thanks to many detailed reports we received, we were able to land performance improvements that not only speed up pausing and stepping but also cut down on memory usage over time.

#### JavaScript & CSS Source Maps that just work

Source maps were part of this outreach and saw their own share of performance boosts. Some cases of inline source maps improved 10x in load time. More importantly though, we improved reliability for many more source map configurations. We were able to tweak the fallbacks for parsing and mapping, thanks to your reports about specific cases of slightly-incorrect generated source maps. Overall, you should now see projects that just work, that previously failed to load your original CSS and JavaScript/TypeScript/etc code.

### Step JavaScript in the selected stack frame

Stepping is a big part of debugging but not intuitive. You can easily lose your way and overstep when moving in and out of functions, and between libraries and your own code.

The debugger will now respect the currently selected stack when [stepping](https://developer.mozilla.org/en-US/docs/Tools/Debugger/How_to/Step_through_code). This is useful when you’ve stepped into a function call or paused in a library method further down in the stack. Just select the right function in the [Call Stack](https://developer.mozilla.org/en-US/docs/Tools/Debugger/UI_Tour#Call_stack) to jump to its currently paused line and continue stepping from there.

We hope that this makes stepping through code execution more intuitive and less likely for you to miss an important line.

### Overflow settings for Network and Debugger

To make for a leaner toolbar, Network and Debugger follow Console’s example in combining existing and new checkboxes into a new settings menu. This puts powerful options like *“Disable JavaScript”* right at your fingertips and gives room for more powerful options in the future.

### Pause on property read & write

Understanding state changes is a problem that is often investigated by console logging or debugging. [Watchpoints](https://wiki.developer.mozilla.org/en-US/docs/Tools/Debugger/How_to/Use_watchpoints), which landed in Firefox 72, can pause execution while a script reads a property or writes it. Right-click a property in the Scopes panel when paused to attach them.

Contributor [Janelle deMent](https://bugzilla.mozilla.org/user_profile?user_id=637866) made watchpoints easier to use with a new option that combines get/set, so any script reference will trigger a pause.

### Improved Network data preview

Step by step over each release, the Network details panels have been rearchitected. The old interface had event handling bugs that made selecting and copying text too flaky. While we were at it, we also improved performance for larger data entries.

This is part of a larger interface cleanup in the Network panel, which we have been surveying our community about [via @FirefoxDevTools Twitter](https://twitter.com/FirefoxDevTools) and [Mozilla’s Matrix community](https://chat.mozilla.org/#/room/#devtools:mozilla.org). Join us there to have your voice heard. More parts of the Network-panel sidebar redesign are also available in [Firefox DevEdition](https://www.mozilla.org/firefox/developer/) for early access.

## Web platform updates

Firefox 77 supports a couple of new web platform features.

`String#replaceAll`


Firefox 67 introduced [ String#matchAll](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String/matchAll), a more convenient way to iterate over

[regex](https://en.wikipedia.org/wiki/Regular_expression)result matches. In Firefox 77 we’re adding more comfort:

[helps with replacing all occurrences of a string – an operation that’s probably one of those things you have searched for a thousand times in the past already (thanks StackOverflow for being so helpful!).](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String/replaceAll)

`String#replaceAll`

Previously, when trying to replace all cats with dogs, you had to use a global regular expression

`.replace(/cats/g, 'dogs');`


Or, you could use [split](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String/split) and [join](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/join):

`.split('cats').join('dogs');`


Now, thanks to [String#replaceAll](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String/replaceAll), this becomes much more readable:

`.replaceAll('cats', 'dogs');`


### IndexedDB cursor requests

Firefox 77 exposes the request that an [IDBCursor](https://developer.mozilla.org/docs/Web/API/IDBCursor) originated from as an [attribute on that cursor](https://developer.mozilla.org/docs/Web/API/IDBCursor/request). This is a nice improvement that makes it easier to write things like wrapper functions that “upgrade” database features. Previously, to do such an upgrade on a cursor you’d have to pass in the cursor object and the request object that it originated from, as the former is reliant on the latter. With this change, you now only need to pass in the cursor object, as the request is available on the cursor.

## Extensions in Firefox 77: Fewer permission requests and more

Since Firefox 57, users see the permissions an extension wants to access during installation or when any new permissions are added during an update. The frequency of these prompts can be overwhelming, and failure to accept a new permission request during an extension’s update can leave users stranded on an old version. We’re making it easier for extension developers to avoid triggering as many prompts by making more permissions available as [optional permissions](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/optional_permissions). Optional permissions don’t trigger a permission request upon installation or when they are added to an extension update, and can also be [requested at runtime](https://extensionworkshop.com/documentation/develop/request-the-right-permissions/?utm_source=blog.mozilla.org&utm_medium=blog&utm_campaign=hacks-fx-77#request-permissions-at-runtime) so users see what permissions are being requested in context.

Visit the [Add-ons Blog](https://blog.mozilla.org/addons/) to see more updates for extensions in Firefox 77!

## Summary

These are the highligts of Firefox 77! Check out the new features and have fun playing! As always, feel free to give feedback and ask questions in the comments.

## About
[
Florian Scholz ](https://developer.mozilla.org)

Florian is the Content Lead for MDN Web Docs, writes about Web platform technologies and researches browser compatibility data. He lives in Bremen, Germany.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.

## 4 comments

Michael DougallJune 2nd, 2020 at 16:10Harald Kirschner (digitarald)June 9th, 2020 at 10:00maxidoine allianceJune 11th, 2020 at 11:25Doug DyerJune 11th, 2020 at 13:54