---
title: Twitter Direct Message Caching and Firefox – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2020/04/twitter-direct-message-caching-and-firefox/
author: Martin Thomson
published: '2020-04-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Editor’s Note: April 6, 7:00pm pt – After some more investigation into this problem, it appears that the initial analysis pointing to the Content-Disposition was based on bad information. The reason that some browsers were not caching direct messages was that Twitter includes the non-standard Pragma: no-cache header in responses. Using Pragma is invalid as it is defined to be equivalent to Cache-Control: no-cache only for requests. Though it is counter-intuitive, ‘no-cache’ does not prevent a cache from storing content; ‘no-cache’ only means that the cache needs to check with the server before reusing that response. That doesn’t change the conclusion: limited observations of behavior are no substitute for building to standards.*

Twitter is telling its users that their [personal direct messages might be stored in Firefox’s web cache](https://privacy.twitter.com/en/blog/2020/data-cache-firefox).

This problem affects anyone who uses Twitter on Firefox from a shared computer account. Those users should [clear their cache](https://support.mozilla.org/en-US/kb/delete-browsing-search-download-history-firefox#w_how-do-i-clear-my-history).

This post explains how this problem occurred, what the implications are for those people who might be affected, and how problems of this nature might be avoided in future. To get there, we need to dig a little into how web caching works.

Over on The Mozilla Blog, Eric Rescorla, the CTO of Firefox, shares insights on [What you need to know about Twitter on Firefox](https://blog.mozilla.org/blog/2020/04/03/what-you-need-to-know-about-twitter-on-firefox/), with this important reminder:


The web is complicated and it’s hard to know everything about it. However, it’s also a good reminder of how important it is to have web standards rather than just relying on whatever one particular browser happens to do.

## Web Caching Privacy Basics

Caching is critical to performance on the web. Browsers cache content so that it can be reused without talking to servers, which can be slow. However, the way that web content is cached can be quite confusing.

The [Internet Engineering Task Force](https://ietf.org/) published [RFC 7234](https://tools.ietf.org/html/rfc7234), which defines how web caching works. A key mechanism is the [ Cache-Control header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control), which allows web servers to say how they want caches to treat content.

Sites can to use Cache-Control to let browsers know what is safe to store in caches. Some content needs to be fetched every time; other content is only valid for a short time. Cache-Control tells the browser what can be cached and for how long. Or, as is relevant to this case, Cache-Control can tell the browser that content is sensitive and that it should not be stored.

Separately, in the absence of Cache-Control instructions from sites, browsers often make guesses about what can be cached. Sites often do not provide any caching information for content. But caching content makes the web faster. So browsers cache most content unless they are told not to. This is referred to as “heuristic caching”, and differs from browser to browser.

Heuristic caching involves the browsing guessing which content is cached, and for how long. Firefox heuristic caching stores most content without explicit caching information for 7 days.

There are a bunch of controls that Cache-Control provides, but most relevant to this case is a directive called ‘no-store’. When a site says ‘no-store’, that tells the browser never to save a copy of the content in its cache. Using ‘no-store’ is the only way to guarantee that information is never cached.

## The Case with Twitter

In this case, Twitter did not include a ‘no-store’ directive for [direct messages](https://help.twitter.com/en/using-twitter/direct-messages). The content of direct messages is sensitive and so should not have been stored in the browser cache. Without Cache-Control or Expires, however, browsers used heuristic caching logic.

Testing from Twitter showed that the request was not being cached in other browsers. This is because some other browsers disable heuristic caching if an unrelated HTTP header, [Content-Disposition](https://tools.ietf.org/html/rfc6266), is present. Content-Disposition is a feature that allows sites to identify content for download and to suggest a name for the file to save that content to.

In comparison, Firefox legitimately treats Content-Disposition as unrelated and so does not disable heuristic caching when it is present.

The HTTP messages Twitter used for direct messages did not include any Cache-Control directives. For Firefox users, that meant that even when a Twitter user logged out, direct messages were stored in the browser cache on their computer.

## Who is Affected?

As much as possible, Firefox maintains separate caches.

People who have different user accounts on the same computer will have their own caches that are completely inaccessible to each other. People who share an account but use different Firefox profiles will have different caches.

Firefox also provides controls that allow control over what is stored. Using [Private Browsing](https://support.mozilla.org/en-US/kb/private-browsing-use-firefox-without-history) means that cached data is not stored to permanent storage and any cache is discarded when the window is closed. Firefox also provides other controls, like Clear Recent History, Forget About This Site, and automatic clearing of history. These options are all documented [here](http://mzl.la/1BAQKDJ).

This problem only affects people who share an account on the same computer and who use none of these privacy techniques to clear their cache. Though they might have logged out of Twitter, their direct messages will remain in their stored cache.

It is not likely that other users who later use the same Firefox profile would inadvertently access the cached direct messages. However, a user that shares the same account on the computer might be able to find and access the cache files that contain those messages.

## What Users Can Do

People who don’t share accounts on their computer with anyone else can be assured that their direct messages are safe. No action is required.

People who do use shared computer accounts can clear their Firefox cache. Clearing just the browser cache using [Clear Recent History](https://support.mozilla.org/en-US/kb/delete-browsing-search-download-history-firefox#w_how-do-i-clear-my-history) will remove any Twitter direct messages.

## What Website Developers Can Do

We recommend that sites carefully identify information that is private using Cache-Control: no-store.

A common misconception here is that Cache-Control: private will address this problem. The ‘private’ directive is used for shared caches, such as those provided by CDNs. Marking content as ‘private’ will not prevent browser caching.

More generally, developers that build sites need to understand the difference between standards and observed behavior. What browsers do today can be observed and measured, but unless behavior is based on a documented standard, there is no guarantee that it will remain that way forever.