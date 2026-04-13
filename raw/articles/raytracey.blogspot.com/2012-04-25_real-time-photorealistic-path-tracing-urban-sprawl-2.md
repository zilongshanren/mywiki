---
title: 'Real-time photorealistic path tracing: Urban Sprawl 2'
url: http://raytracey.blogspot.com/2012/04/real-time-photorealistic-path-tracing.html
author: Sam Lapere
published: '2012-04-25'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Urban Sprawl 2 from Stonemason is a very detailed 3d city model, so it was a no-brainer to test this scene with Brigade. Since the scene rendered much more smoothly than expected, I also threw in a high poly Transformer model to make it a bit more challenging (the materials on the Transformer model still need some tweaking). Surprisingly, Brigade doesn't break a sweat. All the eye candy inherent to path tracing is present: glossy and specular reflection, refraction, global illumination with diffuse color bleeding, ambient occlusion (under the cars) and depth of field. With Brigade performing so great, there's a lot of headroom left for dynamic objects like cars and animated characters (which will be shown in another post). For example, a photorealistic GTA or real-time photorealistic urban planning with dynamic day-night cycle are some of the possibilities.

A plethora of screenshots (some of them have already been shown in previous posts) for thy viewing pleasure:

## 8 comments:

Beautiful stuff once again! You will run out of scenes, you know. :)



Did you receive the latest version from Jeroen, with the tweaked gamma? Also, Jeroen got 30% extra performance today. Somewhere a small mistake was introduced, we stumbled upon it today.

- Jacco.

Small suggestion: pick the three nicest shots, and leave the rest to the video. :)

Jacco, 30% speed increase, that's amazing news! :)



I still have some spare scenes, but I will stick with this one for a while, updating it with dynamic stuff.

Anonymous: thanks, I know :) I always want to show as much as possible in screens, but it also spoils some surprises. I'll try to limit myself to the best screenshots next time.

Great video!


Since noise is hard on video encoding, if you could decouple the rendering resolution from the output resolution, you could render at 640x480 but capture at 720p or 1080p. Then you might benefit from the higher bitrates that youtube streams HD videos at, which might remove some of the youtube encoding artifacts.

Hi Sam. Is it difficut to implement new scene to brigade? Do you have some simple importer or something? For example, scene from 3ds max, how much do you have to twake it?

Anonymous, thanks for the tip, but I'm afraid that if I capture at 720p, the size of the video will increase too much. It already takes half a day to upload a video now.


Vojtech: it depends, some scenes can be loaded pretty easily, others (like the one in this post) need to go back and fourth through multiple programs (daz3d, max, blender, deep exploration) before they can be displayed properly. All these programs encode the same scene slightly differently in obj or collada format. These programs often crash during import or export of huge models, which is a pain. There was a lot of trial and error involved before this scene could be rendered with good performance at all viewpoints. In obj format it gave a massive performance drop, so I had to convert it to collada (multiple times actually). Sometimes you need to alter or remove some of the problematic geometry (which wasn't the case here luckily). Also the materials and textures (diffuse + normal maps) need to be created manually, which can take a while in a scene with over 300 individual materials.

@Sam


What do you use to capture/encode the video? Have you tried something like FRAPS? How large are your uploads?

I'm using FRAPS for capturing. The last video (6 minute video) was almost 4 GB and took 9 hours to upload to Youtube. I think FRAPS doesn't encode noisy images very efficiently which might explain the huge video size. I've tried reencoding the video before upload, but a lot of detail gets lost in the process, so I prefer to upload the raw original video.

Post a Comment