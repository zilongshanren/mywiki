---
title: 'WebRTC: Sending DTMF in Firefox – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/11/webrtc-sending-dtmf-in-firefox/
author: Adam Roach
published: '2015-11-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

One of the features defined in [WebRTC](https://developer.mozilla.org/en-US/docs/Web/Guide/API/WebRTC) is the ability to send [DTMF tones](https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling) (popularly known in some markets as “touch tones”). While this has basically no purpose in the browser-to-browser case, it is somewhat important when using WebRTC to initiate calls to the legacy telephone network: many companies still use voice menu systems that require callers to send DTMF digits to indicate why they are calling, input credit card numbers and passcodes, and perform similar tasks.

Until recently, there had been very little interest expressed by developers to make use of this interface; and, as a consequence, it has been a relatively low priority for the Firefox WebRTC team. Over the past few weeks, there has been a surprising spike in queries about the availability of [RTCDTMFSender](http://w3c.github.io/webrtc-pc/#rtcdtmfsender target=). While there is no milestone fixed for implementing it, the feature does remain on our roadmap.

In the meanwhile, there is a reasonable stop-gap approach that will work in the vast majority of use cases. Through the use of [WebAudio](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API) [oscillators](https://developer.mozilla.org/en-US/docs/Web/API/OscillatorNode), it is possible to synthesize DTMF tones and mix them into an audio stream. It is worth noting that this results in behavior that is slightly different than that described in the specification: rather than using [RFC4733](https://tools.ietf.org/html/rfc4733) to send DTMF, this approach will actually encode the tones using the audio codec in use (for telephone gateways, this is almost always [G.711](https://en.wikipedia.org/wiki/G.711)). In practice, this works fine in almost all cases.

I have included an example implementation of this approach at the end of this post. For versions of Firefox prior to 44, applications will need to explicitly construct the DTMFSender with the stream they want to mix DTMF into, and then retrieve a new stream from the DTMFSender to add to the [RTCPeerConnection](https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection) (or wherever it wants to send DTMF tones). For example:

```
navigator.mediaDevices.getUserMedia({ audio: true })
.then(function(micStream) {
var sender = new DTMFSender(micStream);
/* Now that we have a stream that represents microphone
input mixed with the DTMF ("sender.outputStream"), we
can do whatever we want with it. This example plays
it locally, but you could just as easily add it to
a PeerConnection. */
var audio = document.createElement("audio");
document.body.appendChild(audio);
audio.mozSrcObject = sender.outputStream;
audio.play();
sender.ontonechange = function(e) {
console.log(JSON.stringify(e));
}
sender.insertDTMF("2145551212,1");
});
```


That’s admittedly a bit clunky. Fortunately, starting with Firefox 44, the addition of the ability to construct a [MediaStream](https://developer.mozilla.org/en-US/docs/Web/API/MediaStream) directly from a [MediaStreamTrack](https://developer.mozilla.org/en-US/docs/Web/API/MediaStreamTrack) gives us a way to transparently polyfill the DTMF sender: we intercept calls to `<a href="https://developer.mozilla.org/en-US/docs/Web/API/MediaStream.addTrack" target="_blank">addTrack()</a>`

, create a `DTMFSender`

, swap out the original track with the new one containing the DTMF generator, and attach the `DTMFSender`

to the `RTCRTPSender`

object where it belongs.

You can demonstrate this by including the `DTMFSender`

object and then running through a basic local audio call:

```
/* Note: Requires Firefox 44 or later */
var pc1 = new RTCPeerConnection();
var pc2 = new RTCPeerConnection();
pc2.onaddtrack = function(e) {
var stream = new MediaStream([e.track]);
var audio = document.createElement("audio");
document.body.appendChild(audio);
audio.mozSrcObject = stream;
audio.play();
};
pc1.onicecandidate = function(e) {
if (e.candidate) {
pc2.addIceCandidate(e.candidate);
}
};
pc2.onicecandidate = function(e) {
if (e.candidate) {
pc1.addIceCandidate(e.candidate);
};
};
navigator.mediaDevices.getUserMedia({ audio: true })
.then(function(stream) {
var track = stream.getAudioTracks()[0];
var sender = pc1.addTrack(track, stream);
pc1.createOffer().then(function(offer) {
pc1.setLocalDescription(offer).then(function() {
pc2.setRemoteDescription(offer).then(function() {
pc2.createAnswer().then(function(answer) {
pc2.setLocalDescription(answer).then(function() {
pc1.setRemoteDescription(answer).then(function() {
sender.dtmf.ontonechange = function(e) {
console.log(JSON.stringify(e));
}
sender.dtmf.insertDTMF("2145551212,1");
});
});
});
});
});
});
});
```


If you’d like to be notified when platform work to implement RTCDTMFSender natively begins, add yourself to the CC list on [Bug 1012645](https://bugzilla.mozilla.org/show_bug.cgi?id=1012645). And we would love to hear from you in the comments about successes and challenges you encounter in applying the oscillator-based method we describe in this post, as well as any suggestions you might have for improving the example implementation.

Finally, here’s the source of the DTMFSender object:

```
/*
* DTMFSender.js
*
* This serves as a polyfill that adds a DTMF sender interface to the
* RTCRTPSender objects on RTCRTPPeerConnecions for Firefox 44 and later.
* Implementations simply include this file, and then use the DTMF sender
* as described in the WebRTC specification.
*
* For versions of Firefox prior to 44, implementations need to manually
* instantiate a version of the DTMFSender object, pass it a stream, and
* then retreive "outputStream" from the sender object. Implmentations
* may also choose to attach the sender to the corresponding RTCRTPSender,
* if they wish.
*
* This Source Code Form is subject to the terms of the Mozilla Public License,
* v. 2.0. If a copy of the MPL was not distributed with this file, You can
* obtain one at https://mozilla.org/MPL/2.0/.
*/
// The MediaStream enhancements we need to make a polyfill work landed
// at the same time as the "addTrack" method as added to MediaStream.
// If this is possible, we monkeypatch ourselves into RTCPeerConnection.addTrack
// so thatwe attach a new DTMF sender to each RTP Sender as they are created.
if ("addTrack" in MediaStream.prototype) {
RTCPeerConnection.prototype.origAddTrack =
RTCPeerConnection.prototype.addTrack;
RTCPeerConnection.prototype.addTrack = function(track, stream) {
var sender = this.origAddTrack(track, stream);
new DTMFSender(sender);
return(sender);
}
}
function DTMFSender(senderOrStream) {
var ctx = this._audioCtx = new AudioContext();
this._outputStreamNode = ctx.createMediaStreamDestination();
var outputStream = this._outputStreamNode.stream;
var inputStream;
var rtpSender = null;
if ("track" in senderOrStream) {
rtpSender = senderOrStream;
inputStream = new MediaStream([rtpSender.track]);
} else {
inputStream = senderOrStream;
this.outputStream = outputStream;
}
this._source = ctx.createMediaStreamSource(inputStream);
this._source.connect(this._outputStreamNode);
this._f1Oscillator = ctx.createOscillator();
this._f1Oscillator.connect(this._outputStreamNode);
this._f1Oscillator.frequency.value = 0;
this._f1Oscillator.start(0);
this._f2Oscillator = ctx.createOscillator();
this._f2Oscillator.connect(this._outputStreamNode);
this._f2Oscillator.frequency.value = 0;
this._f2Oscillator.start(0);
if (rtpSender) {
rtpSender.replaceTrack(outputStream.getAudioTracks()[0])
.then(function() {
rtpSender.dtmf = this;
}.bind(this));
}
}
/* Implements the same interface as RTCDTMFSender */
DTMFSender.prototype = {
ontonechange: undefined,
get duration() {
return this._duration;
},
get interToneGap() {
return this._interToneGap;
},
get toneBuffer() {
return this._toneBuffer;
},
insertDTMF: function(tones, duration, interToneGap) {
if (/[^0-9a-d#\*,]/i.test(tones)) {
throw(new Error("InvalidCharacterError"));
}
this._duration = Math.min(6000, Math.max(40, duration || 100));
this._interToneGap = Math.max(40, interToneGap || 70);
this._toneBuffer = tones;
if (!this._playing) {
setTimeout(this._playNextTone.bind(this), 0);
this._playing = true;
}
},
/* Private */
_duration: 100,
_interToneGap: 70,
_toneBuffer: "",
_f1Oscillator: null,
_f2Oscillator: null,
_playing: false,
_freq: {
"1": [ 1209, 697 ],
"2": [ 1336, 697 ],
"3": [ 1477, 697 ],
"a": [ 1633, 697 ],
"4": [ 1209, 770 ],
"5": [ 1336, 770 ],
"6": [ 1477, 770 ],
"b": [ 1633, 770 ],
"7": [ 1209, 852 ],
"8": [ 1336, 852 ],
"9": [ 1477, 852 ],
"c": [ 1633, 852 ],
"*": [ 1209, 941 ],
"0": [ 1336, 941 ],
"#": [ 1477, 941 ],
"d": [ 1633, 941 ]
},
_playNextTone: function() {
if (this._toneBuffer.length == 0) {
this._playing = false;
this._f1Oscillator.frequency.value = 0;
this._f2Oscillator.frequency.value = 0;
if (this.ontonechange) {
this.ontonechange({tone: ""});
}
return;
}
var digit = this._toneBuffer.substr(0,1);
this._toneBuffer = this._toneBuffer.substr(1);
if (this.ontonechange) {
this.ontonechange({tone: digit});
}
if (digit == ',') {
setTimeout(this._playNextTone.bind(this), 2000);
return;
}
var f = this._freq[digit.toLowerCase()];
if (f) {
this._f1Oscillator.frequency.value = f[0];
this._f2Oscillator.frequency.value = f[1];
setTimeout(this._stopTone.bind(this), this._duration);
} else {
// This shouldn't happen. If it does, just move on.
setTimeout(this._playNextTone.bind(this), 0);
}
},
_stopTone: function() {
this._f1Oscillator.frequency.value = 0;
this._f2Oscillator.frequency.value = 0;
setTimeout(this._playNextTone.bind(this), this._interToneGap);
}
};
```


## About
[
Adam Roach ](http://sporadicdispatches.blogspot.com/)

Adam Roach works as part of Mozilla's CTO organization on WebRTC and related technologies. He has been crafting the world of Real Time Communications over IP since 1997 by doing protocol standardization, architecture, design, and implementation.