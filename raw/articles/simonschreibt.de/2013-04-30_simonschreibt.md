---
title: Simonschreibt.
url: https://simonschreibt.de/gat/doom-3-modding-notes/
author: Simon
published: '2013-04-30'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

The following stuff is only important for Modders! I just do some notes about what i learned during my investigation.

# Export & test assets from 3Ds Max to Doom 3

**3Ds Max Material**

The documentation (iddevnet) says two different things. The truth is, that you have to define *only* the diffuse texture in 3Ds Max. **NOT** the specular and/or normal map like it’s said [here](http://www.iddevnet.com/doom3/modelexport_3dsmax.php). The texture itself isn’t important here, the texture **name** is!

*C:\Spiele\Steam\SteamApps\common\Doom 3\base\models\tb\tb.tga*

Your material has to be named like this:

**models\tb\tb** (without the .TGA)


**3Ds Max Multi Material**

If you want to have several materials on one object, you have to separate the faces physically. At the end you will have several objects! It’s not enough to just assign the materials to different faces and let the object be one piece. This will exported perfectly but isn’t interpreted by Doom 3!

**3Ds Max ASE Export**

3Ds Max already has an ASE exporter. But you have to check the option for UV Layout/Vertex Color/Normals which aren’t checked as default!


**Paths & Steam Version**

Since you shall store you assets (also the .MAX file) right in the Doom 3 directory you get problems with the Steam version because it installs the game to “Doom 3” and [there are no space (” “) allowed in the path](http://www.iddevnet.com/doom3/modelexport.php)!

After the ASE export you have to delete every space out of the path in the ASE file. You don’t need the whole path. You can delete everything before the “base” directly and put “\\” in front of it:

**Before**: *BITMAP “C:\Spiele\Steam\SteamApps\common\Doom 3\base\models\tb\tb.tga”

**After**: *BITMAP “\\base\models\tb\tb”

**MTR Material File**

The material file has to lay in the **MATERIALS Folder** and not where all the other assets are. The stupid thing what happened to me was, that Doom 3 will show the diffuse texture on the model (i guess the game takes this information from the ASE file) even it couldn’t find the material file! The lighting will be totally wrong and also normal/specular files will not show up.

**MTR File Extensions**

You never need to write .TGA/.DDS or whatever. Neither in the ASE files, nor in the material files. My material file (base\materials\tb.mtr) looked like this (unsmoothedTangents is a keyword which can help if you have lighting problems on you model):

models\tb\tb


{

unsmoothedTangents

diffusemap models\tb\tb

bumpmap models\tb\tb_local

specularmap models\tb\tb_s

}