---
title: MDN localization in March — Tier 1 locales unfrozen, and future plans – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2021/03/mdn-localization-in-march-tier-1-locales-unfrozen-and-future-plans/
author: Chris Mills
published: '2021-03-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Since we [last talked about MDN localization](https://hacks.mozilla.org/2021/02/mdn-localization-update-february-2021/), a lot of progress has been made. In this post we’ll talk you through the unfreezing of Tier 1 locales, and the next steps in our plans to stop displaying non-active and unmaintained locales.

## Tier 1 locales unfrozen!

It has been a long time coming, but we’ve finally achieved our goal of unfreezing our Tier 1 locales. the `fr`

, `ja`

, `ru`

, `zh-CN`

, and `zh-TW`

locales can now be edited, and we have active teams working on each of these locales. We added Russian (`ru`

) to the list very recently, after great interest from the community helped us to rapidly assemble a team to maintain those docs — we are really excited about making progress here!

If you are interested in helping out with these locales, or asking questions, you can find all the information you need at our all-new [translated-content README](https://github.com/mdn/translated-content). This includes:

- How to contribute
- The policies in place to govern the work
- Who is in the active localization teams
- How the structure is kept in sync with the en-US version.

We’d like to thank everyone who helped us get to this stage, especially the localization team members who have stepped up to help us maintain our localized content:

- Our French (fr) team:
- Our Japanese (ja) team:
- Our Russian (ru) team:
- Our Chinese (zh-CN and zh-TW) team:

## Stopping the display of unmaintained locales on MDN

Previously we said that we were planning to stop the display of all locales except for `en-US`

, and our Tier 1 locales.

We’ve revised this plan a little since then — we looked at the readership figures of each locale, as a percentage of the total MDN traffic, and decided that we should keep a few more than just the 5 we previously mentioned. Some of the viewing figures for non-active locales are quite high, so we thought it would be wise to keep them and try to encourage teams to start maintaining them.

In the end, we decided to keep the following locales:

`en-US`

`es`

`ru`

(already unfrozen)`fr`

(already unfrozen)`zh-CN`

(already unfrozen)`ja`

(already unfrozen)`pt-BR`

`ko`

`de`

`pl`

`zh-TW`

(already unfrozen)

We are planning to stop displaying the other 21 locales. Many of them have very few pages, a high percentage of which are out-of-date or otherwise flawed, and we estimate that the total traffic we will lose by removing all these locales is less than 2%.

## So what does this mean?

We are intending to stop displaying all locales outside the top ten by a certain date. The date we have chosen is April 30th.

We will remove all the source content for those locales from the translated-content repo, and put it in a new retired translated content repo, so that anyone who still wants to use this content in some way is welcome to do so. We highly respect the work that so many people have done on translating MDN content over the years, and want to preserve it in some way.

We will redirect the URLs for all removed articles to their en-US equivalents — this solves an often-mentioned issue whereby people would rather view the up-to-date English article than the low-quality or out-of-date version in their own language, but find it difficult to do so because of they way MDN works.

We are also intending to create a new tool whereby if you see a really outdated page, you can press a button saying “retire content” to open up a pull request that when merged will check it out to the retired content repo.

After this point, we won’t revive anything — the journey to retirement is one way. This may sound harsh, but we are taking determined steps to clean up MDN and get rid of out-of-date and out-of-remit content that has been around for years in some cases.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.