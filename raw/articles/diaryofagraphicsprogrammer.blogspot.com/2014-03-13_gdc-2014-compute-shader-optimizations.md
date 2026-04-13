---
title: GDC 2014 - Compute Shader Optimizations
url: http://diaryofagraphicsprogrammer.blogspot.com/2014/03/gdc-2014-compute-shader-optimizations.html
author: Wolfgang Engel
published: '2014-03-13'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I will be speaking at the Sony booth on Wednesday at 5pm on compute shader optimizations. The 15 minute talk will be broadcast on Twitch.

The talk will cover performance numbers of three different AMD GPUs: RADEON 6770, RADEON 7750 and RADEON 7850.

The main topics are:



The talk will cover performance numbers of three different AMD GPUs: RADEON 6770, RADEON 7750 and RADEON 7850.

The main topics are:

- Sequential Shared Memory (TGSM) Access: utilizing the Memory bank layout
- When to Unroll Loops in a compute shader
- Overhead of address arithmetic and loop instructions
- Skipping Memory Barriers: Wavefront
- Pre-fetching data into Shared Memory
- Packing data into Shared Memory

Looking at two different generations of AMD GPUs makes it better visible which one of the ground rules developed for GPU optimizations works on current GPUs, compared to previous generations.

This is based on some of the optimization work we did on AAA games last year.

At Confetti we have Aura - our Dynamic Global Illumination System- and PixelPuzzle - our PostFX pipeline - running in compute.

This talk will deal with how to optimize parts of a PostFX pipeline with Compute. I am also planning to write a blog series about this.

## 6 comments:

Rats! I will be covering the Qualcomm Adreno Graphics Tools booth from 2-6 on Wed and won't be able to see your talk.

I can send you the slide deck and then we can talk about it and geek out :-)

Looking forward to your presentation. If you can provide a link to the Live Stream on Twitch sometime before 5 PM on Wednesday or if you decide to upload the talk/slides somewhere then that would be very greatly appreciated by me & others. Thanks. :-)

Seems like Sony stopped recording the talks already the day before my talk ... so there is no Twitch stream unfortunately.

Could you post the slides? I don't think I will be programming for PS4 in the near future, but still I'm curious :-)

It was not PS4 specific. It was targeting PC AMD GPUs ... you can find most of the talk now in the blog entry above.

Post a Comment