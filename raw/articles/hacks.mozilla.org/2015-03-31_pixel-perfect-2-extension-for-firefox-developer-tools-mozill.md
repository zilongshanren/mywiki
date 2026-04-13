---
title: 'Pixel Perfect 2: extension for Firefox Developer Tools – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2015/03/pixel-perfect-2-extension-for-firefox-developer-tools/
author: Jan Honza Odvarko
published: '2015-03-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Pixel Perfect](https://github.com/firebug/pixel-perfect/wiki) is a Firefox extension that enables web designers to overlay a web page with semi-transparent images (layers). The designer can then tweak the page’s content until it exactly matches the layer.

![](../../assets/95a50925f27a0fe2.png)



This extension was originally introduced for Firebug back in 2008 but has not been maintained for several years. Many of its existing users asked us to bring the feature back, and the [Firebug Working Group](https://getfirebug.com/wiki/index.php/Firebug_Working_Group) got the opportunity to build it again from scratch using the Remote Debugging Protocol that’s built into Firefox. This enabled us to support new features like [multiprocess Firefox](https://developer.mozilla.org/en-US/Firefox/Multiprocess_Firefox) and [remote debugging](https://developer.mozilla.org/en-US/docs/Tools/Remote_Debugging). The extension also integrates with [Firebug 3](https://github.com/firebug/firebug.next) (aka Firebug.next), but Firebug isn’t required.

We had two goals in mind when building the extension:

- Make the Pixel Perfect feature available again
- Show how to build a real world extension on top of the Remote Debugging Protocol and other Firefox APIs

This post is about the feature, but if you are an extension developer interested in learning how to build developer or designer tools using the latest Firefox APIs, you might want to read about its [internal architecture](http://www.softwareishard.com/blog/extension-architecture/pixel-perfect-2-developer-tool-extension-architecture).

## Getting started with Pixel Perfect 2

The latest Pixel Perfect 2 (PP2) release can be installed from [addons.mozilla.org](https://addons.mozilla.org/en-US/firefox/addon/pixel-perfect/) (you need to have at least Firefox 36 installed). After installation, you should see a new item in the main Firefox toolbar, with a button on the left and an arrow on the right.

Clicking the button opens PP2, and clicking the arrow shows a menu with links to online resources.

![](../../assets/72f94382ec1b1581.png)


If you have Firebug 3 (currently [alpha](https://github.com/firebug/firebug.next/releases)) installed, you can also open PP2 from the Style Editor panel.

![](../../assets/bfe6dd8671cb5c00.png)


The PP2 UI consists of one floating window that is used to add and remove layers. This is how it looks after installation.

![](../../assets/d2b4ca4ab83a86c1.png)


Add the first layer using the *Add Layer* button. Click the button and pick an image file from your hard drive.

The new layer should be visible inside the floating popup window as well as in the page.

![](../../assets/19e0b56ffc6f6c02.png)


You can change its properties, such as location and opacity. You can also drag the layer in the page.

![](../../assets/e4b57c10a6f30ac6.png)


The screenshot shows a page with the text *Form Editor: Contact Us* and one layer, shown with a blue dashed border, that shows how the page should look. Now you can use the Developer Toolbox to tweak the page to pixel perfection!

Jan ‘Honza’ Odvarko

## About
[
Jan Honza Odvarko ](http://www.softwareishard.com/)

Honza is working on Firefox Developer Tools

## One comment

AlokApril 1st, 2015 at 23:40