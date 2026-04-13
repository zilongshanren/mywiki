---
title: New Firefox Command Line helps you develop faster – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2012/08/new-firefox-command-line-helps-you-develop-faster/
author: Kdangoor
published: '2012-08-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 16, now on the Beta channel, has a fantastic feature that was mentioned briefly in [the Aurora 16 blog post](https://hacks.mozilla.org/2012/07/aurora-16-is-out/) and first introduced in [a separate post by Joe Walker](http://incompleteness.me/blog/2012/06/18/firefox-command-line/), the feature’s creator. We’ve devoted a sizable portion of the new Developer Toolbar to the “command line”, which you may sometimes see us call GCLI (short for Graphical Command Line Interface). The command line gives you quick keyboard control over your tools and access to features that don’t have any other user interface.

I have made a video version of this blog post so you can see the command line in action:

To get to the Developer Toolbar and the command line, you can use the shift-F2 keyboard shortcut, or select Developer Toolbar from the Web Developer menu. If you want a quicker keyboard shortcut (this *is *a keyboard-heavy feature, after all!), you can use the [Customize Shortcuts](https://addons.mozilla.org/en-US/firefox/addon/customizable-shortcuts/) add-on to override a shortcut that you don’t use.

This command line is designed to be quick-to-type and discoverable. It will complete commands and parameters for you, to save you typing. There’s also a lot of help built in for the commands and their options. Here’s a look at the list of commands shipped with the initial command line release:

## Control Your Tools

Personally, I hate having to reach for my trackpad. Removing my hands from the keyboard just slows me down. The problem is that it’s not easy to remember all of the keyboard shortcuts and traditional keyboard navigation is sometimes not as quick as reaching for the trackpad. Let’s look at how the new command line helps with this.

Let’s say that I forgot the keyboard shortcut for the Web Console. I *could* reach for my trackpad and hit the Web Console button that is conveniently located on the new Developer Toolbar. Or, I can just remember the keyboard shortcut for the command line and run the command `console open`

. Voila! The console opens. What I actually type to run that command is “con<tab>o<tab><enter>”, which is quick to type indeed.

Want to see what else you can do with the Web Console? Type `help console`

.I’m not even sure if there’s a keyboard shortcut for the Clear button in the Web Console. It’s easier to just run the ![](../../assets/4a5e07cac7256f7f.png)


`console clear`

command than try to remember a seldom used shortcut.Here are the current commands that control the developer tools:

**console**– open, clear and close the Web Console**dbg**and**break**– many controls for the Debugger and breakpoints**edit**– open the Style Editor on any of the CSS files loaded in the page**inspect**– open the Page Inspector for a part of the page**resize**– control the Responsive Design View**tilt**– control the 3D page view

Let’s look at a more interesting example. The current design of [mozilla.org](http://mozilla.org/) is a [responsive design](http://en.wikipedia.org/wiki/Responsive_Web_Design). I want to see how the headings will show up on a smaller screen. If I’ve been working on the page, I would likely know some of the IDs and structure used in the page, so I could enter a command like:

`inspect "#home-news h3"`


The “**inspect**” command takes as a parameter a CSS selector that is used to select a node on the page. An easy way to jump into page inspection on any page is to type `inspect body`

, because every page will have only one. After typing `inspect "#home-news h3"`

, I’ll see something like this:

In the style panel, I can see that the font size is set to 28px on this heading. How would it look on a phone-sized screen? Many phones report their size as 320×480. Let’s give that a try by typing the following command:![](https://hacks.mozilla.org/wp-content/uploads/2012/08/Inspection-On-500x255.png)


`resize to 320 480`


That turns on the Responsive Design View and sets the size at the same time. Here’s what the result looks like:

In the Style panel, we can now see that a media query with a max-width has taken effect and the font-size on the heading has dropped to 24px. We can also scroll down and see that the three columns that were side-by-side are now stacked. You could use the ![](https://hacks.mozilla.org/wp-content/uploads/2012/08/Responsive-Inspector-500x254.png)


`resize off`

command to turn off the Responsive Design View, or you could just hit <esc> a couple of times to get back to normal browsing mode.## Entirely New Developer Features

We’ve also added a handful of commands giving you some new and useful powers. Let’s take a look at a few of them.

### Put your hands in the cookie jar

The “**cookie**” command highlights why this command line is a “graphical” command line and not your old ’70s-style command line. Running `cookie list`

on mozilla.org, I see:

The output shows me all of the cookies that I have right now for this site. If I want to remove that cookie, all I have to do is type ![](https://hacks.mozilla.org/wp-content/uploads/2012/08/Cookie-List-500x54.png)


`cookie remove WT_FPC`

*or*, if I think it’s easier, I can click on the “Remove” action listed next to the cookie and that command will be entered on the command line for me. I can also give myself new cookies using the “cookie set” command.

### Screenshots for fun and profit

The “**screenshot**” command is really handy. At mozilla.org, I ran this command:

`screenshot heading.png 0 false h1`


This said to make a file called “heading.png”, wait 0 seconds before taking the shot, don’t include anything outside the visible browser window and finally grab just the element selected by the “h1” CSS selector. The result, saved conveniently in my Downloads directory, looks like this:

The command line provides hints inline for each parameter. Pressing F1 gives me even more help about the current parameter.![](https://hacks.mozilla.org/wp-content/uploads/2012/08/heading-500x56.png)


### Stop the blinking!

The “**pagemod**” command lets you quickly make some bulk changes to the page. If you’re looking at a page and there’s something flashing at you, you can nuke it using the “pagemod remove element” command. See how everything on the page looks without classes by typing:

`pagemod remove attribute class *`


Or, take a look at how a different headline looks:

`pagemod replace "Out of Date News" "The New Hotness"`


Here’s a fun one that’s interesting to try out on popular sites:

`pagemod remove element iframe`


See if you can spot the bits that go away.

### More goodies: grab the HTML, reconfigure Firefox

The “**export html**” command opens a new tab with an HTML snapshot of the current state of the page.

The “**addon**” command lets you quickly enable and disable addons. This is useful for isolating an add-on that might be causing you trouble, or for keeping some add-ons that you don’t use often turned off.

The “**pref**” command lets you easily change one of the many configuration options that Firefox has. For example, if you’d like to do some Firefox add-on development, you may find this command handy:

`pref set devtools.chrome.enabled true`


After that, use the “**restart**” command to restart the browser, and you’ll find that tools like Scratchpad have gained some extra powers for hacking on your browser. While many add-ons these days are restartless, you’ll find that there are still some popular ones that require a restart when enabling or disabling them, and the restart command is handy for that as well.

## Add Your Own

One of the best features of command lines in general is that they are a very scalable form of user interface. Adding more commands does not add visual clutter in the UI you look at all day. Expect to see more commands in future Firefox releases, plus new commands that appear in add-ons.

In a future command line article, we’ll show you how to create your own commands. It’s easier than you might expect!

## 107 comments

RodrigoAugust 30th, 2012 at 11:21Robert NymanAugust 30th, 2012 at 23:56Adrian QuevedoAugust 30th, 2012 at 12:20Robert NymanAugust 30th, 2012 at 23:56DanielAugust 30th, 2012 at 12:36Robert NymanAugust 30th, 2012 at 23:56MartinAugust 30th, 2012 at 13:44Robert NymanAugust 30th, 2012 at 23:57FlakiAugust 30th, 2012 at 13:55Kevin DangoorAugust 31st, 2012 at 07:03FlakiAugust 31st, 2012 at 11:23Sean PalmerAugust 30th, 2012 at 13:57GirishAugust 31st, 2012 at 03:34some_loserAugust 30th, 2012 at 14:36PaulAugust 31st, 2012 at 03:26SeanAugust 30th, 2012 at 15:19Robert NymanAugust 30th, 2012 at 23:58AnonymousAugust 30th, 2012 at 15:23PaulAugust 31st, 2012 at 03:25Joe WalkerAugust 31st, 2012 at 03:29B. MooreAugust 30th, 2012 at 21:48Robert NymanAugust 31st, 2012 at 00:03B. MooreAugust 31st, 2012 at 07:26PaulAugust 31st, 2012 at 03:23B. MooreAugust 31st, 2012 at 07:25M KlemolaAugust 31st, 2012 at 00:50andriyAugust 31st, 2012 at 00:57omissisAugust 31st, 2012 at 01:20Matthew CopperwaiteAugust 31st, 2012 at 01:54Kevin DangoorAugust 31st, 2012 at 07:21Matěj CeplAugust 31st, 2012 at 03:01Kevin DangoorAugust 31st, 2012 at 09:01RobAugust 31st, 2012 at 03:33Kevin DangoorAugust 31st, 2012 at 09:00MauriceAugust 31st, 2012 at 04:15JonathanAugust 31st, 2012 at 06:00Kevin DangoorAugust 31st, 2012 at 08:57Simon StewartAugust 31st, 2012 at 06:50Jean BonbeurAugust 31st, 2012 at 07:01Kevin DangoorAugust 31st, 2012 at 08:55Jean-TiareAugust 31st, 2012 at 07:33Kevin DangoorAugust 31st, 2012 at 07:43wicaAugust 31st, 2012 at 07:46RussAugust 31st, 2012 at 09:32Kevin DangoorSeptember 1st, 2012 at 18:42jiveAugust 31st, 2012 at 10:21Matěj CeplSeptember 1st, 2012 at 01:04Kevin DangoorSeptember 1st, 2012 at 18:43Ronildo CostaOctober 10th, 2012 at 07:30ToufiqAugust 31st, 2012 at 11:01bobAugust 31st, 2012 at 12:09Kevin DangoorSeptember 1st, 2012 at 18:44Marco BerrocalSeptember 1st, 2012 at 13:05mbSeptember 1st, 2012 at 14:00MIKESeptember 2nd, 2012 at 05:18Latrasweb.netSeptember 2nd, 2012 at 06:35NiKoSeptember 3rd, 2012 at 00:03Kevin DangoorSeptember 3rd, 2012 at 06:00NiKoSeptember 3rd, 2012 at 06:05Kevin DangoorSeptember 3rd, 2012 at 06:17Brett ZamirOctober 9th, 2012 at 23:36Kevin DangoorOctober 10th, 2012 at 06:06Brett ZamirMarch 13th, 2013 at 10:55vishal dadwaniSeptember 3rd, 2012 at 14:25diwaker srivastavaSeptember 6th, 2012 at 11:24Xannax ProzaxxSeptember 6th, 2012 at 17:42RussSeptember 7th, 2012 at 06:30deewakerSeptember 7th, 2012 at 07:45Vaidik KapoorSeptember 7th, 2012 at 12:36Kevin DangoorSeptember 7th, 2012 at 19:42sofiSeptember 9th, 2012 at 03:20johnOctober 9th, 2012 at 10:18Kevin DangoorOctober 9th, 2012 at 11:13Vaidik KapoorOctober 9th, 2012 at 23:49Kevin DangoorOctober 10th, 2012 at 06:04Vaidik KapoorOctober 10th, 2012 at 10:11FrankOctober 9th, 2012 at 10:56Miron CatalinOctober 9th, 2012 at 23:50KhalidOctober 10th, 2012 at 02:30RahulOctober 10th, 2012 at 13:05IbeczOctober 14th, 2012 at 10:42Kevin DangoorOctober 14th, 2012 at 18:06NickOctober 15th, 2012 at 12:48Kevin DangoorOctober 15th, 2012 at 17:55Girish SharmaOctober 15th, 2012 at 21:43Kevin DangoorOctober 16th, 2012 at 05:32mark entinghOctober 18th, 2012 at 16:42Vaidik KapoorOctober 18th, 2012 at 22:11vinayOctober 19th, 2012 at 00:27Kevin DangoorOctober 22nd, 2012 at 05:39FlanschOctober 23rd, 2012 at 14:59vinayOctober 25th, 2012 at 03:29jeremyOctober 20th, 2012 at 22:12jeremyOctober 20th, 2012 at 22:14warren nazarenoNovember 2nd, 2012 at 05:41Kevin DangoorNovember 2nd, 2012 at 06:16NickNovember 2nd, 2012 at 06:34Kevin DangoorNovember 2nd, 2012 at 06:50Girish SharmaNovember 2nd, 2012 at 06:52Girish SharmaNovember 2nd, 2012 at 06:52thinsoldierNovember 10th, 2012 at 21:35Louis WangNovember 12th, 2012 at 21:32Arán non ei CatalonhaJanuary 31st, 2013 at 08:50Girish SharmaJanuary 31st, 2013 at 09:28Robert Nyman [Editor]January 31st, 2013 at 09:28Leon VictorFebruary 26th, 2013 at 02:56mspreijApril 11th, 2013 at 06:12