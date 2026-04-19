---
title: For Keep’s Sake! Explained
url: https://www.boristhebrave.com/2020/12/12/for-keeps-sake-explained/
author: Boris
published: '2020-12-12'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I recently entered make [a game](https://boristhebrave.itch.io/for-keeps-sake) for PROCJAM 2020. As I was making it purely for fun (there’s no winners in the competition), I focussed thing to make something that expanded my skills and was technically impressive. As such, there’s lots of interesating techniques that I felt were worth briefly explaning here.

The toy generates castles.

![](../../assets/c7ec350b20fcc916.png)

I modeled a lot of the details after [Corvin Castle](https://en.wikipedia.org/wiki/Corvin_Castle) in Romania. I’ve always loved castles from reading too many fantasy books as a child, and I thought that the shapes they made were a particularly interesting challenge for procedural generation. I think I succeeded, though of course there is much I wasn’t able to do for lack of time. I’ll break down the process step by step.

## Laying the Foundation

Because castles are designed architecturally, but have to conform to the hilly terrain they are placed on, and are rebuild and extended over the years, they have an unusual combination of natural and unnatural features. I’ve tried to replicate that, the generator is based off squares and right angles, but they are curved and angled relative to each other.

To mimic this look, I generate random polygons to form the outline of the building. Each polygon is made by picking some points in a random ring around the center, then ordering them clockwise to form a single shape. There a 10% chance of using a rectangle instead.

Once the outline was established, I filled in the center with a pattern of distorted squares.

![](../../assets/776254a000ada8e4.gif)

The process of doing this is called quadrangulation, and it’s very tricky to do well and robustly. It’s still an active area of research. So, naturally, I cheated. As you can see in the above gif, I repeatedly slice off a line of quads, until I’m left with something small enough. That final shape isn’t necessarily square, so I then subdivide the entire grid. The subdivision process ensures that everything is made out of quads (as, e.g. a pentagon is subdivided into 5 quads, one for each corner of the pentagon).

Finally I apply a variant of [Lloyd’s algorithm](https://en.wikipedia.org/wiki/Lloyd%27s_algorithm) to smooth and relax the mesh. This gives a more curved look and less sharp angles. As the exterior is kept in place, there’s still lots of flat surfaces.

As this process sometimes gives horrible layouts, if the final foundation has any angles more acute than 35 degrees, I throw it out and start over. Sadly, this does exclude a lot of more interesting shapes in favour of generally round polygons.

## Brick by Brick

Once the foundation is in place, I construct the building itself. This was the easiest part of the project, as I re-used the software I’ve already written, [Tessera](https://assetstore.unity.com/packages/tools/modeling/tessera-pro-161077) which already does a lot of the hard work of running the Wave Function Collapse (WFC) algorithm on an arbitrary grid, and distorting the generated tiles to fit together seamlessly. I’ve already [written extensively about WFC](https://www.boristhebrave.com/2020/04/13/wave-function-collapse-explained/).

![](../../assets/5cb09c063b8896d5.gif)

The tile set I ultimately ended up using is a variant of Marching Squares, similar to the sample that comes with Tessera. As WFC copes very well with missing tiles, I only had to create as many as I felt were necessary for the right look.

![](../../assets/fae925ebadb99ef3.png)

I’m not skilled at 3d modelling, so getting the machicolations done was the hardest part.

I also applied some extra rules using the features Tessera offers:

- Certain tiles cannot back onto each other, effectively stopping very thin structures from being generated.
- The castle must be one contiguous unit, which I think looks better.
- The bottom row of tiles cannot contain any roof tiles. This is important as the “stories” of the building are actually offset between two tiles due to the nature of marching cubes. So the bottom row of tiles is sunk 50% into the ground.

## Roofing

At this point I had a castle that looked like this.

![](../../assets/4b6e103c81edff4d.png)

It looks nicely solid, and that flat roof would be appropriate for many castle designs, but I wanted a more gothic look than medieval, so I started investigating how to cover the roof.

I’d made things somewhat difficult for myself thanks to the arbitrary curving shapes of the building. And I’ve found from experience that tile-based approaches don’t do such a great job with rooves. I needed an algorithm that would work with arbitrary shapes.

After some false starts, I discovered the concept of a [Straight Skeleton](https://en.wikipedia.org/wiki/Straight_skeleton), which is basically a mathematical formalism for the shape gabled rooves make when they have a constant slope. I had to import two libraries – [NetTopologySuite](https://github.com/NetTopologySuite/NetTopologySuite) for assistance taking the output of Tessera and converting the top level into a set of polygons with holes, then [StraightSkeletonNet](https://github.com/reinterpretcat/csharp-libs/tree/master/straight_skeleton) for actually computing the desired mesh.

I then calculated [UVs](https://en.wikipedia.org/wiki/UV_mapping) for the output mesh by walking around the perimeter and increasing the u co-ordinate as a function of distance, and setting v to the distance from the perimeter (which is trivial to calculate given the striaght skeleton).

The results are extremely robust to bizarre shapes.

I repeat the same process for the top 3 layers of tiles. The roofs of the lower sections intersect with the building geometry, which fortunately gives a rather good looking effect (at least after amping up the ambient occulsion to hide the seam).

![](../../assets/1b2c7337bc6e5248.png)

## Texturing

Although I did end up generating UVs for the roof, I found once again that the irregular shape of the building was causing problems. I wanted to apply a large brick texture, but it’s virtually impossible to apply a texture automatically to such an irregular shape.

Well, this is PROCJAM isn’t it? Time for some procedurally generated textures. I got [Shader Graph](https://www.youtube.com/watch?v=gJMeSkolnw4) up and running, which conveniently comes with a brick shader. After some playing around, I was able to make some variants of the brick shader. They each show a pattern of bricks with varying colors with a low-frequency noise and an appropriate normal map to impart realism, but they differ in how they map that brick pattern to the mesh geometry.

![](../../assets/d9624d8137880ac9.png)

Variant one uses UVs, like a regular textured mesh. This variant is used for the ceramic tiles on the roof mesh. It’s also used for the sides of the building. The UVs of each building tile don’t line up with each other, every tile just goes from 0 to 1 across each face, so there is a discontinuity at the borders. But as the brick texture is just repeating anyway, and shader ensures that the brick colors don’t repeat, it looks pretty good.

![](../../assets/17cd8170b24a9be5.png)

Shader variant 2 uses the world XZ position. This is used for the unroofed tops of building tiles so they are always square.

Variant 3 is uses cylindrical co-ordinates, used for towers, described later.

![](../../assets/0b31be84922e6482.gif)

## Odds and Ends

While making all this, I found that the end result was still looking kinda blocky. The tiles I am using and the generated rooves all have incredibly sharp edges, which looks unrealistic. So I kept finding additional ways to add more geometry to break up the scene.

The crenellations helped a great deal, but I also randomly found corners of the building and added tower structures. Some of the towers have a cylinder that runs all the way to the ground, others extend out of the building itself, a classic fantasy trope for wizard towers. Inspired by [this generator](https://www.thingiverse.com/thing:1682427), the towers themselves sometimes have extra towers extending out.

The other addition is more subtle: the rooves have brown ridges running along them. This is found by analysing the roof mesh for angles sharper than a given threshold. As well as breaking up the sharpness of the original mesh, it also hides awkward UV seams between, and draws the eye away from the tile based nature of the building itself.

Sadly I didn’t have the time to explore more things to add, there are still many little details that I’d have liked to sell the building as a real place, or add to the epic fantasy feel.

## Conclusion

I’m pretty pleased with how the whole thing came out, and I learnt a lot of new skills. It also helped me clear out some bugs in the experimental version of Tessera I was using. But I still feel a bit disappointed I worked fairly solidly for a week, and have so little to show for it. My [previous project](https://www.boristhebrave.com/2020/07/18/lucky-fluke-post-mortem/) was done in a weekend and feels far more complete. Partly that’s because I was focussing on interesting techniques rather than just making a thing, but also I think that shows the power of teams. Gamedev is hard, you can’t be a master of all unless you are some kind of god.