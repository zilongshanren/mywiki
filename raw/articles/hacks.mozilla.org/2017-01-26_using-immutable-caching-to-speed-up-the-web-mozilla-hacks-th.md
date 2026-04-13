---
title: Using Immutable Caching To Speed Up The Web – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/01/using-immutable-caching-to-speed-up-the-web/
author: Patrick McManus
published: '2017-01-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When Firefox 49 shipped it contained the [Cache-Control: Immutable feature](https://bitsup.blogspot.com/2016/05/cache-control-immutable.html) to allow websites to hint which HTTP resources would never change. At almost the same time, Facebook began deploying the server side of this change widely. They use a URI versioning development model which works very well with immutable. This has made a significant impact on the performance of Facebook reloads with Firefox. It looks like other content providers will adopt it as well.

The benefits of immutable mean that when a page is refreshed, which is an extremely common social media scenario, elements that were previously marked immutable with an HTTP response header do not have to be revalidated with the server. Lacking this hint, the browser needs to guess which objects may or may not change on reload – wasting time on one hand or risking website incompatibility on the other.

For smaller objects, the work of this revalidation via a 304 HTTP response code can be almost as much work as just transferring the response fully.

It turns out this can save a lot of work. The page’s javascript, fonts, and stylesheets do not change between reloads. More importantly, the dozens of images do not change either – different images may be included by the markup, but the content of individual images do not change. Indeed, about the only thing that might change is the markup itself.

For Firefox users reloading Facebook content this has been a tremendous boon – the fastest request is one that is never made, and that is exactly what happens over and over again when refreshing a Facebook page. In my testing a typical feed may initially be comprised of 150 different resources. Pressing refresh in Firefox 49 generates just 25 network requests.

![meta-chart](../../assets/647f10ff5dfbebc0.png)


As you might imagine, this radically speeds things up. In my testing, it can often cut page reloading time in half. Facebook was also an early adopter of the brotli compression encoding. They use that to reduce the bandwidth usage of the dynamic markup, which cannot be cached, saving around 20% of the bytes transferred when compared to the older gzip standard. [Brotli has been available in Firefox](https://hacks.mozilla.org/2015/11/better-than-gzip-compression-with-brotli/) since Firefox 44.

Facebook’s servers are big winners too of course – a request never made saves bandwidth and CPU utilization which can in turn be spent on making the site faster for other requests.


“This change effectively eliminated revalidation requests to us from up-to-date versions of Firefox which, in many cases, can improve load times by seconds.”– Nathan Schloss, Software Engineer, Facebook


### WE’RE GROWING


Facebook has been a great partner in this effort. Lately I’ve been spreading the word about immutable and other developers are adopting it too.

The BBC has picked it up on a trial basis:


[@mcmanusducksong]I’ve only had a quick look but immutable seems to be working well for us too. Bonus is how easy it is to implement :-)— Neil Craig (@tdp_org)

[October 27, 2016]

Anecdotally, BBC sees reload times improve up to almost 50%, and finds 90% of requests are optimized away by immutable.

Implementations as future-looking as the [InterPlanetary File System](https://ipfs.io/) are interested too:


[@bergie][@mcmanusducksong][@jaffathecake]In fact go-ipfs already sets Cache-Control: immutable since v0.4.2 :)— IPFS (@IPFSbot)

[October 28, 2016]

Also, products as venerable as the [Squid proxy](http://www.squid-cache.org/):

![sq](../../assets/3000869b19f6d507.png)


This has enough experience in the wild now to heartily recommend its use. To ensure adequate documentation it has also been adopted into the [IETF](https://tools.ietf.org/wg/httpbis/draft-ietf-httpbis-immutable/) on the Standards Track. All you need is a [proper caching header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control) to get started with your development.

## About Patrick McManus

Principal Engineer at Mozilla focused on Platform Networking

## 28 comments

Jeff R.January 26th, 2017 at 10:43JayFebruary 9th, 2017 at 10:01Gerd NeumannJanuary 26th, 2017 at 11:42JeremieJanuary 26th, 2017 at 12:58Patrick McManusJanuary 27th, 2017 at 04:49Joshua SinkfieldJanuary 26th, 2017 at 14:48Jason BrownJanuary 26th, 2017 at 15:58OmegaJanuary 26th, 2017 at 17:17Patrick McManusJanuary 27th, 2017 at 04:48Sjon HortensiusJanuary 27th, 2017 at 00:34Patrick McManusJanuary 27th, 2017 at 04:47Maarten ScholderJanuary 27th, 2017 at 05:23Gerd NeumannJanuary 27th, 2017 at 05:42AnchalJanuary 27th, 2017 at 00:49Justin AveryJanuary 27th, 2017 at 01:59Patrick McManusJanuary 27th, 2017 at 04:44Jason GrigsbyJanuary 30th, 2017 at 10:49Jason GrigsbyJanuary 30th, 2017 at 12:32Wellington TorrejaisFebruary 2nd, 2017 at 15:16Tara LiFebruary 4th, 2017 at 10:40Jeremie MFebruary 5th, 2017 at 10:49Tara LiFebruary 18th, 2017 at 10:49Patrick McManusFebruary 18th, 2017 at 14:21RyanFebruary 6th, 2017 at 13:25CoryFebruary 7th, 2017 at 16:57Patrick McManusFebruary 8th, 2017 at 05:22CoryFebruary 8th, 2017 at 08:13YoFebruary 8th, 2017 at 12:34