---
title: Using throttling to reduce network errors
url: http://joostdevblog.blogspot.com/2014/07/using-throttling-to-reduce-network.html
author: Joost van Dongen
published: '2014-07-27'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)by 10% by improving our throttling algorithm. While automatic throttling by a router is killing, smart throttling by the game itself can be a good tool to make the game work better on crappy internet connections. Today I would like to explain what throttling is and how we approached this topic.

(Note that the throttling improvements were in Awesomenauts

[patch 2.5.3](http://www.awesomenauts.com/forum/viewtopic.php?f=6&t=2440). This post is unrelated to the bandwidth optimisations in

[patch 2.5.4](http://www.awesomenauts.com/forum/viewtopic.php?f=19&t=33000)that are currently being tested in beta.)

The basic idea of throttling is that if you detect that an internet connection cannot handle as much as you are sending, then you start sending less. This can happen on the side of the game, or on the side of the connection itself (by the modem or router, for example). If we keep sending more than the connection can handle, then either we lose a lot of packets or, even worse, the internet connection is lost altogether, causing a network error. Throttling is intended to keep this from happening.

![](../../assets/7c60b553012033a3.gif)

The basic idea may sound simple enough, but actually implementing this is a lot more difficult. There are two problems: how can we reduce bandwidth dynamically, and how can we detect whether we need to throttle?

Lets start with how to reduce bandwidth. Modems usually have an approach to this that is simple enough: they just throw away some packets. This is a very efficient way of reducing bandwidth, but completely killing to any game. If a packet with important data is dropped then it needs to be resent. We cannot do this immediately as the internet connection doesn't notify the game that a packet was dropped. The only thing we can do is just wait for the acknowledgement to come in. If after a while we still haven't received an acknowledgement, then we conclude that the packet has probably been lost and needs to be resent.

Resending based on acknowledgements is the best we can do, but it is a pretty imperfect solution: the acknowledgement might still be under way. We cannot know whether it is, so we just need to pick a duration and decide to resend if that much time has passed. If we set this duration too long, then it takes very long before the packet is resent, causing extra delay in the gameplay if the packet was really dropped. If we choose a very short resending duration, then we will probably be sending a lot of data double that had actually already arrived. This wastes a lot of bandwidth and is not an option either.

![](../../assets/91625c80ac302466.jpg)

Since we cannot pick such a short resending time, we need to wait a little while before resending. This means that dropped packets arrive in the long run, but with an enormous delay. If for example the packet contained information on a player's death then he might die one second too late, which is really bad for the gameplay experience.

In other words: we never ever want the modem to throttle. We want to decide ourselves what gets thrown away, so that we can make sure that the really important packets are never dropped. If we need to throttle, then we want to at least throttle data that is less important. The problem with this is that if we could get away with sending less, then we would always do that instead of only when throttling. After all, an important goal in multiplayer programming is to use as little bandwidth as possible. This means that throttling comes with a drawback and we don't want to do it unless necessary.

In Awesomenauts we reduce bandwidth and packet count when throttling by sending less position updates. During normal gameplay Awesomenauts will send the position of a character 30 times per second. This way if a player turns around quickly, other players will know about it as soon as possible. If we send position updates less often, then we essentially add a bit of lag: we don't send the latest information as soon as we know it. We would prefer not doing that of course. However, if the alternative is that the modem is going to throttle by randomly throwing away packets that might be important, then our hand is forced and we prefer sending less position updates.

![](../../assets/87e0c01d14ddf5d3.gif)

Now that we know

*how*to throttle we get to the much more important question:

*when*to throttle. How can we know whether we need to throttle? It is not possible to just ask an internet connection how much bandwidth it can handle. Nor do you get notifications when the connection starts dropping packets because it is too much. We therefore can never know for sure whether throttling is needed and have to deduce this somehow.

Our initial approach to this was to throttle if the ping was too high. The idea is that if a connection cannot handle the packets it needs to send, then latency will increase and we can detect this. This works fine for connections that normally have low ping: if the standard ping is 50ms and suddenly it rises to 300ms, then it is extremely likely that we are sending too much and need to throttle to keep the connection from being lost altogether.

This approach is too simplistic however: internet connections are a very complex topic and can have all kinds of properties. Some people might indeed have a fast connection and a painfully low maximum bandwidth. However, if an Australian and a European player are playing together and they both have a really good internet connection, then their ping will still be high because the distance is so large. In this case throttling won't help at all. In fact, since our throttling essentially increases lag by sending less often, throttling in this case will actually decrease the quality of the connection!

This brings us to the change we recently made in Awesomenauts patch 2.5.3. Instead of looking at ping, we now look at packet loss. Awesomenauts uses UDP packets and we have our own manual reliability system, since various parts of the game require various degrees of reliability. This means that we send and receive our own acknowledgements and thus know exactly how many packets are lost. This is a much better indicator of connection problems than ping. If a lot of packets are dropped by the connection, then apparently we need to throttle to keep from sending too much over a limited internet connection.

It doesn't end there though. I already mentioned that internet connections are a complex topic, and this new plan too is thwarted. Some internet connections are just inherently lossy. For example, maybe someone is playing on a wireless connection and has a wall in between the computer and the modem. Maybe this causes 10% of all packets to be lost, no matter how many packets are sent. I don't know whether wireless routers actually work like that, but we have definitely seen connections that always drop a percentage of the packets, no matter how few we send. Since throttling increases lag we only want to do it when it significantly improves the internet connection. If, like in this case, throttling does not reduce the number of dropped packets, then we do

*not*want the throttle.

[Ronimo](http://www.ronimo-games.com)programmer Maarten came up with a nice approach to solve this problem. His throttling algorithm is based on letting the game perform little experiments. If a player has high packet loss, then the game enables throttling and starts sending less. Then it measures the packet loss again. If packet loss decreased significantly, then we keep throttling. If packet loss remains roughly the same, then we stop throttling and start sending at maximum sending rate again.

![](../../assets/af0527e83f70fb35.gif)

The result of this approach is that we only throttle if it actually improves the internet connection. If throttling does not help, then we only throttle shortly during those experiments. These experiments take place automatically during gameplay, but are short and subtle enough that players won't actually notice this happening. If the connection is really good, then we never ever throttle: we don't even do those experiments.

The result of adding this throttling algorithm is that network errors due to losing the connection have been reduced by 10%. This is not a spectacular improvement that many players will have noticed directly, but it is definitely significant enough that we are happy with this result.

In conlusion I would like to stress that internet connections are extremely unpredictable. We have seen all kinds of weird situations: connections that are really fast but stop for a few seconds every couple of minutes, connections that send packets in groups instead of immediately, connections that have low ping but also low bandwidth capacity, and many other combinations of properties. The big lesson we have learned from this is to not make assumptions about properties of internet connections, and to assume any random weirdness can happen for anyone's internet connection. This why I like the approach with the experiments so much: instead of assuming throttling works, it just tries it.

Smart solution! :) And interesting read, I definitely have a better idea now why network programming can be really complex. So much work for a small (but significant) improvement.


ReplyDeleteI myself have a wireless connection with a floor between my pc and the modem. It usually works fine if not too many people use it, but I do sometimes (still happening) randomly get thrown out and have to manually reconnect. So yeah, wireless connections are tricky.

Your explanation of why it's hard to know you're losing packets without waiting for an acknowledgment is clear. But then you say "we have our own manual reliability system... we send and receive our own acknowledgements and thus know exactly how many packets are lost." This apparently obviates the whole problem so why doesn't everyone do it?

ReplyDeleteThese are two different things. If you look back 5 seconds, then you can know what packets were dropped, since packets in practice hardly ever take that long to travel. For the purpose of throttling we can look at such a long period and thus know exactly how many packets dropped.


DeleteFor the purpose of resending we are looking at much shorter times, below one second. For such short durations it is impossible to know for sure whether a packet was really dropped or not.

i have an idea for a new character for awesomenauts, where can i send my idea to ? (awesomenauts has to have a email i just don't know it)

ReplyDeleteWe have a forum specifically for that, so you can post it there: http://www.awesomenauts.com/forum/viewforum.php?f=12 :)

DeleteInteresting article, thanks for the link! :) It is a pity I cannot reply to their post directly on their site. I'll reply here instead and try to contact them to read this and continue the discussion here. Their article is full of misconceptions about games but they obviously know a lot about the internet so I would be really interested in continuing the discussion here. :)






ReplyDeleteTheir main point indeed seems to be "use TCP". This is a really bad idea for games. In fact, amongst game developers it is common wisdom that real-time games should never use TCP for gameplay synching. The main reason is that TCP does packet ordering. If one packet drops, then all the packets after it are not passed to the game until that one packet is resent. This adds massive latency whenever there is a high packet loss, making games completely unplayable. For a fast game like Awesomenauts the ping needs to be well below 200ms for good gameplay. TCP also does a form of congestion control that is horrible for fast real-time games.

As for ping: the writer of that article assumes we use the ICMP Echo Request for ping detection, but we don't use that. Since we are constantly sending packets ourselves, we piggyback our ping messages to that. This allows us to send many pings per second without significant overhead, giving us pretty fast detection of ping changes. Ping for us is an average of those recent ping messages. If a packet is lost we consider that one really high ping, we don't just ignore it. This means that high packet loss greatly increases our version of ping. Technically this does not fall under the official definition of "ping" but it works well for what we want. It also means that if a connection suddenly starts dropping a lot of packets, then we also see our ping quickly increasing.

As for "bufferfloat": I didn't mention that because I don't know anything we can do in Awesomenauts to fix that problem. As far as I know it is a problem of the internet itself. IWL doesn't seem to give a solution for it either.

I was not aware of "DCCP". I looked it up and read some stuff about it, but couldn't get a clear overview of exactly how it would be used. Could you elaborate on that? Will DCCP allow me to know the state of the network so that I can decide exactly which data to drop and what to send, or will DCCP decide itself what to send? We need really tight control over what is sent and what is not sent and create different packets based on that. A single packet for us contains many sub-packets with different kinds of data, some of which needs to be sent quickly and some of which would be fine to just drop, so the game needs to decides what is dropped and what is not.

Since DCCP resides in the transport layer I also assume that DCCP would need to be a feature of the connection library we use? I have never seen an option for it in any of the libraries we have used, only TCP and UDP. Is that because of a lack of support, or because we should do DCCP ourselves over UDP or something like that?

Our newly revised posting is here:






ReplyDeletehttp://iwl.com/blog/some-thoughts-about-networking-for-game-developers

It includes:

---more context about where we are coming from

---an explanation about the IETF and the process for creating these network protocols

---some suggested protocols to consider SCTP, RTCP, RTP, and more

---clarification and expansion of the "ping" discussion

---a set of resources for characterizing network performance based on academic research

After some more internal discussions, we are not sure that DCCP would be the best solution. But to answer the questions about DCCP ... In order for a network protocol to move forward in the standards process in the IETF, there have to be at least two interoperable implementations. Sometimes this is called the "rough consensus, running code" rule. Sometimes these implementations are open source and sometimes a commercial product with a license. However, there would be no guarantee that an implementation would be available for all the game player potential platforms. So, in that case, yes you would have to do your own implementation. But let's see if we can find a network protocol(s) that comes closer to addressing your requirements.

Also, I have contacted some experts and described the requirements of the game application, and the experts are now weighing in. I will post that shortly.

As promised, here are some comments from Steve Casner who has been active in the IETF as a contributor, author, and Working Group Chair:




ReplyDeleteThe game developers have discovered that congestion control

is a requirement in any Internet protocol. That is a big step forward

relative to those who believe they can blast away with packets

however they like.

As your article says, they should draw on the knowledge that has

been built up in the IETF and the Internet community over

decades regarding RTT measurement and congestion control,

including what we've learned about how to detect and adapt

to congestion. However, I'm not sure that the existing protocols

will help them significantly. In particular, I agree with them that

TCP is not appropriate, at least not using a single TCP

connection, due to the "head of line blocking problem".

It might be possible for them to use multiple TCP

connections in parallel for different kinds of data, but

I'm not sure that would solve the problem, either.

RTP might be useful if its sequencing and timestamping

functions are needed, but RTCP feedback is probably

too low-rate to address the congestion control requirements.

This is a topic currently beingdiscussed in the IETF

AVTCORE and RMCAT working groups. Tracking

those working groups and getting involved in those

discussions would be a good idea.