---
title: 'Introducing HumbleNet: a cross-platform networking library that works in the
  browser – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2017/06/introducing-humblenet-a-cross-platform-networking-library-that-works-in-the-browser/
author: Edward Rudd
published: '2017-06-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[HumbleNet](https://humblenet.github.io/) started out as a project at [Humble Bundle](https://www.humblebundle.com/) in 2015 to support an initiative to port peer-to-peer multiplayer games at first to [asm.js](http://asmjs.org/) and now to [WebAssembly](http://webassembly.org/). In 2016, Mozilla’s web games program identified the need to enable [UDP (User Datagram Protocol)](https://en.wikipedia.org/wiki/User_Datagram_Protocol) networking support for web games, and asked if they could work with Humble Bundle to release the project as open source. Humble Bundle graciously agreed, and Mozilla worked with [OutOfOrder.cc](http://www.outoforder.cc/) to polish and document HumbleNet. Today we are releasing the 1.0 version of this library to the world!

## Why another networking library?

When the idea of HumbleNet first emerged we knew we could use [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) to enable multiplayer gaming on the web. This approach would require us to either replace the entire protocol with WebSockets (the approach taken by the asm.js port of [Quake 3](http://www.quakejs.com/)), or to tunnel UDP traffic through a WebSocket connection to talk to a UDP-based server at a central location.

In order to work, both approaches require a middleman to handle all network traffic between all clients. WebSockets is good for games that require a reliable ordered communication channel, but real-time games require a lower latency solution. And most real-time games care more about receiving the most recent data than getting ALL of the data in order. WebRTC’s UDP-based data channel fills this need perfectly. HumbleNet provides an easy-to-use API wrapper around WebRTC that enables real-time UDP connections between clients using the WebRTC data channel.

## What exactly is HumbleNet?

HumbleNet is a simple C API that wraps [WebRTC](https://webrtc.org/) and WebSockets and hides away all the platform differences between browser and non-browser platforms. The current version of the library exposes a simple peer-to-peer API that allows for basic peer discovery and the ability to easily send data (via WebRTC) to other peers. In this manner, you can build a game that runs on Linux, macOS, and Windows, while using any web browser — and they can all communicate in real-time via WebRTC. This means no central server (except for peer discovery) is needed to handle network traffic for the game. The peers can talk directly to each other.

HumbleNet itself uses a single WebSocket connection to manage peer discovery. This connection only handles requests such as “let me authenticate with you”, and “what is the peer ID for a server named “bobs-game-server”, and “connect me to peer #2345”. After the peer connection is established, the games communicate directly over WebRTC.

## HumbleNet demos

We have integrated HumbleNet into asm.js ports of [Quake 2](https://github.com/HumbleNet/quake2) and [Quake 3](https://github.com/HumbleNet/quake3) and we provide a [simple Unity3D demo](https://github.com/HumbleNet/WebGLRoller) as well.

Here is a simple video of me playing Quake 3 against myself. One game running in Firefox 54 (general release), the other in Firefox Developer Edition.

## Getting started

You can find pre-built redistributables at [https://humblenet.github.io/](https://humblenet.github.io/). These include binaries for Linux, macOS, Windows, a C# wrapper, Unity3D plugin, and [emscripten](https://github.com/kripken/emscripten) (for targeting asm.js or WebAssembly).

### Starting your peer server

Read the documentation about the peer server on the website. In general, for local development, simply starting the peer server is good enough. By default it will run in non-SSL mode on port 8080.

### Using the HumbleNet API

#### Initializing the library

To initialize HumbleNet just call `humblenet_init()`

and then later `humblnet_p2p_init()`

. The second call will initiate the connection to the peer server with the specified credentials.

```
humblenet_init();
// this initializes the P2P portion of the library connecting to the given peer server with the game token/secret (used by the peer server to validate the client).
// the 4th parameter is for future use to authenticate the user with the peer server
humblenet_p2p_init("ws://localhost:8080/ws", "game token", "game secret", NULL);
```


#### Getting your local peer id

Before you can send any data to other peers, you need to know what your own peer ID is. This can be done by periodically polling the `humblenet_p2p_get_my_peer_id()`

function.

```
// initialization loop (getting a peer)
static PeerId myPeer = 0;
while (myPeer == 0) {
// allow the polling to run
humblenet_p2p_wait(50);
// fetch a peer
myPeer = humblenet_p2p_get_my_peer_id();
}
```


#### Sending data

To send data, we call `humblenet_p2p_sendto`

. The 3rd parameter is the send mode type. Currently HumbleNet implements 2 modes:SEND_RELIABLE and SEND_RELIABLE_BUFFERED. The buffered version will attempt to do local buffering of several small messages and send one larger message to the other peer. They will be broken apart on the other end transparently.

```
void send_message(PeerId peer, MessageType type, const char* text, int size)
{
if (size > 255) {
return;
}
uint8_t buff[MAX_MESSAGE_SIZE];
buff[0] = (uint8_t)type;
buff[1] = (uint8_t)size;
if (size > 0) {
memcpy(buff + 2, text, size);
}
humblenet_p2p_sendto(buff, size + 2, peer, SEND_RELIABLE, CHANNEL);
}
```


#### Initial connections to peers

When initially connecting to a peer for the first time you will have to send an initial message several times while the connection is established. The basic approach here is to send a hello message once a second, and wait for an acknowledge response before assuming the peer is connected. Thus, minimally, any application will need 3 message types: HELLO, ACK, and some kind of DATA message type.

```
if (newPeer.status == PeerStatus::CONNECTING) {
time_t now = time(NULL);
if (now > newPeer.lastHello) {
// try once a second
send_message(newPeer.id, MessageType::HELLO, "", 0);
startPeerLastHello = now;
}
}
```


#### Retrieving data

To actually retrieve data that has been sent to your peer you need to use `humblenet_p2p_peek`

and `humblenet_p2p_recvfrom`

. If you assume that all packages are smaller than a max size, then a simple loop like this can be done to process any pending messages. Note: Messages larger than your buffer size will be truncated. Using `humblenet_p2p_peek`

you can see the size of the next message for the specified channel.

```
uint8_t buff[MAX_MESSAGE_SIZE];
bool done = false;
while (!done) {
PeerId remotePeer = 0;
int ret = humblenet_p2p_recvfrom(buff, sizeof(buff), &remotePeer, CHANNEL);
if (ret < 0) {
if (remotePeer != 0) {
// disconnected client
} else {
// error
done = true;
}
} else if (ret > 0) {
// we received data process it
process_message(remotePeer, buff, sizeof(buff), ret);
} else {
// 0 return value means no more data to read
done = true;
}
}
```


#### Shutting down the library

To disconnect from the peer server, other clients, and shut down the library, simply call `humblenet_shutdown`

.

```
humblenet_shutdown();
```


#### Finding other peers

HumbleNet currently provides a simple “DNS” like method of locating other peers. To use this you simply register a name with a client, and then create a virtual peer on the other clients. Take the client-server style approach of Quake3 for example – and have your server register its name as “awesome42.”

```
humblenet_p2p_register_alias("awesome42");
```


Then, on your other peers, create a virtual peer for awesome42.

```
PeerID serverPeer = humblenet_p2p_virtual_peer_for_alias("awesome42");
```


Now the client can send data to serverPeer and HumbleNet will take care of translating the virtual peer to the actual peer once it resolves the name.

We have two systems on the roadmap that will improve the peer discovery system. One is an event system that allows you to request a peer to be resolved, and then notifies you when it’s resolved. The second is a proper lobby system that allows you to create, search, and join lobbies as a more generic means of finding open games without needing to know any name up front.

## Development Roadmap

We have a roadmap of what we plan on adding now that the project is released. Keep an eye on the [HumbleNet site](https://humblenet.github.io/) for the latest development.

Future work items include:

- Event API
- Allows a simple SDL2-style polling event system so that game code can easily check for various events from the peer server in a cleaner way, such as connects, disconnects, etc.

- Lobby API
- Uses the Event API to build a means of creating lobbies on the peer server in order to locate game sessions (instead of having to register aliases).

- WebSocket API
- Adds in support to easily connect to any websocket server with a clean simple API.


## How can I contribute?

If you want to help out and contribute to the project, HumbleNet is being developed on GitHub: [https://github.com/HumbleNet/humblenet/](https://github.com/HumbleNet/humblenet/). Use the issue tracker and pull requests to contribute code. Be sure to read the [CONTRIBUTING.md](https://github.com/HumbleNet/humblenet/blob/master/CONTRIBUTING.md) guide on how to create a pull request.

## About
[
Edward Rudd ](http://www.outoforder.cc/)

## About Andre Vrignaud

Andre Vrignaud is the Head of Platform Strategy for Mozilla’s Mixed Reality Program, where he guides the strategy for Mozilla's efforts to enable an open, sustainable 3D web and ecosystem. With a side of net neutrality and privacy advocacy.