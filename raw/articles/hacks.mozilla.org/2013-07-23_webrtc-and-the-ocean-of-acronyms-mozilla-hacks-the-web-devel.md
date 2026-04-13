---
title: WebRTC and the Ocean of Acronyms – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/07/webrtc-and-the-ocean-of-acronyms/
author: Louis Stowasser
published: '2013-07-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

My experience getting started with WebRTC can be summarised in a three letter acronym so I decided to write this article dedicated to answering my many questions. I’ve always said, if you don’t know an acronym, it’s probably a networking protocol.

## What is ICE?

[Interactive Connectivity Establishment (ICE)](http://en.wikipedia.org/wiki/Interactive_Connectivity_Establishment) is a framework to allow your web browser to connect with peers. There are many reasons why a straight up connection from Peer A to Peer B simply won’t work. It needs to bypass firewalls that would prevent opening connections, give you a unique address if like most situations your device doesn’t have a public IP address, and relay data through a server if your router doesn’t allow you to directly connect with peers. ICE uses some of the following techniques described below to achieve this:

## What is STUN?

[Session Traversal Utilities for NAT (STUN)](http://en.wikipedia.org/wiki/STUN) (acronym within an acronym) is a protocol to discover your public address and determine any restrictions in your router that would prevent a direct connection with a peer.

The client will send a request to a STUN server on the internet who will reply with the client’s public address and whether or not the client is accessible behind the router’s NAT.

![](../../assets/2ccc0718890990cd.png)


## What is NAT?

[Network Address Translation (NAT)](http://en.wikipedia.org/wiki/NAT) is used to give your device a public IP address. A router will have a public IP address and every device connected to the router will have a private IP address. Requests will be translated from the device’s private IP to the router’s public IP with a unique port. That way you don’t need a unique public IP for each device but can still be discovered on the internet.

Some routers will have restrictions on who can connect to devices on the network. This can mean that even though we have the public IP address found by the STUN server, not anyone can create a connection. In this situation we need to turn to TURN.

## What is TURN?

Some routers using NAT employ a restriction called ‘Symmetric NAT’. This means the router will only accept connections from peers you’ve previously connected to.

[Traversal Using Relays around NAT (TURN)](http://en.wikipedia.org/wiki/TURN) is meant to bypass the Symmetric NAT restriction by opening a connection with a TURN server and relaying all information through that server. You would create a connection with a TURN server and tell all peers to send packets to the server which will then be forwarded to you. This obviously comes with some overhead so is only used if there are no other alternatives.

![](../../assets/eb5e2ac9d82c04d9.png)


## What is SDP?

[Session Description Protocol (SDP)](http://en.wikipedia.org/wiki/Session_Description_Protocol) is a standard for describing the multimedia content of the connection such as resolution, formats, codecs, encryption, etc so that both peers can understand each other once the data is transferring. This is not the media itself but more the metadata.

## What is an Offer/Answer and Signal Channel?

Unfortunately WebRTC can’t create connections without some sort of server in the middle. We call this the Signal Channel. It’s any sort of channel of communication to exchange information before setting up a connection, whether by email, post card or a carrier pigeon… it’s up to you.

The information we need to exchange is the Offer and Answer which just contains the SDP mentioned above.

Peer A who will be the initiator of the connection, will create an Offer. They will then send this offer to Peer B using the chosen signal channel. Peer B will receive the Offer from the signal channel and create an Answer. They will then send this back to Peer A along the signal channel.

## What is an ICE candidate?

As well as exchanging information about the media (discussed above in Offer/Answer and SDP), peers must exchange information about the network connection. This is know as an ICE candidate and details the available methods the peer is able to communicate (directly or through a TURN server).

## The entire exchange in a complicated diagram

## About
[
Louis Stowasser ](http://louisstowasser.com)

I am a Partner Engineer for Mozilla, maintainer of [Gamedev Weekly](http://gamedevweekly.com) and creator of the [CraftyJS](http://craftyjs.com) game engine, based in Brisbane Australia.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 6 comments

Chris AllenJuly 23rd, 2013 at 13:19Fabrizzio RiveraJuly 24th, 2013 at 12:13Robert ReeseAugust 10th, 2013 at 03:10LuisJuly 24th, 2013 at 18:19Website Developer BrisbaneJuly 25th, 2013 at 03:30StephanJuly 26th, 2013 at 21:22