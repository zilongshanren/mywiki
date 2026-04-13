---
title: WebRTC and the Early API – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/07/webrtc-and-the-early-api/
author: Louis Stowasser
published: '2013-07-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s Note:** A lot has changed since this post was published in 2013… WebRTC is now widely available in all major browsers, but its API looks a bit different. As part of the web standardization process, we’ve seen improvements such as finer-grained control of media (through tracks rather than streams). Check out this [ Simple RTCDataChannel sample on MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Simple_RTCDataChannel_sample) for a more up-to-date example.

In my last article, [WebRTC and the Ocean of Acryonyms](https://hacks.mozilla.org/2013/07/webrtc-and-the-ocean-of-acronyms/), I went over the networking terminology behind WebRTC. In this sequel of sorts, I will go over the new WebRTC API in great laboring detail. By the end of it you should have working peer-to-peer DataChannels and Media.

## Shims

As you can imagine, with such an early API, you must use the browser prefixes and shim it to a common variable.

```
var PeerConnection = window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
var IceCandidate = window.mozRTCIceCandidate || window.RTCIceCandidate;
var SessionDescription = window.mozRTCSessionDescription || window.RTCSessionDescription;
navigator.getUserMedia = navigator.getUserMedia || navigator.mozGetUserMedia || navigator.webkitGetUserMedia;
```

## PeerConnection

This is the starting point to creating a connection with a peer. It accepts information about which servers to use and options for the type of connection.

`var pc = new PeerConnection(server, options);`

`server`


The server object contains information about which TURN and/or STUN servers to use. This is required to ensure most users can actually create a connection by avoiding restrictions in NAT and firewalls.

```
var server = {
iceServers: [
{url: "stun:23.21.150.121"},
{url: "stun:stun.l.google.com:19302"},
{url: "turn:numb.viagenie.ca", credential: "webrtcdemo", username: "louis%40mozilla.com"}
]
}
```

Google runs a [public STUN server](https://code.google.com/p/natvpn/source/browse/trunk/stun_server_list) that we can use. I also created an account at http://numb.viagenie.ca/ for a free TURN server to access. You may want to do the same and replace with your own credentials.

`options`


Depending on the type of connection, you will need to pass some options.

```
var options = {
optional: [
{DtlsSrtpKeyAgreement: true},
{RtpDataChannels: true}
]
}
```

`DtlsSrtpKeyAgreement`

is required for Chrome and Firefox to interoperate.

`RtpDataChannels`

is required if we want to make use of the DataChannels API on Firefox.

## ICECandidate

After creating the PeerConnection and passing in the available STUN and TURN servers, an event will be fired once the ICE framework has found some “candidates” that will allow you to connect with a peer. This is known as an ICE Candidate and will execute a callback function on PeerConnection#onicecandidate.

```
pc.onicecandidate = function (e) {
// candidate exists in e.candidate
if (e.candidate == null) { return }
send("icecandidate", JSON.stringify(e.candidate));
pc.onicecandidate = null;
};
```

When the callback is executed, we must use the signal channel to send the Candidate to the peer. On Chrome, multiple ICE candidates are usually found, we only need one so I typically send the first one then remove the handler. Firefox includes the Candidate in the Offer SDP.

## Signal Channel

Now that we have an ICE candidate, we need to send that to our peer so they know how to connect with us. However this leaves us with a chicken and egg situation; we want PeerConnection to send data to a peer but before that we need to send them metadata…

This is where the signal channel comes in. It’s any method of data transport that allows two peers to exchange information. In this article, we’re going to use [FireBase](http://firebase.com) because it’s incredibly easy to setup and doesn’t require any hosting or server-code.

For now just imagine two methods exist: `send()`

will take a key and assign data to it and `recv()`

will call a handler when a key has a value.

The structure of the database will look like this:

```
{
"
```": {
"candidate:": …
"offer": …
"answer": …
}
}

Connections are divided by a `roomId`

and will store 4 pieces of information, the ICE candidate from the offerer, the ICE candidate from the answerer, the offer SDP and the answer SDP.

## Offer

An Offer SDP (Session Description Protocol) is metadata that describes to the other peer the format to expect (video, formats, codecs, encryption, resolution, size, etc etc).

An exchange requires an offer from a peer, then the other peer must receive the offer and provide back an answer.

```
pc.createOffer(function (offer) {
pc.setLocalDescription(offer);
send("offer", JSON.stringify(offer));
}, errorHandler, constraints);
```

`errorHandler`


If there was an issue generating an offer, this method will be executed with error details as the first argument.

```
var errorHandler = function (err) {
console.error(err);
};
```

`constraints`


Options for the offer SDP.

```
var constraints = {
mandatory: {
OfferToReceiveAudio: true,
OfferToReceiveVideo: true
}
};
```

`OfferToReceiveAudio/Video`

tells the other peer that you would like to receive video or audio from them. This is not needed for DataChannels.

Once the offer has been generated we must set the local SDP to the new offer and send it through the signal channel to the other peer and await their Answer SDP.

## Answer

An Answer SDP is just like an offer but a response; sort of like answering the phone. We can only generate an answer once we have received an offer.

```
recv("offer", function (offer) {
offer = new SessionDescription(JSON.parse(offer))
pc.setRemoteDescription(offer);
pc.createAnswer(function (answer) {
pc.setLocalDescription(answer);
send("answer", JSON.stringify(answer));
}, errorHandler, constraints);
});
```

## DataChannel

I will first explain how to use PeerConnection for the DataChannels API and transferring arbitrary data between peers.

*Note: At the time of this article, interoperability between Chrome and Firefox is not possible with DataChannels. Chrome supports a similar but private protocol and will be supporting the standard protocol soon.*

`var channel = pc.createDataChannel(channelName, channelOptions);`

The offerer should be the peer who creates the channel. The answerer will receive the channel in the callback `ondatachannel`

on PeerConnection. You must call `createDataChannel()`

once before creating the offer.

`channelName`


This is a string that acts as a label for your channel name. *Warning: Make sure your channel name has no spaces or Chrome will fail on createAnswer().*

`channelOptions`


`var channelOptions = {};`

Currently these options are not well supported on Chrome so you can leave this empty for now. Check the [RFC](http://dev.w3.org/2011/webrtc/editor/webrtc.html#attributes-7) for more information about the options.

### Channel Events and Methods

`onopen`


Executed when the connection is established.

`onerror`


Executed if there is an error creating the connection. First argument is an error object.

```
channel.onerror = function (err) {
console.error("Channel Error:", err);
};
```

`onmessage`


```
channel.onmessage = function (e) {
console.log("Got message:", e.data);
}
```

The heart of the connection. When you receive a message, this method will execute. The first argument is an event object which contains the data, time received and other information.

`onclose`


Executed if the other peer closes the connection.

**Binding the Events**

If you were the creator of the channel (meaning the offerer), you can bind events directly to the DataChannel you created with `createChannel`

. If you are the answerer, you must use the `ondatachannel`

callback on PeerConnection to access the same channel.

```
pc.ondatachannel = function (e) {
e.channel.onmessage = function () { … };
};
```

The channel is available in the event object passed into the handler as `e.channel`

.

`send()`


`channel.send("Hi Peer!");`

This method allows you to send data directly to the peer! Amazing. You must send either String, Blob, ArrayBuffer or ArrayBufferView, so be sure to stringify objects.

`close()`


Close the channel once the connection should end. It is recommended to do this on page unload.

## Media

Now we will cover transmitting media such as audio and video. To display the video and audio you must include a `<video>`

tag on the document with the attribute `autoplay`

.

### Get User Media

```
var video = document.getElementById("preview");
navigator.getUserMedia(mediaOptions, function (stream) {
video.src = URL.createObjectURL(stream);
}, errorHandler);
```

`mediaOptions`


Constraints on what media types you want to return from the user.

```
var mediaOptions = {
video: true,
audio: true
};
```

If you just want an audio chat, remove the `video`

key.

`errorHandler`


Executed if there is an error returning the requested media.

### Media Events and Methods

`addStream`


Add the stream from `getUserMedia`

to the PeerConnection.

`pc.addStream(stream);`

`onaddstream`


Executed when the connection has been setup and the other peer has added the stream to the peer connection with `addStream`

. You need another `<video>`

tag to display the other peer’s media.

```
var otherPeer = document.getElementById("otherPeer");
pc.onaddstream = function (e) {
otherPeer.src = URL.createObjectURL(e.stream);
};
```

The first argument is an event object with the other peer’s media stream.

## View the Source already

You can see the source built up from all the snippets in this article at [my WebRTC repo](http://github.com/louisstow/WebRTC).

## About
[
Louis Stowasser ](http://louisstowasser.com)

I am a Partner Engineer for Mozilla, maintainer of [Gamedev Weekly](http://gamedevweekly.com) and creator of the [CraftyJS](http://craftyjs.com) game engine, based in Brisbane Australia.

## 14 comments

JonathanJuly 31st, 2013 at 17:50barduAugust 1st, 2013 at 09:09Fabian GortAugust 2nd, 2013 at 03:54Randell JesupAugust 2nd, 2013 at 10:20Fabian GortAugust 2nd, 2013 at 14:26BinyaminAugust 7th, 2013 at 00:10Randell JesupAugust 7th, 2013 at 05:43Louis StowasserAugust 11th, 2013 at 16:06Nathan GordonAugust 7th, 2013 at 16:42Louis StowasserAugust 11th, 2013 at 16:07Sam DuttonAugust 8th, 2013 at 03:17Benjamin SlaterAugust 19th, 2013 at 14:16nicole riversAugust 22nd, 2013 at 00:00Jan Honza OdvarkoAugust 28th, 2013 at 07:33