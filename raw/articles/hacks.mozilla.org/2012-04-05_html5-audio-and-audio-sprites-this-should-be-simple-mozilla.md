---
title: HTML5 audio and audio sprites – this should be simple – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2012/04/html5-audio-and-audio-sprites-this-should-be-simple/
author: Chris Heilmann
published: '2012-04-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As we’re having a [HTML5 Audio developer derby](https://developer.mozilla.org/en-US/demos/devderby) this month, I thought it fun to play with audio again. And I found it sadly enough pretty frustrating.

One thing I proposed in a lot of talks is using the idea of [CSS sprites](http://css-tricks.com/css-sprites/) and apply them to HTML5 audio. You’ll get the same benefits – loading one file in one HTTP request instead of many, avoiding failure as files might not get loaded and so on.

To test this out I wrote [the following small demo](http://thewebrocks.com/demos/audiosprite/) using the awesome [Music Non Stop by Kraftwerk](http://www.youtube.com/watch?v=lj1qLbJfmE8).

Clicking the different buttons should play the part of the music file and nothing more. This works fine in Firefox, Chrome and Opera on my computer here. Safari, however, fails to preload the audio and the setting of the current time is off. The code is simple enough that this should work:

```
```

```
// get the audio element and the buttons container
// define a sprite object with the names and the start and end times
// of the different sounds.
var a = document.querySelector('audio'),
buttoncontainer = document.querySelector('#buttons'),
audiosprite = {
'all': [ 0, 5 ],
'boing': [ 0, 1.3 ],
'boomtchack': [ 2, 2.5 ],
'peng': [ 4, 5 ]
},
end = 0;
// when the audio data is loaded, create the buttons
// this way non-HTML5 browsers don't get any buttons
a.addEventListener('loadeddata', function(ev) {
for (var i in audiosprite) {
buttoncontainer.innerHTML += '';
}
}, false);
// If the time of the file playing is updated, compare it
// to the current end time and stop playing when this one
// is reached
a.addEventListener('timeupdate', function(ev) {
if (a.currentTime > end) {
a.pause();
}
},false);
// Play the current audio sprite by setting the currentTime
function play(sound) {
if ( audiosprite[sound] ) {
a.currentTime = audiosprite[sound][0];
end = audiosprite[sound][1];
a.play();
}
}
```

Now, this is nothing new, [Remy Sharp wrote about audio sprites in 2010](http://remysharp.com/2010/12/23/audio-sprites/) and lamented especially the buggy support in iOS (audio won’t load at all until you activate it with a touch – something that sounds horribly like the “click to active” Flash has on IE).

Other issues are looping and latency of HTML5 audio. As reported by Robert O’Callahan [there is a work-around by cloning the audio element before playing it](http://robert.ocallahan.org/2011/11/latency-of-html5-sounds.html) (with an [incredibly annoying test](http://people.mozilla.org/~roc/audio-latency-repeating.html)) and this fix has been [used in the Gladius HTML5 game engine](https://github.com/alankligman/gladius-core/blob/develop/src/sound/default.js).

All in all it seems HTML5 audio still needs a lot of work which is why a lot of Games released lately under the banner of HTML5 use Flash audio or no audio at all. This is sad and needs fixing.

Interestingly enough there are some great projects that you could be part of. [Are we playing yet?](http://areweplayingyet.com/) by Soundcloud and others for example is a test suite for audio support in browsers. You can [write own tests on GitHub](http://areweplayingyet.com/get-involved) and report results to the browser makers.

The jPlayer team has a great [HTML5 Media Event Inspector](http://www.jplayer.org/HTML5.Media.Event.Inspector/) showing just how many of the HTML5 media events are supported in your current browser.

If you want to be safe, you can use [SoundManager 2](http://www.schillmania.com/projects/soundmanager2/) by Scott Schiller to have an API that uses HTML5 when possible and falls back to Flash when the browser doesn’t have any support. It also fixes a few issues for you.

Speaking of Scott Schiller, he continually gives good insight on the state of audio. There is [a 51 minute video](http://www.youtube.com/watch?v=ffk65q5Rl9I) of his article on 24 ways “[Probably, Maybe, No: The State of HTML5 Audio](http://24ways.org/2010/the-state-of-html5-audio)“.

A [shorter and more recent talk on the same subject](http://www.youtube.com/watch?v=C2Tw0BeZb8Q) is also available:

All in all it would be interesting to hear what you think of the state of HTML5 audio:

- Did the companies that heralded HTML5 as the end of plugins drop the ball?
- Is it really sensible to have an API that returns
[probably or maybe or ”](http://www.whatwg.org/specs/web-apps/current-work/multipage/the-video-element.html#dom-navigator-canplaytype)when you ask it if the browser can play a certain type of media? - What could be done to work around these issues?

Let’s re-ignite the discussion on HTML5 audio, after all we need it for the future of [messaging in the browser](http://hacks.mozilla.org/2012/04/webrtc-efforts-underway-at-mozilla/) and telephony, too.

Oh and another thing. Of course there is the [Audio Data API of Firefox](https://wiki.mozilla.org/Audio_Data_API) and [the web audio proposal](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html) from Webkit available but getting those running in mobile devices will be a much bigger change. If you want to know more about those and libraries to work around their differences, there is a great [overview post available on Happyworm](http://happyworm.com/blog/2011/11/15/html5-audio-apis-how-low-can-we-go/).

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 6 comments

BOSSoNeApril 6th, 2012 at 15:57Yves Van GoethemApril 11th, 2012 at 07:11KJune 11th, 2012 at 08:15Niels GregersenJuly 22nd, 2012 at 14:50Javier FrancoMarch 1st, 2013 at 04:48JohnnyApril 2nd, 2013 at 22:00