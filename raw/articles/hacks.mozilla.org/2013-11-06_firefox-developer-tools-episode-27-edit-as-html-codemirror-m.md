---
title: 'Firefox Developer Tools: Episode 27 – Edit as HTML, Codemirror & more – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2013/11/firefox-developer-tools-episode-27-edit-as-html-codemirror-more/
author: Paul Rouget
published: '2013-11-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 27 was just uplifted to the [Aurora release channel](http://www.mozilla.org/en-US/firefox/aurora/) which means we are back to report on new features in Firefox Developer Tools. Below are just some of the new features, you can also take a look at [all bugs resolved in DevTools for this release](http://mzl.la/HbV06a )).

## JS Debugger: Break on DOM Events

You can now automatically break on a variety of DOM events, without needing to manually set a breakpoint. To do this, click on the “Expand Panes” button on the top right of the debugger panel (right next to the search box). Then flip over to the events tab. Click on an event name to automatically pause the next time it happens. This will only show events that currently have listeners bound from your code. If you click on one of the headings, like “Mouse” or “Keyboard”, then all of the relevant events will be selected.

## Inspector improvements

We’ve listened to feedback from web developers and made a number of enhancements to the Inspector:

### Edit as HTML

Now in the inspector, you can right click on an element and open up an editor that allows you to set the outerHTML on an element.

### Select default color format

You now have an option to select the default color format in the option panel:

### Color swatch previews

The Developer Tools now offer color swatch previews that show up in the rule view:

![](../../assets/59b5aea1f8dd4c1a.png)


### Image previews for background image urls

Highly requested, we now offer image previews for background image URLs:

In addition to above improvements, **Mutated DOM elements are now highlighted** in the Inspector.

Keep an eye out for more [tooltips](https://groups.google.com/forum/#!topic/mozilla.dev.developer-tools/de0xBvHmN4s) coming soon, and feel free to chime in if you have any others you’d like to see!

## Codemirror

[Codemirror](http://codemirror.net/) is a popular HTML5-based code editor component used on web sites. It is customizable and theme-able. The Firefox Devtools now use CodeMirror in various places: Style editor, Debugger, Inspector (Edit as HTML) and Scratchpad.

From the Option panel, the user can select which theme to use (dark or light).

## WebConsole: Reflow Logging

When the layout is invalidated (CSS or DOM changes), gecko needs to re-compute the position of some nodes. This computation doesn’t happen immediatly. It’s triggered for various reasons. For example, if you do “node.clientTop”, gecko needs to do this computation. This computation is called a “reflow”. Reflows are expensive. Avoiding reflows is important for responsiveness.

To enable reflow logging, check the “Log” option under the “CSS” menu in the Console tab. Now, everytime a reflow happens, a log will be printed with the name of the JS function that triggered this reflow (if caused by JS).

That’s all for this time. Hope you like the new improvements!

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 50 comments

Mindaugas J.November 6th, 2013 at 12:05Brian GrinsteadNovember 6th, 2013 at 19:01ChrisNovember 6th, 2013 at 12:07Heather ArthurNovember 7th, 2013 at 10:32ericNovember 6th, 2013 at 12:09PaulNovember 6th, 2013 at 16:43Jeff GriffithsNovember 6th, 2013 at 18:19Brian GrinsteadNovember 6th, 2013 at 19:03Bryce Fisher-FleigNovember 6th, 2013 at 12:23PaulNovember 6th, 2013 at 16:45Jeff GriffithsNovember 6th, 2013 at 18:21Marian KostadinovNovember 7th, 2013 at 10:29Nathan DemickNovember 6th, 2013 at 12:36ChuckNovember 6th, 2013 at 12:38Robert Nyman [Editor]November 6th, 2013 at 12:47Chris ClarkeNovember 6th, 2013 at 13:28Jeff GriffithsNovember 6th, 2013 at 18:22LukeNovember 7th, 2013 at 19:24Gene VayngribNovember 6th, 2013 at 13:41Jeff GriffithsNovember 6th, 2013 at 19:17FlavioNovember 6th, 2013 at 19:13Gene VayngribNovember 6th, 2013 at 23:13Panos AstithasNovember 7th, 2013 at 04:39Gene VayngribNovember 7th, 2013 at 08:35Nathan KleynNovember 7th, 2013 at 02:31Panos AstithasNovember 7th, 2013 at 04:35Mark VNovember 7th, 2013 at 04:18Adonis K.November 7th, 2013 at 04:46Tomer CohenNovember 7th, 2013 at 05:03SamNovember 7th, 2013 at 05:06J. Ryan StinnettNovember 7th, 2013 at 09:59SamNovember 7th, 2013 at 10:21spiritNovember 7th, 2013 at 07:18Brian GrinsteadNovember 7th, 2013 at 08:01nniicoNovember 7th, 2013 at 08:29GaritoNovember 7th, 2013 at 08:39Mindaugas J.November 7th, 2013 at 13:35Jeff GriffithsNovember 7th, 2013 at 13:53Mindaugas J.November 7th, 2013 at 14:23PeterNovember 7th, 2013 at 15:51voracityNovember 7th, 2013 at 21:07PeterNovember 12th, 2013 at 01:38J. Ryan StinnettNovember 12th, 2013 at 08:46LearnerNovember 12th, 2013 at 13:16Jeff GriffithsNovember 12th, 2013 at 14:30Felix NagelNovember 13th, 2013 at 06:18Ryan B.November 18th, 2013 at 14:04Robert Nyman [Editor]November 19th, 2013 at 05:15Ryan BNovember 20th, 2013 at 10:03Robert Nyman [Editor]November 20th, 2013 at 17:02