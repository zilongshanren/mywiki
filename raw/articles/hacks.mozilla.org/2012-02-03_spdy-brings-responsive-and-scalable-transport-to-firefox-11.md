---
title: SPDY Brings Responsive and Scalable Transport to Firefox 11 – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2012/02/spdy-brings-responsive-and-scalable-transport-to-firefox-11/
author: Patrick McManus
published: '2012-02-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 11 contains the first Firefox implementation of the SPDY protocol. SPDY is a secure web transport protocol that encapsulates HTTP/1 while replacing its aging connection management strategies. This results in more responsive page loads today and enables better scalability with the real time web of tomorrow.

The most important goal of SPDY is to transport web content using fewer TCP connections. It does this by multiplexing large numbers of transactions onto one TLS connection. This has much better latency properties than native HTTP/1. When using SPDY a web request practically never has to wait in the browser due to connection limits being exhausted (e.g. the limit of 6 parallel HTTP/1 connections to the same host name). The request is simply multiplexed onto an existing connection.

Many web pages are full of small icons and script references. The speed of those transfers is limited by network delay instead of bandwidth. SPDY ramps up the parallelism which in turn removes the serialized delays experienced by HTTP/1 and the end result is faster page load time. By using fewer connections, SPDY also saves the time and CPU needed to establish those connections.

The page-load waterfall diagram below tells the story well. Note the large number of object requests that all hit the network at the same time. All of their individual load times are comprised exclusively of network delay and by executing them in parallel the total page load time is reduced to a single round trip.

![Waterfall](../../assets/b7a505861825129d.png)


Generally speaking, web pages on high latency connections with high numbers of embedded objects will see the biggest benefit from SPDY. That’s great because its where the web should be going. High latency mobile is a bigger part of the Internet every day, and as the Internet spreads to parts of the world where it isn’t yet common you can count on the fact that the growth will be mobile driven. Designs with large numbers of objects are also proving to be a very popular paradigm. Facebook, G+, Twitter and any avatar driven forum are clear examples of this. Rather than relying on optimization hacks such as sprites and data urls that are hard to develop and harder to maintain we can let the transport protocol do its job better.

Beyond better page load time, there is good reason to think this approach is good for the web’s foundation. The way HTTP/1 uses large numbers of small and parallel active connections creates a giant networking congestion problem. This inhibits the deployment of real time applications like WebRTC, VOIP, and some highly interactive games. SPDY’s small number of busier connections fits the congestion control model of the Internet much better and enables the transport of classic web content to cooperate better with these real time applications. Web browsers have only managed to keep the congestion problem in check with HTTP/1 through arbitrary limits on its parallelism. With SPDY we can have our parallel-cake and eat it in low latency conditions too. This property is what I find most promising about SPDY, and [I’ve written about it extensively in the past](http://bitsup.blogspot.com/2011/12/spdy-bufferbloat-http-and-real-time.html).

There is a great transition path onto SPDY. It is a new protocol, but it uses the old https:// protocol scheme in URIs. No changes to markup are needed to use SPDY. Generally SPDY servers support both SPDYand HTTP/1 for use with browsers that are not SPDY capable. The protocol used is silently negotiated through a TLS extension called Next Protocol Negotiation. The great news here is that upgrading to SPDY is just a matter of an administrative server upgrade. No changes to content are needed and things like REST APIs continue to work unmodified. Indeed, a SPDY site is not visually different in any way from an HTTP/1 site.

Google did a lot of work to launch this technology and to evolve it in the open, but it isn’t a Google only project any more. Since the implementations in Chrome and various Google web services were introduced we have seen either code or commitments regarding SPDY from many other products and groups including Amazon’s tablet, node.js, an Apache module, curl, nginx, and even a couple CDNs along with Mozilla. In my opinion, that kind of reaction is because engineers have looked at this and decided that it is solves several serious problems with HTTP’s connection handling and that this is a technology well positioned for us all to cooperate on. There is also discussion and preliminary movement in all the right standardization forums such as the W3C TAG and the IETF. Open standardization of the protocol is a key condition of Mozilla’s interest in it, but it is not a precondition to using it. Gathering operational experience instead of just engineering on whiteboards, is a valuable part of how the best protocols are made. The details of SPDY can be iterated based on that experience and the standardization process. The protocol is well suited to that evolution at this stage.

SPDY needs to be explicitly enabled through about:config in Firefox 11. Go to that URL and search for network.http.spdy.enabled and set it to true. Future revisions hope to have it enabled by default.

## About Patrick McManus

Principal Engineer at Mozilla focused on Platform Networking

## 37 comments

Pikadude No. 1February 3rd, 2012 at 19:13nototoadFebruary 3rd, 2012 at 22:42DanFebruary 3rd, 2012 at 19:48Patrick McManusFebruary 4th, 2012 at 08:30AdamFebruary 3rd, 2012 at 21:48Techy MikeFebruary 4th, 2012 at 02:00Patrick McManusFebruary 4th, 2012 at 08:27driaxFebruary 3rd, 2012 at 22:52MookFebruary 4th, 2012 at 00:07Patrick McManusFebruary 4th, 2012 at 08:24cuz84dFebruary 4th, 2012 at 01:11Jo HermansFebruary 4th, 2012 at 14:01Jo HermansFebruary 5th, 2012 at 10:54Dmitry PashkevichFebruary 5th, 2012 at 05:09louisremiFebruary 5th, 2012 at 10:18RyanVMFebruary 5th, 2012 at 17:32Matt WilcoxFebruary 6th, 2012 at 09:38AnunturiFebruary 7th, 2012 at 23:38MajorFebruary 9th, 2012 at 02:57Patrick McManusFebruary 9th, 2012 at 06:40Pikadude No. 1February 9th, 2012 at 17:05Gautam DewanFebruary 13th, 2012 at 21:45Patrick McManusFebruary 14th, 2012 at 07:05Gautam DewanFebruary 16th, 2012 at 20:50GrammarNaziFebruary 28th, 2012 at 21:09Robert Nyman [Mozilla]February 29th, 2012 at 00:17Christian EatonMarch 5th, 2012 at 06:48fracjackmacMarch 11th, 2012 at 10:56Bill FuJune 6th, 2012 at 00:56Patrick McManusJune 6th, 2012 at 05:57Bill FuJune 27th, 2012 at 19:38Patrick McManusJune 27th, 2012 at 20:20Bill FuJune 27th, 2012 at 22:02SriramJuly 18th, 2012 at 08:05Kevin L.August 4th, 2012 at 18:26John HosfieldSeptember 7th, 2012 at 16:23John HosfieldSeptember 7th, 2012 at 16:25