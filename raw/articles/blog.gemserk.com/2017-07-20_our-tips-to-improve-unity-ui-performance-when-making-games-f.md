---
title: Our tips to improve Unity UI performance when making games for mobile devices
url: https://blog.gemserk.com/2017/07/20/our-tips-to-improve-unity-ui-performance-when-making-games-for-mobile-devices/
published: '2017-07-20'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

There is a Unity Unite talk named “[Unite Europe 2017 - Squeezing Unity: Tips for raising performance](https://www.youtube.com/watch?v=_wxitgdx-UI&list=PLX2vGYjWbI0Rzo8D-vUCFVb_hHGxXWd9j&index=9)” by [Ian Dundore ](https://www.linkedin.com/in/idundore)about things you can do in your game to improve Unity performance by explaining how Unity works behind the scenes.

Update: I just noted (when I was about to complete the post) there is another talk by Ian from Unite 2016 named “[Unite 2016 - Let’s Talk (Content) Optimization](https://www.youtube.com/watch?v=n-oZa4Fb12U)”, which has other good tips as well.

There are two techniques to improve Unity UI performance we use at work they didn’t mention in the video and we want to share them in this blog post. One of them is using [CanvasGroup](https://docs.unity3d.com/Manual/class-CanvasGroup.html) component and the other one is using [RectMask2D](https://docs.unity3d.com/ScriptReference/UI.RectMask2D.html).

## CanvasGroup

[CanvasGroup](https://docs.unity3d.com/Manual/class-CanvasGroup.html) component controls the alpha value of all the elements inside in its RectTransform hierarchy and whether that hierarchy handle input or not. The first one is mainly used for render purposes while the second one for user interaction.

What is awesome about CanvasGroup is, if you want to avoid rendering a hierarchy of elements, you can just put alpha in 0 and that will avoid sending it to render queue improving gpu usage, or at least that is what the FrameDebugger and our performance tests say. If you also want to avoid that hierarchy to consume events from the EventSystem, you can turn off the block raycast property and that will avoid all the raycast checks for its children, improving cpu usage. The combination of those two is important. It is also easier and more designer friendly than iterating over all the children with CanvasRender and disable them. Same thing to disable/enable all objects handling raycasts.

In our case, at work, we are using multiple Canvas objects and have all of them “disabled” (not being rendered nor handling input) using CanvasGroup alpha and block raycasts properties. That improves a lot the speed of activating and deactivating our metagame screens since it avoids regenerating the mesh and calculating layout again which GameObject SetActive() does.

## RectMask2D

The idea when using masks it to hide part of the screen in some way, even using particular shapes. We use masks a lot at work in the metagame screens, mainly to show stuff in a ScrollRect in a nice way.

We started using just Mask component, with an Image without Sprite set, to crop what we wanted. Even though it worked ok, it wasn’t performing well on mobile devices. After investigating a bit with FrameDebugger we discovered we had tons of render calls of stuff that was outside the ScrollRect (and the mask).

Since we are just using rectangle containers for those ScrollRects, we changed to use [RectMask2D](https://docs.unity3d.com/ScriptReference/UI.RectMask2D.html) instead. For ScrollRects with a lot of elements, that change improved enormously the performance since it was like the elements outside the mask weren’t there anymore in terms of render calls.

This was a great change but only works if you are using rectangle containers, doesn’t work with other shapes. Note that the [Unity UI Mask tutorial](https://unity3d.com/es/learn/tutorials/topics/user-interface-ui/ui-mask) only shows image masks and doesn’t say anything about performance cost at all (it should).

Note: when working with masks there is a common technique of adding something over the mask to hide possible ugly mask borders, we normally do that on all our ScrollRect that doesn’t cover all the screen.

## Bonus track: The touch hack

There is another one, a hack, we call it the Touch Hack. It is a way to handle touch all over the screen without render penalty, not sure it is a great tip but it helped us.

The first thing we thought when handling touch all over the screen (to do popup logic and/or block all the other canvases) was to use an Image, without Sprite set, expanded to all the screen with raycast enabled. That worked ok but it was not only breaking the batch but also rendering a big empty transparent quad to all the screen which is really bad on mobile devices.

Our solution was to change to use a Text instead, also expanded to all the screen but without Font nor text set. It doesn’t consume render time (tested on mobile devices) and handles the raycasts as expected, I suppose it is because it doesn’t generate the mesh (since it doesn’t have text nor font set) and at the same time still has the bounding box for raycasts configured.

# Conclusion

It is really important to have good tools to detect where the problems are and a way to know if you are improving or not. We use a lot the FrameDebugger (to see what was being drawn, how many render calls, etc), the overdraw Scene view and the Profiler (to see the Unity UI CPU cost).

Hope these tips could help when using Unity UI to improve even more the performance of your games.

# More

Optimizing Unity UI - [http://www.tantzygames.com/blog/optimizing-unity-ui/](http://www.tantzygames.com/blog/optimizing-unity-ui/)

A guide to optimizing Unity UI - [https://unity3d.com/es/learn/tutorials/temas/best-practices/guide-optimizing-unity-ui](https://unity3d.com/es/learn/tutorials/temas/best-practices/guide-optimizing-unity-ui)

Implementing Multiple Canvas Groups In Unity 5 - [http://www.israel-smith.com/thoughts/implementing-multiple-canvas-groups-in-unity-5/](http://www.israel-smith.com/thoughts/implementing-multiple-canvas-groups-in-unity-5/)