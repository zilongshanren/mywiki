---
title: Vaulting Out of Walled Gardens with Fancy Links – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2016/09/vaulting-out-of-walled-gardens-with-fancy-links/
author: Dietrich Ayala Posted; Web Developers
published: '2016-09-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Have you ever noticed that in Twitter, Facebook, Google and Pinterest some links are displayed quite fancily, with preview images, descriptive text summaries and other information?

These links are

*fancy*because of metadata in the source code of the web page itself, implemented specifically for the rich display of links inside each of these companies’ content platforms.
Unfortunately for developers, each of these internet industry titans has implemented their own metadata formats for this: Twitter has

[Cards](https://dev.twitter.com/cards/overview), Facebook and Pinterest use[Open Graph](http://ogp.me/)metadata and Google uses[Schema.org](http://schema.org/)markup.
Thus creating a

**<header> soup of doom**for each and every individual developer who dares to tread this path:![screen-shot-2016-09-09-at-12-30-58-pm](../../assets/282a8789b0162a68.png)

Well that looks like a

**mess**. And it’s different for each website. However, it’s worth doing for two reasons:The first reason is that fancy links increase click-through rates,

**increasing engagement and driving traffic**to your website. This is good for your blog, your business, or whatever reason you’re sharing the link in the first place.The second reason is that high click-through rates in walled gardens mean people are

**escaping**those walled gardens, spending time on the Wild Wild Web.![screen-shot-2016-09-09-at-12-30-00-pm](../../assets/40573616742bbbce.png)

Silo Buster is an easy-to-use website where you enter a small amount of information, and all that <header> goop is generated for you. You can then copy and paste it into your web pages or integrate it into your template or content management system.

Take

[Silo Buster](https://autonome.github.io/silobuster/)for a spin, and then check your analytics and see if there’s any change. Experiment with it: Tweak the photos, or the summary text and check again.If you’d like to learn more about how these sites implement their metadata, and how to debug your rich links, check out the links at the bottom of Silo Buster.

If you’ve got other tips and tricks for fancy links, or experiences either good or bad with them, share your thoughts in the comments!

## 7 comments

Gabriel FinkelsteinSeptember 12th, 2016 at 09:56Dietrich AyalaSeptember 13th, 2016 at 05:25FloSeptember 12th, 2016 at 10:51Šime VidasSeptember 12th, 2016 at 19:04Dietrich AyalaSeptember 13th, 2016 at 05:26soleSeptember 13th, 2016 at 05:26Šime VidasSeptember 13th, 2016 at 18:00