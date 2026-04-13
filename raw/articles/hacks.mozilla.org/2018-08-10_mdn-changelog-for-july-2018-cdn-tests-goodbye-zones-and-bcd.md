---
title: 'MDN Changelog for July 2018: CDN tests, Goodbye Zones, and BCD – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2018/08/mdn-changelog-for-july-2018-cdn-tests-goodbye-zones-and-bcd/
author: John Whitlock
published: '2018-08-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s note:** *A changelog is “a log or record of all notable changes made to a project. [It] usually includes records of changes such as bug fixes, new features, etc.” Publishing a changelog is kind of a tradition in open source, and a long-time practice on the web. We thought readers of Hacks and folks who use and contribute to MDN Web Docs would be interested in learning more about the work of the MDN engineering team, and the impact they have in a given month. We’ll also introduce code contribution opportunities, interesting projects, and new ways to participate.*

Here’s what happened in July to the [code, data, and tools](https://github.com/mdn/) that support [MDN Web Docs](https://developer.mozilla.org):

[Experimented with the CDN](https://hacks.mozilla.org#cdn-jul-18)[Decommissioned zones](https://hacks.mozilla.org#zones-jul-18)[Converted compatibility data](https://hacks.mozilla.org#bcd-jul-18)[Shipped tweaks and fixes](https://hacks.mozilla.org#tweaks-jul-18)by merging 307 pull requests, including 58 pull requests from 43 new contributors.

Here’s the plan for August:

## Done in July

### Experimented with longer CDN expirations

We moved MDN Web Docs to a CDN in [April 2018](https://hacks.mozilla.org/2018/05/cdn-bcd-and-svg-mdn-changelog-for-april-2018/), and saw a 16% improvement in page load times. We shipped with 5 minute expiration times for MDN pages, so that the CDN will request a fresh copy after a short time. MDN is a wiki, and we can’t predict when a page will change. 300 seconds was a compromise between some caching for our most popular pages, and how long an author would need to wait for a changed page to be published to all visitors. 80% of visitors are getting an uncached page.

Longer cache expirations would require cache invalidation, [one of the two hard things in computer science](https://twitter.com/codinghorror/status/506010907021828096). Before committing to the work, we wanted to estimate the expected performance benefits. From July 9 to 15, [Ryan Johnson](https://github.com/escattone) bumped the timeout from 5 minutes to 48 hours ([PR 4876](https://github.com/mozilla/kuma/pull/4876)), and we gathered the performance data.

Average page load time decreased 3% over the previous week, a small and not significant improvement. The results for different countries was mixed, some slightly improved, and some slightly worse. The outlier was China, where average page load time increased 22%, a significant *decrease* in performance.

The page load time varied on weekdays versus weekends as well (positive percents are shorter page load times, better for users):

| Country | Page Load Decrease, Weekday |
Page Load Decrease, Weekend |
|---|---|---|
| All | 1% | -2% |
| USA | 3% | 3% |
| India | 2% | -7% |
| China | -22% | -35% |
| Japan | 0% | 10% |
| France | -1% | -5% |
| Germany | 3% | 3% |
| UK | 2% | 2% |
| Russia | 0% | 2% |
| Brazil | 2% | -2% |
| Ukraine | 6% | 1% |

This is a successful experiment. We got an unexpected result, with minimal work to get those results. At the same time, we’re curious why the longer CDN expiration had little effect for most users, and a negative effect for China. We have some theories.

CloudFront is Amazon’s CDN, and uses the same data centers and networks as MDN’s servers. MDN is optimized for quickly serving wiki pages, so a cache miss adds only 50-100 milliseconds to a request. The primary benefit of the CDN is reducing server load, and we did see a 25% – 50% reduction in requests made to the servers, especially during peak hours.

We’re currently directing CloudFront to cache pages, but telling downstream proxies and browsers not to cache the pages. A wiki page can change after someone edits it, and we wanted to avoid several layers of caches holding on to stale copies. Downstream caches may have a bigger impact than we expect on page load, and we can try allowing caching in the next experiment.

China has country-wide policies to monitor and control internet traffic. We don’t know the details, but longer caching times result in slower processing. We saw an improvement in China moving developer.mozilla.org to CloudFront, lowering the average page load time by 30%. It is possible that most of the benefit was due to removing a second domain lookup for assets. A future experiment may skip CloudFront for traffic from China.

There’s a significant difference between weekday and weekend traffic in some countries, like China and Japan. Our guess is that weekday traffic is dominated by developers using MDN for work, weekend traffic by developers using MDN for hobbies and learning. We also suspect there are differences between the capabilities of work week devices and home devices.

Finally, the results may be a limitation of CloudFront, and we would see different results with a different CDN provider.

We’ll look elsewhere for ways to speed up our page load times. For example, [Schalk Neethling](https://github.com/schalkneethling) is working to replace icons via webfonts with SVG icons ([PR 4860](https://github.com/mozilla/kuma/pull/4860)), and inlining short JavaScript files rather than making a request ([PR 4881](https://github.com/mozilla/kuma/pull/4881)). We have further plans for reducing page load time, to meet our new performance goals.

## Decommissioned zones

[Ryan Johnson](https://github.com/escattone) removed zones on July 24, merging [PR 4853](https://github.com/mozilla/kuma/pull/4853). From a user’s perspective, there are a few changes.

Custom zone URLs, like [https://developer.mozilla.org/en-US/Firefox/Releases/61](https://developer.mozilla.org/en-US/Firefox/Releases/61), are now at standard wiki URLs under `/docs/`

, like [https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/61](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/61). There are redirects to the new URLs, so old links should continue working.

Custom zone styling is removed, and zone pages now look like other wiki pages. This is subtle on most pages, such as removing an icon next to the title. Other pages required a re-write, such as [The History of MDN](https://developer.mozilla.org/en-US/docs/MDN_at_ten/History_of_MDN).

Zone sidebars were converted to KumaScript sidebars, and added to each page in the zone, through the heroic efforts of [wbamberg](https://github.com/wbamberg) ([PR 711](https://github.com/mdn/kumascript/pull/711) and a few others).

About 2600 lines of code were removed, about 10% of the codebase. The wiki code is now simpler, less error prone, and safer to update.

### Converted compatibility data

In July of last year, the Browser Compatibility Data (BCD) project hit the milestone of over 1000 MDN pages using the new compatibility data, with about 4900 to convert. This month, there are less than 850 pages left to convert, and over 5000 MDN pages are using the new data. The steady work of the BCD team has made a huge impact on MDN and the community.

Visual Studio Code [improved the accuracy of their data](https://code.visualstudio.com/updates/v1_25#_improved-accuracy-of-browser-compatibility-data) by adopting the BCD project in the June 2018 release. This was proposed by [Pine](https://github.com/octref) in [vscode-css-languageservice issue #102](https://github.com/Microsoft/vscode-css-languageservice/issues/102) and implemented in [PR #105](https://github.com/Microsoft/vscode-css-languageservice/pull/105), with feedback from BCD and mdn/data contributor [Connor Shea](https://github.com/connorshea).

After a long discussion, the BCD project has updated the policy for Node.js versions numbers ([PR 2196](https://github.com/mdn/browser-compat-data/pull/2196), [PR 2294](https://github.com/mdn/browser-compat-data/pull/2294), and others). At first, browser-style version numbers were used, such as `“4”`

, `“6”`

, and `“8”`

, but the Node.js community requested `“4.0.0”`

, `“6.0.0”`

, and `“8.0.0”`

, to reflect how they think of release numbers. This affected lots of files and unstuck several Node.js pull requests.

[Florian Scholz](https://github.com/Elchi3) went on vacation, and [Daniel D. Beck](https://github.com/ddbeck) took the lead on project maintenance, including shipping the npm package, now documented via [PR 2480](https://github.com/mdn/browser-compat-data/pull/2480). Most of the [PRs from the Paris Hack on MDN event](https://github.com/mdn/browser-compat-data/pulls?utf8=%E2%9C%93&q=is%3Apr+label%3A%22HackOnMDNParis2018+%3Afr%3A%22+) are now merged or closed, and the project is down to 120 open PRs, representing about half of the remaining conversion work.

### Shipped Tweaks and Fixes

There were 307 PRs merged in July:

[197 mdn/browser-compat-data PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[48 mdn/interactive-examples PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[26 mozilla/kuma PRs](https://github.com/mozilla/kuma/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[13 mdn/kumascript PRs](https://github.com/mdn/kumascript/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[6 mdn/bob PRs](https://github.com/mdn/bob/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[5 mdn/infra PRs](https://github.com/mdn/infra/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[4 mdn/learning-area PRs](https://github.com/mdn/learning-area/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[1 mdn/learning-area-pt-br PR](https://github.com/mdn/learning-area-pt-br/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[1 mdn/dom-examples PR](https://github.com/mdn/dom-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[1 mdn/voice-change-o-matic PR](https://github.com/mdn/voice-change-o-matic/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[1 mdn/web-components-examples PR](https://github.com/mdn/web-components-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[1 mdn/webextensions-examples PR](https://github.com/mdn/webextensions-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[1 mdn/doc-linter-webextension PR](https://github.com/mdn/doc-linter-webextension/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[1 mdn/data PR](https://github.com/mdn/data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")[1 mdn/web-speech-api PR](https://github.com/mdn/web-speech-api/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31")

58 of these were from first-time contributors:

- Correct node support for spread (
`...`

) in object literals ([BCD PR 2189](https://github.com/mdn/browser-compat-data/pull/2189)), from[Tobias](https://github.com/m4staka). - Add NodeJS versions for some features (
[BCD PR 2196](https://github.com/mdn/browser-compat-data/pull/2196)), from[Solant](https://github.com/Solant). - Update JavaScript spread operator (
`...`

) for Node.js ([PR 2262](https://github.com/mdn/browser-compat-data/pull/2262)), Update Node.js versions ([PR 2294](https://github.com/mdn/browser-compat-data/pull/2294)), and[9 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-07-01..2018-07-31"+author:jcsahnwaldt)to BCD from[Christopher Sahnwaldt](https://github.com/jcsahnwaldt). - Add browser compatibility table for
`<input type="checkbox">`

([PR 2383](https://github.com/mdn/browser-compat-data/pull/2383)), Add browser compatibility table for`<input type="button">`

([PR 2384](https://github.com/mdn/browser-compat-data/pull/2384)), and Add browser compatibility table for`<input type="search">`

([PR 2385](https://github.com/mdn/browser-compat-data/pull/2385)), to BCD from[varun singh](https://github.com/varun07). - Add missing entity ampersands in description. (
[BCD PR 2397](https://github.com/mdn/browser-compat-data/pull/2397)), from[epistemex](https://github.com/epistemex). - Add
`DOMStringMap`

([BCD PR 2401](https://github.com/mdn/browser-compat-data/pull/2401)), from[Ayush Poddar](https://github.com/Mr-Magnificent). - Add Edge support for
`overflow-wrap`

([BCD PR 2406](https://github.com/mdn/browser-compat-data/pull/2406)), from[Quentin Calvez](https://github.com/quentez). - Add missing
`browserSettings`

permission ([BCD PR 2407](https://github.com/mdn/browser-compat-data/pull/2407)), from[Juraj Mäsiar](https://github.com/icl7126). - Add data on
`window.scroll`

for MS Edge ([BCD PR 2433](https://github.com/mdn/browser-compat-data/pull/2433)), from[David Wheatley](https://github.com/davwheat). - Update data on
`<input type="color">`

for Edge ([BCD PR 2434](https://github.com/mdn/browser-compat-data/pull/2434)), from[Thomas Prochazka](https://github.com/zlypher). - Add IDEA (IntelliJ, WebStorm, etc.) to
`.gitignore`

([PR 2435](https://github.com/mdn/browser-compat-data/pull/2435)), and Add Node.js 8.0.0 support for JavaScript features ([PR 2436](https://github.com/mdn/browser-compat-data/pull/2436)), to BCD from[Peter Mouland](https://github.com/peter-mouland). - Update
`backdrop-filter`

([BCD PR 2438](https://github.com/mdn/browser-compat-data/pull/2438)), from[Philip Goto](https://github.com/flipflop97). - Add
`text-align`

’s`<string>`

value ([BCD PR 2442](https://github.com/mdn/browser-compat-data/pull/2442)), from[Jakob Krigovsky](https://github.com/sonicdoe). - Add
`search.get`

,`search.search`

API data ([BCD PR 2444](https://github.com/mdn/browser-compat-data/pull/2444)), from[Geoffrey De Belie](https://github.com/Smile4ever). - Add compatibility for
`window.scrollTo`

([BCD PR 2445](https://github.com/mdn/browser-compat-data/pull/2445)), from[Mauro Mandracchia](https://github.com/M3kH). - Add support for CSS selector
`:defined`

([BCD PR 2454](https://github.com/mdn/browser-compat-data/pull/2454)), from[Estelle Weyl](https://github.com/estelle). - Add support for
`window.scroll`

functions in Safari ([BCD PR 2462](https://github.com/mdn/browser-compat-data/pull/2462)), from[Raz Goldin](https://github.com/zargold). - Mark properties defined in ECMA-262 Annex B as deprecated (
[BCD PR 2469](https://github.com/mdn/browser-compat-data/pull/2469)), from[TSlivede](https://github.com/TSlivede). - Add support for
`MediaDevices`

API ([BCD PR 2472](https://github.com/mdn/browser-compat-data/pull/2472)), from[Gaurav Mahto](https://github.com/gauravmahto). - Update Safari support for CSS property
`overscroll-behavior`

from unknown to unsupported ([BCD PR 2490](https://github.com/mdn/browser-compat-data/pull/2490)), from[Peter Fernandes](https://github.com/fernap3). - Update Safari support for
`Navigator.registerProtocolHandler`

API from unknown to unsupported ([BCD PR 2499](https://github.com/mdn/browser-compat-data/pull/2499)), from[Lioman](https://github.com/lioman). - Move Firefox support for
`Server-Timing`

header from 59 to 61 ([BCD PR 2504](https://github.com/mdn/browser-compat-data/pull/2504)), from[Charles Vazac](https://github.com/cvazac). - Fix JS
`RegExp`

lookbehind assertion description ([BCD PR 2521](https://github.com/mdn/browser-compat-data/pull/2521)), from[Nate Weaver](https://github.com/Wevah). - Update IE’s support of CSS property
`text-align-last`

([BCD PR 2525](https://github.com/mdn/browser-compat-data/pull/2525)), from[Refael Iliaguyev](https://github.com/rellect). - Add Node.js 10 support for
`promise.finally`

([BCD PR 2529](https://github.com/mdn/browser-compat-data/pull/2529)), from[NKN1396](https://github.com/NKN1396). - Add Chrome support for
`crisp-edges`

as`-webkit-optimize-contrast`

([BCD PR 2531](https://github.com/mdn/browser-compat-data/pull/2531)), from[Eugene Pankov](https://github.com/Eugeny). - Fix CSP term
`navigate-to`

(was`navigation-to`

) ([BCD PR 2532](https://github.com/mdn/browser-compat-data/pull/2532)), from[Malvoz](https://github.com/Malvoz). - Lowercase
`minlength`

attribute for`<input type=password>`

example ([Interactive Examples PR 1024](https://github.com/mdn/interactive-examples/pull/1024)), from[Timo Tijhof](https://github.com/Krinkle). - Change
`<select>`

examples to use “placeholder label option” pattern ([Interactive Examples PR 1025](https://github.com/mdn/interactive-examples/pull/1025)), from[Taylor Hunt](https://github.com/tigt). - Add a new line for markdown bullet list (
[Interactive Examples PR 1028](https://github.com/mdn/interactive-examples/pull/1028)), from[Enguerran](https://github.com/enguerran). - Add
`balance-all`

value to`column-fill`

example ([Interactive Examples PR 1039](https://github.com/mdn/interactive-examples/pull/1039)), from[Estelle Weyl](https://github.com/estelle). - Add
`id`

as reference for`<label for=>`

attribute ([Interactive Examples PR 1045](https://github.com/mdn/interactive-examples/pull/1045)), from[Jon Borglund](https://github.com/Row). - Make “Publish and Keep Editing” height the same as others (
[Kuma PR 4900](https://github.com/mozilla/kuma/pull/4900)), from[Mihir Karbelkar](https://github.com/Mihir-Karbelkar). - Update the URL of Web Speech API (
[KumaScript PR 731](https://github.com/mdn/kumascript/pull/731)), from[Kagami Sascha Rosylight](https://github.com/saschanaz). - Updating Learn sidebar to add new Layout guides (
[PR 736](https://github.com/mdn/kumascript/pull/736)), from[Rachel Andrew](https://github.com/rachelandrew)(first contribution to KumaScript). - Move Writing Modes Level 4 to Candidate Recommendation (CR) (
[KumaScript PR 744](https://github.com/mdn/kumascript/pull/744)), from[Estelle Weyl](https://github.com/estelle). - Reference correct video source video file (
[learning-area PR 84](https://github.com/mdn/learning-area/pull/84)), from[Rohit Arondekar](https://github.com/rohit). - Fix “farenheit” typo (
[learning-area PR 85](https://github.com/mdn/learning-area/pull/85)), from[arda152](https://github.com/arda152). - Fix comparison operator (
`!==`

) in Event Listener ([learning-area PR 86](https://github.com/mdn/learning-area/pull/86)), from[Mourad El garma](https://github.com/aka-yuki). - Add folder
`javascript/object-basics`

for chapter translation ([learning-area-pt-br PR 2](https://github.com/mdn/learning-area-pt-br/pull/2)), from[Felipe Maia](https://github.com/webfelipemaia). - Change convolver to disconnect and reconnect to the audio path (
[voice-change-o-matic PR 15](https://github.com/mdn/voice-change-o-matic/pull/15)), from[LUCAS GARIBALDI ALVES](https://github.com/lgaribaldi). - Use ES2015+ syntax (
[web-components-examples PR 8](https://github.com/mdn/web-components-examples/pull/8)), from[Kevin Nagurski](https://github.com/knagurski). - Add
`EventRef`

to the list of allowed macros ([PR 70](https://github.com/mdn/doc-linter-webextension/pull/70)), from[Eric Shepherd](https://github.com/a2sheppy)(first contribution to Doc Linter WebExtension). - Maintain case consistency (
[web-speech-api PR 26](https://github.com/mdn/web-speech-api/pull/26)), from[utkarsh-raj](https://github.com/utkarsh-raj).

Other significant PRs:

- Check bugzil.la link format (
[BCD PR 2511](https://github.com/mdn/browser-compat-data/pull/2511)), one of[32 Pull Requests](https://github.com/mdn/browser-compat-data/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed+merged%3A%222018-07-01..2018-07-31%22+author%3Acaugner)from[Claas Augner](https://github.com/caugner). - Open interactive example links in a new tab (
[Interactive Examples PR 1009](https://github.com/mdn/interactive-examples/pull/1009)), from[Stephan Max](https://github.com/stephanmax). - Update node 8, dependencies (
[Kuma PR 4852](https://github.com/mozilla/kuma/pull/4852)), from[me](https://github.com/jwhitlock).

## Planned for August

In August, we’ll continue working on new and improved interactive examples, converting compatibility data (aiming for less than 50 open PRs), switching to Python 3, improving performance, and other long-term projects.

### Upgrade to Elasticsearch 5.6

Elasticsearch powers our little-loved site search, and we’re using version 2.4 in production. This version went [out of support](https://www.elastic.co/support/eol) in February 2018, but our provider gave us until August to update. We used that grace period to [update from Django 1.8 to 1.11](https://hacks.mozilla.org/2018/07/mdn-changelog-for-june-2018/#shipped-django-111). In August, we’ll update our client libraries and code so we can update to Elasticsearch 5.6, the next major release. We don’t expect many user-visible changes with the new server, but we also don’t plan to lose site search due to missing the deadline.

## About John Whitlock

John is a web developer working on the engine of MDN Web Docs