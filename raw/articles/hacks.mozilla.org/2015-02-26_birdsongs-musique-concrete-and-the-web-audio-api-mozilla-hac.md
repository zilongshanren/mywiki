---
title: Birdsongs, Musique Concrète, and the Web Audio API – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2015/02/birdsongs-musique-concrete-and-the-web-audio-api/
author: Ali Almossawi
published: '2015-02-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In January 2015, my friend and collaborator [Brian Belet](http://www.beletmusic.com/Home_Page.html) and I presented [Oiseaux de Même](http://birdwalker.com/quartet) — an audio soundscape app created from recordings of birds — at the first [Web Audio Conference](http://wac.ircam.fr/program). In this post I’d like to describe my experience of implementing this app using the [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API), [Twitter Bootstrap](http://getbootstrap.com/), Node.js, and REST APIs.

![Screenshot showing Birds of a Feather, a soundscape created with field recordings of birds that are being seen in your vicinity.](../../assets/937bcc242b7d76a4.png)


![Screenshot showing Birds of a Feather, a soundscape created with field recordings of birds that are being seen in your vicinity.](../../assets/937bcc242b7d76a4.png)

Screenshot showing Birds of a Feather, a soundscape created with field recordings of birds that are being seen in your vicinity.

### What is it? Musique Concrète and citizen science

We wanted to create a web-based [Musique Concrète](http://en.wikipedia.org/wiki/Musique_concr%C3%A8te), building an artistic sound experience by processing field recordings. We decided to use [xeno-canto](http://www.xeno-canto.org/) — a library of over 200,000 recordings of 9,000 different bird species — as our source of recordings. Almost all the recordings are licensed under Creative Commons by their generous recordists. We select recordings from this library based on data from [eBird](http://ebird.org/content/ebird/), a database of tens of millions of bird sightings contributed by bird watchers everywhere. By using the [Geolocation API](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/Using_geolocation) to [retrieve eBird sightings near to the listeners’ location](https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-RecentNearbyObservations), our soundscape can consist of recordings of bird species that bird watchers have reported recently near the listener — each user gets a personalized soundscape that changes daily.

### Use of the Web Audio API

We use the browser’s Web Audio API to play back the sounds from xeno-canto. The Web Audio API allows developers to play back, record, analyze, and process sound by creating AudioNodes that are connected together, like an old [modular synthesizer](https://en.wikipedia.org/wiki/Modular_synthesizer).

Our soundscape is implemented using four AudioBuffer nodes, each of which plays a field recording in a loop. These loops are placed in a stereo field using Panner nodes, and mixed together before being sent to the listener’s speakers or headphones.

### Controls

After all the sounds have loaded and begin playing, we offer users several controls for manipulating the sounds as they play:

- The
**Pan**button randomizes the spatial location of the sound in 3D space. - The
**Rate**button randomizes the playback rate. - The
**Reverse**button reverses the direction of sound playback. - Finally, the
**Share**button lets you capture the state of the soundscape and save that snapshot for later.

The controls described above are implemented as typical JavaScript event handlers. When the **Pan** button is pressed, for example, we run this handler:

```
// sets the X,Y,Z position of the Panner to random values between -1 and +1
BirdSongPlayer.prototype.randomizePanner = function() {
this.resetLastActionTime();
// NOTE: x = -1 is LEFT
this.panPosition = { x: 2 * Math.random() - 1, y: 2 * Math.random() - 1, z: 2 * Math.random() - 1}
this.panner.setPosition( this.panPosition.x, this.panPosition.y, this.panPosition.z);
}
```

### Some parts of the Web Audio API are write-only

I had a few minor issues where I had to work around shortcomings in the Web Audio API. Other authors have already documented similar experiences; I’ll summarize mine briefly here:

**Can’t read Panner position**: In the event handler for the**Share**button, I want to retrieve and store the current Audio Buffer playback rate and Panner position. However, the current Panner node does not allow retrieval of the position after setting it. Hence, I store the new Panner position in an instance variable in addition to calling`setPosition()`

.This has had a minimal impact on my code so far. My longer-term concern is that I’d rather store the position in the Panner and retrieve it from there, instead of storing a copy elsewhere. In my experience, multiple copies of the same information becomes a readability and maintainability problem as code grows bigger and more complex.

**Can’t read AudioBuffer’s playbackRate**: The**Rate**button described above calls`linearRampToValueAtTime()`

on the`playbackRate AudioParam`

. As far as I can tell, AudioParams don’t let me retrieve their values after calling`linearRampToValueAtTime()`

, so I’m obliged to keep a duplicate copy of this value in my JS object.**Can’t read AudioBuffer playback position**: I’d like to show the user the current playback position for each of my sound loops, but[the API doesn’t provide this information](https://github.com/WebAudio/web-audio-api/issues/296). Could I compute it myself? Unfortunately, after a few iterations of ramping an AudioBuffer’s`playbackRate`

between random values, it is very difficult to compute the current playback position within the buffer. Unlike some API users, I don’t need a highly accurate position, I just want to visualize for my users when the current sound loop restarts.

### Debugging with the Web Audio inspector

I had great success using Firefox’s Web Audio inspector to watch my Audio Nodes being created and interconnected as my code runs.

In the screenshot above, you can see the four `AudioBufferSource`

s, each feeding through a `GainNode`

and `PannerNode`

before being summed by an `AudioDestination`

. Note that each recording is also connected to an `AnalyzerNode`

; the Analyzers are used to create the scrolling amplitude graphs for each loop.

### Visualizing sound loops

As the soundscape evolves, users often want to know which bird species is responsible for a particular sound they hear in the mix. We use a scrolling visualization for each loop that shows instantaneous amplitude, creating distinctive shapes you can correlate with what you’re hearing. The visualization uses the Analyzer node to perform a [fast Fourier transform (FFT)](http://en.wikipedia.org/wiki/Fast_Fourier_transform) on the sound, which yields the amplitude of the sound at every frequency. We compute the average of all those amplitudes, and then draw that amplitude at the right edge of a Canvas. As the contents of the Canvas shift sideways on every animation frame, the result is a horizontally scrolling amplitude graph.

```
BirdSongPlayer.prototype.initializeVUMeter = function() {
// set up VU meter
var myAnalyser = this.analyser;
var volumeMeterCanvas = $(this.playerSelector).find('canvas')[0];
var graphicsContext = volumeMeterCanvas.getContext('2d');
var previousVolume = 0;
requestAnimationFrame(function vuMeter() {
// get the average, bincount is fftsize / 2
var array = new Uint8Array(myAnalyser.frequencyBinCount);
myAnalyser.getByteFrequencyData(array);
var average = getAverageVolume(array);
average = Math.max(Math.min(average, 128), 0);
// draw the rightmost line in black right before shifting
graphicsContext.fillStyle = 'rgb(0,0,0)'
graphicsContext.fillRect(258, 128 - previousVolume, 2, previousVolume);
// shift the drawing over one pixel
graphicsContext.drawImage(volumeMeterCanvas, -1, 0);
// clear the rightmost column state
graphicsContext.fillStyle = 'rgb(245,245,245)'
graphicsContext.fillRect(259, 0, 1, 130);
// set the fill style for the last line (matches bootstrap button)
graphicsContext.fillStyle = '#5BC0DE'
graphicsContext.fillRect(258, 128 - average, 2, average);
requestAnimationFrame(vuMeter);
previousVolume = average;
});
}
```

### What’s next

I’m continuing to work on cleaning up my JavaScript code for this project. I have several user interface improvements suggested by my Mozillia colleagues that I’d like to try. And Prof. Belet and I are considering what other sources of geotagged sounds we can use to make more soundscapes with. In the meantime, please [try Oiseaux de Même](http://birdwalker.com/quartet) for yourself and let us know what you think!

## 6 comments

Bill WalkerFebruary 26th, 2015 at 18:54shavounetFebruary 27th, 2015 at 00:39Havi Hoffman [Editor]February 27th, 2015 at 08:19Bill WalkerFebruary 27th, 2015 at 17:14AndrewFebruary 26th, 2015 at 23:43Bill WalkerMarch 11th, 2015 at 15:22