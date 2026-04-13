---
title: Firebug 1.10 New Features – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/07/firebug-1-10-new-features/
author: Jan Honza Odvarko
published: '2012-07-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Firebug 1.10](https://addons.mozilla.org/en-US/firefox/addon/firebug/) has been [released](https://blog.getfirebug.com/2012/07/13/firebug-1-10-0/) and so, let’s see what new features are introduced in this version.

![Firebug](../../assets/e7f20c7022579428.png)


First of all, check out the compatibility table:

**Firefox 5.0 – 13.0**with**Firebug 1.9****Firefox 13.0 – 16.0**with**Firebug 1.10**

*Firebug 1.10 is true community achievement and so, let me also introduce all developers who contributed to Firebug 1.10
*

|
|

## New Features

|

### Bootstrapped Installation

Firebug installation doesn’t require browser restart. Install, press F12 and Firebug is immediately ready at your fingertips.

*If you are updating the previous 1.9 version that require restart you need to restart the browser.*

### Delayed Load

Firebug doesn’t slow down Firefox start-up time anymore! It’s loaded as soon as the user actually needs it for the first time. Only the Firebug start-button and menu is loaded at the start up time.

### Cookie Management

Firebug allows to view and manage cookies in your browser. You can deny cookies for specific sites, filter cookies, create new and delete existing cookies. You can also break into the debugger when specific cookie changes its value and see the line of script that caused the change. And much more! Check out full list of [cookie related features](https://getfirebug.com/cookies).

![Cookie Management](../../assets/6c04730d1c92890f.png)


### Command Editor Syntax Highlighting

Command editor (aka multiline command line) supports syntax highlighting.

![Command Editor Syntax Highlilghting](../../assets/255f9b79c29cca28.png)


### Autocompletion

Autocompletion in Firebug has never been better. This feature helps you when editing CSS properties, variables in the Watch panel, break-point conditions, any numbers, colors, font-families, etc. Just try to edit your page through Firebug UI and you’ll see for yourself.

![Autocompletion within the Watch panel](../../assets/ed1a091e6ff8843d.png)


Check out the screenshot. When typing into the Watch panel, the autocompletion offers variables in the current scope.

### Trace Styles

This feature allows tracing all places which affected specific CSS property. The feature is part of the Computed side panel where every CSS property is expandable. The Computed side panel also supports tooltips for colors, images and fonts.

![Trace CSS Styles](../../assets/07eb08d92433a94c.png)


See, there are three places trying to set the font-size of the selected element (the one in black succeeded). Of course, the blue text/location on the right is click-able and navigates the user the right place. See also [detailed explanation](http://www.softwareishard.com/blog/firebug/firebug-tip-trace-styles/).

### New Command: help

If you are interested what built-in commands are actually available in the Command Line (within the Console panel) just type: `help`

. You’ll see a list of commands with a description.

![Help Command](../../assets/cb6011f3d5266c30.png)


The green command name is a link navigating the user to Firebug wiki with more info (and how-to-examples) about clicked command.

### Link to Web-font Declaration

This feature allows to quickly inspect custom font-family declarations. All you need to do is to right-click on your font-family value, pick *Inspect Declaration* and you’ll be automatically navigated to the CSS panel that shows the place where the font-family is declared. Check out the screenshot below.

![Inspect Font Declaration](../../assets/09ed9383474a930b.png)


### Support For Media Queries

Media queries of @import CSS rules are displayed inside the CSS panel and it’s possible to edit them. Of course, auto-completion works in this case too (e.g. when I did the screenshot, I clicked on 400px value and pressed up-arrow, that’s why there is 401px).

![CSS Media Queries](../../assets/8074b15b6cc15e1b.png)


### Displayed Entities Format

There are new options in the HTML panel that allow changing displayed format of HTML entities.

![Format of displayed HTML entities](../../assets/751186a86df4aa1d.png)


And by the way, MathML entities are also supported.

### Displayed Color Format

There are also new options allowing to change displayed format of CSS colors. Firebug offers three options: Hex, RGB and HSL. These options are available in CSS, Style and Computed panels.

![Format of displayed CSS colors](../../assets/c2140d7005c16a76.png)


### Tooltips for Menu Items

This is one of many little and neat improvements. Every menu item has also a tooltip that explains the associated action. It’s especially useful for options.

![Tooltips For Menu Items](../../assets/86a2a4c84cae2bec.png)


### Support for “focus” CSS pseudo class

Apart from *hover* and *active* CSS pseudo classes, Firebug is also supporting: *focus*.

This feature helps in situations where you want to inspect CSS rules that applies only if the inspected element has focus. Here is what you need to do.

- Use Firebug Inspector to select your element
- Open the option menu for the Style side panel (click the black triangle next to the panel label)
- Check
**:focus**option - Now Firebug simulates the focus state and so, every CSS rule using :focus pseudo class in the selector will be displayed

![Support for :focus pseudo CSS class](../../assets/f838bb91ecd3257c.png)


### HTTP Requests From BFCache

Firebug Net panel is able to display also HTTP requests coming from so called [BFCache](https://developer.mozilla.org/En/Using_Firefox_1.5_caching) (Back-Forward Cache). This cache makes backward and forward navigation between visited pages very fast. Note that this has nothing to do with the [browser cache](https://developer.mozilla.org/en/HTTP_Caching_FAQ).

![Show responses coming from Back-Forward cache](../../assets/0b9bfb51f5988cff.png)


Check out the screenshot, we changed the background for requests coming from the BFCache and so they can be easily differentiated from other requests. Only the last request on the screenshot is coming from the server.

In order to see those requests you need to check *Show BFCache Responses* option.

### Delete CSS Rule

Another neat feature that allows to delete whole CSS rule together with all its properties. Just right click a CSS rule…

![Delete CSS rule with all its properties](../../assets/67c899e69a7db051.png)


Check out our issue tracker for all [79 enhancements](http://code.google.com/p/fbug/issues/list?can=1&q=label%3Afixed-1.10+label%3AType-Enhancement&colspec=ID+Type+Status+Owner+Test+Summary+Reporter&cells=tiles) in Firebug 1.10.

Also, follow us on [Twitter](http://twitter.com/#!/firebugnews) to be updated about upcoming Firebug news!

Jan ‘Honza’ Odvarko

## About
[
Jan Honza Odvarko ](http://www.softwareishard.com/)

Honza is working on Firefox Developer Tools

## 58 comments

BenjaminJuly 13th, 2012 at 07:55BrianJuly 13th, 2012 at 08:53ismaailJuly 13th, 2012 at 13:44SpencerJuly 13th, 2012 at 14:23JesseJuly 13th, 2012 at 16:03jlapitanJuly 13th, 2012 at 16:07JoshuaJuly 14th, 2012 at 02:32ByzodJuly 14th, 2012 at 03:50Sebastian Z.July 17th, 2012 at 00:31asdfasdfJuly 19th, 2012 at 16:08MossJuly 14th, 2012 at 04:42MahendraJuly 14th, 2012 at 05:01SebastianJuly 14th, 2012 at 08:06WebdocJuly 14th, 2012 at 09:25JeffJuly 14th, 2012 at 11:57Jakub VránaJuly 14th, 2012 at 12:16Jan OdvarkoJuly 14th, 2012 at 23:52Vincent F.July 14th, 2012 at 13:55MikeJuly 14th, 2012 at 14:28Stuart GuthrieJuly 14th, 2012 at 17:35kenJuly 14th, 2012 at 19:15Jan OdvarkoJuly 16th, 2012 at 01:19KenJuly 24th, 2012 at 07:09AdrianJuly 15th, 2012 at 23:49pdJuly 16th, 2012 at 02:09spsoftJuly 16th, 2012 at 07:38Jan OdvarkoJuly 16th, 2012 at 08:04John DoeJuly 17th, 2012 at 03:31njspsoftJuly 17th, 2012 at 08:59cancel bubbleJuly 17th, 2012 at 10:09Jan OdvarkoJuly 18th, 2012 at 04:16agadirJuly 18th, 2012 at 03:47JaredJuly 18th, 2012 at 11:19Janet SwisherJuly 18th, 2012 at 12:26Jan OdvarkoJuly 19th, 2012 at 03:58DotJuly 18th, 2012 at 13:15Jan Honza OdvarkoJuly 19th, 2012 at 04:03njspsoftJuly 20th, 2012 at 23:32Sebastian Z.July 24th, 2012 at 22:07Paul LowtherJuly 24th, 2012 at 06:53Just some dudeJuly 31st, 2012 at 15:51MaheshAugust 1st, 2012 at 19:34SatejAugust 1st, 2012 at 21:49IanAugust 3rd, 2012 at 14:35Jan Honza OdvarkoAugust 4th, 2012 at 02:58IanAugust 6th, 2012 at 09:16Ken AmronAugust 5th, 2012 at 04:29Sebastian Z.August 5th, 2012 at 08:06TlacaelelAugust 6th, 2012 at 15:43Jan Honza OdvarkoAugust 6th, 2012 at 22:39TlacaelelAugust 7th, 2012 at 08:48elparoleAugust 21st, 2012 at 06:46Jan Honza OdvarkoAugust 21st, 2012 at 06:53elparoleAugust 21st, 2012 at 07:25Hossein ZolfiAugust 22nd, 2012 at 13:36Ngo HuynhNovember 7th, 2012 at 04:47Jan OdvarkoNovember 7th, 2012 at 06:27Ngo HuynhNovember 7th, 2012 at 06:59