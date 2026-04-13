---
title: 'CDN, BCD, and SVG: MDN Changelog for April 2018 – Mozilla Hacks - the Web
  developer blog'
url: https://hacks.mozilla.org/2018/05/cdn-bcd-and-svg-mdn-changelog-for-april-2018/
author: John Whitlock
published: '2018-05-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s note:** *A changelog is “a log or record of all notable changes made to a project. [It] usually includes records of changes such as bug fixes, new features, etc.” Publishing a changelog is kind of a tradition in open source, and a long-time practice on the web. We thought readers of Hacks and folks who use and contribute to MDN Web Docs would be interested in learning more about the work of the MDN engineering team, and the impact they have in a given month. We’ll also introduce code contribution opportunities, interesting projects, and new ways to participate.*

## Done in April

Here’s what happened in April to the [code, data, and tools](https://github.com/mdn/) that support [MDN Web Docs](https://developer.mozilla.org):

[Moved MDN to a CDN, improving page load time by 16%](https://hacks.mozilla.org#cdn-apr-18)[Migrated more compatibility data, now 72% complete](https://hacks.mozilla.org#bcd-apr-18)[Replaced font-based icons with inline SVG](https://hacks.mozilla.org#svg-apr-18)[Shipped tweaks and fixes](https://hacks.mozilla.org#tweaks-apr-18)by merging 510 pull requests, including 140 pull requests from 57 new contributors.

Here’s the plan for May:

On April 17, we switched [developer.mozilla.org](https://developer.mozilla.org) to be served by [CloudFront](https://aws.amazon.com/cloudfront/), Amazon’s Content Delivery Network (CDN). CDNs have several benefits, and MDN’s visitors are seeing many of them now.

A CDN has a network of servers around the world, and visitors connect to the closest CDN server. Our server connect time, which accounts for 10% of the page load time, has improved 57% world-wide, and 72% across Europe.

A CDN can request a page once from our web server, save a copy, and then serve the copy when a new visitor requests it. We’re starting with short, conservative caching times, but we’re already noticing that popular pages (including [a page](https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/So_you_just_built_Firefox) used in the Firefox build process) have faster load times because they are often served from the CDN directly. For example, we’ve measured a 50% improvement in page load time in India for the [JavaScript basics](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/JavaScript_basics) page.

We were already using a CDN for our static assets like JavaScript, CSS, and JS. Moving the main site to a CDN means we can serve static assets from developer.mozilla.org instead of an assets domain. This impacts site speed in two ways. First, the browser skips a second DNS lookup for the assets domain, saving 5% or so per view. Second, modern browsers can request the follow-on assets over the same HTTP/2 connection. [Stephanie Hobson](http://stephaniehobson.ca/) researched the impact of [HTTP/2 on MDN](http://stephaniehobson.ca/wordpress/2017/07/10/http2-on-mdn/) when we added it to the assets domain in 2017, and we implemented the follow-on work this month.

All of this adds up to a significant improvement in page load time. We’ve measured page load with [WebPageTest](http://www.webpagetest.org/), which provides reliable best-case metrics for the [homepage](https://developer.mozilla.org/en-US/):

| Location | Before the CDN | With the CDN | Improvement |
|---|---|---|---|
| Dulles, VA | 1.93s | 1.42s | 0.51s |
| Hong Kong, China | 2.68s | 1.79s | 0.89s |
| London, UK | 2.40s | 1.49s | 0.91s |
| Sydney, Australia | 2.68s | 1.63s | 1.05s |

We also use Google Analytics, which measures average page load for actual visitors across the site:

| Location | Before the CDN | With the CDN | Improvement |
|---|---|---|---|
| All MDN Visitors | 3.91s | 3.28s | 0.63s |
| USA | 2.44s | 2.11s | 0.33s |
| France | 3.03s | 2.29s | 0.74s |
| India | 6.05s | 4.45s | 1.60s |
| China | 7.87s | 5.60s | 2.27s |

Most of the preparation of the last few months was writing our CDN caching rules, to make sure that first-time visitors were likely to get a cached copy from the CDN, but that logged-in users, page editors, and translators continue talking directly to our web servers. A serious bug got past our initial testing, which caused problems for users editing MDN in multiple browser tabs. We fixed this bug ([PR 4757](https://github.com/mozilla/kuma/pull/4757)), and now editing is back to normal, and the site is still faster than it has ever been.

The community continues to migrate compatibility data from MDN to the [browser-compat-data repository](https://github.com/mdn/browser-compat-data). After a record 329 merged pull requests, the data is now 72% migrated, versus 63% at the start of April. Thanks to [Florian Scholz](https://github.com/Elchi3), [Mark Boas](https://github.com/maboa), [Daniel Beck](https://github.com/ddbeck), [ExE Boss](https://github.com/ExE-Boss), and many others for migrating data and reviewing PRs.

We learned about three projects using this data. The [polyfill-checker](https://github.com/instea/polyfill-checker) verifies that running code is using polyfills rather than built-ins, to ensure code runs the same on older browsers. [eslint-plugin-bultin-compat](https://github.com/instea/eslint-plugin-builtin-compat) does similar work using static analysis with [ESLint](http://eslint.org/). [MDN Browser Compatibility Data Explorer](https://mdn-compat-data-explorer.herokuapp.com) is a [Rails](http://rubyonrails.org) application for exploring the data, and includes feature search as well as summary graphs of browser support.

[Mark Dittmer](https://github.com/mdittmer) continued work on the [mdn-confluence tool](https://github.com/mdittmer/mdn-confluence). This tool generates potential compatibility data updates from the [Web API Confluence](https://web-confluence.appspot.com/#!/), which collects JavaScript API availability by testing browsers directly. The mdn-confluence tool has been integrated into the BCD development environment. Once the data migration is complete, our focus will shift to correcting and updating the data, and tools like this will be part of that process.

MDN has been using [Font Awesome](https://fontawesome.com/) for high-quality icons. One feature of font-based icons was strong support for Internet Explorer 7, which was still a priority in 2014 when we last updated our icon system. We’ve been updating our list of supported browsers, and in April [Schalk Neethling](https://github.com/schalkneethling) started the switch from font-based icons to inline SVG icons.

Both methods result in crisp icons that look good on high DPI displays. An icon font requires a network request to download the font file, either the standard version (which includes lots of icons we don’t use), or a minimized version (which we maintain and serve ourselves). With inline SVG, the browser gets the icon data with the initial HTML request, and doesn’t get any extra icons not used on the page. Inline SVG is also a better fit for our template system, making it clearer to developers what image is being used.

This work will continue in May, as we improve [accessibility](https://www.sitepoint.com/tips-accessible-svg/) and localization when using SVG icons. We will also remove code that supports the font-based icons, simplifying the CSS and JavaScript.

There were 510 PRs merged in April:

[329 mdn/browser-compat-data PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[77 mdn/interactive-examples PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[27 mozilla/kuma PRs](https://github.com/mozilla/kuma/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[24 mdn/kumascript PRs](https://github.com/mdn/kumascript/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[20 mdn/data PRs](https://github.com/mdn/data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[18 mdn/bob PRs](https://github.com/mdn/bob/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[5 mdn/mdn-fiori PRs](https://github.com/mdn/mdn-fiori/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[2 mdn/dom-examples PRs](https://github.com/mdn/dom-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[2 mdn/pwa-examples PRs](https://github.com/mdn/pwa-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[1 mdn/browser-compat-toolkit PR](https://github.com/mdn/browser-compat-toolkit/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[1 mdn/django-diy-blog PR](https://github.com/mdn/django-diy-blog/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[1 mdn/learning-area PR](https://github.com/mdn/learning-area/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[1 mdn/webextensions-examples PR](https://github.com/mdn/webextensions-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[1 mdn/viewsourceconf PR](https://github.com/mdn/viewsourceconf/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)[1 mdn/indexeddb-examples PR](https://github.com/mdn/indexeddb-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22)

140 of these were from first-time contributors:

- Add compat data for Web Storage API (
[BCD PR 1187](https://github.com/mdn/browser-compat-data/pull/1187)), from[Adam](https://github.com/avb100). - Add compat data for Presentation (
[BCD PR 1249](https://github.com/mdn/browser-compat-data/pull/1249)), from[Lars Bärtschi](https://github.com/LarsBaertschi). - Adding compat data for SVGAnimatedInteger (
[PR 1310](https://github.com/mdn/browser-compat-data/pull/1310)), Adding compat data for SVGAnimatedLength ([PR 1773](https://github.com/mdn/browser-compat-data/pull/1773)), and[21 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22+author:flashyincceo)to BCD from[Peter Folkins](https://github.com/flashyincceo). - Update Chrome/Firefox support for ReadableStream in Request Body (
[BCD PR 1333](https://github.com/mdn/browser-compat-data/pull/1333)), from[AnthumChris](https://github.com/AnthumChris). - Add: Functional syntax with floats value notations (
[PR 1342](https://github.com/mdn/browser-compat-data/pull/1342)), and New: add calc() values in grid-gap(gutter properties) ([PR 1378](https://github.com/mdn/browser-compat-data/pull/1378)), from[一丝](https://github.com/yisibl)(first contributions to BCD). - Add compat data for Bluetooth Web API (
[BCD PR 1385](https://github.com/mdn/browser-compat-data/pull/1385)), from[Brian Pierce](https://github.com/theCalibrius). - HTMLEmbedElement (
[PR 1399](https://github.com/mdn/browser-compat-data/pull/1399)), Add compat data for HTMLFontElement ([PR 1436](https://github.com/mdn/browser-compat-data/pull/1436)), and[6 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22+author:jmswisher)to BCD from[Janet Swisher](https://github.com/jmswisher). - Add compat data for CSSConditionRule (
[PR 1569](https://github.com/mdn/browser-compat-data/pull/1569)), Add compat data for CSSCounterStyleRule ([PR 1571](https://github.com/mdn/browser-compat-data/pull/1571)), and[5 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22+author:jwalvies)to BCD from[James W. Alvies](https://github.com/jwalvies). - Add compat data for CompositionEvent (
[BCD PR 1676](https://github.com/mdn/browser-compat-data/pull/1676)), from[Karl Stolley](https://github.com/karlstolley). - Add BeforeUnloadEvent (
[BCD PR 1696](https://github.com/mdn/browser-compat-data/pull/1696)), from[Kayce Basques](https://github.com/kaycebasques). - Fix Chrome/Opera versions for RTCPeerConnection.getSenders (
[PR 1713](https://github.com/mdn/browser-compat-data/pull/1713)), and Fix Chrome/Opera versions for RTCPeerConnection.getReceivers ([PR 1714](https://github.com/mdn/browser-compat-data/pull/1714)), to BCD from[Jeremy Lainé](https://github.com/jlaine). - Update SyncManager.json (
[BCD PR 1716](https://github.com/mdn/browser-compat-data/pull/1716)), from[Isaac Kwan](https://github.com/isaackwan). - Add alternative names to
`fullscreenElement`

([BCD PR 1724](https://github.com/mdn/browser-compat-data/pull/1724)), from[timm-gs](https://github.com/timm-gs). - Update Safari data for AbortController (
[PR 1729](https://github.com/mdn/browser-compat-data/pull/1729)), and Update Safari data for AbortSignal ([PR 1730](https://github.com/mdn/browser-compat-data/pull/1730)), to BCD from[mata007](https://github.com/mata007). - Firefox does not support transceiver.setCodecPreferences() (
[BCD PR 1735](https://github.com/mdn/browser-compat-data/pull/1735)), from[jan-ivar](https://github.com/jan-ivar). - Add compat data for Comment (
[BCD PR 1736](https://github.com/mdn/browser-compat-data/pull/1736)), from[katzrkool](https://github.com/katzrkool). - Update nodejs compat for javascript.function.rest_parameters (
[BCD PR 1744](https://github.com/mdn/browser-compat-data/pull/1744)), from[Charles Samborski](https://github.com/demurgos). - Add -webkit-progress-* psuedo-selectors (
[PR 1748](https://github.com/mdn/browser-compat-data/pull/1748)), Add -webkit-meter-* selectors ([PR 1749](https://github.com/mdn/browser-compat-data/pull/1749)), and[3 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22+author:connorshea)to BCD from[Connor Shea](https://github.com/connorshea). - Web APIs: add HashChangeEvent (
[PR 1759](https://github.com/mdn/browser-compat-data/pull/1759)), Web APIs: add CaretPosition ([PR 1765](https://github.com/mdn/browser-compat-data/pull/1765)), and[2 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22+author:caugner)to BCD from[Claas Augner](https://github.com/caugner). - Update compat data for css.selectors.marker (
[BCD PR 1775](https://github.com/mdn/browser-compat-data/pull/1775)), from[Martin Schneider](https://github.com/MA-Maddin). - Add missing colon to alternative selectors (
[PR 1778](https://github.com/mdn/browser-compat-data/pull/1778)), Correct alternatives for`border-radius`

longhand properties ([PR 1895](https://github.com/mdn/browser-compat-data/pull/1895)), and[2 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22+author:frenic)to BCD from[Fredrik Nicol](https://github.com/frenic). - Add compat data for string substitution support in IE (
[BCD PR 1780](https://github.com/mdn/browser-compat-data/pull/1780)), from[Steven Goris](https://github.com/GoGoris). - Correct Opera compat for summary and details elements. (
[PR 1786](https://github.com/mdn/browser-compat-data/pull/1786)), and Fix(api.Node.getRootNode): Fix IE/Edge compat ([PR 1833](https://github.com/mdn/browser-compat-data/pull/1833)), to BCD from[Ryan Johnson](https://github.com/CITguy). - Fix IE compatibility version for overrideMimeType (
[BCD PR 1792](https://github.com/mdn/browser-compat-data/pull/1792)), from[Marie P-W](https://github.com/mariepw). - Transfer of data for Web/API/Element/matches (
[BCD PR 1801](https://github.com/mdn/browser-compat-data/pull/1801)), from[Maarten Brouwers](https://github.com/murb). - nth-child and nth-last-child support data update (
[BCD PR 1805](https://github.com/mdn/browser-compat-data/pull/1805)), from[SelenIT](https://github.com/SelenIT). - Fix <legend> IE compat data (
[BCD PR 1821](https://github.com/mdn/browser-compat-data/pull/1821)), from[Shaun Dillon](https://github.com/shaundillon). - Fix incorrect URL for URL.searchParams (
[BCD PR 1828](https://github.com/mdn/browser-compat-data/pull/1828)), from[Zack Harley](https://github.com/zackharley). - Update Edge support for WebAssembly streaming API (
[BCD PR 1829](https://github.com/mdn/browser-compat-data/pull/1829)), from[Michael Ferris](https://github.com/Cellule). - Chrome supports filter attribute on SVG (
[BCD PR 1870](https://github.com/mdn/browser-compat-data/pull/1870)), from[ypnos-web](https://github.com/ypnos-web). - Update CSS Shapes data (
[PR 1871](https://github.com/mdn/browser-compat-data/pull/1871)), from[Rachel Andrew](https://github.com/rachelandrew)(first contribution to BCD). - Add font element compat data according Caniuse. (
[BCD PR 1880](https://github.com/mdn/browser-compat-data/pull/1880)), from[Michal Čaplygin](https://github.com/myfonj). - Update/data channel edge safari (
[BCD PR 1940](https://github.com/mdn/browser-compat-data/pull/1940)), from[Brian Peiris](https://github.com/brianpeiris). - More illustrative example for font-synthesis (
[Interactive Examples PR 715](https://github.com/mdn/interactive-examples/pull/715)), from[Chen Hui Jing](https://github.com/huijing). - Remove hard-coded ‘height’ (
[Interactive Examples PR 724](https://github.com/mdn/interactive-examples/pull/724)), from[Mats Palmgren](https://github.com/MatsPalmgren). - Add <kbd> example (
[PR 756](https://github.com/mdn/interactive-examples/pull/756)), Add <mark> example ([PR 775](https://github.com/mdn/interactive-examples/pull/775)), and[10 more PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22+author:Elchi3)from[Florian Scholz](https://github.com/Elchi3)(first contributions to Interactive Examples). - Issue #730 – Content Sectioning – header (
[PR 789](https://github.com/mdn/interactive-examples/pull/789)), Add interactive example for dl element ([PR 826](https://github.com/mdn/interactive-examples/pull/826)), and[2 more PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22+author:a2sheppy)from[Eric Shepherd](https://github.com/a2sheppy)(first contributions to Interactive Examples). - Add <footer> example (
[PR 804](https://github.com/mdn/interactive-examples/pull/804)), Add <del> example ([PR 844](https://github.com/mdn/interactive-examples/pull/844)), and[2 more PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22+author:2alin)from[Adilson Sandoval](https://github.com/2alin)(first contributions to Interactive Examples). - Configure Renovate (
[Interactive Examples PR 850](https://github.com/mdn/interactive-examples/pull/850)), from[renovate[bot]](https://github.com/renovate%5Bbot%5D). - Only preload .woff2 font files (
[Kuma PR 4728](https://github.com/mozilla/kuma/pull/4728)), from[Alex Gibson](https://github.com/alexgibson). - Update jinja and django-jinja (
[Kuma PR 4747](https://github.com/mozilla/kuma/pull/4747)), from[Mohammed Ali Zubair](https://github.com/Alig1493). - Add Japanese titles to LearnSideBar (
[KumaScript PR 638](https://github.com/mdn/kumascript/pull/638)), from[T. Uemura](https://github.com/Uemmra3). - Update L10n-Common.json (
[KumaScript PR 644](https://github.com/mdn/kumascript/pull/644)), from[sigoa](https://github.com/sigoa). - Add and update Simplified Chinese (zh-CN) translation (
[KumaScript PR 648](https://github.com/mdn/kumascript/pull/648)), from[佛壁灯](https://github.com/f0rb1d). - Add Brazil Portuguese translation (pt-BR) in L10nStatusOverview.ejs (
[KumaScript PR 661](https://github.com/mdn/kumascript/pull/661)), from[Matheus Cuba](https://github.com/MatheusMCuba). - Add pt-BR localized texts for LearnSidebar macro (
[PR 663](https://github.com/mdn/kumascript/pull/663)), and Add pt-BR translations ([PR 664](https://github.com/mdn/kumascript/pull/664)), to KumaScript from[Giorgio](https://github.com/GPrimola). - Provide tests for cssxref (
[PR 684](https://github.com/mdn/kumascript/pull/684)), and Provide tests for svginfo ([PR 690](https://github.com/mdn/kumascript/pull/690)), from[Jeremie Patonnier](https://github.com/JeremiePat)(first contributions to KumaScript). - Check if selector exists in selectors.json (
[KumaScript PR 687](https://github.com/mdn/kumascript/pull/687)), from[Kasper Christensen](https://github.com/fALKENdk). - Fix ES8/ES2017 Links in SpecData (
[KumaScript PR 688](https://github.com/mdn/kumascript/pull/688)), from[choeun](https://github.com/techhtml). - Add justify-self CSS property (
[PR 184](https://github.com/mdn/data/pull/184)), Add justify-items CSS property ([PR 185](https://github.com/mdn/data/pull/185)), and[5 more PRs](https://github.com/mdn/data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22+author:pkuczynski)to Data from[Piotr Kuczynski](https://github.com/pkuczynski). - Add
`clip`

keyword to overflow[-(x|y)] ([PR 202](https://github.com/mdn/data/pull/202)), Add missing keywords`recto`

and`verso`

to page-break-(after|before) ([PR 203](https://github.com/mdn/data/pull/203)), and[4 more PRs](https://github.com/mdn/data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-04-01..2018-04-30%22+author:frenic)to Data from[Fredrik Nicol](https://github.com/frenic). - Mark image-resolution as experimental. Fix #214 (
[PR 215](https://github.com/mdn/data/pull/215)), and Mark ruby properties as experimental. Fix #216 ([PR 217](https://github.com/mdn/data/pull/217)), to Data from[Pine](https://github.com/octref). - Configure Renovate (
[bob PR 26](https://github.com/mdn/bob/pull/26)), from[renovate[bot]](https://github.com/renovate%5Bbot%5D). - Update baseURL to point to MDN GitHub (
[mdn-fiori PR 6](https://github.com/mdn/mdn-fiori/pull/6)), from[Stephen Coogan](https://github.com/coogie). - Fix outdated
`mdn-browser-compat-data`

dependency ([PR 4](https://github.com/mdn/browser-compat-toolkit/pull/4)), from[ExE Boss](https://github.com/ExE-Boss)(first contribution to browser-compat-toolkit). - Update admin.py (
[django-diy-blog PR 5](https://github.com/mdn/django-diy-blog/pull/5)), from[Özgür](https://github.com/ozgurturkiye). - Update text-start.html (typo – capitalization) (
[learning-area PR 68](https://github.com/mdn/learning-area/pull/68)), from[Matt Buckley](https://github.com/mbuc). - Fix end tag in HTML fragment. (
[webextensions-examples PR 355](https://github.com/mdn/webextensions-examples/pull/355)), from[Daniel Dawson](https://github.com/ddawson). - Remove registration code for 404 service worker (
[viewsourceconf PR 239](https://github.com/mdn/viewsourceconf/pull/239)), from[Alex Gibson](https://github.com/alexgibson). - Filter by rating (
[indexeddb-examples PR 1](https://github.com/mdn/indexeddb-examples/pull/1)), from[matthewchao](https://github.com/matthewchao).

Other significant PRs:

- Big ol’ PR to populate a lot of Samsung Internet data. (
[BCD PR 1606](https://github.com/mdn/browser-compat-data/pull/1606)), from[Ada Rose Cannon](https://github.com/AdaRoseCannon). - Disallow additional properties in release_statement (
[BCD PR 1790](https://github.com/mdn/browser-compat-data/pull/1790)), from[Florian Scholz](https://github.com/Elchi3). - Make
`prefix`

and`alternative_name`

mutually exclusive ([BCD PR 1836](https://github.com/mdn/browser-compat-data/pull/1836)), from[ExE Boss](https://github.com/ExE-Boss). - Add hreflang for the current document (
[Kuma PR 4745](https://github.com/mozilla/kuma/pull/4745)), from[Maton Anthony](https://github.com/MatonAnthony). - Add tests to avoid division by zero (
[KumaScript PR 665](https://github.com/mdn/kumascript/pull/665)), from[Clément](https://github.com/Porkepix). - Add some missing items to selectors.json. (
[Data PR 198](https://github.com/mdn/data/pull/198)), from[Joe Medley](https://github.com/jpmedley).

## Planned for May

MDN staff and volunteers are writing HTML interactive examples, such as [a demonstration of <datalist>](https://interactive-examples.mdn.mozilla.net/pages/tabbed/datalist.html). This adds to the JavaScript and CSS examples, and will complete the first phase of the interactive examples project. There’s [a bug](https://github.com/mdn/interactive-examples/issues/706) that’s preventing publishing the HTML examples that will be fixed in May, and then these new examples can be published to MDN.

If you’d like to help write HTML examples, please see the [call for help](https://discourse.mozilla.org/t/html-interactive-examples-help-wanted/27966) on Discourse.

The work for Django 1.11 continued in April, but the CDN took more effort than expected. We’ll continue work on the Django upgrade, and should deploy it in May.

## About John Whitlock

John is a web developer working on the engine of MDN Web Docs