---
title: 'Kuma: Cool URL tricks – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2012/08/kuma-cool-url-tricks/
author: Eric Shepherd
published: '2012-08-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

If you’re fiddling with automation, or want to be able to pull information out of the [Mozilla Developer Network](https://developer.mozilla.org/) wiki, there are some helpful queries you can do with URLs that may help you out. Today, I’m going to share those.

**The Kuma API**


| Command | Description |
|---|---|
| ?raw | Instructs Kuma to return the raw content of the page, without any of the skin material, such as the headers, footers, and so forth. This does not execute templates or scripts. For example,
|

[https://developer.mozilla.org/en-US/docs/HTML/HTML5?raw¯os](https://developer.mozilla.org/en-US/docs/HTML/HTML5?raw¯os)[https://developer.mozilla.org/en-US/docs/HTML/HTML5?raw§ion=Introduction_to_HTML5](https://developer.mozilla.org/en-US/docs/HTML/HTML5?raw§ion=Introduction_to_HTML5)[https://developer.mozilla.org/en-US/docs/HTML/HTML5$json](https://developer.mozilla.org/en-US/docs/HTML/HTML5$json)These offer a lot of capability, and hopefully will be useful for people building developer tools and other utilities.

**Kuma feeds**


All feeds start with the string “https://developer.mozilla.org/<locale>/docs/feeds/<format>/”, where <locale> is one of the standard locale strings, such as “en-US”, “ja”, and so forth. Note that at present, the locale you specify doesn’t impact the output, but it may eventually do so (indeed, I hope it will). <format> is one of “atom”, “rss”, or “json”.

| Feed | Description |
|---|---|
| all | All recently changed articles, in order of modification date. This includes newly created articles. All changes are combined into one entry in the feed for each article. |
| revisions | Each revision made to an article, in order by modification date, including newly created articles. Each revision has a separate entry in the feed. |
| tag/<tagname> | Recently changed articles, in order by modification date. Only articles that have the specified tag are included in the feed. |
| files | Recently changed or uploaded files. |
| needs-review[/<reviewtype>] | A list of articles that have the specified review request checked, or all articles with a review requested if you don’t specify a review type. The review type can be one of “tech”, “editorial”, or “kumascript”. |

So, for example, you can get an atom format feed of recently changed articles tagged with “JavaScript” thusly: [https://developer.mozilla.org/en-US/docs/feeds/atom/tag/JavaScript](https://developer.mozilla.org/en-US/docs/feeds/tag/JavaScript).

**Wrapping up**

Hopefully these are useful! There’s more to come, but these are a great start! Enjoy!

## 4 comments

les orchardAugust 9th, 2012 at 06:59les orchardAugust 9th, 2012 at 07:00Salman AbbasAugust 9th, 2012 at 18:46Eric ShepherdAugust 9th, 2012 at 20:31