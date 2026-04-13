---
title: MDN Changelog for August 2018 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/09/mdn-changelog-for-august-2018/
author: John Whitlock
published: '2018-09-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Here’s what happened in August to the [code, data, and tools](https://github.com/mdn/) that support [MDN Web Docs](https://developer.mozilla.org):

[Migrated 95% of compatibility data](https://hacks.mozilla.org#migrated-95-of-compatibility-data)[Improved performance and experience](https://hacks.mozilla.org#improved-performance-and-experience)[Maintained the platform](https://hacks.mozilla.org#maintained-the-platform)[Shipped tweaks and fixes](https://hacks.mozilla.org#shipped-tweaks-and-fixes)by merging 400 pull requests, including 78 pull requests from 55 new contributors

Here’s the plan for September:

## Done in August

### Migrated 95% of compatibility data

The MDN content team prioritized reviewing and merging Browser Compatibility Data pull requests (PRs) in August, and met their goal of getting the [open PRs](https://github.com/mdn/browser-compat-data/pulls) to less than 50. The team reviewed and merged [85 PRs](https://github.com/mdn/browser-compat-data/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed+created%3A%22%3C2018-08-01%22+merged%3A%222018-08-01..2018-08-31%22+) that were open at the start of the month, including a schema change to catch duplicate identifiers ([PR 1415](https://github.com/mdn/browser-compat-data/pull/1415)) from [Dominique Hazael-Massieux](https://github.com/dontcallmedom). The team also merged [123 PRs](https://github.com/mdn/browser-compat-data/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed+created%3A%22%3E%3D2018-08-01%22+merged%3A%222018-08-01..2018-08-31%22+) that were opened during the month, including [Visual Studio Code](https://code.visualstudio.com/) configurations for BCD editing ([PR 2498](https://github.com/mdn/browser-compat-data/pull/2498)) from [ExE Boss](https://github.com/ExE-Boss).

A lot of these were migration PRs, and the migration is now 95% complete, with 10,000 features over 6,300 pages. Some of the remaining migration work will be straightforward. Other data sources will require strategy and format discussions, such as [Event support](https://github.com/mdn/browser-compat-data/issues/935) and [summary pages](https://github.com/mdn/kumascript/pull/650). These discussions will be easier with the experience of migrating thousands of simpler features.

Existing data also got some love. Contributors fixed incorrect data, clarified if and when a browser supported a feature, and celebrated support in new browser releases. We expect a steady stream of maintenance PRs as the project transitions from migration to ongoing maintenance.

[Florian Scholz](https://github.com/Elchi3) has worked to make this a community project, organizing the effort with [spreadsheets](https://github.com/mdn/browser-compat-data/issues/731) and transitioning to [issues](https://github.com/mdn/browser-compat-data/issues/2684) as the remaining work becomes manageable. This has been a successful effort, and [GitHub insights](https://github.com/mdn/browser-compat-data/pulse/monthly) shows that most contributions were not from MDN staff.










Thanks to [ExE Boss](https://github.com/ExE-Boss) ([24 PRs](https://github.com/mdn/browser-compat-data/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed+merged%3A%222018-08-01..2018-08-31%22+author%3AExE-Boss)), [Connor Shea](https://github.com/connorshea) ([23 PRs](https://github.com/mdn/browser-compat-data/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed+merged%3A%222018-08-01..2018-08-31%22+author%3Aconnorshea)), [Claas Augner](https://github.com/caugner) ([18 PRs](https://github.com/mdn/browser-compat-data/pulls?utf8=✓&q=is%3Apr+is%3Aclosed+merged%3A"2018-08-01..2018-08-31"+author%3Acaugner)), [David Ross](https://github.com/bunnybooboo) ([17 PRs](https://github.com/mdn/browser-compat-data/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed+merged%3A%222018-08-01..2018-08-31%22+author%3Abunnybooboo)), [Lucian Condrea](https://github.com/luciancic) ([13 PRs](https://github.com/mdn/browser-compat-data/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed+merged%3A%222018-08-01..2018-08-31%22+author%3Aluciancic)), [Joe Medley](https://github.com/jpmedley) ([8 PRs](https://github.com/mdn/browser-compat-data/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed+merged%3A%222018-08-01..2018-08-31%22+author%3Ajpmedley)), and all our contributors, and thanks to the staff and tool builders that keep the review queue moving!

### Improved performance and experience

[Tim Kadlec](https://github.com/tkadlec) audited MDN in July, and created [performance metrics and goals](https://github.com/mdn/mdn-fiori/wiki), as well as [recommending changes](https://github.com/mdn/sprints/issues/252). In August, we started implementing these changes. [Schalk Neethling](https://github.com/schalkneethling) improved the load time for the homepage by optimizing the hero image ([PR 4903](https://github.com/mozilla/kuma/pull/4903)) and removing a section with an image ([PR 4912](https://github.com/mozilla/kuma/pull/4912)). [Ryan Johnson](https://github.com/escattone) automated recording deployments and re-calculating metrics with [Speedcurve](https://speedcurve.com/) ([PR 4902](https://github.com/mozilla/kuma/pull/4902)). We’ll continue working on performance in the coming months.

Previously, if you wanted to link to a section in a page, such as MDN’s advice on [why you should use labels for <input> elements](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#Why_you_should_use_labels), you had to use the Developer Tools to get the section ID. Schalk added section-level anchor links (

[PR 4901](https://github.com/mozilla/kuma/pull/4901)), so that you can quickly grab the link and paste it into a code review:











### Maintained the platform

[Anthony Maton](https://github.com/MatonAnthony) is switching Kuma to Python 3. Our [memcached library](https://github.com/jezdez/django-memcached-hashring) hasn’t been updated for Python 3, and instead of a library swap, Anthony simplified the caching configuration and switched to Redis ([PR 4870](https://github.com/mozilla/kuma/pull/4870)). He continues to make incremental changes ([PR 4899](https://github.com/mozilla/kuma/pull/4899)) to get to a shared Python 2 / Python 3 codebase, with a goal of switching to Python 3 by the end of the year.

I completed the ElasticSearch 5.6 update, which was harder than expected. The update from 1.7 to 2.4 only required updating the servers ([PR 4192](https://github.com/mozilla/kuma/pull/4192)), and didn’t even merit a mention in the [April 2017 report](https://mozilla.github.io/meao/2017/05/02/kuma-report/). ElasticSearch no longer provides libraries that span major versions. The upgrade from 2.5 to 5.6 required updating the client libraries, the Kuma code that uses them ([PR 4906](https://github.com/mozilla/kuma/pull/4906)), and the server ([PR 4904](https://github.com/mozilla/kuma/pull/4904)), all at the same time. This update included some minor fixes, and search with 5.x appears faster, but site search still needs a lot of work. The next update, to ElasticSearch 6.x, will be in March 2019.

[Ryan Johnson](https://github.com/escattone) is continuing the work of migrating from [MozMEAO](https://github.com/mozmeao) to Mozilla IT support. [Ed Lim](https://github.com/limed) provisioned the new Kubernetes cluster ([PR 24](https://github.com/mdn/infra/pull/31)) and backing services ([PR 31](https://github.com/mdn/infra/pull/31)), with support from [Dave Parfitt](https://github.com/metadave) and [Josh Mize](https://github.com/jgmize). Ryan configured the new Jenkins server to run parallel tests and deployments ([PR 4931](https://github.com/mozilla/kuma/pull/4931)), and to publish Docker images to a [new repository](https://hub.docker.com/u/mdnwebdocs/) ([PR 4933](https://github.com/mozilla/kuma/pull/4933)). We’re now deploying to both the [MozMEAO staging environment](https://developer.allizom.org/en-US/) and the [MozIT staging environment](https://developer-stage.mdn.mozit.cloud/en-US/).

We’ll continue with production and disaster-recovery environments in September, and prioritize the [infrastructure issues](https://github.com/mdn/infra). The goal is to switch traffic in October.

### Shipped tweaks and fixes

There were 400 PRs merged in August:

[208 mdn/browser-compat-data PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31")[53 mozilla/kuma PRs](https://github.com/mozilla/kuma/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31")[34 mdn/bob PRs](https://github.com/mdn/bob/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31")[34 mdn/interactive-examples PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31")[29 mdn/kumascript PRs](https://github.com/mdn/kumascript/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31")[17 mdn/data PRs](https://github.com/mdn/data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31")[16 mdn/infra PRs](https://github.com/mdn/infra/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31")[4 mdn/css-examples PRs](https://github.com/mdn/css-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31")[2 mdn/learning-area PRs](https://github.com/mdn/learning-area/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31")[1 mdn/webextensions-examples PR](https://github.com/mdn/webextensions-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31")[1 mdn/sw-test PR](https://github.com/mdn/sw-test/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31")[1 mdn/webaudio-examples PR](https://github.com/mdn/webaudio-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31")

This includes some important changes and fixes:

- Fix the survey banner on standard DPI displays (
[Kuma PR 4907](https://github.com/mozilla/kuma/pull/4907)), from[Schalk Neethling](https://github.com/schalkneethling). - Avoid “remember this preference” dialog if the language preference is already set (
[Kuma PR 4890](https://github.com/mozilla/kuma/pull/4890)), from[Safwan Rahman](https://github.com/safwanrahman). - Add Discourse field to user profiles (
[Kuma PR 4930](https://github.com/mozilla/kuma/pull/4930)), from[Mihir Karbelkar](https://github.com/Mihir-Karbelkar). - Improve document purging (
[Kuma PR 4934](https://github.com/mozilla/kuma/pull/4934)), from[me](https://github.com/jwhitlock). - Improve reliability of Interactive Example performance metrics (
[Kuma PR 4935](https://github.com/mozilla/kuma/pull/4935)), from[Schalk Neethling](https://github.com/schalkneethling). - Replace
`KUMA_WIKI_IFRAME_ALLOWED_HOSTS`

with`ALLOWED_IFRAME_PATTERNS`

([Kuma PR 4940](https://github.com/mozilla/kuma/pull/4940)), from[me](https://github.com/jwhitlock). - Replace the survey banner with a Firefox Development banner (
[Kuma PR 4938](https://github.com/mozilla/kuma/pull/4938)), from[Schalk Neethling](https://github.com/schalkneethling). - On mobile, show the browser name instead of an icon in compatibility table (
[Kuma PR 4948](https://github.com/mozilla/kuma/pull/4948)), from[Schalk Neethling](https://github.com/schalkneethling).

78 pull requests were from first-time contributors:

- Add Service Worker support in Safari 11.1 (
[BCD PR 1881](https://github.com/mdn/browser-compat-data/pull/1881)), from[Abdón Rodríguez Davila](https://github.com/abdonrd). - Correct SMIL compatibility information (
[BCD PR 1956](https://github.com/mdn/browser-compat-data/pull/1956)), from[Robert Longson](https://github.com/longsonr). - Add compat data for
`Element`

([BCD PR 2316](https://github.com/mdn/browser-compat-data/pull/2316)), from[Bobu aka Sébastien](https://github.com/Rambobafet). - Add compat data for
`PositionError`

. ([BCD PR 2398](https://github.com/mdn/browser-compat-data/pull/2398)), from[Deepraj Pandey](https://github.com/DeeprajPandey). - Fix Mobile Edge support for
`gap`

,`row-gap`

and`column-gap`

([BCD PR 2500](https://github.com/mdn/browser-compat-data/pull/2500)), from[Kumar Harsh](https://github.com/kumarharsh). - Update
`setIcon`

to include Edge notes ([BCD PR 2513](https://github.com/mdn/browser-compat-data/pull/2513)), from[Morgan Gangwere](https://github.com/indrora). - Add missing
`<input type="password">`

description ([BCD PR 2543](https://github.com/mdn/browser-compat-data/pull/2543)), from[weary-adventurer](https://github.com/weary-adventurer). - Update
`datalist`

, not supported by Android WebView. ([BCD PR 2544](https://github.com/mdn/browser-compat-data/pull/2544)), from[Valentin](https://github.com/vpodk). - Rename “ExperimentalCanvasFeatures” to “Experimental Web Platform Features” (
[BCD PR 2547](https://github.com/mdn/browser-compat-data/pull/2547)), from[Indi Kernick](https://github.com/Kerndog73). - Remove Safari support for
`href`

from SVG`<use>`

([BCD PR 2548](https://github.com/mdn/browser-compat-data/pull/2548)), from[Michal Miky Jankovský](https://github.com/Michal-Miky-Jankovsky). - Remove support fort
`proxy.settings`

from Firefox Android ([PR 2550](https://github.com/mdn/browser-compat-data/pull/2550)), from[Martin Giger](https://github.com/freaktechnik)(first contribution to BCD). - Remove support for
`chrome_url_overrides`

from Edge ([BCD PR 2556](https://github.com/mdn/browser-compat-data/pull/2556)), from[Lucas Everett](https://github.com/lucaseverett). - Add support for
`Upgrade-Insecure-Requests`

in Edge 17 ([PR 2561](https://github.com/mdn/browser-compat-data/pull/2561)), and Add support for`:matches()`

in Edge ([PR 2578](https://github.com/mdn/browser-compat-data/pull/2578)), to BCD from[Eric Eggert](https://github.com/yatil). - Add support for
`Request.destination`

in Chrome, Opera and Edge ([BCD PR 2562](https://github.com/mdn/browser-compat-data/pull/2562)), from[Nicolas Hoizey](https://github.com/nhoizey). - Add support for
`InputEvent.getTargetRanges()`

in Safari 10.1 ([PR 2565](https://github.com/mdn/browser-compat-data/pull/2565)), and Add support for Asynchronous Clipboard API in Opera 53 and Chrome 66 ([PR 2703](https://github.com/mdn/browser-compat-data/pull/2703)), to BCD from[Makoto Kato](https://github.com/makotokato). - Add support for
`onbeforeunload`

in Edge ([BCD PR 2566](https://github.com/mdn/browser-compat-data/pull/2566)), from[Sumit Chahal](https://github.com/smtchahal). - Update support for
`-webkit-overflow-scrolling`

, not supported ([BCD PR 2577](https://github.com/mdn/browser-compat-data/pull/2577)), from[Summon528](https://github.com/Summon528). - Update
`X-Frame-Options`

compatibility for Safari and Edge ([PR 2579](https://github.com/mdn/browser-compat-data/pull/2579)), and Fix`Navigator.share`

compatibility for Chrome and Opera ([PR 2595](https://github.com/mdn/browser-compat-data/pull/2595)), to BCD from[Nick Zahn](https://github.com/Manc). - Migrate compat data for
`Coordinates`

([BCD PR 2587](https://github.com/mdn/browser-compat-data/pull/2587)), from[Omar Boukli-Hacene](https://github.com/oboukli). - Update
`window.open`

support IE and Edge ([BCD PR 2594](https://github.com/mdn/browser-compat-data/pull/2594)), from[David Patterson](https://github.com/bob0the0mighty). - Use correct name for
`menus`

permission ([PR 2612](https://github.com/mdn/browser-compat-data/pull/2612)), and Use correct name for`contextMenus`

permission ([PR 2613](https://github.com/mdn/browser-compat-data/pull/2613)), to BCD from[Jay Linski](https://github.com/jaylinski). - Remove Mobile Safari support for
`href`

from SVG`<use>`

([BCD PR 2616](https://github.com/mdn/browser-compat-data/pull/2616)), from[Erno](https://github.com/ernonewman). - Add support for numeric font weights in Chrome 62 (
[PR 2619](https://github.com/mdn/browser-compat-data/pull/2619)), and Move support for RGBA hex notation to Chrome 62 from 63 ([PR 2630](https://github.com/mdn/browser-compat-data/pull/2630)), to BCD from[Kasper Isager](https://github.com/kasperisager). - Add
`Promise.finally`

support in Safari 11.1 ([PR 2623](https://github.com/mdn/browser-compat-data/pull/2623)), and Add Safari 11 support for Performance APIs ([PR 2645](https://github.com/mdn/browser-compat-data/pull/2645)), to BCD from[jakub-g](https://github.com/jakub-g). - Update support for
`NetworkInformation.effectiveType`

([BCD PR 2656](https://github.com/mdn/browser-compat-data/pull/2656)), from[Seul-gi Choi(Chase)](https://github.com/cs09g). - Add support for
`xml:space`

in SVG in Firefox 3 and 4 ([BCD PR 2670](https://github.com/mdn/browser-compat-data/pull/2670)), from[linkmauve](https://github.com/linkmauve). - Add support for
`location.origin`

and`.toString`

in IE 11 ([BCD PR 2672](https://github.com/mdn/browser-compat-data/pull/2672)), from[Nik Rolls](https://github.com/nikrolls). - Add support for
`Document.hasFocus`

in Opera ([BCD PR 2678](https://github.com/mdn/browser-compat-data/pull/2678)), from[Mass Carl](https://github.com/McContax). - Migrate note on Firefox 3.5 support for the Geolocation API (
[BCD PR 2680](https://github.com/mdn/browser-compat-data/pull/2680)), from[Mingye Wang](https://github.com/Artoria2e5). `<details>`

is not in development in Edge ([PR 2688](https://github.com/mdn/browser-compat-data/pull/2688)), from[Kagami Sascha Rosylight](https://github.com/saschanaz)(first contribution to BCD).- Update support for
`NetworkInformation`

for Firefox and Edge ([PR 2689](https://github.com/mdn/browser-compat-data/pull/2689)), and Add support for`Document.exitFullscreen`

([PR 2699](https://github.com/mdn/browser-compat-data/pull/2699)), to BCD from[Thomas den Hollander](https://github.com/ThomasdenH). - Add Edge 15 support version for
`Element.closest`

([BCD PR 2702](https://github.com/mdn/browser-compat-data/pull/2702)), from[Randall Leeds](https://github.com/tilgovi). - Add support for
`word-break`

for Edge ([BCD PR 2704](https://github.com/mdn/browser-compat-data/pull/2704)), from[k-utsumi](https://github.com/k-utsumi). - Fix typo of “user-agent” in
`console.error()`

calls ([Kuma PR 4916](https://github.com/mozilla/kuma/pull/4916)), from[Stephen Donner](https://github.com/stephendonner). - Remove reference to incorrect restart command (
[Kuma PR 4922](https://github.com/mozilla/kuma/pull/4922)), from[James Hobin](https://github.com/hobinjk). - Add examples for async iterators and generators. (
[PR 1036](https://github.com/mdn/interactive-examples/pull/1036)), from[Joe Medley](https://github.com/jpmedley)(first contribution to Interactive Examples). - Add
`String`

`concat`

,`ends`

/`startswith`

,`padend`

/`start`

live examples ([Interactive Examples PR 1068](https://github.com/mdn/interactive-examples/pull/1068)), from[Melissa](https://github.com/meowwwls). - Add method for
`String[@@iterator]()`

([PR 1069](https://github.com/mdn/interactive-examples/pull/1069)), Create an example for the`String.raw()`

method ([PR 1070](https://github.com/mdn/interactive-examples/pull/1070)), and[4 more PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31"+author:irenesmith)from[Irene Smith](https://github.com/irenesmith)(first contributions to Interactive Examples). - Make variable names consistent (
[Interactive Examples PR 1090](https://github.com/mdn/interactive-examples/pull/1090)), from[Roy Revelt](https://github.com/revelt). - Improve example code (
[Interactive Examples PR 1111](https://github.com/mdn/interactive-examples/pull/1111)), from[Arjan Einbu](https://github.com/aeinbu). - Add Japanese Translation for CompatibilityTable.ejs (
[KumaScript PR 692](https://github.com/mdn/kumascript/pull/692)), from[hmatrjp](https://github.com/hmatrjp). - Add data for XPath specifications (
[PR 726](https://github.com/mdn/kumascript/pull/726)), Correct broken`<a>`

and`<strong>`

DOM hierarchy in AddonSidebar ([PR 771](https://github.com/mdn/kumascript/pull/771)), and Add the`overheadIndicator`

class to`SeeCompatTable`

([PR 788](https://github.com/mdn/kumascript/pull/788)), from[ExE Boss](https://github.com/ExE-Boss)(first contributions to KumaScript). - Update CSS4 Text specification (
[PR 735](https://github.com/mdn/kumascript/pull/735)), from[Jakob Krigovsky](https://github.com/sonicdoe)(first contribution to KumaScript). - Add CSS Environment Variables spec (
[KumaScript PR 748](https://github.com/mdn/kumascript/pull/748)), from[Nicolas Hoizey](https://github.com/nhoizey). - Localize WebExtensions Sidebar (
[KumaScript PR 755](https://github.com/mdn/kumascript/pull/755)), from[Etienne Wan](https://github.com/etiennewan). - Add Japanese translation (
[KumaScript PR 763](https://github.com/mdn/kumascript/pull/763)), from[WhiteHawk](https://github.com/WhiteHawk-taka). - Mark a couple of
`scroll-snap`

properties as obsolete ([PR 251](https://github.com/mdn/data/pull/251)), from[Dominique Hazael-Massieux](https://github.com/dontcallmedom)(first contribution to Data). - Add
`place-items`

property. ([PR 252](https://github.com/mdn/data/pull/252)), from[Connor Shea](https://github.com/connorshea)(first contribution to Data). - Add MDN URLs to CSS properties data (
[PR 256](https://github.com/mdn/data/pull/256)), Add MDN URLs to at-rules data ([PR 258](https://github.com/mdn/data/pull/258)), and[3 more PRs](https://github.com/mdn/data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31"+author:ddbeck)from[Daniel D. Beck](https://github.com/ddbeck)(first contributions to Data). - Add initial value
`auto`

to`min-width`

and`min-height`

([PR 263](https://github.com/mdn/data/pull/263)), and Rename the`offset-`

logical properties to`inset-`

([PR 273](https://github.com/mdn/data/pull/273)), from[Rachel Andrew](https://github.com/rachelandrew)(first contributions to Data). - Add
`media-document(<string>)`

to`@document`

([PR 268](https://github.com/mdn/data/pull/268)), from[Estelle Weyl](https://github.com/estelle)(first contribution to Data). - Create code examples for Variable Fonts Guide (
[PR 4](https://github.com/mdn/css-examples/pull/4)), Update widths and spacing ([PR 5](https://github.com/mdn/css-examples/pull/5)), and[2 more PRs](https://github.com/mdn/css-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-08-01..2018-08-31"+author:jpamental)to css-examples from[Jason Pamental](https://github.com/jpamental). - Fix spelling error (
[learning-area PR 74](https://github.com/mdn/learning-area/pull/74)), from[Utkarsh Nag](https://github.com/utkarshnag). - Fix spelling error (
[learning-area PR 91](https://github.com/mdn/learning-area/pull/91)), from[LittleMang](https://github.com/LittleMang). - Make minor adjustments to the setup instructions (
[sw-test PR 28](https://github.com/mdn/sw-test/pull/28)), from[Zunino](https://github.com/Zunino). - Add audio analyser (
[webaudio-examples PR 7](https://github.com/mdn/webaudio-examples/pull/7)), from[peterchang](https://github.com/wahengchang).

## Planned for September

In September, we’ll continue working on new and improved interactive examples, converting compatibility data, migrating MDN services, and other long-term projects.

### Hack on accessibility

We’re happy with the results of the [Paris Hack on MDN event](https://hacks.mozilla.org/2018/03/hack-on-mdn-building-useful-tools-with-browser-compatibility-data/) in March, and are doing it again in September. MDN staff will meet in London for a week of meetings and 2019 planning, and then have the fourth [Hack on MDN event](https://wiki.mozilla.org/MDN/Hack_on_MDN), focusing on accessibility. We plan to write docs, build tools, and explore ways to help web developers make the internet more accessible for all users.

### Ship more performance improvements

We’ll continue working on the suggested performance improvements, to meet the [performance goals](https://github.com/mdn/mdn-fiori/wiki) for the year.

One area for improvement is optimizing MDN’s use of custom web fonts. These fonts often need to be downloaded, increasing page load time. Some plugins and clients, like [Firefox Focus](https://www.mozilla.org/en-US/firefox/mobile/), improve the mobile experience by blocking these by default. Our goal is to improve the experience for desktop users by downloading optimized fonts after the initial page load, and avoiding required custom fonts like FontAwesome for icons.

Another focus is Interactive Examples, which are useful but have a large impact on page load time. [James Hobin](https://github.com/hobinjk) is working through the requirements to [load the examples directly into the page](https://github.com/mdn/sprints/issues/264), rather than via an `<iframe>`

. Schalk is improving the [asset builder](https://github.com/mdn/bob) for new features and for optimized asset building.

## About John Whitlock

John is a web developer working on the engine of MDN Web Docs