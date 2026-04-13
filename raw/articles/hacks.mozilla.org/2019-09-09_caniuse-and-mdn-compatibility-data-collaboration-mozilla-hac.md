---
title: Caniuse and MDN compatibility data collaboration – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2019/09/caniuse-and-mdn-compat-data-collaboration/
author: Florian Scholz
published: '2019-09-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Web developers spend a good amount of time making web compatibility decisions. Deciding whether or not to use a web platform feature often depends on its availability in web browsers.

### A brief history of compatibility data

[More than 10 years ago](http://a.deveria.com/2009/when-can-i-use/), [@fyrd](https://twitter.com/Fyrd) created the [caniuse](https://caniuse.com/) project, to help developers check feature availability across browsers. Over time, caniuse has evolved into the go-to resource to answer the question that comes up day to day: *“Can I use this?”*

About 2 years ago, the MDN team started re-doing its browser compatibility tables. The team was on a mission to [take the guesswork out of web compatibility](https://hacks.mozilla.org/2018/02/mdn-browser-compatibility-data/). Since then, the BCD project has become a large dataset with more than 10,000 data points. It stays up to date with the help of over [500 contributors on GitHub](https://github.com/mdn/browser-compat-data).

MDN compatibility data is available as [open data on npm](https://www.npmjs.com/package/mdn-browser-compat-data) and has been integrated in a variety of projects including [VS Code](https://code.visualstudio.com/updates/v1_25#_improved-accuracy-of-browser-compatibility-data) and [webhint.io](https://webhint.io/docs/user-guide/hints/hint-compat-api/) auditing.

### Two great data sources come together

Today we’re announcing the integration of MDN’s compat data into the caniuse website. Together, we’re bringing even more web compatibility information into the hands of web developers.

Before we began our collaboration, the caniuse website only displayed results for features available in the caniuse database. Now all search results can include support tables for MDN compat data. This includes data types already found on caniuse, specifically the HTML, CSS, JavaScript, Web API, SVG & and HTTP [categories](https://github.com/mdn/browser-compat-data#repository-contents). By adding MDN data, the caniuse support table count expands from roughly 500 to 10,500 tables! Developers’ caniuse queries on what’s supported where will now have significantly more results.

The new feature tables will look a little different. Because the MDN compat data project and caniuse have compatible yet somewhat different goals, the implementation is a little different too. While the new MDN-based tables don’t have matching fields for all the available metadata (such as links to resources and a full feature description), support notes and details such as bug information, prefixes, feature flags, etc. will be included.

The MDN compatibility data itself is converted under the hood to the same format used in caniuse compat tables. Thus, users can filter and arrange MDN-based data tables in the same way as any other caniuse table. This includes access to browser usage information, either by region or [imported through Google Analytics](http://caniuse.com/#stats_import) to help you decide when a feature has enough support for your users. And the different view modes available via both datasets help visualize support information.

### Differences in the datasets

We’ve been asked why the datasets are treated differently. Why didn’t we merge them in the first place? We discussed and considered this option. However, due to the intrinsic differences between our two projects, we decided not to. Here’s why:

MDN’s support data is very broad and covers feature support at a very granular level. This allows MDN to provide as much detailed information as possible across all web technologies, supplementing the reference information provided by MDN Web Docs.

Caniuse, on the other hand, often looks at larger features as a whole (e.g. [CSS Grid](https://caniuse.com/#feat=css-grid), [WebGL](https://caniuse.com/#feat=webgl), specific file format support). The caniuse approach provides developers with higher level at-a-glance information on whether the feature’s supported. Sometimes detail is missing. Each individual feature is added manually to caniuse, with a primary focus on browser support coverage rather than on feature coverage overall.

Because of these and other differences in implementation, we don’t plan on merging the source data repositories or matching the data schema at this time. Instead, the integration works by matching the search query to the feature’s description on caniuse.com. Then, caniuse generates an appropriate feature table, and converts MDN support data to the caniuse format on the fly.

### What’s next

We encourage community members of both repos, [caniuse](https://github.com/Fyrd/caniuse) and [mdn-compat-data](https://github.com/mdn/browser-compat-data), to work together to improve the underlying data. By sharing information and collaborating wherever possible, we can help web developers find answers to compatibility questions.

## About
[
Florian Scholz ](https://developer.mozilla.org)

Florian is the Content Lead for MDN Web Docs, writes about Web platform technologies and researches browser compatibility data. He lives in Bremen, Germany.

## About Alexis Deveria

Alexis is the creator & maintainer of caniuse.com by night, and a web developer at Adobe by day.

## One comment

Clint PriestSeptember 10th, 2019 at 04:38