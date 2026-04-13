---
title: 'Help us to make Firefox 4 better: How to open a bug – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2010/08/help-us-to-make-firefox-4-better-how-to-open-a-bug/
author: Paul Rouget
published: '2010-08-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*If you run Firefox Beta or Firefox nightlies, you will probably run into some issues. Reporting these bugs and crashes will help us to make sure the user experience is better for all Firefox 4 users.*

*Marcia Knous is part of the Firefox QA team. Because reporting a good bug is not that easy but extremely important, Marcia explains us how to file a bug correctly:*

## Starting out with bugzilla

So you found a bug – To make sure this bug will be considered, you need to create an entry into our bug database: [bugzilla](http://bugzilla.mozilla.org). And as a good first step into Bugzilla, I strongly suggest you start by watching this video:

**Bugzilla For Humans** – *by Johnathan Nightingale*

You can also use the [Bugzilla Guided Tour](https://bugzilla.mozilla.org/enter_bug.cgi?product=Core&format=guided) which is a step by step Guide to filing a bug.

## Reporting a bug

After you have a better grasp of how to file a bug, it’s time to gather the data we will need to enter the bug into Bugzilla.

As we are web developers, experimenting with pre-release of Firefox and experimenting with new standards, you can be faced with crashes and incorrect behavior.

### Search [Bugzilla](https://bugzilla.mozilla.org/) for the bug first

Although you may not find it, this will at least try to prevent duplicate bugs from being filed. Also consult the [Bugs filed Today](https://bugzilla.mozilla.org/buglist.cgi?cmdtype=dorem&remaction=run&namedcmd=Bugs%20Filed%20Today&sharer_id=159758) link to see if someone beat you to it! You can also add ”’DUPEME”’ to the status whiteboard if you are unsure, and a query will pick that up so we can check to see if it a dupe.

### It’s a crash? Go get the Crash Information

We are keeping a stack trace of crashes. You can see these traces

if you type “about:crashes” in the URL bar

Locate the crash stack – the latest one is the first of the list – it will look something like `[@ libgcrypt.11.dylib@0xc21a ]`

.

Add it in that **exact form** in the Summary field. An example would be: `Crash in [@ libgcrypt.11.dylib@0xc21a ] while loading Zimbra calendar`

.

Paste the report ID link in the Bug Summary section. (This is important so the crash shows up in [crash-stats.mozilla.com](http://crash-stats.mozilla.com) with a bug associated to it). A report ID will look like this: `bp-68a686c4-9a15-4326-a812-c8b772100812`


### Have a Layout bug or Reproducible Crash? Add a Testcase

As you can imagine, it’s way easier to work on a bug with a testcase.

You can attach the testcase under the attachment section. And in this case, add the “`testcase`

” keyword to the bug

### Make the Bug Summary useful

Which version of Firefox do you run? To know that, we

need the “Build ID”. Click “help” then “about Firefox/Minefield”.

It should look like this:

Mozilla/5.0 (X11; Linux i686; rv:2.0b4pre) Gecko/20100817 Minefield/4.0b4pre

Also, include a set of **Steps to Reproduce **the bug. Please be as **detailed **as possible. For example, you should include whether you used the mouse or keyboard to initiate a command. [Mozilla Developer Bug Writing Guidelines](https://developer.mozilla.org/en/Bug_writing_guidelines) has many other suggestions as to what you should include in the bug.

These [Bug Guidelines](https://wiki.mozilla.org/QA/Bug_Guidelines) will take you through a tour of some of the other information that needs to be included, such as Product, Component, Version, Hardware/OS, and Keywords.

(Tip: As a web developer, you probably want to open a bug into the Product **“Core”**. Then, choose the Component depending on the bug.)


### Thank you!!!

We know how difficult it can be to open a bug. Opening a bug is extremely useful. So thank you so much to taking the time to make Firefox better!

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 28 comments

DanAugust 20th, 2010 at 14:27Mike ParksAugust 20th, 2010 at 18:34ex700September 2nd, 2010 at 19:08EthanSeptember 9th, 2010 at 06:01John BeattieOctober 3rd, 2010 at 10:06MikeOctober 24th, 2010 at 15:12MikeOctober 24th, 2010 at 15:20Eric KolotylukOctober 31st, 2010 at 13:48Eric KolotylukNovember 1st, 2010 at 08:07Justo NegronMarch 31st, 2011 at 15:34IchabodNovember 12th, 2010 at 02:24bugsyFebruary 3rd, 2011 at 14:50annetter88March 28th, 2011 at 10:42Justo NegronMarch 31st, 2011 at 15:29Patricia013April 2nd, 2011 at 11:06Amir PApril 21st, 2011 at 14:32AlexMay 7th, 2011 at 02:36Greg SimkinsMay 13th, 2011 at 08:03GlenJune 7th, 2011 at 10:23louisremiJune 8th, 2011 at 05:53ozstampsJune 8th, 2011 at 06:01chamaraJune 16th, 2011 at 20:30louisremiJune 17th, 2011 at 04:21ozstampsJune 17th, 2011 at 04:27louisremiJune 17th, 2011 at 08:07PatriciaJune 17th, 2011 at 08:14PatriciaJune 17th, 2011 at 08:18ChrisFebruary 19th, 2013 at 09:39