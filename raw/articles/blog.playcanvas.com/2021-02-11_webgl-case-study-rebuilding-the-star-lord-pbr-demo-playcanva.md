---
title: 'WebGL Case Study: Rebuilding the Star-Lord PBR Demo | PlayCanvas Blog'
url: https://blog.playcanvas.com/webgl-case-study-rebuilding-the-star-lord-pbr-demo
author: Will Eastcott
published: '2021-02-11'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

Way back in 2014, [PlayCanvas was the first WebGL Engine to integrate PBR](https://blog.playcanvas.com/physically-based-rendering-comes-to-webgl/) (Physically Based Rendering). To mark the event, we built the Star-Lord tech demo:

In the intervening 6 or so years, PlayCanvas has moved on dramatically. So we decided to leverage all of the latest engine features and republish it.

The most significant improvements are related to load time. Let's start out by comparing some key stats:

|
|---|

[Star-Lord 2021](https://playcanv.as/p/SA7hVBLt/)

** Cache disabled on 100Gbps connection*

Those are some pretty ** significant wins**! So what are the differences between the two builds of the demo? Let's step through them one by one.

### Convert JSON Meshes to GLB[](https://blog.playcanvas.com#convert-json-meshes-to-glb)

In October 2020, [PlayCanvas officially switched](https://blog.playcanvas.com/faster-load-times-with-gltfs-glb-format/) from JSON to glTF 2.0 (GLB) for storing all model and animation data. While gzipped GLB is reasonably similar in size to gzipped JSON, it is up to an order of magnitude faster to parse a GLB file once it has been downloaded. Plus, a GLB file occupies less system memory than the equivalent JSON file. Converting all of the assets from JSON to GLB is a simple process. First, flip the project setting 'Convert to GLB' in the 'Asset Tasks' group to true:

![Convert to GLB](../../assets/658a8868aecc76a0.png)


Now, simply reupload all FBX files and a .glb asset will be generated rather than a .json asset. The last step is to use the Replace command in the right-click context menu to replace the .json asset with the .glb asset (plus any materials as well).

![Switch from JSON to GLB](../../assets/f2287ef9ef0d84ac.gif)


You can then delete the old JSON asset (plus any unreferenced related materials).

### Basis Compress Textures[](https://blog.playcanvas.com#basis-compress-textures)

Last month, [we announced](https://blog.playcanvas.com/basis-texture-compression-arrives-in-playcanvas/) the integration of Basis texture compression into the Editor. Star-Lord was originally configured to use DXT, PVR and ETC compressed textures. A download size comparison is as follows:

| Texture Format | Download Size (MB) |
|---|---|
| DXT | 7.56 |
| PVR | 6.09 |
| ETC1 | 7.18 |
| Basis | 2.38 |

This explains much of the download savings in the updated version.

Fortunately, applying Basis compression to the app's textures is literally a two-click operation:

### Prefilter Cubemaps in the Editor[](https://blog.playcanvas.com#prefilter-cubemaps-in-the-editor)

When PBR first arrived in PlayCanvas, the Editor could not prefilter cubemaps. This conversion had to be performed externally with RGBM format cubemap faces being added to the Editor:

Each cubemap had 6 mip levels with 6 faces for each level. And with 5 different cubemaps, that meant 180 of the demo's 220 HTTP requests were for these PNGs!

These days, the Editor makes is super easy to import 6 HDR cubemap faces, build a cubemap and then prefilter it.

So instead of loading 180 PNGs, the demo now loads just 5 DDS files. Much faster. 🚀

### Asynchronously Load Assets[](https://blog.playcanvas.com#asynchronously-load-assets)

To achieve an optimal load time, it is important to only load what is required to make your app functional. It is arguable that music is not strictly a necessary precondition for your app to start. Therefore, the demo now asynchronously loads the mp3 asset that contains the music track and auto-plays it as soon as it is downloaded. It is 3.9MB which accounts for nearly 40% of the app's payload! So be sure to carefully audit your app for assets that can be streamed instead of preloaded.

Read more about preloading and streaming of assets in the [User Manual](https://developer.playcanvas.com/user-manual/assets/preloading-and-streaming/).