---
title: MDN Changelog for June 2018 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/07/mdn-changelog-for-june-2018/
author: John Whitlock
published: '2018-07-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s note:** *A changelog is “a log or record of all notable changes made to a project. [It] usually includes records of changes such as bug fixes, new features, etc.” Publishing a changelog is kind of a tradition in open source, and a long-time practice on the web. We thought readers of Hacks and folks who use and contribute to MDN Web Docs would be interested in learning more about the work of the MDN engineering team, and the impact they have in a given month. We’ll also introduce code contribution opportunities, interesting projects, and new ways to participate.*

## Done in June

Here’s what happened in June to the [code, data, and tools](https://github.com/mdn/) that support [MDN Web Docs](https://developer.mozilla.org/):

[Shipped 100+ HTML Interactive Examples](https://hacks.mozilla.org#shipped-100-html-interactive-examples)[Shipped Django 1.11](https://hacks.mozilla.org#shipped-django-111)[Shipped tweaks and fixes](https://hacks.mozilla.org#shipped-tweaks-and-fixes)by merging 252 pull requests, including 32 pull requests from 26 new contributors.

Here’s the plan for July:

In June, we shipped over 100 HTML interactive examples, adding quick references and playgrounds for our HTML element documentation.

[Schalk Neethling](https://github.com/schalkneethling) fixed the remaining blockers, such as applying an `output`

class as a style target ([PR 961](https://github.com/mdn/interactive-examples/pull/961)), and adding some additional size options ([PR 962](https://github.com/mdn/interactive-examples/pull/962)). [wbamberg](https://github.com/wbamberg) wrote instructions for adding the examples to MDN, and [SphinxKnight](https://github.com/SphinxKnight) and [Irene Smith](https://github.com/irenesmith) pitched in to deploy them in less than 24 hours. MDN visitors have fun, informative examples on JS, CSS, and now HTML reference pages.

Irene Smith joined the MDN writer’s team in June as a Firefox Developer Content Manager. She started work right away, including helping with this project. Welcome to the team, Irene!

### Shipped Django 1.11

We deployed Django 1.11 on June 6th. There are no visible changes, but also no errors for MDN visitors. Sometimes a engineering project is successful if you just get back to where you started.

We did most of the [preparation work](https://hacks.mozilla.org/2018/06/media-mathml-and-django-1-11-mdn-changelog-for-may-2018/#django-1-11-may-18) in development environments. On June 1st, we shipped Django 1.11 to our staging environment ([PR 4830](https://github.com/mozilla/kuma/pull/4830)). This exposed a few issues that were quick to fix, such as the logging configuration ([PR 4831](https://github.com/mozilla/kuma/pull/4831)) and client-side translation catalogs ([PR 4831](https://github.com/mozilla/kuma/pull/4831)). Tests in the production-like staging environment ensured the last bugs were fixed before MDN’s visitors saw them.

We’re looking ahead to the next framework update. Django 1.11 is the last to support Python 2.7, so we’ll need to switch to [Python 3.6](https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-pep498). We’ve added a [Python 3 build to TravisCI](https://travis-ci.org/mozilla/kuma), and will ratchet up compatibility over time ([PR 4848](https://github.com/mozilla/kuma/pull/4848)). [Anthony Maton](https://github.com/MatonAnthony) started the Python 3 changes at the Mozilla All-Hands, updating tests to expect random dictionary order, [a security feature enabled in Python 3.3](https://stackoverflow.com/a/14959001/10612) ([PR 4851](https://github.com/mozilla/kuma/pull/4851)). We expect many more changes, and we plan to switch to Python 3 with Django 1.11 by the end of the year.

The next Django Long-Term Support (LTS) release will be 2.2, [scheduled for April 2019](https://www.djangoproject.com/download/#supported-versions). The work will be similar to the last upgrade, updating the code to be compatible with Django 1.11 through 2.2. [Ryan Johnson](https://github.com/escattone) started the process by converting to the [new-style middleware](https://docs.djangoproject.com/en/1.11/topics/http/middleware/), required in 2.0 ([PR 4841](https://github.com/mozilla/kuma/pull/4841)). We plan a smooth switch to Django 2.2 by June 2019.

### Shipped Tweaks and Fixes

There were 252 PRs merged in June:

[133 mdn/browser-compat-data PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=%E2%9C%93&q=is:pr+is:closed+merged:%222018-06-01..2018-06-30%22)[45 mdn/interactive-examples PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=%E2%9C%93&q=is:pr+is:closed+merged:%222018-06-01..2018-06-30%22)[39 mozilla/kuma PRs](https://github.com/mozilla/kuma/pulls?page=1&utf8=%E2%9C%93&q=is:pr+is:closed+merged:%222018-06-01..2018-06-30%22)[12 mdn/kumascript PRs](https://github.com/mdn/kumascript/pulls?page=1&utf8=%E2%9C%93&q=is:pr+is:closed+merged:%222018-06-01..2018-06-30%22)[10 mdn/bob PRs](https://github.com/mdn/bob/pulls?page=1&utf8=%E2%9C%93&q=is:pr+is:closed+merged:%222018-06-01..2018-06-30%22)[7 mdn/infra PRs](https://github.com/mdn/infra/pulls?page=1&utf8=%E2%9C%93&q=is:pr+is:closed+merged:%222018-06-01..2018-06-30%22)[4 mdn/data PRs](https://github.com/mdn/data/pulls?page=1&utf8=%E2%9C%93&q=is:pr+is:closed+merged:%222018-06-01..2018-06-30%22)[1 mdn/learning-area PR](https://github.com/mdn/learning-area/pulls?page=1&utf8=%E2%9C%93&q=is:pr+is:closed+merged:%222018-06-01..2018-06-30%22)[1 mdn/webextensions-examples PR](https://github.com/mdn/webextensions-examples/pulls?page=1&utf8=%E2%9C%93&q=is:pr+is:closed+merged:%222018-06-01..2018-06-30%22)

32 of these were from first-time contributors:

- Fix compat data for
`let`

in Chrome ([BCD PR 1632](https://github.com/mdn/browser-compat-data/pull/1632)), from[zx](https://github.com/genezx). - Update Function.json (
[BCD PR 1988](https://github.com/mdn/browser-compat-data/pull/1988)), from[Jack Giffin](https://github.com/anonyco). - Add compat data for
`Window`

sub features from A to F ([BCD PR 2109](https://github.com/mdn/browser-compat-data/pull/2109)), from[Keshav Mesta](https://github.com/keshavmesta). - Add compat data for CSS type
`timing-function`

([BCD PR 2183](https://github.com/mdn/browser-compat-data/pull/2183)), from[Pavel](https://github.com/severn101). - Update
`replaceTrack`

API support version ([BCD PR 2205](https://github.com/mdn/browser-compat-data/pull/2205)), from[Xin](https://github.com/betimer). - Add safari compatibility for exponentiation operator
`**`

([PR 2212](https://github.com/mdn/browser-compat-data/pull/2212)), from[schlagi123](https://github.com/schlagi123)(first contribution to BCD). `aspect-ratio`

supported in Chrome ([BCD PR 2224](https://github.com/mdn/browser-compat-data/pull/2224)), from[Filip Chalupa](https://github.com/Onset).- Update Edge 17 ParentNode/ChildNode API support (
[PR 2280](https://github.com/mdn/browser-compat-data/pull/2280)), from[Jonathan Neal](https://github.com/jonathantneal)(first contribution to BCD). - Add safari compatibility for
`navigator.sendBeacon`

([BCD PR 2281](https://github.com/mdn/browser-compat-data/pull/2281)), from[Eran Shabi](https://github.com/eranshabi). - Add
`Response`

.{`error`

,`redirect`

} for Edge/Safari ([BCD PR 2285](https://github.com/mdn/browser-compat-data/pull/2285)), from[James Browning](https://github.com/Jamesernator). - Update compat for
`HTMLMediaElement.captureStream()`

([BCD PR 2295](https://github.com/mdn/browser-compat-data/pull/2295)), from[Jakub Knoz](https://github.com/CaptainJKoB). - Add a description for
`javascript.builtins.Promise.Promise`

([PR 2303](https://github.com/mdn/browser-compat-data/pull/2303)), from[kenju](https://github.com/kenju)(first contribution to BCD). - Updated NodeList apis for Edge (
[BCD PR 2325](https://github.com/mdn/browser-compat-data/pull/2325)), from[Richard Eames](https://github.com/Naddiseo). - Update
`grammar.json`

([PR 2328](https://github.com/mdn/browser-compat-data/pull/2328)), and Update`TypedArray.json`

([PR 2331](https://github.com/mdn/browser-compat-data/pull/2331)), to BCD from[Peppesterest](https://github.com/The-Peppester). - Add
`externally_connectable`

([BCD PR 2329](https://github.com/mdn/browser-compat-data/pull/2329)), from[Anatoli Babenia](https://github.com/abitrolly). - Add note about partial support for
`Path2D`

constructor in Edge ([BCD PR 2343](https://github.com/mdn/browser-compat-data/pull/2343)), from[hn3000](https://github.com/hn3000). - Added support information for
`tab_background_separator`

([PR 2349](https://github.com/mdn/browser-compat-data/pull/2349)), and`isPointInStroke`

([PR 2375](https://github.com/mdn/browser-compat-data/pull/2375)), to BCD from[Irene Smith](https://github.com/irenesmith). - Safari has more
`FormData`

support now ([PR 2376](https://github.com/mdn/browser-compat-data/pull/2376)), from[Jimmy Wärting](https://github.com/jimmywarting)(first contribution to BCD). - Correct “expected output” mistake (
[Interactive Examples PR 1000](https://github.com/mdn/interactive-examples/pull/1000)), from[Arkangus](https://github.com/Arkangus). - Add a name to the provided address (
[Interactive Examples PR 1004](https://github.com/mdn/interactive-examples/pull/1004)), from[Robert Katzki](https://github.com/ro-ka). - Update the German localization for
`SeeCompatTable`

([KumaScript PR 719](https://github.com/mdn/kumascript/pull/719)), from[Metaa](https://github.com/metaa). - Replace deprecated
`cache_behavior`

with`ordered_cache_behavior`

([PR 3](https://github.com/mdn/infra/pull/3)), Change behavior from`*/users/*`

to`users/*`

([PR 5](https://github.com/mdn/infra/pull/5)), and[3 more PRs](https://github.com/mdn/infra/pulls?page=1&utf8=%E2%9C%93&q=is:pr+is:closed+merged:%222018-06-01..2018-06-30%22+author:escattone)from[Ryan Johnson](https://github.com/escattone)(first contributions to infra). - MDN infra terraform refactor (
[infra PR 4](https://github.com/mdn/infra/pull/4)), from[Ed Lim](https://github.com/limed). `syntaxes.json`

:`<'border-radius'>`

instead of`<border-radius>`

([Data PR 246](https://github.com/mdn/data/pull/246)), from[abaco](https://github.com/abaco).- Missing parenthesis at the end of sentence (
[learning-area PR 75](https://github.com/mdn/learning-area/pull/75)), from[Jerson Zúñiga](https://github.com/jzunigacoayla). - Removed newline in URL causing match error (
[webextensions-examples PR 360](https://github.com/mdn/webextensions-examples/pull/360)), from[Nicholas Hansen](https://github.com/ndhansen).

Other significant PRs:

- Migrate
`HTMLSelectElement`

from the wiki ([BCD PR 1406](https://github.com/mdn/browser-compat-data/pull/1406)), from[SphinxKnight](https://github.com/SphinxKnight), one of the[11 PRs](https://github.com/mdn/browser-compat-data/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed+merged%3A%222018-06-01..2018-06-30%22+label%3A%22HackOnMDNParis2018+%3Afr%3A%22+)merged from the March[Hack on MDN](https://hacks.mozilla.org/2018/03/hack-on-mdn-building-useful-tools-with-browser-compatibility-data/)event.[27 to go](https://github.com/mdn/browser-compat-data/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+label%3A%22HackOnMDNParis2018+%3Afr%3A%22+)! - Add compat data for input-password (
[BCD PR 2235](https://github.com/mdn/browser-compat-data/pull/2235)), from[Mark Boas](https://github.com/maboa), one of many PRs in the epic`<input>`

data migration. - Use
[mdn/infra](https://github.com/mdn/infra)instead of mozmeao/infra ([Kuma PR 4840](https://github.com/mozilla/kuma/pull/4840)), from[Ryan Johnson](https://github.com/escattone). - Remove
`ok_()`

from tests ([Kuma PR 4865](https://github.com/mozilla/kuma/pull/4865)), from[Anthony Maton](https://github.com/MatonAnthony). - Fix CurrentGecko macro (
[KumaScript PR 720](https://github.com/mdn/kumascript/pull/720)), from[Ryan Johnson](https://github.com/escattone).

## Planned for July

July is the start of the second half of the year, and the team is thinking about what can be done by the end of the year. We’re planning on finishing the compatibility data migration this year, and expanding interactive examples to another documentation section.

### Decommission Zones

Zones are a wiki engine feature that moves a tree of pages to a different URL, and applies additional CSS for those pages. Zones also add complexity to every request, require additional testing, and are a frequent source of bugs and translation problems. Zones have more enemies than fans on the MDN staff.

We’ve been deprecating zones for a few years. We stopped using new zones as a design tool. In [last year’s site redesign](https://hacks.mozilla.org/2017/07/the-mdn-redesign-behind-the-scenes/), we de-emphasized the style differences between zones and “standard” wiki content ([PR 4348](https://github.com/mozilla/kuma/pull/4348)). When migrating MDN to a new data center, we added a [redirects framework](https://github.com/pmac/django-redirect-urls) that can elegantly handle the custom URLs. We’re ready for the final steps.

At the Mozilla All-Hands, [Ryan Johnson](https://github.com/escattone) and [wbamberg](https://github.com/wbamberg) prepared to remove zones. The work took the entire week. On the engine side, custom URLs need redirects to the standard wiki URLs, and some zone styles need to be preserved ([PR 4853](https://github.com/mozilla/kuma/pull/4853)). Zone sidebars need to be reimplemented as KumaScript sidebars, along with translations ([PR 711](https://github.com/mdn/kumascript/pull/711)). Finally, content needs to be changed, to add the KumaScript sidebars and to use standard wiki CSS. While the changes are large, the effect is subtle.

After the work week, we reviewed and refined the code, double-checked the changes, and clarified the plan. We’ll ship the code, update the content, and delete zones in July.

### Focus on Performance

We’re wrapping up the performance audit of MDN in July. We’ve picked some key performance metrics we’d like to track, and the headline metric is how long it takes for the interactive example to be ready on CSS, JS, and HTML reference pages. [Schalk Neethling](https://github.com/schalkneethling) is implementing the timing measurements ([IE PR 967](https://github.com/mdn/interactive-examples/pull/967),[Kuma PR 4854](https://github.com/mozilla/kuma/pull/4854), and others), using the [PerformanceTiming API](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceTiming) so the measurements will be available in browser tools. We also track timing in Google Analytics, to get real-user metrics from MDN’s global audience, unless the user has requested that [we don’t track them](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/DNT).

We’ve found several performance bottlenecks, and we’re prioritizing them to pick the quick wins and the high-impact changes. We’ll ship improvements in July and beyond.

## About John Whitlock

John is a web developer working on the engine of MDN Web Docs