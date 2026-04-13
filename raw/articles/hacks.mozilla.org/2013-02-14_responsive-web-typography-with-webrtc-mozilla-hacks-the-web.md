---
title: Responsive Web Typography with WebRTC – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/02/responsive-web-typography-with-webrtc/
author: Marko Dugonjić
published: '2013-02-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/bd466cf5c7cbde5d.png)


I love where emerging web technologies — such as [WebRTC](http://en.wikipedia.org/wiki/WebRTC) (Web Real-Time Communication) and [WebAPI](https://wiki.mozilla.org/WebAPI#APIs) — are headed, because they make it possible to use various parts of hardware that already exist inside our computers, tablets and smartphones to improve the user experience. Responsive Typography with WebRTC is yet another example of a simple concept that could improve people’s experiences.

## Scratch your itch

Ever since the introduction of media queries and the outbreak of responsive web design, it has bothered me somewhat that current responsive web design methods are based on media queries that solely test the width and height of the viewport (alright, and pixel density too) and that we always have to make assumptions about the rest of the context.

Even though device manufacturers try to follow the [reference pixel](http://www.w3.org/TR/css3-values/#absolute-lengths) “treaty”, the inconsistencies (both occasional and severe, depending on the range of the devices you are developing for) can be frustrating and developers have to [construct special media queries](http://alistapart.com/article/a-pixel-identity-crisis) to get around the problem. By defining the reference pixel sizes for their devices, manufacturers consequentially impel people to use each device in a certain way.

In reality, however, people use their devices at different distances. As of yet, there is no clause in the “device purchase agreement” that would bound the new owner to use the device only at a certain reading distance.

There is an array of natural distances, such as the [wrist, palm, lap, desk, wall](https://twitter.com/lukew/status/273453112902172672) (and mall) distance and devices are already used across those multiple distances, regardless of their form factor. I’ve been pondering that problem every once in a while over the last few years and I came to the conclusion that in order to achieve the perfect experience, we’d have to make the device aware of the user’s exact needs and then adjust the screen to match any given reader-device relationship.

The idea to [track proximity](http://www.w3.org/TR/2012/WD-proximity-20120712/) between the user and the screen has probably lingered in the minds of many people in the industry. I know that [Mark Boulton](http://twitter.com/markboulton/) has been advocating the idea of [introducing sensors for better responsive experience](http://www.markboulton.co.uk/journal/a-responsive-experience) and [Tim Brown](http://twitter.com/timbrown/) gave an excellent talk on [Universal Typography](http://vimeo.com/56276418) at [InspireConf](https://2012.inspireconf.com) in Leiden last fall.

Essentially, I have been of the opinion that we need to start using devices to passively collect information, and I have always kept my eyes on the device camera as the most probable component, but never found anything remotely tangible. That is until recently, after I learnt about WebRTC and getUserMedia.

## WebRTC to the rescue

The WebRTC standard and `getUserMedia`

API haven’t been invented for detecting reading distances — at least according to their names. However, the possibility to capture the user in front of the device with getUserMedia appeared to be the missing link that could turn the idea into a working concept. I thought that if I could use the capture and manipulate it with JavaScript, calculating the reading distance would be the easy part. At least until the real [proximity events](http://www.w3.org/TR/2012/WD-proximity-20120712/) become widely supported.

## Good people of the Internet

By the time I started learning about `getUserMedia`

API, a few developers had already developed their own solutions for face recognition and/or head tracking and posted them on [Github](http://github.com) or their personal websites. After some brief testing, I picked out [Headtrackr](https://github.com/auduno/headtrackr/) developed by [Audun Mathias Øygard](https://twitter.com/matsiyatzy), because it already had everything I needed built in.

![](../../assets/30b37b46e946d458.png)


Headtrackr can return the width and height of the rectangle around a recognized face as well as the head distance from the screen. The later was less accurate when I first tested it, so I have sticked to the face recognition part only. In short, I divided the “face width” by the video width to get the face to canvas ratio, which has been used either as a multiplier for the root element font size, or as a simple breakpoint query for the respective stylesheet. Have a look at [the Responsive Typography demo](http://webdesign.maratz.com/lab/responsivetypography/) for different applications.

The Headtrackr code is [well explained](http://auduno.github.com/headtrackr/documentation/reference.html), but everything in this demo is so ridiculously simple and intuitive that you don’t even need to read the documentation to understand how to use it. For the purpose of the demo, I’ve created three custom, yet fairly simple functions that use the information gathered via Headtrackr to manipulate CSS (we’ll use just two of them in this walkthrough).

The tracking performance is far from perfect at this stage and this is not production grade code. However, I hope that it’s going to spark your imagination and give you a clue about what the future brings.

## DIY responsive typography

For the sake of clarity, the code presented in this article is [the simplest version](http://webdesign.maratz.com/lab/responsivetypography/simple/), without the green rectangle that follows the face (whilst you are rocking back and forth in front of your web cam) and without the cool looking, but completely optional parameters, updated every 50 milliseconds.

First, the HTML part:

`video`

element which is used for the stream`canvas`

element where the magic happens (actually, where the video frames are copied into)

```
```

Second, the JavaScript part where some variables are set and Headtrackr is initialized:

```
var d = document,
videoInput = d.getElementById('video'),
canvasInput = d.getElementById('compare');
var htracker = new headtrackr.Tracker({
altVideo : {
ogv: "./media/capture5.ogv",
mp4: "./media/capture5.mp4"
},
calcAngles: true,
ui: false,
headPosition: false,
debug: false
});
htracker.init(videoInput, canvasInput);
htracker.start();
```

So far, so good.

The first function, `updateFontSize`

, is — wouldn’t you know — updating the HTML element’s font size. It could update any other element’s font size too, but if you are already familiar with [em-based media queries](http://blog.cloudfour.com/the-ems-have-it-proportional-media-queries-ftw/), then controlling the HTML element’s font size makes perfect sense, because it corresponds to how the browser built-in text zooming works (with Ctrl/Cmd + +/-).

The `updateFontSize`

function receives only one argument, the facetrackingEvent event and we only need the width property.

```
function updateFontSize(ev) {
var faceWidth = ev.width,
videoWidth = videoInput.width,
face2canvasRatio = videoWidth/faceWidth,
rootSize = Math.round(face2canvasRatio*10)/10 - 1.5 + 10 + 'px';
d.getElementsByTagName('html')[0].style.fontSize = rootSize;
}
```

You have probably noticed that I’ve done some “manual normalizing” to get the rootSize based on the face2canvasRatio just right. This is far from optimal, but it translates face2canvasRatio to an integer adequate enough to be used as a reasonable font size value.

The second function — again without a particularly inventive name — breakPointClass sets the class name on the BODY element depending on the face2canvasRatio value. These breakpoints are determined empirically by observing and tweaking, so feel free to use your own.

```
function breakPointClass(ev) {
var b = d.getElementsByTagName('body')[0],
faceWidth = ev.width,
videoWidth = videoInput.width,
face2canvasRatio = videoWidth/faceWidth;
if (face2canvasRatio > 3.2) {
b.className = 'far';
}
if (face2canvasRatio < 2.2) {
b.className = 'close';
}
if (face2canvasRatio >= 2.2 && face2canvasRatio <= 3.2) {
b.className = '';
}
}
```

Finally, the event listener for the facetrackingEvent event passes the event object (and its properties) to the function of choice:

```
d.addEventListener('facetrackingEvent', function(event) {
updateFontSize(event);
});
// or
d.addEventListener('facetrackingEvent', function(event) {
breakPointClass(event);
});
```

In case you only need the initial value, you can stop the tracker and pause the video streaming to offload the processor:

```
d.addEventListener('facetrackingEvent', function(event) {
htracker.stop();
updateFontSize(event);
videoInput.pause();
});
```

And that’s it! You’ve done it. Take a look at [the complete example](http://webdesign.maratz.com/lab/responsivetypography/simple/).

![](../../assets/a747fcfb3417657e.jpg)


Now that you know how easy it is to [use the built-in hardware](https://wiki.mozilla.org/WebAPI#APIs), you can start bringing your own ideas to life.

## Unleash the Dragon

It’s obvious that we can use technology to improve people’s lives more directly, besides artificially filling the cracks in our broken social patterns (no pun intended). Apart from reading ergonomics, there are many other areas that are barely scratched or that are simply based on proprietary technologies.

For example, we could build and use sensors to monitor heart rate or blood pressure, collect such data on the fly and upload it to the patient’s file on the doctor’s computer. We can use the device’s accelerometer not only to protect the hard drive in the laptop that’s about to hit the floor, but to also alert an impaired person’s caretaker in case of a sudden collapse.

We already use applications like [Runkeeper](http://runkeeper.com) to collect data from our running sessions, why not couple it with the air pressure on that particular route on that particular day, for a more comprehensive dataset? The mere awareness that there are external factors that influence how we perform on a day to day basis, could lessen everyday frustrations and lead to a happier and healthier life.

The ideas are endless and with emerging technologies like [Firefox OS](http://www.mozilla.org/en-US/firefoxos/) and [Geeksphone](http://www.geeksphone.com) we will soon be able to access all sensors built in those tiny devices we all carry around anyway. And by that time, we will have no excuses to not develop new concepts that can make our lives a tiny bit better.

## About
[
Marko Dugonjić ](http://www.maratz.com/)

Marko Dugonjić is a designer from Velika Gorica, Croatia. As the creative and user experience director at [Creative Nights](http://creativenights.com/), he improves customers’ digital experience for local and international clients and occasionally speaks at international web design conferences. He founded [FFWD.PRO](http://ffwd.pro/), a micro-conference and workshops for internet professionals in Croatia. His favorite pet project is [Typetester](http://typetester.org/), a popular online tool for testing screen fonts. He is [@markodugonjic](http://twitter.com/markodugonjic) on Twitter

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 10 comments

GirishFebruary 14th, 2013 at 07:42Robert Nyman [Editor]February 15th, 2013 at 05:05pdFebruary 14th, 2013 at 10:46Marko DugonjićFebruary 14th, 2013 at 12:48HarshaFebruary 14th, 2013 at 19:12Robert Nyman [Editor]February 15th, 2013 at 05:12Marko DugonjićFebruary 15th, 2013 at 05:15e–pFebruary 15th, 2013 at 08:12Sunil SinghFebruary 16th, 2013 at 03:43KaranMarch 8th, 2013 at 04:20