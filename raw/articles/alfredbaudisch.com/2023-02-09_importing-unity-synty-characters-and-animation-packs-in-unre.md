---
title: Importing Unity Synty Characters and Animation Packs In Unreal Engine 5 (with
  Re-Targeting)
url: https://alfredbaudisch.com/unreal-engine/importing-unity-synty-characters-and-animation-packs-in-unreal-engine-5-with-re-targeting/
author: Alfred Reinold Baudisch
published: '2023-02-09'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

In this post, I show how I imported both character and animation asset packs from the Unity Asset Store into Unreal Engine, and shared animations between models with [UE's IK Rigs Retargeting](https://docs.unrealengine.com/5.1/en-US/unreal-engine-ik-rig/), similarly to Unity's Mecanim. Specifically, the focus are the packs: [Synty's POLYGON Dungeon Characters](https://assetstore.unity.com/packages/3d/environments/dungeons/polygon-dungeons-low-poly-3d-art-by-synty-102677?utm_source=alfredbaudisch&aid=1011lu3e7&utm_campaign=ueretargetpost) and [Kevin Iglesias Basic Motions](https://assetstore.unity.com/packages/3d/animations/basic-motions-157744?utm_source=alfredbaudisch&aid=1011lu3e7&utm_campaign=ueretargetpost).

## Export Content from Unity and import into UE

- Import the asset packs from the Asset Store into a Unity project.
- Look for the FBX files and textures related to the meshes and animations that you want to import into UE.
- If the FBX file has a single mesh and animations, import it as is into Unreal Engine. Do not forget to import as Skeletal Mesh and to also import animations.
- For Synty characters, the FBX file must first be converted to GLTF. See below.

![](../../assets/e350e112db8bf14c.jpg)

![](../../assets/9b5fe3c490eba577.jpg)

### Synty Characters from Unity into Unreal Engine

Synty puts all character skins into a single FBX file:

![](../../assets/20e7a490b37987b1.png)


UE unfortunately always combine meshes from Skeletal Meshes FBX files. So if you try to import Synty's `Characters.fbx`

from Unity into UE, all meshes will be stacked on top of each other:

- Fortunately, UE's GLTF importer allows splitting Skeletal Meshes (thanks to L.F.A from the
[Epic Forums](https://forums.unrealengine.com/t/fbx-file-with-multiple-skeletal-meshes-ue-imports-them-combined-any-way-to-split-them/749057/4?u=alfredbaudisch)for letting me know about that). - The best way I found to convert from FBX to GLTF, was inside Unity.
- Import the open-source Unity package
[UniVRM](https://github.com/vrm-c/UniVRM), which has a FBX to GLTF converter and exporter. - Select your Synty's
`Characters.fbx`

in the Unity Project view and then go to*UnitGLTF -> Export to GLB*, and export the file to`.glb`

.

![](../../assets/c3e15b2e7c3b828d.png)


Now, when importing the file into Unreal Engine 5.1, uncheck *Combine Skeletal Meshes* and then the meshes will be correctly imported separately:

## Create IK Rigs for all packs

In order to share animations between the packs in Unreal Engine, similarly to Unity's Mecanim, you need to **manually create an IK Rig for each of the character and animation packs that you imported**. In my case, I created an IK Rig for BasicMotions and one for the Synty Characters (at least it's one IK Rig per pack, not for each character).

It can be a time-consuming process, but it's worth it, because it enables animation retargeting between Unity's Asset Store packs just like Unity's Mecanim.

I won't go into details on how to do that since it's quite extensive. You can check the official tutorials:

The important thing to notice is that all IK Rigs must share the same chains. As for goals, for the mentioned packs, only 4 goals are needed:

- Arms: RightArm_Goal and LeftArm_Goal
- Legs: LeftArm_Goal and RightArm_Goal

Check my final setup (click to expand):

## IK Retargeter Profiles

To finally be able to retarget and share animations, you need to create IK Retargeter Profiles.

The most important settings are the "Source" and "Target" assets. In this case, the animations come from BasicMotions, so its IKRig is the source. Then, I want to animate the Synty characters with those animations, so I set it as the target:

Also make sure to setup the Chain Mapping:

![](../../assets/e30d78ba7403b295.png)


You can now see the animations in action. If a bone seems wrong or weird, click the bone in the left bone browser and adjust angles, limits and more in the Details panel (click to expand):