---
title: 'A Web for Everyone: Interviews with Web Practitioners — Rachel Andrew – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2016/08/a-web-for-everyone-interviews-with-web-practitioners-rachel-andrew/
author: Justin Crawford
published: '2016-08-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A recent article on Mozilla Hacks, “[Make the Web Work for Everyone](https://hacks.mozilla.org/make-the-web-work-for-everyone/),” explored challenges and opportunities in browser compatibility. In that post we urged developers to build cross-browser compatible web experiences in order to [maximize exposure and market size](https://hacks.mozilla.org/2016/07/make-the-web-work-for-everyone/?utm_source=hacks&utm_medium=article&utm_campaign=compat&utm_content=market_size#other_browser); [prevent interface bugs](https://hacks.mozilla.org/2016/07/make-the-web-work-for-everyone/?utm_source=hacks&utm_medium=article&utm_campaign=compat&utm_content=drive_users_away#wont_change) that drive users away forever; and [demonstrate professional mastery](https://hacks.mozilla.org/2016/07/make-the-web-work-for-everyone/?utm_source=hacks&utm_medium=article&utm_campaign=compat&utm_content=professional_mastery#craft).

Today we’re kicking off a series of interviews with web developers who have earned widespread admiration for their work on the web. Do these professionals at the top of their field take web compatibility as seriously as we do? Why or why not? And how do they go about achieving it?

We’ll start by talking with Rachel Andrew ([@rachelandrew](https://twitter.com/rachelandrew)).

![Rachel Andrew Rachel Andrew](../../assets/c4db06837c9ec4ab.jpg)


Rachel is a founder and managing director of [edgeofmyseat.com](http://edgeofmyseat.com), the company that builds [Perch CMS](https://grabaperch.com/). She has worked on the web since 1996; in that time she’s authored [numerous books about CSS and HTML5](https://rachelandrew.co.uk/books). She is a frequent speaker at web development conferences (you can see her [talking about CSS layouts at View Source 2016](https://viewsourceconf.org/berlin-2016/schedule/#layout) in Berlin, September 12-14). She blogs at [rachelandrew.co.uk](https://rachelandrew.co.uk).

**So Rachel, what does cross-browser compatibility mean to you?**

Doing my job properly! That’s it really.

**How often do you have to think about cross-browser compatibility? Have you found ways to work that allow you to reduce the amount of time you think about it compared to when you were less experienced?**

I think about it a lot less now than I used to. The main core things we want to do work cross-browser in a consistent way. We don’t have wildly buggy behaviour as we had in the past. New developers should go look at [positioniseverything.net/explorer.html](http://www.positioniseverything.net/explorer.html) to see the stuff we used to have to deal with!

Where I do need to think about it is when I am using a new specification, something that isn’t fully implemented perhaps. Or something that hasn’t yet been implemented in all browsers, in that case I need to be sure that my usage of that technique for supporting browsers does not cause a problem for people in a browser that hasn’t got that feature yet.

**What motivates you to make the extra effort to build a cross-browser compatible site or product?**

I’ve always worked from the assumption that the web is for everyone.


I’ve always worked from the assumption that the web is for everyone. I’m also old enough to understand how fast this stuff changes. As far as I can see the absolute best way to ensure that things work well for people now and a year down the line is to get them working in the biggest possible number of browsers and devices today.

**Could anything convince you not to make that effort?**

Not really, because it is so ingrained into how I work. I also know from experience that when someone says the site only needs to work in a certain browser, look a year down the line and that might change.

Also, in a world of evergreen browsers, working cross-browser can actually mean improving the future experience for the people using the browser with the biggest market share. Here’s an example: `position: sticky`

, enabling sticky headers on tables and navigation has been in Firefox for a good while. It is [currently behind a flag in Chrome](http://caniuse.com/#feat=css-sticky). Over 50% of my users are in Chrome, however the sticky headers on a table are a nice enhancement so I might use `position: sticky`

to add that little touch for Firefox users who have support.

We think of cross-browser being dull grunt work, battling with old browsers and weird bugs. However it can also be pretty fun and liberating, especially right now. There is new stuff shipping all of the time, you miss out if you don’t take a look at who is shipping what.


When Chrome ship their support, suddenly all those users will get that nice enhancement. The site will get better for them without me having to ship any code. So being aware of what is shipping in different browsers means you can take advantage of new stuff and leave these enhancements in your site for other browsers to grow into.

We think of cross-browser being dull grunt work, battling with old browsers and weird bugs. However it can also be pretty fun and liberating, especially right now. There is new stuff shipping all of the time, you miss out if you don’t take a look at who is shipping what.

**Can you think of a particularly vexing or interesting compatibility bug you’ve encountered?**

Not really, of course I’ve had them. No matter how much testing you do you can be sure that something subtle or not so subtle will happen at some point. What you find is that the more time you have invested into understanding why things work as they do, the more these issues just become a bit annoying rather than giant showstoppers. Actually practicing working cross-browser in non-stressful situations means that when something baffling does occur you have the ability to take a step back and debug it, figure out how that user could possibly be seeing what they are seeing and get it fixed.

**Have you ever had to convince a client or boss that building a cross-browser compatible site was important? How’d you do it?**

Even back in the days of the browser wars I never mentioned it, I just did it. It’s how we work.

**Did you ever have a specific experience that caused you to take cross-browser compatibility more seriously with your next project?**

Not really, I’ve been doing this for a long time! However I used to do a lot of troubleshooting of work done by other people. Rather than starting from a baseline of solid experience and enhancing from there, they would have all started with something that only worked in one browser and then tried to retrofit compatibility for the others. Fixing the mess often meant going right back to basics, figuring out the core experience that was needed and then building back up the desired result in those browsers that supported the full experience.

**In your post, “Unfashionably Profitable,” you say, “Everything should be possible without JavaScript.” Do you think over-reliance on JavaScript has made the web less cross-browser compatible?**

I think that people will often reach for JavaScript earlier in the process than they need to. Even if they are not building the whole thing as a JavaScript application there is a tendency to assume JavaScript is required for all sorts of things that can be achieved without it, or where a baseline experience can be developed without JavaScript to be enhanced later.

I’m not saying “don’t use JavaScript” but the fact is that as soon as you bring JavaScript into the mix you have a whole host of new potential compatibility problems. A development practice that brings these things in one at a time and encourages testing at each stage makes the whole process much much easier.

**Are there parts of your process/toolchain/etc. that make it easy for you to incorporate or test for compatibility that you would recommend every web developer incorporate into their own?**

I’m pretty old-school when it comes to tools, however I am a big fan of [BrowserStack](https://www.browserstack.com), mostly because I travel a lot and can’t fill that laptop with virtual machines or drag several devices around with me.

**What would you tell a brand new developer graduating from a coding bootcamp about cross-browser compatibility?**

Start out right and you probably won’t have to think about it too much.


Everything gets easier if you start by figuring out what the core thing the site or application or feature you are building needs to do. Build that, make sure it works in a few browsers. Then, and only then start to add the bells and whistles. Don’t get everything working in one browser and then a day before launch think, “hmm maybe I should test this in another browser”. That is when cross-browser becomes difficult, when you try and do the retro-fitting.

Start out right and you probably won’t have to think about it too much.

**Tips from Rachel’s interview**

- Experiment with upcoming or partially-implemented browser features, but use them only to enhance basic functionality, not to deliver basic functionality.
- Add new features one at a time and test their compatibility as you go. Don’t wait to test at the end.
- If you don’t have access to all the machines and devices you need to test on, test in one of the
[online browser testing tools](https://hacks.mozilla.org/2016/07/make-the-web-work-for-everyone/#tools).

## About
[
Justin Crawford ](http://hoosteeno.com)

Justin Crawford is a product engineer at Mozilla, working on developer marketing and growth. He likes thinking about the future, building things and riding bikes.