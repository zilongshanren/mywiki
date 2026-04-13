---
title: Dynamic batching and Deferred
url: https://cmwdexint.com/2017/07/14/dynamic-batching-and-deferred/
author: Ming Wai Chan
published: '2017-07-14'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

Vert and Frag + **Zwrite On** in Deferred are not dynamically batched

(it means transparent shaders will be batched)

unless the shader writes into GBuffer. But then, putting “DisableBatching” = “True” into this shader, it is still batched!

Vert and Frag + **Zwrite On** in Deferred are not dynamically batched

(it means transparent shaders will be batched)

unless the shader writes into GBuffer. But then, putting “DisableBatching” = “True” into this shader, it is still batched!