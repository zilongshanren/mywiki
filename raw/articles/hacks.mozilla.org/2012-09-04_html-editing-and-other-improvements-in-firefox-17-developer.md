---
title: HTML Editing and other improvements in Firefox 17 Developer Tools – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/09/html-editing-and-other-improvements-in-firefox-17-developer-tools/
author: Kdangoor
published: '2012-09-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 17 has recently hit the [Aurora channel](http://mozilla.org/aurora), and with it comes a number of improvements to the built-in web developer tools.

## HTML Editing

This is one of the most-requested features for our tools, and we’re happy with the solution we have for you. With the Style panel in the Page Inspector, you can easily manipulate the styles on the page. When you’re working on a layout, however, you sometimes need to manipulate the DOM of the page as well. The new “Markup panel” lets you do just that.

To open the Markup panel, open the Page Inspector and click on the button that looks like an outline and appears right next to the “breadcrumbs” in the toolbar. In the screenshot above, that button is the third from the left. You can also press alt-M (ctrl-M on Mac) to open the Markup Panel.

As before, you can choose elements to inspect in the Style panel by clicking on them in the Markup panel. You can also right-click on the elements in the Markup panel to access a couple of handy features (copy HTML, delete the node).

What’s new in this version of the Markup panel? Previously, you could double click on an attribute value to change that value. Now you can double click almost anywhere to change anything. Double click on text to change the text. Likewise for the tag itself. See that space just before the closing “>” of a tag? Double click there and you can add new attributes.

You’ll also find that keyboard navigation for getting around and editing the DOM is easy to work with. You can use the tab key to move around within a tag and the arrow keys to move between nodes.

Note: the screenshot above shows the Markup panel with a dark theme. The plan is to replace this with a light theme before the feature is released.

## More to love in the Web Console

The Web Console remains a favorite tool among web developers, and we’re happy to have even more improvements for you in this release.

The most visible change in the Web Console is the refreshed toolbar. The Web Console now has an appearance in line with the rest of the Firefox developer tools.

The screenshot above also shows off another improvement: better autocompletion. We’ve found and fixed some cases (like string objects) where the Web Console wasn’t giving as much help as it could.

Another important change to note: the Web Console comes with a helper function called `$`

. Previously, that function was an alias for `document.getElementById`

. In [conjunction with other browser consoles](http://antennasoft.net/robcee/2012/08/03/webconsoles-convenience-function-queryselector/), we’re changing it to be `document.querySelector`

which is far more useful. To get the behavior you had before, just add a # at the beginning of the argument you pass in (for example, `$("#myElementID")`

). You can continue to use `$$`

as an alias for `document.querySelectorAll`

. If you’re using jQuery, the `$`

helper function will be replaced by jQuery, so this change won’t affect you.

Want to be able to see the Web Console’s text a bit more clearly? You can now zoom the Web Console using the same controls you use to zoom the browser window (ctrl-+, ctrl– and ctrl-0 to reset on Windows/Linux. Use cmd-+, cmd– and cmd-0 on Mac).

Using the built-in console.log function is a very handy way to add tracing to your web application. Now, if you send an object to console.log, you can now click on that object in the output area of the Web Console in order to inspect it.

Also in the screenshot above, you’ll see the “More Tools” button in the Developer Toolbar at the bottom of the window. That button gives you quick access to the rest of the developer tools. (Sharp-eyed readers might notice a mysterious “JSTerm” button on my Developer Toolbar. That’s[ Paul Rouget’s JSTerm add-on](http://paulrouget.com/e/jsterm/), which is really nice to use. Check it out!)

## Page Inspector Visual Update

We’ve been listening to feedback from web designers since the Page Inspector made its debut on the Aurora channel last November. We found that the appearance of the dark “veil” over everything but the selected element was striking, but also making it harder for designers to see styling changes they made in the context of their overall design. We added options to turn off the page dimming a few months ago, but in this update we’ve got a lighter approach:

Instead of darkening the whole page, we highlight the selected element using a subtle dashed line and the useful node toolbar. Even better, when you move your cursor to the Style panel to try out style changes, the highlighting fades away entirely so that you can focus entirely on the styling.

## Debugger Improvements

The Debugger has had tons of improvements, some visible and some not, since it hit Aurora three months ago. One of the visible changes that you can see in the screenshot above: search across all scripts! Just go to the find box and start your search with “!” (exclamation point) and you’ll rapidly find matches across all of the scripts in the area just below the toolbar.

If you want more space to look at your code, there’s a new button in the toolbar (the second button on the left in the screenshot) that will close the two side panels to give your code all of the room it needs.

Finally, we’ve got more keyboard shortcuts to make using the Debugger quicker than ever:

- alt-shift-P (Windows), ctrl-shift-P (Mac) to focus the search box
- alt-shift-T (Windows), ctrl-shift-T (Mac) to do a string (token) search
- F6 for continue
- F7 for step over
- F8 for step in
- shift-F8 for step out

**Update: **One more debugger improvement to call out: as noted in the [Firefox 15 release notes](http://www.mozilla.org/en-US/firefox/15.0/releasenotes/), there was a problem with [the debugger not hitting its breakpoints on page reload](https://bugzilla.mozilla.org/show_bug.cgi?id=783393). This is fixed in Firefox 16 (which is now in Beta).

## Try Aurora: it’s good for you!

All of these changes are available today on the [Aurora channel](http://mozilla.org/aurora) and are scheduled for release later in the year. I think you’ll find that Aurora works quite well, so give it a try and let us know what you think via the Feedback button!

## 28 comments

RussSeptember 4th, 2012 at 06:45Kevin DangoorSeptember 4th, 2012 at 07:16RussSeptember 4th, 2012 at 08:07Kevin DangoorSeptember 4th, 2012 at 09:33RussSeptember 4th, 2012 at 10:39tom jonesSeptember 5th, 2012 at 18:18Robert Nyman [Mozilla]September 4th, 2012 at 12:03thinsoldierSeptember 7th, 2012 at 12:56RussSeptember 7th, 2012 at 13:06DanielSeptember 4th, 2012 at 09:34Kevin DangoorSeptember 5th, 2012 at 06:54Jeff SibbachSeptember 4th, 2012 at 23:59FoxinniSeptember 5th, 2012 at 02:41Roman SemenenkoSeptember 5th, 2012 at 02:54tom jonesSeptember 5th, 2012 at 18:11starwedSeptember 5th, 2012 at 21:15SynonymousSeptember 6th, 2012 at 09:36Peter GasstonSeptember 10th, 2012 at 11:11Kevin DangoorSeptember 10th, 2012 at 11:15Dave RodriguezSeptember 12th, 2012 at 09:41Kevin DangoorSeptember 12th, 2012 at 10:50RussSeptember 12th, 2012 at 11:00tom jonesSeptember 21st, 2012 at 18:45Emre AycaOctober 14th, 2012 at 14:44ZsoltNovember 26th, 2012 at 03:11Kevin DangoorNovember 26th, 2012 at 06:22Leho Kraav (@lkraav)December 2nd, 2012 at 05:14Adolfo BenedettiDecember 15th, 2012 at 09:18