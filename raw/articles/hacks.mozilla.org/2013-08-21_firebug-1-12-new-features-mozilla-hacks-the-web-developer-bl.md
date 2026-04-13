---
title: Firebug 1.12 New Features – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/08/firebug-1-12-new-features/
author: Jan Honza Odvarko
published: '2013-08-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firebug team released fresh new [Firebug 1.12](http://blog.getfirebug.com/2013/08/21/firebug-1-12-0/) and here is a list of some new features we have implemented in this version.

![Firebug](../../assets/e7f20c7022579428.png)


**Firebug 1.12**is compatible with**Firefox 23 – 26**

*Firebug is an open source project maintained by developers from around the world and I can’t miss this opportunity to introduce all members who contributed to Firebug 1.12*

|
|

## New Features

### Copy CSS Properties

Copying CSS properties into the clipboard has never been easier. It is now possible to copy individual CSS properties or rules or entire styles into the clipboard. Just right click on the part you want to copy. See detailed [description](https://getfirebug.com/wiki/index.php/Style_Side_Panel#Context_Menu) of this feature.

![Copy CSS Properties copy-css](../../assets/6af7ad0d4fbb6d45.png)


### New Net Panel Filters

The old Flash filter has been renamed to Plugins and covers Flash as well as Silverlight HTTP requests. There is also a new filter labeled Fonts that is used to see HTTP requests for custom fonts only (font/ttf or font/woff mime-types).

![net-panel-filters](../../assets/0251e15b370f2e9a.png)


*Use filter button tooltip to see detailed info about filtered files.*

### Filter for DOM Events Log

This feature allows to filter DOM event logging that is set for specific element. The next screenshot shows related user interface. There is a new submenu that allows to pick what events should be logged for selected element.

![dom-events-filter](../../assets/c4f9834919cc83f3.png)


You can also [help us improve](http://www.softwareishard.com/blog/firebug/how-to-properly-filter-dom-event-logs/) the UI/UX of this feature.

### Autocompletion Popup Improved

Autocompletion popup window that is available on Firebug Command Line (within the Console panel) has improved its design and it also offers built-in command line API.

![auto-completion-popup](../../assets/25cfd46cfebad4c2.png)


*Note that the bottom section of the popup window offers Firebug Command Line API.*

### Use in Command Line

This feature allows referring various page objects (HTML elements, JS objects, network requests, cookies, etc.) from the command line using new $p variable. The $p variable can also be used within command line expressions.

![use-in-command-line](../../assets/d1190c5424dd89fb.png)


See [detailed description](http://www.softwareishard.com/blog/firebug/new-firebug-feature-use-in-command-line/) of this feature.

### Group Console Messages

Console messages are grouped now in case the messages appear multiple times consecutively. This feature can dramatically decrease number of logs and make the entire logging easier!

![group-console-messages](../../assets/0692b5cfc688ab8d.png)


### Better Infotip for HTTP Request Timings

The tooltip for individual HTTP requests displayed in the Net panel has been improved. It displays all phases of the current request as a little waterfall graph. It’s now a lot easier to understand the timing.

![net-panel-timings](../../assets/42e084069f47e41f.png)


### Multiple Filters for Console & Net Panel

The Console and Net panels support selection of multiple filters at the same time. Just hold down Ctrl key when clicking the filter buttons. This allows to see e.g. only Errors and Warnings in the Console panel or e.g. only HTML, CSS and JS files in the Net panel. See the screenshot.

![multiple-filters](../../assets/22d2b9b151ffb4b5.png)


### Toggle Visibility of Side Panels

You can now toggle visibility of side-panels. The state is persistent across Firefox restarts. See couple of screenshots.

![toggleSidePanels1](../../assets/8203309a2322edcb.png)


If you don’t need the Selectors side panel you can keep it hidden.

![toggleSidePanels2](../../assets/40bb1591f053f557.png)


### Store the result of the last command line evaluation in $_

Firebug implements a new variable available in the Command Line: `$_`

. This variable stores the result of the previous expression evaluation (compatible with Chrome dev tools).

![store-last-command-line-result](../../assets/f1c76b509378f7e3.png)


### New command: getEventListeners()

Firebug implements a new Command Line command: `getEventListeners()`

. This command returns the event listeners registered on a given object. The object is usually an element, but it can also be e.g. a window.

![get-event-listeners1](../../assets/fea4cc4043c700e9.png)


After you execute the command on the Command Line you can further inspect the return object in the DOM panel. See the following screenshot.

![get-event-listeners2](../../assets/8502cc3a2d53309d.png)


### Copy as cURL

It is possible to create cURL command from a network request in order to test the request from the terminal window. Just right click on a request in the Net panel and pick **Copy as cURL**.

![copy-as-curl](../../assets/91dd34fe833e2305.png)


### Precision for Console API %f log pattern

Floats can be rounded by using the %.xf pattern inside the first console.log() argument. Here x denotes the number of decimal places the number should be rounded to.

`console.log("amount: %.2f", 4.3852)`


will output

`amount: 4.39`


![precision](../../assets/981df14325246380.png)


You may want to get to know about the other patterns available inside the [Console API](https://getfirebug.com/wiki/index.php/Console_API#console.log.28object.5B.2C_object.2C_....5D.29).

### Show/hide stack arguments

Stack frames displayed in the Stack panel can be sometimes unusable due to a long list of arguments and so, Firebug introduced a new option *Show Arguments* allowing to show/hide them.

![showArguments](../../assets/4ee487731a091afe.png)


### CSS Panel Improvements

Firebug introduces several improvements for the CSS panel. A lot more CSS information is now available.

- @page rules are displayed
- files with @media elements are displayed
- @keyframes rules are now displayed
- @-moz-document rules are displayed

![css-panel](../../assets/b95ed17a42966c30.png)


There is a lot more new enhancements and you can see the entire list in our [release notes](https://getfirebug.com/wiki/index.php/Firebug_Release_Notes#Firebug_1.12). You can also see the official announcement on [getfirebug.com](http://blog.getfirebug.com/2013/08/21/firebug-1-12-0/).

Follow us on [Twitter](https://twitter.com/firebugnews/) to be updated!

Jan ‘Honza’ Odvarko

## 19 comments

Marc DevolAugust 21st, 2013 at 12:46Ivan DejanovicAugust 22nd, 2013 at 02:27Jan Honza OdvarkoAugust 22nd, 2013 at 05:28JessicaAugust 22nd, 2013 at 05:18Edwin Yip | Live CSS EditorAugust 22nd, 2013 at 06:22Marcelo RamosAugust 22nd, 2013 at 07:54Alexander TkachenkoAugust 22nd, 2013 at 08:32Jan Honza OdvarkoAugust 22nd, 2013 at 09:16Alexander TkachenkoAugust 25th, 2013 at 23:12Damien LebreuillyAugust 22nd, 2013 at 09:27Hoàng nghiêmAugust 24th, 2013 at 08:58Pavel ForkertAugust 25th, 2013 at 12:53Jan Honza OdvarkoAugust 26th, 2013 at 03:26LukeAugust 26th, 2013 at 20:23Jan Honza OdvarkoAugust 27th, 2013 at 00:45pdAugust 28th, 2013 at 07:10Jan Honza OdvarkoAugust 30th, 2013 at 00:52aguruAugust 28th, 2013 at 19:40Mathew PorterSeptember 1st, 2013 at 10:24