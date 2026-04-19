---
title: Notes on optimizing a deferred renderer
url: https://c0de517e.blogspot.com/2012/10/notes-on-optimizing-deferred-renderer.html
published: '2012-10-08'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Oh my, I forget to post things... Space Marine, a game that I'm very fond of having been part of. The second third person action done by Relic, and the first multi-platform console game of a studio well known for incredible PC RTS titles. It came out maybe a bit short on content (cuts, time...) but it's a technically excellent game and it's plenty of fun too (it's one of the few games I had fun playing multiplayer on the 360).


Its rendering does most of the things a modern deferred should do, quite a few things that only an handful of other titles manage to pull off (i.e. almost zero latency) and a couple of novel things as well (the way it does Oren-Nayar, its "world occlusion", the DOF/MB filter, the hair lighting trickery and some other details).



The people working on it were a-m-a-z-i-n-g, I was "overseeing" the rendering performance across the platforms and I was surprised to see that we managed to more than double rendering performance in the six months before shipping, to a solid thirty (I would have bet it was not possible, when I joined. They proved me wrong).

Most of the work described in the notes was done near the end of the product (i.e. shadows, post effects, ssao were rewritten from scratch, software occlusion added, SIMD and threading everywhere, I had a list of more than twenty tasks per each platform and I'd say more than 80% of them were done by the end).


This presentation was done a while ago now, it started as something I wrote internally as a post-mortem for other studios to see, then I removed some implementation details and presented it (thanks to Relic's openness when it comes to sharing knowledge) at a very informal meeting of rendering professionals I organize sporadically here in Vancouver. The version I'm uploading was cleaned up even more (well, censored... mostly replaced images with public screenshots of the game) to be able to publish it online... but then forgot, until today, when I got someone asking me for this material again.

Its rendering does most of the things a modern deferred should do, quite a few things that only an handful of other titles manage to pull off (i.e. almost zero latency) and a couple of novel things as well (the way it does Oren-Nayar, its "world occlusion", the DOF/MB filter, the hair lighting trickery and some other details).

The people working on it were a-m-a-z-i-n-g, I was "overseeing" the rendering performance across the platforms and I was surprised to see that we managed to more than double rendering performance in the six months before shipping, to a solid thirty (I would have bet it was not possible, when I joined. They proved me wrong).

Most of the work described in the notes was done near the end of the product (i.e. shadows, post effects, ssao were rewritten from scratch, software occlusion added, SIMD and threading everywhere, I had a list of more than twenty tasks per each platform and I'd say more than 80% of them were done by the end).

This presentation was done a while ago now, it started as something I wrote internally as a post-mortem for other studios to see, then I removed some implementation details and presented it (thanks to Relic's openness when it comes to sharing knowledge) at a very informal meeting of rendering professionals I organize sporadically here in Vancouver. The version I'm uploading was cleaned up even more (well, censored... mostly replaced images with public screenshots of the game) to be able to publish it online... but then forgot, until today, when I got someone asking me for this material again.

## 3 comments:

hi,



I have a lot of trouble consulting your document on scribd. Is it possible to have it from another plateform ?

The whole stuff seems really interesting.

I think you should be able to download a pdf from scribd if the online viewer gives you issues

Yeah... If you have an account (which costs money).

I recommend using this website instead: https://scribdownload.com/

Post a Comment