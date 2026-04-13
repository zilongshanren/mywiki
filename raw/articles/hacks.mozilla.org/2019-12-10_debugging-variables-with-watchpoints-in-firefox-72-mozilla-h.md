---
title: Debugging Variables With Watchpoints in Firefox 72 – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2019/12/debugging-variables-with-watchpoints-in-firefox-72/
author: Miriam Budayr
published: '2019-12-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The Firefox Devtools team, along with our community of code contributors, have been working hard to pack Firefox 72 full of improvements. This post introduces the *watchpoints* feature that’s available right now in [Firefox Developer Edition](https://www.mozilla.org/firefox/developer/?utm_source=hacks&utm_medium=watchpoints)! Keep reading to get up to speed on watchpoints and how to use them.

## What are watchpoints and why are they useful?

Have you ever wanted to know where properties on objects are read or set in your code, without having to manually add breakpoints or log statements? Watchpoints are a type of breakpoint that provide an answer to that question.

If you add a watchpoint to a property on an object, every time the property is used, the debugger will pause at that location. There are two types of watchpoints: *get* and *set*. The *get* watchpoint pauses whenever a property is read, and the *set* watchpoint pauses whenever a property value changes.

The watchpoint feature is particularly useful when you are debugging large, complex codebases. In this type of environment, it may not be straightforward to predict where a property is being set/read.

Watchpoints are also available in Firefox’s Visual Studio Code Extension where they’re referred to as “data breakpoints.” You can download the [Debugger for Firefox extension](https://marketplace.visualstudio.com/items?itemName=firefox-devtools.vscode-firefox-debug) from the VSCode Marketplace. Then, read more about how to use VSCode’s data breakpoints in [VSCode’s debugging documentation](https://code.visualstudio.com/docs/editor/debugging#_data-breakpoints).

## Getting Started

To set a watchpoint, pause the debugger, find a property in the Debugger’s ‘Scopes’ pane, and right-click it to view the menu. Once the menu is displayed, you can choose to add a *set* or *get* watchpoint. Here we want to debug `obj.a`

, so we will add a *set* watchpoint on it.

Voila, the *set* watchpoint has been added, indicated by the blue watchpoint icon to the right of the property. Here comes the easy part in your code — where you let the debugger inform you when properties are set. Just hit *resume* (or F8), and we’re off.

The debugger has paused on line 7 where `obj.a`

is set. Also notice the yellow pause message panel in the upper right corner which tells us that we are breaking because of a *set* watchpoint.

Deleting a watchpoint is like deleting a regular breakpoint—just click the blue watchpoint icon.

And that’s it! This feature is simple to use, but it’s powerful to have in your debugging toolbox.

## Implementation

When you add a watchpoint to a property, *getter* and *setter* functions are defined for the property using JavaScript’s native [ Object.defineProperty](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty) method. These getter/setter functions run every time your property is used, and they call a function that pauses the debugger. You can

[check out the server code](https://searchfox.org/mozilla-central/source/devtools/server/actors/object.js#118-200)for this feature.

When we built the implementation of watchpoints, we faced an interesting challenge. The team needed to be sure that our use of `Object.defineProperty`

would be transparent to the user. For this reason, we had to make sure that original values rather than getter/setter functions appeared in the debugger.

Some things to keep in mind:

-Watchpoints do not work for getters and setters.

-When a variable is [garbage-collected](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Memory_Management), it takes the watchpoint with it.

## What’s Next

We plan to support adding and viewing watchpoints from the console and in the many other places where DevTools lets you inspect objects. Also, we want to continue polishing this feature, and that’s where we’d love to have your help!

Give watchpoints a spin in [Firefox Developer Edition 72](https://www.mozilla.org/firefox/developer/?utm_source=hacks&utm_medium=watchpoints), and please send us feedback in one of these channels:

- File bug reports in
[Bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?format=guided#h=dupes%7CDevTools%7CGeneral). - Join us on the
[Firefox Devtools Slack](https://devtools-html-slack.herokuapp.com/)to share your input. - Discuss your ideas in Mozilla’s
[Developer](https://discourse.mozilla.org/c/devtools)Tools Discourse. - Tweet to us at
[@FirefoxDevTools](https://twitter.com/FirefoxDevTools)

## About
[
Miriam Budayr ](https://www.linkedin.com/in/miriam-budayr/)

Miriam is an open source developer for Mozilla Firefox where she contributes to the Firefox Debugger. Her background is in classical piano/composition, and she's interested in switching careers to programming.

## One comment

C RDecember 16th, 2019 at 16:31