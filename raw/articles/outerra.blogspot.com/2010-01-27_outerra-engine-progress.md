---
title: Outerra Engine Progress
url: https://outerra.blogspot.com/2010/01/outerra-engine-progress.html
author: Outerra
published: '2010-01-27'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Lots of stuff has been done on the visuals - shadows are finally in, and even though they are not finished yet the output is much nicer with them. It uses a randomized lookup into the shadow map but the blurring pass is not present yet, so the closeups show noisy shadow edges. This will go away with the blurring pass on the shadow map.

![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_tSbTpLVvgV2Vp_Wh05EQa680YNXQRhtFhayDNvuBBtDxuTjeKo-DiJb-fGxYiiBW_xsCv4f1q5_DBfcZFKbjD2pqSmtCiF1zRx=s0-d)


The ugly patterns on the ground visible in older screen shots, resulting from tiled textures have been suppressed by more fractal magic - a free fractal channel has been used to mix three textures (daisies, grass and a lighter grass) together and the pattern is almost completely gone.

![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_tyMYfLFNFjdMUnU6wCy5DXucmMWk6R6tKxzM066BJg-WRFVIHuXt7EqRpzpkZg6gSIr67UNBHv0XkH83gtX6MYPou9EOUVUsoW=s0-d)


Another thing that helped a lot was the color transformation to

[linear space](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch24.html). This included both the input (loading the textures in sRGB format and also correctly computing the mipmaps) and setting the render target. The fix is most obvious on the atmosphere that now looks more natural.

![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_upTP9w5r4P3RPr88MKcL7sqvI8zokDHrFAZmTzjmSY2PPSmyTkK7-wFlOnxfu2fYA_a76k5dnTsTPeyNmT_JWKLXR07sRtcE8u=s0-d)


The trees are also slightly randomly colorized to break the monotonicity.

![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_vJAxIoKdt6r8RCnTMxdx_5tdgvrr2rj9fONaZiuA0SZPLCeK2GIw1uAvKh-1a2Aq4ZB07VeenRV9FmWiOp2UFoFx6irgm3uxhf=s0-d)


The material system has progressed as well, as it can be seen on the new truck model here.

![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_tZ1l20Gg3kZnpqsCf_ixE8muY7D6xrsPRbrGEScmV-crWdcaPlmMyzJR3izLio9bKMCQUjXOj9OrjZiLgNAc7Ot1tK63nfs9Go=s0-d)


![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_sNo-cK_Vs_yqGtHj2cYCdbNLIk67lF27TKnoAxwYbRimU2L5pWy2muYK2QDUX8n-egxPuIo2agyLYw2BA2acqqxzhwkKMsbFTR=s0-d)


![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_vcZu-ZZqy0KmOKXO8zn1QW-mnFV1XH5PPPa1F5PxmN4x6osqi73Nbb78jFM2o05H_Y7bJqNBE8rcoR6NUTctkCpHFkdt-8tHRV=s0-d)


Also new is the support for dirty windows.

![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_sOUtKp6ItfpJT69k9KVmVEFMo3xZo__5p99lcoLPOepyAVtLn9w1TNkpUtkvLpV3HSpI3sxvBTuXyR2puJ855X0TrS6LVYS0Jb=s0-d)


A gun is mounted on the roof, with a separate controller. It should be also functional soon, along with some flying prey to ground

![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_vpRYkZvq1WI8QFmGOBpQZ538I0NWjkxeX088XTI12su628jZ4zqYMysRwg1dHwBLjidJ3aX8624sYQCClZSb3WEblOH9PsmSAT=s0-d)


![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_tgDQUFls63IvJ3FWV2rvk6LOoP8-diME0tbTCNnApp9oN8FBW6y2vPVseQ0e-WKZ0nEtg6S_fYiswbP_3Jscd-6VTdLOUMsO-W=s0-d)


![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_s68YoxaWjkySuAFmYKHn8vYQD1kR8jlQ8qCh9CQIP6JU29_syIrF4c7akjIdGxJwKiEYaZdwIMO6gqToMm76Ld6rNV-WSINg=s0-d)


![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_upVo-Qjo0ee7kDcpuSsBzu6PHUzNIIZCzcNy3ew1TuyJLgbo8_xiww3YwI7GQmRUkmln2ecyLN8O4z3JMiP0oryS120VoS-MA=s0-d)


The new model appearing in the shots is the Tatra T813 8x8 heavy all-terrain truck with unique independent swing half axles. I wrote specialized code to handle its physics, and it works quite nicely. It is much better visible in motion, a video will be coming soon.

![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_vDIqaakczp96yKTHNT-VJWaZQFQYRxSGEe5mUaX2BboseV0jHPdO5u_L_vRFtOKGq-u4XqufuXKtEBeQShwWxClp3B7yQGWwg=s0-d)


![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_tT7Hj-n5kalcdmv0l4fB-2ivrXsTWHPT1d5pbmPAwr9JPTkby_g09dIpKcK48Mldpy5DrXO20A6HtIGuJ53lRftOUP3PvtmU1E=s0-d)


![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_uTWWGR9qRf962WYbtNajBjEXvivw9Npy95JlZZqYwk8xSTrLxVSTnnjAKm6o14X1ULbtZjNCIpjmM2bhrFMc72yb87oK260dI=s0-d)


![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_vpyP6KGMVuMdgLULRnWk7MrZxDvLyygw3RKQ9uFJQqXhzP-_u4e9SZNBDgkB1OAeFRFU67UsP0f-t0B4P-NSsssgnAI1u6DNcT=s0-d)


## 4 comments:

That is amazing! Im really looking forward to test this one day. Great job!

It will be available for download soon?



I would like to test by myself all those amazing capabilities - especially for roads and terrain vehicles, because I'm a fan of vehicle simulators like Racer at www.racer.nl.

Use Google Earth as 'virtual traveling' was always a dream for me.

Congratulations for this noticeable effort.

Thanks. We are working on the demo where you'll be able to fly a plane and drive the truck, so hopefully there will be something by the end of the month.

Post a Comment