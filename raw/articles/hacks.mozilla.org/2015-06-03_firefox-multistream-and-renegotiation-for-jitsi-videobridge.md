---
title: Firefox multistream and renegotiation for Jitsi Videobridge – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2015/06/firefox-multistream-and-renegotiation-for-jitsi-videobridge/
author: George Politis
published: '2015-06-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

# Firefox multistream and renegotiation for Jitsi Videobridge

**Author’s note:** Firefox landed support for multistream and renegotiation support in Firefox 38. This article talks about how the team at Jitsi Videobridge, a WebRTC service, collaborated with the Firefox WebRTC team to get Jitsi’s multi-party video conferencing working well in Firefox. In the process, several issues were identified and fixed on both sides of the system. Firefox 40 (our newly released [Developer Edition](https://www.mozilla.org/en-US/firefox/developer/)) and later versions include all those fixes. This post, written by Jitsi engineer George Politis, assumes some [basic knowledge of WebRTC](https://en.wikipedia.org/wiki/WebRTC) and how it works.

Firefox is the first browser to implement the spec-compliant “Unified Plan” for multistream support, which Chrome will be moving to, but hasn’t implemented yet. Thus, services that currently work on Chrome will need some modifications to work on Firefox. I encourage all service providers who have or are thinking of adding multistream support to give Firefox 40 or later a try and let us know how it works for you. Thanks.

Maire Reavy

Engineering Manager, Web RTC

Many of you WebRTC developers out there have probably already come across the name Jitsi Videobridge. Multi-party video conferencing is arguably one of the most popular use cases for WebRTC and once you start looking for servers that allow you to implement it, Jitsi’s name is among the first you stumble upon.

For a while now, a number of JavaScript applications have been using WebRTC and Jitsi Videobridge to deliver a rich conferencing experience to their users. The bridge provides a lightweight way (think routing vs. mixing) of conducting high quality video conferences, so it has received its fair share of attention.

The problem was that, until recently, applications using Jitsi Videobridge only worked on a limited set of browsers: Chromium, Chrome, and Opera.

This limitation is now gone!

After a few months of hard work by Mozilla and Jitsi developers, both Firefox and Jitsi have added the missing pieces and can now work together.

While this wasn’t the most difficult project on Earth, it wasn’t quite a walk in the park either. In this post we’ll tell you more about the nitty-gritty details of our collaborative adventure.

[Jitsi Videobridge](https://github.com/jitsi/jitsi-videobridge) is an open source (LGPL) lightweight video conferencing server. WebRTC JavaScript applications such as Jitsi Meet use Jitsi Videobridge to provide high quality, scalable video conferences. Jitsi Videobridge receives video from every participant and then relays some or all of it to everyone else. The IETF term for Jitsi Videobridge is a [Selective Forwarding Unit](https://webrtcglossary.com/sfu/) (SFU). Sometimes such servers are also referred to as video routers or MCUs. The same technology is used by most modern video conferencing systems like Google Hangouts, Skype, Vidyo, and many others.

From a WebRTC perspective, every browser establishes exactly one PeerConnection with the videobridge. The browser sends and receives all audio and video data to and from the bridge over that one PeerConnection.

In a Jitsi Videobridge-based conference, all signaling goes through a separate server-side application called the *Focus*. It is responsible for managing media sessions between each of the participants and the videobridge. Communication between the Focus and a given participant is done through Jingle and between the Focus and the Jitsi Videobidge through * COLIBRI*.

When discussing interoperability between Firefox and Chrome for multi-party video conferences, it is impossible not to talk a little bit (or a lot!) about the [Unified Plan](https://tools.ietf.org/html/draft-roach-mmusic-unified-plan-00) and [Plan B](https://tools.ietf.org/html/draft-uberti-rtcweb-plan-00). These were two competing IETF drafts for the negotiation and exchange of multiple media sources (i.e., MediaStreamTracks or MSTs) between WebRTC endpoints. Unified Plan has been incorporated into the [JSEP draft](https://tools.ietf.org/html/draft-ietf-rtcweb-jsep-09) and [Bundle negotiation draft](https://tools.ietf.org/html/draft-ietf-mmusic-sdp-bundle-negotiation-19), which are on their way to becoming IETF standards. Plan B expired in 2013 and nobody should care about it anymore … at least in theory.

In reality, Plan B lives on in Chrome and its derivatives, like Chromium and Opera. There’s actually an issue in the Chromium bug tracker to add support for [Unified Plan in Chromium](https://code.google.com/p/chromium/issues/detail?id=465349), but that’ll take some time. Firefox, on the other hand, has, [as of recently](https://hacks.mozilla.org/2015/03/webrtc-in-firefox-38-multistream-and-renegotiation/), implemented Unified Plan.

Developers who implement many-to-many WebRTC-based videoconferencing solutions and want to support both Firefox and Chrome have to deal with this situation and implement some kind of interoperability layer between Chrome and and Firefox. Jitsi Meet is no exception of course; in the beginning it was a no-brainer to assume Plan B because that’s what Chrome implements and Firefox didn’t have [multistream support](https://bugzilla.mozilla.org/show_bug.cgi?id=1095218). As a result, most of Jitsi’s abstractions were built around this assumption.

The most substantial difference between Unified Plan and Plan B is how they represent media stream tracks. Unified Plan extends the standard way of encoding this information in SDP which is to have each [RTP flow (i.e., SSRC)](http://en.wikipedia.org/wiki/Real-time_Transport_Protocol) appear on its own [m-line](https://tools.ietf.org/html/rfc4566#section-5.14). So, each media stream track is represented by its own unique m-line. This is a strict one-to-one mapping; a single media stream track cannot be spread across several m-lines, nor may a single m-line represent multiple media stream tracks.

Plan B takes a different approach, and creates a hierarchy within SDP; an m= line defines an “envelope”, specifying codec and transport parameters, and a=ssrc lines are used to describe individual media sources within that envelope. So, typically, a Plan B SDP has three channels, one for audio, one for video, and one for the data.

On the Jitsi side, it was obvious from the beginning that all the magic should happen in the client. The Focus communicates with the clients using Jingle, which is in turn transformed into SDP, and then handed over to the browser. There’s no SDP going around on the wire. Furthermore, there’s no signaling communication between the endpoints and the Jitsi Videobridge, it’s the Focus that mediates this procedure using [COLIBRI](http://xmpp.org/extensions/xep-0340.html). So the question for the Jitsi team was: “*What’s the easiest way to go from Jingle to Unified Plan for Firefox, given that we have code that assumes Plan B in all imaginable places?*”

In its first few attempts, the Jitsi team tried to provide general abstractions wherever there was Plan B specific code. This could have worked, but at the same period of time Jitsi Meet was undergoing some massive refactoring and the inbound Unified Plan patches were constantly broken. On top of that, with multistream support in Firefox in its very early stages, Firefox was breaking more often than it worked. Result: *0* progress. One could even argue that the progress was negative, because of the wasted time.

It was time to change course. The Jitsi team decided to try a more general solution to the problem and deal with it at a lower level. The idea was to build a PeerConnection adapter that would feed the right SDP to the browser, i.e. Unified Plan to Firefox and Plan B to Chrome, and that would give a Plan B SDP to the application. Enter [sdp-interop](https://www.npmjs.com/package/sdp-interop).

sdp-interop is a reusable npm module that offers the two simple methods:

`toUnifiedPlan(sdp)`

that takes an SDP string and transforms it into a Unified Plan SDP.`toPlanB(sdp)`

that, not surprisingly, takes an SDP string and transforms it into a Plan B SDP.

The PeerConnection adapter wraps the `setLocalDescription()`

, `setRemoteDescription()`

methods, and the success callbacks of the `createAnswer()`

and `createOffer()`

methods. If the browser is Chrome, the adapter does nothing. If, on the other hand, the browser is Firefox the PeerConnection adapter does as follows:

- Calls the
`toUnifiedPlan()`

method of the sdp-interop module prior to calling the`setLocalDescription()`

or the`setRemoteDescription()`

methods, thus converting the Plan B SDP from the application to a Unified Plan SDP that Firefox can understand. - Calls the
`toPlanB()`

method prior to calling the`createAnswer()`

or the`createOffer()`

success callback, thus converting the Unified Plan SDP from Firefox to a Plan B SDP that the application can understand.

Here’s a sample PeerConnection adapter built on top of [adapter.js](https://github.com/webrtc/adapter):

```
function PeerConnectionAdapter(ice_config, constraints) {
this.peerconnection = new RTCPeerConnection(ice_config, constraints);
this.interop = new require('sdp-interop').Interop();
}
PeerConnectionAdapter.prototype.setLocalDescription
= function (description, successCallback, failureCallback) {
// if we're running on FF, transform to Unified Plan first.
if (navigator.mozGetUserMedia)
description = this.interop.toUnifiedPlan(description);
this.peerconnection.setLocalDescription(description,
function () { successCallback(); },
function (err) { failureCallback(err); }
);
};
PeerConnectionAdapter.prototype.setRemoteDescription
= function (description, successCallback, failureCallback) {
// if we're running on FF, transform to Unified Plan first.
if (navigator.mozGetUserMedia)
description = this.interop.toUnifiedPlan(description);
this.peerconnection.setRemoteDescription(description,
function () { successCallback(); },
function (err) { failureCallback(err); }
);
};
PeerConnectionAdapter.prototype.createAnswer
= function (successCallback, failureCallback, constraints) {
var self = this;
this.peerconnection.createAnswer(
function (answer) {
if (navigator.mozGetUserMedia)
answer = self.interop.toPlanB(answer);
successCallback(answer);
},
function(err) {
failureCallback(err);
},
constraints
);
};
PeerConnectionAdapter.prototype.createOffer
= function (successCallback, failureCallback, constraints) {
var self = this;
this.peerconnection.createOffer(
function (offer) {
if (navigator.mozGetUserMedia)
offer = self.interop.toPlanB(offer);
successCallback(offer);
},
function(err) {
failureCallback(err);
},
constraints
);
};
```


Like most things in life, sdp-interop is not “perfect,” it makes certain assumptions and has some limitations. First and foremost, unfortunately, a Plan B offer/answer does not have enough information to rebuild an equivalent Unified Plan offer/answer. So, while it is easy, with some limitations, to go from Unified Plan to Plan B, the reverse is not possible without keeping some state.

Suppose, for example, that a Firefox client gets an offer from the Focus to join a large call. In the *native* create answer success callback you get a Unified Plan answer that contains multiple m-lines. You convert it in a Plan B answer using the sdp-interop module and hand it over to the app to do its thing. At some point later-on, the app calls the adapter’s`setLocalDescription()`

method. The adapter will have to convert the Plan B answer back to a Unified Plan one to pass it to Firefox.

That’s the tricky part because you can’t naively put any SSRC in any m-line, each SSRC should be put back into the same m-line that it was in the original answer from the native create answer success callback. The order of the m-lines is important too, so each m-line has to be in the same position as it was in the original answer from the native create answer success callback (matching the position of the m-line in the Unified Plan offer). It is also forbidden to remove an m-line, instead they must be marked as inactive, if they’re no longer used. Similar considerations have to be taken into account when converting a Plan B offer to a Unified Plan one when doing renegotiation, for example.

sdp-interop solves this issue by caching both the most recent Unified Plan offer and the most recent Unified Plan answer. When one goes from Plan B to Unified Plan, sdp-interop uses the cached Unified Plan offer/answer and adds the missing information from there. You can see [here](https://github.com/jitsi/sdp-interop/blob/d4569a12875a7180004726633793430eccd7f47b/lib/interop.js#L175) exactly how this is done.

Another limitation is that, in some cases, a unified plan SDP cannot be mapped to a plan B SDP. If the unified SDP has two audio m-lines (for example) that have different media or transport attributes, these cannot be reconciled when trying to squish them together in a single plan B m-section. This is why sdp-interop can only work if the transport attributes are the same (i.e., bundle and rtcp-mux are being used), and if all codec attributes are exactly the same for each m-line of a given media type. Fortunately, Chrome and Firefox do both of these things by default. (This is probably also part of the reason why implementing Unified Plan won’t be trivial for Chrome.)

One last soft limitation is that the SDP interoperability layer has only been tested when Firefox answers a call and not when it offers one because in the Jitsi architecture the endpoints always get invited by the Focus to join a call and never offer one.

Even with the SDP interoperability layer in place, a number of difficulties had to be overcome to bring Firefox support to Jitsi Videobridge and Mozilla has been a *great* help in solving all of them. In most cases, the problem was easy to fix, but required time and effort to identify. For reference (and for fun!) we’ll briefly describe a few of those problems here.

One of our first unpleasant surprises was that one day the Jitsi prototype implementation decided to stop working all of a sudden. The DTLS negotiation started failing soon after Mozilla [enabled DTLS 1.2 in Firefox](https://bugzilla.mozilla.org/show_bug.cgi?id=1132813), and, as it turned out, there was a problem in the DTLS version negotiation between Firefox and our Bouncy Castle-based stack. The RFCs are a little ambiguous in relation to the record layer versions, but we assumed the openssl rules to be the standard and [patched](https://github.com/bcgit/bc-java/pull/111) our stack to behave according to those rules.

Another minor issue was that Firefox was [missing msids](https://bugzilla.mozilla.org/show_bug.cgi?id=1095218) but Mozilla kindly took care of that.

Next, the Jitsi team faced a very weird issue where the remote video playback on the Firefox side froze or never started. The decoder was stalling. The weird thing about this was that, in the test environment (LAN conditions), the problem appeared to be triggered only when goog-remb was signaled in the SDP. After some digging, it turned out that the problem had nothing to do with goog-remb. The real issue was that the Jitsi Videobridge was relaying RED to Firefox but the latter [doesn’t currently support ulpfec/red](https://bugzilla.mozilla.org/show_bug.cgi?id=875922) so nothing made it through to the decoder. Signaling goog-remb probably tells Chrome to encapsulate VP8 into RED right from the beginning of the streaming, even before packet loss is detected. (Due to the overhead introduced by adding any redundant data, it’s usually a good idea to activate only when the network conditions require it.) The Jitsi Videobridge now decapsulates RED into plain VP8 when it streams to Firefox (or any other client that doesn’t support ULPFEC/RED).

The Jitsi team has also discovered and fixed a few issues in the Jitsi code base, including a non-zero offset bug in our stack, probably inside the SRTP transformers, that was causing SRTP auth failures.

Finally, and maybe most importantly, in a typical multistream enabled conference, Firefox creates two (potentially three) sendrecv channels (for audio, for video, and potentially for data) and N recvonly channels, some for incoming audio and some for incoming video. Those recvonly channels will send RTCP feedback with an internally generated SSRC. Here’s where the trouble begun.

Those internally generated SSRCs of the recvonly channels are known *only* to Firefox. They’re not known neither to the client app (as they’re not included in the SDP), nor to the Jitsi Videobridge, nor to the other endpoints, notably Chrome.

When using bundle, Chrome will discard RTCP traffic coming from [unannounced SSRCs](https://code.google.com/p/webrtc/issues/detail?id=1772) as it uses SSRCs to decide if an RTCP packet should go the the sending Audio or the sending Video channel. If it can’t find where to dispatch an RTCP packet, it drops it. Firefox is not affected as it handles this differently. The webrtc code that does the filtering is in [bundlefilter.cc](https://chromium.googlesource.com/external/webrtc/trunk/talk/+/6a741d7299ddc9eaa9c989729e02d5fdd145bc6e/session/media/bundlefilter.cc) which is not included in mozilla-central. Unfortunately we (Jitsi) have the same filtering/demux logic implemented in our gateway.

This is hugely important because PLIs/RRs/NACKs/etc from recvonly channels although they might reach Chrome, they’re discarded, so the typical result is a stalled decoder on the Firefox side. Mozilla fixed this in [Bug 1160280](https://bugzilla.mozilla.org/show_bug.cgi?id=1160280) by exposing in the SDP the SSRC for recvonly channels.

It’s been quite an interesting journey but we are almost there! Firefox Nightly (v41) and [Firefox Developer Edition 40](https://www.mozilla.org/firefox/developer/) have all the required pieces in place and Jitsi based many-to-many conferences work fine using multistream.

One of the last things for Jitsi to tackle is simulcast support in Firefox. Jitsi’s simulcast implementation relies heavily on MediaStream constructors but they’re [not available](https://bugzilla.mozilla.org/show_bug.cgi?id=1070216) in Firefox at the moment. The Jitsi team is working on an alternative approach that doesn’t require MediaStream constructors. Desktop sharing is another significant item that’s missing when Jitsi runs on Firefox, but it is also currently work in progress.

In other words, Firefox and Jitsi are about to become best buddies!

## About George Politis

## About Maire Reavy

Maire is the engineering manager for Mozilla’s WebRTC team.

## 14 comments

Adam BraultJune 3rd, 2015 at 10:37Gustavo GarciaJune 3rd, 2015 at 23:44MichaelJune 4th, 2015 at 03:14fossJune 4th, 2015 at 06:42George PolitisJune 4th, 2015 at 08:30MatějJune 4th, 2015 at 08:10George PolitisJune 4th, 2015 at 08:25MatějJune 4th, 2015 at 08:43George PolitisJune 4th, 2015 at 09:02Oswaldo SaumetJune 8th, 2015 at 00:38danzoJune 9th, 2015 at 20:35George PolitisJune 10th, 2015 at 01:19danzoJune 10th, 2015 at 03:49George PolitisJune 10th, 2015 at 04:18