---
title: 'Report from Ancona: CONFSL 2012 – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2012/07/report-from-ancona-confsl-2012/
author: Marco Castelluccio
published: '2012-07-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Last month I attended [CONFSL](http://www.confsl.org/confsl12/), an interesting conference about Free Software that took place in [Ancona, Italy](http://en.wikipedia.org/wiki/Ancona). I had the opportunity to meet other Mozillians ([Iacopo Benesperi](http://www.mozillaitalia.org/home/author/iacchi/) and [Francesco Lodolo](http://blog.mozilla.org/l10n/2012/03/23/awesome-l10n-contributor-francesco-lodolo/)) and to talk to some people working for Mozilla: [Tristan Nitot](http://blog.mozilla.org/beyond-the-code/tristan-nitot-bio/), [Marcia Knous](http://bonjourmozilla.fr/?post/2012/02/28/Bonjour-WoMoz-%3A-Marcia-Knous), [Marco Bonardo](http://blog.bonardo.net/), [Paolo Amadini](https://archive.fosdem.org/2012/schedule/.../paolo_amadini.html). They are amazing people who make our lives better with evangelism, development, quality assurance, translations and so on.

The most impressive thing for me was to see how they are passionate about Mozilla and its mission. They all work harder than a typical company employee! This is what Mozilla is about: a great community to be involved in and a great organization to work for. If you believe that what you do will improve users’ freedom, you will work a lot faster and better.

But let me talk about the conference itself: there were many people from all over Italy and there were many interesting talks. Tristan’s keynote was about the Mozilla mission and the new projects to accomplish it: [Firefox Mobile](https://play.google.com/store/apps/details?id=org.mozilla.firefox&hl=en), [Web Apps](https://www.mozilla.org/en-US/apps/partners/) and [B2G](https://www.mozilla.org/en-US/b2g/). (His talk was the most followed, and he did also some interviews for the Italian press).

It is really exciting to see something that you’ve worked on ([Web Apps](https://quality.mozilla.org/2012/06/desktop-web-apps-linux-support-and-mozilla-marketplace/)) demoed! Especially if people show a lot of interest in it. Some of the recurring questions I heard were:

*1) Can we develop using “low-level code” for b2g?
2) Do the webapps need an internet connection?*

These are, in my opinion, the most important questions we need to answer and let developers *and* users know. Here are my **answers**:

*1) Actually with JS and a pinch of WebAPIs, you can use every feature of the underlying hardware. There’s no need to write “low-level code”.
2) This is probably caused by the name of the project. A lot of people think that web apps will work exclusively with an Internet connection, but this isn’t true at all! Web Apps are apps written for a particularly simple and powerful framework: the browser. You can’t see any difference between “native” apps and Web Apps. To
create a web app that works offline, you just need to use this API:
*

[https://developer.mozilla.org/en/Offline_resources_in_Firefox](https://developer.mozilla.org/en/Offline_resources_in_Firefox).

[Another interesting talk](https://quality.mozilla.org/2012/06/joint-dev-qa-presentation-at-italian-free-software-conference/) was led by Marco Bonardo and Marcia Knous. It was about [QA](https://wiki.mozilla.org/QA) and how Mozilla successfully ensures quality for its software, also with the help of users. It was really interesting also because I’m studying testing and quality assurance for an University exam. And I saw something I’ve started to use: [MozTrap](https://github.com/mozilla/moztrap/#readme), a really powerful manual test case management system written by Mozilla.

The last (but not the least) Mozilla talk was about B2G. There were two devices with B2G installed and people were really excited to try them. They were also interested in how to create applications for the device and how to ship them. There’s still a bit of confusion about these matters because the project is still so young and devices are scarce. Someone asked if development was happening behind closed doors.

Obviously not! Like every other Mozilla project, this is free *as in freedom* and you can participate in the development simply. You can start with pulling [the repo](https://github.com/mozilla-b2g/B2G) or visiting the [wiki](https://wiki.mozilla.org/B2G). Just remember that the project is still in its

early stages and so it isn’t stable for everyday use.

There were also other interesting talks about free software, for example a keynote by [Stefano Zacchiroli](http://upsilon.cc/~zack/) (the Debian project leader) and many talks about how to spread free software in Italian schools and public administrations and how to make these PAs use open data formats. There was also an interesting talk about [Mozilla Open Badges](http://openbadges.org/), not held by Mozilla.

So thanks to Mozilla, Tristan, Marcia, Marco, Paolo, Iacopo and Francesco. *“Ci vediamo presto!”*

## About
[
Marco Castelluccio ](https://marco-c.github.io/)

Marco is a passionate Mozilla hackeneer (a strange hybrid between hacker and engineer), who contributed and keeps contributing to Firefox, PluotSorbet, Open Web Apps. More recently he has been working on using machine learning and data mining techniques for software engineering (testing, crash handling, bug management, and so on).