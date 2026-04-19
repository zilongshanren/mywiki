---
title: 'Notes: Reversing Revopoint Scanner.'
url: https://c0de517e.com/002_reversing_revopoint.htm
author: Angelo Pesce
published: '2023-09-07'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

I have to admit, I bought my (...checking the settings...) iPhone 13 pro back in the day mostly because of its 3d scanning abilities, I wanted to have fun with acqusition of 3d scenes. It turns out that the lidar camera is not that strong, it's still good fun both for "serious" uses photogrammetry is better (RealityScan or the nerf-based Luma.ai)... but I digress...

![SiteScape iOS app.](../../assets/42210b93172c0bca.png)

SiteScape iOS app.
![No NERFs, only nerds.](../../assets/729509abcc2df7d5.png)

No NERFs, only nerds.
Point is, I have been fascinated with 3d scanning for quite a while, so when

[revopoint](https://forum.revopoint3d.com/) came out with a new kickstarter for its "range" scanner, I bit the bullet and got me one.

Unfortunately, as it often happens with new companies and products, albeit the hardware in the scanner is quite competent, the software side is still lacking. A fact that is often brought up in the support forums, the most annoying issue being its propensity to lose tracking of the object being scanned, and thus failing to align frames.

![I assure you, there is no Toshiba Libretto with a keyboard that large...](../../assets/2868e0da97f4a1d4.png)

I assure you, there is no Toshiba Libretto with a keyboard that large...
This is especially infuriating as in theory one could run a more expensive alignment algorithm on the captured frames offline, but the software only works with realtime alignment, and it is not good enough to actually succeed at that.

Well, this is where knowing a bit of (python) programming, a bit about 3d and a dash of numerical optimization can come to rescue.

Luckily, revoscan saves a "cache" of raw frames in a trivial to load format. The output of the color camera is stored straight as images, while the depth camera is saved in ".dph" files - all being the same size: 500kb.

Now... 640*400 is 256000... so it seems that the depth is saved in a raw 2-byte per pixel format, which indeed is the case. Depth appears to be encoded as a 16 bit integer, with actual range going in the frames I've dumped from circa 3000 to 7000, with zero signaling an invalid pixel.

This seems close enough to the spec sheet, which describes the scanner as able to go from 300 to 800mm with a 0.1mm precision. So far so good!

![From the revopoint website.](../../assets/7fb3dcca9f1849eb.png)

From the revopoint website.
I don't want to make this too long, but suffice to say that trying to guess the right projection entirely from the specs I saw, didn't work. In fact, it seems to me the measurements they give (picture above) do not really make for a straight furstum.

![Trying to do some math on pen an paper, from the specs - clearly wrong.](../../assets/a337613aaefff5f5.png)

Trying to do some math on pen an paper, from the specs - clearly wrong.
One idea could be to just scan a simple scene with the included software, either capturing just a single frame (turns out the easiest is to delete all other frames in the "cache" folder, then reopen the scan) or using the included tripod to get a static scan, then convert it to a point cloud with as minimal processing as possible, and try to deduce the projection from there.

Well... that's exactly what I've done.

![Trying to create a scene with a good, smooth depth range and some nice details.](../../assets/f5977136e23929a3.png)

Trying to create a scene with a good, smooth depth range and some nice details.
![How it looks like in RevoScan.](../../assets/d2d375bb6f454fd2.png)

How it looks like in RevoScan.
Point clouds are a well known thing, so of course you can find packages to handle them. For this I chose to work with

[open3d](http://www.open3d.org/) in Python/Jupyter (I use the Anaconda distribution), which is nowadays my go-to setup for lots of quick experiments.

Open3d provides a lot of functionality, but what I was interested on for this is that it has a simple interface to load and visutalize point clouds, to find alignment between two clouds and estimate the distance between clouds.

Not, here is where a lot of elbow grease was wasted. It's trivial enough to write code to do numerical optimization for this problem, especially as open3d provides a fast enough distance metric that can be directly plugged in as an error term. The problem is to decide what parameters to optimize and how the model should look like. Do we assume everything is linear? Is there going to be any sort of lens distortion to compensate for? Do we allow for a translation term? A rotation term? How to best formulate all of these parameters in order to help the numerical optimization routine?

I tried a bunch of different options, I went through using quaternions, I tried optimizing first with some rigid transform compentation by having open3d align the point clouds before computing the error, to isolate just the projection parameters, and then fixing the projection and optimizing for translation and rotation (as unfortunately I did not find a way to constrain open3d alignment to an orthogonal transform) and so on.

At the beginning I was using differential evolution for a global search, followed by Nelder-Mead to refine the best candidate found, but I quickly moved to just doing NM for as a local optimizer and just "eyeballing" good starting parameters for a given model. I did restart NM by hand, by feeding it the best solution it found if the error seemed still large - this is a common trick as there is a phenomenon called "simplex collapse" that scipy does not seem to account for.

In the end, I just gave up trying to be "smart" and optimized a 3x4 matrix... yielding this:

![Eureka! Cyan is the RevoScan .ply exported cloud, Yellow is my own decoding of .dph files](../../assets/5bb90f82ec2305b2.png)

Eureka! Cyan is the RevoScan .ply exported cloud, Yellow is my own decoding of .dph files
In python:


opt_M = [0.,-1.,0.,0., -1.,0.,0.,0. ,0.,0.,-1.,0.] # Initial guess

opt_M = [ 0.00007,-5.20327,0.09691,0.0727 , -3.25187,-0.00033,0.97579,-0.02795, 0.00015,0.00075,-5.00007,0.01569]

#opt_M = [ 0.,-5.2,0.1,0. ,-3.25,0.,0.976,0., 0.,0.,-5.,0.]


def img_to_world_M(ix,iy,d,P=opt_M): # Note: ix,iy are pixel coordinates (ix:0...400, iy:0...640), d = raw uint16 depth at that pixel location

d/=50. # could have avoided this but I didn't want to look at large numbers in the matrix

return np.matmul(np.array(P).reshape(3,4), np.array([(ix/400.0-0.5)*d,(iy/640.0-0.5)*d,d,1]))


with open(dph_file_path, 'rb') as f:

depth_image = np.fromfile(f, dtype=np.uint16)

print(min(depth_image), max(depth_image), min(depth_image[depth_image != 0]))

depth_image = depth_image.reshape(400,640)


subset = [(iy,ix) for iy,ix in np.ndindex(depth_image.shape) if depth_image[iy,ix]!=0]

points = [img_to_world_M(ix,iy,depth_image[iy,ix]) for iy, ix in subset]


Surprisingly... the correct matrix is not orthogonal! To be honest, I would not have imagined that, and this in the end is why all my other fancy attempts failed. I tried with a couple of different scenes, and the results were always the same, so this seems to be the correct function to use.

Now, armed with this, I can write my own offline alignment system, or hack the scanner to produce for example and animated point cloud! Fun!

![Several frames aligned offline.](../../assets/fbde08238cde5fed.png)

Several frames aligned offline.
**Appendix**
- In RevoScan 5, the settings that seemed the best are: "accurate" scanning mode, set the range to the maximum 300 to 1200, fuse the point cloud with the "standard" algorithm set at the minimum distance of 0.1. This still does not produce, even for a single frame, the same exact points as decoding the .dph with my method, as RevoScan seems always to drop/average some points.

- The minimum and maximum scanning distance seem to be mostly limited by the IR illumiation, more than parallax? Too far, the IR won't reach, too near, it seems to saturate the depth cameras. This would explain also why the scanner does better with objects with a simple, diffuse, white albedo, and why it won't work as well in the sun.

![This is probably about ten years old now, around the time Alex Evans (see https://openprocessing.org/sketch/1995/) was toying with structured light scanning, I was doing the same. Sadly, the hard drives with these scans broke and I lost all this :/](../../assets/5e0f4d0892884bfe.png)

This is probably about ten years old now, around the time Alex Evans (see https://openprocessing.org/sketch/1995/) was toying with structured light scanning, I was doing the same. Sadly, the hard drives with these scans broke and I lost all this :/