---
title: Loop from periodic function and offset (Processing) - bleuje
url: https://bleuje.com/tutorial2/
published: '2020-11-28'
source_blog: bleuje
source_site: https://bleuje.com/
category: graphics
fetched: '2026-04-19'
---

This tutorial is about explaining a common method to make animations that loop perfectly.

You basically need 3 things:

- A periodic function (1-periodic)
- What to do with the periodic function
- An offset function

All objects have the same periodic motion or change but with an offset, which can give patterns and a feeling of propagation. Here the periodic function has to be 1-periodic because time goes from 0 to 1.

The word “offset” can often be replaced by “delay” here. A difference can be the fact that the offset could be minus the delay.

For example if we take

- Periodic function: Sinusoid
- Change: Size of a dot
- Offset: Distance from the center

We can get a gif like this

![radialoffset gif](../../assets/759366d941504640.gif)


Here the periodic function that controls the size of black dots is:

The interval [-1,1] of the sinusoid is mapped to [2,8]. The functions map, lerp and constrain (sometimes called clamp outside Processing) are in my opinion essential in creative coding so I strongly advise to learn about them if you haven’t already.

And the (radial) offset is:

The code to draw the black dots is the following:

The important line that means “do the same thing with different offset” is:

There is a minus so that things propagate towards increasing offset values.

Here there’s a function to compute the offset for the sake of clarity of the tutorial but usually I just compute the offset in a variable before using it.

**You can use any offset function, it will loop perfectly.**

Here is the entire code to generate gif frames:

Back to the offset:

You can notice that when the offset is the same modulo 1 we will get the same value of the periodic function at the same time, so here the pattern will be circles repeating every 100 pixels (x and y are positions in pixels).

## More examples

Now let’s use this:

- Periodic function: Sinusoid
- Change: Line rotation
- Offset: (x+2*y)*constant

This gif was obtained:

![rotatinglines gif](../../assets/b3dbac1edfc87762.gif)


The periodic function and the offset were:

The code to draw lines:

The entire code:

Here’s another one, changing the drawing of a face, and using a spiral offset.
The spiral offset is obtained by summing the distance to the center with the angle to the center.
The function `atan2`

is used. `atan2(y,x)`

is the angle of (x,y) to the origin (0,0).

![facesspiral gif](../../assets/dac60bb115f476f3.gif)


Here’s the code:

Using noise (Perlin/simplex/openSimplex noise) as offset can be interesting. For example in the following gif (one of my early gifs) each object oscillates between two positions, and there is 2D noise as offset.

![2dnoise offset gif](../../assets/1e06c7b608c6c287.gif)


Here the examples are in 2D, this also works for 3D stuff.