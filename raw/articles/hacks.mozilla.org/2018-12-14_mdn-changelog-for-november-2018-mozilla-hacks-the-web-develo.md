---
title: MDN Changelog for November 2018 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/12/mdn-changelog-for-november-2018/
author: John Whitlock
published: '2018-12-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Done in November

Here’s what happened in November to the [code, data, and tools](https://github.com/mdn/) that support [MDN Web Docs](https://developer.mozilla.org):

[Shipped monthly MDN Payments](https://hacks.mozilla.org#shipped-monthly-mdn-payments)[Converted from Font Awesome to SVG](https://hacks.mozilla.org#converted-from-font-awesome-to-svg)[Added browser names to compatibility tables](https://hacks.mozilla.org#added-browser-names-to-compatibility-tables)[Welcomed David Flanagan](https://hacks.mozilla.org#welcome-david-flanagan)[Shipped tweaks and fixes](https://hacks.mozilla.org#shipped-tweaks-and-fixes)by merging 248 pull requests, including 35 pull requests from 30 new contributors.

Here’s the plan for December:

### Shipped monthly MDN payments

In September we [launched MDN payments](https://hacks.mozilla.org/2018/10/payments-accessibility-and-dead-macros-mdn-changelog-for-september-2018/#launched-mdn-payments), giving MDN fans [a new way to help MDN grow](https://hacks.mozilla.org/2018/10/a-new-way-to-support-mdn/). On November 20th, we added the ability to [schedule monthly payments](https://developer.mozilla.org/en-US/payments/recurring).

[Potato London](https://p.ota.to/) started work on this shortly after one-time payments launched. We kicked it off with a design meeting where we determined the features that could be delivered in 4 weeks. Potato and MDN worked closely to remove blockers, review code (in over 25 pull requests), and get it into the staging environment for testing. Thanks to everyone’s hard work, we launched a high-quality feature on schedule.

We’ve learned a lot from these payment experiments, and we’ll continue to find ways to maintain MDN’s growth in 2019.

### Converted from Font Awesome to SVG

On November 6th, we deployed [Schalk Neethling’s](https://github.com/schalkneethling) [PR 5058](https://github.com/mozilla/kuma/pull/5058), completing the transition from the FontAwesome webfont to inline SVG icons. There are a few icon and style changes, but the site should look the same to most users.

We had [several reasons](https://bugzilla.mozilla.org/show_bug.cgi?id=1451261#c0) for this change in April, when Schalk started the project. The biggest gains were expected to be in performance and a simpler design. Over the year, we became aware that many content blockers prevent loading web fonts, and many users couldn’t see UIs that depended on icons. For example, the browser compatibility tables [were unusable on mobile](https://bugzilla.mozilla.org/show_bug.cgi?id=1480106) with [Firefox Focus](https://www.mozilla.org/en-US/firefox/mobile/). This change fixes this issue.

We haven’t seen a significant performance improvement, although there may have been small improvements as this switch was rolled out over the year. This month, we explored some more radical changes, such as minimal styling and disabled JS, by shipping manually edited copies of wiki pages. These experiments will help us determine the highest impact changes for front-end performance, and provide insight into what areas to explore next.

### Added browser names to compatibility tables

The new SVG icons are being used in the browser compatibility table. In the wider desktop view, we’ve added rotated browser labels ([Kuma PR 5117](https://github.com/mozilla/kuma/pull/5117) and [KumaScript PR 997](https://github.com/mdn/kumascript/pull/997)), so it is clearer which browser is which. We also launched a survey to ask visitors about their needs for compatibility data ([Kuma PR 5133](https://github.com/mozilla/kuma/pull/5133)).

The compatibility data continues to be released as [an NPM package](https://www.npmjs.com/package/mdn-browser-compat-data), and now [a tagged release](https://github.com/mdn/browser-compat-data/releases) is also created, including the statistics and notable changes from the last release ([BCD PR 3158](https://github.com/mdn/browser-compat-data/pull/3158)).

### Welcome David Flanagan

[David Flanagan](https://github.com/davidflanagan) joined the MDN development team in November. David is the author of [JavaScript: The Definitive Guide](http://shop.oreilly.com/product/9780596101992.do) and [several other books](https://www.oreilly.com/pub/au/156). He is a former Mozilla employee, and recently worked at [Khan Academy](https://www.khanacademy.org/). His skills and passions are a great fit for MDN’s mission, and we look forward to his help as we modernize and expand our tech stack. Welcome David!

### Shipped tweaks and fixes

There were 248 PRs merged in November:

[74 mozilla/kuma PRs](https://github.com/mozilla/kuma/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[59 mdn/browser-compat-data PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[34 mdn/kumascript PRs](https://github.com/mdn/kumascript/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[21 mdn/interactive-examples PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[19 mdn/infra PRs](https://github.com/mdn/infra/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[12 mdn/bob PRs](https://github.com/mdn/bob/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[11 mdn/data PRs](https://github.com/mdn/data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[3 mdn/dom-examples PRs](https://github.com/mdn/dom-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[2 mdn/django-locallibrary-tutorial PRs](https://github.com/mdn/django-locallibrary-tutorial/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[2 mdn/web-speech-api PRs](https://github.com/mdn/web-speech-api/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[2 mdn/stumptown-experiment PRs](https://github.com/mdn/stumptown-experiment/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[2 mdn/short-descriptions PRs](https://github.com/mdn/short-descriptions/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[1 mdn/fetch-examples PR](https://github.com/mdn/fetch-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[1 mdn/web-components-examples PR](https://github.com/mdn/web-components-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[1 mdn/learning-area PR](https://github.com/mdn/learning-area/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[1 mdn/simple-web-worker PR](https://github.com/mdn/simple-web-worker/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[1 mdn/crossbrowser-testing-lab PR](https://github.com/mdn/crossbrowser-testing-lab/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[1 mdn/css-examples PR](https://github.com/mdn/css-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")[1 mdn/imsc PR](https://github.com/mdn/imsc/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-11-01..2018-11-30")

This includes some important changes and fixes:

- Add ARIA roles to notes and warning boxes inside CKEditor (
[Kuma PR 5069](https://github.com/mozilla/kuma/pull/5069)), from[Schalk Neethling](https://github.com/schalkneethling). - More migration from Python 2 to Python 2/3 (
[Kuma PR 5071](https://github.com/mozilla/kuma/pull/5071)), from[Anthony Maton](https://github.com/MatonAnthony). - Prefer
`.blockIndicator`

for styling note and warning boxes ([Kuma PR 5079](https://github.com/mozilla/kuma/pull/5079)), from[ExE Boss](https://github.com/ExE-Boss). - Improve functional tests (
[Kuma PR 5143](https://github.com/mozilla/kuma/pull/5143)), from[Ryan Johnson](https://github.com/escattone). - Fix deployments by fixing issue with the Jenkins build step (
[Interactive Examples PR 1229](https://github.com/mdn/interactive-examples/pull/1229)), from[Ryan Johnson](https://github.com/escattone). - Enforce CSP in staging (
[infra PR 157](https://github.com/mdn/infra/pull/157)), from[me](https://github.com/jwhitlock).

35 pull requests were from first-time contributors:

- Support sticky table of contents on Safari (
[Kuma PR 5113](https://github.com/mozilla/kuma/pull/5113)), from[Anthony Ricaud](https://github.com/rik). - Upgrade clean-css to version 4.x (
[PR 5135](https://github.com/mozilla/kuma/pull/5135)), and Stop adding the SEO root title to all document titles ([PR 5142](https://github.com/mozilla/kuma/pull/5142)), to Kuma from[David Flanagan](https://github.com/davidflanagan). - Add
`intrinsicsize`

to HTML Media elements (`img`

,`video`

) ([PR 2979](https://github.com/mdn/browser-compat-data/pull/2979)), from[ZaneHannanAU](https://github.com/ZaneHannanAU)(first contribution to BCD). - Update browser compatibility for rest properties in objects (
[BCD PR 3038](https://github.com/mdn/browser-compat-data/pull/3038)), from[FichteFoll](https://github.com/FichteFoll). - Update
`insertRule`

optional`index`

compatibility for IE and FF ([BCD PR 3039](https://github.com/mdn/browser-compat-data/pull/3039)), from[Tim](https://github.com/timothympace). - Add compatibility for
`FullScreen`

API on IE11 ([BCD PR 3040](https://github.com/mdn/browser-compat-data/pull/3040)), from[CntChen](https://github.com/CntChen). - Fix tag escaping in Edge note for
`FileSystem`

API ([BCD PR 3043](https://github.com/mdn/browser-compat-data/pull/3043)), from[Ryusei YAMAGUCHI](https://github.com/mandel59). - Add
`object-fit`

and`object-position`

Safari Support Details ([BCD PR 3045](https://github.com/mdn/browser-compat-data/pull/3045)), from[Holt Johnson](https://github.com/holtjohnson). - Add support data for the
`signal`

feature from the`AbortController`

API ([PR 3048](https://github.com/mdn/browser-compat-data/pull/3048)), from[Konstantin Rouda](https://github.com/Konrud)(first contribution to BCD). - Update Firefox compatibility for
`Window.event`

([BCD PR 3057](https://github.com/mdn/browser-compat-data/pull/3057)), from[Matthieu Riegler](https://github.com/kyro38). - Update
`aspect-ratio`

for Safari on iOS ([BCD PR 3066](https://github.com/mdn/browser-compat-data/pull/3066)), from[Eric Celeste](https://github.com/efc). - Add and rename image directives of Feature Policy (
[BCD PR 3095](https://github.com/mdn/browser-compat-data/pull/3095)), from[Jason Chase](https://github.com/jpchase). - Add support for
`<meter>`

in iOS Safari 10.3 ([BCD PR 3109](https://github.com/mdn/browser-compat-data/pull/3109)), from[Sven Wolfermann](https://github.com/maddesigns). - Update “Tracking Preference Expression (DNT)” Editor’s draft URL (
[KumaScript PR 805](https://github.com/mdn/kumascript/pull/805)), from[Vivien Lacourba](https://github.com/vivienlacourba). - Change WebDriver to Living specification (
[PR 930](https://github.com/mdn/kumascript/pull/930)), from[Andreas Tolfsen](https://github.com/andreastt)(first contribution to KumaScript). - Add Spanish support to
`Glossary`

macro ([KumaScript PR 968](https://github.com/mdn/kumascript/pull/968)), from[Joaquín Serna](https://github.com/BubuAnabelas). - Update French string in
`SeeCompatTable`

([KumaScript PR 975](https://github.com/mdn/kumascript/pull/975)), from[lp177](https://github.com/lp177). - Convert
`<audio>`

example to valid and more semantic HTML ([PR 1236](https://github.com/mdn/interactive-examples/pull/1236)), from[Karl Stolley](https://github.com/karlstolley)(first contribution to Interactive Examples). - Add
`grid-area`

label indicators to`div`

content ([Interactive Examples PR 1248](https://github.com/mdn/interactive-examples/pull/1248)), from[Liz Lawley](https://github.com/mamamusings). - Fix
`-webkit-overflow-scrolling`

inheritance ([Data PR 331](https://github.com/mdn/data/pull/331)), from[Timothy Liang](https://github.com/timothy003). - Add chroma keying example (
[PR 29](https://github.com/mdn/dom-examples/pull/29)), Add web crypto examples ([PR 30](https://github.com/mdn/dom-examples/pull/30)), and Remove web crypto examples ([PR 31](https://github.com/mdn/dom-examples/pull/31)), from[wbamberg](https://github.com/wbamberg)(first contributions to dom-examples). - Fix indenting of
`display_genre.short_description = 'Genre'`

([django-locallibrary-tutorial PR 33](https://github.com/mdn/django-locallibrary-tutorial/pull/33)), from[AlekseiMarinichenko](https://github.com/AlekseiMarinichenko). - Convert
`speechResult`

to lowercase to fix phrase matching ([web-speech-api PR 29](https://github.com/mdn/web-speech-api/pull/29)), from[Hartmut Bohnacker](https://github.com/bohnacker). - In the synthesis demo, list the voices into alphabetical order (ignoring case) (
[web-speech-api PR 30](https://github.com/mdn/web-speech-api/pull/30)), from[Chris Chittleborough](https://github.com/c12h). - Add recipes (
[PR 1](https://github.com/mdn/stumptown-experiment/pull/1)), and Add CSS property transform ([PR 3](https://github.com/mdn/stumptown-experiment/pull/3)), from[wbamberg](https://github.com/wbamberg)(first contributions to stumptown-experiment). - Add error handling to multiple fetch examples (
[fetch-examples PR 13](https://github.com/mdn/fetch-examples/pull/13)), from[T.J. Crowder](https://github.com/tjcrowder). - Simplify
`editable-list`

example ([web-components-examples PR 13](https://github.com/mdn/web-components-examples/pull/13)), from[liuxuewei](https://github.com/liuxuewei). - Add
`auto`

to`flex`

to match Firefox’s wrapping in Safari and Chrome ([learning-area PR 108](https://github.com/mdn/learning-area/pull/108)), from[stefsulzer](https://github.com/stefsulzer). - Vary console messages to distinguish between handlers (
[simple-web-worker PR 10](https://github.com/mdn/simple-web-worker/pull/10)), from[Bharath Bhushan Lohray](https://github.com/lordloh). - Update README to reference MDN docs (
[crossbrowser-testing-lab PR 1](https://github.com/mdn/crossbrowser-testing-lab/pull/1)), from[James Thompson](https://github.com/100stacks). - Add grid wrapper example to CSS Layout Cookbook (
[css-examples PR 12](https://github.com/mdn/css-examples/pull/12)), from[Michelle Barker](https://github.com/mbarker84).

## Planned for December

### Meet in Orlando

Twice a year, all of Mozilla comes together for an All-Hands meeting. This winter’s All-Hands is in [Orlando, Florida](https://wiki.mozilla.org/All_Hands/Orlando2018). We were in Orlando in December 2015, when Florian was proposing [moving KumaScript macros to GitHub](https://groups.google.com/forum/#!topic/mozilla.dev.mdn/PEuH7WW2Xtk) and I was deploying the [BrowserCompat API](https://github.com/mdn/browsercompat/blob/master/HISTORY.rst) to beta users. A lot changes in three years!

Many of us at MDN will be taking well-deserved breaks after the All-Hands, and will come back refreshed for 2019. We hope you and yours have an enjoyable winter break!

## About John Whitlock

John is a web developer working on the engine of MDN Web Docs