---
title: Multi-GPU Game Engine
url: http://diaryofagraphicsprogrammer.blogspot.com/2015/05/multi-gpu-game-engine.html
author: Wolfgang Engel
published: '2015-05-31'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Many high-end rendering solutions for -for example- battlefield simulations can utilize now hardware solutions with multiple consumer GPUs. The idea is to split up computational power in-between 4 - 8 GPUs to increase the level of realism as much as possible.

Now with more modern APIs like DirectX 12 and probably Vulcan and before that CUDA, splitting up the rendering pipeline can happen in the following way:

- GPU0 - fills up the G-Buffer after a Z pre-pass

- GPU1 - Renders Deferred Lights and Shadows

- GPU2 - Renders Particles and Vegetation

- GPU3 - Renders Screen-Space Materials like skin etc. and PostFX


Now you can use the result of GPU0 and feed it to GPU1 and then feed it to GPU2 and so on. All this will run in parallel but will introduce two or three frames of lag (depending on how you light Particles and Vegetation). As long as the system renders 60 fps or 120 fps this will not be as much noticeable (obviously one of the targets is to have a high framerate to make animations look smooth and then also having 4K resolution rendering). GPU4 and higher can work on Physics, AI and other things. There is also the opportunity to spread out G-Buffer rendering over several GPUs, like one GPU is doing the Z pre-pass, then another fills up diffuse, normal and probably some geometry data to indentify different objects later or store their edges and another GPU is filling up the terrain data. Vegetation can be rendered on a dedicated GPU etc. etc.. On the CPU side the rule of thumb is that at least 2 cores are needed for one GPU. It is probably better to go for 3 or four. So a four GPU machine should have 8 - 16 CPU cores and a eight GPU machine 16 - 32 CPU cores; which might be split between several physical CPUs. We need at least 2x as much CPU RAM as the GPUs have RAM, so if four GPUs have each 2 GB, we need at least 16 GB Ram, if we have eight GPUs, we need at least 32 GB RAM etc..

A 4K resolution consists of 3840 × 2160 pixels and it will occupy with four render targets, each 32-bit per pixel (8:8:8:8 or 11:11:10), roughly 126.56 MB. This number goes up with 4x or 8x MSAA and maybe super-sampling. It is probably save to assume that the G-Buffer might occupy between 500 and 1GB.

Achieving a frametime of 8 - 16ms, means that even a high-end GPU will be quite busy to fill up a G-Buffer this size. So thinking about splitting this between two GPUs might make sense.

A high-end PostFX pipeline is now < 5ms on medium-class GPUs but dedicating a whole high-end GPU means we can finally switch on the movie settings :-)

A GPU particle system can easily saturate a GPU with 16 ms ... especially if it is not rendering in a quarter size resolution.

For Lights and shadows it depends on the number of lights that should be applied. Caching all the shadow data in partially resident textures or cube maps or any other shadow map technique will hit the memory budget of this card substantially.




Now with more modern APIs like DirectX 12 and probably Vulcan and before that CUDA, splitting up the rendering pipeline can happen in the following way:

- GPU0 - fills up the G-Buffer after a Z pre-pass

- GPU1 - Renders Deferred Lights and Shadows

- GPU2 - Renders Particles and Vegetation

- GPU3 - Renders Screen-Space Materials like skin etc. and PostFX

Now you can use the result of GPU0 and feed it to GPU1 and then feed it to GPU2 and so on. All this will run in parallel but will introduce two or three frames of lag (depending on how you light Particles and Vegetation). As long as the system renders 60 fps or 120 fps this will not be as much noticeable (obviously one of the targets is to have a high framerate to make animations look smooth and then also having 4K resolution rendering). GPU4 and higher can work on Physics, AI and other things. There is also the opportunity to spread out G-Buffer rendering over several GPUs, like one GPU is doing the Z pre-pass, then another fills up diffuse, normal and probably some geometry data to indentify different objects later or store their edges and another GPU is filling up the terrain data. Vegetation can be rendered on a dedicated GPU etc. etc.. On the CPU side the rule of thumb is that at least 2 cores are needed for one GPU. It is probably better to go for 3 or four. So a four GPU machine should have 8 - 16 CPU cores and a eight GPU machine 16 - 32 CPU cores; which might be split between several physical CPUs. We need at least 2x as much CPU RAM as the GPUs have RAM, so if four GPUs have each 2 GB, we need at least 16 GB Ram, if we have eight GPUs, we need at least 32 GB RAM etc..

A 4K resolution consists of 3840 × 2160 pixels and it will occupy with four render targets, each 32-bit per pixel (8:8:8:8 or 11:11:10), roughly 126.56 MB. This number goes up with 4x or 8x MSAA and maybe super-sampling. It is probably save to assume that the G-Buffer might occupy between 500 and 1GB.

Achieving a frametime of 8 - 16ms, means that even a high-end GPU will be quite busy to fill up a G-Buffer this size. So thinking about splitting this between two GPUs might make sense.

A high-end PostFX pipeline is now < 5ms on medium-class GPUs but dedicating a whole high-end GPU means we can finally switch on the movie settings :-)

A GPU particle system can easily saturate a GPU with 16 ms ... especially if it is not rendering in a quarter size resolution.

For Lights and shadows it depends on the number of lights that should be applied. Caching all the shadow data in partially resident textures or cube maps or any other shadow map technique will hit the memory budget of this card substantially.

*Note: I wrote this more than two years ago. At the time a G-Buffer was a valid solution for designing a rendering system. Now with the high-res displays it is not anymore.*
## 4 comments:

You mention G-buffer not being a valid solution for a rendering system. Is this because of the bandwidth requirements for 4K resolution? Or because of other reasons?

Both and memory. A 4K G buffer occupies too much memory

Excuse me, could you tell what alternative approach you can recommend instead of G-buffer?

Sorry for the late reply. You can find articles on "Visibility Buffer" based rendering from Intel and Christoph Schied. You might want to check them out. We -Confetti- will open-source a solution very soon.

Post a Comment