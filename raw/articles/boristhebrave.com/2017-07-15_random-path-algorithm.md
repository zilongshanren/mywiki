---
title: Random Path Algorithm
url: https://www.boristhebrave.com/2017/07/15/random-path-algorithm/
author: Boris
published: '2017-07-15'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Quick follow up to [my previous post](https://www.boristhebrave.com/2017/07/08/fast-traversal-queries-of-procedurally-generated-rooms/), I found the same technique is pretty good at generating organic looking random paths. You simply start with an empty room, and keep randomly filling points until it is no longer possible to add any more without disconnecting the room. What’s left is a nicely wiggly pathway.


Try a demo. Click to add/remove anchor point, where the path *must* pass through.