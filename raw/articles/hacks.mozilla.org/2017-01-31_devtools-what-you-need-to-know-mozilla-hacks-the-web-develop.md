---
title: 'DevTools: What you need to know – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2017/01/devtools-what-you-need-to-know/
author: Patrick Brosset
published: '2017-01-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The end of the year is always very busy, so we wanted to take one final look back at the last months of 2016.

Many things changed in [Firefox DevTools](http://twitter.com/firefoxdevtools) last year, particularly towards the end of the year. The effort to refactor some of our tools started to pay off and we landed some great re-designs that should make web developers’ lives easier.

## Shiny new tools

We shipped a brand new [ CSS Grid inspection tool](https://hacks.mozilla.org/2016/12/css-grid-and-grid-highlighter-now-in-firefox-developer-edition/), first of its kind (thank you

[gabrielluong](https://twitter.com/gabrielluong),

[helenvholmes](https://twitter.com/helenvholmes), and

[jensimmons](https://twitter.com/jensimmons?lang=en)).

We also shipped **a brand new, redesigned, console panel**. It’s only enabled in [Nightly](http://nightly.mozilla.org/) for now, but it’s on track to be enabled everywhere very soon.

A lot of work went into creating [Reps](https://github.com/firefox-devtools/devtools-reps), the reusable widgets responsible for displaying all kinds of output in the console. This is great because these reps are shareable components that we’ve already begun to use in many other DevTools.

Thank you to a lot of people, especially contributor [nicolaschevobbe](https://twitter.com/nicolaschevobbe), [bgrins](https://twitter.com/bgrins), [Honza](https://twitter.com/janodvarko), [linclark](https://twitter.com/linclark), and others.

![Screenshot of the new front-end for the web console panel in firefox](../../assets/5fb2483afadd2b9a.png)


2016 was also the year we shipped our [ brand new debugger front-end](https://hacks.mozilla.org/2016/09/introducing-debugger-html/)! This was an accomplishment that we can be proud of, that sets the stage for more awesome tool releases in 2017.

I’m personally really excited by the impact we’ve seen since moving this project to [GitHub](https://github.com/firefox-devtools/debugger.html). The beginning of 2017 will be an interesting time for us to experiment with moving even more code to GitHub. I’m already confident that this is the right thing for us to do at this stage, and we have the debugger project to thank for this.

Props go to [jasonlaster](https://twitter.com/jasonlaster11), [jlongster](https://twitter.com/jlongster), [clarkbw](https://twitter.com/clarkbw) and the [debugger github community](https://github.com/fireforx-devtools/debugger.html/graphs/contributors) that has been so great.

![Animation showing the new debugger front-end in action in Firefox.](../../assets/f2ef536b06868c93.gif)


As if that’s not enough to impress, we also shipped [ the new, completely redesigned RDM (responsive design mode)](https://hacks.mozilla.org/2016/11/new-responsive-design-mode-rdm-lands-in-firefox-dev-tools/) in November 2016.

Not only do the responsive views look and work better, RDM also comes with major new features like network throttling and more. Thank you to [jryans](https://twitter.com/jryans), [zer0](https://twitter.com/zer0), [gabrielluong](https://twitter.com/gabrielluong).

## There is no XUL. Only Web.

2016 was the year when the team actively removed non-standard XUL markup and Firefox-only privileged JavaScript from the tools. In fact, we were able to load **the inspector panel in a normal browser tab** by end of year, which means that the inspector is now built entirely with HTML and web APIs.

Great work [bgrins](https://twitter.com/bgrins), [juliandescottes](http://twitter.com/juliandescottes), [tromey](https://github.com/tromey).

The team even went as far as putting in place an [ npm-based local development workflow](https://bugzilla.mozilla.org/show_bug.cgi?id=1291049#c150) so you can build the inspector, open it in a browser tab, make changes and see them in the browser by simply reloading the page!

Moving on to the **network panel**, thanks to the hard work of [Honza](https://twitter.com/janodvarko), [rickychien](https://github.com/RickyChien), [steveck](https://github.com/steveck-chung), [gasolin ](https://github.com/gasolin)and contributor [jsnajdr](https://twitter.com/jsnajdr), the panel has been almost entirely [cleaned of its XUL markup and migrated to React](https://bugzilla.mozilla.org/show_bug.cgi?id=1307743)! We now have a new and more modern code base that I’m sure will be very exciting for people to work with.

Speaking of the end of XUL, [tatumcreative](https://twitter.com/tatumcreative) eradicated a large piece of old code by [ re-writing the toolbox tabs using HTML and React](https://bugzilla.mozilla.org/show_bug.cgi?id=1245921).

## Inspector gets a refresh

A lot of work went into fixing “paper-cut” bugs – you know, those little (or not so little) annoyances that make it frustrating to use our UI.

A big thank you to [ochameau](https://github.com/ochameau) for making** the inspector a lot faster and more resilient** and to

[mikeratcliffe](https://twitter.com/ratcliffe_mike)for fixing many bugs of

[.](https://bugzilla.mozilla.org/show_bug.cgi?id=1315639)

**the inspector event tooltip**While I’m covering the inspector, let me mention some other noteworthy new features: [ css level 4 colors are now supported ](https://bugzilla.mozilla.org/show_bug.cgi?id=1310681)(thanks

[jerry](https://github.com/JerryShih)and

[tromey](https://github.com/tromey)), there are

[(thanks](https://bugzilla.mozilla.org/show_bug.cgi?id=1323193)

**visual hints between closing and opening tags**[juliandescottes](http://twitter.com/juliandescottes)),

**text nodes are highlighted**(

[juliandescottes](http://twitter.com/juliandescottes)again), and

[are easy to debug (thanks to](https://blog.nightly.mozilla.org/2016/10/17/devtools-now-display-white-space-text-nodes-in-the-dom-inspector/)

**whitespaces in inline layouts**[me](http://twitter.com/patrickbrosset)😀).

## Random but lovely

Our tools have became a little bit **better for RTL** ([right-to-left](https://en.wikipedia.org/wiki/Right-to-left)) users too, thanks to contributor [tomer](https://twitter.com/tomer).

[ Service worker’s statuses](https://bugzilla.mozilla.org/show_bug.cgi?id=1153292) are now visible in

`about:debugging`thanks to

[juliandescottes](http://twitter.com/juliandescottes).

[ The animation tooling can display easings](https://hacks.mozilla.org/2016/11/visualize-animations-easing-in-devtools/) thanks to

[daisuke](https://twitter.com/dadaaism)and

[birtles](https://twitter.com/brianskold).

**We’ve also written more React than ever before**. I’m very happy that our UI is converging towards one common style. Thank you [jlongster](https://twitter.com/jlongster) for showing us the way!

[mikeratcliffe](https://twitter.com/ratcliffe_mike) did a ton of work on **the storage inspector** too, so it works even better with IndexedDB, is able to delete cookies, and more.

## Looking ahead

In 2016 we also spent time planning for the future and in particular setting up for [ the new Performance Tool](https://github.com/firefox-devtools/perf.html) project.

A lot of talking and design work happened. We are now confident that we’ll be able ship an awesome performance tool that Firefox and web developers will love to use.

Thank you [jimb](https://twitter.com/jimblandy), [tatumcreative](https://twitter.com/tatumcreative), [ejpbruel](https://twitter.com/ejpbruel), [mstange](https://github.com/mstange).

Thanks to all who contributed to making DevTools better in 2016. Thank you to all the contributors who helped fix DevTools bugs. I could not mention them all here unfortunately.

Let’s have a great 2017 together!

Cheers,

Patrick

## About
[
Patrick Brosset ](http://patrickbrosset.com)

Patrick manages the DevTools engineering team at Mozilla

## 25 comments

jxnJanuary 31st, 2017 at 09:22Patrick BrossetFebruary 1st, 2017 at 01:27jxnFebruary 1st, 2017 at 08:52Patrick BrossetFebruary 2nd, 2017 at 00:21jxnFebruary 1st, 2017 at 08:54NoahJanuary 31st, 2017 at 12:54Patrick BrossetFebruary 1st, 2017 at 01:06LucaFebruary 1st, 2017 at 01:06LucaFebruary 1st, 2017 at 00:20Patrick BrossetFebruary 1st, 2017 at 01:03StephenFebruary 1st, 2017 at 04:00Patrick BrossetFebruary 1st, 2017 at 04:32HervéFebruary 1st, 2017 at 10:29Patrick BrossetFebruary 2nd, 2017 at 00:18Vanco OrdanoskiFebruary 2nd, 2017 at 09:21Patrick BrossetFebruary 6th, 2017 at 01:03newtonFebruary 2nd, 2017 at 09:27jasser kandumeFebruary 2nd, 2017 at 09:50Wellington TorrejaisFebruary 2nd, 2017 at 15:00Carm ScaffidiFebruary 5th, 2017 at 07:39Alexandre LeducFebruary 6th, 2017 at 06:20Robert KaiserFebruary 8th, 2017 at 16:04Patrick BrossetFebruary 9th, 2017 at 04:54John BilickiFebruary 10th, 2017 at 01:01Patrick BrossetFebruary 17th, 2017 at 02:10