---
title: 'Performance Updates and Hosting Moves: MDN Changelog for October 2018 – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2018/11/performance-and-hosting-moves-mdn-changelog-for-october-2018/
author: John Whitlock
published: '2018-11-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Done in October

Here’s what happened in October to the [code, data, and tools](https://github.com/mdn/) that support [MDN Web Docs](https://developer.mozilla.org):

[Shipped performance improvements](https://hacks.mozilla.org#shipped-performance-improvements)[Moved MDN to MozIT](https://hacks.mozilla.org#moved-mdn-to-mozit)[Shipped tweaks and fixes](https://hacks.mozilla.org#shipped-tweaks-and-fixes)by merging 352 pull requests, including 78 pull requests from 62 new contributors.

Here’s the plan for November:

We shipped some changes designed to improve MDN’s page load time. The effects were not as significant as we’d hoped.

### Shipped performance improvements

Our sidebars, like the Related Topics sidebar on [<summary>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/summary), use a “mozToggler” JavaScript method to implement open and collapsed sections. This uses [jQueryUI’s toggle effect](https://jqueryui.com/toggle/), and is applied dynamically at load time. [Tim Kadlec](https://github.com/tkadlec) replaced it with the [<details> element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details) ([KumaScript PR 789](https://github.com/mdn/kumascript/pull/789) and [Kuma PR 4957](https://github.com/mozilla/kuma/pull/4957)), which semantically models open and collapsed sections. The `<details>`

element is supported by most current browsers, with the notable exception of Microsoft Edge, which is supported with a polyfill.

The `<details>`

update shipped October 4th, and the 31,000 pages with sidebars were regenerated to apply the change.

A second change was intended to reduce the use of [Web Fonts](https://developer.mozilla.org/en-US/docs/Learn/CSS/Styling_text/Web_fonts), which must be downloaded and can cause the page to be repainted. Some browsers, such as [Firefox Focus](https://www.mozilla.org/en-US/firefox/mobile/), block web fonts by default for performance and to save bandwidth.

One strategy is to eliminate the web font entirely. We replaced [OpenSans](https://www.opensans.com/) with the built-in Verdana as the body font in September ([PR 4967](https://github.com/mozilla/kuma/pull/4967)), and then again with Arial on October 22 ([PR 5023](https://github.com/mozilla/kuma/pull/5023)). We’re also replacing [Font Awesome](https://fontawesome.com/), implemented with a web font, with inline SVG ([PR 4969](https://github.com/mozilla/kuma/pull/4969) and [PR 5053](https://github.com/mozilla/kuma/pull/5053)). We expect to complete the SVG work in November.

A second strategy is to reduce the size of the web font. The custom Zilla font, introduced with the [June 2017](https://mozilla.github.io/meao/2017/07/06/kuma-report/) redesign, was reduced to standard English characters, cutting the file sizes in half on October 10 ([PR 5024](https://github.com/mozilla/kuma/pull/5024)).

These changes have had an impact on total download size and rendering time, and we’re seeing improvements in our [synthetic metrics](https://speedcurve.com/features/synthetic/). However, there has been [no significant change in page load](https://github.com/mdn/sprints/issues/258#issuecomment-428225500) as measured for MDN users. In November, we’ll try some more radical experiments to learn more about the components of page load time.

![A graph of page load over time, declining noisily from 5 - 6 seconds to 4 -5 seconds over October](../../assets/2efabf49c501ae3e.png)

SpeedCurve Synthetic measurements show steady improvement, but not yet on target.

### Moved MDN to MozIT

[Ryan Johnson](https://github.com/escattone), [Ed Lim](https://github.com/limed), and [Dave Parfitt](https://github.com/metadave) switched production traffic from the Marketing to the IT servers on October 29th. The site was placed in read-only mode, so all the content was available during the transition. There were some small hiccups, mostly around running out of API budget for [Amazon’s Elastic File System](https://aws.amazon.com/efs/) (EFS), but we handled the issues within the maintenance window.

In the weeks leading up to the cut over, the team tested deployments, updated documentation, and checked data transfer processes. They created a list of tasks and assignments, detailed the process for the migration, and planned the cleanup work after the cut over. The team’s attention to detail and continuous communication made this a smooth transition for MDN’s users, with no downtime or bugs.

The MozIT cluster is very similar to the previous MozMEAO cluster. The [technical overview](https://mozilla.github.io/meao/2017/11/07/kuma-report/#aws-intro) from the October 10, 2017 launch is still a decent guide to how MDN is deployed.

There are a handful of changes, most of which MDN users shouldn’t notice. We’re now hosting images in [Docker Hub](https://hub.docker.com/u/mdnwebdocs/) rather than [quay.io](https://quay.io/). The MozMEAO cluster ran Kubernetes 1.7, and the new MozIT cluster runs 1.9. This may be responsible for more reliable DNS lookups, avoiding occasional issues when connecting to the database or other AWS services.

In November, we’ll continue monitoring the new servers, and shut down the redundant services in the MozMEAO account. We’ll then re-evaluate our plans from the beginning of the year, and prioritize the next infrastructure updates. The top of the list is reliable acceptance tests and deploys across multiple AWS zones.

### Shipped tweaks and fixes

There were 352 PRs merged in October:

[127 mdn/browser-compat-data PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[48 mozilla/kuma PRs](https://github.com/mozilla/kuma/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[45 mdn/kumascript PRs](https://github.com/mdn/kumascript/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[39 mdn/interactive-examples PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[32 mdn/infra PRs](https://github.com/mdn/infra/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[25 mdn/bob PRs](https://github.com/mdn/bob/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[10 mdn/webaudio-examples PRs](https://github.com/mdn/webaudio-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[6 mdn/data PRs](https://github.com/mdn/data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[4 mdn/ansible-jenkins PRs](https://github.com/mdn/ansible-jenkins/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[2 mdn/web-components-examples PRs](https://github.com/mdn/web-components-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[2 mdn/css-examples PRs](https://github.com/mdn/css-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[2 mdn/imsc PRs](https://github.com/mdn/imsc/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[2 mdn/short-descriptions PRs](https://github.com/mdn/short-descriptions/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[1 mdn/django-locallibrary-tutorial PR](https://github.com/mdn/django-locallibrary-tutorial/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[1 mdn/learning-area PR](https://github.com/mdn/learning-area/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[1 mdn/webextensions-examples PR](https://github.com/mdn/webextensions-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[1 mdn/web-tech-games PR](https://github.com/mdn/web-tech-games/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[1 mdn/pwa-examples PR](https://github.com/mdn/pwa-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[1 mdn/fibonacci-worker PR](https://github.com/mdn/fibonacci-worker/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[1 mdn/sprints PR](https://github.com/mdn/sprints/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")[1 mdn/express-locallibrary-tutorial PR](https://github.com/mdn/express-locallibrary-tutorial/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")

This includes some important changes and fixes:

- Fix anchor links like
[#Using_thisArg](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach#Using_thisArg)([Kuma PR 4954](https://github.com/mozilla/kuma/pull/4954)), from[Schalk Neethling](https://github.com/schalkneethling). - Add permissive
[Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)(CSP) ([Kuma PR 5002](https://github.com/mozilla/kuma/pull/5002)), from[me](https://github.com/jwhitlock). - Prefer
`.blockIndicator`

for styling block indicators ([KumaScript PR 830](https://github.com/mdn/kumascript/pull/830)), part of a series of changes to standardize[indicators](https://developer.mozilla.org/en-US/docs/Sandbox/All-Indicators)from[ExE Boss](https://github.com/ExE-Boss). - Remove the
`localize`

macro ([KumaScript PR 897](https://github.com/mdn/kumascript/pull/897)), from[wbamberg](https://github.com/wbamberg), one of 25 macros removed in the[macro massacre](https://github.com/mdn/kumascript/pulls?q=is%3Apr+is%3Aclosed+merged%3A2018-10-01..2018-10-31+label%3A%22Macro+massacre%22). - A
[step sequencer demo](https://mdn.github.io/webaudio-examples/step-sequencer/)([webaudio-examples PR 13](https://github.com/mdn/webaudio-examples/pull/13)), one of[several audio demos](https://github.com/mdn/webaudio-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31")from[Ruth John](https://github.com/Rumyra).

78 pull requests were from first-time contributors:

- Add details for MS Edge support of
`SubtleCrypto`

([BCD PR 2738](https://github.com/mdn/browser-compat-data/pull/2738)), from[Wim L](https://github.com/wiml). - Add support for CSS property
`-moz-image-region`

([BCD PR 2853](https://github.com/mdn/browser-compat-data/pull/2853)), from[Shivam Singhal](https://github.com/championshuttler). - Add browser versions for CSS property
`scroll-snap-type`

([BCD PR 2867](https://github.com/mdn/browser-compat-data/pull/2867)), from[Chris Bitsakis](https://github.com/northamerican). - Add data for
`overflow-clip-box-*`

,`-moz-user-focus`

, and (`-moz-`

)`user-modify`

([PR 2868](https://github.com/mdn/browser-compat-data/pull/2868)), Add data for many non-standard CSS properties/selectors ([PR 2874](https://github.com/mdn/browser-compat-data/pull/2874)), and[11 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-10-01..2018-10-31"+author:vinyldarkscratch)to BCD from[Vinyl Darkscratch](https://github.com/vinyldarkscratch). - Add Edge support for
`Intl`

([BCD PR 2882](https://github.com/mdn/browser-compat-data/pull/2882)), from[Jack Horton](https://github.com/jackhorton). - Add Edge 18 and supported features (
[BCD PR 2907](https://github.com/mdn/browser-compat-data/pull/2907)), from[Merih Akar](https://github.com/merih). - Fix typo (“performace.now()” to “performance.now()”) (
[BCD PR 2914](https://github.com/mdn/browser-compat-data/pull/2914)), from[Merlin Luntke](https://github.com/Luntke). - Update to extend 3.0.2 (
[BCD PR 2916](https://github.com/mdn/browser-compat-data/pull/2916)), from[Jonathan Felchlin](https://github.com/GreenGremlin). - Update Firefox’s supported
`<iframe sandbox>`

attributes ([BCD PR 2919](https://github.com/mdn/browser-compat-data/pull/2919)), from[Dan Callahan](https://github.com/callahad). - Fix typo and link to
[capabilities](https://developer.mozilla.org/en-US/docs/Web/WebDriver/Capabilities)on MDN ([BCD PR 2930](https://github.com/mdn/browser-compat-data/pull/2930)), from[Andreas Tolfsen](https://github.com/andreastt). - Add Edge Mobile’s support of
`<input type=date>`

([BCD PR 2932](https://github.com/mdn/browser-compat-data/pull/2932)), from[Jeff Powell](https://github.com/jeffrpowell). - Add IE’s partial support of
`HTMLHyperlinkElementUtils.pathname`

([BCD PR 2934](https://github.com/mdn/browser-compat-data/pull/2934)), from[wizzwizz4](https://github.com/wizzwizz4). - Add Firefox 57 support for
`MediaPlayPause`

([BCD PR 2936](https://github.com/mdn/browser-compat-data/pull/2936)), from[Carlin Scott](https://github.com/carlin-q-scott). - Add note that IE does not support
`Node.contains`

for SVG elements ([BCD PR 2942](https://github.com/mdn/browser-compat-data/pull/2942)), from[Pascal Duez](https://github.com/pascalduez). - Add notes for
`Origin`

header change in Firefox 59 ([BCD PR 2943](https://github.com/mdn/browser-compat-data/pull/2943)), from[Théophile Helleboid – chtitux](https://github.com/chtitux). - Add support details for
`FontFaceSet`

API in Chromium and Opera ([BCD PR 2948](https://github.com/mdn/browser-compat-data/pull/2948)), from[Gerhard Preuss](https://github.com/lipp). - Update IE support for
`window.scrollBy`

([BCD PR 2975](https://github.com/mdn/browser-compat-data/pull/2975)), from[Mathieu Lemoine](https://github.com/lemoinem). - Add Safari 11.1 support for
`CacheStorage`

API ([BCD PR 2976](https://github.com/mdn/browser-compat-data/pull/2976)), from[Jianrong Yu](https://github.com/YuJianrong). - Update Chrome’s and Opera’s support for
`MediaRecorder`

([PR 2977](https://github.com/mdn/browser-compat-data/pull/2977)), Update`Selection`

support in Chrome and Opera ([PR 3032](https://github.com/mdn/browser-compat-data/pull/3032)), and Update`ImageBitmap`

API support ([PR 3033](https://github.com/mdn/browser-compat-data/pull/3033)), to BCD from[Xiaoru Li](https://github.com/hexrcs). - Change Edge 17 to partial support for
`fieldset`

`disabled`

attribute ([PR 2978](https://github.com/mdn/browser-compat-data/pull/2978)), and Change IE 9 to partial support for`box-shadow`

`inset`

([PR 2996](https://github.com/mdn/browser-compat-data/pull/2996)), to BCD from[Bart Groeneveld](https://github.com/BartG95). - Add notes that Edge support for
`CustomElements`

and`ShadowDOM`

is in development ([BCD PR 2982](https://github.com/mdn/browser-compat-data/pull/2982)), from[Jim Montgomery](https://github.com/jimmont). - Add details of browser support for CSS
`all`

([BCD PR 2986](https://github.com/mdn/browser-compat-data/pull/2986)), from[Pier Bover](https://github.com/PierBover). - Add Safari versions that support
`FormData`

methods ([BCD PR 2988](https://github.com/mdn/browser-compat-data/pull/2988)), from[Rouven Bühlmann](https://github.com/nirazul). - Remove Edge support for
`::cue selector`

([BCD PR 2998](https://github.com/mdn/browser-compat-data/pull/2998)), from[Clement Allen](https://github.com/clementallen). - Add Android WebView 61 support for JavaScript
`import`

([BCD PR 3001](https://github.com/mdn/browser-compat-data/pull/3001)), from[happy-monk](https://github.com/happy-monk). - Add IE and Safari support for
`document.createComment`

([BCD PR 3003](https://github.com/mdn/browser-compat-data/pull/3003)), from[Giordano Ricci](https://github.com/Elfo404). - Add Edge 12 support for
`Element.scrollIntoView`

([BCD PR 3006](https://github.com/mdn/browser-compat-data/pull/3006)), from[Michel Plungjan](https://github.com/mplungjan). - Add support for CSS properties
`block-size`

and`inline-size`

([BCD PR 3012](https://github.com/mdn/browser-compat-data/pull/3012)), from[cartinez](https://github.com/cartinez). - Add Edge 18 support for
`Promise.finally`

([BCD PR 3013](https://github.com/mdn/browser-compat-data/pull/3013)), from[Pedro Barbiero](https://github.com/Barbiero). - Add Chrome 69 support for
`OffscreenCanvas`

without a flag ([PR 3017](https://github.com/mdn/browser-compat-data/pull/3017)), and Add Chrome 69 support for`transferControlToOffscreen`

without a flag ([PR 3019](https://github.com/mdn/browser-compat-data/pull/3019)), to BCD from[SMUsamaShah](https://github.com/SMUsamaShah). - Add Edge 15 support for Brotli compression (
[BCD PR 3023](https://github.com/mdn/browser-compat-data/pull/3023)), from[Jacob Stamm](https://github.com/stamminator). - Remove Safari support for
`Element.animate`

([BCD PR 3028](https://github.com/mdn/browser-compat-data/pull/3028)), from[Jérémy Thulliez](https://github.com/zthulj). - Fix alternative names for
`WebGL`

in Firefox ([BCD PR 3029](https://github.com/mdn/browser-compat-data/pull/3029)), from[Anis Ladram](https://github.com/anis-ladram). - Add Safari 7 support for
`document.createComment`

([BCD PR 3037](https://github.com/mdn/browser-compat-data/pull/3037)), from[Ben Keith](https://github.com/benlk). - Add accessible text to social icons (
[PR 5000](https://github.com/mozilla/kuma/pull/5000)), from[Hidde de Vries](https://github.com/hidde)(first contribution to Kuma). - Hide code line numbers from screen readers (
[PR 5047](https://github.com/mozilla/kuma/pull/5047)), from[arai-a](https://github.com/arai-a)(first contribution to Kuma). - Fix hash link on pages without Table of Contents (
[Kuma PR 5057](https://github.com/mozilla/kuma/pull/5057)), from[urty5656](https://github.com/urty5656). - Add Stripe customer ID to MDN user record (
[Kuma PR 5059](https://github.com/mozilla/kuma/pull/5059)), from[Michal Macioszczyk](https://github.com/michal-macioszczyk). - Update sidebars to use details/summary (
[PR 789](https://github.com/mdn/kumascript/pull/789)), from[tkadlec](https://github.com/tkadlec)(first contribution to KumaScript). - Change wording of vendor prefix note in compatibility table (
[PR 806](https://github.com/mdn/kumascript/pull/806)), from[Connor Shea](https://github.com/connorshea)(first contribution to KumaScript). - Remove lightweight themes from the sidebar. (
[PR 965](https://github.com/mdn/kumascript/pull/965)), from[Irene Smith](https://github.com/irenesmith)(first contribution to KumaScript). - Use
`+=`

instead of`a = a + x`

([PR 1171](https://github.com/mdn/interactive-examples/pull/1171)), from a now[deleted user](https://github.com/ghost)(first contribution to Interactive Examples). - Add example for headings
`<h1>`

through`<h6>`

([Interactive Examples PR 1180](https://github.com/mdn/interactive-examples/pull/1180)), from[Tremaine Neethling](https://github.com/TremaineNeethling). - Update JavaScript
`Object.entries`

example ([Interactive Examples PR 1182](https://github.com/mdn/interactive-examples/pull/1182)), from[Raju Gautam](https://github.com/GAUTAMRAJU15). - Use template strings to improve readability (
[Interactive Examples PR 1187](https://github.com/mdn/interactive-examples/pull/1187)), from[Flying-Toast](https://github.com/Flying-Toast). - Add “attribute-“ prefix to HTML attribute examples (
[Interactive Examples PR 1189](https://github.com/mdn/interactive-examples/pull/1189)), from[Dimitri Belopopsky](https://github.com/ShadowMitia). - Fix bug in
`String.normalize`

live example ([Interactive Examples PR 1193](https://github.com/mdn/interactive-examples/pull/1193)), from[Eugene Dzhumak](https://github.com/ElForastero). - Use consistent white space, switch to arrow functions, and address other nits (
[webaudio-examples PR 20](https://github.com/mdn/webaudio-examples/pull/20)), from[Stoyan](https://github.com/stoyan). - Add
`:blank`

CSS selector data ([PR 298](https://github.com/mdn/data/pull/298)), from[Michal Čaplygin](https://github.com/myfonj)(first contribution to Data). - Correct the list of observed attributes (
[web-components-examples PR 10](https://github.com/mdn/web-components-examples/pull/10)), from[LordRegentTB](https://github.com/LordRegentTB). - Improve edit-word demo (
[web-components-examples PR 11](https://github.com/mdn/web-components-examples/pull/11)), from[Jan Murmann](https://github.com/Silvester23). - Remove warning about Firefox 33 from
`@counter-style`

demo ([css-examples PR 10](https://github.com/mdn/css-examples/pull/10)), from[Razvan Caliman](https://github.com/oslego). - Add minimal
`ttml`

sample for live preview ([imsc PR 3](https://github.com/mdn/imsc/pull/3)), from[Andreas Tai](https://github.com/tairt). - Add inline styles example (
[imsc PR 4](https://github.com/mdn/imsc/pull/4)), from[Pierre-Anthony Lemieux](https://github.com/palemieux). - Add initial license info (
[PR 1](https://github.com/mdn/short-descriptions/pull/1)), from[Daniel D. Beck](https://github.com/ddbeck)(first contribution to short-descriptions). - Add guidelines for CSS short descriptions (
[PR 3](https://github.com/mdn/short-descriptions/pull/3)), from[wbamberg](https://github.com/wbamberg)(first contribution to short-descriptions). - Update
`var`

to`let`

([learning-area PR 106](https://github.com/mdn/learning-area/pull/106)), from[Lisa Tidball](https://github.com/li3097). - Make website responsive (
[web-tech-games PR 2](https://github.com/mdn/web-tech-games/pull/2)), from[Purushottam Sharma](https://github.com/pm-sharma). - Reduce image sizes for A2HS demo (
[pwa-examples PR 9](https://github.com/mdn/pwa-examples/pull/9)), from[Nemo](https://github.com/captn3m0). - Change the
`var`

keyword to`let`

([fibonacci-worker PR 3](https://github.com/mdn/fibonacci-worker/pull/3)), from[Varsha Chahal](https://github.com/VarshaChahal). - Add custom issue template to replace Bugzilla documentation requests (
[PR 505](https://github.com/mdn/sprints/pull/505)), from[Janet Swisher](https://github.com/jmswisher)(first contribution to sprints). - Add authentication and role-based authorization (
[express-locallibrary-tutorial PR 54](https://github.com/mdn/express-locallibrary-tutorial/pull/54)), from[Caglar Turali](https://github.com/caglarturali).

## Planned for November

We’ll continue on performance experiments in November, such as removing Font Awesome and looking for new ways to lower page load time. We’ll continue ongoing projects, such as migrating and updating browser compatibility data and shipping more HTML examples like the one on [<input>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Input).

### Ship recurring payments

In October, we shipped [a new way to support MDN](https://hacks.mozilla.org/2018/10/a-new-way-to-support-mdn/) with one-time payments. For November, we’re working with [Potato London](https://p.ota.to/) again to add the option for monthly payments to MDN.

Interested in contributing to MDN? Don’t miss [Getting started on MDN](https://developer.mozilla.org/en-US/docs/MDN/Getting_started) or jump right in to the [Kuma repo](https://github.com/mozilla/kuma/blob/master/CONTRIBUTING.md) to begin contributing code.

If you’re just getting started, take a look at the MDN wiki page for new contributors or have a look at

## About John Whitlock

John is a web developer working on the engine of MDN Web Docs

## 5 comments

AndersNovember 10th, 2018 at 00:24RaphaelNovember 10th, 2018 at 01:27DDNovember 10th, 2018 at 13:43Kadir TopalNovember 11th, 2018 at 16:32AndersNovember 14th, 2018 at 13:44