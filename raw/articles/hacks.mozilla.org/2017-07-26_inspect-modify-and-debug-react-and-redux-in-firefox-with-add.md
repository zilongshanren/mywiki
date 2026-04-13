---
title: Inspect, Modify, and Debug React and Redux in Firefox with Add-ons – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/07/debug-react-redux-firefox-add-ons/
author: Dustin Driver
published: '2017-07-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

React, along with Redux, is one of the fastest and most flexible UI frameworks on the web. It’s easy to write, easy to use and is great for teams. In fact, the Mozilla community uses React to build a lot of the Firefox DevTools UI and, famously, the Facebook UI is built with React. Despite its popularity, it’s still not easy to debug React in the browser. [React Developer Tools](https://addons.mozilla.org/en-US/firefox/addon/react-devtools/?src=search) by [Facebook](https://facebook.github.io/react/) and [Redux DevTools](https://addons.mozilla.org/en-US/firefox/addon/remotedev/) by [Zalmoxisus](https://github.com/zalmoxisus) however, let you inspect, modify, and debug your code right in the browser. And now they’re available for Firefox. These add-ons, and others like the [Vue add-on](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools) will make debugging popular JavaScript frameworks easier. When combined with Mozilla’s [Debugger.html tool](https://hacks.mozilla.org/2016/09/introducing-debugger-html/), all these stand-alone tools will turn your browser into a full-featured debugger.

**React**

Get the latest version of the React DevTool add-on [here](https://addons.mozilla.org/en-US/firefox/addon/react-devtools/). Once it’s installed, you’ll be able to examine React code on any site that uses it. When you visit a React-powered site, the add-on icon will appear to the right of the Firefox address bar:

Open your DevTools by hitting command-option-i (control-shift-i for Windows), clicking the button in the toolbar, or right-clicking on the page and selecting “inspect.” You’ll see the React panel alongside the basic DevTools panels. The main panel will now show you the React tree view:

The React tool works pretty much like every other DevTool. Use the arrow keys or hjkl keys to navigate the code, right-click components to examine them in the elements pane, show source, and so on. Expand or collapse items by clicking the arrows.

The side pane is a great place to store variables and see updates to the code.

There’s also an awesome search bar.

Inspect a React element on a page using the regular inspector, then switch to the React tab. The element will automatically be selected in the React tree.

You can also right-click an element and choose “Find the DOM node” to, well, find the DOM node of any element.

**Redux**

React and Redux go together like avocado and toast. Redux creates a predictable state container for your React library that lets it run reliably on virtually any system. It also lets you “time travel” to previous versions of your states. [The Redux devtool for Firefox](https://addons.mozilla.org/en-US/firefox/addon/remotedev/) lets you inspect Redux actions and payloads, cancel actions, log action reducer errors, and automatically re-evaluate staged actions when you change reducer code.

The Redux devtool has extensive docs [on its GitHub repository](https://github.com/zalmoxisus/redux-devtools-extension), including [arguments](https://github.com/zalmoxisus/redux-devtools-extension/blob/master/docs/API/Arguments.md), [methods](https://github.com/zalmoxisus/redux-devtools-extension/blob/master/docs/API/Methods.md), and even a tutorial on how to [create a Redux store for debugging](https://github.com/zalmoxisus/redux-devtools-extension/blob/master/docs/API/Methods.md). Check them out.

With Firefox [Add-ons](https://addons.mozilla.org/en-US/firefox/), you can have a complete React/Redux debugging toolset right in your browser.

[Download Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) and then check out all the add-ons available at [addons.mozilla.org](https://addons.mozilla.org).

## About Dustin Driver

Journalist, tech writer, and video producer helping Mozilla keep the Web open and accessible for everyone.