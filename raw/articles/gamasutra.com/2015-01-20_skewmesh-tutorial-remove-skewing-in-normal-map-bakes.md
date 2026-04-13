---
title: 'Skewmesh Tutorial: Remove Skewing in Normal map bakes'
url: https://www.gamedeveloper.com/art/skewmesh-tutorial-remove-skewing-in-normal-map-bakes
author: Peter Kojesta
published: '2015-01-20'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Skewmesh Tutorial: Remove Skewing in Normal map bakes

This is a technique we developed to remove skewing on normal maps for mechanical models. It comlpetely eliminates poor skewed normals.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

# Skewmesh Technique

Normal map baking is an art unto itself. In our role as an art outsrouce team, we experiment a lot with new ideas to improve our work, and give better results to our clients. As such, I developed a technique to remove skewing/strange waviness from normal map bakes: Enter the "skewmesh" technique. This tutorial assumes you're using 3dsmax, but it should work in any equivalent application.

### So what is it we're trying to solve?

When baking a normal map , it's important to understand that the vertex normals of your low poly model are averaged in relation to the face normal, so we get skewed results for our normal map details, as seen here on the right:

![](../../assets/6ca7b68c37fecade.img)


Our preference would be no skewing of the details, like so:

![](../../assets/e684aaa7416e0315.img)


in order to achieve this clean bake effect, we use an intermediate mesh known as a "skew mesh". A skewmesh is just your low poly model with a tesselate modifier added to it. Please note that the tension is set to 0. We do this to prevent strange mesh smoothing on the sew mesh.

![](../../assets/6347fb9354bae6a8.img)


Once you've created the skewmesh, you can use it to bake your normal map from your high polygon model. Make sure to bake an object space map (local space/XYZ).

![](../../assets/dac27f763ef01360.img)


Once you've baked your object space map unto your skewmesh, you'll notice that due to the extra points/raycasts, the skewing is gone. The next step is to rebake this local space map to a tangent space map on your actual low polygon model. When doing this transfer, you may want to turn off filter maps in the render setup tp prevent graininess in your normal map(found in "Render Setup -> renderer" tab). Also, make sure to choose "tangent" space maps un the baking options window.

![](../../assets/1f5249a34ce71472.img)


When you've rebaked , you will transfer the clean bake from your skewmesh to your low poly, and all of the skewing will be gone.

![](../../assets/d59d4dba173d64cc.img)


You can do this in max, or Xnormal. Both of which I've done a video tutorial for. Ignore the wierd bake at the end of the Xnromal video, I messed up the settings, but the process is the same. This works great on complex shapes as well:

![](../../assets/d809ce6de6ecdadf.img)


Use this technique, and you'll never have awful waviness again.

Peter Kojesta[http://www.ExisInteractive.com](http://www.ExisInteractive.com)


## 3ds Max:

## Xnormal: