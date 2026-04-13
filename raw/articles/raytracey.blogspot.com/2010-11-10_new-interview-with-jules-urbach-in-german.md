---
title: New interview with Jules Urbach (in German)
url: http://raytracey.blogspot.com/2010/11/new-interview-with-jules-urbach-in.html
author: Sam Lapere
published: '2010-11-10'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Google translation from German](http://translate.google.be/translate?hl=en&sl=de&u=http://www.heise.de/ct/artikel/Cloud-Spiele-mit-Hollywood-Effekten-1102461.html&ei=8OPaTK2IAozrOZbvzJ8J&sa=X&oi=translate&ct=result&resnum=3&ved=0CCEQ7gEwAg&prev=/search%3Fq%3DCloud-Spiele%2Bmit%2BHollywood-Effecten%2Bjules%2Burbach%26hl%3Dnl%26client%3Dfirefox-a%26hs%3D4na%26rls%3Dorg.mozilla:nl:official%26prmd%3Do)

There's an interesting part about latency:


For encoding and decoding of 1080p we just need a millisecond, which is negligible. A data packet travels the nearly 4,000 miles between New York and Los Angeles in 85 milliseconds, in addition there are about eight milliseconds input delay. So we are below our targeted 100 milliseconds which doesn't matter for a 3D shooter like Crysis. If we distribute our hosting offerings to five strategically placed data centers in the U.S., the total latency drops to around 30 milliseconds. Our biggest concern is therefor not so much the connection speed, but server-scaling. After all, it costs a lot of money to provide one GPU per user. This is where virtualization comes into play: for example, on a modern graphics card we can run eight instances of the CryEngine. We also do not stream games 24 hours a day. Only five to ten minutes go by, until enough data is present in the local cache (on the client side) to run it from there. A title such as Lego Batman is streamed in the background in a single minute on the client computer, which again frees up resources on the server. This works on both the Mac and the PC - and we are working on a special mini-hardware that does the job without a local computer.



## 4 comments:

Thanks for the interview



I read about local streaming before. Otoy are offering two types of play. 1. The game is streamed directly off the cloud. 2. a small part of the game is downloaded as in progressive downloading like with Steam and then the rest is streamed. Which Steam doesn't do.

What's really interesting, is that it can stream under 100ms a 4000 mile trip from LA to NY from 1 data center. You have to be within 1000 miles from data center with Onlive. So I wonder if people in the UK could get access to the data center. As the UK is 3000 miles from New York.

I think I have read somewhere that OTOY will have cloud servers in Europe as well. OnLive is already testing servers here in Belgium and in the UK.

OTOY is vaporware and the average ping is 500ms in the real world.

Forget playing a FPS game in the cloud with the current technology.

OnLive has proven that it's perfectly possible to play an FPS from the cloud (with impercectible lag depending on your distance to the server) so I don't see any reason why OTOY couldn't do the same. They really need to start marketing and deploying the damn thing though.

Post a Comment