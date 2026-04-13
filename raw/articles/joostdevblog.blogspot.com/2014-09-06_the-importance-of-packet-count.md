---
title: The importance of packet count
url: http://joostdevblog.blogspot.com/2014/09/the-importance-of-packet-count.html
author: Joost van Dongen
published: '2014-09-06'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)we learned that packet count can in some cases be equally important. Somehow I have rarely seen this mentioned in articles or books, so I figured it was about time to write a blogpost to tell the world:

**packet count is also important!**

When we started development of Awesomenauts I though that packet count was only relevant because of the size of the packet headers. Every UDP packet has a UDP header (8 bytes) and an IP header (at least 20 bytes). This means that no matter how little data you send per packet, it always gets an added 28 bytes. This makes packet count relevent for bandwidth: if you send 200 packets per second, then you are sending 5600 bytes per second only in headers.

I thought this is where the importance of packet count ends. If I can somehow optimise my game to send only 30 bytes per packet, then it is okay to send 200 packets per second because the total bandwidth will still only be 200 * (20+8+30) = 11600 bytes per second, which is fine for a modern game.

It turns out that this is not true on the real internet. During development of Awesomenauts we found out that high packet count by itself is a serious problem. Quite a few internet connections that would happily send as much as 40 packets per second of 1200 bytes each (totalling 48kB/s) become problematic when they need to send 200 packets per second of 50 bytes each (totalling only 10kB/s).

![](../../assets/4db2a09126e585ad.gif)

In our experience sending more than 100 packets per second is problematic for some connections, resulting in packet loss, lag spikes and ultimately losing the connection altogether. We recently decreased the average send rate in a full Awesomenauts match from 150 packets per second to 75 and this seems to have decreased the number of connection errors by around 25%. In that same patch we also decreased the average bandwidth by 50%, so I cannot say for sure whether decreasing just the packet count would have had the same effect. However, based on earlier experiments with this I think the packet count decrease was more important than the bandwidth decrease. Our impression is that packet counts above 100 per second are a problem while below 100 packets per second it is not very relevant to optimise further

The internet in general is a weird topic because it behaves so unpredictably on some connections. For example, we have seen that some routers always bunch our packets: they constantly arrive two at a time even though there is 33ms between sending.

Note that there is more to packet headers and overhead than the UDP and IP headers I mentioned above. For example, I recently learned that when on a DSL line an extra DSL header is added. This is all hidden from the game code, but it means that having lots of packets can on some connections also mean using more bandwidth than you realise.

So there you have it: be mindful of your packet counts! Sending lots of small packets is not a good idea and should be avoided if possible. This is especially relevant for peer-to-peer games, since everyone in the game talks to everyone else and packet counts thus rise quickly.

Awesome blog and thanks for sharing your knowledge and thoughts!

ReplyDeleteI would love to read a post about 2d collision in your games :)

Thanks

Lukas

Some people have asked for that before but I am reluctant to write about that because I am not quite happy with our collision handling code in Awesomenauts. It is filled with difficult-to-understand exceptions and such... Which is extra embarrassing because it seems like such a simple topic!

DeleteIt is good to see, that im not the only one who has little problems with collision detection :) In 2D i mostly use raycasts, but as you say the code gets often messy!

DeleteOur main problem is the glass platforms: you can jump down through those but can also stand on them, and you can jump up through them. Physically that concept is really weird and this shows in the code: there are all kinds of weird exceptions for them, especially for when they are also moving vertically.


DeleteWe don't use raycasts for collision handling by the way: practically everything is box-box collision with AABBs.

Thanks for explaining :)

DeleteI think i will try to use box-box collisions next time, maybe a mix of both box and raycasts!

Why would you want to use raycasts at all? Are these very fast-moving objects? Usually player collision is all about volumes in my experience.

DeleteI think that raycasts are for performance, but this could be wrong!

DeleteI also remember that in a official unity3d video, they said that in 2D you should use raycasts for more precision or so...

But i will implement both collision methods in my experimental "engine"! Propably they have talked about fast objects and the more i think about your question, the more i think you are right and raycasts are not that great for this type of collision!

You will probably need a bunch of raycasts per character in several directions, which would definitely be slower than a single box check.

DeleteOk, i will try box collision today, i think! Thanks :)

DeleteYet another great post, love hearing about the challenges which arise in supporting this game and how they are being addressed.





ReplyDeleteI've been curious about one detail in the Peer-to-Peer networking, considering a case where:

- Some players are connecting to an online battle from within the same LAN, where perhaps direct communication on the LAN would be possible

- Other players are not a part of the LAN and communication must occur via the Internet

Does Awesomenauts initiate local peer-to-peer connections?

A typical Awesomenaut session for me usually involves 2-3 PCs on a LAN connecting with other players on the Internet.

We don't have anything specifically for a LAN, but Awesomenauts does make direct connections between players. I don't know how routers handle this kind of situation but I sure hope that the average router recognises that a message is being sent to another computer on his own network and thus doesn't send the packet outside the building. We don't use relay servers or anything like that so Awesomenauts itself does not impose sending anything over long unneeded distances.

DeleteAh right that is a good point; if the router is doing it's job intelligently it should be providing that functionality without the Ronitech having to worry about those types of networking details.


DeleteThanks for the clarity; I may try and spin up a test at home to see how my router handles this.