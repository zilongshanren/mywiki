---
title: The Visibility Monitor supported by Gaia – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/10/the-visibility-monitor-supported-by-gaia/
author: John Hu
published: '2014-10-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

With the booming ultra-low-price device demands, we have to more carefully calculate about each resource of the device, such as CPU, RAM, and Flash. Here I want to introduce the [Visibility Monitor](https://github.com/mozilla-b2g/gaia/blob/eb04b0228011a34b8c45d1fc675a6b9b7965b79d/shared/js/tag_visibility_monitor.js) which has existed for a long time in Gaia.

## Origin

The Visibility Monitor originated from the Gallery app of Gaia and appeared in [Bug 809782](https://bugzilla.mozilla.org/show_bug.cgi?id=809782) (gallery crashes if too many images are available on sdcard) for the first time. It solves the problem of the memory shortage which is caused by storing too many images in the Gallery app. After a period of time, Tag Visibility Monitor, the “brother” of Visibility Monitor, was born. Both of their functionalities are almost the same, except that [Tag Visibility Monitor](https://github.com/mozilla-b2g/gaia/blob/master/shared/js/tag_visibility_monitor.js) follows pre-assigned tag names to filter elements which need to be monitored. So, we are going to use the Tag Visibility Monitor as the example in the following sections. Of course, the Visibility Monitor is also applicable.

For your information, the Visibility Monitor was done by JavaScript master David Flanagan. He is also the author of [JavaScript: The Definitive Guide](http://shop.oreilly.com/product/9780596805531.do) and works at Mozilla.

## Working Principle

Basically, the Visibility Monitor removes the images that are outside of the visible screen from the DOM tree, so Gecko has the chance to release the image memory which is temporarily used by the image loader/decoder.

You may ask: “The operation can be done on Gecko. Why do this on Gaia?” In fact, Gecko enables the Visibility Monitor by default; however, the Visibility Monitor only removes the images which are image buffers (the uncompressed ones by the image decoder). However, the original images are still temporarily stored in the memory. These images were captured by the image loader from the Internet or the local file system. However, the Visibility Monitor supported by Gaia will completely remove images from the DOM tree, even the original ones which are temporarily stored in the image loader as well. This feature is extremely important for the Tarako, the codename of the Firefox OS low-end device project, which only equips 128MB memory.

To take the graphic above as the example, we can separate the whole image as:

- display port
- pre-rendered area
- margin
- all other area

When the display port is moving up and down, the Visibility Monitor should dynamically load the pre-rendered area. At the same time, the image outside of the pre-rendered area will not be loaded or uncompressed. The Visibility Monitor will take the margin area as a dynamically adjustable parameter.

- The higher the margin value is, the bigger the part of the image Gecko has to pre-render, which will lead to more memory usage and to scroll more smoothly (FPS will be higher)
- vice versa: the lower the margin is, the smaller the part of the image Gecko has to pre-render, which will lead to less memory usage and to scroll less smoothly (FPS will be lower).

Because of this working principle, we can adjust the parameters and image quality to match our demands.

## Prerequisites

It’s impossible to “have your cake and eat it too”. Just like it’s impossible to “use the Visibility Monitor and be out of its influence.” The [prerequisites to use the Visibility Monitor](https://github.com/mozilla-b2g/gaia/blob/0a0f549c6b341b8b14c4188390abbefe52847cb4/shared/js/tag_visibility_monitor.js#L46-L51)) are listed below:

### The monitored HTML DOM Elements are arranged from top to bottom

The original layout of Web is from top to bottom, but we may change the layout from bottom to top with some CSS options, such as flex-flow. After applying them, the Visibility Monitor may become more complex and make the FPS lower (we do not like the result), and this kind of layout is not acceptable for the Visibility Monitor. When someone uses this layout, the Visibility Monitor shows nothing at the areas where it should display images and sends errors instead.

### The monitored HTML DOM Elements cannot be absolutely positioned

The Visibility Monitor calculates the height of each HTML DOM Elements to decide whether to display the element or not. So, when the element is fixed at a certain location, the calculation becomes more complex, which is unacceptable. When someone uses this kind of arrangement, the Visibility Monitor shows nothing at the area where it should display images and sends error message.

### The monitored HTML DOM Elements should not dynamically change their position through JavaScript

Similar to absolute location, dynamically changing HTML DOM Elements’ locations make calculations more complex, both of them are unacceptable. When someone uses this kind of arrangement, the Visibility Monitor shows nothing at the area.

### The monitored HTML DOM Elements cannot be resized or be hidden, but they can have different sizes

The Visibility Monitor uses [MutationObserver](https://developer.mozilla.org/en/docs/Web/API/MutationObserver) to monitor adding and removal operations of HTML DOM Elements, but not appearing, disappearing or resizing of an HTML DOM Element. When someone uses this kind of arrangement, the Visibility Monitor again shows nothing.

### The container which runs monitoring cannot use *position: static*

Because the Visibility Monitor uses *offsetTop* to calculate the location of display port, it cannot use *position: static*. We recommend to use *position: relative* instead.

### The container which runs monitoring can only be resized by the resizing window

The Visibility Monitor uses the *window.onresize* event to decide whether to re-calculate the pre-rendered area or not. So each change of the size should send a *resize* event.

## Tag Visibility Monitor API

The Visibility Monitor API is very simple and has only one function:

```
function monitorTagVisibility(
container,
tag,
scrollMargin,
scrollDelta,
onscreenCallback,
offscreenCallback
)
```

The parameters it accepts are defined as follows:

- container: a real HTML DOM Element for users to scroll. It doesn’t necessarily have be the direct parent of the monitored elements, but it has to be one of their ancestors
- tag: a string to represent the element name which is going to be monitored
- scrollMargin: a number to define the margin size out of the display port
- scrollDelta: a number to define “how many pixels have been scrolled should that shoukd have a calculation to produce a new pre-rendered area”
- onscreenCallback: a callback function that will be called after a HTML DOM Element moved into the pre-rendered area
- offscreenCallback: a callback function that will be called after a HTML DOM Element moved out of the pre-rendered area

Note: the “move into” and “move out” mentioned above means: as soon as only one pixel is in the pre-rendered area, we say it moves into or remains on the screen; as soon as none of the pixels are in the pre-rendered area, we say it moves out of or does not exist on the screen.

## Example: Music App (1.3T branch)

One of my tasks is to the add the Visibility Monitor into the 1.3T Music app. Because lack of understanding for the structure of the Music app, I asked help from another colleague to find where I should add it in, which were in three locations:

- TilesView
- ListView
- SearchView

Here we only take TilesView as the example and demonstrate the way of adding it. First, we use the [App Manager](https://developer.mozilla.org/en/Firefox_OS/Using_the_App_Manager) to find out the real HTML DOM Element in TilesView for scrolling:

With the App Manager, we find that TilesView has `views-tile`

, `views-tiles-search`

, `views-tiles-anchor`

, and `li.tile`

(which is under all three of them). After the test, we can see that the scroll bar shows at `views-tile`

; `views-tiles-search`

will then automatically be scrolled to the invisible location. Then each tile exists in the way of `li.tile`

. Therefore, we should set the container as `views-tiles`

and set tag as `li`

. The following code was used to call the Visibility Monitor:

```
monitorTagVisibility(
document.getElementById('views-tile'),
'li',
visibilityMargin, // extra space top and bottom
minimumScrollDelta, // min scroll before we do work
thumbnailOnscreen, // set background image
thumbnailOffscreen // remove background image
);
```

In the code above, `visibilityMargin`

is set as 360, which means 3/4 of the screen. `minimumScrollDelta`

is set as 1, which means each pixel will be recalculated once. `thumbnailOnScreen`

and `thumbnailOffscreen`

can be used to set the background image of the thumbnail or clean it up.

## The Effect

We performed practical tests on the Tarako device. We launched the Music app and made it load nearly 200 MP3 files with cover images, which were totally about 900MB. Without the Visibility Monitor, the memory usage of the Music app for images were as follows:

```
├──23.48 MB (41.04%) -- images
│ ├──23.48 MB (41.04%) -- content
│ │ ├──23.48 MB (41.04%) -- used
│ │ │ ├──17.27 MB (30.18%) ── uncompressed-nonheap
│ │ │ ├───6.10 MB (10.66%) ── raw
│ │ │ └───0.12 MB (00.20%) ── uncompressed-heap
│ │ └───0.00 MB (00.00%) ++ unused
│ └───0.00 MB (00.00%) ++ chrome
```

With the Visibility Monitor, we re-gained the memory usage as follows:

```
├───6.75 MB (16.60%) -- images
│ ├──6.75 MB (16.60%) -- content
│ │ ├──5.77 MB (14.19%) -- used
│ │ │ ├──3.77 MB (09.26%) ── uncompressed-nonheap
│ │ │ ├──1.87 MB (04.59%) ── raw
│ │ │ └──0.14 MB (00.34%) ── uncompressed-heap
│ │ └──0.98 MB (02.41%) ++ unused
│ └──0.00 MB (00.00%) ++ chrome
```

To compare both of them:

```
├──-16.73 MB (101.12%) -- images/content
│ ├──-17.71 MB (107.05%) -- used
│ │ ├──-13.50 MB (81.60%) ── uncompressed-nonheap
│ │ ├───-4.23 MB (25.58%) ── raw
│ │ └────0.02 MB (-0.13%) ── uncompressed-heap
│ └────0.98 MB (-5.93%) ── unused/raw
```

To make sure the Visibility Monitor works properly, we added more MP3 files which reached about 400 files in total. At the same time, the usage of memory maintained around 7MB. It’s really a great progress for the 128MB device.

## Conclusion

Honestly, we don’t have to use the Visibility Monitor if there weren’t so many images. Because the Visibility Monitor always influences FPS, we can have Gecko deal with the situation. When talking about apps which use lots of images, we can control memory resources through the Visibility Monitor. Even if we increase the amount of images, the memory usage still keeps stable.

The margin and delta parameters of the Visibility Monitor will affect the FPS and memory usage, which can be concluded as follows:

- the value of higher marginvalue: more memory usage, FPS will be closer to Gecko native scrolling
- the value of lower margin: less memory usage, lower FPS
- The value of higher delta: memory usage increases slightly, higher FPS, higher possibility to see unloaded images
- the value of lower delta: memory usage decreases slightly, lower FPS, lower possibility to see unloaded images

## About
[
John Hu ](http://john.hu)

John Hu is a front-end engineer from Mozilla Taipei office and based in Taiwan. Hu is a peer of video app and mainly focuses on the Gaia of Firefox OS. Currently, he joined the emerging device team who tries to bring the Firefox OS into unknown world. John Hu has about 10 years experiences on software development, including web services, window applications, and embedded softwares. One of his app published globally is miidio recorder which is a well designed Android MP3 recorder. He is interested in learning new things, like Raspberry Pi, 3D printer and welcome to contact him.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## One comment

Fawad HassanOctober 28th, 2014 at 14:19