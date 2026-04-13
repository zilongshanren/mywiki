---
title: '@media, MathML, and Django 1.11: MDN Changelog for May 2018 – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2018/06/media-mathml-and-django-1-11-mdn-changelog-for-may-2018/
author: John Whitlock
published: '2018-06-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s note:** *A changelog is “a log or record of all notable changes made to a project. [It] usually includes records of changes such as bug fixes, new features, etc.” Publishing a changelog is kind of a tradition in open source, and a long-time practice on the web. We thought readers of Hacks and folks who use and contribute to MDN Web Docs would be interested in learning more about the work of the MDN engineering team, and the impact they have in a given month. We’ll also introduce code contribution opportunities, interesting projects, and new ways to participate.*

## Done in May

Here’s what happened in May to the [code, data, and tools](https://github.com/mdn/) that support [MDN Web Docs](https://developer.mozilla.org):

[Migrated CSS @media and MathML compat data](https://hacks.mozilla.org#bcd-may-18)[Prepared for Django 1.11](https://hacks.mozilla.org#django-1-11-may-18)[Started tracking work in ZenHub](https://hacks.mozilla.org#zenhub-may-18)[Continued HTML Interactive Examples](https://hacks.mozilla.org#ie-may-18)[Shipped tweaks and fixes](https://hacks.mozilla.org#tweaks-may-18)by merging 397 pull requests, including 60 pull requests from 43 new contributors.

We’ll [continue this work](https://hacks.mozilla.org#continue-may-18) in June.

The browser compatibility migration continued, jumping from 72% to 80% complete. [Daniel D. Beck](https://github.com/ddbeck) completed the [CSS @media rule](https://developer.mozilla.org/en-US/docs/Web/CSS/@media) features, by converting data ([PR 2087](https://github.com/mdn/browser-compat-data/pull/2087) and a half-dozen others) and by reviewing PRs like [1977](https://github.com/mdn/browser-compat-data/pull/1977) from [Nathan Cook](https://github.com/nathancharles). [Mark Boas](https://github.com/maboa) finished up [MathML](https://developer.mozilla.org/en-US/docs/Web/MathML), submitting [26 pull requests](https://github.com/mdn/browser-compat-data/pulls?q=is%3Apr+is%3Aclosed+merged%3A2018-05-01..2018-05-31+author%3Amaboa+label%3A%22data%3Amathml+%3Aheavy_division_sign%3A%22).

There are over 8500 features in the BCD dataset, and half of the remaining work is already submitted as pull requests. We’re making steady progress toward completing the migration effort.

MDN runs on Django 1.8, the second long-term support (LTS) release. In May, we updated the code so that MDN’s test suite and core processes work on Django 1.8, 1.9, 1.10, and 1.11. We didn’t make it by the end of May, but by the time this report is published, we’ll be on Django 1.11 in production.

Many Mozilla web projects use Django, and most stick to the LTS releases. In 2015, the MDN team upgraded from Django 1.4 LTS to 1.7 in [PR 3073](https://github.com/mozilla/kuma/pull/3073/), which weighed in at 223 commits, 12,000 files, 1.2 million lines of code, and at least six months of effort. Django 1.8 followed six months later in [PR 3525](https://github.com/mozilla/kuma/pull/3525), a lighter change of 30 commits, 2,600 files, and 250,000 lines of code. After this effort, the team was happy to stick with 1.8 for a while.

Most of the upgrade pain was specific to [Kuma](https://developer.mozilla.org/en-US/docs/MDN/Kuma). The massive file counts were due to importing libraries as [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules), a common practice at the time for security, reliability, and customization. It was also harder to update libraries, which meant updates were often delayed until necessary. The 1.7 upgrade included an update from Python 2.6 to 2.7, and it is challenging to support dual-Python installs on a single web server.

The MDN team worked within some of these constraints, and tackled others. They re-implemented the development VM setup scripts in [Ansible](https://www.ansible.com/), but kept [Puppet](https://puppet.com/) for production. They updated submodules for the 1.7 effort, and switched to hashed requirements files for 1.8. A lot of codebase and process improvements were gained during the update effort. Other improvements, such as [Dockerized environments](https://www.docker.com/what-docker), were added later to avoid issues in the next big update.

[Django 1.4](https://docs.djangoproject.com/en/2.0/releases/1.4/) wasn’t originally planned as an LTS release, but instead was [scheduled for retirement](https://docs.djangoproject.com/en/2.0/releases/1.5/#python-compatibility) after the [1.6 release](https://docs.djangoproject.com/en/2.0/releases/1.6/). The end of support was repeatedly pushed further into the future, finally extending to [six months after 1.8 was published](https://groups.google.com/forum/#!topic/django-developers/W1sMVXwh8TU).

On the other hand, the Django team knew that [1.8 was an LTS release](https://docs.djangoproject.com/en/2.0/releases/1.8/) when they shipped it, and would get security updates for three years. Many of the Django team’s decisions in 2015 made MDN’s update easier. Django 1.11 retained Python 2.7 support, avoiding the pain of a simultaneous Python upgrade. Django now has a [predictable release process](https://docs.djangoproject.com/en/1.11/internals/release-process/), which is great for website and library maintainers.

Django also maintains [a guide on updating Django](https://docs.djangoproject.com/en/1.11/howto/upgrade-version/), and the suggested process worked well for us.

The [first step](https://docs.djangoproject.com/en/1.11/howto/upgrade-version/#dependencies) was to upgrade third-party libraries, which we’ve been working on for the past two years. Our goal was to get a library update into most production pushes, and we updated dozens of libraries while shipping unrelated features. Some libraries, such as [django-pipeline](https://github.com/jazzband/django-pipeline/pull/629), didn’t support Django 1.11, so we had to update them ourselves. In other cases, like [django-tidings](https://github.com/mozilla/django-tidings/pulls?q=is%3Apr+is%3Aclosed), we also had to take over project maintenance for a while.

The [next step](https://docs.djangoproject.com/en/1.11/howto/upgrade-version/#resolving-deprecation-warnings) was to turn on Django’s deprecation warnings, to find the known update issues. This highlighted a few more libraries to update, and also the big changes needed in our code. One problem area was our language-prefixed URLs. MDN uses Mozilla-standard language codes, such as `/en-US/`

, where the region is in capital letters. Django ships a [locale-prefixed URL framework](https://docs.djangoproject.com/en/1.11/topics/i18n/translation/#module-django.conf.urls.i18n), but uses lowercase language codes, such as `/en-us/`

. Mozilla’s custom framework broke in 1.9, and we tried a few approaches before copying Django’s framework and making adjustments for Mozilla-style language codes ([PR 4790](https://github.com/mozilla/kuma/pull/4790)).

Next we [ran our automated tests](https://docs.djangoproject.com/en/1.11/howto/upgrade-version/#testing), and started fixing the many failures. Our goal was to support multiple Django versions in a single codebase, and we added optional builds to TravisCI to run tests on 1.9, 1.10, and 1.11 ([PR 4806](https://github.com/mozilla/kuma/pull/4806)). We split the fixes into over 50 pull requests, and tested small batches of changes by deploying to production. In some cases, the same code works across all four versions. In other cases, we switched between code paths [based on the Django version](https://github.com/mozilla/kuma/pull/4807/commits/067382bc01c44627256fd1648ff4526ee196d870). Updates for Django 1.9 were about 90% of the upgrade effort.

This incremental approach is safer than a massive PR, and avoids issues with keeping a long-running branch up to date. It does make it harder to estimate the scope of a change. Looking at the commits that mention the [update bugs](https://bugzilla.mozilla.org/showdependencytree.cgi?id=1401246), we changed 2500 to 3000 lines, which represents 10% of the project code.

For the past two years, the MDN team had been using [Taiga](https://tree.taiga.io/project/viya-mdn-durable-team/) to plan and track our work in 3-week sprints. The team was unhappy with performance issues, and had been experimenting with GitHub’s project management features. [Janet Swisher](https://github.com/jmswisher) and [Eric Shepherd](https://github.com/a2sheppy) led an effort to explore alternatives. In May, we started using [ZenHub](https://www.zenhub.com/), which provides a sprint planning layer on top of GitHub issues and milestones.

If you have the ZenHub plugin installed, you can view the sprint board in the new [mdn/sprints](https://github.com/mdn/sprints/issues#boards?repos=121649843,55001853,70901646,134759439,90252175,1352520,3311772,82040629,121278372,33677290,132630865) repository, which collects tasks across our 10 active repositories. It adds additional data to GitHub issues and pull requests, linking them into project planning. If you don’t have the plugin, you can view the sprint board on the [ZenHub website](https://app.zenhub.com/workspace/o/mdn/sprints/boards). If you don’t want to sign in to ZenHub with your GitHub account, you can view the milestones in the individual projects, like the [Sprint 4 milestone](https://github.com/mdn/interactive-examples/milestone/6) in the [Interactive Examples project](https://hacks.mozilla.org/2018/03/bringing-interactive-examples-to-mdn/).

We’re still working through the technical challenges of shipping HTML interactive examples. One of the blocking issues was restricting style changes to the demo output on the right, but not the example code on the left. This is a use case for [Shadow DOM](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_shadow_DOM), which can restrict styles to a subset of elements. [Schalk Neethling](https://github.com/schalkneethling) shipped a solution based on Shadow DOM in [PR 873](https://github.com/mdn/interactive-examples/pull/873) and [PR 927](https://github.com/mdn/interactive-examples/pull/927), and it works natively in Chrome. [Not all current browsers support Shadow DOM](https://developer.mozilla.org/en-US/docs/Web/API/Element/attachShadow#Browser_compatibility), so Schalk added a shim in [PR 894](https://github.com/mdn/interactive-examples/pull/894). There are some [other issues](https://github.com/mdn/interactive-examples/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc+milestone%3A%22Sprint+4+Q2+2018%22) that we’ll continue to fix before including tabbed HTML examples on MDN.

Meanwhile, contributors from the global MDN community have written some interesting demos for [<track>](https://interactive-examples.mdn.mozilla.net/pages/tabbed/track.html) ([Leonard Lee](https://github.com/sheeeng), [PR 940](https://github.com/mdn/interactive-examples/pull/940)), [<map>](https://interactive-examples.mdn.mozilla.net/pages/tabbed/map.html) ([Adilson Sandoval](https://github.com/2alin), [PR 931](https://github.com/mdn/interactive-examples/pull/931)), and [<blockquote>](https://interactive-examples.mdn.mozilla.net/pages/tabbed/blockquote.html) ([Florian Scholz](https://github.com/Elchi3), [PR 906](https://github.com/mdn/interactive-examples/pull/906)). We’re excited to get these and the other examples on MDN.

There were 397 PRs merged in May:

[176 mdn/browser-compat-data PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-05-01..2018-05-31")[95 mdn/interactive-examples PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-05-01..2018-05-31")[70 mozilla/kuma PRs](https://github.com/mozilla/kuma/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-05-01..2018-05-31")[25 mdn/bob PRs](https://github.com/mdn/bob/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-05-01..2018-05-31")[16 mdn/data PRs](https://github.com/mdn/data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-05-01..2018-05-31")[8 mdn/kumascript PRs](https://github.com/mdn/kumascript/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-05-01..2018-05-31")[2 mdn/dom-examples PRs](https://github.com/mdn/dom-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-05-01..2018-05-31")[1 mdn/voice-change-o-matic PR](https://github.com/mdn/voice-change-o-matic/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-05-01..2018-05-31")[1 mdn/infra PR](https://github.com/mdn/infra/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-05-01..2018-05-31")[1 mdn/mdn PR](https://github.com/mdn/mdn/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-05-01..2018-05-31")[1 mdn/learning-area PR](https://github.com/mdn/learning-area/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-05-01..2018-05-31")[1 mdn/pwa-examples PR](https://github.com/mdn/pwa-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-05-01..2018-05-31")

60 of these were from first-time contributors:

- Chrome no longer supports
`caretPositionFromPoint`

([BCD PR 1909](https://github.com/mdn/browser-compat-data/pull/1909)), from[Micah Cowsik-Herstand](https://github.com/herstand). - Update MSE for
`EventHandlers`

attributes support ([BCD PR 1949](https://github.com/mdn/browser-compat-data/pull/1949)), from[Nicolas Le Gall](https://github.com/neovov). - Record that
`timeZone`

works ([BCD PR 1959](https://github.com/mdn/browser-compat-data/pull/1959)), from[Chris Angelico](https://github.com/Rosuav). - Mark the
`th`

`scope`

attribute as not deprecated ([PR 1960](https://github.com/mdn/browser-compat-data/pull/1960)), and Mark the`th`

`abbr`

attribute as not deprecated ([PR 1961](https://github.com/mdn/browser-compat-data/pull/1961)), to BCD from[Roland Warmerdam](https://github.com/Rowno). - Fix Chrome/Opera versions
`RTCPeerConnection.addTrack`

/`removeTrack`

(#1288) ([PR 1963](https://github.com/mdn/browser-compat-data/pull/1963)), from[Josiah Ulfers](https://github.com/julfers)(first contribution to BCD). - Update
`source`

element and its attributes for Safari desktop/iOS ([BCD PR 1964](https://github.com/mdn/browser-compat-data/pull/1964)), from[Josh Schneider](https://github.com/Josh68). - nodejs supports
`Error.prototype.stack`

([BCD PR 1970](https://github.com/mdn/browser-compat-data/pull/1970)), from[Chaim-Leib Halbert](https://github.com/chaimleib). - Enable
`append()`

for edge browser ([BCD PR 1973](https://github.com/mdn/browser-compat-data/pull/1973)), from[midzer](https://github.com/midzer). - Add compat data for css at-rules media
`any-hover`

([BCD PR 1977](https://github.com/mdn/browser-compat-data/pull/1977)), from[Nathan Cook](https://github.com/nathancharles). - EdgeHTML 17 updates (part 2) (
[BCD PR 1981](https://github.com/mdn/browser-compat-data/pull/1981)), from[Libby McCormick](https://github.com/libbymc). - Change MDN page for chrome support of
`AnimationEvent.pseudoElement`

([BCD PR 1986](https://github.com/mdn/browser-compat-data/pull/1986)), from[xidachen](https://github.com/xidachen). - Update Edge desktop & mobile support of
`text-decoration-style`

CSS property ([BCD PR 2004](https://github.com/mdn/browser-compat-data/pull/2004)), from[Lucas Volle](https://github.com/lrvolle). - Add
`HTMLIFrame`

element ([PR 2017](https://github.com/mdn/browser-compat-data/pull/2017)), from[SphinxKnight](https://github.com/SphinxKnight)(first contribution to BCD). - Update
`WorkerGlobalScope.importScripts`

([BCD PR 2046](https://github.com/mdn/browser-compat-data/pull/2046)), from[mantou](https://github.com/mantou132). - Update
`toLocaleString`

compat in Firefox Android ([BCD PR 2055](https://github.com/mdn/browser-compat-data/pull/2055)), from[Zacqary Adam Xeper](https://github.com/Zacqary). `SameSite`

supported in Firefox 60. ([BCD PR 2088](https://github.com/mdn/browser-compat-data/pull/2088)), from[Dominik Picheta](https://github.com/dom96).- Fix typo in
`<form>`

([BCD PR 2142](https://github.com/mdn/browser-compat-data/pull/2142)), from[acshef](https://github.com/acshef). - Add compatibility data for
`AudioNodeOptions`

([BCD PR 2160](https://github.com/mdn/browser-compat-data/pull/2160)), and Fix capitalization of Firefox’s`DocumentOrShadowRoot.fullscreenElement`

([BCD PR 2161](https://github.com/mdn/browser-compat-data/pull/2161)), from[haykam821](https://github.com/haykam821). `ChildNode.remove`

works in iOS Safari ([BCD PR 2171](https://github.com/mdn/browser-compat-data/pull/2171)), from[Scott Koenig](https://github.com/scottastrophic).- Add compat data for Edge (
[BCD PR 2174](https://github.com/mdn/browser-compat-data/pull/2174)), from[Zouhir ⚡️](https://github.com/zouhir). - Correct Chrome version for
`is`

support ([PR 2175](https://github.com/mdn/browser-compat-data/pull/2175)), from[Jonathan Pool](https://github.com/jrpool)(first contribution to BCD). - Inline text semantics for
`br`

([Interactive Examples PR 828](https://github.com/mdn/interactive-examples/pull/828)), from[Kadir Topal](https://github.com/atopal). - Add
`picture`

example. ([PR 842](https://github.com/mdn/interactive-examples/pull/842)), Add`embed`

example. ([PR 863](https://github.com/mdn/interactive-examples/pull/863)), and[7 more PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:"2018-05-01..2018-05-31"+author:sheeeng)to Interactive Examples from[Leonard Lee](https://github.com/sheeeng). - Improve js function
`bind`

example ([Interactive Examples PR 886](https://github.com/mdn/interactive-examples/pull/886)), from[Théis Bazin](https://github.com/tbazin). - Add Input
`<input type="button">`

([PR 891](https://github.com/mdn/interactive-examples/pull/891)), and Add Input`<input>`

example ([PR 892](https://github.com/mdn/interactive-examples/pull/892)), to Interactive Examples from[Neha Nupoor](https://github.com/nnupoor). - Add
`Array.prototype.values()`

([Interactive Examples PR 917](https://github.com/mdn/interactive-examples/pull/917)), from[Sid Vishnoi](https://github.com/sidvishnoi). - Added
`no-repeat`

property for`background-origin`

example. ([Interactive Examples PR 918](https://github.com/mdn/interactive-examples/pull/918)), from[Paul Ferlito](https://github.com/pferlito). - Add HTML example for
`<details>`

([PR 924](https://github.com/mdn/interactive-examples/pull/924)), and Add HTML example for`<summary>`

([PR 926](https://github.com/mdn/interactive-examples/pull/926)), to Interactive Examples from[Christian Stuff](https://github.com/Regaddi). - Add
`(max-)width`

to container ([PR 929](https://github.com/mdn/interactive-examples/pull/929)), Add HTML example for`<audio>`

([PR 930](https://github.com/mdn/interactive-examples/pull/930)), and Change`html`

to`tabbed`

in Publishing section ([PR 942](https://github.com/mdn/interactive-examples/pull/942)), to Interactive Examples from[Stephan Max](https://github.com/stephanmax). - Add object-keys.html (
[Interactive Examples PR 937](https://github.com/mdn/interactive-examples/pull/937)), from[Yahya Elharony](https://github.com/elharony). - Implemented example for
`<figcaption>`

tag ([Interactive Examples PR 941](https://github.com/mdn/interactive-examples/pull/941)), from[daGo](https://github.com/dagolinuxoid). - Directly use
`Math.round`

in the demo code. ([PR 956](https://github.com/mdn/interactive-examples/pull/956)), from[arai-a](https://github.com/arai-a)(first contribution to Interactive Examples). - Remove depreciated
`CELERYD_LOG_LEVEL`

([Kuma PR 4748](https://github.com/mozilla/kuma/pull/4748)), from[mashrikt](https://github.com/mashrikt). - Add
`<title>`

in code samples ([Kuma PR 4767](https://github.com/mozilla/kuma/pull/4767)), from[Antonio Fernando Santos Ladeia](https://github.com/Ladeia). - Add build status badge to README.md (
[PR 51](https://github.com/mdn/bob/pull/51)), from[ExE Boss](https://github.com/ExE-Boss)(first contribution to bob). - Reorder
`<display-listitem>`

to put`list-item`

last ([PR 220](https://github.com/mdn/data/pull/220)), from[Oriol Brufau](https://github.com/Loirooriol)(first contribution to Data). - Fix data for
`line-height-step`

([PR 224](https://github.com/mdn/data/pull/224)), from[Fuqiao Xue](https://github.com/xfq)(first contribution to Data). - Update
`font-weight`

syntax for CSS Fonts 4 ([PR 234](https://github.com/mdn/data/pull/234)), Update`font-stretch`

for CSS Fonts Level 4 ([PR 235](https://github.com/mdn/data/pull/235)), and Update`font-style`

for CSS Fonts Level 4 ([PR 236](https://github.com/mdn/data/pull/236)), from[wbamberg](https://github.com/wbamberg)(first contributions to Data). - Add Ukrainian translation for
`js_property_attributes`

macro ([KumaScript PR 700](https://github.com/mdn/kumascript/pull/700)), from[Nikola Myslovskij](https://github.com/AdriandeCita). - Added server-sent-events/README.md (
[PR 20](https://github.com/mdn/dom-examples/pull/20)), and server-sent-events: Break the`while(1)`

loop on`connection_aborted()`

([PR 21](https://github.com/mdn/dom-examples/pull/21)), to dom-examples from[Dumitru Uzun](https://github.com/duzun). - Update app.js (
[voice-change-o-matic PR 14](https://github.com/mdn/voice-change-o-matic/pull/14)), from[Alexander Leon](https://github.com/alien35). - Focus the repository on MDN Web Docs (
[PR 1](https://github.com/mdn/infra/pull/1)), from[me](https://github.com/jwhitlock)(first contribution to infra). - Fixed spelling error in comments (
[learning-area PR 71](https://github.com/mdn/learning-area/pull/71)), from[Stephen Borutta](https://github.com/SteviBee).

Other significant PRs:

- Add a name property to the browser schema (
[BCD PR 2025](https://github.com/mdn/browser-compat-data/pull/2025)), from[Connor Shea](https://github.com/connorshea). - Note
`>>>`

(shadow-piercing descendant combinator) alias in Chrome ([BCD PR 2158](https://github.com/mdn/browser-compat-data/pull/2158)), from[wbamberg](https://github.com/wbamberg). - Add headless tests for CDN (
[Kuma PR 4765](https://github.com/mozilla/kuma/pull/4765)), from[Ryan Johnson](https://github.com/escattone). - Remove
`aria-hidden`

from social SVG ([Kuma PR 4776](https://github.com/mozilla/kuma/pull/4776)), from[Schalk Neethling](https://github.com/schalkneethling). - Fix
`select_related`

to select only foreign key fields ([Kuma PR 4804](https://github.com/mozilla/kuma/pull/4804)), from[Safwan Rahman](https://github.com/safwanrahman). - Add
`::slotted`

pseudo-element and necessary syntaxes ([Data PR 169](https://github.com/mdn/data/pull/169)), from[Chris Mills](https://github.com/chrisdavidmills). - Add
`:host`

/`:host()`

/`:host-context()`

([Data PR 171](https://github.com/mdn/data/pull/171)), from[Chris Mills](https://github.com/chrisdavidmills). - Improve JSON schema errors output (
[Data PR 231](https://github.com/mdn/data/pull/231)), from[Roman Dvornov](https://github.com/lahmatiy).

We plan to ship Django 1.11 to production in early June, even before this post is published. We’ll spend some additional time in June fixing any issues that MDN’s millions of visitors discover, and upgrading the code to take advantage of some of the new features.

We plan to keep working on the compatibility data migration, HTML interactive examples, and other in-progress projects. June is the end of the second quarter, and is a deadline for many quarterly goals.

We are gathering in San Francisco for [Mozilla’s All-Hands](https://wiki.mozilla.org/All_Hands/SanFrancisco2018). It will be a chance for the remote team to be together in the same room, to celebrate the year’s accomplishments to date, and to make plans for the rest of the year.

## About John Whitlock

John is a web developer working on the engine of MDN Web Docs

## One comment

John WhitlockJune 8th, 2018 at 11:16