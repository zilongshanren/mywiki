---
title: Hello Chrome, it's Firefox calling! – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/02/hello-chrome-its-firefox-calling/
author: Maire Reavy
published: '2013-02-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Mozilla is excited to announce that we’ve achieved a major milestone in WebRTC development: WebRTC RTCPeerConnection interoperability between Firefox and Chrome. This effort was made possible because of the close collaboration between the open Web community and engineers from both Mozilla and Google.

RTCPeerConnection (also known simply as PeerConnection or PC) interoperability means that developers can now create Firefox WebRTC applications that make direct audio/video calls to Chrome WebRTC applications without having to install a third-party plugin. Because the functionality is now baked into the browser, users can avoid problems with first-time installs and buggy plugins, and developers can deploy their apps much more easily and universally.

To help celebrate this momentous milestone, we thought it would be fun to [call up our friends at Google](https://www.youtube.com/embed/MsAWR_rJ5n8?rel=0) to discuss it with them. Check out this Firefox-Chrome demonstration call between Mozilla’s Chief Innovation Officer, Todd Simpson, and Google’s Director of Product Management, Hugh Finnan, and read what Google had to say about this momentous occasion in [their blog post](http://blog.chromium.org/2013/02/hello-firefox-this-is-chrome-calling.html).

This milestone builds on an earlier demo we showed late last year of [WebRTC integrated with Social API](https://blog.mozilla.org/futurereleases/2012/11/30/webrtc-makes-social-api-even-more-social/). There we demonstrated an industry first with our implementation of DataChannels, a powerful component of WebRTC that can combined with an audio/video chat to allow users to share almost anything on their computer or device. Send vacation photos, memorable videos, links news stories etc., simply by dragging the item into your video chat window. Look out for more on this to come.

The purpose of WebRTC, an open standard being defined jointly at the W3C and IETF standards organizations, is to provide a common platform for all user devices to communicate and share audio, video and data in real-time. This is a first step toward that vision of interoperability and true, open, real-time communication on the web.

Posted by:

Serge Lachapelle, Chrome Product Manager and Maire Reavy, Firefox Media Product Lead

## Start Developing Using RTCPeerConnection in Firefox

For JavaScript developers who haven’t tried RTCPeerConnection in Firefox yet (since it is a brand new feature for us), you can try this out using the most recent Firefox Nightly by setting the media.peerconnection.enabled pref to “true” (browse to about:config and search for the media.peerconnection.enabled pref in the list of prefs). Here is a snippet of code from [a sample app](https://github.com/jesup/nightly-gupshup) that shows off how to initiate, accept, and end a WebRTC call in Firefox using RTCPeerConnection:

```
function initiateCall(user) {
document.getElementById("main").style.display = "none";
document.getElementById("call").style.display = "block";
// Here's where you ask user permission to access the camera and microphone streams
navigator.mozGetUserMedia({video:true, audio:true}, function(stream) {
document.getElementById("localvideo").mozSrcObject = stream;
document.getElementById("localvideo").play();
document.getElementById("localvideo").muted = true;
// Here's where you set up a Firefox PeerConnection
var pc = new mozRTCPeerConnection();
pc.addStream(stream);
pc.onaddstream = function(obj) {
log("Got onaddstream of type " + obj.type);
document.getElementById("remotevideo").mozSrcObject = obj.stream;
document.getElementById("remotevideo").play();
document.getElementById("dialing").style.display = "none";
document.getElementById("hangup").style.display = "block";
};
pc.createOffer(function(offer) {
log("Created offer" + JSON.stringify(offer));
pc.setLocalDescription(offer, function() {
// Send offer to remote end.
log("setLocalDescription, sending to remote");
peerc = pc;
jQuery.post(
"offer", {
to: user,
from: document.getElementById("user").innerHTML,
offer: JSON.stringify(offer)
},
function() { console.log("Offer sent!"); }
).error(error);
}, error);
}, error);
}, error);
}
function acceptCall(offer) {
log("Incoming call with offer " + offer);
document.getElementById("main").style.display = "none";
document.getElementById("call").style.display = "block";
// Here's where you ask user permission to access the camera and microphone streams
navigator.mozGetUserMedia({video:true, audio:true}, function(stream) {
document.getElementById("localvideo").mozSrcObject = stream;
document.getElementById("localvideo").play();
document.getElementById("localvideo").muted = true;
// Here's where you set up a Firefox PeerConnection
var pc = new mozRTCPeerConnection();
pc.addStream(stream);
pc.onaddstream = function(obj) {
document.getElementById("remotevideo").mozSrcObject = obj.stream;
document.getElementById("remotevideo").play();
document.getElementById("dialing").style.display = "none";
document.getElementById("hangup").style.display = "block";
};
pc.setRemoteDescription(JSON.parse(offer.offer), function() {
log("setRemoteDescription, creating answer");
pc.createAnswer(function(answer) {
pc.setLocalDescription(answer, function() {
// Send answer to remote end.
log("created Answer and setLocalDescription " + JSON.stringify(answer));
peerc = pc;
jQuery.post(
"answer", {
to: offer.from,
from: offer.to,
answer: JSON.stringify(answer)
},
function() { console.log("Answer sent!"); }
).error(error);
}, error);
}, error);
}, error);
}, error);
}
function endCall() {
log("Ending call");
document.getElementById("call").style.display = "none";
document.getElementById("main").style.display = "block";
document.getElementById("localvideo").mozSrcObject.stop();
document.getElementById("localvideo").mozSrcObject = null;
document.getElementById("remotevideo").mozSrcObject = null;
peerc.close();
peerc = null;
}
```

You’ll notice that Firefox still prefixes the RTCPeerConnection API call as mozRTCPeerConnection because the standards committee is not yet done defining it. Chrome prefixes it as webkitRTCPeerConnection. Once the standards committee finishes its work, we will remove the prefixes and use the same API, but in the meantime, you’ll want to support both prefixes so that your app works in both browsers.

## Trying Interop Yourself

For those eager to give interop a try, [here are instructions and information about “trying this at home”](http://www.webrtc.org/demo).

This is Firefox’s and Chrome’s first version of PeerConnection interoperability. As with most early releases, there are still bugs to fix, and interop isn’t supported yet in every network environment. But this is a major step forward for this new web feature and for the Web itself. We thank the standards groups and every contributor to the WebRTC community. While there’s more work to do, we hope you’ll agree that the Web is about to get a lot more awesome.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 128 comments

MarkoFebruary 4th, 2013 at 12:40Robert Nyman [Editor]February 4th, 2013 at 13:59js audio apiFebruary 4th, 2013 at 13:44Robert Nyman [Editor]February 4th, 2013 at 14:05Matt MontagFebruary 5th, 2013 at 01:06Robert Nyman [Editor]February 5th, 2013 at 01:24Ali HelmyFebruary 4th, 2013 at 14:20Robert Nyman [Editor]February 4th, 2013 at 14:32Tin Aung LinnFebruary 5th, 2013 at 04:27SyFebruary 4th, 2013 at 14:54Robert Nyman [Editor]February 4th, 2013 at 15:08MichaelFebruary 5th, 2013 at 21:48Robert Nyman [Editor]February 6th, 2013 at 03:22Phil HannentFebruary 6th, 2013 at 06:24Robert Nyman [Editor]February 6th, 2013 at 07:20timrpetersonFebruary 4th, 2013 at 15:12Robert Nyman [Editor]February 4th, 2013 at 15:17Joe EkineFebruary 4th, 2013 at 15:19Robert Nyman [Editor]February 4th, 2013 at 15:21VenkyFebruary 4th, 2013 at 15:29Robert Nyman [Editor]February 5th, 2013 at 01:09r.kofmanMarch 10th, 2013 at 13:13Maire ReavyFebruary 5th, 2013 at 12:03Abel LuclFebruary 6th, 2013 at 03:02Andrew HimeFebruary 4th, 2013 at 15:34AntiHimeFebruary 4th, 2013 at 16:13Andrew HimeFebruary 5th, 2013 at 01:04tom jonesFebruary 4th, 2013 at 20:17tom jonesFebruary 4th, 2013 at 20:22Andrew HimeFebruary 4th, 2013 at 21:45Andrew HimeFebruary 4th, 2013 at 21:44Robert Nyman [Editor]February 5th, 2013 at 01:14Andrew HimeFebruary 5th, 2013 at 01:30Robert Nyman [Editor]February 5th, 2013 at 01:46Andrew HimeFebruary 5th, 2013 at 04:20Robert Nyman [Editor]February 5th, 2013 at 04:31AlFebruary 5th, 2013 at 01:42Robert Nyman [Editor]February 5th, 2013 at 01:53bryanFebruary 4th, 2013 at 15:53Robert Nyman [Editor]February 5th, 2013 at 01:00Maire ReavyFebruary 5th, 2013 at 12:33bryanFebruary 15th, 2013 at 16:05markFebruary 27th, 2013 at 07:27HandrusFebruary 4th, 2013 at 16:01Robert Nyman [Editor]February 5th, 2013 at 01:00ClementFebruary 4th, 2013 at 16:10Robert Nyman [Editor]February 5th, 2013 at 00:59njnFebruary 4th, 2013 at 18:04bjFebruary 4th, 2013 at 19:24dudeFebruary 4th, 2013 at 20:57CraigFebruary 4th, 2013 at 21:35PlutoFebruary 4th, 2013 at 23:03Robert Nyman [Editor]February 5th, 2013 at 01:17MosselmanFebruary 5th, 2013 at 02:14Florent TatardFebruary 4th, 2013 at 19:43Robert Nyman [Editor]February 5th, 2013 at 00:58genuineFebruary 4th, 2013 at 19:43Robert Nyman [Editor]February 5th, 2013 at 00:58AnentropicFebruary 5th, 2013 at 03:36rakshitFebruary 4th, 2013 at 23:27Robert Nyman [Editor]February 5th, 2013 at 00:56KontrolFebruary 5th, 2013 at 00:34Robert Nyman [Editor]February 5th, 2013 at 00:56Maire ReavyFebruary 5th, 2013 at 12:37BooderanFebruary 5th, 2013 at 00:47Robert Nyman [Editor]February 5th, 2013 at 00:55MaurizioFebruary 5th, 2013 at 01:49RobFebruary 5th, 2013 at 03:01Robert Nyman [Editor]February 5th, 2013 at 04:17Sourav ChakrabortyFebruary 5th, 2013 at 03:51Robert Nyman [Editor]February 5th, 2013 at 04:18Capi EtherielFebruary 5th, 2013 at 04:33Robert Nyman [Editor]February 5th, 2013 at 05:00Peeyush ChandelFebruary 5th, 2013 at 05:08Robert Nyman [Editor]February 5th, 2013 at 07:18Sam DuttonFebruary 5th, 2013 at 05:16Robert Nyman [Editor]February 5th, 2013 at 07:18Simon GriffeeFebruary 5th, 2013 at 07:18Robert Nyman [Editor]February 5th, 2013 at 07:20CrazyManFebruary 5th, 2013 at 07:27Robert Nyman [Editor]February 5th, 2013 at 13:05christian westmanFebruary 5th, 2013 at 07:39Robert Nyman [Editor]February 5th, 2013 at 13:03Andrius KairiukstisFebruary 5th, 2013 at 07:49Robert Nyman [Editor]February 5th, 2013 at 13:03Afshin MehrabaniFebruary 5th, 2013 at 08:15Robert Nyman [Editor]February 5th, 2013 at 13:05Stephan BardubitzkiFebruary 5th, 2013 at 10:09Robert Nyman [Editor]February 5th, 2013 at 13:06Martin ZatrochFebruary 5th, 2013 at 12:17Robert Nyman [Editor]February 5th, 2013 at 13:11Rahul patulaFebruary 5th, 2013 at 12:53Robert Nyman [Editor]February 5th, 2013 at 13:12Robert KaiserFebruary 5th, 2013 at 13:38Robert Nyman [Editor]February 5th, 2013 at 13:47InfinityFebruary 5th, 2013 at 15:09Robert Nyman [Editor]February 6th, 2013 at 03:16BUGHUNTERFebruary 6th, 2013 at 03:37Robert Nyman [Editor]February 6th, 2013 at 03:57Sam DuttonFebruary 6th, 2013 at 04:34Robert Nyman [Editor]February 6th, 2013 at 07:14Richard norburnFebruary 6th, 2013 at 04:42Robert Nyman [Editor]February 6th, 2013 at 07:17EdgarFebruary 6th, 2013 at 07:30Robert Nyman [Editor]February 7th, 2013 at 02:17maxw3stFebruary 6th, 2013 at 15:13Robert Nyman [Editor]February 7th, 2013 at 02:19EthanFebruary 6th, 2013 at 20:32Robert Nyman [Editor]February 7th, 2013 at 02:16HrishiFebruary 8th, 2013 at 13:18Robert Nyman [Editor]February 12th, 2013 at 03:31VPXFebruary 8th, 2013 at 14:11Robert Nyman [Editor]February 12th, 2013 at 03:31QFebruary 8th, 2013 at 14:37Robert Nyman [Editor]February 12th, 2013 at 03:30Leon VictorFebruary 11th, 2013 at 01:00Robert Nyman [Editor]February 12th, 2013 at 03:23Vikram LeleFebruary 13th, 2013 at 13:50Robert Nyman [Editor]February 14th, 2013 at 05:44Maire ReavyFebruary 27th, 2013 at 07:42Vikram LeleFebruary 27th, 2013 at 19:15johnFebruary 26th, 2013 at 10:58Robert Nyman [Editor]February 26th, 2013 at 16:48chenlin zhongMarch 6th, 2013 at 03:32Robert Nyman [Editor]March 6th, 2013 at 03:37FabianMarch 15th, 2013 at 11:28FabianMarch 20th, 2013 at 02:35Robert Nyman [Editor]March 20th, 2013 at 06:07