---
title: Intersection Effect Shader with Depth Buffer
url: https://tedsieblog.wordpress.com/2016/10/28/intersection-effect-shader-with-depth-buffer/
author: Ted Sie
published: '2016-10-28'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

Recently, I saw my friend shared [the presentation](https://blogs.unity3d.com/2011/09/08/special-effects-with-depth-talk-at-siggraph/) from Unity Blog by [Kuba Cupisz](https://twitter.com/kubacupisz) and [Ole Ciliox](https://twitter.com/rsxole).

[“SPECIAL EFFECTS WITH DEPTH” TALK AT SIGGRAPH](https://blogs.unity3d.com/2011/09/08/special-effects-with-depth-talk-at-siggraph/)

I have started reading it and made some practices until today.


The presentation contains several features with Depth Buffer which are intersection highlights, force field effect, object outlines and fog.

And I implemented the intersection highlights effect in this practice.

Below are the result and implement steps I have tried to test the intersection effect.

**Depth Buffer**

In order to read Depth Buffer, we had to switch the camera to Depth mode.

using UnityEngine; public class DepthMode : MonoBehaviour { private void Awake() { GetComponent<Camera>().depthTextureMode = DepthTextureMode.Depth; } }

And implemented a simple post effect to verify the Depth Buffer is correct.

![depthtexture](../../assets/064af8f2076443cb.png)


**Intersection Highlights Plane**

Then, we could start to compare the depth value with the world position of the pixel.

Once the depth value approximated the world position z of the pixel, instead the final color with the intersection color.

And we would have the result like this.

![simpleintersection](../../assets/105581672d7b10a9.gif)


**Intersection with glancing and UVs animation effect**

Finally I added the glacing effect and the UVs animation with simple tween animation.

Below are the final results.

![positionanimation](../../assets/da438d352df93ce3.gif)


![scaleanimation](../../assets/3f67939485c231df.gif)


請問這是在deferred or forward rendering模式下實作的?

LikeLike

DepthTextureMode.Depth 模式下使用 Forward 或是 Deferred 都可以

DepthTextureMode.DepthNormals 模式就必須使用 Deferred

LikeLike