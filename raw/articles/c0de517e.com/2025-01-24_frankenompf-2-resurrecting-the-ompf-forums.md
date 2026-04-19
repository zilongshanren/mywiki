---
title: FrankenOMPF/2!Resurrecting the OMPF forums.
url: https://c0de517e.com/_ompf.htm
author: Angelo Pesce
published: '2025-01-24'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

After writing on the

[history of offline rendering](018_rthistory.htm), I realized once again how

[ephemeral](https://c0de517e.com/JOURNAL/log_003.htm#39) the web it.

With a bit of nostalgia, and having done something similar already for certain

[usenet newsgroups](003_usenet_archive.htm), I decided to resuscitate the historic OMPF forums, that were once an amazing resource for people interested in the state of the art of raytracing and pathtracing.

I made a script to scrape everything the

[Wayback Machine](https://wayback.archive.org/) archived, and then parse it and translate it to static web pages, including all the images I could get.

Here's the results:

-

[Original OMPF forum (2006-2011).](EXTERNAL/ompf/index_main.htm)
-

[OMPF2 forum (2011-2021).](EXTERNAL/ompf2/index_main.htm)
If you want to do something similar, the script is

[here](MISC/phpbb_wayback.py), should be a good starting point for PHPBB-based forum scraping from wayback.

**Some considerations:**
- Even if we have the IA, that does not mean that the archived content is usable. Currently, I'm sure in an effort to stop AI and other bots, the IA throttling limits are painfully low (5 requests per minute), which makes projects like this take much longer than ideal.

-- I wonder if there is a future for the IA to have some of these transforms ran directly on their machines and linked as part of the archive. For example, it could be possible to detect PHPBB boards and, similarly to what I've done, convert their contents into a format that is easier to deal with.

- The modern web will be entirely lost, now most of the content is not on webpages or static archives, but behind proprietary APIs.

- We moved most of the discussions to real-time forums, especially in computer graphics - we have discords/slacks, groups on twitter/mastodon/bluesky - and all these things that build communities and friendships are amazing! We had that in the old web in IRC. But having everything in these real-time platforms, instead of separating the space for chats from the space for long-form discussions (mailing lists, newsgroups, forums), is not imho the right arrangement. Real-time platforms should look and be ephemeral!

-- I'm convinced this is the right setup also at work - e.g. the old jabber (messenger etc)/email separation is better than Slack/Teams for everything...