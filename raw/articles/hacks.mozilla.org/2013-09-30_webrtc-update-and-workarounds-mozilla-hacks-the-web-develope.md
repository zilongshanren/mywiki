---
title: 'WebRTC: Update and Workarounds – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2013/09/webrtc-update-and-workarounds/
author: Adam Roach
published: '2013-09-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As you’ve probably noticed, [we’ve been making lots of progress on our WebRTC implementation](https://hacks.mozilla.org/2013/09/firefox-24-for-android-gets-webrtc-support-by-default/), and we expect additional improvements over the next few releases.

We have work in the pipeline to improve audio quality issues ([yes, we know we still have some!](https://wiki.mozilla.org/Media/WebRTC_Audio_Issues)) and to assist with troubleshooting NAT traversal issues (you can follow the progress in [Bug 904622](https://bugzilla.mozilla.org/show_bug.cgi?id=904622)).

## Existing limitations

But beyond these upcoming improvements, I’d like to take a moment to look at a couple of our existing limitations that you might have noticed, and offer some advice for writing apps that work within these limitations.

The first issue, described in [Bug 857115](https://bugzilla.mozilla.org/show_bug.cgi?id=857115), is that mozRTCPeerConnection does not currently support renegotiation of an ongoing session. Once a session is set up, its parameters are fixed. In all practicality, this means that you can’t, for example, start an audio-only call and then add video to that same PeerConnection later in that session. We have another similar limitation in that we don’t currently support more than one each audio and video stream on a single PeerConnection (see [Bug 784517](https://bugzilla.mozilla.org/show_bug.cgi?id=784517) and [Bug 907339](https://bugzilla.mozilla.org/show_bug.cgi?id=907339)).

## Solutions for now

We’re going to fix these limitations as soon as we can, but it’s going to take a few months for our code changes to ride the Firefox train out into release. Until that happens, I want to give you a couple of workarounds so you can continue to use Firefox to make awesome things.

### Muting audio and video streams

Media renegotiation has two main use cases: muting and unmuting media in the middle of a session; and adding/removing video in the middle of a session. For muting and unmuting, the trick is to make judicious use of the “enabled” attribute on the MediaStreamTrack object: simply set a track’s enabled to “false” when you want to mute it.

```
var pc = new mozRTCPeerConnection;
navigator.mozGetUserMedia({video: true},
function (mediaStream) {
// Create a new self-view video element
var video = document.createElement("video");
video.setAttribute("width", 640);
video.setAttribute("height", 480);
video.setAttribute("style", "transform: scaleX(-1)");
video.src = window.URL.createObjectURL(mediaStream);
document.body.appendChild(video);
video.play();
// Add a button to hold/unhold video stream
var button = document.createElement("button");
button.appendChild(document.createTextNode("Toggle Hold"));
button.onclick = function(){
mediaStream.getVideoTracks()[0].enabled =
!(mediaStream.getVideoTracks()[0].enabled);
}
document.body.appendChild(document.createElement("br"));
document.body.appendChild(button);
// Add the mediaStream to the peer connection
pc.addStream(mediaStream);
// At this point, you're ready to start the call with
// pc.setRemoteDescription() or pc.createOffer()
},
function (err) { alert(err); }
);
```

Note that setting a MediaStreamTrack’s “enabled” attribute to “false” will not stop media from flowing, but it will change the media that’s being encoded into a black square (for video) and silence (for audio), both of which compress very well. Depending on your application, it may also make sense to use browser-to-browser signaling (for example, WebSockets or DataChannels) to let the other browser know that it should hide or show the video window when the corresponding video is muted.

### Adding video mid-call

For adding video mid-call, the most user-friendly work-around is to destroy the audio-only PeerConnection, and create a new PeerConnection, with both audio and video. When you do this, it will prompt the user for both the camera and the microphone; but, since Firefox does this in a single dialog, the user experience is generally pretty good. Once video has been added, you can either remove it by performing this trick in reverse (thus releasing the camera), or you can simply perform the “mute video” trick I describe above (which will leave the camera going — this might upset some users).

### Send more than one audio or video stream

To send more than one audio or video stream, you can use multiple simultaneous peer connections between the browsers: one for each audio/video pair you wish to send. You can also use this technique as an alternate approach for adding and removing video mid-session: set up an initial audio-only call; and, if the user later decides to add video, you can create a new PeerConnection and negotiate a separate video-only connection.

One subtle downside to using the first approach for adding video is that it restarts the audio connection when you add video, which may lead to some noticeable glitches in the audio stream. However, once we have audio and video synchronization landed, making sure that audio and video tracks are in the same MediaStream will ensure that they remain in sync. This synchronization isn’t guaranteed for multiple MediaStreams or multiple PeerConnections.

## Temporary workarounds and getting there

We recognize that these workarounds aren’t ideal, and we’re working towards spec compliance as quickly as we can. In the meanwhile, we hope that this information proves helpful in building out applications today. The good news is that these techniques should continue to work even after we’ve addressed the limitations described above, so you can migrate to a final solution at your leisure.

Finally, I would suggest that anyone interested in renegotiation and/or multiple media streams keep a eye on the bugs I mention above. Once we’ve implemented these features, they should appear in the released version of Firefox within about 18 weeks. After that happens, you’ll want to switch over to the “standard” way of doing things to ensure the best possible audio and video quality.

Thanks for your patience. Go out and make great things!

## About
[
Adam Roach ](http://sporadicdispatches.blogspot.com/)

Adam Roach works with Mozilla's WebRTC implementation team putting real-time technologies into the core library shared by Firefox and FirefoxOS. He has been crafting the world of Real Time Communications over IP since 1997 by doing protocol standardization, architecture, design, and implementation.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 9 comments

Kyle SimpsonSeptember 30th, 2013 at 05:23Randell JesupSeptember 30th, 2013 at 08:10pirannaSeptember 30th, 2013 at 15:15Robert Nyman [Editor]October 2nd, 2013 at 10:11Randell JesupOctober 2nd, 2013 at 10:31Fabian GortOctober 1st, 2013 at 07:00Adam RoachOctober 2nd, 2013 at 09:30Fabian GortOctober 2nd, 2013 at 13:14Fabian GortOctober 2nd, 2013 at 13:19