---
title: Making WebRTC Simple with conversat.io – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/03/making-webrtc-simple-with-conversat-io/
author: Henrik Joreteg
published: '2013-03-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

WebRTC is awesome, but it’s a bit unapproachable. Last week, my colleagues and I at [&yet](http://andyet.com) released a couple of tools we hope will help make it more tinkerable and pose a real risk of actually being useful.

As a demo of these tools, we very quickly built a simple product called [conversat.io](http://conversat.io) that lets you create free, multi-user video calls with no account and no plugins, just by going to a url in a modern browser. Anyone who visits that same URL joins the call.

The purpose of [conversat.io](http://conversat.io) is two fold. First, it’s a useful communication tool. Our team uses [And Bang](http://next.andbang.com) for tasks and group chat, so being able to drop a link to a video conversation “room” into our team chat that people can join is super useful. Second, it’s a demo of the [SimpleWebRTC.js library](http://simplewebrtc.com) and the little [signaling server](https://github.com/andyet/signalmaster) that runs it, signalmaster.

(Both [SimpleWebRTC](https://github.com/HenrikJoreteg/SimpleWebRTC) and [signalmaster](https://github.com/andyet/signalmaster) are open sourced on Github and MIT licensed. Help us make them better!)

## Quick note on browser support

WebRTC currently only works in Chrome stable and FireFox Nightlies (with the `media.peerconnection.enabled`

preference enabled in about:config).

Hopefully we’ll see much broader browser support soon. I’m particularly excited about having WebRTC available on smartphones and tablets.

## Approachability and adoption

I firmly believe that widespread adoption of new web technologies is directly corellated to how easy they are to play with. When I was a new JS developer, it was jQuery’s approachability that made me feel empowered to build cool stuff.

My falling in love with javascript all started with doing this with jQuery:

```
$('#demo').slideDown();
```

And then seeing the element move on my screen. I knew nothing. But as cheesy as it sounds, this simple thing left me feeling empowered to build more interesting things.

[Socket.io](http://socket.io/) did the same thing for people wanting to build apps that pushed data from the server to the client:

```
// server:
client.emit("something", {
some: "data"
});
```

```
// client:
socket = io.connect();
socket.on("something", function (data) {
// here's my data!
console.log(data);
});
```

Rather than having to figure out how to set up long-polling, BOSH, and XMPP in order to get data pushed out to the browser, I could now just send messages to the browser. In fact, if I didn’t want to, I didn’t even have to think about serializing and de-serializing. I could now just pass simple javascript objects seamlessly back and forth between the client and server.

I’ve heard some “hardcore” devs complain that tools like this lead to too many poorly made tools and too many “wannabe” developers who don’t know what they’re doing. That’s garbage.

Approachable tools that make developers feel empowered to build cool stuff is the reason the web is as successful and vibrant as it is.

Tools like this are the gateway drug for getting us hooked on building things on these types of technologies. They introduce the concept and help us think about what could be built. Whether or not we ultimately end up building the final app with the tool whose simplicity introduced it to us is irrelevant.

## The potential of WebRTC

I’m convinced WebRTC has the potential to have a *huge* impact on how we communicate. It already has for our team at &yet. Sure, we already used stuff like Skype, Facetime, and Google Hangouts. But the simplicity and convenience of just opening a URL in a browser and instantly being in a conversation is powerful.

Once this technology is broadly available and on mobile devices, it’s nothing short of a game changer for communications.

## Challenges

There are definitely quite a few hurdles that get in the way of just playing with WebRTC: complexity and browser differences in instantiating peer connections, generating and processing signaling messages, and attaching media streams to video elements.

Even at the point you have those things, you still need a way to let two users find each other and have a mechanism for each user to send the proper signaling messages directly to the other user or users that they want to connect to.

SimpleWebRTC.js is our answer to the clientside complexities. It abstracts away API differences between Firefox and Chrome.

## Using SimpleWebRTC

At its simplest, you just need to include the SimpleWebRTC.js script, provide a container for your local video, a container for the remote video(s) like this:

```
```

Then in you just init a `webrtc`

object and tell it which containers to use:

```
var webrtc = new WebRTC({
// the id of (or actual element) to hold "our" video
localVideoEl: 'localVideo',
// the id of or actual element that will hold remote videos
remoteVideosEl: 'remoteVideos',
// immediately ask for camera access
autoRequestMedia: true
});
```

At this point, if you run the code above, you’ll see your video turn on and render in the container you gave it.

The next step is to actually specify who you want to connect to.

For simplicity and maximum “tinkerability” we do this by asking that both users who want to connect to each other join the same “room”, which basically means: call “join” with the same string.

So, for demonstration purposes we’ll just tell our `webrtc`

to join a certain room once it’s ready (meaning it’s connected to the signaling server). We do this like so:

```
// we have to wait until it's ready
webrtc.on('readyToCall', function () {
// you can name it anything
webrtc.joinRoom('your awesome room name');
});
```

Once a user has done this, he/she is ready and waiting for someone to join.

If you want to test this locally, you can either open it in Firefox and Chrome or in two tabs within Chrome. (Firefox doesn’t yet let two tabs both access local media).

At this point, you should automatically be connected and be having a lively (probably very echo-y!) conversation with yourself.

If you happen to be me, it’d look like this:

## The signaling server

The example above will connect to a sandbox signaling server we keep running to make it easy to mess around with this stuff.

We aim to keep it available for people to use to play with SimpleWebRTC, but it’s definitely not meant for production use and we may kill it or restart it at any time.

If you want to actually build an app that depends on it, you can either run one yourself, or if you’d rather not mess with it, we can host, and keep up to date, and help scale one for you. The code for that server is [on github](https://github.com/andyet/signalmaster).

You can just pass a URL to a different signaling server as part of your config by passing a “url” option when initiating your `webrtc`

object.

## So, what’s it actually doing under the hood?

It’s not too bad, really. You can read the full source of the client library here: [https://github.com/HenrikJoreteg/SimpleWebRTC/blob/master/simplewebrtc.js](https://github.com/HenrikJoreteg/SimpleWebRTC/blob/master/simplewebrtc.js) and the signaling server here: [https://github.com/andyet/signalmaster/blob/master/server.js](https://github.com/andyet/signalmaster/blob/master/server.js)

**The process of starting a video call in conversat.io looks something like this:**

-
Establish connection to the signaling server. It does this with socket.io and connects to our sandbox signaling server at: http://signaling.simplewebrtc.com:8888

-
Request access to local video camera by calling browser prefixed

`getUserMedia`

. -
Create or get local video element and attach the stream that we get from

`getUserMedia`

to the video element.firefox:

element.mozSrcObject = stream; element.play();

webkit:

element.autoplay = true; element.src = webkitURL.createObjectURL(stream);

-
Call

`joinRoom`

which sends a socket.io message to the signaling server telling it the name of the room name it wants to connect to. The signaling server will either create the room if it doesn’t exist or join it if it does. All I mean by “room” is that the particular socket.io session ID is grouped by that room name so we can broadcast messages about people joining/leaving that room to only the clients connected to that room. -
Now we play an awesome rocket lander game that

[@fritzy](http://twitter.com/fritzy)wrote while we wait for someone to join us:![](../../assets/f87f08a70e3b1bf8.png)

-
When someone else joins the same “room” we broadcast that to the other connected users and we create a

`Conversation`

object that we’ve defined which wraps the browser’s`peerConnection`

. The peer connection represents, as you’d probably guess, the connection between you and another person. -
The signaling server broadcasts the new socket.io session ID to each user in the room and each user’s client creates a Conversation object for every other user in the room.

-
At this point we have a mechanism of knowing who to connect to and how to send direct messages to each of their sessions.

-
Now we use the peerConnection to create an “offer” and store our local offer and set it in our peer connection as the local description. This contains information about how another client can reach and talk to our browser.

peerConnection.createOffer();

We then send this over our socket.io connection to the other people in the room.

-
When a client receives and offer we add it to our peer connection:

var remote = new RTCSessionDescription(message.payload); peerConnection.setRemoteDescriptionremoteDescription);

and generate an answer by calling

`peerConnection.createAnswer()`

and send that back to the person we got the offer from. -
When the answer is received we set it as the remote description. Then we create and send ICE Candidates much in the same way. This will negotiate our connection and connect us.

-
If that process is successful we’ll get an

`onaddstream`

event from our peer connection and we can then create a video element and attach that stream to it. At this point the video call should be in progress.

If you wish to dig into it further, send pull requests and file issues on the [SimpleWebRTC project](https://github.com/HenrikJoreteg/SimpleWebRTC) on github.

## The road ahead

This is just a start. Help us make this stuff better!

There’s a lot more we’d like to see with this:

- Making the signaling piece more pluggable (so you can use whatever you want).
- Adding support for pausing and resuming video/audio.
- It’d be great to be able to figure out who’s talking and emit an event to other connected users when that changes.
- Better control over handling/rejecting incoming requests.
- Setting max connections, perhaps determined based on HTML5 connection APIs?

Hit me up on twitter ([@henrikjoreteg](http://twitter.com/henrikjoreteg)) if you do something cool with this stuff or run into issues or just want to talk about it. I’d love to hear from you.

Keep building awesome stuff, you amazing web people! Go go gadget Internet!

## About
[
Henrik Joreteg ](http://andyet.com)

[Henrik Joreteg](http://twitter.com/henrikjoreteg) is a Partner at [&yet](http://andyet.com), where he’s written dozens of realtime apps two dozen ways. At &yet, he works on [And Bang](http://next.andbang.com) and provides consulting and training on JavaScript and HTML5 applications. Henrik also curates [RealtimeConf](http://realtimeconf.com) and the [Keeping it Realtime Newsletter](http://keepingitrealtime.com). He believes WebRTC is the most interesting technology to hit the web in many years.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 27 comments

JulienMarch 21st, 2013 at 02:44louisremiMarch 21st, 2013 at 05:03Steve PriceMarch 21st, 2013 at 11:44Nikos RoussosMarch 21st, 2013 at 09:00Henrik JoretegMarch 22nd, 2013 at 07:03Chris PetersonMarch 21st, 2013 at 11:10FabianMarch 21st, 2013 at 12:39Robert O’CallahanMarch 21st, 2013 at 19:28Henrik JoretegMarch 22nd, 2013 at 07:04Clayton GulickMarch 30th, 2013 at 19:45Clayton GulickMarch 30th, 2013 at 20:03Henrik JoretegApril 7th, 2013 at 08:19Robert Nyman [Editor]April 8th, 2013 at 10:11FranApril 1st, 2013 at 15:12Henrik JoretegApril 8th, 2013 at 08:57DamianApril 2nd, 2013 at 15:07fileneedApril 6th, 2013 at 20:12Henrik JoretegApril 8th, 2013 at 08:54GuoApril 5th, 2013 at 00:27Henrik JoretegApril 8th, 2013 at 08:56GuoApril 8th, 2013 at 19:04Robert Nyman [Editor]April 8th, 2013 at 23:52Jon EllisApril 13th, 2013 at 07:46Robert Nyman [Editor]April 13th, 2013 at 08:57RahulApril 14th, 2013 at 03:04Russ PetersenApril 18th, 2013 at 15:10Henrik JoretegApril 19th, 2013 at 11:41