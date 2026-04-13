---
title: 'Dweb: Decentralised, Real-Time, Interoperable Communication with Matrix –
  Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2018/10/dweb-decentralised-real-time-interoperable-communication-with-matrix/
author: Ben Parsons
published: '2018-10-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*In the Dweb series, we are covering projects that explore what is possible when the web becomes decentralized or distributed. These projects aren’t affiliated with Mozilla, and some of them rewrite the rules of how we think about a web browser. What they have in common: These projects are open source and open for participation, and they share Mozilla’s mission to keep the web open and accessible for all.*

*While Scuttlebutt is person-centric and IPFS is document-centric, today you’ll learn about Matrix, which is all about messages. Instead of inventing a whole new stack, they’ve leaned on some familiar parts of the web today – HTTP as a transport, and JSON for the message format. How those messages get around is what distinguishes it – a system of decentralized servers, designed with interoperability in mind from the beginning, and an extensibility model for adapting to different use-cases. Please enjoy this introduction from Ben Parsons, developer advocate for Matrix.org.*

*– Dietrich Ayala*

## What is Matrix?

Matrix is an open standard for *interoperable*, *decentralised*, *real-time* communication over the Internet. It provides a standard HTTP API for publishing and subscribing to real-time data in specified channels, which means it can be used to power Instant Messaging, VoIP/WebRTC signalling, Internet of Things communication, and anything else that can be expressed as JSON and needs to be transmitted in real-time over HTTP. The most common use of Matrix today is as an Instant Messaging platform.

- Matrix is
*interoperable*in that it follows an[open standard](https://matrix.org/docs/spec)and can freely communicate with other platforms. Matrix messages are JSON, and easy to parse. Bridges are provided to enable communication with other platforms. - Matrix is
*decentralised*– there is no central server. To communicate on Matrix, you connect your client to a single “homeserver” – this server then communicates with other homeservers. For every room you are in, your homeserver will maintain a copy of the history of that room.**This means that no one homeserver is the host or owner of a room if there is more than one homeserver connected to it.**Anyone is free to host their own homeserver, just as they would host their own website or email server.

## Why create another messaging platform?

The initial goal is to fix the problem of fragmented IP communications: letting users message and call each other without having to care what app the other user is on – making it as easy as sending an email.

In future, we want to see Matrix used as a generic HTTP messaging and data synchronization system for the whole web, enabling IoT and other applications through a single unified, understandable interface.

## What does Matrix provide?

Matrix is an [Open Standard](https://matrix.org/docs/spec), with a specification that describes the interaction of homeservers, clients and Application Services that can extend Matrix.

There are reference implementations of clients, servers and SDKs for various programming languages.

## Architecture

You connect to Matrix via a client. Your client connects to a single server – this is your *homeserver*. Your homeserver stores and provides history and account information for the connected user, and room history for rooms that user is a member of. To sign up, you can find a list of public homeservers at [hello-matrix.net](https://www.hello-matrix.net/public_servers.php), or if using [Riot](https://matrix.org/docs/projects/client/riot.html) as your client, the client will suggest a default location.

Homeservers synchronize message history with other homeservers. In this way, your homeserver is responsible for storing the state of rooms and providing message history.

Let’s take a look at an example of how this works. Homeservers and clients are connected as in the diagram in figure 1.

*Figure 1.* Homeservers with clients

![Figure 1. Homeservers with clients](../../assets/b561b2e6b6dd98bf.png)


If we join a homeserver (Figure 3), that means we are connecting our client to an account on that homeserver.

Now we send a message. This message is sent into a room specified by our client, and given an event id by the homeserver.

Our homeserver sends the message event to every homeserver which has a user account belonging to it in the room. It also sends the event to every local client in the room. (Figure 5.)

Finally, the remote homeservers send the message event to their clients, which in are the appropriate room.

## Usage Example – simple chatbot

Let’s use the [matrix-js-sdk](https://github.com/matrix-org/matrix-js-sdk) to create a small chatbot, which listens in a room and responds back with an echo.

Make a new directory, install matrix-js-sdk and let’s get started:

```
mkdir my-bot
cd my-bot
npm install matrix-js-sdk
touch index.js
```


Now open `index.js`

in your editor. We first create a `client`

instance, this connects our client to our homeserver:

```
var sdk = require('matrix-js-sdk');
const client = sdk.createClient({
baseUrl: "https://matrix.org",
accessToken: "....MDAxM2lkZW50aWZpZXIga2V5CjAwMTBjaWQgZ2Vu....",
userId: "@USERID:matrix.org"
});
```


The `baseUrl`

parameter should match the homeserver of the user attempting to connect.

Access tokens are associated with an account, and provide full read/write access to all rooms available to that user. You can obtain an access token using Riot, by going to the settings page.

It’s also possible to get a token programmatically if the server supports it. To do this, create a new client with no authentication parameters, then call `client.login()`

with `"m.login.password"`

:

```
const passwordClient = sdk.createClient("https://matrix.org");
passwordClient.login("m.login.password", {"user": "@USERID:matrix.org", "password": "hunter2"}).then((response) => {
console.log(response.access_token);
});
```


With this access_token, you can now create a new client as in the previous code snippet. It’s recommended that you save the access_token for re-use.

Next we start the client, and perform a first sync, to get the latest state from the homeserver:

```
client.startClient({});
client.once('sync', function(state, prevState, res) {
console.log(state); // state will be 'PREPARED' when the client is ready to use
});
```


We listen to events from the rooms we are subscribed to:

```
client.on("Room.timeline", function(event, room, toStartOfTimeline) {
handleEvent(event);
});
```


Finally, we respond to the events by echoing back messages starting “!”

```
function handleEvent(event) {
// we know we only want to respond to messages
if (event.getType() !== "m.room.message") {
return;
}
// we are only interested in messages which start with "!"
if (event.getContent().body[0] === '!') {
// create an object with everything after the "!"
var content = {
"body": event.getContent().body.substring(1),
"msgtype": "m.notice"
};
// send the message back to the room it came from
client.sendEvent(event.getRoomId(), "m.room.message", content, "", (err, res) => {
console.log(err);
});
}
}
```


## Learn More

The best place to come and find out more about Matrix is on Matrix itself! The absolute quickest way to participate in Matrix is to use Riot, a popular web-based client. Head to <[https://riot.im/app](https://riot.im/app)>, sign up for an account and join the [ #matrix:matrix.org](https://matrix.to/#/#matrix:matrix.org) room to introduce yourself.

[matrix.org](https://matrix.org) has many resources, including the [FAQ](https://matrix.org/docs/guides/faq) and [Guides](https://matrix.org/docs/guides/) sections.

Finally, to get stuck straight into the code, take a look at the [Matrix Spec](https://matrix.org/docs/spec/), or get involved with the many [Open-Source projects](https://github.com/matrix-org).

## About Ben Parsons

Ben works as a Developer Advocate for matrix.org.

## 9 comments

PlutoOctober 17th, 2018 at 16:02Ben ParsonsOctober 19th, 2018 at 02:15amitOctober 18th, 2018 at 10:39Ben ParsonsOctober 18th, 2018 at 12:12frustigorOctober 18th, 2018 at 19:29Ben ParsonsOctober 19th, 2018 at 02:12geek42October 18th, 2018 at 19:49Ben ParsonsOctober 19th, 2018 at 02:18Ranjith RajOctober 19th, 2018 at 20:33