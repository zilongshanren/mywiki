---
title: Event listeners popup, @media sidebar, Cubic bezier editor + more – Firefox
  Developer Tools Episode 33 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/07/event-listeners-popup-media-sidebar-cubic-bezier-editor-more-firefox-developer-tools-episode-33/
author: Heather Arthur
published: '2014-07-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A new set of Firefox Developer Tools features has just been uplifted to the [Aurora channel](http://www.mozilla.org/firefox/aurora/). These features are available right now in Aurora, and will be in the Firefox 33 release in October. This release brings many new additions, especially to the Inspector tool:

## Event listeners popup

Any node with a JavaScript event listener attached to it will now have an “ev” icon next to it in the [Inspector](https://developer.mozilla.org/docs/Tools/Page_Inspector). Clicking the icon will open a list of all the event listeners attached to that element. Click the pause icon to get taken to that function in the [Debugger](https://developer.mozilla.org/docs/Tools/Debugger), where you can set breakpoints and debug it further. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=736078) & [UserVoice request](http://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas/suggestions/5896562-provide-info-about-attached-event-listeners-when-i))

Keep in mind the [events pane](https://developer.mozilla.org/docs/Tools/Debugger#Events_pane) in the Debugger as well, which lists all the event listeners on the page

## @media sidebar

There’s a new sidebar in the [Style Editor](https://developer.mozilla.org/docs/Tools/Style_Editor) which displays a list of shortcuts to every [@media rule](http://css-tricks.com/css-media-queries/) in the stylesheet (or [Sass source](https://hacks.mozilla.org/2014/02/live-editing-sass-and-less-in-the-firefox-developer-tools/)) you’re editing. Click an item to jump to that rule. The condition text of the rule is greyed-out if the media query doesn’t currently apply. This works well in conjunction with the [Responsive Design View](https://developer.mozilla.org/en-US/docs/Tools/Responsive_Design_View) (Opt+Cmd+M / Ctrl+Shift+M) for creating and debugging mobile layouts. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=1012806))

## Add new rule

Right-click anywhere in the Rules section of the Inspector to get an “Add Rule” option. Selecting this will add a new CSS rule, pre-populated with a selector that matches the currently selected node. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=966895) & [UserVoice request](http://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas/suggestions/5871330-adding-new-rules-to-the-current-selection-in-the-c))

## Edit keyframes

Any @keyframes rules associated with the currently selected element are now displayed in the Rules section of the Inspector, and are editable. This is the first step on the way to better debugging of [CSS animations](https://developer.mozilla.org/docs/Web/Guide/CSS/Using_CSS_animations). ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=1030889))

## Cubic bezier editor

To aid in editing easing animations, there’s now a cubic bezier editor that appears when you click the icon next to an animation timing function in a CSS rule. This feature used open source code from [Lea Verou’s cubic-bezier.com](http://cubic-bezier.com). ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=711941))

## Transform highlighter

There’s a new awesome way to visualize how an element has been transformed from its original position and shape. Hovering over a CSS `transform`

property in the Inspector will show the original position of the element on the page and draw lines mapping the original points to their new positions. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=1014547))

## Persistent disable cache

You can disable the browser cache while you’re developing by checking `Advanced Settings`

> `Disable Cache`

in the [Settings](https://developer.mozilla.org/docs/Tools/Tools_Toolbox#Settings_2) tab. Now this setting will persist the next time you open the devtools. As usual, caching is re-enabled for the tab when you close the tools. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=994732) & [UserVoice request](http://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas/suggestions/5895323-option-to-disable-cache-when-developer-tools-are-o))

## New Commands

New commands have been added to the [Developer Toolbar](https://developer.mozilla.org/en-US/docs/Tools/GCLI) (Shift+F2):

- inject
- The new
`inject`

command lets you easily inject jQuery or other JavaScript libraries into your page. Use`inject jQuery`

,`inject underscore`

, or provide your own url with`inject <url>`

. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=1016578)) - highlight
- The
`highlight`

command takes a selector and highlights all the nodes on that page that match that selector. ([video](https://www.youtube.com/watch?v=ImRQQb71gEI))([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=971662)) - folder
- The
`folder`

command opens a directory in your system’s file explorer. Use`folder openprofile`

to open your[Firefox profile directory](https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data). ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=803831))

## Editor preferences

A host of editor preferences are now available in the [Settings](https://developer.mozilla.org/docs/Tools/Tools_Toolbox#Settings_2) panel. From here you can change your indentation settings and change editor keybindings to Sublime Text, Vim, or Emacs. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=964356))

## WebIDE

A big feature called WebIDE has landed, but is behind a preference for this release while it gets more testing. WebIDE is a tool for in-browser app development. See [WebIDE lands in Nightly](https://hacks.mozilla.org/2014/06/webide-lands-in-nightly/) for more details.

## Other features

- Edit selectors
- Click the selector of any CSS rule in the Inspector to edit it. (
[development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=966896)) - Black boxed minified sources
- JavaScript sources with “min.js” extensions are now automatically
[black boxed](https://developer.mozilla.org/en-US/docs/Tools/Debugger#Black_box_a_source). You can turn this option off in the Debugger settings menu. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=1032379)) - Custom viewport dimensions
- The dimensions in the Responsive Design View are now editable so you can input the exact size you want the content to be. (
[development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=762848))

Special thanks to the 33 contributors that added [all the features and fixes](http://mzl.la/1pGLFDs) in this release.

Three of the features from this release came from feedback on the [Developer Tools feedback channel](http://mzl.la/devtools), so that’s a great way to suggest features. You can also comment here or shoot feedback to [@FirefoxDevTools](https://twitter.com/firefoxdevtools) on Twitter. If you’d like to help out, check out the [guide to getting involved](https://wiki.mozilla.org/DevTools/GetInvolved).

## About Heather Arthur

Firefox developer tools developer at Mozilla, working mainly on the style tools.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 21 comments

Brett ZamirJuly 29th, 2014 at 10:07Orville BennettJuly 30th, 2014 at 09:23Robert Nyman [Editor]July 31st, 2014 at 01:23Rachel NaborsJuly 30th, 2014 at 14:17Robert Nyman [Editor]July 31st, 2014 at 01:25AlbertJuly 30th, 2014 at 18:37Robert Nyman [Editor]July 31st, 2014 at 01:29AlbertJuly 31st, 2014 at 15:03Robert Nyman [Editor]August 1st, 2014 at 02:33AlbertAugust 3rd, 2014 at 11:07Robert Nyman [Editor]August 4th, 2014 at 01:31ChristianJuly 30th, 2014 at 22:59Robert Nyman [Editor]July 31st, 2014 at 01:23Heather ArthurAugust 1st, 2014 at 11:02NoitidartAugust 1st, 2014 at 15:50CriaçãoAugust 3rd, 2014 at 11:37Robert Nyman [Editor]August 4th, 2014 at 01:32JeffreyAugust 3rd, 2014 at 12:30Robert Nyman [Editor]August 4th, 2014 at 01:33Dave CampAugust 4th, 2014 at 11:03JeffreyAugust 5th, 2014 at 11:11