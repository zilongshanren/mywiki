---
title: Relay servers
url: http://joostdevblog.blogspot.com/2014/09/relay-servers.html
author: Joost van Dongen
published: '2014-09-21'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[core network structures for games](http://joostdevblog.blogspot.ch/2014/09/core-network-structures-for-games.html). There is one really important topic that I left out then:

*relay servers*. Relay servers are especially important to understand since I have recently heard them confused with dedicated servers quite often. Today I would like to explain what relay servers are, and what they are not.

A relay server is essentially just a computer that sends and receives packets. It does not really process data and does not do any gameplay logic. All it does is that if player A sends a packet to player B, then instead of sending it directly player A sends it to the relay server. The relay server then sends it to player B. The relay server is essentially just a glorified router.

![](../../assets/f229e2d6df09923f.gif)

So why is this useful? Relay servers have two big advantages. The first is that players can practically always connect to them. Security measures in routers are a big problem in internet connections, causing many users to not be able to connect to each other directly. Usually this can be solved in the router settings by setting UPNP or port forwarding, but many users don't know how to do this. Techniques like NAT punch-through help, but still don't solve the problem in a lot of cases.

An important aspect of connectivity issues is that if

*one*of the two computers that try to connect to each other is set up entirely right, then it is almost always possible to connect the two computers, no matter how badly the other computer is set up. This is where relay servers come in: the developer manages those and can thus make sure they are set up optimally. So even if two players cannot connect to each other directly, it is extremely likely that they can both connect to the relay server and send packets to each other through that.

The other big benefit of relay servers is that they can massively reduce packet count, especially in peer to peer situations. As I explained in a

[previous blogpost](http://joostdevblog.blogspot.nl/2014/09/the-importance-of-packet-count.html), packet count is an important factor in connection quality.

The internet does not allow multicasting, so if you want to send the same message to several other players, then you just need to send it several times. A relay server can work around this. Whenever a player wants to send to all other players, she sends only one packet to the relay server. The relay server then copies the packet and sends it to each client. If several players are all sending to the same player the relay server can also combine their packets into one bigger packet. These features greatly reduce packet count and bandwidth in a peer to peer situation, or for the host in a situation where a player is the host. This way relay servers theoretically make it possible to have a peer to peer game without dedicated servers.

Note that dedicated servers have these exact same benefits. Players can practically always connect to them and players only have to send packets to the dedicated server instead of to all other players. For this reason there is normally no point to having relay servers if you already have dedicated servers.

A big downside to relay servers is that sending all data through the relay server adds a little bit of latency to the connection. This is especially problematic if players from several continents are playing together in one match. You might think intercontinental play should never automatically happen, but you need thousands of simultaneous players to always avoid this. Even then international friends might send each other invites.

Let's say we have a match with four European players and two Australian players. The relay server for this match is in Europe. The connection between the Europeans will likely be a little bit slower but still fine because the relay server is close. The connection between a European player and an Australian player will also not be affected too much, because the data needs to be sent that far anyway. The problem happens between the two Australian players: since everything does through the relay server, their traffic now goes through Europe instead of directly, massively increasing their ping!

For this reason I would never want to use rigid relay servers for a game where latency matters. If players can connect directly and have a fast enough connection to handle the packet count, then it is probably faster to let them communicate directly. This also saves on the cost of running expensive relay servers. I think relay servers are mostly useful as a last resort for players who otherwise cannot connect at all, and for players whose internet is too slow for the number of players they need to send to.

[Awesomenauts](http://www.awesomenauts.com)currently does not have relay servers. Instead it solves the problem of two players not being able to connect directly by sending through one of the other players. This often works fine but it is an imperfect solution: it increases the burden on that player's connection. Also, in extremely rare cases a player cannot connect to anyone in the match.

We are currently putting a lot of effort into improving the connection quality for players in Awesomenauts. Relay servers are a feature we are considering for the future, but right now we think we can gain more by improving matchmaking first. We are writing a completely new matchmaking system that will allow us to match players better based on their connection and location. Better matchmaking also brings many other benefits that are unrelated to connection quality. A big recent improvement is that we managed to halve (!) the average bandwidth and packet count used by Awesomenauts. In the long run we will need to research relay servers further to know how beneficial their trade-of of connection quality versus latency would really be.

To summarize I would like to stress that relay servers are

*not*the same as dedicated servers. Relay servers are a tool for reducing bandwidth and packet count and for improving connection quality, potentially at the cost of latency.

*Note: I have edited this post on 27-9-2014 to remove references to the Photon network library. It turned out they had added new features that I was not aware of and that made my analysis of what Photon offers incorrect and irrelevant to this post.*

All that this game doesnt need is more laggers so if relay servers increase latency...

ReplyDeleteIt is really much more complex than that. For some players sending too many packets might increase latency, so in that case a relay server might decrease lag despite having to go through an extra computer. Relay servers might also decrease lag spikes. Very difficult to say what the effect will be exactly, that is why we would need to do more research to make a decision.

DeleteCan a dedicated server also act as a relay server?

ReplyDeleteWith the definition I use in these posts there is no point to that. What I mean when I describe a dedicated server results in clients never talking to each other any more: they ONLY talk to the dedicated server. The point of a relay server is that peer-to-peer clients still talk with each other, but send their data through the relay server instead of directly.

DeleteGood post!

ReplyDelete