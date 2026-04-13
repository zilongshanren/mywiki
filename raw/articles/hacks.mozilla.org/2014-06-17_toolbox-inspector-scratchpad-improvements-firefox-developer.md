---
title: Toolbox, Inspector & Scratchpad improvements – Firefox Developer Tools Episode
  32 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/06/toolbox-inspector-scratchpad-improvements-firefox-developer-tools-episode-32/
author: Brian Grinstead
published: '2014-06-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 32 was just uplifted to the [Aurora release channel](https://www.mozilla.org/en-US/firefox/aurora/), so let’s take a look at the most important Developer Tools changes in this release.

First, we would like to thank all 41 people who contributed patches to DevTools this release! Here is a [list](http://mzl.la/1kFlu0C) of all DevTools bugs resolved for Firefox 32.

# Toolbox

We’ll start out the list with a couple of features that were requested on the new [UserVoice feedback channel](http://mzl.la/devtools) that we are [trying out](https://hacks.mozilla.org/2014/05/launching-feedback-channels-let-us-know-your-ideas-for-firefox-developer-tools/).

Node dimensions are now displayed in the box model infobar. Similar to how other tools work, you can easily refer to the dimensions of the highlighted node directly from the infobar. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=718250) & [UserVoice request](https://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas/suggestions/5894689-show-dimensions-when-hovering-over-an-element-in-i))

![Screenshot of node dimensions being shown in the infobar above the box model highlighter](../../assets/3180cfc36c6d28fd.png)


The ‘pick an element from the page’ button is now closer to the inspector tab so it is quicker to jump between them. *Protip:* you can also use the Ctrl+Shift+C or Cmd+Opt+C [keyboard shortcuts](https://developer.mozilla.org/en-US/docs/Tools/Keyboard_shortcuts) to do the same thing. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=991810) & [UserVoice request](https://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas/suggestions/5714267-inspector-icon-on-the-left))

![Screenshot of the new Inspect Element position on the left side of the toolbox](../../assets/c925bc6ae7eee66f.png)


There is now a ‘full page screenshot’ [command button](https://developer.mozilla.org/en-US/docs/Tools/Tools_Toolbox#Extra_tools). After enabling this button, just press it and a screenshot will appear in your downloads folder. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=991045))

![Screenshot of taking a screenshot of the current page with DevTools](../../assets/75325d7e8843c7e8.png)


A demonstration of the screenshot can be seen in the animated gif below:

![Animated gif of taking a screenshot of the current page with DevTools](../../assets/f7bf7761c4d10455.gif)


New images are being used throughout the DevTools UI to support high pixel density displays (HiDPI), so the UI looks much sharper on these devices. Big thanks to our contributor Tim Nguyen for his hard work on these changes! ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=837188))

# Web Audio Editor

Joining the Shader Editor and Canvas Debugger, the Web Audio Editor is a new media tool that has landed in Firefox 32. After enabling it in the options panel, you can inspect the AudioContext graph and modify properties on AudioNodes. Check out the [Introducing the Web Audio Editor](https://hacks.mozilla.org/2014/06/introducing-the-web-audio-editor-in-firefox-developer-tools/) hacks post for much more information about this tool.

![Screenshot of the new web audio tool](../../assets/f09174394d62c31e.png)


# Inspector

User agent styles can be shown in the Inspector. Since these default styles can interact with your page styles, it is handy to see them. This can be enabled from the options panel, and there is [more documentation](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector#Rules_view) about this feature on MDN. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=935803) & [UserVoice request](https://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas/suggestions/5908197-show-user-agent-css-as-in-firebug))

![Screenshot of viewing user agent styles in the Inspector Panel](../../assets/968a2aab3a5d375b.png)


![Animated gif of viewing user agent styles in the Inspector Panel](../../assets/cd2e6e0c0aca1799.gif)


Hidden nodes are now displayed differently from visible nodes in the markup view. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=911209) & [UserVoice request](https://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas/suggestions/5871316-show-nodes-that-are-display-none-differently))

![Screenshot of hidden nodes being displayed differently in the Inspector panel](../../assets/117c39c483467440.png)


Web fonts are previewable within the font inspector tooltip. When hovering a font stack, you will see the currently applied font in the tooltip (including any web fonts). ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=987797))

![Screenshot of a web font being previewed in the Inspector panel](../../assets/f519a94da97337a6.png)


There is now a ‘Paste Outer HTML’ context menu entry for nodes in the markup view. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=993416) & [UserVoice request](https://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas/suggestions/5871356-context-menu-to-paste-html-in-a-node))

# Scratchpad

There is now type-inference based code completion for JavaScript in [Scratchpad](https://developer.mozilla.org/en-US/docs/Tools/Scratchpad). Open a list of suggestions at your current cursor position with `Ctrl+Space`

and type information about the current symbol can be shown with `Shift+Space`

. It is being powered by the excellent [tern code-analysis engine](http://ternjs.net/). ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=968896))

![Screenshot of scratchpad showing an autocompletion list](../../assets/172c25f5dde4287f.png)


![Screenshot of scratchpad showing type information about a function](../../assets/8c4dad3bac26593e.png)


Do you have feedback, bug reports, feature requests, or questions? As always, you can comment here, [add/vote for ideas on UserVoice](http://mzl.la/devtools) or get in touch with the team at [@FirefoxDevTools on Twitter](https://twitter.com/FirefoxDevTools).

## About Brian Grinstead

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 17 comments

MindaugasJune 17th, 2014 at 08:49Brian GrinsteadJune 17th, 2014 at 09:03MindaugasJune 17th, 2014 at 09:05SkouaJune 17th, 2014 at 08:58Jeff GriffithsJune 17th, 2014 at 11:34neeksJune 17th, 2014 at 09:28Brian GrinsteadJune 17th, 2014 at 09:33LukeJune 18th, 2014 at 19:05MindaugasJune 17th, 2014 at 09:44ScampDoodleJune 17th, 2014 at 15:04Brian GrinsteadJune 18th, 2014 at 05:28JuniorJune 18th, 2014 at 05:22JuniorJune 18th, 2014 at 05:25Robert Nyman [Editor]June 18th, 2014 at 10:29EduardoJune 21st, 2014 at 09:07SebastianJune 27th, 2014 at 00:43Brian GrinsteadJune 27th, 2014 at 05:29