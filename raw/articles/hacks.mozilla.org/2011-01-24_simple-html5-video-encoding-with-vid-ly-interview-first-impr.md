---
title: Simple HTML5 video encoding with vid.ly – interview, first impressions and
  invite code – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/01/simple-html5-video-encoding-with-vid-ly-interview-first-impressions-and-invite-code/
author: Chris Heilmann
published: '2011-01-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Today encoding.com released a new service called [vid.ly](http://vid.ly) which is not yet another URL shortener, but actually a very impressive service for converting video.

One of the biggest annoyance of using HTML5 video is to convert your movie to various formats supported by different browsers. Vid.ly does this job for you: it converts the video you upload into 14 different formats for different browsers and, more importantly, devices. The interface is very intuitive and you can stand by and watch the conversion happen or simply let it run whilst you go offline or do other things. Once the service finished creating the different formats for you, you get an email. You then can visit the vid.ly URL on different devices and you get the video in the correct format.

## Interview with Jeff Malkin about vid.ly

To learn more about the service, I got Jeff Malkin, president of Encoding.com on the phone and asked him a few things about the service. You can [listen to the interview](http://www.archive.org/download/InterviewWithJeffMalkinOfEncoding.comAboutVid.ly/InterviewWithJeffMalkinAboutVid.ly.mp3):

In the interview Jeff answered a few questions and explained a few of my concerns:

- Vid.ly uses the same cloud backend as encoding.com, consisting of Amazon’s EC2 and S3 services and fallbacks
- The conversion happens with ffmpeg and a few other, commercial products as vid.ly also creates a high quality FLV for you
- The videos are tested on the real devices and they are also using services that give them access to more exotic physical devices on demand
- In addition to simply converting the videos to MP4 and Ogg (which can be done using
[Archive.org](http://archive.org)), vid.ly also creates iOS versions that support adaptive streaming and webm versions. - There is no API to make part of a build process in the free version but they are working on a pro version that will allow you to batch process videos and have more granular access to the encoding parameters
- Right now, you can’t send the converted videos back to a hosting platform of your own choice but this is also in the making.

## First impressions

When trying out the service with a video, I was very impressed with the interface. After entering your code you get a video URL. Pressing start asks you for an email (to notify you once the conversion is done) and offers you an interface to upload your video, either from FTP, HTTP, S3 or your hard drive. A log on the page tells you at any time what is happening:

The whole page is a progress bar. Once you uploaded the video the progress starts from left to right and tells you in the log box what is going on. You can stand by or close the page – vid.ly emails you once the conversion is done.

## Under the hood

Once the conversion is done, you get the email with your URL and you can try it on different devices. I checked it on my Nexus One and my iPod and got working videos on each without any redirect, ad display or other annoyances.

The embed code vid.ly sends you can be improved a bit but was built for ease of use:

Instead of linking the different sources, vid.ly adds a JavaScript that re-writes the source accordingly. If you check [the script](http://m.vid.ly/js/html5.js) you see that it includes the [VideoJS player by Zencoder](https://github.com/zencoder/video-js) and that there is a lot of detection going on – both using the HTML5 Video API and browser sniffing for Quicktime support or to fall back to Flash.

This seems a bit overkill and could be improved. The other annoyance are IDs on the video and script as that prevents you from using several vid.ly videos in the same document. But then again, the power of open tech is that you can work around that:

The email is that it tells you that there is a high quality FLV file created for you at `http://vidly.s3.amazonaws.com/{ID}/flv.flv`

. This means that your videos are stored in Amazon’s S3 with a bucket with the ID of your video. If you rename the `flv.flv`

to `ogv.ogv`

, `webm.webm`

and `mp4/mp4`

accordingly you use these URLs to create your own video embed without JavaScript or you can download the different versions.

## Try it out yourself

You can try vid.ly yourself using the **HNY2011** code. What do you think?

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 6 comments

Chris WilliamsJanuary 24th, 2011 at 13:42Leon MatthewsJanuary 24th, 2011 at 15:38Jeff MalkinJanuary 24th, 2011 at 18:18Darren ArmstrongJanuary 25th, 2011 at 03:18c0d3rFebruary 11th, 2011 at 12:51sliminexJanuary 25th, 2013 at 12:22