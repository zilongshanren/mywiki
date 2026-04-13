---
title: Building 2d sprites from 3d models using Blender
url: https://blog.gemserk.com/2011/07/20/building-2d-sprites-from-3d-models-using-blender/
published: '2011-07-20'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

In this post I want to share the process used to create the [ship sprite sheet](https://github.com/gemserk/superflyingthing/raw/459c03b516ad72af94bbd2211b4d8f850938259e/superflyingthing-desktop/src/main/resources/data/images/ship_animation.png) of Super Flying Thing (STF from now on). I will assume you have a basic experience with Blender or software alike.

## Model and texture

The first step will be to get or create a model you want for the sprite sheet. In my case, the ship was created from zero, following this [excellent tutorial](http://www.celsiusgs.com/blog/?p=326) (a bit boring to watch, but great content). Of course, as I am not an artist and I only dedicated three hours, my model sucks a bit compared to the one of the tutorial.

## Set the camera

Now that you have a model, you will have to configure the camera for the Blender rendering process. The idea is to put it pointing to the model, and bring it closer to the model until you get it in the camera view port. The next image shows an example:

In the case of SFT, I configured the view port to be 64x64.

## Create the animation

Now, you have to create the animation you want to render. For SFT, I wanted to create the animation of ship rotating 360 degrees. As the speed of the ship is approx 300 degrees per second, and I was using a 30FPS animation, then I wanted to have the matching frames for the complete rotation animation, in this case, 36 frames. So I created one key frame for 0 degrees, 90, 180, 270 and 360 degrees. The last one is only used to complete the interpolation and is not included in the final animation.

Be sure to configure the animation to use a linear interpolation to match the frame with the ship’s angle, unless you want otherwise. To do that, open the Graph Editor, and from Key menu modify Interpolation Mode to Linear.

Finally, export the animation using Render animation from blender, it will create each frame of the animation in your temp folder. Be aware you will get a better result using an Anti-Aliasing algorithm, for example, [Catmull-Rom](http://www.spot3d.com/vray/help/150SP1/examples_image_sampler.htm), thanks [void256](http://nifty-gui.lessvoid.com/) for the tip.

Here is the difference:

![](../../assets/934aea543f0b3b9e.png)


The left image is not using anti aliasing at all, the right one is using Catmull-Rom with 16 samples per pixel.

And here is the animation:

![](../../assets/7fb69aea295d301a.gif)


The process is tools independent, so you could use, for example, 3D Studio if you want. You only need a good artist, as we do.

As always, hope you like the post and it could be of help.