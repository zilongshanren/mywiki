---
title: The European MDN access snafu – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/03/the-european-mdn-access-snafu/
author: Eric Shepherd
published: '2011-03-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Over the last couple of days, we had a problem come up that broke access to MDN documentation from Europe. I thought I’d share an explanation of what happened because it’s a slightly interesting story, and our European users deserve to know.

A few days ago, we started having a round of persistent spamming, with users creating accounts, posting a lot of spam, then I’d ban them, and they’d create another account and do it again. Finally, it became clear it was one user (or perhaps a small group of people working together) responsible for all of it, so I went into our tool that pulls up IP addresses based on username, found that indeed they were all coming from one IP address, and banned that IP address.

Now flash to our San Jose data center, where we have a proxy that handles routing. It had a minor configuration problem that had not previously been detected: instead of appending to the X-Forwarded-For header, it was replacing the header entirely. The result: the X-Forwarded-For header, instead of listing both the end user’s IP and any intermediate proxies’ IP addresses, only listed the most recent proxy’s IP.

So if a user connected to the documentation from somewhere in Europe, they’d pass through the Amsterdam proxy, which would forward them to the San Jose proxy, which would remove the end user’s IP address and replace it with the address of the proxy, resulting in the Amsterdam proxy looking like the end user’s IP address.

As a result, the tool that looks up the user’s IP address was reporting one of the Amsterdam proxy’s IP addresses instead of the user’s IP address, so what I banned was actually the Amsterdam proxy, which therefore meant our users in Europe couldn’t reliably connect.

Once we figured out what had happened, it was easy to fix: I removed the ban for the IP address in question, and IT fixed the configuration of the proxy in San Jose so that this shouldn’t happen again in the future.

Sorry for the problems, and welcome back to the wonderful world of MDN documentation!

## 2 comments

Danny MoulesMarch 29th, 2011 at 17:17Mike RatcliffeMarch 30th, 2011 at 10:35