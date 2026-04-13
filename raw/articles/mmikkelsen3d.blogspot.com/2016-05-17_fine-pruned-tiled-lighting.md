---
title: Fine Pruned Tiled Lighting
url: http://mmikkelsen3d.blogspot.com/2016/05/fine-pruned-tiled-lighting.html
author: Morten S Mikkelsen
published: '2016-05-17'
source_blog: Mikkelsen and 3D Graphics
source_site: http://mmikkelsen3d.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

During the development of Rise of the Tomb Raider (ROTR) we came up with a new tiled lighting variant which we named Fine Pruned Tiled Lighting (FPTL) which we describe in GPU Pro 7. There are many details to the full implementation discussed in the article and I will not go over them here but the main point is the cost of fine pruning can easily be absorbed by using asyncronous compute. This implies we obtain a light list with a very minimal amount of false positives almost for free.

As explained in the article the technique will work with essentially any methodology such as deferred shading, pre-pass deferred, tiled forward and even hybrids between these. A

[demo sample](https://github.com/wolfgangfengel/GPU-Pro-7/tree/master/02_Lighting/02_Fine%20Pruned%20Tiled%20Light%20Lists)is available though it was written in vanilla directx 11 which implies the asyncronous compute part is left as an exercise for the reader! The demo shows a single terrain mesh lit by 1024 lights (heat map and fine pruning enabled by default). For simplicity the demo is setup as tiled forward though on ROTR we used a hybrid where we supported pre-pass deferred, tiled forward and conventional forward.

When running the demo you will notice fine pruning enabled runs faster than disabled despite the fact that there is no asyncronous compute in the demo (since it is standard DX11). However, the improvement on speed is of course much more significant when asyncronous compute is used correctly.

Other interesting aspects to the implementation is we determine screen-space AABBs around each light (regardless of type of shape) on the GPU. This allows us to reduce coverage significantly for partially visible lights (accellerates fine pruning) and reduces pressure on registers during light list generation (explained in the article). Additionally, we keep light lists sorted by type of shape to miminize chances of thread divergence during tiled forward lighting.

For more information on the details....Buy GPU Pro 7! :)

This comment has been removed by a blog administrator.

ReplyDeleteGambling 101 - Casino and Gaming Guide [mgc]

ReplyDeleteThis guide shows 충주 출장마사지 you the casino 화성 출장안마 gaming 이천 출장마사지 laws, how to legally gamble 강원도 출장안마 online, the laws, how to get gambling licenses and information 김제 출장샵 on the