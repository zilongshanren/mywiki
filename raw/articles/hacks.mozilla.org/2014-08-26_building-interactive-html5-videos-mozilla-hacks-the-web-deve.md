---
title: Building Interactive HTML5 Videos – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/08/building-interactive-html5-videos/
author: Jeroen Wijering
published: '2014-08-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The HTML5 <video> element makes embedding videos into your site as easy as embedding images. And since all major browsers support <video> since 2011, it’s also the most reliable way to get your moving pictures seen by people.

A more recent addition to the HTML5 family is the <track> element. It’s a sub-element of <video>, intended to make the video timeline more accessible. Its main use case is adding closed captions. These captions are loaded from a separate text file (a [WebVTT](https://developer.mozilla.org/en-US/docs/Web/API/Web_Video_Text_Tracks_Format) file) and printed over the bottom of the video display. Ian Devlin has written [an excellent article](https://hacks.mozilla.org/2014/07/adding-captions-and-subtitles-to-html5-video/) on the subject.

Beyond captions though, the <track> element can be used for any kind of interaction with the video timeline. This article explores 3 examples: chapter markers, preview thumbnails, and a timeline search. By the end, you will have sufficient understanding of the <track> element and its scripting API to build your own interactive video experiences.

## Chapter Markers

Let’s start with an example made popular by DVD disks: chapter markers. These allow viewers to quickly jump to a specific section. It’s especially useful for longer movies like Sintel:

The chapter markers in this example reside in an [external VTT file](http://demo.jwplayer.com/text-tracks/assets/chapters.vtt) and are loaded on the page through a <track> element with a *kind* of **chapters. The track is set to load by default:

```
```

Next, we use JavaScript to load the cues of the text track, format them, and print them in a controlbar below the video. Note we have to wait until the external VTT file is loaded:

```
track.addEventListener('load',function() {
var c = video.textTracks[0].cues;
for (var i=0; i
```
In above code block, we’re adding 2 properties to the list entries to hook up interactivity. First, we set a data attribute to store the start position of the chapter, and second we add a click handler for an external *seek* function. This function will jump the video to the start position. If the video is not (yet) playing, we’ll make that so:

function seek() {
video.currentTime = this.getAttribute('data-start');
if(video.paused){ video.play(); }
};

That’s it! You now have a visual chapter menu for your video, powered by a VTT track. Note the [actual live Chapter Markers example](http://demo.jwplayer.com/text-tracks/chapters.html) has a little bit more logic than described, e.g. to toggle playback of the video on click, to update the controlbar with the video position, and to add some CSS styling.

## Preview Thumbnails

This second example shows a cool feature made popular by Hulu and Netflix: preview thumbnails. When mousing over the controlbar (or dragging on mobile), a small preview of the position you’re about to seek to is displayed:

This example is also powered by an [external VTT file](http://demo.jwplayer.com/text-tracks/assets/thumbs.vtt), loaded in a metadata track. Instead of texts, the cues in this VTT file contain links to a [separate JPG image](http://demo.jwplayer.com/text-tracks/assets/thumbs.jpg). Each cue could link to a separate image, but in this case we opted to use a single JPG sprite - to keep latency low and management easy. The cues link to the correct section of the sprite by using [Media Fragment URIs](http://www.w3.org/TR/media-frags/).Example:

http://example.com/assets/thumbs.jpg?xywh=0,0,160,90

Next, all important logic to get the right thumbnail and display it lives in a `mousemove`

listener for the controlbar:

controlbar.addEventListener('mousemove',function(e) {
// first we convert from mouse to time position ..
var p = (e.pageX - controlbar.offsetLeft) * video.duration / 480;
// ..then we find the matching cue..
var c = video.textTracks[0].cues;
for (var i=0; i p) {
break;
};
}
// ..next we unravel the JPG url and fragment query..
var url =c[i].text.split('#')[0];
var xywh = c[i].text.substr(c[i].text.indexOf("=")+1).split(',');
// ..and last we style the thumbnail overlay
thumbnail.style.backgroundImage = 'url('+c[i].text.split('#')[0]+')';
thumbnail.style.backgroundPosition = '-'+xywh[0]+'px -'+xywh[1]+'px';
thumbnail.style.left = e.pageX - xywh[2]/2+'px';
thumbnail.style.top = controlbar.offsetTop - xywh[3]+8+'px';
thumbnail.style.width = xywh[2]+'px';
thumbnail.style.height = xywh[3]+'px';
});

All done! Again, the [actual live Preview Thumbnails example](http://demo.jwplayer.com/text-tracks/thumbs.html) contains some additional code. It includes the same logic for toggling playback and seeking, as well as logic to show/hide the thumbnail when mousing in/out of the controlbar.

## Timeline Search

Our last example offers yet another way to unlock your content, this time though in-video search:

This example re-uses an existing [captions VTT file](http://demo.jwplayer.com/text-tracks/assets/captions.vtt), which is loaded into a *captions* track. Below the video and controlbar, we print a basic search form:


Like with the thumbnails example, all key logic resides in a single function. This time, it’s the event handler for submitting the form:

```
form.addEventListener('submit',function(e) {
// First we’ll prevent page reload and grab the cues/query..
e.preventDefault();
var c = video.textTracks[0].cues;
var q = document.querySelector("input").value.toLowerCase();
// ..then we find all matching cues..
var a = [];
for(var j=0; j
``` -1) {
a.push(c[j]);
}
}
// ..and last we highlight matching cues on the controlbar.
for (var i=0; i
Three time’s a charm! Like with the other ones, the [actual live Timeline Search example](http://demo.jwplayer.com/text-tracks/search.html) contains additional code for toggling playback and seeking, as well as a snippet to update the controlbar help text.

## Wrapping Up

Above examples should provide you with enough knowledge to build your own interactive videos. For some more inspiration, see our experiments around [clickable hot spots](http://www.jwplayer.com/labs/experiments/hot-spots/), [interactive transcripts](http://www.jwplayer.com/labs/experiments/interactive-transcripts/), or [timeline interaction](http://www.jwplayer.com/labs/experiments/timeline-interaction/).

Overall, the [HTML5 <track> element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/track) provides an easy to use, cross-platform way to add interactivity to your videos. And while it definitely takes time to author VTT files and build similar experiences, you will see higher accessibility of and engagement with your videos. Good luck!

## About
[
Jeroen Wijering ](http://www.jwplayer.com)

Creator of the successful JW Player and co-founder of the company with the same name. He is the team's Product Evangelist, driving innovation and market awareness.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.


## 16 comments

Elijah LynnAugust 26th, 2014 at 15:13Robert Nyman [Editor]August 27th, 2014 at 03:27Mathew PorterAugust 28th, 2014 at 08:59Chris AdamsAugust 27th, 2014 at 05:52Robert Nyman [Editor]August 27th, 2014 at 06:45Heather ZhongAugust 27th, 2014 at 07:16Chris AdamsAugust 27th, 2014 at 11:25alexander farkasAugust 29th, 2014 at 06:57Chris AdamsAugust 29th, 2014 at 08:04happyWangAugust 27th, 2014 at 07:20Raymond CamdenAugust 27th, 2014 at 07:42Robert Nyman [Editor]August 27th, 2014 at 08:35Jx PrinceAugust 27th, 2014 at 11:14Md Mizanur RahmanSeptember 19th, 2014 at 02:59Robert Nyman [Editor]September 25th, 2014 at 13:02KrisSeptember 22nd, 2014 at 15:10