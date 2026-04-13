---
title: The Making of Face to GIF – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/07/the-making-of-face-to-gif/
author: Horia Dragomir
published: '2013-07-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Face to gif](http://hdragomir.github.io/facetogif/) is a simple webapp that lets you record yourself and gives you an infinitely looping animated gif. In this post I will walk you through how it came to be and what I’ve learned from building the small app.

It started with [Chris Heilmann’s post](http://christianheilmann.com/2013/06/22/use-your-words/) about people losing expressiveness to internet memes. At least, that was what I wanted to understand out of it. I thought it really came down to tooling, like most problems do.

It is the year 2000 and something and we still haven’t found a solution to simple problems like sending large files, doing taxes automatically and reliably online or recording an animated gif in your browser. Also, because memes are so popular and easily accessible, why would people even bother trying to create original content when they can make do with a cute kitten image. I thought some things should be easier.

I had already played around with downloading files generated on the client, so I knew text files were trivial and static images were not that hard. But I didn’t find anything about making gif files client side. I thought that I’d figure out the gif part later or even write it myself – how hard could it actually be, right?

## The Humble Beginning

Since WebRTC is gaining traction, [getUserMedia](https://developer.mozilla.org/en-US/docs/WebRTC/navigator.getUserMedia) is becoming a somewhat viable API. Getting a stream from a webcam to be displayed on a video element was very easy.

```
navigator.getUserMedia({video: true, audio: false}, yes, no);
…
video.src = URL.createObjectURL(stream);
```

I then needed to capture the images that would later make up the gif’s frames. This was not that hard, either. Luckily, you can paint a video element on a canvas context directly using

```
context.drawImage(video, 0,0, width,height);
```

This also allows you to scale the captured frames right there, to normalise the different webcam resolutions. Just make sure your `canvas`

element has the correct width and height properties specified, and you should be fine. Also, you should either `display: none;`

it or remove it from the DOM to avoid unnecessary paints.

```
```

To capture frames, just set an interval at your desired frame rate and cache the frames in an array.

```
setInterval(function () {
context.drawImage(video, 0,0, width,height);
frames.push(context.getImageData(0,0, width,height));
}, 67);
```

Please note that there is no need to use `requestAnimationFrame`

in this case. The video stream continues to play even when the page it’s on is not visible – so I guess capturing it also makes sense. More importantly, you will need a specific interval between frames that will most probably not end up being 60 frames per second.

After stopping the interval – that is to stop “recording” – you are left with a lot of frames, each frame having a lot of pixel data from the video stream that comes from your webcam. And all that data never leaves the web page that’s being displayed on your computer.

At one point, I was considering to add a “download raw data” button so people could do other things than just make a gif of themselves. I decided to actually solve the gif part first, then think about bells and whistles.

## The GIF Writer

After reading too much about the GIF89a and dithering and the LZW algorithm, I cowardly decided to see if I could not find a ready made library. I was lucky to find a demo that combined a series of images into an animated gif – all in JavaScript. I quickly retrofitted the library into my small app and things started moving again.

```
gifworker.sendMessage({ images: frames, delay: 67 });
...
gifworker.onmessage = function(event) {
var img = document.createElement('img');
img.src = event.data.gifDataString;
document.body.appendChild(img);
};
```

What needs to be done from there is as follows:

- write a binary header that describes a file as a GIF98a file.
- write a block describing the width, height and looping control.
- write each frame from the image data list.
- write a trailer 59 – aka semicolon.

Using WebWorkers to do the heavy lifting in a separate thread, keeping the UI responsive was a no-brainer. After it’s done processing, the library provides you with a base64 encoded string representing the gif file. That can be used as a data url for an image.

At one point in my life, I was using data urls so intensively, that I would provide clients with mockups consisting of just one HTML file that had images, css and javascript base64`d in and that wouldn’t require and internet connection to work. And that wouldn’t work in IE.

But I was about to face a different set of problems this time around…

## Saving the files

Data urls can be saved if they’re small enough. If you want to save a gif that is too long and displayed via data url, the browser will not even let you try do that. Trying to be clever with the download attribute on links didn’t help either.

![image of the generated gif and its options in face to gif](../../assets/12bd2bb76671623c.jpg)


While data urls are really cool, there is a limit to how long they can be. I didn’t want to impose what seemed to be a legacy limit on this app.

I altered the library a little to provide me with the raw bytes instead of a base64 string and I used the raw bytes to create a [Blob](http://docs.webplatform.org/wiki/apis/file/Blob), then used `URL.createObjectURL`

to make something I could set an image’s source attribute to.

```
var blob = new Blob([uint8array], {type: "image/gif"});
img.src = URL.createObjectURL(blob);
```

This method of using user generated resources as source attributes is much more reliable and scalable than the old data url method. This also allowed for easier saving of the image.

I use a trick for the download link you will find in my app: I place a simple anchor, with an empty href attribute and I attach a simple ‘click’ event handler. When the user clicks on it, my event handler function simply changes the href attribute to be the same with the source attribute of the image. The browser does the rest.

```
a.addEventListener('click', function (e) {
a.href = img.src;
// the real trick is to let the event bubble up
}, false);
```

We spend so much time as web developers hijacking control from the browser so we may do our own thing. The truth is, we can most of the time just tell the browser where to go and he’ll do a much better job at getting there on its own than if we would be involved.

Getting back to my app, though, I had gotten it to a place where it was doing what I hoped it would be doing: Recording my face with my webcam and serving me a gif of it.

## The Speed

The app was rocking, but it was more like a ballad than a heavy metal song. It took 16 seconds of my life for each 1 second of a gif. This was also because I was writing the gif files at 640×480 originally, but also because it turns out that binary operations on pixel data can be quite slow if not optimised.

I was scrambling for solutions, looking into the library’s TypeScript source code and the generated JavaScript to find ways to improve it, considering asm.js, using TypedArrays more, anything – when I stumbled upon another JavaScript library for writing animated gifs.

[gif.js](https://github.com/hdragomir/gif.js) was leaner, could use several web workers to process the frames and had what I thought was a better looking API. After retrofitting this new library, tweaking the settings and halving the size, I was able to produce gifs, right in the web app at blazing speeds.

The one downfall was that what I had gained in speed, I had lost in compression. A mere 10 seconds of GIF would produce about 30 MB worth of data. After some more heavy tweaking, I was able to get that down to about 5 MB / 10s. Still a lot, but it is uncompressed and aggressive compression via online tools can bring that down to as little as 600KB.

The other cool thing about working with Blobs is that you can append them directly to FormData objects, which meant that doing a cross origin ajax call to imgur.com to upload the generated gif was a breeze, and a much welcomed addition to the web app.

## What I’ve learned

- URL.createObjectURL is a great api for client generated media, solving so many problems you’d have otherwise.
- Using TypedArrays will boost your data intensive app’s performance a lot.
- Dividing workload between multiple concurrent WebWorkers actually works and helps.
- WebRTC is at a pretty stable point where you can use the media devices of about 40% of internet users.
- It is easy to make an app that lets users generate content without involving your server.
- People really like playing with their web cams. I think using them in a web app makes perfect sense.
- It is easy to fill up 2MB, imgur’s file limit, with gif data.

![thumbs up!](../../assets/44b3af90bf7ec698.gif)


I would also like to thank [Johan Nordberg](https://github.com/jnordberg) and [nobuoka](https://github.com/nobuoka) for their hard work coming up with their JavaScript gif writing libraries.

You can take face to gif for a quick spin, or look at the [source code on github](https://github.com/hdragomir/facetogif/) and fork it, improve it and have lots of fun; Just like I did.

I cannot wait until WebRTC becomes really available on mobile devices too!

## About
[
Horia Dragomir ](http://hdragomir.com)

UI Developer, Hungry and Foolish

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 8 comments

grasteJuly 10th, 2013 at 05:36Horia DragomirJuly 10th, 2013 at 05:44HenriJuly 10th, 2013 at 12:54grasteJuly 10th, 2013 at 13:46Domingos Jorge VelhoJuly 10th, 2013 at 10:56Robert Nyman [Editor]July 10th, 2013 at 11:07FuzzyJuly 18th, 2013 at 07:27Horia DragomirJuly 18th, 2013 at 08:16