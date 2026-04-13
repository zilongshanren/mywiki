---
title: WebRTC Data Channels for Great Multiplayer – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/03/webrtc-data-channels-for-great-multiplayer/
author: Ack
published: '2013-03-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

WebRTC is getting great press lately for it’s [amazing](https://hacks.mozilla.org/2013/02/hello-chrome-its-firefox-calling/) [applications](https://hacks.mozilla.org/2013/03/making-webrtc-simple-with-conversat-io/) in voice and video communication. But did you know that WebRTC also has support for peer-to-peer data? Below I’ll talk about the ‘what’ and ‘how’ of data channels, and then I’ll show you how we’re using them in [BananaBread](https://developer.mozilla.org/en-US/demos/detail/bananabread) to support peer-to-peer multiplayer.


*5-player BananaBread with WebRTC, filmed at Mozilla Toronto on a Friday afternoon.*

## Browser caveats

If you want to use WebRTC data channels, you’ll need the latest [Firefox Nightly](http://nightly.mozilla.org/) or [Chrome Canary](https://www.google.com/intl/en/chrome/browser/canary.html). BananaBread multiplayer requires binary message support for WebRTC data channels, which hasn’t landed just yet in Chrome.

## What is a data channel?

A WebRTC data channel lets you send text or binary data over an active peer connection. Data channels come in two flavors. Reliable channels will guarantee that messages you send have arrived at the other peer. If you send multiple reliable messages, they will be received in the same order. You can also send unreliable message that are not guaranteed to arrive in the order they were sent, or they may not arrive at all. These are analogous to TCP and UDP.

## Creating and using data channels

Unfortunately, setting up peer connections and creating data channels requires a non-trivial amount of work. It’s very reasonable to rely on a library to handle these things, as well as abstract away some of the implementation details between Firefox and Chrome.

The library used in the examples here is [p2p](https://github.com/js-platform/p2p). It provides a simple API for establishing peer connections and setting up streams and data channels. There’s also a broker server component and a hosted broker you can use instead of setting one up for yourself.

## Using p2p

You can start with a simple web page. Something like this will do:

```
```

In a simple configuration, one peer acts as host and listens for other peers that want to connect.

```
/* This is the address of a p2p broker server, possibly the example one at http://mdsw.ch:8080 */
var broker = "http://";
/* We'll use this to store any active connections so we can get to them later. */
var connections = {};
/* This creates an object that will handle let us listen for incoming connections. */
var peer = new Peer(broker, {video: false, audio: false});
/* This is invoked whenever a new connection is established. */
peer.onconnection = function(connection) {
connections[connection.id] = connection;
connection.ondisconnect = function() {
delete connections[connection.id];
};
connection.onmessage = function(label, msg) {
console.log(msg.data);
};
};
/* This is called when your peer has received a routing address from the broker.
The route is what lets other peers send messages through the broker that are used to
establish the peer-to-peer connection. */
peer.onroute = function(route) {
console.log(route);
}
/* This tells the broker that this peer is interested in hosting. */
peer.listen();
```

The connection object pass into `onconnection`

comes with two data channels, helpfully labelled *reliable* and *unreliable*. The label, along with the data, is passed to `onmessage`

whenever that connection receives a message.

If your peer is hosting, it’s handy to capture the routing address assigned by the broker. Another peer needs both the broker URL and the route to connect to your peer.

Finally, the connection object also exposes the local and remote streams, in case you want to send video or audio as well:

```
connection.streams['local'];
connection.streams['remote'];
```

If your peer is connecting to another peer, the code is the same as above except that instead of calling `listen`

you should:

```
/* Call this with the routing address that the host received from the broker. */
peer.connect();
```

## Sockets for Emscripten

In case you’re unfamiliar with [Emscripten](http://emscripten.org), the important thing to know is that it compiles C++ libraries and programs to JavaScript, allowing them to run in your browser. This is exactly what we used to turn [Sauerbraten](http://sauerbraten.org/) into [BananaBread](https://developer.mozilla.org/en-US/demos/detail/bananabread).

Sauerbraten has built-in multiplayer support that relies on the POSIX sockets that work very differently from WebRTC peer connections. C++ programs that use sockets expect to communicate with remote hosts by giving an IP address and a port number to the sockets API, along with a buffer containing some arbitrary data. BananaBread in particular only makes four kinds of API calls: socket, bind, recvmsg, and sendmsg.

Each time socket is called, we create a new JS object to hold an address, a port, and a message queue. The queue is important because we will need to hold onto messages that arrive from a data channel so they can be handled later by the application, which will call recvmsg. There’s also some space to build a small header that we will use for sending messages.

Since we’re using the same p2p library from above, the code to create a new Peer is identical except for the event handlers. Here’s the code for onconnection:

```
peer.onconnection = function(connection) {
var addr;
// Assign 10.0.0.1 to the host
if(route && route === connection['route']) {
addr = 0x0100000a; // 10.0.0.1
} else {
addr = Sockets.addrPool.shift();
}
connection['addr'] = addr;
Sockets.connections[addr] = connection;
connection.ondisconnect = function() {
// Don't return the host address (10.0.0.1) to the pool
if(!(route && route === Sockets.connections[addr]['route']))
Sockets.addrPool.push(addr);
delete Sockets.connections[addr];
};
connection.onmessage = function(label, message) {
var header = new Uint16Array(message, 0, 2);
if(Sockets.portmap[header[1]]) {
/* The queued message is retrived later when the program calls recvmsg. */
Sockets.portmap[header[1]].inQueue.push([addr, message]);
}
}
```

`Sockets.addrPool`

is a list of available IP addresses that we can assign to new connections. The address is used to find the right active connection when the C++ program wants to send or receive data.

```
socket: function(family, type, protocol) {
var fd = Sockets.nextFd ++;
Sockets.fds[fd] = {
addr: undefined,
port: undefined,
inQueue: [],
header: new Uint16Array(2),
};
return fd;
};
```

Bind is invoked directly when a program wants to listen on a given port, and indirectly when sendmsg is used with an unbound socket (so that recvmsg can be called on the socket and the remote host can send a reply). In the latter case we can give the socket any unused port. We don’t need to worry about the IP address here.

```
bind: function(fd, addr, addrlen) {
var info = Sockets.fds[fd];
if (!info) return -1;
if(addr) {
/* The addr argument is actually a C++ pointer, so we need to read the value from the Emscripten heap. */
info.port = _ntohs(getValue(addr + Sockets.sockaddr_in_layout.sin_port, 'i16'));
} else {
/* Finds and returns an unused port. */
info.port = _mkport();
}
/* We might need to pass the local address to C++ code so we should give it a meaningful value. */
info.addr = 0xfe00000a; // 10.0.0.254
/* This is used to find the socket associated with a port so we can deliver incoming messages. */
Sockets.portmap[info.port] = info;
};
```

For sendmsg, we need find the socket associated with the given IP address. We also need to prepend a small header onto the message buffer that contains the destination port (so the remote host can deliver the message) and the source port (so the remote host can send a reply to the message). Recvmsg is very similar to sendmsg.

(Note that the code for reading and writing data to the *msg* argument is omitted because it’s quite dense and

doesn’t add very much.)

```
sendmsg: function(fd, msg, flags) {
var info = Sockets.fds[fd];
if (!info) return -1;
/* Here's where we bind to an unused port if necessary. */
if(!info.port) {
bind(fd);
}
/* The next three lines retrieve the destination address and port from the msg argument. */
var name = {{{ makeGetValue('msg', 'Sockets.msghdr_layout.msg_name', '*') }}};
var port = _ntohs(getValue(name + Sockets.sockaddr_in_layout.sin_port, 'i16'));
var addr = getValue(name + Sockets.sockaddr_in_layout.sin_addr, 'i32');
var connection = Sockets.connections[addr];
if (!(connection && connection.connected)) {
/* Emscripten requires that all socket operations are non-blocking. */
___setErrNo(ERRNO_CODES.EWOULDBLOCK);
return -1;
}
/* Copy the message data into a buffer so we can send it over the data channel. */
var bytes = new Uint8Array();
info.header[0] = info.port; // Source port
info.header[1] = port; // Destination port
/* Create a new array buffer that's big enough to hold the message bytes and the header. */
var data = new Uint8Array(info.header.byteLength + bytes.byteLength);
/* Copy the header and the bytes into the new buffer. */
buffer.set(new Uint8Array(info.header.buffer));
buffer.set(bytes, info.header.byteLength);
connection.send('unreliable', buffer.buffer);
};
```

```
recvmsg: function(fd, msg, flags) {
var info = Sockets.fds[fd];
if (!info) return -1;
/* There's no way to deliver messages to this socket if it doesn't have a port. */
if (!info.port) {
assert(false, 'cannot receive on unbound socket');
}
/* Similar to sendmsg, if there are no messages waiting we return instead of blocking. */
if (info.inQueue.length() == 0) {
___setErrNo(ERRNO_CODES.EWOULDBLOCK);
return -1;
}
var entry = info.inQueue.shift();
var addr = entry[0];
var message = entry[1];
var header = new Uint16Array(message, 0, info.header.length);
var bytes = new Uint8Array(message, info.header.byteLength);
/* Copy the address, port and bytes into the msg argument. */
return bytes.byteLength;
};
```

## What’s next

Both the p2p library and sockets for Emscripten were made to support multiplayer BananaBread, so they’re both missing features that would be useful for building other applications. Specifically,

- Add support for peer-based brokering in the p2p library (so connected peers can broker new connections for each other)
- Add support for connection-oriented and reliable webrtc-based sockets in Emscripten

If you’re building something cool with this, or you’d like to and you have questions, feel free to ask me on [Twitter](http://twitter.com/modeswitch) or in #games on [irc.mozilla.org](https://wiki.mozilla.org/IRC).

## About
[
ack ](http://blog.modeswitch.org)

My name is Alan. I'm a computer scientist and a hacker. I work at Mozilla on various platform projects. Right now I'm focused on improving high-performance real-time applications (games!) on the web. Most things I do revolve around open source for software, hardware, and design.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 5 comments

SebastiánMarch 31st, 2013 at 11:48ackApril 2nd, 2013 at 12:55MarkApril 7th, 2013 at 09:06MarkApril 7th, 2013 at 10:50ackApril 8th, 2013 at 16:14