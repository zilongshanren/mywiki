---
title: Developer Tools in Firefox Aurora 10 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/11/developer-tools-in-firefox-aurora-10/
author: Kdangoor
published: '2011-11-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## The Preview You Can Use Now

Mozilla is building a collection of stable, fast and usable developer tools that ship with the browser. I’d like to introduce a collection of improvements that are scheduled to be released in final form on January 31, 2012.

But, you can *get them now* by downloading the [Firefox Aurora channel](http://www.mozilla.org/en-US/firefox/channel/). I personally find Aurora builds to be quite stable and usable for general browsing and web development. Give it a try and see what you think. You can install Aurora alongside your stable release of Firefox.

## The New Page Inspector

Using built-in tools, you can now peek into your page’s structure and layout. Choose “Inspect” from the “Web Developer” menu, or press the handy ctrl-shift-I (cmd-shift-I on Mac) keyboard shortcut, and you can visually select the page element that is of interest to you.

You’ll also find a new “Inspect Element” context menu item that lets you immediately select the element that’s under your cursor.

When you’re inspecting a page, you’ll see something like this:

[We overlay the page to highlight the element that you’re working with ] (1). The highlighter also shows you the tag, ID and classes associated with the page element you’re viewing.

At the bottom of the window, there’s a toolbar that gives you options for changing or working with the selected element. Starting from the left, there’s a close button to close the page inspector and return to normal browsing. The “Inspect” button toggles visual selection mode so that you can highlight another element. ProTip: pressing the ESC key also switches modes.

### Breadcrumbs

We call the next part of the toolbar the “breadcrumbs”. They show you where you are in the HTML structure *and* let you quickly switch to another element. The selected element is the dark “pushed” button. To the left of it are its parents, and to the right one of its children. Just click one of the buttons to move between the page elements. If you click and hold a button, you get a menu that lets you select from the siblings of the element listed on the button. The breadcrumbs make navigation quick without taking up much of your screen.

### HTML

Sometimes looking at the HTML representation of a page is the quickest way to figure out what’s going on. Click the HTML button and that’s the view you’ll get. There’s a resizer on the right side of the toolbar to set just how much space you want for the HTML view. Also, clicking on a node in the HTML view will select that element for further inspection. ProTip: ctrl-H toggles the HTML view.

### Styles

Last, but definitely not least, is the Style view. This lets you dive in, explore and experiment with your CSS. It offers two separate views of the CSS attached to the selected element: a CSS rules-based view (left, above), and a properties-based view (right, above).

The rules view is organized much like your stylesheets, showing all of the rules that apply to the element and all of those properties that those rules give you. Properties that are overridden are crossed out. You can toggle any single property easily using the checkbox to the left of it. A single click on a property name or value lets you edit it and see the results immediately on the page. If you click anywhere on the line with the brace at the bottom of the rule, you can add a new property there.

On a page with lots of styles, you sometimes just want to find out what the font-size is set to. That’s where the property view comes in. You can expand the “font-size” property and see how its set and which stylesheet set it. By default, only styles that are set in your stylesheets will be displayed (so you don’t get browser defaults listed). If you have a lot of properties listed, as you might if you use a reset stylesheet, you can quickly find what you’re looking for by typing in the search box.

ctrl-S toggles the Style view.

### Web Console + Page Inspector: Great Together

The Web Console is available whenever you want it, even when you’re using the page inspector. If you have an element selected, that element is available to JavaScript in the console using the variable `$0`

.

## Scratchpad

The Scratchpad feature, which we released in August, gives you a very friendly way to experiment with JavaScript. Rather than being confined to a small input box, you get a whole editor window to work with. Now, Scratchpad uses the [Orion](http://eclipse.org/orion/) code editor to provide syntax highlighting, better indentation and other features you’d expect from a modern code editor.

Scratchpad is now wired into Firefox’s “session restore” feature. This means that you can try out a bunch of code in Scratchpad and if you restart Firefox, restoring your session will also bring back your Scratchpad. Of course, you can always save and reload your Scratchpad files, just as you could before.

If you are only doing web development, we’ve streamlined the user interface. If you’re doing Firefox add-on development, you owe it to yourself to set devtools.chrome.enabled to true in about:config. That setting allows Scratchpad to run code in a privileged browser context and not just against the current web page.

## The `console`

Object

We’ve been building out the `console`

object that you call from your JavaScript code or use at the Web Console’s JavaScript input. It is now in line with the [de facto standard](http://getfirebug.com/wiki/index.php/Console_API), implementing the methods that are standard across browsers. Firebug has a couple of others that we don’t implement yet (console.table, console.profile, console.dirxml), but the commonly used methods are there.

## More Is On The Way

All of these features are available now in [Firefox Aurora builds](http://www.mozilla.org/en-US/firefox/channel/). We’re working on getting more new features together for you for the next Aurora.

Check out our [Get Involved](https://wiki.mozilla.org/DevTools/GetInvolved) page to see how you can provide feedback and help make these tools even better.

Footnotes:

[1]. Other web developer tools make changes to your page (for example, adding a class) to make the selected element visible. Firefox’s highlighter does its work without making any changes to your content [.↩](https://hacks.mozilla.org#nochangesreturn)

## 92 comments

patricioNovember 16th, 2011 at 11:08Simon GymerFebruary 1st, 2012 at 06:23danNovember 16th, 2011 at 11:54Kevin DangoorNovember 17th, 2011 at 08:36Josh T.November 16th, 2011 at 12:17Jon zNovember 16th, 2011 at 12:19Kevin DangoorNovember 17th, 2011 at 08:37Kevin DangoorNovember 16th, 2011 at 12:51Robson SobralNovember 16th, 2011 at 13:58Stephan SokolowNovember 16th, 2011 at 14:26Stephan SokolowNovember 16th, 2011 at 16:21Stephan SokolowNovember 16th, 2011 at 14:17Edwin MartinNovember 16th, 2011 at 15:25Stephan SokolowNovember 16th, 2011 at 16:29Robert Nyman [Mozilla]November 17th, 2011 at 02:25GilmoreNovember 16th, 2011 at 17:52Kevin DangoorNovember 17th, 2011 at 08:49AldiNovember 16th, 2011 at 18:13Kevin DangoorNovember 17th, 2011 at 08:51SkouaNovember 16th, 2011 at 18:27Kevin DangoorNovember 17th, 2011 at 08:59selekoNovember 16th, 2011 at 22:46magsoutNovember 16th, 2011 at 23:18pdNovember 17th, 2011 at 04:05Robert Nyman [Mozilla]November 17th, 2011 at 04:11AldiNovember 17th, 2011 at 07:17Robert Nyman [Mozilla]November 17th, 2011 at 07:23AldonioNovember 17th, 2011 at 12:16RaphaelNovember 17th, 2011 at 07:30DharmeshNovember 17th, 2011 at 17:34AlistairNovember 17th, 2011 at 22:18Robert Nyman [Mozilla]November 21st, 2011 at 06:55Robert Nyman [Mozilla]November 18th, 2011 at 01:28Neil OsmanNovember 20th, 2011 at 03:14Robert Nyman [Mozilla]November 21st, 2011 at 06:56BobNovember 21st, 2011 at 10:38Kevin DangoorNovember 21st, 2011 at 10:45Brandon BenvieNovember 21st, 2011 at 14:16Brandon BenvieNovember 21st, 2011 at 14:29Robert Nyman [Mozilla]November 23rd, 2011 at 03:32JamesNovember 21st, 2011 at 16:41Robert Nyman [Mozilla]November 23rd, 2011 at 03:32RahulNovember 28th, 2011 at 11:46RahulNovember 28th, 2011 at 11:57Kevin DangoorNovember 28th, 2011 at 12:46SkouaNovember 28th, 2011 at 15:32RahulNovember 28th, 2011 at 21:24Marco CamposDecember 1st, 2011 at 06:41Kenneth PedersenDecember 1st, 2011 at 11:02EvertDecember 1st, 2011 at 14:57Kevin DangoorDecember 2nd, 2011 at 06:40EvertDecember 2nd, 2011 at 07:12Kevin DangoorDecember 2nd, 2011 at 07:50Dan BlumenthalDecember 1st, 2011 at 19:54Webstandard Blog (Heiko)December 2nd, 2011 at 01:46SimonDecember 2nd, 2011 at 02:08ad4zDecember 2nd, 2011 at 02:53Mister M.December 2nd, 2011 at 05:21Kevin DangoorDecember 2nd, 2011 at 06:43Pablo FernandesDecember 2nd, 2011 at 12:14Brian FentonDecember 2nd, 2011 at 15:27Kevin DangoorDecember 5th, 2011 at 06:58RegnarebDecember 3rd, 2011 at 05:12Kevin DangoorDecember 5th, 2011 at 07:01zahidul hossainDecember 3rd, 2011 at 06:08Oğuz ÇelikdemirDecember 3rd, 2011 at 11:44Kevin DangoorDecember 5th, 2011 at 08:26brentonanthonyDecember 6th, 2011 at 16:03Saeed NeamatiDecember 7th, 2011 at 08:20Corban BrookDecember 7th, 2011 at 10:00Kevin DangoorDecember 8th, 2011 at 06:44Ray M.January 4th, 2012 at 18:40Kevin DangoorJanuary 23rd, 2012 at 14:05AndriyJanuary 13th, 2012 at 15:14Kevin DangoorJanuary 23rd, 2012 at 14:05SamFebruary 7th, 2012 at 10:23Kevin DangoorFebruary 8th, 2012 at 08:58SamFebruary 8th, 2012 at 09:04Kevin DangoorFebruary 8th, 2012 at 09:24AldiFebruary 8th, 2012 at 16:58AmanFebruary 8th, 2012 at 12:43AmanFebruary 8th, 2012 at 12:47Kevin DangoorFebruary 9th, 2012 at 09:38AmanFebruary 9th, 2012 at 10:45Kevin DangoorFebruary 9th, 2012 at 10:57Kevin DangoorFebruary 9th, 2012 at 09:37AmanFebruary 9th, 2012 at 11:05burkMarch 3rd, 2012 at 09:43mmrtntMay 11th, 2012 at 16:59surajJuly 11th, 2012 at 04:31markk morannOctober 6th, 2012 at 00:37Kevin DangoorOctober 6th, 2012 at 08:01