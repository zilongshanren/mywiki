---
title: MDN Changelog – Looking back at 2018 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/01/mdn-changelog-looking-back-at-2018/
author: John Whitlock
published: '2019-01-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

December is when Mozilla meets as a company for our biannual All-Hands, and we reflect on the past year and plan for the future. Here are some of the highlights of 2018.

The [browser-compat-data](https://github.com/mdn/browser-compat-data) (BCD) project required a sustained effort to convert MDN’s documentation to structured data. The conversion was 39% complete at the start of 2018, and ended the year at 98% complete. [Florian Scholz](https://github.com/Elchi3) coordinated a large community of staff and volunteers, breaking up the work into human-sized chunks that could be done in parallel. The community converted, verified, and refreshed the data, and converted thousands of MDN pages to use the new data sources. Volunteers also built tools and integrations on top of the data.

The [interactive-examples project](https://github.com/mdn/interactive-examples/) had a great year as well. [Will Bamberg](https://github.com/wbamberg) coordinated the work, including some all-staff efforts to write new examples. [Schalk Neethling](https://github.com/schalkneethling) improved the platform as it grew to handle CSS, JavaScript, and HTML examples.

In 2018, MDN developers moved from MozMEAO to Developer Outreach, joining the content staff in Emerging Technologies. The organizational change in March was followed by a nine-month effort to move the servers to the new ET account. [Ryan Johnson](https://github.com/escattone), [Ed Lim](https://github.com/limed), and [Dave Parfitt](https://github.com/metadave) completed the smoothest server transition in MDN’s history.

The strength of MDN is our documentation of fundamental web technologies. Under the leadership of [Chris Mills](https://github.com/chrisdavidmills), this content was maintained, improved, and expanded in 2018. It’s a lot of work to keep an institution running and growing, and there are few opportunities to properly celebrate that work. Thanks to [Daniel Beck](https://github.com/ddbeck/), [Eric Shepherd](https://github.com/a2sheppy), [Estelle Weyl](https://github.com/estelle), [Irene Smith](https://github.com/irenesmith), [Janet Swisher](https://github.com/jmswisher), [Rachel Andrew](https://github.com/rachelandrew), and our community of partners and volunteers for keeping MDN awesome in 2018.

[Kadir Topal](https://github.com/atopal) led the rapid development of the [payments project](https://developer.mozilla.org/en-US/payments/). We’re grateful to all the MDN readers who are supporting the maintenance and growth of MDN.

There’s a lot more that happened in 2018:

[January](https://mozilla.github.io/meao/2018/02/07/mdn-changelog/)– Added a language preference dialog, and added rate limiting.[February](https://mozilla.github.io/meao/2018/03/08/mdn-changelog/)– Prepared to move developers to Emerging Technologies.[March](https://hacks.mozilla.org/2018/04/mdn-changelog-for-march-2018/)– Ran a Hack on MDN event for BCD, and tried Brotli.[April](https://hacks.mozilla.org/2018/05/cdn-bcd-and-svg-mdn-changelog-for-april-2018)– Moved MDN to a CDN, and started switching to SVG.[May](https://hacks.mozilla.org/2018/06/media-mathml-and-django-1-11-mdn-changelog-for-may-2018/)– Moved to ZenHub.[June](https://hacks.mozilla.org/2018/07/mdn-changelog-for-june-2018/)– Shipped Django 1.11.[July](https://hacks.mozilla.org/2018/08/mdn-changelog-for-july-2018-cdn-tests-goodbye-zones-and-bcd/)– Decommissioned zones, and tried new CDN experiments.[August](https://hacks.mozilla.org/2018/09/mdn-changelog-for-august-2018/)– Started performance improvements, added section links, removed memcache from Kuma, and upgraded to ElasticSearch 5.[September](https://hacks.mozilla.org/2018/10/payments-accessibility-and-dead-macros-mdn-changelog-for-september-2018/)– Ran a Hack on MDN event for accessibility, and deleted 15% of macros.[October](https://hacks.mozilla.org/2018/11/performance-and-hosting-moves-mdn-changelog-for-october-2018/)– Completed the server migration, and shipped some performance improvements.[November](https://hacks.mozilla.org/2018/12/mdn-changelog-for-november-2018/)– Completed the migration to SVG, and updated the compatibility table header rows.

There were 124 PRs merged in December, including 27 pull requests from 26 new contributors:

[65 mdn/browser-compat-data PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-12-01..2018-12-31")[22 mozilla/kuma PRs](https://github.com/mozilla/kuma/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-12-01..2018-12-31")[20 mdn/interactive-examples PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-12-01..2018-12-31")[4 mdn/bob PRs](https://github.com/mdn/bob/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-12-01..2018-12-31")[3 mdn/data PRs](https://github.com/mdn/data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-12-01..2018-12-31")[2 mdn/infra PRs](https://github.com/mdn/infra/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-12-01..2018-12-31")[2 mdn/learning-area PRs](https://github.com/mdn/learning-area/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-12-01..2018-12-31")[2 mdn/kumascript PRs](https://github.com/mdn/kumascript/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-12-01..2018-12-31")[1 mdn/dom-examples PR](https://github.com/mdn/dom-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-12-01..2018-12-31")[1 mdn/stumptown-experiment PR](https://github.com/mdn/stumptown-experiment/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-12-01..2018-12-31")[1 mdn/html-examples PR](https://github.com/mdn/html-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-12-01..2018-12-31")[1 mdn/short-descriptions PR](https://github.com/mdn/short-descriptions/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-12-01..2018-12-31")

This includes some important changes and fixes:

- Add the Accessibility Checker plugin to CKEditor (
[Kuma PR 4989](https://github.com/mozilla/kuma/pull/4989)), from[Florian Scholz](https://github.com/Elchi3). - Add
`Jest`

and`True`

, and initial tests ([Kuma PR 5162](https://github.com/mozilla/kuma/pull/5162)), from[Schalk Neethling](https://github.com/schalkneethling). - Fix
`test_footer_language_selector`

test ([Kuma PR 5163](https://github.com/mozilla/kuma/pull/5163)), and Fix`test_header_signin`

and`test_edit_sign_in`

([Kuma PR 5166](https://github.com/mozilla/kuma/pull/5166)), from[Ryan Johnson](https://github.com/escattone), part of the successful effort to get acceptance tests working reliably again. - Add conic gradient examples (
[Interactive Examples PR 1265](https://github.com/mdn/interactive-examples/pull/1265)), from[Estelle Weyl](https://github.com/estelle).

27 pull requests were from first-time contributors:

- Add compatibility data for the SVG
`paint-order`

attribute ([PR 3074](https://github.com/mdn/browser-compat-data/pull/3074)), and Fix SVG`text`

MDN URLs, and`textLength`

IE support ([PR 3098](https://github.com/mdn/browser-compat-data/pull/3098)), to BCD from[Steven Kalt](https://github.com/SKalt). - Add Edge support for
`lastElementChild`

element of`ParentNode`

([BCD PR 3099](https://github.com/mdn/browser-compat-data/pull/3099)), from[Andrew Stewart Gibson](https://github.com/goofballLogic). - Add Opera 36 support for
`class`

([BCD PR 3102](https://github.com/mdn/browser-compat-data/pull/3102)), from[Christian Sirolli](https://github.com/HeyITGuyFixIt). - Add that “Experimental JavaScript Features” preference needed for Edge support of
`RegExp.flags`

([BCD PR 3142](https://github.com/mdn/browser-compat-data/pull/3142)), from[ulrichb](https://github.com/ulrichb). - Fix typo in
`KeyboardEvent`

notes ([BCD PR 3146](https://github.com/mdn/browser-compat-data/pull/3146)), from[Philipp Spiess](https://github.com/philipp-spiess). - Samsung Browser does not support CSS media feature
`display-mode`

([BCD PR 3153](https://github.com/mdn/browser-compat-data/pull/3153)), from[Sumurai8](https://github.com/Sumurai8). - Update desktop Edge compatibility data for
`URLSearchParams`

([BCD PR 3162](https://github.com/mdn/browser-compat-data/pull/3162)), from[Vitaly K.](https://github.com/VitalyKrenel). - Add node.js v11 support for
`flatMap`

([BCD PR 3163](https://github.com/mdn/browser-compat-data/pull/3163)), from[Artur Klesun](https://github.com/klesun). `Document.hasFocus`

,`ChildNode.remove`

are not supported by Opera 12.18 ([BCD PR 3165](https://github.com/mdn/browser-compat-data/pull/3165)), from[Abradoks](https://github.com/Abradoks).`Lookbehind`

has no firefox support ([BCD PR 3189](https://github.com/mdn/browser-compat-data/pull/3189)), from[StefanSchoof](https://github.com/StefanSchoof).- Add support row for
`for await...of`

([BCD PR 3194](https://github.com/mdn/browser-compat-data/pull/3194)), from[Yuichi Nukiyama](https://github.com/YuichiNukiyama). - Add Safari iOS support for
`animateMotion`

([BCD PR 3222](https://github.com/mdn/browser-compat-data/pull/3222)), from[Paul Masson](https://github.com/paulmasson). - Add support for
`BigInt`

([BCD PR 3224](https://github.com/mdn/browser-compat-data/pull/3224)), from[VFDan](https://github.com/VFDan). - Opera still supports
`@keyframes`

([BCD PR 3227](https://github.com/mdn/browser-compat-data/pull/3227)), from[Tony Ross](https://github.com/antross). - Fix preference name for Firefox for CSS property
`scrollbar-color`

([BCD PR 3234](https://github.com/mdn/browser-compat-data/pull/3234)), from[Josh Smith](https://github.com/joshua-s). - Simplify
`Math.round`

example ([Interactive Examples PR 1230](https://github.com/mdn/interactive-examples/pull/1230)), from[Kevin Simper](https://github.com/kevinsimper). - Add
`Intl.RelativeDateFormat`

example ([Interactive Examples PR 1245](https://github.com/mdn/interactive-examples/pull/1245)), from[Romulo Cintra](https://github.com/romulocintra). - Put prefixed
`position: -webkit-sticky`

value before the standard value ([Interactive Examples PR 1249](https://github.com/mdn/interactive-examples/pull/1249)), from[Daniel Holbert](https://github.com/dholbert). - Use example name for employee (
[Interactive Examples PR 1259](https://github.com/mdn/interactive-examples/pull/1259)), from[Osama Soliman](https://github.com/microsmsm). - Change expected output of
`Math.trunc`

to negative 0 ([Interactive Examples PR 1264](https://github.com/mdn/interactive-examples/pull/1264)), from[Hugo Nogueira](https://github.com/Marabyte). - Fix spelling of
`nonExistentFunction`

([Interactive Examples PR 1274](https://github.com/mdn/interactive-examples/pull/1274)), from[Dale Harris](https://github.com/Da13Harris). - Drop
`<length>`

from`scrollbar-width`

([Data PR 334](https://github.com/mdn/data/pull/334)), from[Emilio Cobos Álvarez](https://github.com/emilio). - Add
`lang`

attribute to`<span class="nt"><html></span>`

element ([learning-area PR 113](https://github.com/mdn/learning-area/pull/113)), from[Alexey Filin](https://github.com/alexphilin). - Add
`id`

attribute to`<input>`

element ([learning-area PR 114](https://github.com/mdn/learning-area/pull/114)), from[lfzyx](https://github.com/lfzyx). - Add travis-based markdown linting and spell checking (
[PR 6](https://github.com/mdn/stumptown-experiment/pull/6)), from[Ryan Johnson](https://github.com/escattone)(first contribution to stumptown-experiment). - Remove bulk preloading all fonts (
[html-examples PR 3](https://github.com/mdn/html-examples/pull/3)), from[Vadim Makeev](https://github.com/pepelsbey).

## Planned for January

[David Flanagan](https://github.com/davidflanagan) took a look at [KumaScript](https://github.com/mdn/kumascript), MDN’s macro rendering engine, and is proposing several changes to modernize it, including using [await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await) and [Jest](https://jestjs.io). These changes are performing well in the development environment, and we plan to get the new code in production in January.

## About John Whitlock

John is a web developer working on the engine of MDN Web Docs