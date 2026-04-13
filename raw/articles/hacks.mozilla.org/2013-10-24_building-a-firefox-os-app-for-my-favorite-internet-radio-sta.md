---
title: Building a Firefox OS App for my favorite Internet radio station – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/10/building-a-firefoxos-app-for-my-favorite-internet-radio-station/
author: Aras Balali Moghaddam
published: '2013-10-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

I recently created [a Firefox OS app for my favourite radio station](https://marketplace.firefox.com/app/radio-paradise/) — radio paradise. It was a lot of fun making this app, so I thought it would be good to share some notes about how I built it.

## The audio tag

It started by implementing the main functionality of the app, playing an ogg stream I got from the Internet radio station, using the [HTML5 audio](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio) element

`<pre lang="xml">`


<audio src="http://stream-sd.radioparadise.com/rp_192m.ogg" controls preload></audio>

</pre>

That was easy! At this point our app is completely functional. If you don’t believe me, checkout [this jsfiddle](http://jsfiddle.net/arasbm/7sQAr/12/). But please continue reading, since there will be a few more sweet features added. In fact, checkout the short video below to see how it will turn out.

Because this content belongs to radio paradise, before implementing the app, I contacted them to ask for their permission to make a Firefox OS app for their radio station; they responded:

Thanks. We’d be happy to have you do that.

[Our existing web player]is html5-based. That might be a place to start. Firefox should have native support for our Ogg Vorbis streams.

I couldn’t have asked for a more encouraging response, and that was enough to set things in motion.

## Features of the app

I wanted the app to be very minimal and simple — both in terms of user experience and the code backing it. Here is a list of the features I decided to include:

- A single, easy to access, button to play and pause the music
- Artist name, song title and album cover for the current song playing should fill up the interface
- Setting option to select song quality (for situation when bandwidth is not enough to handle highest quality)
- Setting option to start app with music playing or paused
- Continue playing even when the app is sent to the background
- Keep the screen on when the app is running in the forground

Instead of using the HTML tag, I decided to create the audio element and configure it in JavaScript. Then I hooked up an event listener for a button to play or stop music.

`<pre lang="javascript">`


var btn = document.getElementById('play-btn');

var state = 'stop';

btn.addEventListener('click', stop_play);

// create an audio element that can be played in the background

var audio = new Audio();

audio.preload = 'auto';

audio.mozAudioChannelType = 'content';

function play() {

audio.play();

state = 'playing';

btn.classList.remove('stop');

btn.classList.add('playing');

}

function stop() {

audio.pause();

state = 'stop';

btn.classList.add('stop');

btn.classList.remove('playing');

}

// toggle between play and stop state

function stop_play() {

(state == 'stop') ? play() : stop();

}

</pre>

## Accessing current song information

The first challenge I faced was accessing the current song information. Normally we should not need any special privilege to access third party API’s as long as they provide correct header information. However, the link radio paradise provided me for getting the current song information did not allow for cross origin access. Luckily FirefoxOS has a special power reserved for this kind of situation — systemXHR comes to the rescue.

`<pre lang="javascript">`


function get_current_songinfo() {

var cache_killer = Math.floor(Math.random() * 10000);

var playlist_url =

'http://www.radioparadise.com/ajax_rp2_playlist.php?' +

cache_killer;

var song_info = document.getElementById('song-info-holder');

var crossxhr = new XMLHttpRequest({mozSystem: true});

crossxhr.onload = function() {

var infoArray = crossxhr.responseText.split('|');

song_info.innerHTML = infoArray[1];

next_song = setInterval(get_current_songinfo, infoArray[0]);

update_info();

};

crossxhr.onerror = function() {

console.log('Error getting current song info', crossxhr);

nex_song = setInterval(get_current_singinfo, 200000);

};

crossxhr.open('GET', playlist_url);

crossxhr.send();

clearInterval(next_song);

}

</pre>

This meant that the app would have to be privileged and thus packaged. I normally would try to keep my apps hosted, because that is very natural for a web app and has several benefits including the added bonus of being accessible to search engines. However, in cases such as this we have no other option but to package the app and give it the special privileges it needs.

`<pre lang="javascript">`


{

"version": "1.1",

"name": "Radio Paradise",

"launch_path": "/index.html",

"description": "An unofficial app for radio paradise",

"type": "privileged",

"icons": {

"32": "/img/rp_logo32.png",

"60": "/img/rp_logo60.png",

"64": "/img/rp_logo64.png",

"128": "/img/rp_logo128.png"

},

"developer": {

"name": "Aras Balali Moghaddam",

"url": "http://arasbm.com"

},

"permissions": {

"systemXHR": {

"description" : "Access current song info on radioparadise.com"

},

"audio-channel-content": {

"description" : "Play music when app goes into background"

}

},

"installs_allowed_from": ["*"],

"default_locale": "en"

}

</pre>

## Updating song info and album cover

That XHR call to radio paradise proides me with three important pieces of information:

- Name of the current song playing and it’s artist
- An image tag containing the album cover
- Time left to the end of current song in miliseconds

Time left to the end of current song is very nice to have. It means that I can execute the XHR call and update the song information only once for every song. I first tried using the setTimeout function like this:

`<pre lang="javascript">`


//NOT working example. Can you spot the error?

crossxhr.onload = function() {

var infoArray = crossxhr.responseText.split('|');

song_info.innerHTML = infoArray[1];

setTimeout('get_current_songinfo()', infoArray[0]);

update_info();

};

</pre>

To my surprise, that did not work, and I got a nice error in logcat about a [CSP restriction](https://developer.mozilla.org/en-US/Apps/CSP). It turns out that any attempt at dynamically executing code is banned for security reasons. All we have to do in this scenario to avoid the CSP issue is to pass a callable object, instead of a string.

`<pre lang="javascript">`


// instead of passing a string to setTimout we pass

// a callable object to it

setTimeout(get_current_songinfo, infoArray[0]);

</pre>

**Update:** Mindaugas [pointed out in the comments below](https://hacks.mozilla.org/2013/10/building-a-firefoxos-app-for-my-favorite-internet-radio-station/comment-page-1/#comment-2153793) that using [innerHTML](https://developer.mozilla.org/en-US/docs/Web/API/Element.innerHTML) to parse unknown content in this way, introduces some security risks. Because of these security implications, we should retrieve the remote content as text instead of HTML. One way to do this is to use *song_info.textContent* which does not interpret the passed content as HTML. Another option, as Frederik Braun [pointed out](https://hacks.mozilla.org/2013/10/building-a-firefoxos-app-for-my-favorite-internet-radio-station/comment-page-1/#comment-2153896) is to use a text node which can not render HTML.

## Adding a unique touch

One of the great advantages of developing mobile applications for the web is that you are completely free to design your app in any way you want. There is no enforcement of style or restriction on interaction design innovation. Knowing that, it was hard to hold myself back from trying to explore new ideas and have some fun with the app. I decided to hide the settings behind the main content and then add a feature so user can literally cut open the app in the middle to get to setting. That way they are tucked away, but still can be discovered in an intuitive way. For UI elements in the setting page to toggle options I decided to give [Brick](http://mozilla.github.io/brick/index.html) a try., with a bit of custom styling added.

## Using the swipe gesture

As you saw in the video above, to open and close the cover image I use pan and swipe gestures. To implement that, I took [gesture detector from Gaia](https://github.com/mozilla-b2g/gaia/blob/master/shared/js/gesture_detector.js). It was very easy to integrated the gesture code as a module into my app and hook it up to the cover image.

## Organizing the code

For an app this small, we do not have to use modular code. However, since I have recently started to learn about AMD practices, I decided to use a module system. I asked [James Burke](https://twitter.com/jrburke) about implications of using requirejs in an app like this. He suggested I use [Alameda](https://github.com/requirejs/alameda) instead, since it is geared toward modern browsers.

## Saving app settings

I wanted to let users choose stream quality as well as whether they want the app to start playing music as soon as it opens. Both of these options need to be persisted somewhere and retrieved when the app starts. I just needed to save a couple of key/value pairs. I went to [#openwebapps](irc://irc.mozilla.org/openwebapps) irc channel and asked for advice. [Fabrice](https://twitter.com/fabricedesre) pointed me to a nice piece of code in Gaia (again!) that is used for [asynchronous storing](https://github.com/mozilla-b2g/gaia/blob/master/shared/js/async_storage.js) of key/value pairs and even whole objects. That was perfect for my use case, so I took it as well. [Gaia](https://github.com/mozilla-b2g/gaia) appears to be a goldmine. Here is the module I created for settings.

`<pre lang="javascript">`


define(['helper/async_storage'], function(asyncStorage) {

var setting = {

values: {

quality: 'high',

play_on_start: false

},

get_quality: function() {

return setting.values.quality;

},

set_quality: function(q) {

setting.values.quality = q;

setting.save();

},

get_play_on_start: function() {

return setting.values.play_on_start;

},

set_play_on_start: function(p) {

setting.values.play_on_start = p;

setting.save();

},

save: function() {

asyncStorage.setItem('setting', setting.values);

},

load: function(callback) {

asyncStorage.getItem('setting', function(values_obj) {

if (values_obj) setting.values = values_obj;

callback();

});

}

};

return setting;

});

</pre>

## Splitting the cover image

Now we get to the really fun part that is splitting the cover image in half. To achieve this effect, I made two identical overlapping canvas element both of which are sized to fit the device width. One canvas clips the image and keeps the left portion of it while the other keeps the right side.

Here is the code for draw function where most of the action is happening. Note that this function runs only once for each song, or when user changes the orientation of the device from portrait to landscape and vice versa.

`<pre lang="javascript">`


function draw(img_src) {

width = cover.clientWidth;

height = cover.clientHeight;

draw_half(left_canvas, 'left');

draw_half(right_canvas, 'right');

function draw_half(canvas, side) {

canvas.setAttribute('width', width);

canvas.setAttribute('height', height);

var ctx = canvas.getContext('2d');

var img = new Image();

var clip_img = new Image();

// opacity 0.01 is used to make any glitch in clip invisible

ctx.fillStyle = 'rgba(255,255,255,0.01)';

ctx.beginPath();

if (side == 'left') {

ctx.moveTo(0, 0);

// add one pixel to ensure there is no gap

var center = (width / 2) + 1;

} else {

ctx.moveTo(width, 0);

var center = (width / 2) - 1;

}

ctx.lineTo(width / 2, 0);

// Draw a wavy pattern down the center

var step = 40;

var count = parseInt(height / step);

for (var i = 0; i < count; i++) {

ctx.lineTo(center, i * step);

// alternate curve control point 20 pixels, every other time

ctx.quadraticCurveTo((i % 2) ? center - 20 :

center + 20, i * step + step * 0.5, center, (i + 1) * step);

}

ctx.lineTo(center, height);

if (side == 'left') {

ctx.lineTo(0, height);

ctx.lineTo(0, 0);

} else {

ctx.lineTo(width, height);

ctx.lineTo(width, 0);

}

ctx.closePath();

ctx.fill();

ctx.clip();

img.onload = function() {

var h = width * img.height / img.width;

ctx.drawImage(img, 0, 0, width, h);

};

img.src = img_src;

}

}

</pre>

## Keeping the screen on

The last feature I needed to add was keeping the screen on when the app is running in foreground and that turned out to be very easy to implement as well. We need to request a [screen wake lock](https://developer.mozilla.org/en-US/docs/Web/API/window.navigator.requestWakeLock)

`<pre lang="javascript">`


var lock = window.navigator.requestWakeLock(resourceName);

</pre>

The screen wake lock is actually pretty smart. It will be automatically released when app is sent to the background, and then will given back to your app when it comes to the foreground. Currently in this app I have not provided an option to release the lock. If in future I get requests to add that option, all I have to do is release the lock that has been obtained before setting the option to false

`<pre lang="javascript">`


lock.unlock();

</pre>

## Getting the app

If you have a FirefoxOS device and like great music, you can now install this app on your device. Search for “radio paradise” in the marketplace, or install it directly[ from this link](https://marketplace.firefox.com/app/radio-paradise/). You can also checkout the [full source code from github](https://github.com/arasbm/radio-paradise). Feel free to fork and modify the app as you wish, to create your own Internet Radio apps! I would love it if you report [issues](https://github.com/arasbm/radio-paradise/issues?state=open), ask for features or send pull requests.

## Conclusion

I am more and more impressed by how quickly we can create very functional and unique mobile apps using web technologies. If you have not build a mobile web app for Firefox OS yet, you should definitely give it a try. The future of open web apps is very exciting, and Firefox OS provides a great platform to get a taste of that excitement.

Now it is your turn to leave a comment. What is your favourite feature of this app? What things would you have done differently if you developed this app? How could we make this app better (both code and UX)?

## About
[
Aras Balali Moghaddam ](http://arasbm)

Aras is an interaction designer and a frontend engineer living in beautiful British Columbia, Canada. He is passionate about the open web and likes to build awesome mobile web apps. You can learn more about him on [his blog](http://arasbm.com/about/).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 17 comments

SanThosh KOctober 24th, 2013 at 23:06Aras Balali MoghaddamOctober 25th, 2013 at 11:43Ivan DejanovicOctober 25th, 2013 at 01:19Aras Balali MoghaddamOctober 25th, 2013 at 11:42Mindaugas J.October 25th, 2013 at 09:44Aras Balali MoghaddamOctober 25th, 2013 at 11:52Mindaugas J.October 28th, 2013 at 09:21Aras Balali MoghaddamOctober 28th, 2013 at 11:42Frederik BraunOctober 29th, 2013 at 12:46Aras Balali MoghaddamOctober 30th, 2013 at 14:53nadrimajstorOctober 25th, 2013 at 15:39Aras Balali MoghaddamOctober 25th, 2013 at 18:05nadrimajstorOctober 26th, 2013 at 12:02Aras Balali MoghaddamOctober 26th, 2013 at 13:28KevinOctober 30th, 2013 at 00:57Aras Balali MoghaddamOctober 30th, 2013 at 15:43KevinOctober 31st, 2013 at 00:28