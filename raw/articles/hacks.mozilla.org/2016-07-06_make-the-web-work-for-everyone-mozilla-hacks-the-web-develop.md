---
title: Make the Web Work For Everyone – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/07/make-the-web-work-for-everyone/
author: Justin Crawford
published: '2016-07-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Updated 2016/07/22:Commenters found a few data errors (thanks!) which have now been corrected.

Millions of websites have compatibility problems on one or more of the major browsers, leading to a poor user experience. The web developer community can fix this.

The web has changed immensely in the past 20 years. In 1996 there were roughly [a million websites](http://www.mit.edu/people/mkgray/net/web-growth-summary.html); now there are [more than a billion](http://www.internetlivestats.com/watch/websites/). Back then there were roughly 50 million internet users; today there are [more than 3 billion](https://en.wikipedia.org/wiki/List_of_web_browsers). We have more content than we ever dreamed was possible. People are enjoying it on [8.1 billion connected devices](http://press.ihs.com/press-release/technology/over-8-billion-connected-devices-globally-ihs-says), including [more than 24,000 distinct mobile device types](http://opensignal.com/reports/2015/08/android-fragmentation/).

This explosive growth in content, devices and users has made cross browser compatibility even more essential than it was in 1996. Stack Overflow has [almost 55,000 questions that include the string “cross-browser”](http://stackoverflow.com/search?q=cross-browser), and hundreds of thousands of questions about things that work fine in [Browser X]. Any question about how a particular browser handles a particular site is a potential compatibility question.

So yeah, cross-browser compatibility is still a thing. It’s a thing we care about at Mozilla, and we think you should care about it too. Why? Well, [your users probably aren’t on the same browser as you](https://hacks.mozilla.org#other_browser). They have [different abilities and needs](https://hacks.mozilla.org#accessibility) than you think. They [won’t change browsers if your site breaks for them](https://hacks.mozilla.org#wont_change). Serving them well is [one way to demonstrate mastery of your craft](https://hacks.mozilla.org#craft). And [modern tools](https://hacks.mozilla.org#tools) make it easier than ever.

What causes cross-browser incompatibilities? It’s complex. Here are some of today’s top culprits:

- Developers who use browser-specific features (e.g. vendor-specific prefixing) to achieve certain effects without fallbacks or polyfills for other browsers.
- Browser vendors who rush to implement features developers want before they are standardized.
- Browser vendors who are slow to implement standards and fix bugs in their browsers.
- Sites that employ user agent sniffing to serve different content to different browsers.
- Developers who are over-reliant on a single toolset (which sometimes only reliably supports a single browser) and may miss cross-browser compatibility bugs.
- Growth in the industry — intense demand has encouraged many new web developers to join the field, which means
[developers overall are less experienced on average than they were a few years ago](https://www.developereconomics.com/reports/developer-economics-state-of-developer-nation-q1-2016).

Some of these challenges have been with us since the early days of the web. But since those days, web development has made great progress. Best practices and modern tools can help us build vibrant experiences on every browser.

So, developers, here are a few things to inspire you to **make your next web site work for everyone.**

## More people use *that other browser* than you think

Many developers believe the browser they use is the only browser that anyone really uses, therefore they should just develop for it. [By some measures](http://www.w3schools.com/browsers/browsers_stats.asp), 70% of web developers use Chrome on the desktop. But only about 50% of web traffic across all device types is on Chrome, and only about 62% of web traffic on the desktop is on Chrome. Building and testing only on Chrome alone ignores [almost half of global users](http://gs.statcounter.com/#all-browser-ww-monthly-201506-201606). (It’s worth pointing out here that [different browser share trackers use different methodologies and produce different numbers](https://www.google.com/url?q=https://www.netmarketshare.com/&sa=D&ust=1469221730309000&usg=AFQjCNHyOWMv5Rjg6AmLwWdoqmwaCq1xiw), and the numbers change quickly and often.)

And browser use varies by geography. Chrome, Firefox and IE/Edge are the top browsers in many locales, but the proportion of users on each varies. German users favor Firefox over Chrome. IE is big in Japan. Quite a few Australians choose Safari. [More than 1 in 5 Vietnamese users](http://gs.statcounter.com/#browser-VN-monthly-201505-201605) run a fork of Chromium called Cốc Cốc. Building and testing on just one browser ignores these market differences.

Finally, [features present in your browser may not be present in other browsers](https://developer.microsoft.com/en-us/microsoft-edge/platform/catalog/). Browser vendors implement features on different schedules, so a cool new API in your favorite browser might be missing for a lot of users.

These factors combine in unexpected ways: Choosing an API that isn’t supported in all browsers, testing your site only in one browser, and launching in a market where that browser isn’t dominant could mean excluding substantially more than half of your potential audience. Leaving money on the table. Leaving customers out in the cold. That’s worth making the extra effort to avoid.

## Compatibility intersects with accessibility

Building cross-browser compatible web sites means designing and coding for unknown client environments, in order to make content available to the widest possible audience. And that audience undoubtedly includes people with disabilities — probably more than you think. If your web site works in every browser but falls apart in a screen reader, you’re missing a powerful opportunity.

People with disabilities represent a significant market share. For example, in the U.S. alone, [there are more visually impaired internet users than all Canadian internet users combined.](http://www.interactiveaccessibility.com/accessibility-statistics) Modern web features address this audience’s needs; you just have to implement them.

Accessibility techniques don’t just benefit disabled users either — for example:

- Pages that are more accessible to screen readers are also more accessible to search engine algorithms. Simple accessibility techniques such as using alt-text on images, using descriptive text in links, using CSS for style only (never for meaning), and using HTML5’s semantic tags improve the overall SEO of a page.
-
Transcripts of video content aren’t just good for people with auditory impairments — they are also useful for users on mobile devices in low bandwidth areas that can’t download the video, and people in noisy environments that can’t hear the video. And more text content means more opportunity for relevant keywords, so again, more SEO.


## Users won’t switch browsers, they’ll switch sites

You might think that users will switch browsers to use your site. But many won’t or can’t.

Users have no patience for things that don’t work, and they’ll just go to a competitor’s site instead. Failing at a critical point could turn a potential user away forever. According to [Akamai](https://content.akamai.com/PG2920-Performance-Matters.html),

- 32% of users who encounter a problem on your site are less likely to make online transactions with your company
- 35% will have a more negative perception of your company
- 45% are less likely to visit your web site again
- And more than 1 in 5 users (22%) will leave for good.

What’s more, many users don’t know how to install a new browser, or even know what a browser is (many users don’t know the difference between a browser, a search engine, and a web site).

And even if users know how to install a new browser, and want to, they might not be able to. Many companies mandate which browsers their employees are allowed to use, and many people use public computers in places like libraries.

For example, Microsoft gave a deadline of Jan. 12, 2016 for users to switch to a newer version of the browser, but in March 2016 more than a third of IE users remained on outdated versions that no longer receive security updates. Over the [last year](http://gs.statcounter.com/#desktop-browser_version_partially_combined-ww-monthly-201506-201605-bar) (June 2015-May 2016) 2.07% were running IE8, a browser that Microsoft no longer patches; the same goes for more than three-quarters of the 1.59% on IE9 and for virtually all of the 10.95% who ran IE10 (although it should be noted that the usage of these browsers has dropped significantly since March).

Broken web experiences drive users away. If half of your users are on a different browser, and you want to keep them, testing it in that browser is essential.

## Compatibility === Craft

Creating for the web is a skilled discipline, not just a menial task — we all want to take pride in what we do, hone our craft, and demonstrate our mastery of it. This involves:

- Staying current with the latest technologies, frameworks, and techniques.
- Testing carefully and implementing cross browser/platform apps including fallbacks for less capable browsers. Is the experience acceptable?
- Making sure your web content is accessible to people with disabilities.
- Making sure the general look and user experience of your creations is pleasant and fits in with your/your client’s brand.

So, as a web developer, launched sites are your resumé. A high quality experience is important to your users, your peers and your present and future employers.

But so often, time and business constraints get in the way of such things. You have a hard deadline to hit. Your boss only cares about how the site works on their iPad and hasn’t heard of accessibility. You don’t have time to fix that IE bug in this sprint. We do what we can most of the time, rather than what we’d ideally like to do.

It can be tempting to let cross-browser testing become a corner to be cut when deadlines loom, hoping your chosen framework’s testing will cover you. But your site isn’t purely framework code, and you’re responsible for all of it. Testing to ensure that your code works well across browsers is a corner that you should strongly resist cutting.

Writing code that stands up over time; delivering information to anyone who requests it; creating rich functionality that works for all: These are the noble goals of a great web developer.

## Modern tools can help

Now you know a few great reasons to make your web site more compatible. But how do you do it?

- If you’ve found a bug on
*someone else’s site*, file it at[webcompat.com](http://webcompat.com?utm_source=hacks&utm_medium=blog-post&utm_campaign=compat)! If you’re debugging your own site, read on. - Try your site in different browsers and move through it as a user might. Watch the developer console in the browser’s developer tools for errors (most modern desktop browsers have incredibly capable developer tools built in to help you debug issues, even on mobile):
- If you find a bug that is not in your site, maybe it’s a bug in the browser! Open a bug report so your browser’s developers can fix it:
- Integrate a popular cross-browser-testing tool into your deploy process, to make cross-browser testing automatic:
- Understand which browsers have implemented web features before using them on your site:
- Explore coding tools that can improve cross-browser compatibility:
[Autoprefixer](https://github.com/postcss/autoprefixer),[CSSNext](http://cssnext.io/),[Oldie](https://github.com/jonathantneal/oldie)and other[PostCSS](https://github.com/postcss/postcss#readme)plugins make it possible to write pure, modern CSS that does not break in older browsers[Modernizr](https://modernizr.com/)helps you identify and handle implementation differences between browsers (use this instead of UA sniffing)[@supports](https://developer.mozilla.org/en-US/docs/Web/CSS/@supports?utm_source=hacks&utm_medium=blog-post&utm_campaign=compat)helps you build[progressive enhancements](https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement?utm_source=hacks&utm_medium=blog-post&utm_campaign=compat)into the web experience for more capable browsers

- Go deep. Learn about the web’s many features and quirks. The more you know about it the more you will love it:

## Delivering on the web’s promise

The promise of the web is that anyone can access content using any browser on any device. Woven into this promise are some of humanity’s greatest aspirations — self-determination, freedom, education and discovery. Designing for cross-browser compatibility opens your work up to the largest possible audience and market, advances your mastery of the craft, and is a noble end in itself.

While the modern device and browser landscape presents many challenges, modern tools offer many solutions. More than 3 billion people are out there looking for your site — is it ready for them?

## About
[
Justin Crawford ](http://hoosteeno.com)

Justin Crawford is a product engineer at Mozilla, working on developer marketing and growth. He likes thinking about the future, building things and riding bikes.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## About Ali Spivak

[@alispivak](https://twitter.com/alispivak). Ali is the head of Developer Ecosystem at Mozilla, and has been developing and managing web sites for longer than she cares to admit. She's passionate about keeping the web open and working on things developers love (like MDN).

## 37 comments

Ada Rose EdwardsJuly 6th, 2016 at 06:48Lucas MagroskiJuly 6th, 2016 at 07:39Lucas MagroskiJuly 6th, 2016 at 07:51Chris MillsJuly 6th, 2016 at 09:03Chris MillsJuly 6th, 2016 at 09:08Richard EverettJuly 6th, 2016 at 08:10Chris MillsJuly 6th, 2016 at 09:23PotchJuly 6th, 2016 at 10:41PotchJuly 6th, 2016 at 11:39Nicolas GrillyJuly 6th, 2016 at 08:32Ali SpivakJuly 6th, 2016 at 10:08Nicolas GrillyJuly 7th, 2016 at 05:31Chris MillsJuly 7th, 2016 at 05:39Nicolas GrillyJuly 7th, 2016 at 05:39KenJuly 6th, 2016 at 10:40Chris MillsJuly 6th, 2016 at 10:47MarkJuly 6th, 2016 at 11:15bl4deJuly 6th, 2016 at 11:51Chris MillsJuly 7th, 2016 at 01:19VincentJuly 6th, 2016 at 12:20VincentJuly 6th, 2016 at 12:36Web AxeJuly 6th, 2016 at 18:23Chris MillsJuly 7th, 2016 at 01:19JeremyJuly 6th, 2016 at 22:10RafaelJuly 6th, 2016 at 22:52Chris MillsJuly 7th, 2016 at 01:25YvesJuly 7th, 2016 at 00:43Chris MillsJuly 7th, 2016 at 01:30Niels MatthijsJuly 7th, 2016 at 03:29Chris MillsJuly 7th, 2016 at 04:50Niels MatthijsJuly 7th, 2016 at 04:56Chris MillsJuly 7th, 2016 at 05:02Dietrich AyalaJuly 7th, 2016 at 09:56Dietrich AyalaJuly 7th, 2016 at 17:17Hiroyuki HatanakaJuly 14th, 2016 at 16:44Chris MillsJuly 15th, 2016 at 01:25DanielAugust 2nd, 2016 at 15:16