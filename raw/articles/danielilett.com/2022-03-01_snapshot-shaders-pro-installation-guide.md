---
title: Snapshot Shaders Pro - Installation Guide
url: https://danielilett.com/snapshot-shaders-pro/install-guide/
author: Daniel Ilett
published: '2022-03-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The installation process might look different depending on where you got the pack from.

On the Unity Asset Store, you will get the Complete version, which has the built-in files already installed and separate packages for URP and HDRP. If you are using a different pipeline, please delete the **Snapshot Shaders Pro/Built-in Pipeline** folder. Then, use the installer window (*Tools -> Snapshot Shaders Pro -> Open Installer Window*) and install the package for your pipeline of choice. I realize that this is annoying, but this is a requirement for the Asset Store - I can’t bundle the Built-in version into a package.

If you downloaded from itch.io or Gumroad, then you can download an individual package for your pipeline. Use *Assets -> Import Package -> Custom Package* to import it. You can also get the Complete version, in which case, see above.

# Activating effects

Use the following instructions to enable effects in your chosen pipeline.

# ✨ Universal Render Pipeline (URP)

- Find your
**URP Renderer Asset**and add the effect(s) you wish to use in the**Renderer Features**section at the bottom of the Inspector.- This asset is most commonly found in the
*Assets/Settings*folder if you created a new project using the URP template from the Unity Hub. - This asset will be named something like
*“UniversalRP-HighQuality”*(Unity versions 2022.3 and prior) or*“PC_RPAsset”*(Unity 6) by default. *Snapshot Shaders Pro*also includes a ready-made asset named*“SnapshotRP”*which has every effect pre-added.

- This asset is most commonly found in the
- Create a volume profile asset via
*Create -> Volume Profile*and add the same effects you want to use to the profile.- You will also find preset profiles in the
*Demo/Profiles*folder. - This step is
**crucial**- your effects won’t do anything if they are not in this list, even if you have a volume profile in your scene.

- You will also find preset profiles in the
- Add a volume to your scene and attach the volume profile.
- Tweak the settings on your volume profile.
**All effects start in an inactive state**on a new volume profile, so don’t panic if you don’t see any difference when you add them. Take note of which effects require textures to work properly (they are listed in the full effect list).

# ✨ High Definition Render Pipeline (HDRP)

- Go to
*Project Settings -> HDRP Default Settings -> Custom Post Process Orders*and add each effect you want to use to the*After Post Process*section. The only exception to this is the**Light Streaks**effect, which is in the*Before Post Process*section. - Create a volume profile asset via
*Create -> Volume Profile*and add the same effects you want to use to the profile. - Add a volume to your scene and attach the volume profile.
- Tweak the settings on the volume profile. All effects will start in an inactive state. Take note of which effects require textures to work properly.

# ✨ Built-in Render Pipeline

- Add a
*Post Processing Layer*component to the camera you will use to render the effects. - Set a layer mask to determine which volumes in which layers will be activated by this camera.
- Create a volume profile asset via
*Create -> Post Processing Profile*and add the same effects you want to use to the profile. - Add a
*Post Processing Volume*to your scene and attach the volume profile. - Tweak the settings on the volume profile. All effects will start in an inactive state. Take note of which effects require textures to work properly.