---
title: Spirit of Indiana (Jones) – syncing HTML5 Video with Maps – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2010/12/spirit-of-indiana-jones-syncing-html5-video-with-maps/
author: Chris Heilmann
published: '2010-12-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

I’ve always been a big fan of the travel/flight sequences in the Indiana Jones movies and judging by the amount of [copy attempts on YouTube](http://www.youtube.com/results?search_query=indiana+jones+map+animation&aq=f) I am not alone in this. As I don’t own any video editing software I thought it should be possible to create the same effect with web technologies and Google Maps and lo and behold it is:

You can [download the animation demo](https://github.com/codepo8/HTML5---map-and-video-syncing) for yourself and try it out locally – all you need is a browser that supports HTML5 video. I know – the music is not quite the same as in the movies, but at least this one is not copyright infringing and it came from the heart (5 minutes in a meeting room in the Mozilla office).

So how was this done and what are problems that needed solving? Here’s how and what.

## Step 1: Find the movie and get it to the right format

That was the easy part. [Archive.org](http://www.archive.org/) has a lot of awesome public domain movies available for you and they are already in the formats needed to use in an HTML5 video element. In this case, I took the short [movie of Charles Lindbergh](http://www.archive.org/details/CharlesLindbergTakesOff) taking off for [his record breaking flight from New York to fly to Paris in 1927](http://en.wikipedia.org/wiki/Charles_Lindbergh).

## Step 2: Displaying the video

Using the video [is pretty simple](http://isithackday.com/spirit-of-indiana/video.html):

```
```

The MP4 format will be used by Webkit based browsers and the Ogg version by Firefox and others. As we want to control the video we omit the `controls`

attribute on the `video`

element – instead we create a button to play the video with JavaScript:

```
window.addEventListener('load',
function() {
var stage = document.getElementById('stage');
var v = document.getElementsByTagName('video')[0];
but = document.createElement('button');
but.innerHTML = 'Click to see Lindbergh's flight';
stage.appendChild(but);
but.addEventListener('click',function(e) {
v.play();
e.preventDefault();
},false);
},
false);
```

As the video is markup we can do whatever we please with it – the power of open technologies. For example as we will do here we can set its opacity in CSS and put in on top of a map.

## Step 3: Create the map path animation

Talking of which, let’s get that moving path done. Google Earth has an API to do that, but it needs a special plugin. Google Maps allows you to paint paths on maps (which actually are SVG, another open standard). Put that in a recursive function and you [get the desired effect](http://isithackday.com/spirit-of-indiana/map.html):

In essence, what I did was take the latitude and longitude of the start and end points and calculate as many points in between the two as I need for the duration of the animation. I store the points in an array called `pos`

and then paint a path from the start to the current point and move the map centre to this point on every iteration.

```
spirit.draw = function(){
var path = new google.maps.Polyline({
path: [startpos,pos[now]],
strokeColor: "#c00",
strokeOpacity: .7,
strokeWeight: 10
});
path.setMap(map);
map.panTo(pos[now])
now = now + 1;
if(now < animationend-1){
setTimeout(spirit.draw,200);
}
}
```

Check the [highly commented source of the map example](https://github.com/codepo8/HTML5---map-and-video-syncing/blob/master/map.js) for the details. Now, we could use this kind of animation and play the video over it - the problem though is that they may get out of sync. When the movie stalls (as it frequently does on this hotel wireless connection) we don't want the animation to keep moving, right?

## Step 4: Syncing video and the map movement

Instead of having two sources of timing information we have to limit ourselves to one source of truth. This is the time stamp of the currently playing movie.

By the way - you might have noticed that I wrapped the map code in a `tilesloaded`

event handler. This is another safeguard for keeping things in sync. I found that on slow connections the tile loading can delay the whole interface immensely (because of all the subdomain lookups), so I make the whole interface dependent on the loading of the map and only proceed when the tiles have finished loading. As the `tilesloaded`

event also fires when the map pans we need to use a boolean to stop it from starting the effect several times:

```
google.maps.event.addListener(map,'tilesloaded',function(){
if(played === false){
// [...other code...]
played = true;
}
});
```

You can read the current timestamp of a video with `video.currentTime`

and whilst the movie is playing it constantly fires an event called `timeupdate`

. As the event fires a lot we need to throttle it somehow. The trick here is to only take the full seconds and increase a counter when a new second is reached. You can see the timestamp and the second interval firing in [the video syncing demo](http://isithackday.com/spirit-of-indiana/video-sync.html):

```
var now = 0;
v.addEventListener('timeupdate',function(o){
log.innerHTML = v.currentTime; /* logging the real timestamp */
var full = parseInt(v.currentTime);
if(full >= now) {
seqlog.innerHTML = now; /* logging the seconds firing */
now = now + 1;
}
},false);
```

That way the movie can lag in between and the sequence still stays in sync. Check the [source of this demo on Github](https://github.com/codepo8/HTML5---map-and-video-syncing/blob/master/video-sync.html).

## Putting it all together

And that was about it - all I had to do is to set the movie's opacity at a certain time stamp, start the sound at another and show and hide the copyright complaint at another. As we rely on the timestamp for the other effects we needed a boolean switch to avoid repeated firing:

```
v.addEventListener('timeupdate',function(o){
full = parseInt(v.currentTime);
if(full === now-1){
mapelm.style.opacity = .8;
v.style.opacity = .4;
}
if(full === animationstart+1 && audioplay === false){
a.play();
audioplay = true;
}
if(full === animationstart+2 && hidden === true){
drmbedamned.style.display = 'block';
hidden = false;
}
if(full === animationstart+3 && hidden === false){
drmbedamned.style.display = 'none';
hidden = true;
}
if(full >= now) {
path = new google.maps.Polyline({
path: [startpos,pos[full]],
strokeColor: "#c00",
strokeOpacity: .7,
strokeWeight: 10
});
path.setMap(map);
map.panTo(pos[full])
now = now + 1;
}
},false);
```

Another event we needed to subscribe to was the movie ending so we can stop the music and start to roll the credits:

```
v.addEventListener('ended',function(o){
a.pause();
spirit.credslist.parentNode.style.display = 'block';
spirit.creds();
},false)
```

As the theme is too short for the whole animation we need to loop it. This can be done by testing for the `ended`

event and rolling back the time to 0:

```
a.addEventListener('ended', function(o) {
a.currentTime = 0;
},false);
```

## Summary

And there you have it - Indiana Jones style maps using open services and open technologies. A workaround for the copyrighted audio (recorded, edited and converted with the free [Audacity](http://audacity.sourceforge.net/) sound editor) and using [Google's Web Fonts](http://code.google.com/webfonts/) as graphics.

You can now take this and change it for even more awesome:

- Replace Google Maps with Openstreetmap to avoid going over the limit
- Add a slight curve to the path from NYC to Paris to make it more accurate (but then again the time is not accurate either - it took charles a tad longer)
- Use a static map and paint the path with Canvas to speed up and smoothen the animation

Why not have a go - it is free and fun to play.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 9 comments

DerekDecember 16th, 2010 at 08:38Tom SkeltonDecember 18th, 2010 at 12:14ShmerlDecember 16th, 2010 at 09:05Robert KaiserDecember 16th, 2010 at 10:07cheilmannDecember 16th, 2010 at 10:09tackDecember 16th, 2010 at 12:40Robert LongsonDecember 18th, 2010 at 03:51paulDecember 18th, 2010 at 14:56NinnaJanuary 7th, 2011 at 08:20