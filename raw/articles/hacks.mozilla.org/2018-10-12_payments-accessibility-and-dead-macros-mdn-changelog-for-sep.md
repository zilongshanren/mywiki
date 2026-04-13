---
title: 'Payments, accessibility, and dead macros: MDN Changelog for September 2018
  – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2018/10/payments-accessibility-and-dead-macros-mdn-changelog-for-september-2018/
author: John Whitlock
published: '2018-10-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Done in September

Here’s what happened in September to the [code, data, and tools](https://github.com/mdn/) that support [MDN Web Docs](https://developer.mozilla.org):

[Launched MDN payments](https://hacks.mozilla.org#launched-mdn-payments)[Improved MDN’s accessibility resources](https://hacks.mozilla.org#improved-mdns-accessibility-resources)[Removed 15% of KumaScript macros](https://hacks.mozilla.org#removed-15-of-kumascript-macros)[Shipped tweaks and fixes](https://hacks.mozilla.org#shipped-tweaks-and-fixes)by merging 379 pull requests, including 66 pull requests from 38 new contributors.

Here’s the plan for October:

### Launched MDN payments

We’ve been thinking about the direction and growth of MDN. We’d like a more direct connection with developers, and to provide them with valuable features and benefits they need to be successful in their web projects. We’ve researched several promising ideas, and decided that direct payments would be the first experiment. Logged-in users and 1% of anonymous visitors see the banner that asks them to directly support MDN. See Ali Spivak’s and Kadir Topal’s post, [A New Way to Support MDN](https://hacks.mozilla.org/2018/10/a-new-way-to-support-mdn/), for more information.

![Payment page on MDN](../../assets/9b5a5460cdf6c4dd.png)

Payment page on MDN

The implementation phase started in August, when [Potato London](https://p.ota.to/) was hired to design and implement payments. Potato did an amazing job executing on a 5-week schedule, including several design meetings, daily standups, and a trip from Bristol to London to meet face-to-face during the MDN work week. Thanks to the hard work from the Potato team, including Charlie Harding, [Josh Jarvis](https://github.com/joshJarr), [Matt Hall](https://github.com/matthewhall), [Michał Macioszczyk](https://github.com/michal-macioszczyk), Philip Lackmaker, and Rachel Lee.

Mozilla staff across the organization helped keep this project on schedule, from writing copy to security reviews to [pull request reviews and fixes](https://github.com/mozilla/kuma/pulls?page=3&q=is%3Apr+is%3Aclosed), including me, Ali Spivak, Caglar Ulucenk, Diane Tate, Havi Hoffman, [Kadir Topal](https://github.com/atopal), Kevin Fann, [Ryan Johnson](https://github.com/escattone), and [Schalk Neethling](https://github.com/schalkneethling).

After the work week, we met with accessibility experts for the Hack on MDN event. Volunteers and staff improved MDN’s coverage of accessibility. This included discussions of accessibility topics, improving and expanding MDN’s documentation, and writing related blog posts. It also included code changes, improving MDN’s color contrast and adding markup for screen readers. See Janet Swisher’s [Hack on MDN: Better accessibility for MDN Web Docs](https://hacks.mozilla.org/2018/10/hack-on-mdn-better-accessibility-for-mdn-web-docs/) for the details.

Seren Davies ([@ninjanails](https://twitter.com/ninjanails)) was there, and many nails were painted.

![A circle of people showing their painted nails and looking at the camera](../../assets/43b05f75a7525780.jpg)


![A circle of people showing their painted nails and looking at the camera](../../assets/43b05f75a7525780.jpg)

Clockwise from the top: Chris Mills (*headless mode*), Glenda Sims, Bruce Lawson (with camera), Irene Smith, Estelle Weyl, Michiel Bijl, and Seren Davies

### Removed 15% of KumaScript macros

The MDN team got together for a week at the London office to reflect on the quarter and plan the coming year.

We discussed KumaScript, our macro language and rendering service that implements standardized sidebars, banners, and internal links. It’s been easier to analyze macros since we moved them to GitHub in [November 2016](https://groups.google.com/d/msg/mozilla.dev.mdn/MJHUaWtF0mU/cKppYPz0CwAJ). We’re happy with the performance gains, but code reviews take forever, translations are hard, and we’re slow to write [tests](https://github.com/mdn/kumascript/tree/master/tests/macros). These issues contributed to an incident in August where a sidebar macro was broken, and all the API reference pages showed an error for a day ([bug 1487640](https://bugzilla.mozilla.org/show_bug.cgi?id=1487640)).

Staff is getting impatient with KumaScript, and wants to replace it with something better. Florian wrote up the notes from the meeting on Discourse as [Next steps for KumaScript](https://discourse.mozilla.org/t/next-steps-for-kumascript/32227).

[Florian](https://github.com/Elchi3), [Will Bamberg](https://github.com/wbamberg), and [Ryan Johnson](https://github.com/escattone) started on the first step, identifying and removing unused or seldom-used macros, such as [hello.ejs](https://github.com/mdn/kumascript/blob/8462c9db6da3b00f1dd84004609e03ad49e698c3/macros/hello.ejs). ([PR 849](https://github.com/mdn/kumascript/pull/849)).

The team removed [72 macros](https://github.com/mdn/kumascript/pulls?q=is%3Apr+is%3Aclosed+merged%3A2018-09-01..2018-09-30+label%3A%22Macro+massacre%22) in about 2 weeks, and will continue removing them for the rest of the year. This will leave a [smaller number of important macros](https://developer.mozilla.org/en-US/dashboards/macros), and we can analyze them for the next steps in the project.

### Shipped tweaks and fixes

There were 379 PRs merged in September:

[135 mdn/browser-compat-data PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")[83 mdn/kumascript PRs](https://github.com/mdn/kumascript/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")[47 mozilla/kuma PRs](https://github.com/mozilla/kuma/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")[38 mdn/interactive-examples PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")[28 mdn/infra PRs](https://github.com/mdn/infra/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")[24 mdn/bob PRs](https://github.com/mdn/bob/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")[10 mdn/data PRs](https://github.com/mdn/data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")[4 mdn/learning-area PRs](https://github.com/mdn/learning-area/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")[3 mdn/webaudio-examples PRs](https://github.com/mdn/webaudio-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")[2 mdn/dom-examples PRs](https://github.com/mdn/dom-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")[2 mdn/webextensions-examples PRs](https://github.com/mdn/webextensions-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")[1 mdn/django-locallibrary-tutorial PR](https://github.com/mdn/django-locallibrary-tutorial/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")[1 mdn/ansible-jenkins PR](https://github.com/mdn/ansible-jenkins/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")[1 mdn/css-examples PR](https://github.com/mdn/css-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30")

This includes some important changes and fixes:

`EmbedLiveSample`

: Avoid XSS, and add`allow=`

parameter ([KumaScript PR 786](https://github.com/mdn/kumascript/pull/786)), from[me](https://github.com/jwhitlock). This and related PRs fix live samples, like[media constraints](https://developer.mozilla.org/en-US/docs/Web/API/Media_Streams_API/Constraints#Result), that broke when Chrome and Safari began enforcing feature policies in an`<iframe>`

. See[Google’s explainer page](https://goo.gl/EuHzyv),[Policy Controlled Features](https://github.com/WICG/feature-policy/blob/master/features.md), and[bug 1482159](https://bugzilla.mozilla.org/show_bug.cgi?id=1482159).- End compat tables beta (
[KumaScript PR 860](https://github.com/mdn/kumascript/pull/860)) from[Florian Scholz](https://github.com/Elchi3), and[Kuma PR 4988](https://github.com/mozilla/kuma/pull/4988)from[Stephanie Hobson](https://github.com/stephaniehobson). With 96% of the data migrated, and more than 6,500 pages using the new layout, it was time to stop calling it a beta. - First chunk of unittest fixes for Python 3 (
[Kuma PR 4910](https://github.com/mozilla/kuma/pull/4910)), from[Anthony Maton](https://github.com/MatonAnthony). We plan to switching to Python 3 by the end of the year. - Update
`<div>`

example to use CC0 image ([Interactive Examples PR 1088](https://github.com/mdn/interactive-examples/pull/1088)), from[Eric Shepherd](https://github.com/a2sheppy), a continuing project to get consistent licensing for the interactive examples repository. - Add first iteration of console (
[bob PR 129](https://github.com/mdn/bob/pull/129)), from[Schalk Neethling](https://github.com/schalkneethling), a new feature for WebAPI interactive examples to see the output of JavaScript code snippets. - Remove certain contributions as part of relicensing plan (
[Data PR 294](https://github.com/mdn/data/pull/294)), and Change repo license to CC0 ([Data PR 301](https://github.com/mdn/data/pull/301)), from[Chris Mills](https://github.com/chrisdavidmills). This is part of a[4 month effort](https://github.com/mdn/data/issues/240)to change the license of the[mdn/data repo](https://github.com/mdn/data)and[mdn-data npm package](https://www.npmjs.com/package/mdn-data)to[CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/), to allow the data to be used in similar contexts as the[mdn-browser-compat-data npm package](https://www.npmjs.com/package/mdn-browser-compat-data)and data.

66 pull requests were from first-time contributors:

- Update compatibility data for
`onpopstate`

event ([BCD PR 2697](https://github.com/mdn/browser-compat-data/pull/2697)), from[Abhishek Gupta](https://github.com/a1626). - Update the data for
`ScreenOrientation`

([PR 2698](https://github.com/mdn/browser-compat-data/pull/2698)), from[Christophe Coevoet](https://github.com/stof)(first contribution to BCD). - Update
`flex-grow`

IE support ([BCD PR 2701](https://github.com/mdn/browser-compat-data/pull/2701)), from[Nils Lundquist](https://github.com/nlundquist). - Add compat data for CSS
`::-ms-value`

pseudo-element ([BCD PR 2708](https://github.com/mdn/browser-compat-data/pull/2708)), from[Andrew C. Dvorak](https://github.com/acdvorak). - Update compat data for
`Worker`

`name`

option ([BCD PR 2709](https://github.com/mdn/browser-compat-data/pull/2709)), from[Johan Holmerin](https://github.com/johanholmerin). - Add compat data for the webextension
`find`

optional permission ([PR 2710](https://github.com/mdn/browser-compat-data/pull/2710)), and Add compat data for the webextension`tabHide`

optional permission ([PR 2719](https://github.com/mdn/browser-compat-data/pull/2719)), to BCD from[glacambre](https://github.com/glacambre). - Update
`upgrade-insecure-requests`

Safari compatibility ([BCD PR 2729](https://github.com/mdn/browser-compat-data/pull/2729)), from[David Harbage](https://github.com/dharb). - Chrome does not defer scripts in XHTML (
[BCD PR 2754](https://github.com/mdn/browser-compat-data/pull/2754)), from[Franklin Tse](https://github.com/FranklinWhale). - Fix
`<script>`

`integrity`

for Edge and Safari ([PR 2765](https://github.com/mdn/browser-compat-data/pull/2765)), Update standard status for`immutable`

response ([PR 2793](https://github.com/mdn/browser-compat-data/pull/2793)), and[3 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30"+author:franklinyu)to BCD from[Franklin Yu](https://github.com/franklinyu). - Add JavaScript dynamic import support for Safari and IE (
[BCD PR 2785](https://github.com/mdn/browser-compat-data/pull/2785)), from[dhodder](https://github.com/dhodder). - Add
`partial-implementation`

to CSS’s`align-content`

([PR 2786](https://github.com/mdn/browser-compat-data/pull/2786)), Fix typo in`Node.ownerDocument`

notes ([PR 2787](https://github.com/mdn/browser-compat-data/pull/2787)), and[3 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30"+author:mpaktiti)to BCD from[Maria Paktiti](https://github.com/mpaktiti). - Update
`HTMLElement.click`

support table ([PR 2789](https://github.com/mdn/browser-compat-data/pull/2789)), and Update`HTMLFormElement.submit`

compat table ([PR 2796](https://github.com/mdn/browser-compat-data/pull/2796)), to BCD from[Daniel Smith](https://github.com/jellymann). - Fix
`RTCPeerConnection`

`connectionState`

compat information ([BCD PR 2815](https://github.com/mdn/browser-compat-data/pull/2815)), from[Philipp Hancke](https://github.com/fippo). - Mark the
`<menuitem>`

element as deprecated ([PR 2837](https://github.com/mdn/browser-compat-data/pull/2837)), Mark`<contextMenu>`

as deprecated ([PR 2838](https://github.com/mdn/browser-compat-data/pull/2838)), and[5 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30"+author:sideshowbarker)from[Michael[tm] Smith](https://github.com/sideshowbarker)(first contributions to BCD). - Add dynamic import status for MS Edge (
[BCD PR 2844](https://github.com/mdn/browser-compat-data/pull/2844)), from[dennisameling](https://github.com/dennisameling). - Correct
`RTCPeerConnection.canTrickleIceCandidates`

support ([BCD PR 2849](https://github.com/mdn/browser-compat-data/pull/2849)), from[Sean Bright](https://github.com/seanbright). - Update node.js support for
`Date[@@toPrimitive]`

([BCD PR 2865](https://github.com/mdn/browser-compat-data/pull/2865)), from[Fayti1703](https://github.com/Fayti1703). - Add Safari support for compatibility of
`navigator.onLine`

([BCD PR 2866](https://github.com/mdn/browser-compat-data/pull/2866)), from[Márcio Lucas R. Oliveira](https://github.com/marciioluucas). - Comment out the indicator
`:matches(…)`

block for now ([PR 4961](https://github.com/mozilla/kuma/pull/4961)), from[ExE Boss](https://github.com/ExE-Boss)(first contribution to Kuma). - Reduce web font usage (
[PR 4967](https://github.com/mozilla/kuma/pull/4967)), and Removing preload for Zilla Bold ([PR 4982](https://github.com/mozilla/kuma/pull/4982)), to Kuma from[tkadlec](https://github.com/tkadlec). - MDN Contribution payment flow implementation (
[PR 4970](https://github.com/mozilla/kuma/pull/4970)), Contribution views flow ([PR 4976](https://github.com/mozilla/kuma/pull/4976)), and[3 more PRs](https://github.com/mozilla/kuma/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-09-01..2018-09-30"+author:joshJarr)to Kuma from[Josh Jarvis](https://github.com/joshJarr). - Add more helpful technique for accessing
`Promise`

([Interactive Examples PR 1124](https://github.com/mdn/interactive-examples/pull/1124)), from[Dan Levy](https://github.com/justsml). - Handle new Jenkins / AWS services (
[PR 1135](https://github.com/mdn/interactive-examples/pull/1135)), Make`irc-notify.sh`

executable again ([PR 1136](https://github.com/mdn/interactive-examples/pull/1136)), and Make`awscli`

profile optional ([PR 1137](https://github.com/mdn/interactive-examples/pull/1137)), from[Ryan Johnson](https://github.com/escattone)(first contributions to Interactive Examples). - Each radio button in the group should have distinct
`value`

attribute ([Interactive Examples PR 1141](https://github.com/mdn/interactive-examples/pull/1141)), from[Konstantin Rouda](https://github.com/Konrud). - Fix incorrect label selector in password example (
[Interactive Examples PR 1147](https://github.com/mdn/interactive-examples/pull/1147)), from[Gene Wood](https://github.com/gene1wood). - Updating picture example to work better on small screens (
[PR 1149](https://github.com/mdn/interactive-examples/pull/1149)), from[Olle Lauri Boström](https://github.com/ollelauribostrom)(first contribution to Interactive Examples). - Increase colour contrast of comments in code examples (
[Interactive Examples PR 1159](https://github.com/mdn/interactive-examples/pull/1159)), from[Seren D](https://github.com/ninjanails). - Add password info for AES backup decryption (
[PR 63](https://github.com/mdn/infra/pull/63)), from[Dave Parfitt](https://github.com/metadave)(first contribution to infra). `rm -rf elbs`

([PR 86](https://github.com/mdn/infra/pull/86)), from[Josh Mize](https://github.com/jgmize)(first contribution to infra).- Update syntaxes to match latest specs (
[Data PR 104](https://github.com/mdn/data/pull/104)), from[Albert Scheiner](https://github.com/scheinercc). - Add the
`:matches(…)`

selector ([PR 284](https://github.com/mdn/data/pull/284)), Add the`||`

column combinator ([PR 285](https://github.com/mdn/data/pull/285)), and Add the`:has(…)`

selector ([PR 286](https://github.com/mdn/data/pull/286)), from[ExE Boss](https://github.com/ExE-Boss)(first contributions to Data). - Fix filename path in fallback paragraph (
[learning-area PR 94](https://github.com/mdn/learning-area/pull/94)), from[RACZ Andras](https://github.com/torzsmokus). - Remove unused variable (
[PR 95](https://github.com/mdn/learning-area/pull/95)), and Fix undefined variable ([PR 96](https://github.com/mdn/learning-area/pull/96)), to learning-area from[Xu Chunyang](https://github.com/xuchunyang). - Changed reference to female chickens from cock to hen. (
[PR 99](https://github.com/mdn/learning-area/pull/99)), from[Irene Smith](https://github.com/irenesmith)(first contribution to learning-area). - Add IIR Filter Demo (
[PR 10](https://github.com/mdn/webaudio-examples/pull/10)), and Add Audio Basics Demo ([PR 11](https://github.com/mdn/webaudio-examples/pull/11)), to webaudio-examples from[Ruth John](https://github.com/Rumyra). - Add IIR Filter Demo (
[PR 12](https://github.com/mdn/webaudio-examples/pull/12)), from[Chris Mills](https://github.com/chrisdavidmills)(first contribution to webaudio-examples). - Use
`switch`

,`srcObject`

, return`response.blob`

. Attempt to make video download not one time. ([dom-examples PR 28](https://github.com/mdn/dom-examples/pull/28)), from[ZaneHannanAU](https://github.com/ZaneHannanAU). - Fix grammar error in
`models.py`

([django-locallibrary-tutorial PR 22](https://github.com/mdn/django-locallibrary-tutorial/pull/22)), from[Leonard Meerwood](https://github.com/lmeerwood). - Enable
`apt`

to do automated security updates ([PR 4](https://github.com/mdn/ansible-jenkins/pull/4)), from[Ed Lim](https://github.com/limed)(first contribution to ansible-jenkins).

## Planned for October

October is the start of the fourth quarter. We have a few yearly goals to complete, including the Python 3 transition, the next round of the payments experiment, and performance experiments. This quarter also contains major holidays and the [Mozilla All Hands](https://wiki.mozilla.org/All_Hands/Orlando2018), which mean it has about half the working days of other quarters. Time to get to work!

### Move to Mozilla IT infrastructure

In October, [Ryan Johnson](https://github.com/escattone), [Ed Lim](https://github.com/limed), [Dave Parfitt](https://github.com/metadave), and [Josh Mize](https://github.com/jgmize) will complete the setup of MDN services in the Mozilla IT infrastructure, and switch production traffic to the new systems. This will complete the migration of MDN from Mozilla Marketing to Emerging Technologies, started in [February 2018](https://mozilla.github.io/meao/2018/03/08/mdn-changelog/). The team is organizing the switch-over checklist, and experimenting with the parallel staging environments.

The production switch is planned for October 29th, and will include a few hours when the site is in read-only mode.

## About John Whitlock

John is a web developer working on the engine of MDN Web Docs