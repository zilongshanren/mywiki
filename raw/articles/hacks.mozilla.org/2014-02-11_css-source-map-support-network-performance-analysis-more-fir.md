---
title: CSS source map support, network performance analysis & more – Firefox Developer
  Tools Episode 29 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/02/css-source-map-support-network-performance-analysis-more-firefox-developer-tools-episode-29/
author: Brian Grinstead
published: '2014-02-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 29 was just uplifted to the [Aurora release channel](https://www.mozilla.org/en-US/firefox/aurora/). This means that it is time to report some of the major changes that you can expect to see inside of the Developer Tools for this release.

## Better Looking Tools

In addition to new features, we have been updating the look and feel of our dark and light themes. The light theme has been completely overhauled, and both themes feature a more consistent design throughout the toolbox. Your current theme can be changed from the [Toolbox settings](https://developer.mozilla.org/en-US/docs/Tools_Toolbox#Settings). [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=957117)

## Network Monitor

The Network Monitor now shows you how long it takes the browser to load different parts of your page. This will help measure the network performance of applications, both on first-run and with a primed cache. [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=946601)

To open the performance analysis tool, click the stopwatch icon in the network panel. For more information, watch the screencast below or [read more on MDN](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor#Performance_analysis).

You can now copy an image request as a Data URI. Just right click on the image request, select the item from the context menu, and the Data URI will be on your clipboard. [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=964014)

## Inspector

We’ve [updated the inspector highlighter behavior](https://hacks.mozilla.org/2014/01/upcoming-changes-to-the-firefox-developer-tools-node-picker/) to bring the highlighting functionality more in line with other tools. [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=916443)

CSS transform preview tooltips have been added to the CSS rule view. Now, if you hover over a CSS transform, you will get a tooltip with a visualization of the transform. Grab a download of Firefox Nightly or Aurora and try it out on some [live CSS transfom examples](https://developer.mozilla.org/en-US/docs/Web/CSS/transform#Live_examples). [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=726427)

![](../../assets/70e5f862aec615c5.png)


CSS rule view now supports pasting multiple CSS declarations at once, like `background: #ccc; color: red`

. [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=913630).

Just like in the network panel, you can now copy `<img>`

elements as Data URIs. [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=964014)

## Style Editor

CSS source map support has been added to the Style Editor. [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=926014), and CSS properties and values will now be autocompleted in the Style Editor. [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=717369)

Want to read more? We have published a post with more information about [using source maps in DevTools to live edit Sass and Less](https://hacks.mozilla.org/2014/02/live-editing-sass-and-less-in-the-firefox-developer-tools/).

## Debugger

We have added a classic call stack list in the debugger next to the list of sources. [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=905981)

There is a new ‘enable/disable all breakpoints’ button in the debugger. This will toggle the active state of all existing breakpoints at once, to allow switching between normal usage and debugging quickly. [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=815280)

You can now highlight and inspect DOM nodes from the debugger. If you hover a DOM node in the variables listing it will be highlighted on the page, and if you click on the inspect icon the node will be opened in the inspector tab. This feature is also available in the console output. [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=952277)

![](../../assets/45e155f1a3573320.png)


Pretty printing now preserves code comments. We are using the open source [pretty-fast](https://github.com/mozilla/pretty-fast) pretty printer, so it should be pretty fast. If it isn’t, be sure to let us know. [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=921163)

## Console

`console.trace`

improvements. The call stack is shown inline with other output, and includes links to access each line in the debugger. [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=790309)

![](../../assets/bf566341080e722c.png)


We’ve also improved console object output to show additional information based on the object type. [(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=843004)

![](../../assets/9b5be55ca00d8377.png)


## Code Editor

The code editor can be seen throughout the tools in places like Scratchpad, Style Editor, and Debugger. Here are some of the updates you will see in this release:

- Code folding in the editor.
[(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=734439) - Emacs and VIM keybindings are now available in the code editor. To enable them, open about:config, and set “devtools.editor.keymap” to either “vim” or “emacs”, then restart DevTools.
[(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=941725) - ES6 syntax highlighting support
[(development notes)](https://bugzilla.mozilla.org/show_bug.cgi?id=960704)

![](../../assets/7c0c88f652c2ab18.png)


Big thanks to all of our DevTools contributors this release (43 people)! Here is a [list of all DevTools bugs resolved for Firefox 29](http://mzl.la/1jpYhzy).

Do you have feedback, bug reports, feature requests, or questions? As always, you can comment here or get in touch with the team at [@FirefoxDevTools](https://twitter.com/firefoxdevtools).

## About Brian Grinstead

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 38 comments

Mindaugas J.February 11th, 2014 at 10:18Stefan BFebruary 11th, 2014 at 10:54Tin Aung LinFebruary 11th, 2014 at 11:24ThomasFebruary 11th, 2014 at 11:42Victor PorofFebruary 11th, 2014 at 11:49tarsolyaFebruary 11th, 2014 at 12:38tarsolyaFebruary 11th, 2014 at 12:42Brian GrinsteadFebruary 11th, 2014 at 12:51al3xaFebruary 11th, 2014 at 16:47Brian GrinsteadFebruary 11th, 2014 at 20:16al3xaFebruary 12th, 2014 at 00:47robceeFebruary 12th, 2014 at 09:58Mike RatcliffeFebruary 12th, 2014 at 03:18keripixFebruary 12th, 2014 at 01:37Brian GrinsteadFebruary 12th, 2014 at 05:56Matěj CeplFebruary 12th, 2014 at 07:00Brian GrinsteadFebruary 12th, 2014 at 08:59FernandoFebruary 12th, 2014 at 10:20Brian GrinsteadFebruary 12th, 2014 at 10:40FernandoFebruary 12th, 2014 at 17:02MikeFebruary 12th, 2014 at 13:04Brian GrinsteadFebruary 12th, 2014 at 16:56NitijFebruary 12th, 2014 at 22:46ChristianFebruary 13th, 2014 at 01:44Victor PorofFebruary 13th, 2014 at 02:45Ivan DejanovicFebruary 13th, 2014 at 07:14OmegaFebruary 13th, 2014 at 11:44toupeiraFebruary 13th, 2014 at 12:48Brian GrinsteadFebruary 13th, 2014 at 13:01Brian GrinsteadFebruary 13th, 2014 at 13:16Tiago CelestinoFebruary 15th, 2014 at 08:23TanimaFebruary 16th, 2014 at 04:10TanimaFebruary 16th, 2014 at 04:13HochzeitsfotografFebruary 19th, 2014 at 12:46Cezary TomczykFebruary 24th, 2014 at 13:31Brian GrinsteadFebruary 24th, 2014 at 13:36Cezary TomczykFebruary 24th, 2014 at 13:52JoseFebruary 27th, 2014 at 10:33