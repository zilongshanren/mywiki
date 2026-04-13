---
title: Embedding WebRTC Video Chat Right Into Your Website – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2013/05/embedding-webrtc-video-chat-right-into-your-website/
author: Dmitry Dragilev
published: '2013-05-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/3dac0f9a76446eed.png)


Most of you remember the [Hello Chrome, it’s Firefox calling!](https://hacks.mozilla.org/2013/02/hello-chrome-its-firefox-calling/) blog post right here in Mozilla Hacks demonstrating WebRTC video chat between Firefox and Chrome. It raised a lot of attention. Since then we here at Fresh Tilled Soil have seen a tremendous amount of startups and companies which have sprung up building products based WebRTC video chat technology. Tsashi Levent-Levi who is a WebRTC evangelist has been interviewing most of these companies on his blog, the list is [quite impressive](http://bloggeek.me/webrtc-interviews/)!

## WebRTC chat demo

Much like most of early adopters we have been playing around with WebRTC for quite awhile now. We have of course created [our own WebRTC video chat demo](http://freshtilledsoil.com/the-future-of-web/webrtc-video/) and have also very recently released WebRTC video chat widgets.

The widgets work very simply, anybody can take the following HTML embed code:

```
```

and add this code to any website or blog post. You’ll see the following widget on their website:

![](../../assets/d966a296223af5bd.png)


From here it’s dead simple to start a WebRTC video chat, just make up a name for a room, type it in and click start chat. Tell the other person to do the same and you’re all set.

As always make sure you’re giving this a try in [Firefox Nightly](http://nightly.mozilla.org/) or the latest stable build of [Google Chrome](https://www.google.com/intl/en/chrome/browser/). If you are on a tablet make sure you are on Google Chrome beta if you are using the Google Chrome browser.

Something else to note is that for this first version our video chat is limited to just two participants per a room. If a room name is occupied by two people the third person who tries to connect to this room simply won’t be able to connect.

## How It Works

Without getting too deep into the code behind how WebRTC video chat actually works, let’s briefly go over what is actually happening behind the scenes when you click the start chat button and how WebRTC video chat actually works. Here is a step by step timeline of what actually happens to give you a better idea:

A quick note about this step: “Once remote media starts streaming stop adding ICE candidates” – this is a temporary solution which might result in suboptimal media routing for many network topologies. It should only be used until Chrome’s ICE support is fixed.

A quick and very important tip to remember when you are trying to get this to work. We used a ‘polyfill’ like technique as shown [in this article by Remy Sharp.](http://remysharp.com/2010/10/08/what-is-a-polyfill/) As Remy describes we wrote a piece of code to adapt for the Firefox syntax to get cross-browser functionality.

## Issues We Ran Into and How We Solved Them

As you might expect we ran into a number of problems and issues trying to build this. WebRTC is evolving quickly so we are working through a number of issues every day. Below are just some of the problems we ran into and how we solved them.

### PeerConnection capability in Google Chrome

While working with the new PeerConnection capability in Chrome we discovered a strict order of operation for it to work; more specifically:

- Peers must be present with local streaming video before sending SIP (offer/answer SDP)
- For ‘Answerer’; Do not add ICE candidate until the peer generates the ‘Answer SDP’
- Once remote media starts streaming stop adding ICE candidates
- Never create peer connect for answerer until you get the ‘Offer SDP’

We fixed it by handling those issues and handling the connection in the order described above. This was crucial to making the connection work flawlessly. Before we did that it would work only every once in a while.

### Added latency due to lag

When streaming to a mobile device there is added latency due to lag and limitations of surfing the net via mobile phone.

We solved this by making the resolution of streamed video reduced via a hash tag at the end of the URL. URL can optionally contain `'#res=low'`

for low resolution stream video & `'#res=hd'`

for HiDefinition streaming video as an optional URL parameter. A quick note here that other configurable properties are now available such as frames per second which you can use for this same purpose.

### Recording the WebRTC demo

We’ve been dabbling with recording video WebRTC demo. When recording video we used the new JavaScript type arrays to save the streaming data. We quickly discovered that it is only possible to record the video and audio separately.

We solved this by creating two instances of recording, one for the audio and one for the video, that utilized the new javascript data types and recorded both streams simultaneously.

## Conclusion

It’s exciting to dabble in this stuff, we love WebRTC so much that we created an entire [page dedicated to our experiments](http://freshtilledsoil.com/the-future-of-web/) with this technology and others which we believe will transform the web in 2013. If you have any question please give us a shout.

## About
[
Dmitry Dragilev ](http://www.freshtilledsoil.com/)

Dmitry Dragilev is a Tech Evangelist at Fresh Tilled Soil, a team of designers, coders and UX experts that helps entrepreneurs and businesses create bloody brilliant user experiences for web and mobile applications through consulting, training, and events. Since 2005 they’ve helped 300+ clients including General Electric, Microsoft, MIT, Harvard, TEDx, Time Warner Cable, Walgreens, Hubspot among many others.

## About Paul Greenlea

Senior Front-End Developer & Strategist at Fresh Tilled Soil. Paul is an inventor. He's been tinkering with electronics and technology since he can remember. He started designing and programming at age 12 when he began creating his own computer games, and over the years he's led teams through strategy, concept, and execution phases in positions ranging from UI designer to lead engineer. He currently follows the rapidly evolving industry of mobile closely and firmly believes it is the future.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 26 comments

Emanuel HoogeveenMay 7th, 2013 at 07:40Adam RoachMay 7th, 2013 at 08:38Emanuel HoogeveenMay 7th, 2013 at 09:54LennieMay 8th, 2013 at 08:34Alexander FarkasMay 7th, 2013 at 14:21alexander farkasMay 7th, 2013 at 23:21Robert Nyman [Editor]May 8th, 2013 at 02:46Dmitry DragilevMay 8th, 2013 at 07:31Paul GreenleaMay 8th, 2013 at 19:36agilobMay 8th, 2013 at 03:17Paul GreenleaMay 8th, 2013 at 19:48agilobMay 9th, 2013 at 16:58Robert Nyman [Editor]May 9th, 2013 at 03:58FabianMay 8th, 2013 at 04:17FabianMay 9th, 2013 at 01:07Robert Nyman [Editor]May 9th, 2013 at 03:55Steve SoudersMay 8th, 2013 at 09:59Robert Nyman [Editor]May 9th, 2013 at 03:54RoyMay 8th, 2013 at 10:20xinzhou yeMay 8th, 2013 at 19:40ashMay 9th, 2013 at 06:08Dmitry DragilevMay 9th, 2013 at 07:34ashMay 9th, 2013 at 08:39Chauffagiste compétent Paris: dépannage chauffageMay 16th, 2013 at 11:17Dmitry DragilevMay 16th, 2013 at 14:10GozzinMay 25th, 2013 at 09:29