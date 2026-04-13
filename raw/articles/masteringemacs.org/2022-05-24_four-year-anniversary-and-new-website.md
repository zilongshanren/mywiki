---
title: Four year anniversary and new website
url: https://www.masteringemacs.org/article/four-year-anniversary-new-website
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Welcome to the new *Mastering Emacs* website. After four years (yes, four!) it’s time for a site refresh. The old site was never meant to last that long; it was a temporary theme hastily picked so I could start writing about Emacs. Back then there were fewer blogs and Emacs resources. We didn’t even have a package manager.

The old site did serve its purpose as a launchpad for my blogging adventures. But Apache/WordPress is slow out of the box, even with SuperCache. A slight breeze and the thing would fall over — and it did, every time it featured on HackerNews or high-traffic subreddits.

Eventually I moved to FastCGI and nginx to host WordPress, but as it’s not officially supported it was a major pain to get working. [António P. P. Almeida’s wordpress-nginx](https://github.com/perusio/wordpress-nginx) made my life so much easier and the site *so much* faster.

Alas, it’s time to retire the old site. Over the years I came to a number of conclusions:

**People don’t use tags** I spent a good amount of time adding tags to every article I wrote, but almost no one ever really used them. Sure people *did* click on them, but overall the [reading guide](https://www.masteringemacs.org/reading-guide) proved far more useful. My goal is to re-implement a “tag”-like system but around concepts (Shells, Dired, etc.) instead of tags.

**Not enough categories** I had categories like “For Beginners”, “Tutorials”, and so on. They worked OK, but I am of the opinion now that manually curating my content makes more sense. Automatic content generation’s fine but throwing articles into a two or three baskets is never good enough.

**Spammers are getting smarter** I had to ditch Akismet, a free anti-spam checker for WordPress, after several years of near-perfect operation. The spammers simply mimicked humans too much and the filter would trip up on *real* content. I eventually switched to manual approval but that’s a lot of work.

**Encourage visitors to read other articles** A lot of visitors would leave after reading a single article, even though I would often have several related articles. I tried some of the “Suggested Content” plugins but they were universally terrible — another mark against content automation.

**Apache is a memory hog** Yes, yes. I am sure you can tame Apache and make it into a lithe and agile webserver but my best efforts failed me. The second I switched to nginx the memory and CPU usage dropped like a rock. Not to mention that nginx is much easier to configure.

So what about the new site then? Well it’s custom written for the job, though I may one day open source the blog engine. I launched it Tuesday the 14th of October, and immediately my site got slammed by reddit, Twitter and Hackernews on the announcement of Emacs 24.4. Talk about baptism by fire! The site held up just fine though.

The stack is Python and Flask running PostgreSQL with nginx as a reverse proxy and uWSGI as the application server, and with memcached for page caching. It took about three weeks of casual coding to write it, including the harrowing experience of having to convert the old blog articles — but more on that in a bit.

I opted for Memcached over Redis as my needs were simple, and because nginx ships with memcached support meaning nginx could short-circuit the trip to my upstream application server should the need ever arise. For now it just goes to uWSGI which checks the cache and returns the cached copy. That’s actually more than quick enough to survive HackerNews, the most high-traffic site visits I’ve gotten.

The slowness comes from page generation and not querying the database (databases are fast, Python is not) so that’s where memcached comes in. I thought about using nginx’s own proxy cache mechanism but invalidating the cache when you add a new comment or when I edit a page is messy.

Converting the blog articles proved a greater challenge than you might think. First of all, I like reStructuredText so I wanted to write and edit my articles in rST and convert them automatically to HTML when I publish them.

Enter Pandoc, which is a fine tool for the job. But there’s a snag. The original WordPress format is pseudo-HTML, meaning blank lines signify new paragraphs. Converting that without spending too much time with a hand-rolled, one-off state machine to convert to “real HTML” (for Pandoc to convert to rST) involved some compromises and hand editing. (And no, wrapping text blocks in paragraph tags is not enough when you have `<pre>`

tags with newlines and other tag flotsam.)

So that was painful.

Coming up with a new design proved a fun challenge as well. CSS has come a long way in four years and things like text-justified automatic hyphenation work great (unless you’re on Chrome, in which case it’s the dark ages for you) on both Firefox and IE. Drop caps, ligatures, kerning and old-style numerals also work well and is possible in CSS alone. I’m surprised how good HTML/CSS is at typesetting nowadays. The font is *Cardo*, an open source font inspired by Monotype’s Bembo, a font itself inspired by [Aldus Manutius’](http://en.wikipedia.org/wiki/Bembo) from the 1500s, which I originally wanted to use but it’s way, way, WAY too expensive for web font use. If you’re a Chrome user on Windows the font will look weird as Chrome does not see fit to grace your eyes with aliasing. Again, both Firefox and IE render properly.

I opted for larger font sizes than normal in the belief that: it’s not the 1990s any more, and big font sizes mean people won’t have to zoom in or squint their eyes. Or at least that’s what I always end up doing, and my vision’s perfectly fine. Apparently doing that was a mistake: the amount of vitriol I received from certain quarters of the internet for having *large font sizes* was… perplexing to say the least.

So I made the fonts smaller.

The site’s still undergoing changes and I plan on adding to it over time. I am particularly keen on getting people to explore my site and learn more about Emacs.

Here’s to another four years.

Mickey.