---
title: An Introduction to 360° Videos - Alan Zucconi
url: https://www.alanzucconi.com/2020/05/19/an-introduction-to-360-videos/
author: Alan Zucconi
published: '2020-05-19'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This online series will cover everything you need to know about 360° videos; from how to create them in Unity, to how to edit them in Premiere Pro in a format compatible with YouTube. Whether you want to create an immersive 360° video, or a trailer for your VR game, this is the tutorial for you. You will also learn how to create and edit Ambisonic tracks with Head-Lock stereo audio, which is perfect for 360° videos with narrated voiceovers.

If you are unfamiliar with 360° videos, you can have a look at one that I have recently created, which features a journey through all of the discovered exoplanets.

This online course is split into two modules. The first one will focus on how to create the videos in Unity, and is already available:

**Part 1.**[An Introduction to 360° Videos](https://www.alanzucconi.com/?p=11711)- Part 2.
[How to Create a 360° Video in Unity](https://www.alanzucconi.com/?p=11729)

The second module will focus on editing the videos, and will be released at a later time:

- Part 3. 🚧
[How to Edit a 360° Video in Premiere Pro](https://www.alanzucconi.com/?p=11758) - Part 4. 🚧 How to Edit Ambisonic Audio in Premiere Pro
- Part 5. 🚧 How to Record Ambisonic Audio in Unity

A link to download a working Unity scene can be found at the end of this page.

## Why 360° Videos?

Most of the articles on this blog are targeted to game developers. If you are one of them, you might wonder why creating 360° videos should be of any interest to you. Virtual Reality is a very successful industry, with more and more VR games being released every year across a variety of different platforms. Many players will find out about VR games via trailers, which are unfortunately 2D.

If you want to be a step further, you could actually create an additional 360° video trailer to showcase your game at its full potential. While playing a VR game usually requires an expensive headset, 360° videos are natively supported by YouTube without the need for any additional equipment. And if you have a phone, you can also turn it into a VR headset very easily with [Google Cardboard](https://arvr.google.com/cardboard/).

This can give people a much more immersive experience, and a tasty preview of what your game is really about. Movies such as “IT” (below) and “The Conjuring” have taken full advantage of that, creating VR games (with their respective 360° video trailers) to provide a more interactive experience.

Lastly, 360° videos are very good for educational purposes, as shown in [All Discovered Exoplanets: A Narrated 360 VR Journey](https://www.youtube.com/watch?v=eH_ud3jIKcg).

## Understanding 360° Videos

It is safe to assume that you are all familiar with YouTube, and how it works. Fewer people, however, might be familiar with 360° videos. Most videos are recorded using a camera, which only captures a small portion of its surroundings. 360° videos, instead, somehow record what is happening in every direction at the same time. They typically require special cameras, called [omnidirectional cameras](https://en.wikipedia.org/wiki/Omnidirectional_camera). They work by either using curved mirrors to reflect the surroundings into a traditional camera (pretty much like a fisheye lens would), or by using multiple cameras pointing in different directions. One such camera is, for instance, the GoPro Omni (below) which is literally a rig that holds six standard cameras, with fisheye lenses.

![](../../assets/8a06830ec6e7717e.jpg)

It is easy to understand why the hardware necessary to record a 360° video is typically more expensive, compared to a traditional camera. That, however, is not the only reason that is limiting their diffusion. 360° videos need special software and hardware to be played correctly. Screens, pretty much like cameras, are only intended to reproduce a small fraction of your surrounding. YouTube managed to get around this limitation by allowing viewers to “rotate” the video, so that you can look around. If you are watching a 360° video from a phone or a tablet, you can typically move it in space to look at different parts of the 360° “sphere”.

YouTube supports two different types of 360° videos: **mono** and **stereo** (with the latter often referred to as **virtual reality videos**). The difference is that stereo VR videos are designed for VR headsets, and can provide a sense of depth that you cannot experience with traditional videos. This is achieved by providing not one, but two videos: one for each eye. These two videos are captured at the same time by two cameras, which distance is comparable to the distance between the eyes. As a result, VR videos can trick the brain into perceiving true distance, pretty much as you normally would in your everyday life.

The table below shows the different requirements that those two types of videos have.

| Name | 360° video | Virtual Reality Video |
|---|---|---|
| Mono | Stereo | |
| 2D | 3D | |
Link |
|

[Support](https://support.google.com/youtube/answer/6316263?hl=en-GB&ref_topic=9257783)**Framerate****Format**2:1 aspect ratio

1:1 aspect ratio

**Resolution**up to 8192 x 4096

up to 8192 x 8192

Please, bear in mind that YouTube is constantly working to improve its 360° support, so they might change in the near future. Before committing to any of those specifications, double-check with the links provided.

## Video Projection

The first challenge that 360° videos have to overcome is how to encode a sphere into a flat surface. This is necessary because even though omnidirectional cameras can record in all directions, each frame still needs to be converted into a traditional flat image.

There are many ways to “remap” (technically, to **project**) a sphere into a rectangle. The most well-known one is probably the **cylindrical projection**, which was popularised in when the cartographer Marcator Geradus started using it in 1569 to remap the surface of the planet onto flat maps.

The most commonly used for 360° videos, however, is the **equirectangular projection** (below).

![](../../assets/2e4b066de7f684f5.jpg)

## Spatial Audio

360° videos, both mono and stereo, can support **spatial audio**. Standard videos include two audio channels (Left and Right) which are used to have a sense of directionality when listened with stereo headphones. Spatial audio, instead, allows encoding the proper direction a sound comes from, beyond a simple left/right. This means that providing you are using appropriate equipment, you can have a truly immersive experience with full depth perception and directional sounds all around you.

Despite the name, VR videos are not as good as “proper” VR games. This is because even if the VR headset you are using can track your head, the video is rendered from a fixed location. You cannot move your head to see what is behind an object, as you would in a VR game. This can feel a bit disorienting, especially when coupled with spatial audio. When you are working for a long time on a VR project (either a game or a video) you might get used to it. It is important to have enough playtesting sessions to ensure your final product can be accessible, and limits any discomfort to your players or viewers.

A 360° video does not necessarily need to have spatial audio. If you need to, YouTube supports two formats:

- First-Order Ambisonics
- First-Order Ambisonics with Head-Locked Stereo

**Ambisonics** is an audio format that is used to record not just a sound, but also the direction it comes from. The **First-Order Ambisonics** (FOA) uses four audio channels to encode the directionality of an audio source. To get a rough idea of how it works, recording FOA audio is a bit like recording a sound using four microphones. A common misconception is imagining those four microphones placed at the four cardinal points (one in front of you, one behind you, one to your left, and one to your right). Ambisonics does not work like that, but there will be plenty of time to discuss that in a later post.

While FOA uses 4 channels, YouTube also supports a 6 channel version, which simply adds the traditional left/right stereo channels. This format is known as **FOA with Head-Locked Stereo**.

Particular attention needs to be paid when encoding a 360° video (either stereo or mono), because not all formats support 4 or 6 audio channels. YouTube suggests the following:

- Format: MP4, MOV
- Codec: H.264, ProRes, DNxHR

If you are using Premiere Pro 2018 or above, the best way is to encode your video as Quicktime, using a ProRes code. You can read more about YouTube supported format for spatial audio [here](https://support.google.com/youtube/answer/6395969).

## What’s Next…

This first post introduced 360° videos: how they work, and what you can do with them. In the next instalment of this online course, you will learn how to create them in Unity.

**Part 1.**[An Introduction to 360° Videos](https://www.alanzucconi.com/?p=11711)- Part 2.
[How to Create a 360° Video in Unity](https://www.alanzucconi.com/?p=11729)

The second module will focus on editing the videos, and will be released at a later time:

- Part 3. 🚧
[How to Edit a 360° Video in Premiere Pro](https://www.alanzucconi.com/?p=11758) - Part 4. 🚧 How to Edit Ambisonic Audio in Premiere Pro
- Part 5. 🚧 How to Record Ambisonic Audio in Unity

## Download

You can download the script used for this tutorial on [Patreon](https://www.patreon.com/posts/32886275/).

## Leave a Reply Cancel reply