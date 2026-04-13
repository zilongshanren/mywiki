---
title: Rendering antialiased shadows with moment shadow mapping
url: http://momentsingraphics.de/GDCEurope2016.html
published: '2016-01-01'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Rendering antialiased shadows with moment shadow mapping

Christoph Peters.

2016–08 in *Game Developers Conference Europe 2016*. One hour lecture.

[Official version](https://gdcvault.com/play/1023864/Rendering-Antialiased-Shadows-with-Moment)

## Abstract

Shadow map aliasing is a common artifact in games. Moment shadow maps can improve on this situation. Similar to exponential variance shadow maps, they can be filtered and antialiased directly. However, they offer reduced light leaking and greater robustness at comparable cost. Since they scale well to high output resolutions, they are particularly attractive for virtual reality and 4k rendering.

The session will explain when to utilize moment shadow maps, how they work and how to implement them. It will also explain how they can be used to render contact-hardening soft shadows with large penumbrae and convincing crepuscular rays.

**Keywords:** filterable shadow maps, moment shadow mapping, participating media, real-time rendering, real-time shadows, single scattering, soft shadows, translucent occluders, lecture, talk, explanation

## Takeaway

Attendees will learn the circumstances under which their games can benefit from moment shadow mapping, best practice for their implementation and how they can be used for filtered hard shadows, shadows for translucent occluders, soft shadows and crepuscular rays.

## Intended audience

The indended audience for this talk is graphics programmers who are looking for new ways to improve the visual fidelity of their games. The talk includes a recap of shadow mapping basics, however some prior experience with shadow mapping is recommended for attendees.

## Flash forward (79 seconds)

## Lecture video with audio (53 minutes)

## Downloads

[PowerPoint slides](http://momentsingraphics.de/Media/GDCE2016/MomentShadowMappingGDCE2016.pptx)(highest quality but require a[PowerPoint viewer](http://www.microsoft.com/en-us/download/details.aspx?id=13)and an[h.264 codec](https://sourceforge.net/projects/x264vfw/files/))[Lecture video with audio narrations](http://momentsingraphics.de/Media/GDCE2016/MomentShadowMappingGDCE2016.mp4)(save link as, 53 minutes)[Static PDF version with notes](http://momentsingraphics.de/Media/GDCE2016/MomentShadowMappingGDCE2016.pdf)(lacks videos and animations)[Demo with documented shader code](http://momentsingraphics.de/Media/JCGT2016Demo/MSMDemoV2.zip)