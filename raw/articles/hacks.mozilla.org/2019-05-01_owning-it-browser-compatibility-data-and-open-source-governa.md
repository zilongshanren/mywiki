---
title: 'Owning it: browser compatibility data and open source governance – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2019/05/browser-compatibility-data-and-open-source-governance/
author: Daniel Beck
published: '2019-05-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

What does it mean to “own” an open-source project? With the [browser-compat-data](https://github.com/mdn/browser-compat-data) project (“BCD”), the MDN (Mozilla Developer Network) community and I recently had the opportunity to find out.

In 2017, the MDN Web Docs team invited me to work on what was described to me as a small, but growing project ([previously on Hacks](https://hacks.mozilla.org/2018/02/mdn-browser-compatibility-data/)). The little project had a big goal: to provide detailed and reliable structured data about what Web platform features are supported by different browsers. It sounded ambitious, but my part was narrow: convert hand-written HTML compatibility tables on MDN into structured JSON data.

As a technical writer and consultant, it was an unusual project to get to work on. Ordinarily, I look at data and code and use them to write words for people. For BCD, I worked in the opposite direction: [reading what people wrote and turning it into structured data for machines](https://ddbeck.com/browser-compat-data/). But I think I was most excited at the prospect of working on an open source project with a lot of reach, something I’d never done before.

Plus the project appealed to my sense of order and tidiness. Back then, most of the compatibility tables looked something like this:

In their inconsistent state, they couldn’t be updated in bulk and couldn’t be redesigned without modifying thousands upon thousands of pages on MDN. Instead, we worked to liberate the data in the tables to a structured, validated JSON format that we could [publish in an npm package](https://www.npmjs.com/package/mdn-browser-compat-data). With this change, [new tables](https://developer.mozilla.org/en-US/docs/Web/CSS/linear-gradient#Browser_compatibility) could be generated and [other projects](https://github.com/mdn/browser-compat-data#projects-using-the-data) could use the data too.

Since then, the project has grown considerably. If there was a single inflection point, it was the *Hack on MDN* event in Paris, where we met in early 2018 to [migrate more tables, build new tools, and play with the data](https://hacks.mozilla.org/2018/03/hack-on-mdn-building-useful-tools-with-browser-compatibility-data/). In the last year and a half, we’ve accomplished so many things, including replacing the last of the legacy tables on MDN with shiny, new BCD-derived tables, and seeing our data used in [Visual Studio Code](https://code.visualstudio.com/).

## Building a project to last

We couldn’t have built BCD into what it is now without the help of the hundreds of new contributors that have joined the project. But some challenges have come along with that growth. My duties shifted from copying data into the repository to reviewing others’ contributions, learning about the design of the schema, and hacking on supporting tools. I had to learn so much about being a thoughtful, helpful guide for new and established contributors alike. But the increased size of the project also put new demands on the project as a whole.

[Florian Scholz](https://github.com/Elchi3), the project leader, took on answering a question key to the long-term sustainability of the project: how do we make sure that contributors can be more than mere inputs, and can really be part of the project? To answer that question, Florian wrote and helped us adopt [a governance document](https://github.com/mdn/browser-compat-data/blob/master/governance.md) that defines how any contributor—not just MDN staff—can become an *owner* of the project.

Inspired by the JS Foundation’s [Technical Advisory Committee](https://github.com/JSFoundation/TAC), the [ESLint project](https://github.com/eslint/eslint.github.io/blob/master/docs/maintainer-guide/governance.md), and others, BCD’s governance document lays out how contributors can become committers (known as *peers*), how important decisions are made by the project leaders (known as *owners*), and how to become an owner. It’s not some stuffy rule book about votes and points of order; it speaks to the project’s ambition of being a community-led project.

Since adopting the governance document, BCD has added new peers from outside Mozilla, reflecting how the project has grown into a cross-browser community. For example, [Joe Medley](https://github.com/jpmedley), a technical writer at Google, has joined us to help add and confirm data about Google Chrome. We’ve also added one new owner: me.

If I’m being honest, not much has changed: peers and owners still review pull requests, still research and add new data, and still answer a lot of questions about BCD, just as before. But with the governance document, we know what’s expected and what we can do to guide others on the journey to project ownership, like I experienced. It’s reassuring to know that as the project grows so too will its leadership.

## More to come

We accomplished a lot in the past year, but our best work is ahead. In 2019, we have an ambitious goal: get 100% real data for Firefox, Internet Explorer, Edge, Chrome, Safari, mobile Safari, and mobile Chrome for all Web platform features. That means data about whether or not any feature in our data set is supported by each browser and, if it is, in what version it first appeared. If we achieve our goal, BCD will be an unparalleled resource for Web developers.

But we can’t achieve this goal on our own. We need to fill in the blanks, by testing and researching features, updating data, verifying pull requests, and more. We’d love for you to [join us](https://github.com/mdn/browser-compat-data/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted+%3Asos%3A%22).