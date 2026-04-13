---
title: Simonschreibt.
url: https://simonschreibt.de/gat/stylized-vfx-in-rime-water-edition/
author: Simon
published: '2018-05-01'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This is a talk I gave on the [Unreal Fest Europe 2018](http://unrealfesteurope.com/) about three stylized effects in [RIME](http://www.tequilaworks.com/proyectos/rime/). It’s based on the one I gave 2017 but extended about the water materials of RiME.

![](../../assets/b056c70ebe6dee9f.png)


![](../../assets/b056c70ebe6dee9f.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

Thanks to [Tequila Works](http://www.tequilaworks.com/) for letting me speak about the effects and all the nice people I had the opportunity to speak to at the event. It was awesome!

Unreal Material

To get the material working on your Unreal Version (tested with 4.13 and 4.19.1):

[Download Material Package](https://cloud.simont.de/index.php/s/YwcWFnLwaZptLAp)- Extract directly to your content folder (not in a subfolder!)
- Start Unreal and open the main material:

\Content\BaseMaterials\SeaShaders\Shaders\**OceanMaster_M**

Or the material instance which contains all the settings for the water in Rime Level 1:

\Content\BaseMaterials\SeaShaders\Settings\**Settings_SeaStage1**

Useful Links

**You can find many creations of the RiME-Fire and -Water below the “old” RiME VFX article from 2017!**

[https://simonschreibt.de/gat/stylized-vfx-in-rime/#update1](https://simonschreibt.de/gat/stylized-vfx-in-rime/#update1)

**The Talk from 2017 with more Information about the Fire & Smoke**

[https://simonschreibt.de/gat/stylized-vfx-in-rime/](https://simonschreibt.de/gat/stylized-vfx-in-rime/)

**Julian Love – “Technical Artist Bootcamp: The VFX of Diablo”**

[https://archive.org/details/GDC2013Love](https://archive.org/details/GDC2013Love)

**Tutorial: Ocean Shader with Gerstner Waves**

[https://80.lv/articles/tutorial-ocean-shader-with-gerstner-waves/](https://80.lv/articles/tutorial-ocean-shader-with-gerstner-waves/)

**Fortnite Sky Optimisation**

[https://youtu.be/1xiwJukvb60?t=41m46s](https://youtu.be/1xiwJukvb60?t=41m46s)

**Chromatic Aberration**

[https://en.wikipedia.org/wiki/Chromatic_aberration](https://en.wikipedia.org/wiki/Chromatic_aberration)

[https://simonschreibt.de/gat/teleglitch-rgb-flickering/](https://simonschreibt.de/gat/teleglitch-rgb-flickering/)

**Unreal Custom UVs**

[https://docs.unrealengine.com/en-us/Engine/Rendering/Materials/CustomizedUVs](https://docs.unrealengine.com/en-us/Engine/Rendering/Materials/CustomizedUVs)

![](../../assets/ba0680151067ebbc.png)

[Ninjin42](https://twitter.com/Ninjin42)just mentioned, that the Custom UVs workflow is NOT necessary anymore to move the processing from the Pixel Shader to the Vertex Shader. Since 4.16 there is a new node called “Vertex Interpolator”. You can find more information in the

[Patch Log by searching for “Vertex Interpolator”](https://docs.unrealengine.com/en-us/Support/Builds/ReleaseNotes/4_16).

Here is the part from the Patch Log:

![](../../assets/c6b32ba0b5ec715e.png)

![](../../assets/ba0680151067ebbc.png)

I think I’ve solved the crash problem…

The issue seems to be related to the SeaDiscmesh_Cylinder003 mesh.

Looking at the saved snapshot, its default material seems to be the instance of OceanMaster_M (i see a light blue mesh, about the same colors of the instance).

While on 4.19.3 opening the material goes fine, in an older engine version like 4.15 opening the master material seems to trigger something on referenced assets too (so the mesh): and that makes the engine crash.

I’ve tried to open directly the mesh asset on 4.19 (where the material is ok) and the engine crashes as well: maybe in this version no strange behaviour on referenced assets happens.

If you delete the mesh and try again to open the material, no more crashes even in 4.15 ;)

I’ve tried deleting the mesh because my log file stated:

[2018.05.01-21.34.56:564][409]LogWindows:Error: === Critical error: ===

[2018.05.01-21.34.56:564][409]LogWindows:Error:

[2018.05.01-21.34.56:564][409]LogWindows:Error: Fatal error: [File:D:\Build\++UE4+Release-4.15+Compile\Sync\Engine\Source\Runtime\CoreUObject\Private\UObject\LinkerLoad.cpp] [Line: 3498]

[2018.05.01-21.34.56:564][409]LogWindows:Error: StaticMesh /Game/BaseMaterials/SeaShaders/Mesh/Mergedversion/SeaDiscmesh_Cylinder003.SeaDiscmesh_Cylinder003: Serial size mismatch: Got 6301, Expected 6317

And pointed me to that specific asset.

Hope this helps… (if a proper solution)

Now we should understand what’s the problem of the mesh is :)

Thank for testing! I’ve investigated as well and removed the mesh. I had a problem with a cubemap too but now it seems to work (I tested with 4.13 and 4.191). If you want, here’s a ZIP file:

https://www.dropbox.com/s/vb73kqmamygmc30/unrealContentRimeWater.zip?dl=0

Thanks a lot I had the same crash!

Also excellent talk! As always very useful informations!

luv u bye

But now it works, does it?

Hey Simon! let me tell you that your videos and techniques are blowin’ my mind :D really nice of resources.. however am trying to replicate some of your stuff for study porpouses.. but the mayor problem that am having is about material behavior,for example; if i create a foam material for a mesh behaves the same for all my meshes and particle meshes (i know, it natural)

my question: is there any way to say “hey material am a different object! do something different!” am thinking on panners velocity and stuff like that.

Your articles about zelda wind waker are interesting as hell too :D

thank you for sharing all your work!

Hi Eduardo, please notice that the majority of the work presented on this blog was NOT done by me, I’m just talking about it. But the amazing ideas for the things come from other people.

Regarding your question: You can use “StaticSwitchParameter” to have different behaviors in your material. When you use the material in a material-instance, you can change the state of this switch depending on what behavior you need. I hope this helped :)

https://docs.unrealengine.com/en-us/Engine/Rendering/Materials/ExpressionReference/Parameters

Thank you very much for answer me! it was very useful :D

about the content, i was aware about the fact that some work wasnt made by you, but doenst matter, you rock :D

there is just a few websites dedicated to this kind of stuff.

thank you simon! kind regards :D

I’m on 4.19.2 (Mac), and when I open the material all of the functions from the functions folder (pixel2distance, ocean_gerstner, exp2, etc etc) are listed as “Unspecified Function” in the OceanMaster material and some of the nodes are disconnected. Anybody else have this problem?

Downloading 4.13.2 now to try it there and will try it on Windows when I am able in a few days.

I’m a fool!! I had the wrong folder structure. I placed the unrealContentRimeWater folder in content, rather than just placing the BaseMaterials folder in there. My mistake!

Hi Simon, great talk!

I’m a bit confused, in the OceanMaster material, there are normals going into the Normal slot on the master output node.

I thought you couldn’t do that with unlit material? What are the normals in that slot affecting? Is it just for the refraction?

Does anyone have the material files still by any chance? I watched this 2 years too late and the Dropbox link is dead now sadly. :(

Thanks for the hint, I’ve corrected the link.

Does anyone have the material files still by any chance? the Dropbox link is dead now sadly

thanks i download it

hi simon i need the dropbox to download the link does not work