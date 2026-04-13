---
title: Firefox Aurora 13 Developer Tools Updates – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/03/firefox-aurora-13-developer-tools-updates/
author: Kdangoor
published: '2012-03-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

While users of the Firefox release channel are just now getting to enjoy the [Style Editor and the Page Inspector 3D (Tilt)](http://blog.mozilla.com/blog/2012/03/13/firefox-adds-new-developer-tools-and-add-on-sync/), we have a number of nice developer tools improvements that we’ve shipped to the [Aurora channel](http://mozilla.org/aurora) for Firefox 13. Aurora users are up to 12 weeks ahead of the release channel.

## Page Inspector

Styling CSS menus and other elements that are styled with the :hover, :active and :focus pseudo-classes has gotten much easier. You now have the ability to **lock in a pseudo-class for the selected page element** in the Page Inspector. I have made a 1 minute video to show this feature in action.

Right-click on the page element “infobar” for the selected element to toggle the pseudo-class lock. When you have selected an element in the Page Inspector, the infobar is the hovering box that has the tag name, element ID and classes. We are planning to [add a convenient menu for this feature](https://bugzilla.mozilla.org/show_bug.cgi?id=733612), but you can use pseudo-class locking today with a simple right-click.

When you reopen the Page Inspector, **the HTML panel and Style sidebar will reopen as well**, if you had them open when you last used Page Inspector. This saves you from having to press ctrl-H and ctrl-S to reopen them. If you’re wondering about those keyboard shortcuts, you can find those and other useful tips on the [MDN page for the Page Inspector](https://developer.mozilla.org/en/Tools/Page_Inspector).

When using the Page Inspector 3D view, you can **press the “f” key to bring an element back into view** (focus it). Hint: if you don’t see the 3D button in the Page Inspector, you might have [a blocklisted graphics driver](https://wiki.mozilla.org/Blocklisting/Blocked_Graphics_Drivers). A simple driver update may be all you need.

The **element context menu in the HTML panel now offers some handy actions**.

## Style Inspector

The Style Inspector sidebar of the Page Inspector has had a number of useful upgrades.

You can now select and **copy a rule out of the Rules view.** ~~To make things even quicker and easier, you can copy a rule or part of a rule from the context menu.~~ Update: due to some bugs found during Aurora, the context menu shown to the right has been backed out. You can still copy rules out of the rules view by selecting the text of the rule.

In the Computed view, the **links to the CSS files now go to the Style Editor** rather than View Source. This can make some workflows quicker (see the video in the Style Editor section below).

**Invalid entries in the rules view are now marked with a warning sign.** The tooltip can give you further information about the problem.

Rules applied as the result of a media query will be **shown with the media query**.

## Style Editor and Scratchpad

The Style Editor now **saves CSS files loaded via file:// URLs without prompting**. This makes the workflow for experimenting with CSS *very quick*. This feature actually ships in Firefox 12. It was added during the Firefox 12 Aurora cycle and wasn’t in the original notes posted here.

See the 1 minute video below to get an idea of how smooth this is.

There were a couple of notable changes to the editor code that is shared by both Scratchpad and the Style Editor. **Theme add-ons can now change the editor styles** and you can **select a whole line of code by clicking on the line number** in the gutter of the editor.

## Our top secret developments

I hope you enjoy these updates. I wish I could tell you more about what’s in coming releases, but [no one knows when they’ll land](http://kev.deadsquid.com/?p=1136) or has [any idea](https://bugzilla.mozilla.org/) what could [possibly be in them](https://wiki.mozilla.org/Features). In fact, only a select few can see [unfinished features](http://blog.astithas.com/2012/02/debugging-javascript.html) and we try to ensure that [our secret cabal remains impenetrable](https://wiki.mozilla.org/DevTools/GetInvolved).

It’s just [how we roll](http://www.mozilla.org/about/manifesto.html).

**Update (April 18, 2012): **Note that the context menu for rules in the Style Inspector Rules view has been removed from Firefox 13. Expect to see it return in a future Firefox.

## 28 comments

Ken SaundersMarch 19th, 2012 at 13:46Kevin DangoorMarch 20th, 2012 at 03:22AnonMarch 19th, 2012 at 18:18HanifMarch 20th, 2012 at 01:05Kevin DangoorMarch 20th, 2012 at 03:45Andi SmithMarch 20th, 2012 at 06:28Felipe Kautzmann de MelloMarch 20th, 2012 at 06:43Kevin DangoorMarch 20th, 2012 at 09:58alexleducMarch 20th, 2012 at 10:02Kevin DangoorMarch 20th, 2012 at 10:16Joshua EllingerMarch 22nd, 2012 at 16:20Kevin DangoorMarch 26th, 2012 at 06:07CSSGuyMarch 24th, 2012 at 09:46TorranceMarch 25th, 2012 at 18:48Kevin DangoorMarch 26th, 2012 at 06:09MehranMarch 27th, 2012 at 11:00Kevin DangoorMarch 28th, 2012 at 07:27MehranMarch 27th, 2012 at 11:01Ishan ChaitanyaMay 3rd, 2012 at 02:00RamonJune 6th, 2012 at 10:37Kevin DangoorJune 6th, 2012 at 10:47Alex MarinoJune 8th, 2012 at 09:36Kevin DangoorJune 10th, 2012 at 19:20Alex MarinoJune 11th, 2012 at 06:47Alex MarinoJune 14th, 2012 at 08:02Kevin DangoorJune 14th, 2012 at 08:29Alex MarinoJune 14th, 2012 at 08:49Kevin DangoorJune 14th, 2012 at 08:55