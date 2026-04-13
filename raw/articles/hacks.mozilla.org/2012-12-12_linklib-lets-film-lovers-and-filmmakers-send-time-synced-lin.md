---
title: Linklib – lets film lovers and filmmakers send time synced links from videos
  to phones – a WebFWD project – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/12/linklib-lets-film-lovers-and-filmmakers-send-time-synced-links-from-videos-to-phones/
author: Simon Klose
published: '2012-12-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Have you ever googled films and TV-shows while you watch them? Do you think Youtube’s popup annotations in the middle of a video are distracting?

Having shot a documentary about the Pirate Bay for 4 years I wanted to embed links directly into the film to give the audience more nuances in the complex and bizarre story about the Swedish file-sharing site. I constantly google videos I watch.

## What problem is Linklib solving?

[Linklib](http://linklib.org/) lets filmmakers, film fans, journalists and bloggers send time synched links from a full screen video directly to their audiences’ phones. Instead of googling an actor, fact checking an election video or feverishly trying to find the soundtrack to that TV-series, just pick up the phone and the information is right there.

When I stumbled over [popcorn.js](http://popcornjs.org/) in 2011 I realized the amazing potential of embedding time synched links into films, but I was still looking for a way to hide the hyperlinks from the fullscreen video.

So we built Linklib, a system that sends time synced links from streamed video to phones. That way you can read up on that actress, fact check that election video or follow that rapper on twitter while you’re watching the video. Without obtrusive annotations in the frame.

Linklib is a free and open library of time synced video commentary. Film directors, journalists and fan communities can add facts and comments to give films more depth and nuances. The system works just as well for feature films, documentaries, music videos, educational and commercical films. Linklib is an open source project that wants to tell better stories by using the open web.

## How it works

The basic components of Linklib’s system are a remote, usually a smartphone or a tablet, and a video viewer, typically a computer. The remote shows synchronized links from the video viewer and can send and receive events such as play, pause, forward and rewind. To sync the phone with the video we show a QR code that you can scan with your phone. At the moment our video viewer can show youtube, vimeo and html5 video streams.

A lobby server handles the communication between the remote and the video. The remote uses [socket.io](http://socket.io/) to communicate with the lobby server and is written in JavaScript.

For users to be able to add videos and create link feeds of their own we’ve built a web based authoring tool focused on simplicity. The tool is built using [Twitter bootstrap](http://twitter.github.com/bootstrap/) and [jQuery](http://jquery.com/). All links and account information are stored on a mysql database on Amazon AWS.

### Components

- Remote – shows synchronized links from the Video Viwer and can send receive events such as play, pause, forward and rewind.
- Video Viewer – Shows a youtube or vimeo stream.
- Lobby server – handles communication between Remote and Video Viewer
- Authoring Tool – Web based system that allows users to add videos and create link flows for them

### APIs and Libraries

- Remote uses socket.io to communicate with Lobby server and is written in JavaScript.
- Lobby server is based on
[node.js](http://nodejs.org/) - Video viewer uses popcorn.js to play videos
- All links and account information are store on a mysql database on Amazon AWS
- Authoring Tool uses Twitter bootstrap and jQuery

## Help us test out Linklib

Are you a filmmaker looking for a way to tie closer bonds to your audience? Or a Game of Thrones-fan looking for a way to fill your favorite episode with geeky references? Maybe you want to throw in a bunch of research that you couldn’t explain in your last conference video? Or you’re a fashion designer that wants to reveal the details of your catwalk? If you’re a film producer you could fill your youtube trailer with your characters’ social media and reviews, like the great documentary Indiegame: The Movie here beneath.

You can also add mashups and remixes to that banging new Outkast music video! And help activists worldwide spread information that doesn’t make the mainstream news! Linklib puts the web into videos without ruining the traditional viewing experience.

We just launched a beta and we’d love your feedback about bugs and features!

## About
[
Simon Klose ](http://www.tpbafk.tv/)

I'm a filmmaker from Sweden. After law school I decided to move to South Africa and start filming documentaries instead. I've also live and worked on and off in Japan. For the past four years I've been following the file sharing debate in a film about the Pirate Bay. The film will premiere early 2013.

## 2 comments

GeorgeJanuary 26th, 2013 at 11:31Robert Nyman [Editor]January 28th, 2013 at 08:58