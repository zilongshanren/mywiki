---
title: PeerSquared – one-on-one online teaching with WebRTC – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2013/07/peersquared-one-on-one-online-teaching-with-webrtc/
author: Fabian Gort
published: '2013-07-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

It was somewhere in the midst of 2010 when I first learned that the people at Ericson Labs were working on an [‘open standards’ browser implementation](http://labs.ericsson.com/blog/beyond-html5---full-duplex-conversational-voice-and-video-in-browsers-and-web-runtimes) for P2P video chat. I was excited right away. The fact that you could only use video chat in your web browser through Flash or other plug-ins bothered me. Webcams had already been around for quite a few years, but their use was mainly limited to proprietary programs like MSN Messenger and Skype.

We’re now three years later and it is all going to change. Just a couple of days ago P2P video chat made it to the Final Release of Firefox 22. That means, with Google Chrome already supporting this technology shortly, there are over a billion people now able to use native webcam chat in their browser. I think that is truly awesome and that it will probably cause a new big wave of change on the Internet. Imagine in just a few years from now that the old trusty telephone line will be obsolete and we will all be making browser based video calls.

## PeerSquared

After reading about Google Chrome and Firefox adding data channels to P2P connections I was getting even happier, since it offers loads of new possibilities. I am very interested in e-learning and so I got the idea to build a whiteboard system for online tutoring, called [PeerSquared](http://www.peersquared.info).

The current version is a **proof of concept**, to see for myself what is really possible with the PeerConnection API and data channels in particular. To use PeerSquared simply log in on two different screens as a teacher and student respectively but using the same and **unique** room name. After logging in on both screens the P2P connection is established and the teacher is able to become creative with the whiteboard.

Actions performed by the teacher, like painting, writing and creating shapes, are also instantly visible on the student’s whiteboard, making it some sort of screen sharing. Most functions are self-explanatory but a less obvious feature is the ability to drop images from your file system onto the whiteboard to show them to the student, as you can see in the picture below (the earth and moon are drawn as dataURL images onto the canvas, which itself has an image of the universe as a background).

*Note: PeerSquared does not work in Google Chrome yet, because it doesn’t have reliable data channels implemented at the moment*

## Progressively uploading data

All data messages sent through a data channel are nicely queued. This means when for example the teacher sends a big image to the student and just after that he draws a line (which is a small amount of data to send), there is no risk that the student receives the line data first. In addition, they are also suitable for uploading larger data chunks. I have uploaded pictures up to 6MB to the student’s whiteboard canvas, without any problem.

However, for larger data it’s nice to be able to see the upload progress. So that made me wonder whether it would be possible for the teacher to reliably send data in chunks to the student. This appeared to be really simple. All that is required is reading a file into an ArrayBuffer, slice it with the [slice method](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Typed_arrays/ArrayBuffer), and then send the chunks through the data channel:


<pre lang="javascript">

// after obtaining an 'arrayBuffer' from a FileReader:

var chunkSize = 1000, byteLength = arrayBuffer.byteLength;

for(i = 0; i < byteLength; i = i + chunkSize) {

dataChannel.send(arrayBuffer.slice(i, i + chunkSize));

}

</pre>


Of course it is also necessary to send meta information such as file name, size and type, in order to create a download link on the student’s side, but it’s easy to do so. Just send the array buffer data raw and the file meta data as a stringified JSON object. Then on the student’s side in the `onmessage`

event handler you can differentiate between the two:


<pre lang="javascript">

/*

1. The teacher sends meta information, for example: JSON.stringify({status : 'start', name: 'image.jpg', type: 'image/jpg', chunkCount : 20});

2. The teacher sends the file chunks, see code above

3. After the last chunk the teacher sends a message that the upload is complete, for example: JSON.stringify({status : 'complete'});

*/

var arrayBufferChunks = [], blob = null, meta = {}, container = document.getElementById('some_div');

dataChannel.onmessage = function(evt) {

var data = evt.data;

if(typeof data == 'object') {

// step 2: put the chunks together again

arrayBufferChunks.push();

// note: arrayBufferChunks.length / meta.chunkCount would be a measure for the progress status

}

else if(typeof data == 'string') {

data = JSON.parse(data);

if(data.status == 'start') {

// step 1: store the meta data temporarily

meta = data;

}

else if(data.status == 'complete') {

// step 3: create an object URL for a download link

blob = new Blob(arrayBufferChunks, { "type" : meta.type });

container.innerHTML = '<a href="' + URL.createObjectURL(blob) + '" download="' + meta.name + '">' + meta.name + '</a> is completed

}

}

}

</pre>


Like this I have been able to upload multiple files in a row and with a size over 200 MB. With even bigger files the browser starts taking up loads of memory and may become frozen (This seems to be due to reading the file though, not the sending). Another issue was that when adding 8+ files from the file picker I sometimes experienced a browser crash. This may have been the consequence of instantiating independent data channels on the fly for each file being read, so it’s worth trying to queue all files just in one data channel.

I’ve also noted a few times that a file upload froze. This could simply be due to a hampering Internet connection. It’s nice to know then that it shouldn’t be too hard to make the progressive downloads resumable as well. As long as the receiver keeps track of the last received data chunk, he can just send a message back to the sender after a paused or interrupted upload: ‘please send me file X but starting from chunk Y’. And there you have a quite sophisticated P2P file sharing tool made simple.

You can try the progressive file upload in PeerSquared by selecting one of more files on your system and drag them to the chat input box on the teacher’s side, like in this screenshot:

![](../../assets/ac330c94d0083f1f.png)


## Adding to and removing from a PeerConnection

Currently a drawback of the PeerConnection object in Firefox is that it isn’t possible (yet) to just add and remove multiple data channels and video streams to a single PeerConnection object, because every addition/removal requires to renegotiate a session. From [http://www.w3.org/TR/webrtc/](http://www.w3.org/TR/webrtc/):

In particular, if a RTCPeerConnection object is consuming a MediaStream and a track is added to one of the stream’s MediaStreamTrackList objects, by, e.g., the add() method being invoked, the RTCPeerConnection object must fire the

`negotiationneeded`

event. Removal of media components must also trigger`negotiationneeded`

.

The `negotiationneeded`

event hasn’t arrived yet. As a bypass in PeerSquared I am using several independent `PeercConnection`

objects: one for all the data channels together and one per video stream. That way it works fine.

## The next step in P2P sharing

I believe PeerSquared’s whiteboard and webcam are great tools together for online one-on-one teaching and there are plenty of options to build more interaction on top of the whiteboard. However sometimes it is desirable to share video or even the whole desktop. How can that be done? One way to that is to use a virtual webcam driver like [manycam](http://www.manycam.com/) which is able to capture streams from a video or your desktop to your webcam. The drawback is that you are depending on external proprietary software again.

Since version 26, Google Chrome experimentally allows `getUserMedia()`

access to the screen and share it through a peer connection, as you can test in [WebRTC Plugin-free Screen Sharing](https://webrtc-experiment.appspot.com/Pluginfree-Screen-Sharing/#2229MJX8-BRB). I’m not sure if or when this will become a web standard though. The last option I can think of, and which only captures the current tab content, is using a library like [html2canvas](http://html2canvas.hertzen.com/). I have not tried this myself yet, and I wonder if it will be fast and reliable enough for a good ‘tab share experience’.

## In conclusion

There have already been some great demonstrations of [online multiplayer gaming](https://hacks.mozilla.org/2013/03/webrtc-data-channels-for-great-multiplayer/) and [video](https://hacks.mozilla.org/2013/03/making-webrtc-simple-with-conversat-io/) [conferencing](https://hacks.mozilla.org/2013/05/embedding-webrtc-video-chat-right-into-your-website/) with HTML5 on Mozilla Hacks. I hope that in addition my PeerSquared demo will give you a good a idea of some awesome possibilities for online collaboration and teaching with it and inspires you to go P2P. Any questions or suggestions? Please don’t hesitate to [contact](http://peersquared.info/contact.php) me.

## About Fabian Gort

Fabian Gort is currently an independent interpreneur living in Amsterdam and the maker of PeerSquared. As a biology student he was already developing educational software for a Dutch university in 2001. Since then he has been involved in several web based projects for NGO's and the university.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 12 comments

shavounetJuly 4th, 2013 at 08:23shavounetJuly 4th, 2013 at 08:45Robert Nyman [Editor]July 4th, 2013 at 09:12DanielJuly 4th, 2013 at 09:55Fabian GortJuly 4th, 2013 at 10:46DanielJuly 4th, 2013 at 14:18FabianJuly 5th, 2013 at 00:26JeroenJuly 4th, 2013 at 15:09Brett ZamirJuly 4th, 2013 at 20:45FabianJuly 5th, 2013 at 00:29vrobbiJuly 10th, 2013 at 21:17Mathew PorterJuly 24th, 2013 at 09:49