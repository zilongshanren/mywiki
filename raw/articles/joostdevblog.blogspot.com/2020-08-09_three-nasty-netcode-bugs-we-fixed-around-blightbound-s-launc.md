---
title: Three nasty netcode bugs we fixed around Blightbound's launch
url: http://joostdevblog.blogspot.com/2020/08/three-nasty-netcode-bugs-we-fixed.html
author: Joost van Dongen
published: '2020-08-09'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Blightbound](https://www.blightbound.com/)we've been fixing a lot of bugs, including 3 very stubborn netcode bugs. They weren't any fun while we were looking for them for days, but now that we've found and fixed these they're actually quite intriguing. So today I'd like to share 3 of the more interesting bugs I've seen in the past few years.

[While these bugs mostly say something about issues in our code, I think they're also nice examples of how complex low level netcode is, and how easy it is to make a mistake that's overlooked for years, until a specific circumstance makes it come to the surface. All three of these bugs were also in the code of our previous game](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi9KTxiAyEAV3nA5t2pM4XqDCpYL_tI-B5QXfcZ5SaePM7kmJbIRMzFa5Fau0wKtZ_T6_KzE-YYpDHtnIHMTMO4Ov3QpOHAg3iDAKOsMQ4_WCgNTQ1qGDBFMycc75gtPcVqqmO4FqSojmEL/s500/Netcode+bugs+-+Blightbound.jpg)![](../../assets/187785a365520168.jpg)


![](../../assets/187785a365520168.jpg)

[Awesomenauts](https://www.awesomenauts.com/), but none of them actually occurred there due to the different circumstances of an Awesomenauts match compared to a Blightbound party.

The one thing all three of these bugs have in common is that they were very hard to reproduce. While they happened often enough to be game-breaking, they rarely happened in testing. This made them very hard to find. For the first two we found a way to reproduce them after a lot of experimenting, while for the final one we never got it ourselves until we had figured out the solution and knew exactly how to trigger it. Finding that one without being able to see it was some solid detective work by my colleague Maarten.

## Endless loading screens number 1

This bug occasionally caused clients to get stuck in the loading screen forever. After adding additional logging we saw that the client never received the HostReady message. This is a message that the host sends to the clients to let them know that loading is done and they should get into the game. The client was forever waiting for that HostReady message. Upon further investigation it turned out that the host did actually send the message, but the client received it and then threw it away as irrelevant. Why was that?

To answer that question, I need to give some background information. An issue with the internet is that it's highly unreliable. Packets can be lost altogether and they can also come in out-of-order or come in very late. One odd situation this can cause, is that a message from a previous level can come in once you're already in the next level, especially if loading times are very low. Applying a message from the previous level to the next level can cause all kinds of weird situations, so we need to recognise such an outdated message and throw it away. We do this with a simple

*level ID*that tells us which level the message belongs to. If we get a message with the wrong level ID, we discard it.

That's simple enough, but we saw that both client and host were in the loading screen for the next level. Why then would the client discard the HostReady message as being from the wrong level? The reason turned out to be in our packet ordering system. Some messages we want to process in the order in which they are sent. So if one message goes missing, we store the ones after it and don't process them until the previous missing one is received and handled.

The bug turned out to be in that specific piece of code: the stored messages didn't store their level ID. Instead, when they were released, we used the level ID for the message that had just come in. This went wrong when a message from the previous level went missing and came in a second or two too late. By that time the HostReady message had already been received, but had been stored since it needed to be processed in order. Since the level ID from the previous room was used for all out-of-order messages, the HostReady message was processed as if it came from the previous room. Thus it was discarded.

I imagine reading this might be mightily confusing, so hopefully this scheme helps explain what went wrong:

Once we had figured this out, the fix was simple enough: store the level ID with each message that is stored for later processing, so that we know the correct level ID when we get to it.

## Endless loading screens number 2

The second loading screen bug we had around that time had a similar cause, but in a different way. When a client is done loading, it tells the host so in a ClientReady message. The host needs to wait for that. Similar to the bug I described above, the ClientReady message was received but discarded because it was from the wrong level. The cause however was a different one.Sometimes the client starts loading before the host, for whatever reason. Since loading times between levels are very quick in Blightbound, the client can be done loading before the host starts loading. Once the client is done loading, it sends the ClientReady message. However, if the host isn't loading yet and is still in the previous room, then it discards the ClientReady message because it's from the wrong room. A moment later the host starts loading and when it's done loading, it starts waiting for the ClientReady message. Which never comes because it was already received (and discarded).

Here too the solution was pretty straightforward. We first changed the level ID to be incremental (instead of random) so that we can see in the level ID whether an incorrect message is from the next or the previous room. If it's from the previous room, we still discard the message. But if the message is from the next room, we store the message until we have also progressed to that room, and then process it.

## The big desync stink

The final netcode bug I'd like to discuss today is rather painful, because unlike the others it still existed at launch. In fact, we didn't even know about it until a day after release. Once we knew it existed it still took us days to find it. In the end this one was fixed in update 0.1.2, six days after launch.

So, what was the bug? What players reported to us was that randomly occasionally the connection would be lost. In itself this is something that can happen: the internet is a highly unreliable place. However, it happened way too often, but never when we tried to reproduce it, not even with simulated extremely bad connections. Also, we have code that recognises connection problems, but this bug didn't trigger that code, so the game thought it was still connected and kept playing, with very odd results.

After a few days a pattern started to emerge: many players reported that this always happened once they had notoriety 3 or 4, when a legendary item was attainable. We didn't think that the bug was actually linked to notoriety or legendary items, because these are quite unrelated to netcode. Instead, we suspected something else: maybe the bug happened after playing together for a certain amount of time.

With this hypothesis in hand we started looking for anything where time matters. Maybe a memory leak that grew over time? Or, more likely: maybe some counter that looped incorrectly? As I described in the above issues, netcode can have many types of counters. I already described the level ID counter and the counter for knowing whether a message is received in-order. There are others as well.

The thing with data that is sent over the netwerk is that it needs to be very efficient. We don't want to send any bytes more than necessary. So whenever we send a counter, we use as few bits as possible. Why send a 32 bit number when 16 bits will do? However, when using smaller numbers they will overflow more quickly. For example, a 16 bit number can store values up to 65,535. Once we go beyond that, it loops back to 0.

Often looping back to 0 isn't a problem: the last time we received the lower packets is so long ago that we won't have to expect any overlap with the last time we used number 0. However, we do need to handle the looping numbers correctly and not blindly throw away number 0 because it's lower than number 65,535.

And this indeed turned out to be the problem. One of the counters we used was a 16 bit number and after about one hour it looped back. In that particular spot we had forgotten to include code to handle that situation. The result is that from there on the game received all messages but discarded them without applying them. Like in the cases above, the solution was simple enough to implement once we knew what the problem was.

One question remains: why wasn't this a problem in Awesomenauts? For starters, Awesomenauts matches are shorter and the connection is reset after a match. So the counter never reaches 65,535. In Blightbound however the connection is kept up in between dungeon runs, so if players keep playing together the number will go out of bounds. But there's more: if the bug would have happened in Awesomenauts, the game would have thought it was a disconnect and would have reconnected, resetting the counter in the process. In Blightbound we determine connection problems in a different way, causing the connection to not be reset in this particular case.

## A lesson relearned

Netcode being hard is not new to us and getting weird bugs is inherent to coding such complex systems. However, there is one step we did for Awesomenauts that we didn't do here: auto testing. Since Blightbound uses a lot of netcode from Awesomenauts and Awesomenauts has been tested endlessly, we thought we didn't need to do extensive auto testing for this same code in Blightbound. This was a mistake: the circumstances in Blightbound turn out to be different enough that they cause hidden bugs to surface and wreak havoc.

We're currently running autotests for Blightbound to further stabilise the game. This already resulted in another netcode fix in

[update 0.1.2](https://www.blightbound.com/game-updates)and several obscure crash fixes that will be in the next major update.To conclude I'd like to share this older but still very cool video of auto testing in Awesomenauts. It shows four computers each randomly bashing buttons and joining and leaving matches. The crazy movement of the Nauts is fun to watch. For more details on how we implemented auto testing in Awesomenauts, have a look at

## No comments:

## Post a Comment