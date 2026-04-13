---
title: Making the Dino roar – syncing audio and CSS transitions – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2012/03/making-the-dino-roar-syncing-audio-and-css-transitions/
author: Chris Heilmann
published: '2012-03-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

It started with Brian King [setting up our Google+ page](https://plus.google.com/113905062081031761430/posts) using [this round MDN logo by John Slater](http://www.flickr.com/photos/intothefuzz/4402972804/in/photostream/). I thought this looks cool and reminded me of the famous [MGM intro](http://www.youtube.com/watch?v=LRnVotTOPjE) so I wondered if I could turn it into an intro for our video tutorials (not sure if we will do that though). And, some photoshop and sound work later and with a sprinkle of HTML5 audio and CSS transitions, [here we are](http://thewebrocks.com/demos/mdnmgm/) ([source on GitHub](https://github.com/codepo8/mdnmgm)):

I started with the sound. If you need Creative Commons licensed sounds, [Freesound](http://freesound.org) is a good resource. So I took [Chinese Fanfare by Nick-Nack](http://www.freesound.org/people/Nick-Nac/sounds/108248/) and [Roar by CGEffex](http://www.freesound.org/people/CGEffex/sounds/98337/) and put them together in [Audacity](http://audacity.sourceforge.net/).

Saving them as OGG and MP3 gave me an audio element that I could tie into. All I needed was to listen to the `timeupdate`

event and compare the `currentTime`

to trigger the animations. The animations (rotation of the dino and opening and closing of the jaw) are CSS transitions triggered by classes on the parent element. The main trick was to store both the dino and the jaw inside a div and transition them separately. The jaw animation also needed a change in transformation origin as we don’t rotate the image around its center.

If you got seven minutes to spare, here is a blow-by-blow screencast explaining what is going on:

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 7 comments

MardegMarch 20th, 2012 at 09:13JakobMarch 20th, 2012 at 10:42JakobMarch 20th, 2012 at 11:33Chris HeilmannMarch 20th, 2012 at 12:06Josh MatthewsMarch 20th, 2012 at 11:20Caspy7March 21st, 2012 at 14:43SayaKNovember 24th, 2012 at 00:34