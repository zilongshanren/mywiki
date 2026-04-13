---
title: Snapshot Shaders 2 - Installation Guide
url: https://danielilett.com/snapshot-shaders-2/install-guide/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The installation process for *Snapshot Shaders 2* may look slightly different depending on where you bought the pack.

- If you got the pack through the Unity Asset Store, then you can install it into your project through the Package Manager. Go to
*Window -> Package Manager*on the toolbar, then click the My Assets button on the left-hand side. You will find “Snapshot Shaders 2 for Unity URP” somewhere in this list. Click on it, then click the**Download**button on the right-hand panel. Once it has been downloaded, click the**Import**button that appears and then click the second**Import**button which appears on the pop-up window. - If you bought
*Daniel Ilett’s Ultimate Shader Bundle*through the Asset Store, then go to the store page for*Snapshot Shaders 2*to ‘buy’ the pack for free before following the above steps. - If you got the pack anywhere else, then you will receive a
*.unitypackage*file instead. In Unity, go to*Assets -> Import Package -> Custom Package*in the toolbar and find the*.unitypackage*file, and then click the**Import**button on the pop-up window.

After following these steps, *Snapshot Shaders 2* should now be installed in your project. You may find it useful to read the README.pdf under the *Daniel Ilett/Snapshot Shaders 2* folder.

# Activating Effects

*Snapshot Shaders 2* relies on URP’s Renderer Features and Volume system to render each effect. Please follow these steps to ensure your effects run properly and avoid errors:

- Find your
**URP Renderer Asset**and add the effect(s) you wish to use in the*Renderer Features*section at the bottom of the Inspector.- This asset is located in the
*Assets/Settings*folder if you created a new project using the URP template in the Unity Hub and haven’t changed or added your own URP Renderer asset. - The default asset is named something like “PC_RPAsset” by default, although this name may change in future Unity versions.
*Snapshot Shaders 2*also provides an asset in the*Daniel Ilett/Snapshot Shaders 2*folder, and a pipeline asset which uses the renderer in the root*Daniel Ilett*folder.- This step is
**crucial**! If your effects aren’t included in this list, then they will**not**render, even if you add them to a volume profile in the next step.

- This asset is located in the
- Create a volume profile asset via
*Create -> Volume Profile*and add the effects you want to use to this profile.- You can find a range of pre-built profiles under
*Snapshot Shaders 2/Demo/Profiles*. - If you add an effect to a profile which isn’t included in the renderer’s
*Renderer Features*list, then an error message will be displayed in the Inspector with a button to automatically add it for you.

- You can find a range of pre-built profiles under
- Add a volume to your scene via
*GameObject -> Volume -> {any option}*. - Tweak the settings on your volume profile.
**All effects start in an inactive state**when you first add a volume component to your profile, so don’t panic when you don’t see a difference the moment you add one. Just change a few of the parameters.- Some effects require a texture to function correctly. At least one example texture is supplied for each effect in the
*Snapshot Shaders 2/Textures*folder. - When you select a volume in your scene and start tweaking the settings in its Inspector window,
**you are modifying the source shared volume profile**. If you share that profile between multiple volumes, the changes propagate to all those volumes! If you don’t want that to happen, consider using separate profiles for each of those volumes.