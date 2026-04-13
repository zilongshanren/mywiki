---
title: Performance-Tuning a WebVR Game – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/09/performance-tuning-webvr-game/
author: Josh Marinacci
published: '2018-09-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

For the past couple of weeks, I have been working on a VR version of one of my favorite puzzle games, the [Nonogram](https://en.wikipedia.org/wiki/Nonogram), also known as Picross or Griddlers. These are puzzles where you must figure out which cells in a grid are colored in by using column and row counts. I thought this would be perfect for a nice, relaxing VR game. I call it [Lava Flow](https://vr.josh.earth/x/nonogram/).


Since Lava Flow is meant to be a casual game, I want it to load quickly. My goal is for the whole game to be as small as possible and load under 10 seconds on a 3G connection. I also wanted it to run at a consistent 60 frames per second (fps) or better. Consistent frame rate is the most important consideration when developing WebVR applications.

### Measure first

Before I can improve the performance or size, I need to know where I’m starting. The best way to see how big my application really is is to use the [Network tab](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor?utm_source=mozilla&utm_medium=devtools-netmonitor&utm_campaign=default#Filtering_by_properties) of the Firefox Developer tools. Here’s how to use it.

Open the Network tab of Firefox developer tools. Click disable cache, then reload the page. At the bottom of the page, I can see the total page size. When I started this project it was at 1.8MB.![](../../assets/59ab950f6f8951bc.png)


My application uses [three.js](https://threejs.org/), the popular open source 3D library. Not surprisingly, the biggest thing is three.js itself. I’m not using the minified version, so it’s over 1MB! By loading *three.min.js* instead, the size is now **536KB vs 1110KB**. Less than half the size.

The game uses two 3D models of rocks. These are in GLB format, which is compressed and optimized for web usage. My two rocks are already weighing in at less than 3KB each, so there is not much to optimize there. The JavaScript code I’ve written is a bunch of small files. I could use a compressor later to reduce the fetch count, but it’s not worth worrying about yet.

### Image compression

The next biggest resources are the two lava textures. They are PNGs and collectively add up to 561KB.

I re-compressed the two lava textures as JPEGs with medium quality. Also, since the bump map image doesn’t need to be as high resolution as the color texture, I resized it from 512×512 to 128×128. That dropped the sizes from 234KB to 143KB and 339KB to 13KB. Visually there isn’t much difference, but the page is now down to 920KB.

The next two big things are a JSON font and the GLTFLoader JavaScript library. Both of those can be gzip compressed, so I won’t worry about them yet.

### Audio

Now let’s play the game and make sure everything is still working. It looks good. Wait, what’s that? A new network request? Of course, the audio files! The sound isn’t triggered until the first user interaction. Then it downloads over 10MB of MP3s. Those aren’t accounted for by the [DefaultLoader](https://threejs.org/docs/index.html#api/en/loaders/managers/DefaultLoadingManager) because I’m loading it through audio tags instead of JavaScript. Gah!

I don’t really want to wait for the background music to load, however it would be nice to have the sound effects preloaded. Plus audio elements don’t have the control I need for sound effects, nor are they 3D-capable. So I moved those to be loaded as [Audio](https://threejs.org/docs/index.html#api/en/audio/Audio) objects with the [AudioLoader](https://threejs.org/docs/index.html#api/en/loaders/AudioLoader) within three.js. Now they are fully loaded on app start and are accounted for in the download time.

With all of the audio (except the background theme), everything is 2.03 MB. Getting better.

### Slowdowns

There is a weird glitch where the whole scene pauses when rebuilding the game board. I need to figure out what’s going on there. To help debug the problems, I need to see the frames per second inside of VR Immersive mode. The standard [stats.js](https://github.com/mrdoob/stats.js/) module that most three.js apps use actually works by overlaying a DOM element on top of the WebGL canvas. That’s fine most of the time but won’t work when we are in immersive mode.

To address this, I created a little class called [JStats](https://github.com/joshmarinacci/webxr-experiments/blob/master/nonogram/jstats.js) which draws stats to a small square anchored to the top of the VR view. This way you can see it all the time inside of immersive mode, no matter what direction you are looking.

I also created a simple timer class to let me measure how long a particular function takes to run. After a little testing, I confirmed that anywhere from 250 to 450 msec is required to run the setupGame function that happens every time the player gets to a new level.

I dug into the code and found two things. First, each cell is using its own copy of the rounded rectangle geometry and material. Since this is the same for every cell, I can just create it once and reuse it for each cell. The other thing I discovered is that I’m creating the text overlays every time the level changes. This isn’t necessary. We only need one copy of each text object. They can be reused between levels. By moving this to a separate setupText function, I saved several hundred milliseconds. It turns out triangulating text is very expensive. Now the average board setup is about 100 msec, which shouldn’t be noticeable, even on a mobile headset.

As a final test I used the network monitor to throttle the network down to 3G speeds, with the cache disabled. My goal is for the screen to first be painted within 1 second and the game ready to play within 10 seconds. The network screen says it takes 12.36 seconds. Almost there!

### Two steps forward, one step back

As I worked on the game, I realized a few things were missing.

- There should be a progress bar to indicate that the game is loading.
- The tiles need sound effects when entering and exiting the mouse/pointer.
- There should be music each time you complete a level.
- The splash screen needs a cool font.

The progress bar is easy to build because the [DefaultLoadingManager](https://threejs.org/docs/index.html#api/en/loaders/managers/DefaultLoadingManager) provides callbacks. I created a progress bar in the HTML overlay like this:

<progress id="progress" value="0" max="100"></progress>

Then update it whenever the loading manager tells me something is loaded.

THREE.DefaultLoadingManager.onProgress = (url, loaded, total) => { $("#progress").setAttribute('value',100*(loaded/total)) }

Combined with some CSS styling it looks like this:

### Battling bloat

Next up is music and effects. Adding the extra music is another 133KB + 340KB, which bloats the app up nearly another half a megabyte. Uh oh.

I can get a little bit of that back with fonts. Currently I’m using one of the standard three.js fonts which are in JSON format. This is not a terribly efficient format. Files can be anywhere from 100KB to 600KB depending on the font. It turns out three.js can now load TrueType fonts directly without first converting to JSON format. The font I picked was called [Hobby of Night](https://fontlibrary.org/en/font/hobby-of-night) by deFharo, and it’s only 80KB. However, to load TTF file requires TTFLoader.js (4KB) and opentype.min.js which is 124KB. So I’m still loading more than before, but at least opentype.min.js will be amortized across all of the fonts. It doesn’t help today since I’m only using one font, but it will help in the future. So that’s another 100KB or so I’m using up.

The lesson I’ve learned today is that optimization is always two steps forward and one step back. I have to investigate everything and spend the time polishing both the game and loading experience.

The game is currently about 2.5MB. Using the Good 3G setting, it takes 13.22 seconds to load.

### Audio revisited

When I added the new sound effects, I thought of something. All of them are coming from FreeSound.org which generally provides them in WAV format. I have used iTunes to convert them to MP3s, but iTunes may not use the most optimized format. Looking at one of the files I discovered it was encoded at 192KBps, the default for iTunes. Using a command line tool, I bet I could compress them further.

I installed `ffmpeg`

and reconverted the 30-second song like this:

ffmpeg -i piano.wav -codec:a libmp3lame -qscale:a 5 piano.mp3

It went from 348KB to 185KB. That’s a 163KB savings! In total the sounds went from 10MB to 4.7MB, greatly reducing the size of my app. The total download size to start the game without the background music is now 2.01MB.

### Sometimes you get a freebie

I loaded the game to my web server [here](https://vr.josh.earth/x/nonogram/) and tested it on my VR headsets to make sure everything still works. Then I tried loading the public version in Firefox again with the network tab open. I noticed something weird. The total download size is smaller! In the status bar it says: 2.01 MB/1.44 MB transferred. On my local web server where I do development, it says: 2.01 MB/2.01 MB transferred. That’s a huge difference. What accounts for this?

I suspect it’s because my public web server does gzip compression and my local web server does not. For an MP3 file this makes no difference, but for highly compressible files like JavaScript it can be huge. For example, the three.min.js file is 536.08KB uncompressed but an astounding 135.06KB compressed. Compression makes a huge difference. And now the download is just 1.44MB, and download time over Good 3G is 8.3 seconds. Success!

I normally do all of my development on the local web server and only use the public one when the project is ready. This is a lesson to look at everything and always measure.

### In the end

These are the lessons I learned while tuning my application. Making the first version of a game is easy. Getting it ready for release is hard. It’s a long slog, but the end results are so worth it. The difference between a prototype and a game is sweating the little details. I hope these tips help you make your own great WebVR experiences.

## About
[
Josh Marinacci ](https://joshondesign.com/)

I am an author, researcher, and recovering engineer. Formerly on the Swing Team at Sun, the webOS team at Palm, and Nokia Research. I spread the word of good user experiences. I live in sunny Eugene Oregon with my wife and genius Lego builder child.

## 6 comments

Jorge QuiñónezSeptember 20th, 2018 at 19:58Josh MarinacciSeptember 21st, 2018 at 07:40Meizano Ardhi MuhammadSeptember 21st, 2018 at 23:33Josh MarinacciSeptember 22nd, 2018 at 12:34CristianOctober 3rd, 2018 at 23:54Josh MarinacciOctober 4th, 2018 at 09:26