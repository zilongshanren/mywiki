---
title: Editable box model, multiple selection, Sublime Text keys + much more – Firefox
  Developer Tools Episode 31 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/05/editable-box-model-multiple-selection-sublime-text-keys-much-more-firefox-developer-tools-episode-31/
author: Heather Arthur
published: '2014-05-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A new set of the [Firefox Developer Tools](https://developer.mozilla.org/docs/Tools) features has just been uplifted to the [Aurora channel](http://www.mozilla.org/firefox/aurora/). These features are available right now in Aurora, and will be in the Firefox 31 release in July. This release brings new tools, editor improvements, console and inspector features:

## Editable box model

The Box Model tab in the [Inspector](https://developer.mozilla.org/docs/Tools/Page_Inspector) is now editable for easy experimentation. Double-click any of the margin, border, or padding values to change its value for the currently selected element. Enter any valid CSS [<length>](https://developer.mozilla.org/docs/Web/CSS/length) value and use the `Up`

/`Down`

keys to increment or decrement the value by `1`

. `Alt-Up`

increments by `0.1`

and `Shift-Up`

increments by `10`

. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=850336))

![Editing the box model](../../assets/9d22b51edb70dc9c.png)


## Eyedropper

New to the color picker in the Inspector is an [Eyedropper tool](https://developer.mozilla.org/en-US/docs/Tools/Eyedropper) that grabs the color from any pixel on the page. Select the current color by clicking or pressing `Enter`

. Abort the operation by pressing `Esc`

. Use the `Up`

/`Down`

keys to move by one pixel, and `Shift-Up`

/`Shift-Down`

to move by 10 pixels.

![Eyedropper tool](../../assets/de3bb25367c603c5.png)


You can also use the eyedropper directly to copy a color to the clipboard by accessing it from `Web Developer`

menu, or the toolbar icon that’s enabled by going to the [settings panel](https://developer.mozilla.org/docs/Tools_Toolbox#Settings) and checking `Available Toolbox Buttons`

> `Grab a color from the page`

. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=939040))

## Console stack traces

`console.error`

, `console.exception`

, and `console.assert`

logs in the console now include the full stack from where the call was made. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=920116))

![Stack trace in console.error() printout](../../assets/c77ae1cac1aa688d.png)


## Styled console logs

On parity with other browser developer tools, you can now add style to console logging with the `%c`

directive.

([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=823097))

![Using %c in console.log() to format output](../../assets/6ace55e211b2ce42.png)


## Copy as cURL

Replay any network request in the [Network Monitor](https://developer.mozilla.org/docs/Tools/Network_Monitor) from the comfort of your own terminal. Right-click a request and select the `copy as cURL`

menu item to copy a [cURL](http://en.wikipedia.org/wiki/CURL) command to the clipboard, including arguments for headers and data. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=859059))

![Copy as cURL in Network tool](../../assets/b737aa2b7aec7973.png)


## Editor – multiple selection, Sublime Text keys

The source editor used in the developer tools has been upgraded to CodeMirror 4. With that brings:

**Multiple selection**. Hold down

`Ctrl`

/`Cmd`

while selecting to get multiple selections.**Rectangle selection**. Hold down

`Alt`

to select a column-aligned block of text.**Undo selection**. Undo the last selection action with

`Ctrl-U`

/`Cmd-U`

and redo with `Alt-U`

/`Shift-Cmd-U`

.**Sublime Text keybindings**. To enable, go to

`about:config`

in the url bar and set `devtools.editor.keymap`

to `sublime`

.Multiple selection in action:

![animation of multiple selection in the editor](../../assets/1b1797828b2716b6.gif)


## Canvas Debugger

Debug animation frames in WebGL and 2d canvas contexts with the newly-landed canvas debugger. The canvas debugger is an experimental feature that has to be enabled in the setting panel. Multiple canvases are not yet supported ([bug](https://hacks.mozilla.org/978948)) as well as animations generated with setInterval ([bug](https://bugzilla.mozilla.org/show_bug.cgi?id=978948)). The canvas debugger is described in more in this [blog post](https://hacks.mozilla.org/2014/03/introducing-the-canvas-debugger-in-firefox-developer-tools/).

([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=917226))

## Add-on Debugger

If you develop Firefox add-ons using the [Add-on SDK](https://developer.mozilla.org/Add-ons/SDK), there’s now a much easier way to debug your add-on’s JavaScript modules. See the [blog post](https://blog.mozilla.org/addons/2014/04/08/add-on-debugger-now-in-firefox-nightly/) for more details. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=899054))


[Firefox 31: Add-on Debugger](http://vimeo.com/90886107) from [Jordan Santell](http://vimeo.com/user7515802) on [Vimeo](https://vimeo.com).

## Other features

**Expand descendants**. Hold`Alt`

while double-clicking a node in the Inspector to expand all of its children and descendants. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=997622))**Persist network logs**. Check`Enable persistent logs`

in the[settings panel](https://developer.mozilla.org/docs/Tools_Toolbox#Settings)to keep Network panel logs across reloads and navigations. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=925275))**JS warnings on by default**. JavaScript warnings now show up in the Console by default. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=991734))**Scratchpad View menu**. The[Scratchpad](https://developer.mozilla.org/docs/Tools/Scratchpad)tool now has a View menu with options for changing font size, hiding line numbers, wrapping text, and highlighting trailing spaces. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=953206))

Special thanks to the 38 contributors that added [all the features and fixes](http://mzl.la/Ri1gOT) in this release.

Questions or suggestions? Comment here or shoot feedback to [@FirefoxDevTools](https://twitter.com/firefoxdevtools) on Twitter or our brand new [feedback channel for Firefox Developer Tools](https://ffdevtools.uservoice.com/). If you’d like to help out, check out the [guide to getting involved](https://wiki.mozilla.org/DevTools/GetInvolved).

## About Heather Arthur

Firefox developer tools developer at Mozilla, working mainly on the style tools.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 43 comments

StanislasMay 7th, 2014 at 10:33panziMay 7th, 2014 at 12:24Matt HughesMay 7th, 2014 at 14:58Paul IrishMay 7th, 2014 at 17:29Robert Nyman [Editor]May 8th, 2014 at 01:18Tim PetersonMay 8th, 2014 at 04:10ArturMay 7th, 2014 at 18:45VickyMay 7th, 2014 at 10:40Robert Nyman [Editor]May 7th, 2014 at 11:58Nick FitzgeraldMay 7th, 2014 at 13:33LukeMay 7th, 2014 at 17:58SkouaMay 7th, 2014 at 10:47Robert Nyman [Editor]May 8th, 2014 at 01:19FelixMay 7th, 2014 at 11:52Robert Nyman [Editor]May 8th, 2014 at 01:20Brian GrinsteadMay 8th, 2014 at 05:40Richard MagnanoMay 7th, 2014 at 13:09KimMay 8th, 2014 at 11:30ryanMay 7th, 2014 at 15:30Heather ArthurMay 7th, 2014 at 22:10Lewis WeaverMay 7th, 2014 at 16:08Robert Nyman [Editor]May 8th, 2014 at 01:20RafeMay 12th, 2014 at 01:20shadenfrohMay 14th, 2014 at 00:37Mr. MacMay 7th, 2014 at 18:37Robert Nyman [Editor]May 8th, 2014 at 01:22Samuel ReedMay 7th, 2014 at 22:58Robert Nyman [Editor]May 8th, 2014 at 01:07/dev/webMay 8th, 2014 at 01:00Robert Nyman [Editor]May 8th, 2014 at 01:23Mark LearstMay 8th, 2014 at 02:30Robert Nyman [Editor]May 8th, 2014 at 04:21AsadMay 8th, 2014 at 05:55Tim GummerMay 8th, 2014 at 23:03Robert Nyman [Editor]May 9th, 2014 at 02:41NicMay 8th, 2014 at 23:21Che xanhMay 10th, 2014 at 11:19Minh KiênMay 10th, 2014 at 11:22StanimirMay 14th, 2014 at 22:18Robert Nyman [Editor]May 15th, 2014 at 01:11Anton KattsynMay 18th, 2014 at 12:29JeffMay 29th, 2014 at 06:44Alex MarinoJune 1st, 2014 at 07:25