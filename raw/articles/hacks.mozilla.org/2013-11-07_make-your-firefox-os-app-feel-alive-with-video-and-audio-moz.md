---
title: Make your Firefox OS app feel alive with video and audio – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2013/11/make-your-firefox-os-app-feel-alive-with-video-and-audio/
author: Frédéric Harper
published: '2013-11-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox OS applications aren’t just about text: there is no better way to make your app feel alive than adding some videos or audio to it. Let’s explore different ways we can use as developers to enhance our mobile masterpiece.

## Audio and video HTML tags

Since we are talking about HTML, it makes total sense to think about using the `<audio>`

, and `<video>`

tag to play those media in your Firefox OS app. If you want to add a video in your application, just use this code.

```
```

In this code example, the user will see a video player with controls, and will have the opportunity to start the video. If your application is running in a browser not supporting the `video`

tag, the user will see the text between the tag. It’s still a good practice to do so, even if your primary target is a Firefox OS app, because since it uses HTML5, someone may access it from another browser if it’s a hosted app. Note that you can use other [attributes](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video) for this element.

As for the audio tag, it’s basically the same.

```
```

In this example, the audio will start automatically, and will play the audio file, in a loop, from the relative path: it’s perfect for background music if you are building a game. Note that you can add other [attributes](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio) to this element too.

Of course, using those elements without JavaScript give you basic features, but no worries, you can programmatically control them with code. Once you have your HTML element, like the `audio`

example you just saw, you can use JavaScript to play, pause, change the volume, and more.

```
document.querySelector("#demo").play(); //Play the Audio
document.querySelector("#demo").pause(); //Pause the Audio
document.querySelector("#demo").volume+=0.1; //Increase Volume
document.querySelector("#demo").volume-=0.1; //Decrease Volume
```

You can read more on what you can do with those two elements in the [Mozilla Developer Network documentation](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Using_HTML5_audio_and_video). You also want to give a closer look to the [supported format list](https://developer.mozilla.org/en-US/docs/HTML/Supported_media_formats).

## Use audio while the screen is locked

Maybe you are building a podcast app, or at least you need to be able to play audio while the screen is locked? There is a way to do it by using the `audio`

tag. You simply need to add the `mozaudiochannel`

attribute with the value of `content`

to your actual tag.

```
```

Actually, it’s not quite true as this code won’t work as is. You also need to add a permission to the manifest file.

```
"permissions": {
"audio-channel-content":{
"description":"Use the audio channel for the music player"
}
}
```

Having the manifest line above will authorize your application to use the audio channel to play music, even when the screen is locked. Having said that, you probably realize that this code **is specific to Firefox OS for now**. I intentionally put the end of the last sentence in bold as it’s one thing you need to understand about Firefox OS: we had to create some APIs, features or elements to give the power HTML deserve for developers, but we are working with the W3C to make those standards. In the case that the standards won’t be the same as what we created, we’ll change it to reflect it.

## Firefox OS Web activities

Finally, something very handy for Firefox OS developers: the [Web Activities](https://developer.mozilla.org/en-US/docs/WebAPI/Web_Activities). They define a way for applications to delegate an activity to another (usually user-chosen) application. They aren’t standardized, at the time of writing. In the case that will be interesting to us, we’ll use the Web Activity call `open`

, to open music or video files. Note that for video, you can also use the `view`

activity that basically does the same. Let’s say I want to open a remote video when someone clicks on a button with the id `open-video`

: I’ll use the following code in my JavaScript to make it happen.

```
var openVideo = document.querySelector("#open-video");
if (openVideo) {
openVideo.onclick = function () {
var openingVideo = new MozActivity({
name: "open",
data: {
type: [
"video/webm",
"video/mp4",
"video/3gpp",
"video/youtube"
],
url: "http://v2v.cc/~j/theora_testsuite/320x240.ogg"
}
});
}
}
```

In that situation, the video player of Firefox OS will open, and play the video: it’s that easy!

## In the end…

You may or may not need to use those tricks in your app, but adding videos or audio can enhance the quality of your application, and make it feel alive. At the end, you have to give a strong experience to your users, and it’s what will make the difference between a good and a great app!

## About
[
Frédéric Harper ](http://outofcomfortzone.net)

As a Senior Technical Evangelist at Mozilla, Fred shares his passion about the Open Web, and help developers be successful with Firefox OS. Experienced speaker, t-shirts wearer, long-time blogger, passionate hugger, and HTML5 lover, Fred lives in Montréal, and speak Frenglish. Always conscious about the importance of unicorns, and gnomes, you can read about these topics, and other thoughts at outofcomfortzone.net.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 5 comments

David RNovember 11th, 2013 at 16:40Frédéric HarperNovember 12th, 2013 at 07:05web application developersNovember 12th, 2013 at 22:13Frédéric HarperNovember 13th, 2013 at 08:05LukeNovember 13th, 2013 at 14:59