---
title: StungaLab – 21³ Cubic Animation Tech Note
url: https://cmwdexint.com/2018/03/26/21%c2%b3-cubic-animation-tech-documentation/
author: Ming Wai Chan
published: '2018-03-26'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

Me and a few of my friends ([StungaLab](https://www.facebook.com/StungaLab/)) decided to create this animation from last year and I’m responsible for all Unity things – setup / shaders / tools / plug-ins etc. I didn’t help a lot as I have my full-time job in UK so most of the work are actually done by the 2 amazing 3D artists [Felix Yin-Zhen Chu](https://www.artstation.com/felixchuyz) and [Shadow Chi-Ho Wong](https://www.artstation.com/shadowwong65), also 2D part by Carol Tsz-Ching Ng. It is the first time for us all to put ourselves into such a big production — target at high quality, massive amounts of assets, and short time-frame, ~~(esp. ) lack of knowledge of using Unity (they are almost the first time Unity user).~~ The final animation really surprised me.


I only have mobile game development experience in the past so there was no way for me to grab so many plug-ins and use so many expensive graphics features in any projects. So I had no idea how to correctly set things up for a project like this. Glad that I work in Unity and the knowledge I gained supported me a good start.

##### Note: Not everything shown in this blog are being used. But they are the stuff I worked on so I hope to keep them here as a log.



# Setup


![made-with-unity-black](../../assets/4f9864f096998b88.png)


– From Unity 2017.1 to Unity 2017.3 (Free Personal)

– Deferred pipeline

– DX11 only

– Linear color space

– In Quality / Graphics / Player settings

we enabled the features to make sure we get highest rendering quality

– Git, Bitbucket, Sourcetree for source control


# Preview


Here shows the breakdown of visual components in a shot :

![026_f](../../assets/b5b45b6167256f3d.jpg)


Most of the time were spent on design – 3D modeling – texturing – import and integration in Unity – lighting – post-processing settings, and of course, animation. Again, the 3D by the artists are incredible. Just the default standard shader is good enough to create a scene like this.

And some of our old screenshots :

![cubic5](../../assets/3f6aa84c5d6bb305.png)

![capture_03](../../assets/c0e23e23dbc43954.png)



# Environment


### Tessellation on rail track ballast

The track ballast details are generated with a modified Standard Shader — added distance-based tessellation support to it. Normals are recalculated with the height map.

![004b](../../assets/e73cbb437ddc230f.gif)

![004](../../assets/6aad1237a795c1c5.gif)



### Translucent tube

Unity’s default standard shader doesn’t support translucent, and using third party’s translucent shader won’t match the PBR lighting. So again, I have to create another modified standard shader for the translucent effect.

![007](../../assets/07024b42fabda623.png)

![007](../../assets/22b47714fcf7a0cc.gif)



### Black mask

The track has ending. When camera is close enough to the end we will see the “sharp-cut” of the props.

![022](../../assets/12ebc1a6d642ff51.jpg)


I made a black blocker shader which fades according to distance and blending with other props smoothly (using soft particle shader approach).

![022b](../../assets/0c1fdd4262389055.jpg)


So we can fake the endless darkness…

![022](../../assets/f3c18fdc5ecdcc15.gif)




# Character shaders


### Robot’s eye

I used the new Unity 2017.1 feature called Custom Render Texture which we can modify a part of texture with shader very easily. The main point is, I don’t have to make another modified standard shader for the robot eye animation.

![006b](../../assets/bbfedb08c34dea37.gif)


![drone.gif](../../assets/2b71ba74ebd14ab1.gif)


The animation is done with a script which allows the animation editor to control the attributes on the custom render texture shader / material.

![006](../../assets/60516a0f85ef2aac.gif)


This approach can also work on transition between 2 textures :

![erode.gif](../../assets/9c65f6138e3ddea9.gif)



### Girl’s hair Anisotropic highlight

Hair’s shading is different with other objects. So, one more modified Standard Shader is created with addition of anisotropic lighting highlight.

![009b](../../assets/d37389cc294665eb.png)

![009](../../assets/f9eead2e16a2d509.png)

![009](../../assets/1ef4ca59cc165271.gif)





# Effects


### Water Drop

We were suppose to make a water drop and put it on one of the tents. Too lazy to render sprites so I just created a shader which only needs 1 texture to do the whole thing.

![008](../../assets/f5d5759f404ce82f.gif)

![008](../../assets/b0417ac02159d360.jpg)



### Radial zoom blur

A really fake one. Grab pass in shader and sample the texture based on screen positions and loop for about 16 times to do the blur.

![005](../../assets/12f7ea2a19435cec.gif)

![005](../../assets/f41a42573247e5aa.png)



### Monitor glitches

Separated RGB channel in shader to be the monitor-pixel effect for close-ups.

![002ba](../../assets/6eeef085ceb5519a.gif)


Again, this is also applied on custom render texture and applied to the screen object material. Artists just have to animate these properties.![003](../../assets/25e31264236ff3b6.gif)



### Depth transition

A custom post-processing effect for doing transition between 2 styles. It uses the `_CameraDepthTexture`

in shader.

![023b](../../assets/0e501477b6156bab.gif)


Added some distortion effects to the depth UV as well as the camera texture UVs![023](../../assets/10076ef89caca7c6.gif)



### Fake volumetric spotlight halo

Since volumetric lighting rendering is too expensive so we can fake it like this. The shader is just a rim shader which fades from “inside” to “outside”

![024](../../assets/60316b21b98a2b8a.jpg)

![024b](../../assets/36a5ff1a78c934b9.gif)





# Utilities


### Physics Object Dropping

I created a tool for dropping objects with physics so that we don’t have to place little stones one by one manually.

![010](../../assets/899f124ece881631.gif)



### Random object placing / projection

Another mode of the tool which project random objects according to the surfaces.

![011](../../assets/9887a8af0eafce7a.gif)


More control for scale, rotation, preview of next random object.

![013](../../assets/f9d1cdeb6342c960.gif)

![012](../../assets/bb7e7ef14a764e87.gif)



### Game controller

Our project is made in Unity, so why not make a game controller to wonder the beautiful scene?

![gamecontroller](../../assets/f364d063040995a6.gif)



## Plug-ins


I used a lot of plug-ins because they are just great.

[Unity – Post-processing Stack V2
](https://github.com/Unity-Technologies/PostProcessing)The great thing for V2 is that it allows blending between 2 post-processing volumes.

![026](../../assets/351eed66dd4b5be3.gif)

[Unity – Recorder](https://assetstore.unity.com/packages/essentials/beta-projects/recorder-94079)

This is the tool we used to output the frames for the animation video.

![020](../../assets/b70f2d1bf85241fc.jpg)


Unity – Standard Particle Shader (built-in now)

Unity – Timeline & Cinemachine (built-in now)

![025](../../assets/550bb30f5c60887e.jpg)


[FBX exporter](https://github.com/KellanHiggins/UnityFBXExporter)

[Volumetric Lighting
](https://forum.unity.com/threads/true-volumetric-lights-now-open-source.390818/)

[Unity – Deferred Decal](https://blogs.unity3d.com/2015/02/06/extending-unity-5-rendering-pipeline-command-buffers/)


### Challenges


The greatest challenge :

- Source control with artists and between artists. Fixing their merge conflicts, sort out their pulling-commit-pushing orders…
- Create tools that they are willing to use. I have been complained for a several times about being too technical.
- Lack of knowledge. Modifying standard shader struggled me a lot and especially those have to change the lighting models.
- UK-HK remote work. It’s so hard to work remotely + the huge time difference. Artists solved quite a lot of technical problems while I was sleeping.😂

Besides the items in above sections, there were actually a lot of other stuff were made to backup different little things… modified blood decals, particle effects, shear effects on character shaders, cat sprite outline extraction, lighting studies, fur, render target debug viewers, script to clear motion vector between shots … etc.

![image24](../../assets/7779b5b50870f907.gif)

![030](../../assets/568de0ab3699fae8.gif)

![image32](../../assets/4d87c9c92a1cbee9.jpg)


The stuff I did was obviously not good enough. But this was a great opportunity to get my hands on high quality graphics project. Hope you all like the animation!

Visit [here](https://www.artstation.com/artwork/akAd9) for more beautiful rendering. 🙂



Maybe try motion capture…

LikeLike