---
title: Making a first gif with Processing - bleuje
url: https://bleuje.com/tutorial1/
published: '2020-11-28'
source_blog: bleuje
source_site: https://bleuje.com/
category: graphics
fetched: '2026-04-19'
---

This tutorial is about making a basic perfectly looping gif with Processing: a dot doing a circular loop.

![first gif](../../assets/d73b08ef5d5c15d7.gif)


The trajectory of the black dot can be described with maths: the angle depends on time and the radius is fixed. Hence if the radius of the circle is r, the position at time t can be defined with:

Note that if `t`

goes from 0 to 1 (which will always be the case in those tutorials), the position at t=0 is the same as t=1.

So we want to save frames, for example numFrames = 100 frames from t=0 to t=1, but excluding t=1 because this frame is already saved at t=0 (or we take t=1 but not t=0).
t can be defined as `t = 1.0*(frameCount-1)/numFrames`

. In Processing frameCount is incremented each time Processing’s `draw()`

function is called and it is equal to 1 on first call.

Here is the entire code to save frames:

`saveFrame(“fr###.gif”);`

saves frames with a number equal to frameCount and with leading zeros.

In this tutorial I used Processing but you can obviously do the same with your favourite programming tool that’s able to draw and save frames.

## How to make an animated gif from the frames

There are many ways to make animated gifs from frames.

I personally use the command line tool [gifsicle](https://www.lcdf.org/gifsicle/).

Once you have it just run this in your frames folder to make an animated gif:

```
gifsicle --delay=2 --loop fr*.gif > mygifname.gif
```


The delay is in hundredth of second, so here it makes a 50 fps gif.

As far as I know gifsicle only works from .gif frames, but there are lots of other ways to make animated gifs from a set of frames: ffmpeg, GIMP, Photoshop, ezgif.com…

With gifsicle you might want to add the “optimize” flag especially if you want to get a very long gif with few changes between frames.

```
gifsicle --delay=2 --loop --optimize fr*.gif > mygifname.gif
```


For file size optimization I recommend using this website: [ezgif](https://ezgif.com/optimize)

But you can also change optimization parameters and do other things with gifsicle directly.

If this isn’t enough, to have small file sizes you can try:

- having fewer different colors
- having fewer changes between successive frames
- having smaller resolution
- having less frames