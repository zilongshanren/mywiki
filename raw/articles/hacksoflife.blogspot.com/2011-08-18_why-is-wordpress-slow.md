---
title: Why is Wordpress Slow?
url: http://hacksoflife.blogspot.com/2011/08/why-is-wordpress-slow.html
author: Benjamin Supnik
published: '2011-08-18'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I love WordPress, so it breaks my heart when our nice shiny WordPress pages take 9 seconds to load. Here are the results of some investigations. I don't do WP professionally, but WP is really easy to tinker with, so I'll blog this to avoid forgetting it.


The X-Plane blog uses


When we miss the cache, page load is really slow. You can tell whether you missed the cache and why it's slow by looking at the last few lines of the page; WP super cache will list the time the cached page was last built, the render time in seconds, and it'll tell you if it's gzipping. We see dynamic content times from 2 to 9 seconds!


Disabling


So the number one issue is that when we miss the cache, run time costs are killing us.


When we hit the cache, Safari's timeline view of resources tells us what is causing the page to be slow to load. We can see a few things:



Finally the third and weirdest finding: if you have local browser cookies, WP Super Cache dutifully caches the customized version of the page you see with the forms filled out. This means that you get your own private cache site.


This is a bit terrifying first because we could have a really huge build-up of files in the cache. But it's also bad news for cache hits. When the site changes (e.g. a comment is posted) the first user to view the page eats the cache miss. But if you have cookies, you always miss the cache since you have your own private cache.


In our case this is really bad: it means that users who have commented before (and thus have comment-name cookie in place) will always miss the cache once for every new article they see plus every comment posted. Which is to say, the site will virtually always be "slow" (which in our case is "really slow" due to slow plugins).


I discovered this by putting WP Super Cache in debug mode, setting my IP as the debug URL and setting the debug level to 5. Then when I first loaded a page in FireFox, I saw a whole pile of cache output due to cookies - when I viewed the cache meta data on the server, my own commenting name and email were clearly visible.

The X-Plane blog uses

[WP Super Cache](http://wordpress.org/extend/plugins/wp-super-cache/)and a pile of social networking plugins. Here's what I found for speed.When we miss the cache, page load is really slow. You can tell whether you missed the cache and why it's slow by looking at the last few lines of the page; WP super cache will list the time the cached page was last built, the render time in seconds, and it'll tell you if it's gzipping. We see dynamic content times from 2 to 9 seconds!

Disabling

[Tweet This](http://wordpress.org/extend/plugins/tweet-this/)brought the time down to less than a second. I don't know what Tweet This is doing (probably blocking on IO with Twitter on the server side while the page renders) but our first action will be to explore whether another plugin is faster.So the number one issue is that when we miss the cache, run time costs are killing us.

When we hit the cache, Safari's timeline view of resources tells us what is causing the page to be slow to load. We can see a few things:

- One plugin is putting its java script link at the end of the page, so we lose parallelism in loading.
- Some plugins are going to external sites with much higher latency than our server.
- We're "scattering" a bit to get our JS - consolidation might be a good idea, but in practice we don't have enough JS to care, plus the browser will cache.

Finally the third and weirdest finding: if you have local browser cookies, WP Super Cache dutifully caches the customized version of the page you see with the forms filled out. This means that you get your own private cache site.

This is a bit terrifying first because we could have a really huge build-up of files in the cache. But it's also bad news for cache hits. When the site changes (e.g. a comment is posted) the first user to view the page eats the cache miss. But if you have cookies, you always miss the cache since you have your own private cache.

In our case this is really bad: it means that users who have commented before (and thus have comment-name cookie in place) will always miss the cache once for every new article they see plus every comment posted. Which is to say, the site will virtually always be "slow" (which in our case is "really slow" due to slow plugins).

I discovered this by putting WP Super Cache in debug mode, setting my IP as the debug URL and setting the debug level to 5. Then when I first loaded a page in FireFox, I saw a whole pile of cache output due to cookies - when I viewed the cache meta data on the server, my own commenting name and email were clearly visible.

## No comments:

## Post a Comment