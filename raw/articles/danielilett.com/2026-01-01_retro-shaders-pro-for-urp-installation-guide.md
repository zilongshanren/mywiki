---
title: Retro Shaders Pro for URP - Installation Guide
url: https://danielilett.com/retro-shaders-pro/install-guide/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

If you bought this asset pack on the Unity Asset Store, you can use the package manager to install it. If you got it on itch.io or Gumroad, then you will receve a .unitypackage file, which you can install via *Assets -> Import Package -> Custom Package*.

When you download this pack from any storefront, all the assets will be contained in the *Retro Shaders Pro* folder. You also have access to an installer window which will help you install Shader Graph versions of some of the effects in the pack, which are intended to make it a little easier to extend the shaders with your own functionality (although the Shader Graph versions will lack some of the features). The tool can be opened at any time via *Tools -> Retro Shaders Pro -> Open Installer Window*.

When the **Retro Base Lit** graph is imported into your project, you may see compiler errors related to being unable to import the graph. Please go into *Preferences -> Shader Graph* (before Unity 6) or *Project Settings -> Shader Graph* (Unity 6 and after) to increase the **shader variant limit** – this might need to be at least 512. This is due to the usage of shader keywords for the graph’s lighting capabilities.

# Using the shaders

Create a new material and pick any one of the shaders in the pack from the drop-down list at the top, which will be in a subfolder named *Retro Shaders Pro*. You can then tweak the settings of the shader and attach it to any object.

If you want to use the shaders with a terrain, pick the **Retro Terrain Lit** shader on your material and attach it to the terrain’s material slot. This will automatically pull textures from the terrain data and use these for terrain rendering.

For skyboxes, you can create a material with one of the skybox shaders. The **Cubemap** variant can be applied directly onto the sky by dragging the material into empty space in the scene. For the **Procedural** variant, you’ll need to add a large sphere mesh encapsulating the entire scene and apply it to that.