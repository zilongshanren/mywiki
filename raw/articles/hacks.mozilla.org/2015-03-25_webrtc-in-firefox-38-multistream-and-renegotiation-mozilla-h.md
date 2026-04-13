---
title: 'WebRTC in Firefox 38: Multistream and renegotiation – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2015/03/webrtc-in-firefox-38-multistream-and-renegotiation/
author: Nils Ohlmeier
published: '2015-03-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s Note:** A lot has changed since this post was published in 2013… WebRTC is now widely available in all major browsers, but its API looks a bit different. As part of the web standardization process, we’ve seen improvements such as finer-grained control of media (through tracks rather than streams). Check out this [ Simple RTCDataChannel sample on MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Simple_RTCDataChannel_sample) for a more up-to-date example.

Building on the JSEP (Javascript Session Establishment Protocol) engine rewrite introduced in 37, Firefox 38 now has support for multistream (multiple tracks of the same type in a single PeerConnection), and renegotiation (multiple offer/answer exchanges in a single PeerConnection). As usual with such things, there are caveats and limitations, but the functionality seems to be pretty solid.

## Multistream and renegotiation features

Why are these things useful, you ask? For example, now you can handle a group video call with a single PeerConnection (multistream), and do things like add/remove these streams on the fly (renegotiation). You can also add screensharing to an existing video call without needing a separate PeerConnection. Here are some advantages of this new functionality:

- Simplifies your job as an app-writer
- Requires fewer rounds of
[ICE](https://developer.mozilla.org/en-US/docs/Glossary/ICE)(Interactive Connectivity Establishment – the protocol for establishing connection between the browsers), and reduces call establishment time - Requires fewer ports, both on the browser and on TURN relays (if using bundle, which is enabled by default)

Now, there are very few WebRTC services that use multistream (the way it is currently specified, see below) or renegotiation. This means that real-world testing of these features is extremely limited, and there will probably be bugs. If you are working with these features, and are having difficulty, do not hesitate to ask questions in IRC at irc.mozilla.org on #media, since this helps us find these bugs.

Also, it is important to note that Google Chrome’s current implementation of multistream is not going to be interoperable; this is because Chrome has not yet implemented the specification for multistream (called “unified plan” – check on their progress in the [Google Chromium Bug tracker](https://code.google.com/p/chromium/issues/detail?id=465349)). Instead they are still using an older Google proposal (called “plan B”). These two approaches are mutually incompatible.

On a related note, if you maintain or use a WebRTC gateway that supports multistream, odds are good that it uses “plan B” as well, and will need to be updated. This is a good time to start implementing unified plan support. (Check the *Appendix* below for examples.)

## Building a simple WebRTC video call page

So let’s start with a concrete example. We are going to build a simple WebRTC video call page that allows the user to add screen sharing during the call. As we are going to dive deep quickly you might want to check out our earlier Hacks article, [WebRTC and the Early API](https://hacks.mozilla.org/2013/07/webrtc-and-the-early-api/), to learn the basics.

First we need two PeerConnections:

```
pc1 = new mozRTCPeerConnection();
pc2 = new mozRTCPeerConnection();
```

Then we request access to camera and microphone and attach the resulting stream to the first PeerConnection:

```
let videoConstraints = {audio: true, video: true};
navigator.mediaDevices.getUserMedia(videoConstraints)
.then(stream1) {
pc1.addStream(stream1);
});
```

To keep things simple we want to be able to run the call just on one machine. But most computers today don’t have two cameras and/or microphones available. And just having a one-way call is not very exciting. So let’s use a built-in testing feature of Firefox for the other direction:

```
let fakeVideoConstraints = {video: true, fake: true };
navigator.mediaDevices.getUserMedia(fakeVideoConstraints)
.then(stream2) {
pc2.addStream(stream2);
});
```

Note: You’ll want to call this part from within the success callback of the first *getUserMedia()* call so that you don’t have to track with boolean flags if both *getUserMedia()* calls succeeded before you proceed to the next step.

Firefox also has a built-in fake audio source (which you can turn on like this *{audio: true, fake: true}*). But listening to an 8kHz tone is not as pleasant as looking at the changing color of the fake video source.

Now we have all the pieces ready to create the initial offer:

```
pc1.createOffer().then(step1, failed);
```

Now the WebRTC typical offer – answer flow follows:

```
function step1(offer) {
pc1_offer = offer;
pc1.setLocalDescription(offer).then(step2, failed);
}
function step2() {
pc2.setRemoteDescription(pc1_offer).then(step3, failed);
}
```

For this example we take a shortcut: Instead of passing the signaling message through an actual signaling relay, we simply pass the information into both PeerConnections as they are both locally available on the same page. Refer to our previous hacks article [WebRTC and the Early API](https://hacks.mozilla.org/2013/07/webrtc-and-the-early-api/) for a solution which actually uses FireBase as relay instead to connect two browsers.

```
function step3() {
pc2.createAnswer().then(step4, failed);
}
function step4(answer) {
pc2_answer = answer;
pc2.setLocalDescription(answer).then(step5, failed);
}
function step5() {
pc1.setRemoteDescription(pc2_answer).then(step6, failed);
}
function step6() {
log("Signaling is done");
}
```

The one remaining piece is to connect the remote videos once we receive them.

```
pc1.onaddstream = function(obj) {
pc1video.mozSrcObject = obj.stream;
}
```

Add a similar clone of this for our PeerConnection 2. Keep in mind that these callback functions are super trivial — they assume we only ever receive a single stream and only have a single video player to connect it. The example will get a little more complicated once we add the screen sharing.

With this we should be able to establish a simple call with audio and video from the real devices getting sent from PeerConnection 1 to PeerConnection 2 and in the opposite direction a fake video stream that shows slowly changing colors.

## Implementing screen sharing

Now let’s get to the real meat and add screen sharing to the already established call.

```
function screenShare() {
let screenConstraints = {video: {mediaSource: "screen"}};
navigator.mediaDevices.getUserMedia(screenConstraints)
.then(stream) {
stream.getTracks().forEach(track) {
screenStream = stream;
screenSenders.push(pc1.addTrack(track, stream));
});
});
}
```

Two things are required to get screen sharing working:

- Only pages loaded over HTTPS are allowed to request screen sharing.
- You need to append your domain to the user preference
*media.getusermedia.screensharing.allowed_domains*in*about:config*to whitelist it for screen sharing.

For the screenConstraints you can also use ‘*window*‘ or ‘*application*‘ instead of ‘*screen*‘ if you want to share less than the whole screen.

We are using *getTracks()* here to fetch and store the video track out of the stream we get from the getUserMedia call, because we need to remember the track later when we want to be able to remove screen sharing from the call. Alternatively, in this case you could use the *addStream()* function used before to add new streams to a PeerConnection. But the *addTrack()* function gives you more flexibility if you want to handle video and audio tracks differently, for instance. In that case, you can fetch these tracks separately via the *getAudioTracks()* and *getVideoTracks()* functions instead of using the *getTracks()* function.

Once you add a stream or track to an established PeerConnection this needs to be signaled to the other side of the connection. To kick that off, the *onnegotiationneeded* callback will be invoked. So your callback should be setup before adding a track or stream. The beauty here — from this point on we can simply re-use our signaling call chain. So the resulting screen share function looks like this:

```
function screenShare() {
let screenConstraints = {video: {mediaSource: "screen"}};
pc1.onnegotiationneeded = function (event) {
pc1.createOffer(step1, failed);
};
navigator.mediaDevices.getUserMedia(screenConstraints)
.then(stream) {
stream.getTracks().forEach(track) {
screenStream = stream;
screenSenders.push(pc1.addTrack(track, stream));
});
});
}
```

Now the receiving side also needs to learn that the stream from the screen sharing was successfully established. We need to slightly modify our initial *onaddstream* function for that:

```
pc2.onaddstream = function(obj) {
var stream = obj.stream;
if (stream.getAudioTracks().length == 0) {
pc3video.mozSrcObject = obj.stream;
} else {
pc2video.mozSrcObject = obj.stream;
}
}
```

The important thing to note here: With multistream and renegotiation *onaddstream* can and will be called multiple times. In our little example *onaddstream* is called the first time we establish the connection and PeerConnection 2 starts receiving the audio and video from the real devices. And then it is called a second time when the video stream from the screen sharing is added.

We are simply assuming here that the screen share will have no audio track in it to distinguish the two cases. There are probably cleaner ways to do this.

Please refer to the *Appendix* for a bit more detail on what happens here under the hood.

As the user probably does not want to share his/her screen until the end of the call let’s add a function to remove it as well.

```
function stopScreenShare() {
screenStream.stop();
screenSenders.forEach(sender) {
pc1.removeTrack(sender);
});
}
```

We are holding on to a reference to the original stream to be able to call *stop()* on it to release the getUserMedia permission we got from the user. The *addTrack()* call in our *screenShare()* function returned us an RTCRtpSender object, which we are storing so we can hand it to the *removeTrack()* function.

All of the code combined with some extra syntactic sugar can be found on our [MultiStream test page](https://mozilla.github.io/webrtc-landing/pc_test_multi.html).

If you are going to build something which allows both ends of the call to add screen share, a more realistic scenario than our demo, you will need to handle special cases. For example, multiple users might accidentally try to add another stream (e.g. the screen share) exactly at the same time and you may end up with a new corner-case for renegotiation called “glare.” This is what happens when both ends of the WebRTC session decide to send new offers at the same time. We do not yet support the “rollback” session description type that can be used to recover from glare (see [Jsep draft](https://tools.ietf.org/html/draft-ietf-rtcweb-jsep-09#section-4.1.4.2) and the [Firefox bug](https://bugzilla.mozilla.org/show_bug.cgi?id=952145)). Probably the best interim solution to prevent glare is to announce via your signaling channel that the user did something which is going to kick off another round of renegotiation. Then, wait for the okay from the far end before you call *createOffer()* locally.

## Appendix

This is an example renegotiation offer SDP from Firefox 39 when adding the screen share:


v=0

o=mozilla...THIS_IS_SDPARTA-39.0a1 7832380118043521940 1 IN IP4 0.0.0.0

s=-

t=0 0

a=fingerprint:sha-256 4B:31:DA:18:68:AA:76:A9:C9:A7:45:4D:3A:B3:61:E9:A9:5F:DE:63:3A:98:7C:E5:34:E4:A5:B6:95:C6:F2:E1

a=group:BUNDLE sdparta_0 sdparta_1 sdparta_2

a=ice-options:trickle

a=msid-semantic:WMS *

m=audio 9 RTP/SAVPF 109 9 0 8

c=IN IP4 0.0.0.0

a=candidate:0 1 UDP 2130379007 10.252.26.177 62583 typ host

a=candidate:1 1 UDP 1694236671 63.245.221.32 54687 typ srflx raddr 10.252.26.177 rport 62583

a=sendrecv

a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level

a=ice-pwd:3aefa1a552633717497bdff7158dd4a1

a=ice-ufrag:730b2351

a=mid:sdparta_0

a=msid:{d57d3917-64e9-4f49-adfb-b049d165c312} {920e9ffc-728e-0d40-a1b9-ebd0025c860a}

a=rtcp-mux

a=rtpmap:109 opus/48000/2

a=rtpmap:9 G722/8000/1

a=rtpmap:0 PCMU/8000

a=rtpmap:8 PCMA/8000

a=setup:actpass

a=ssrc:323910839 cname:{72b9ff9f-4d8a-5244-b19a-bd9b47251770}

m=video 9 RTP/SAVPF 120

c=IN IP4 0.0.0.0

a=candidate:0 1 UDP 2130379007 10.252.26.177 62583 typ host

a=candidate:1 1 UDP 1694236671 63.245.221.32 54687 typ srflx raddr 10.252.26.177 rport 62583

a=sendrecv

a=fmtp:120 max-fs=12288;max-fr=60

a=ice-pwd:3aefa1a552633717497bdff7158dd4a1

a=ice-ufrag:730b2351

a=mid:sdparta_1

a=msid:{d57d3917-64e9-4f49-adfb-b049d165c312} {35eeb34f-f89c-3946-8e5e-2d5abd38c5a5}

a=rtcp-fb:120 nack

a=rtcp-fb:120 nack pli

a=rtcp-fb:120 ccm fir

a=rtcp-mux

a=rtpmap:120 VP8/90000

a=setup:actpass

a=ssrc:2917595157 cname:{72b9ff9f-4d8a-5244-b19a-bd9b47251770}

m=video 9 RTP/SAVPF 120

c=IN IP4 0.0.0.0

a=sendrecv

a=fmtp:120 max-fs=12288;max-fr=60

a=ice-pwd:3aefa1a552633717497bdff7158dd4a1

a=ice-ufrag:730b2351

a=mid:sdparta_2

a=msid:{3a2bfe17-c65d-364a-af14-415d90bb9f52} {aa7a4ca4-189b-504a-9748-5c22bc7a6c4f}

a=rtcp-fb:120 nack

a=rtcp-fb:120 nack pli

a=rtcp-fb:120 ccm fir

a=rtcp-mux

a=rtpmap:120 VP8/90000

a=setup:actpass

a=ssrc:2325911938 cname:{72b9ff9f-4d8a-5244-b19a-bd9b47251770}


Note that each track gets its own m-section, denoted by the msid attribute.

As you can see from the BUNDLE attribute, Firefox offers to put the new video stream, with its different msid value, into the same bundled transport. That means if the answerer agrees we can start sending the video stream over the already established transport. We don’t have to go through another ICE and DTLS round. And in case of TURN servers we save another relay resource.

Hypothetically, this is what the previous offer would look like if it used plan B (as Chrome does):


v=0

o=mozilla...THIS_IS_SDPARTA-39.0a1 7832380118043521940 1 IN IP4 0.0.0.0

s=-

t=0 0

a=fingerprint:sha-256 4B:31:DA:18:68:AA:76:A9:C9:A7:45:4D:3A:B3:61:E9:A9:5F:DE:63:3A:98:7C:E5:34:E4:A5:B6:95:C6:F2:E1

a=group:BUNDLE sdparta_0 sdparta_1

a=ice-options:trickle

a=msid-semantic:WMS *

m=audio 9 RTP/SAVPF 109 9 0 8

c=IN IP4 0.0.0.0

a=candidate:0 1 UDP 2130379007 10.252.26.177 62583 typ host

a=candidate:1 1 UDP 1694236671 63.245.221.32 54687 typ srflx raddr 10.252.26.177 rport 62583

a=sendrecv

a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level

a=ice-pwd:3aefa1a552633717497bdff7158dd4a1

a=ice-ufrag:730b2351

a=mid:sdparta_0

a=rtcp-mux

a=rtpmap:109 opus/48000/2

a=rtpmap:9 G722/8000/1

a=rtpmap:0 PCMU/8000

a=rtpmap:8 PCMA/8000

a=setup:actpass

a=ssrc:323910839 msid:{d57d3917-64e9-4f49-adfb-b049d165c312} {920e9ffc-728e-0d40-a1b9-ebd0025c860a}

a=ssrc:323910839 cname:{72b9ff9f-4d8a-5244-b19a-bd9b47251770}

m=video 9 RTP/SAVPF 120

c=IN IP4 0.0.0.0

a=candidate:0 1 UDP 2130379007 10.252.26.177 62583 typ host

a=candidate:1 1 UDP 1694236671 63.245.221.32 54687 typ srflx raddr 10.252.26.177 rport 62583

a=sendrecv

a=fmtp:120 max-fs=12288;max-fr=60

a=ice-pwd:3aefa1a552633717497bdff7158dd4a1

a=ice-ufrag:730b2351

a=mid:sdparta_1

a=rtcp-fb:120 nack

a=rtcp-fb:120 nack pli

a=rtcp-fb:120 ccm fir

a=rtcp-mux

a=rtpmap:120 VP8/90000

a=setup:actpass

a=ssrc:2917595157 msid:{d57d3917-64e9-4f49-adfb-b049d165c312} {35eeb34f-f89c-3946-8e5e-2d5abd38c5a5}

a=ssrc:2917595157 cname:{72b9ff9f-4d8a-5244-b19a-bd9b47251770}

a=ssrc:2325911938 msid:{3a2bfe17-c65d-364a-af14-415d90bb9f52} {aa7a4ca4-189b-504a-9748-5c22bc7a6c4f}

a=ssrc:2325911938 cname:{72b9ff9f-4d8a-5244-b19a-bd9b47251770}


Note that there is only one video m-section, with two different msids, which are part of the ssrc attributes rather than in their own a lines (these are called “source-level” attributes).

## About Nils Ohlmeier

Hacking on real time communications since 2002

## 4 comments

Matthew FredricksonMarch 25th, 2015 at 08:35Bruce WilliamsApril 6th, 2015 at 13:25Nils OhlmeierApril 6th, 2015 at 15:18Bruce WilliamsApril 7th, 2015 at 08:57