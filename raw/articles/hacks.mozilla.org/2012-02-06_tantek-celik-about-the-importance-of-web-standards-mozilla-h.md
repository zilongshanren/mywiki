---
title: Tantek Çelik about the importance of Web Standards – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2012/02/tantek-celik-about-the-importance-of-web-standards/
author: Tristan Nitot
published: '2012-02-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is the fourth installment of [Mission:Mozilla](http://hacks.mozilla.org/category/missionmozilla/), a series of interviews that link Mozillians, the technology they produce and the Mozilla mission. This time, We’re interviewing Tantek Çelik, a long-time Web standards contributor. He started working on web standards at Microsoft in 1998, while leading the development of Tasman, the IE Mac rendering engine, and subsequently founded independent efforts like microformats.org, BarCamp, and most recently, IndieWebCamp.org.

**Tristan** – Hi Tantek, could you introduce yourself? (I could point our reader to [your Wikipedia page](http://en.wikipedia.org/wiki/Tantek), but it seems a bit out of date).

**Tantek** – I’ve been passionate about web standards since being inspired at the level of collaboration among different companies, cultures, individuals at my first W3C CSS&PF WG meeting May 1998 in Paris. My interest in standards as building blocks started much earlier with many childhood hours spent building things with LEGOs.

**Tristan** – Ah, LEGOs! I have fond memories of them, particularly LEGO technic! They’ve inspired so many geeks that they somehow should be credited for their work in W3C specs, don’t you think? ;-)

**Tantek** – Indeed I think LEGOs have inspired many an engineer. Simple pieces that could be combined in numerous ways and built into amazing unique and creative structures.

**Tristan** – Sounds like a good description of Web technologies to me! Who was your employer back then?

**Tantek** – I was working for Microsoft at the time, having joined the Macintosh Internet Products Group in 1997. I started work on Macintosh Internet Explorer (MacIE) in mid 1997 with mostly bug fixes and improvements in CSS support which incrementally made their way into MacIE 4. It was soon clear though that we needed a fairly big overhaul to implement better CSS support. Soon after I joined standards discussions in the W3C.

**Tristan** – It’s a little known fact, but IE Mac was really raising the bar when it came to CSS compliance. It was a time where few people cared about Web standards. I was at Netscape back then, and you at Microsoft. It was amazing to see a team trying to push Web standards on the other side of the fence!

**Tantek** – When I was made the developer lead for the MacIE rendering engine, it wasn’t immediately obvious to me what we should focus on, so I decided to interview web design firms in San Francisco and just ask: “Hi I’m with the Microsoft MacIE team. What would you like to see in terms of standards / rendering support in the next version of MacIE?” The answers were loud and clear: dependable standards support! In particular: reliable and ideally complete CSS support, “XML support” (whatever that meant), and better Javascript/DOM support. A few specifically asked for PNG support. Those interviews drove the priorities of what became *Tasman*, the new rendering engine for MacIE5 which itself in the process got renamed to Internet Explorer 5 for Macintosh (IE5/Mac). Little did I know at the time that such a focus on getting web standards right would come as a surprise to others.

**Tristan** – And now, a few years down the road, we’ve seen how Web standards have made the Web what it is today, but they’re also something that Web browser vendors are heavily investing on! What do you do for Mozilla today? Why should Web developers care?

**Tantek** – I joined Mozilla in May 2010 as Web Standards Lead and I’m excited to be working with so many people passionate about standards. In an organization with numerous talented web standards contributors, in addition to editing/iterating specifications, my role is often more of coordination and collaboration, making sure that folks who care about particular standards find each other and work together. One key thing I’ve created and driven in Mozilla is the open documentation of our standards participation, in a public place where not only we (Mozillians) can find each other, but web developers in general can see [how much effort Mozilla and individual Mozillians put into web standards](https://wiki.mozilla.org/Standards).

**Tristan** – I have the impression that Mozilla does not get the share of credit we deserve when it comes to our work on standards. Don’t you agree?

**Tantek** – As someone who’s been involved with web standards for over a decade, I’ve had a deep respect for Mozilla’s involvement with web standards for quite some time. However I do think that recognition can easily be forgotten outside of standards circles. I think the web community as a whole greatly underestimates the longevity, depth, and dedication of Mozilla’s contributions to web standards.

**Tristan** – Where do you think Mozilla particularly shines?

**Tantek** – One thing that’s always impressed me about Mozilla’s commitment to web standards is the level of quality and thoroughness that Mozilla places into implementations. In my experience, historically Firefox has had the highest fidelity handling of various CSS properties for example, focusing more on getting things precisely right rather than shipping quick implementations that may only cover common or 80% cases.

Second, Mozilla works far more in the open, early and often, than any other organization. For example, we do nearly all our project work on open wiki pages on [wiki.mozilla.org](https://wiki.mozilla.org). I even keep my own Mozilla projects list on an open Mozilla wiki page. It makes it really easy to answer when people ask me[ what am I working on these days](https://wiki.mozilla.org/Tantek-Mozilla-projects).

**Tristan** – I agree with you. I sense that Mozilla tends to do the right thing, rather than the thing that makes us look good. Can you give an example why do Web standards matter?

**Tantek** – *The browser compatibility tax*. When the Web Standards Project started in 1998, they raised the real and painful issue of the “browser compatibility tax” that developers had to pay when developing web sites. No matter what standard a web author would use, they’d have to spend potentially 50-75% of their time purely on making their code work in multiple browsers, sometimes having to write multiple versions of their markup and style sheets and then use fragile user-agent string tests to serve different content (a bad habit that still persists to this day). Much of this was due to the abysmal standards support in 1990s browsers.

Web standards are an agreement between authors and browsers: if the author writes valid code (whether HTML, CSS, or JS), the browsers agree to render and execute it predictably and according to the standards. Without standards, web authors end up wasting their time coding for one browser at a time (typically focusing on whatever is the popular browser that year), and browsers developers end up wasting their time writing code fixing one site at a time.

**Tristan** – And if we want the Web to be the platform of choice for all kind of developers and all kinds of applications, from desktop to mobile, we need to remove this “browser compatibility tax”.

**Tantek** – Yes. It’s up to all of us as browser implementers to provide strictly correct implementations of web standards for authors to use, and for implementers to openly propose and test innovations in web standards.

**Tristan** – what’s your biggest concern about Web standards?

**Tantek** – My biggest concern about web standards can be summed up in four words: *“Best Viewed In […]”* where the fourth word can be filled in with a different browser nearly every year. Anything that encourages web authors to focus on a single browser (or browser engine) to the expense of other browsers hurts the web. It’s also short-sighted – next year all the browsers will change and what was “best” last year is not the same this year, even newer versions of the same browser!

Worst of all is when browser vendors themselves either encourage or outright publish “best viewed in” content themselves, thus setting a bad example for web authors.

Judge for yourself – whenever you see a site purporting to show-off or demonstrate web standards, if the site ever gives you an excuse like “Please use browser X to view this” then they’re misbehaving. Standards demonstrations should simply state the standards they require, and then link to test suites (developed in standards bodies) for you to check your own browser.

And “Best Viewed In” is just one of several concerns.

There are many difficult challenges to open web standards that we must acknowledge and continue fighting hard to overcome. Challenges like patents that may hurt Touch Events, devices that only effectively support a single browser engine, and when one or a small number of companies decide to dictate *de-facto* standards through “delayed open” tactics.

**Tristan** – What’s the most exciting thing going on in the world of Web standards these days?

**Tantek** – So many things to choose from! I think the most exciting thing about web standards these days is the unprecedented level of intense interest and collaboration across numerous companies on the open web platform built on web standards. There’s a rising culture of placing importance on the open web, and I think we have Mozilla to thank for keeping that flame alive for so long and setting an ever higher bar for how to best work openly on open web standards.

The Mozilla Manifesto provides an excellent set of principles for how to do so. I think what’s particularly important is to keep evolving openness, and Mozilla encourages community members to contribute their own views on how and why to work openly. Here is some more on the subject:

[http://paulrouget.com/e/openness/](http://paulrouget.com/e/openness/)[http://tantek.com/2010/281/b1/what-is-the-open-web](http://tantek.com/2010/281/b1/what-is-the-open-web)[http://tantek.com/2011/168/b1/practices-good-open-web-standards-development](http://tantek.com/2011/168/b1/practices-good-open-web-standards-development)

**Tristan** – Thank you very much for your time Tantek, and keep up the good (and open) work!

## 4 comments

SvipFebruary 6th, 2012 at 15:03WillFebruary 16th, 2012 at 14:18TonyGuitarFebruary 17th, 2012 at 11:09TonyGuitarFebruary 17th, 2012 at 11:17