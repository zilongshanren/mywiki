---
title: Peering Through the WebRTC Fog with SocketPeer – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/04/peering-through-the-webrtc-fog-with-socketpeer/
author: Sergi Mansilla
published: '2015-04-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

WebRTC allows browsers to do things they never could before, but a soup of unfamiliar terminology and the complexity of the API makes for a steep learning curve. After spending several weeks neck-deep in example code and cargo-culting several libraries, I have emerged with a workable understanding and a nifty library that helps hide some of the complexity of WebRTC for its simplest use case of two way peer-to-peer communication.

But before I start talking about the [library](https://hacks.mozilla.org#using-socketpeer), it helps to understand a bit of what it abstracts away.

## Alice and Bob (and ICE and NAT and STUN and SDP)

When two devices want to speak to each other, we need a way for them to exchange contact information such as their IP addresses. In the same way DNS servers help browsers locate remote machines, we can set up a mutually known server to help potential peers locate each other. In WebRTC this is known as a *signalling server*.

In our simple case, each peer contacts the signalling server. The server provides the peers with each other’s addresses, and then the peers can begin exchanging data.

### The plot thickens

Today’s Internet doesn’t quite work that way. Most computers online don’t have unique IP addresses; they share a public address with all the other devices on their local network. Most local networks also have firewalls that protect machines from unwanted inbound traffic. Swapping IP addresses isn’t enough.

### ICE the wound

The telecommunications industry has been dealing with this problem for a while now[*](https://hacks.mozilla.org#footnote-1). There are a number of different ways a connection can pass back through a firewall and router to an internal network. [ICE](http://tools.ietf.org/html/rfc5245#section-2) is a kitchen-sink protocol that uses the tried-and-true technique “Try Everything and See What Works™.” A server, called a STUN server, uses the ICE protocol to find out and inform a peer of all the possible ways it can be reached from the public Internet. These potential connection methods are called *ICE candidates*.

When a machine receives a candidate, it needs to communicate that to its peer. Here the signalling server comes to the rescue again — relaying each peer’s candidates to the other.

### Call and response

When a device wants to establish a connection, it generates a message called an *offer* and sends it to a peer using the signalling server. The offer, encoded in the [SDP](http://en.wikipedia.org/wiki/Session_Description_Protocol) format, consists of information about the device — such as which protocols it knows how to speak and which communication methods it has. When the remote peer receives the offer, it responds with its own SDP message called an *answer*. Then, the two potential peers send each other possible ICE candidates. Once the peers find a connection method that works for both of them, the connection is established!

### Let’s take it from the top

Let’s review the connection process, incorporating all the techniques from above:

- A device uses a signalling server to relay an SDP offer to a potential peer. In the meantime, it asks an ICE server to find out how it can be reached from the public Internet.
- The potential peer replies with its own connection offer, and also gathers ICE candidates.
- The peers use the signalling server to exchange ICE candidates, attempting to use them to open a connection.
- Once each peer finds a working candidate, the connection is established.

### Let’s give them something to talk a~~bout~~ with

Once a [PeerConnection](https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection) is established, it can be used to carry audio and video [MediaStreams](https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_API) as well as a more general [DataChannel](https://developer.mozilla.org/en-US/docs/Web/API/RTCDataChannel). People are excited about browser-to-browser video conferencing (with good reason!), but WebRTC isn’t just about voice and video. `RTCDataChannel`

provides a general data pipeline that works similarly to a WebSocket. It’s immensely powerful and useful, but under-promoted.

### Boilerplate the ocean

WebRTC is a low level, nuts-and-bolts API. It’s made of multiple small, composable APIs that offer a large amount of flexibility and [extensibility](https://extensiblewebmanifesto.org/). The downside of this is that accomplishing even a basic task can require significant boilerplate code. The notion is that JS libraries and frameworks will step in to abstract away this complexity, and indeed, there are a large number of [WebRTC libraries](https://www.npmjs.com/search?q=webrtc) out there already.

Many of these libraries fall short due to a lack of signalling server and fallback support for browsers with no WebRTC support. To address this, [Chris Van](https://twitter.com/cvanw) and I built [SocketPeer](https://github.com/cvan/socketpeer).

## Using SocketPeer

[SocketPeer](https://github.com/cvan/socketpeer) is, as its name suggests, a combination of WebSockets and `RTCPeerConnection`

. This **node.js** library abstracts away the common pattern of using WebSockets as a signalling server to instantiate a DataChannel over WebRTC. The WebSocket server will also serve as a fallback message relay if the peers cannot establish a peer-to-peer connection.

### Server code

```
// In your server module alongside existing application code.
var SocketPeer = require('socketpeer');
new SocketPeer();
```

`I’ll admit that’s a bit facile, but SocketPeer is designed to simplify the process of running a signalling server — at its simplest, it does everything for you. The server is fairly configurable, but by default it takes care of itself, by:`


- Creating an
`http.Server`

if one is not supplied. - Attaching logic to serve the client-side
`socketpeer.js`

library. - Starting a
[WebSocket](https://github.com/websockets/ws)server if one is not supplied. - Starting to listen on a default port.

If all you need is a basic signalling server, then this is all the code you need. But let’s say you want to integrate SocketPeer with an existing [Express](http://expressjs.com/) app:


```
// `app` is an existing Express Application
var server = http.createServer(app);
new SocketPeer({
httpServer: server
});
server.listen(/* port */);
```

### Client code

As described above, when SocketPeer is running on a server it will serve the client library at a known URL. By default, this can be found at `/socketpeer/socketpeer.js`

. The client library exposes an event interface and a series of [events](https://github.com/cvan/socketpeer#events) to keep you informed of the state of the connection. The three most important events are:

`connect`

– Fires when peers are paired. Data can be exchanged using WebSockets at this point.`upgrade`

– Fires when an RTCPeerConnection is established. Data can now be exchanged peer-to-peer.`data`

– Fires when data arrives from the remote peer.

The last important piece of information is called `pairCode`

. This is an arbitrary string used by the two ends of a peer-to-peer connection to identify each other. It can be any mutually agreed-upon value.


```
var peer = new SocketPeer({
pairCode: 'foobar'
});
peer.on('connect', function () {
// connected via WebSockets
peer.send('Hello via WebSockets.');
});
peer.on('upgrade', function () {
// now using RTCPeerConnection
peer.send('Hello via WebRTC!');
});
peer.on('data', function (data) {
// do something awesome
});
```

## Chat is the new todo

What’s sample code without a working demo? I built a super simple example of peer-to-peer chat using SocketPeer. [Try it out](http://socketpeer-test.herokuapp.com/), and [check out the code on GitHub](https://github.com/potch/test-socketpeer) to see how it works.

![Depiction of the SocketPeer demo chat app.](../../assets/769b85d1b86cd29c.gif)


The library is still a work in progress, but all the core functionality is in place and tested. Please try it out and let us know of any [issues or feedback](https://github.com/cvan/socketpeer/issues/new) on the API.

* The author of this post is not a telecommunications engineer. He read a lot of Wikipedia and skimmed a few RFCs so you don’t have to.

## 2 comments

Kenneth HauglandApril 14th, 2015 at 05:49Jesse OlssonApril 16th, 2015 at 20:43