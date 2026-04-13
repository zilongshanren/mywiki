---
title: Firebug 1.9 New Features – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/01/firebug-1-9-new-features/
author: Jan Honza Odvarko
published: '2012-01-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Firebug 1.9](https://addons.mozilla.org/en-US/firefox/addon/firebug/) has been released and as usual I would like to get this opportunity to present some new features introduced in this version.

![Firebug](../../assets/e7f20c7022579428.png)


First of all, check out the following compatibility table:

**Firefox 4.0**with**Firebug 1.7.3****Firefox 5.0 – 11.0**with**Firebug 1.9****Firefox 12.0**(nightly) with**Firebug 1.10**

*Firebug 1.10 alpha 1 will be available next week, you can use Firebug 1.9b6 for Firefox nightlies in the meantime.*

Here is a summary of all new features

[Firebug UI docking](https://hacks.mozilla.org#docking)[Copy JSON responses to the clipboard](https://hacks.mozilla.org#json-copy)[Syntax error position displayed](https://hacks.mozilla.org#console-errorcolumn)[New column in the Net panel: Protocol](https://hacks.mozilla.org#net-protocol)[Quickly Remove Elements from the page](https://hacks.mozilla.org#inspect-delete)[Function objects: displayName property](https://hacks.mozilla.org#display-name)[Every Console log has its origin info](https://hacks.mozilla.org#log-origin)[Resend HTTP request](https://hacks.mozilla.org#net-resend)[Tooltip for conditional breakpoints](https://hacks.mozilla.org#breakpoint-tooltip)[Add Watch from the DOM panel](https://hacks.mozilla.org#dom-addwatch)[Response Headers from the browser cache](https://hacks.mozilla.org#net-cachedheaders)[Font Viewer](https://hacks.mozilla.org#net-fontviewer)[Font Tooltip](https://hacks.mozilla.org#css-fonttooltip)[Tooltip tip for array items](https://hacks.mozilla.org#script-arrvaluetooltip)

### Firebug UI docking

Firebug UI can be positioned on all fours sides of the browser window. Just open the *start button* popup menu, pick *Firebug UI Location* sub menu and finally select the position you prefer the most.

![docking](../../assets/dbe7b61fdd289715.png)


### Copy JSON responses to the clipboard

Are you dealing with AJAX & JSON? Firebug allows inspecting JSON responses and copying parts of the JSON tree to the clipboard. Just expand an HTTP request (in the Console or Net panel), select the JSON tab and right click in the tree to get the context menu.

![json-copy](../../assets/f4f0862ea8aba126.png)


### Syntax error position displayed

The Console panel shows an arrow to the exact position inside the line of the syntax error when an error occurred.

![console-errorcolumn](../../assets/60b775bdb7f7c756.png)


### New column in the Net panel: Protocol

The Net panel offers a new *Protocol* column displaying HTTP protocol for every request. You can use this column to sort all request by protocol and e.g. see only *https* requests. The column isn’t displayed by default, you need to right-click on the header and customize…

![net-protocol](../../assets/41d11e9176080db0.png)


### Quickly Remove Elements from the page

The well known *Inspector* feature allows quick removal of selected elements from the page. Just inspect an element and press **Delete** key to remove the currently highlighted element on the page.

![inspect-delete](../../assets/609d4f68da044cf0.png)



### Function objects: displayName property

Firebug also supports a *displayName* function object property. You can use this property to specify custom function name for anonymous functions. Firebug is consequently using that property to display stack traces.

![display-name](../../assets/2690f7ecea5aad90.png)



### Every Console log has its origin info

This is just simple new feature. Every log displayed in the Console has it’s origin (file url and line number). Of course, Firebug shows the source as soon as you click on the origin link.

![log-origin](../../assets/0b8a5f1d3760abef.png)


### Resend HTTP request

The net panel allows to resend an existing HTTP request. Just right-click on it and pick *Resend* from the context menu. Nice and easy!

![net-resend](../../assets/fa4de2da7a3a4ba8.png)



### Tooltip for conditional breakpoints

The Script panel is displaying tooltips for conditional breakpoints. You don’t have to open the condition editor to just see the current condition.

![breakpoint-tooltip](../../assets/160ef144c24f4048.png)



### Add Watch from the DOM panel

The DOM panel context menu introduces a new *Add Watch* command. This allows the developer to find specific object or field (can be several layers deep in the structure) and put it directly into the Script panel’s Watch window for further inspection and monitoring.

![dom-addwatch](../../assets/f9ba4c2e0462df4e.png)



### Response Headers from the browser cache

The Net panel is displaying even HTTP headers coming from the browser cache. Just expand an HTTP request and check the *Headers* tab, there is a new section at the bottom (in case the response comes from the cache).

![net-cachedheaders](../../assets/a166cb57a8ca46df.png)



### Font Viewer

Firebug introduces a font viewer (for *.woff files) integrated into the Net panel. If your page is loading such file you can expand appropriate request and see all meta data about the downloaded font. Very cool!

![net-fontviewer](../../assets/53161fb43c39d947.png)



### Font Tooltip

There is yet another neat support for designers. If you move mouse cursor over a font in the CSS panel (or in the Style side panel) you’ll see a tooltip with a font preview.

![css-fonttooltip](../../assets/7265e63126eb51d6.png)



### Tooltip tip for array items

Another nifty improvement is related to debugging and inspecting an array value using tooltips. If you move mouse cursor over array brackets, you can see the actual value, see the screenshot.

![script-arrvaluetooltip](../../assets/810ede0d0a9adf07.png)


Honza

## About
[
Jan Honza Odvarko ](http://www.softwareishard.com/)

Honza is working on Firefox Developer Tools

## 44 comments

YamcshaJanuary 6th, 2012 at 12:38axlotlJanuary 6th, 2012 at 13:10Jan OdvarkoJanuary 7th, 2012 at 00:52Raghav KhungerJanuary 6th, 2012 at 13:32FatihJanuary 6th, 2012 at 14:18Zdeněk ŠtěpánekJanuary 6th, 2012 at 16:27RudyJanuary 6th, 2012 at 16:27SkouaJanuary 6th, 2012 at 20:03Style ThingJanuary 7th, 2012 at 01:47pdJanuary 7th, 2012 at 06:39DanJanuary 7th, 2012 at 07:49Jan OdvarkoJanuary 7th, 2012 at 07:56Fadi El-EterJanuary 7th, 2012 at 22:15Jan ‘Honza’ OdvarkoJanuary 8th, 2012 at 09:59JasonJanuary 7th, 2012 at 22:56AndersHJanuary 8th, 2012 at 09:39Ivan MalopinskyJanuary 8th, 2012 at 09:54Hugh MadisonJanuary 8th, 2012 at 22:37cavo789January 9th, 2012 at 02:25Aamir AfridiJanuary 9th, 2012 at 03:56Julio Silveira MeloJanuary 9th, 2012 at 05:19juan pabloJanuary 9th, 2012 at 05:35SiPlusJanuary 10th, 2012 at 05:52Jan ‘Honza’ OdvarkoJanuary 10th, 2012 at 05:58SiPlusJanuary 10th, 2012 at 05:55Jan ‘Honza’ OdvarkoJanuary 10th, 2012 at 05:59SpudleyJanuary 11th, 2012 at 05:44Jan ‘Honza’ OdvarkoJanuary 11th, 2012 at 06:47Etienne PouvreauJanuary 12th, 2012 at 03:56Jan ‘Honza’ OdvarkoJanuary 12th, 2012 at 04:41JJanuary 13th, 2012 at 08:52Jan OdvarkoJanuary 13th, 2012 at 09:09DmitryJanuary 17th, 2012 at 03:38kenjiruJanuary 30th, 2012 at 03:00melchior blausandFebruary 15th, 2012 at 03:23Jan ‘Honza’ OdvarkoFebruary 15th, 2012 at 04:23vafaFebruary 28th, 2012 at 08:21Jan ‘Honza’ OdvarkoFebruary 29th, 2012 at 07:49Shiv TomarMarch 31st, 2012 at 04:23AghilMay 17th, 2012 at 01:57Jan ‘Honza’ OdvarkoMay 18th, 2012 at 03:33AghilMay 18th, 2012 at 06:08Jan ‘Honza’ OdvarkoMay 18th, 2012 at 06:18YoganshiMay 17th, 2012 at 16:42