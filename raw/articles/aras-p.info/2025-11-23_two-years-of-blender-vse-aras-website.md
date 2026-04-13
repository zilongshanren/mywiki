---
title: Two years of Blender VSE · Aras' website
url: https://aras-p.info/blog/2025/11/23/Two-years-of-Blender-VSE/
published: '2025-11-23'
source_blog: Aras' website
source_site: https://aras-p.info/
category: graphics
fetched: '2026-04-13'
---

So,

[Blender 5.0]has shipped while I was away at the excellent[Graphics Programming Conference], but while all that was happening, I realized it has been two years since I mostly work on the Blender Video Sequence Editor (VSE). Perhaps not surprisingly, a year ago it was[one year of that]:)

Just like [two years ago when I started](https://aras-p.info/blog/2024/02/06/I-accidentally-Blender-VSE/),
I am still mostly flailing my arms around, without realizing what I’m actually doing.

### The good

It *feels* like recently VSE did get quite many improvements across workflow,
user experience and performance. The first one I contributed anything to was Blender 4.1,
and look what has happened since then (pasting screenshots of the release overview
pages):

4.1 ([full notes](https://developer.blender.org/docs/release_notes/4.1/sequencer/)):

![](../../assets/fbeb608a398743f3.png)

![](../../assets/201c1fac3fa0d4c5.png)


4.2 ([full notes](https://developer.blender.org/docs/release_notes/4.2/sequencer/)):

![](../../assets/a184c6814e835a5c.png)

![](../../assets/4b525ed172dc136e.png)


4.3 ([full notes](https://developer.blender.org/docs/release_notes/4.3/sequencer/)):

![](../../assets/b7dee09ef094af89.png)

![](../../assets/87b6fc572f15ecfd.png)


4.4 ([full notes](https://developer.blender.org/docs/release_notes/4.4/sequencer/)):

![](../../assets/d1a5e0b1510a96c0.png)

![](../../assets/5c19f42a3e00ebe2.png)


4.5 ([full notes](https://developer.blender.org/docs/release_notes/4.5/sequencer/)):

![](../../assets/b5dc3f7e4aecb6d8.png)


5.0 ([full notes](https://developer.blender.org/docs/release_notes/5.0/sequencer/)):

![](../../assets/f1202e75a23502d6.png)

![](../../assets/e3b02356e60ad66f.png)

![](../../assets/da55f78d4b7a06a9.png)

![](../../assets/762b3bc23284a7f7.png)


In addition to user-facing features or optimizations, there also has been quite a lot
of code cleanups; too many to list individually but for a taste you could look at “winter of quality”
task list of last year ([#130975](https://projects.blender.org/blender/blender/issues/130975))
or WIP list of upcoming “winter of quality”
([#149160](https://projects.blender.org/blender/blender/issues/149160)).

All of this was done by 3-4 people, all of them working on VSE part time. That’s not too bad! I seem to have landed about 200 pull requests in these two years. Also not terrible!

For upcoming year, we want to tackle three large items: 1) more compositor node-based things
(modifiers, effects, transitions) including more performance to them, 2) hardware acceleration
for video decoding/encoding, 3) workflows like media bins, media preview, three point editing.
That and more “wishlist” type of items is detailed in
[this devtalk thread](https://devtalk.blender.org/t/video-sequence-editor-vse-2026-roadmap/43206).

If you have tried Blender video editor a long time ago, and were not impressed, I suggest you try
it again! *You might still not be impressed, but then you would have learned to not trust
anything I say :P*

### The bad

It can’t all be good; some terrible things have also happened in Blender VSE land too.
For one, I have became the “module owner” (i.e. “a lead”) of the VSE related work. *Uh-oh!*

### The wishlist

From the current
“[things we’d want to work on](https://devtalk.blender.org/t/video-sequence-editor-vse-2026-roadmap/43206)”,
an obvious lacking part is everything related to audio – VSE has *some* audio functionality,
but nowhere near enough for a proper video editing toolbox. Currently out of “just, like, three”
part-time people working on VSE, no one is doing audio besides maintenance.

More community contributions in that area would be good. If you want to contribute, check out
[new developer documentation](https://developer.blender.org/docs/handbook/new_developers/)
and `#module-sequencer`

on the
[developer chat](https://developer.blender.org/docs/handbook/communication/chat/).