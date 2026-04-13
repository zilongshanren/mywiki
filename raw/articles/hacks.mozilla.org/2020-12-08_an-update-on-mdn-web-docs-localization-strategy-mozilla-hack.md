---
title: An update on MDN Web Docs’ localization strategy – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2020/12/an-update-on-mdn-web-docs-localization-strategy/
author: Chris Mills
published: '2020-12-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In our previous post — [MDN Web Docs evolves! Lowdown on the upcoming new platform](https://hacks.mozilla.org/2020/10/mdn-web-docs-evolves-lowdown-on-the-upcoming-new-platform/) — we talked about many aspects of the new MDN Web Docs platform that we’re launching on December 14th. In this post, we’ll look at one aspect in more detail — how we are handling localization going forward. We’ll talk about how our thinking has changed since our previous post, and detail our updated course of action.

## Updated course of action

Based on thoughtful feedback from the community, we did some additional investigation and determined a stronger, clearer path forward.

First of all, we want to keep a clear focus on work leading up to the launch of our new platform, and making sure the overall system works smoothly. This means that upon launch, we still plan to display translations in all existing locales, but they will all initially be frozen — read-only, not editable.

We *were* considering automated translations as the main way forward. One key issue was that automated translations into European languages are seen as an acceptable solution, but automated translations into [CJK languages](https://en.wikipedia.org/wiki/CJK_characters) are far from ideal — they have a very different structure to English and European languages, plus many Europeans are able to read English well enough to fall back on English documentation when required, whereas some CJK communities do not commonly read English so do not have that luxury.

Many folks we talked to said that automated translations wouldn’t be acceptable in their languages. Not only would they be substandard, but a lot of MDN Web Docs communities center around translating documents. If manual translations went away, those vibrant and highly involved communities would probably go away — something we certainly want to avoid!

We are therefore focusing on limited manual translations as our main way forward instead, looking to unfreeze a number of key locales as soon as possible after the new platform launch.

## Limited manual translations

Rigorous testing has been done, and it looks like building translated content as part of the main build process is doable. We are separating locales into two tiers in order to determine which will be unfrozen and which will remain locked.

- Tier 1 locales will be unfrozen and manually editable via pull requests. These locales are required to have
**at least**one representative who will act as a community lead. The community members will be responsible for monitoring the localized pages, updating translations of key content once the English versions are changed, reviewing edits, etc. The community lead will additionally be in charge of making decisions related to that locale, and acting as a point of contact between the community and the MDN staff team. - Tier 2 locales will be frozen, and not accept pull requests, because they have no community to maintain them.

The Tier 1 locales we are starting with unfreezing are:

- Simplified Chinese (zh-CN)
- Traditional Chinese (zh-TW)
- French (fr)
- Japanese (ja)

If you wish for a Tier 2 locale to be unfrozen, then you need to [come to us with a proposal](https://developer.mozilla.org/en-US/docs/MDN/Contribute/Getting_started#Step_4_Ask_for_help), including evidence of an active team willing to be responsible for the work associated with that locale. If this is the case, then we can promote the locale to Tier 1, and you can start work.

We will monitor the activity on the Tier 1 locales. If a Tier 1 locale is not being maintained by its community, we shall demote it to Tier 2 after a certain period of time, and it will become frozen again.

We are looking at this new system as a reasonable compromise — providing a path for you the community to continue work on MDN translations providing the interest is there, while also ensuring that locale maintenance is viable, and content won’t get any further out of date. With most locales unmaintained, changes weren’t being reviewed effectively, and readers of those locales were often confused between using their preferred locale or English, their experience suffering as a result.

## Review process

The review process will be quite simple.

- The content for each Tier 1 locale will be kept in its own separate repo.
- When a PR is made against that repo, the localization community will be pinged for a review.
- When the content has been reviewed, an MDN admin will be pinged to merge the change. We should be able to set up the system so that this happens automatically.
- There will also be some user-submitted content bugs filed at
[https://github.com/mdn/sprints/issues](https://github.com/mdn/sprints/issues), as well as on the issue trackers for each locale repo. When triaged, the “sprints” issues will be assigned to the relevant localization team to fix, but the relevant localization team is responsible for triaging and resolving issues filed on their own repo.

## Machine translations alongside manual translations

We previously talked about the potential involvement of machine translations to enhance the new localization process. We still have this in mind, but we are looking to keep the initial system simple, in order to make it achievable. The next step in Q1 2021 will be to start looking into how we could most effectively make use of machine translations. We’ll give you another update in mid-Q1, once we’ve made more progress.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 8 comments

Janet SwisherDecember 8th, 2020 at 10:22Chris MillsDecember 9th, 2020 at 08:18Eric ShepherdDecember 8th, 2020 at 10:52Chris MillsDecember 9th, 2020 at 08:21Daniele Mte90 ScasciafratteDecember 9th, 2020 at 05:36Chris MillsDecember 9th, 2020 at 08:17Jean-BaptisteDecember 12th, 2020 at 03:41Harvey LiuDecember 18th, 2020 at 13:54