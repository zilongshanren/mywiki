---
title: 'Welcome Yari: MDN Web Docs has a new platform – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2020/12/welcome-yari-mdn-web-docs-has-a-new-platform/
author: Chris Mills
published: '2020-12-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

After several intense months of work on such a significant change, the day is finally upon us: [MDN Web Docs’ new platform](https://hacks.mozilla.org/2020/10/mdn-web-docs-evolves-lowdown-on-the-upcoming-new-platform/) (codenamed [Yari](https://en.wikipedia.org/wiki/Yari)) is finally launched!

![icon for yari, includes a man with a spear, plus the text yari, the mdn web docs platform](../../assets/b309ff956db63208.png)


Between November 2 and December 14, we ran a beta period in which a number of our fabulous community members tested out the new platform, submitted content changes, allowed us to try out the new contribution workflow, and suggested improvements to both the platform and styling. All of you have our heartfelt thanks.

This post serves to provide an update on where we are now, what we’re aiming to do next, and what you can do to help.

## Where we are now

We’ve pulled together a working system in a short amount of time that vastly improves on the previous platform, and solves a number of tangible issues. There is certainly a lot of work still to do, but this new release provides a stable base to iterate from, and you’ll see a lot of further improvements in the coming months. Here’s a peek at where we are now:

### Contributing in GitHub

The most significant difference with the new platform is that we’ve decentralized the content from a SQL database to files in a git repository. To edit content, you now submit pull requests against the [https://github.com/mdn/content](https://github.com/mdn/content) repo, rather than editing the wiki using the old WYSIWYG editor.

This has a huge advantage in terms of contribution workflow — because it’s a GitHub repo, you can insert it into your workflow however you feel comfortable, mass changes are easier to make programmatically, and you can lump together edits across multiple pages in a single pull request rather than as scattered individual edits, and we can apply intelligent automatic linting to edits to speed up work.

The content repo initially comes with a few basic CLI tools to help you with fundamental tasks, such as `yarn start`

(to create a live preview of what your document will look like when rendered on MDN), `yarn content create`

(to add a new page), `yarn content move`

(to move an existing page), etc. You can find more details of these, and other contribution instructions, in the [repo’s README file](https://github.com/mdn/content/blob/main/README.md).

### Caring for the community

Community interactions will not just be improved, but transformed. You can now have a conversation about a change over a pull request before it is finalized and submitted, making suggestions and iterating, rather than worrying about getting it perfect the first time round.

We think that this model will give contributors more confidence in making changes, and allow us to build a much better relationship with our community and help them improve their contributions.

### Reducing developer burden

Our developer maintenance burden is also now much reduced with this update. The existing (Kuma) platform is complex, hard to maintain, and adding new features is very difficult. The update will vastly simplify the platform code — we estimate that we can remove a significant chunk of the existing codebase, meaning easier maintenance and contributions.

This is also true of our front-end architecture: The existing MDN platform has a number of front-end inconsistencies and accessibility issues, which we’ve wanted to tackle for some time. The move to a new, simplified platform gives us a perfect opportunity to fix such issues.

## What we’re doing next

There are a number of things that we could do to further improve the new platform going forward. Last week, for example, we already talked about our [plans for the future of l10n on MDN](https://hacks.mozilla.org/2020/12/an-update-on-mdn-web-docs-localization-strategy/).

The first thing we’ll be working on in the new year is ironing out the kinks in the new platform. After that, we can start to serve our readers and contributors much better than before, implementing new features faster and more confidently, which will lead to an even more useful MDN, with an even more powerful contribution model.

The sections below are by no means definite, but they do provide a useful idea of what we’ve got planned next for the platform. We are aiming to publish a public roadmap in the future, so that you can find out where we’re at, and make suggestions.

### Moving to Markdown

At its launch, the content is stored in HTML format. This is OK — we all know a little HTML — but it is not the most convenient format to edit and write, especially if you are creating a sizable new page from scratch. Most people find Markdown easier to write than HTML, so we want to eventually move to storing our core content in Markdown (or maybe some other format) rather than HTML.

### Improving search

For a long time, the search functionality has been substandard on MDN. Going forward, we not only want to upgrade our search to return useful results, but we also want to search more usefully, for example fuzzy search, search by popularity search by titles, summaries, full text search, and more.

### Representing MDN meta pages

Currently only the MDN content pages are represented in our new content repo. We’d eventually like to stop using our old home, profile, and search pages, which are still currently served from our old Django-based platform, and bring those into the new platform with all the advantages that it brings.

### And there’s more!

We’d also like to start exploring:

- Optimizing file attachments
- Implementing and enforcing CSP on MDN
- Automated linting and formatting of all code snippets
- Gradually removing the old-style KumaScript macros that remain in MDN content, removing, rendering, or replacing them as appropriate. For example, link macros can just be rendered out, as standard HTML links will work fine, whereas all the sidebar macros we have should be replaced by a proper sidebar system built into the actual platform.

## What you can do to help

As you’ll have seen from the above next steps, there is still a lot to do, and we’d love the community to help us with future MDN content and platform work.

- If you are more interested in helping with content work, you can find out how to help at
[Contributing to MDN](https://developer.mozilla.org/en-US/docs/MDN/Contribute). - If you are more interested in helping with MDN platform development, the best place to learn where to start is the
[Yari README](https://github.com/mdn/yari/blob/master/README.md). - In terms of finding a good general place to chat about MDN, you can join the discussion on the
[MDN Web Docs chat room](https://chat.mozilla.org/#/room/#mdn:mozilla.org)on[Matrix](https://wiki.mozilla.org/Matrix).

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 10 comments

maxlohDecember 14th, 2020 at 17:37Chris MillsDecember 15th, 2020 at 00:27AlDecember 15th, 2020 at 04:44Yinsi RioDecember 15th, 2020 at 08:04Rami YushuvaevDecember 15th, 2020 at 12:56Chris MillsDecember 16th, 2020 at 01:28h.rayfloodDecember 15th, 2020 at 14:43Tim EDecember 15th, 2020 at 17:18KnissingDecember 16th, 2020 at 19:58SudarshanDecember 26th, 2020 at 17:05