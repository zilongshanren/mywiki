---
title: Bronson Zgeb
url: https://bronsonzgeb.com/index.php/2021/10/16/low-power-mode-in-unity/
author: Bronson
published: '2021-10-16'
source_blog: Bronson Zgeb
source_site: https://bronsonzgeb.com
category: game programming
fetched: '2026-04-13'
---

# Low Power mode in Unity

![](../../assets/5db808c36061a077.png)

In this article, I’ll show some ways to lower the power consumption of your Unity apps and games. But first, let’s talk about why we might consider doing this.

## Why bother?

If you’re already on board, feel free to skip ahead. For the rest of you, let’s discuss the motivation for low-power apps.

If you’re building a mobile app lowering your power consumption means saving battery life. Mobile games use a lot of battery, and if your game is too greedy with a user’s battery, they won’t want to play. Additionally, the more power your app consumes, the more the device will heat up. Mobile devices have a thermal ceiling, which means that as a device heats up, it’ll begin to throttle the processor. In other words, the hotter your device is, the slower it’ll run. Although this isn’t entirely avoidable, we should do our best to mitigate the damage.

When you’re building desktop games, power consumption is less of an issue. However, it’s common for users to run voice chat apps like Discord or streaming apps like OBS alongside the game these days. When I play games with folks while chatting on Discord, I often notice their voice get choppy or cut out entirely when the game they’re running starts doing a lot of work. The problem, then, isn’t about lowering power consumption but rather about not hogging all the resources.

Finally, as it turns out, Unity is a pretty good platform for building all sorts of creative tools and applications. Often when you’re making tools, rendering at 30+ FPS is wasteful. Generally, you’re only required to render a frame when you receive an input event or something changes.

Let’s talk about why game engines use more power than standard apps.

## Why do game engines use so much power?

Most of the applications we use daily have a simple event loop at their core. If the application receives some input, it’ll consume it and, if necessary, redraw the window. However, games are different. Sure, they still have an event loop, but the world inside the game changes over time. As a result, games will process and render the world whether or not you interact with them. Of course, this is a generalization because there are plenty of games like Chess, Solitaire, Crosswords, Minesweeper, Rogue, etc., that also don’t need to update and render at 60 frames per second. In a way, this is my motivation for writing this article. So to use less power, we need to prevent Unity from updating and rendering so often while also keeping our app responsive.

Let’s explore the tools we have at our disposal.

## Target Frame Rate

The first option is to manipulate `Application.targetFrameRate`

. Setting this value will control the rate at which your application updates and renders. On the surface, this sounds like the answer to our problems, but there’s a caveat. Since modifying the target frame rate affects the rate at which our game updates, our app will feel unresponsive if we set it too low. Even if we crank it up when the inputs start streaming in, it takes too long to recognize the first input that increases the frame rate. But don’t fret! We can use this setting combined with others to get the results we want.

## On-Demand Rendering

Deep inside `UnityEngine.Rendering`

is a little class called `OnDemandRendering`

. This class enables users to control the rate at which our app renders independently from the update loop. In other words, the application will update at full speed but render less often. Since rendering is one of the most expensive operations, this is a big win. We do this by modifying `OnDemandRendering.renderFrameInterval`

. Setting this value will tell the engine only to render every Nth frame, where N is the value we set. That is, `OnDemandRendering.renderFrameInterval = 10`

will render every 10th frame.

Now let’s take it a step further and combine this with `Application.targetFrameRate`

. In doing so, we can maintain an update loop that’s fast enough to react to input while rendering fewer frames, thus saving a lot of power.

```
using UnityEngine;
using UnityEngine.Rendering;
public class PowerManager : MonoBehaviour
{
void Update()
{
if (Input.GetMouseButton(0))
{
```**// Render at full speed**
Application.targetFrameRate = 0;
OnDemandRendering.renderFrameInterval = 0;
}
else
{
**// Render every 2 seconds**
Application.targetFrameRate = 30;
OnDemandRendering.renderFrameInterval = 60;
}
}
}


Here’s a simple power manager. This script will render your application at one frame every two seconds unless the left mouse button is down. At that time, the render speed and update loop will be unbounded. However, if you test this right now, it won’t necessarily work. There’s one last piece of the puzzle to discover.

## VSync

VSync is an option that synchronizes your frame rate to your monitor’s refresh rate. For our purposes, this is important because it overrides all the other frame rate settings. That means that if VSync is on, `Application.targetFrameRate`

and `OnDemandRendering.renderFrameInterval`

are ignored. So we have to disable VSync to turn on low-power mode.

```
using UnityEngine;
using UnityEngine.Rendering;
public class PowerManager : MonoBehaviour
{
```**[SerializeField] bool _enableVSync;**
void Update()
{
if (Input.GetMouseButton(0))
{
**QualitySettings.vSyncCount = _enableVSync ? 1 : 0;**
Application.targetFrameRate = 0;
OnDemandRendering.renderFrameInterval = 0;
}
else
{
**QualitySettings.vSyncCount = 0;**
Application.targetFrameRate = 30;
OnDemandRendering.renderFrameInterval = 60;
}
}
}


By the way, when rendering at full speed, enabling VSync is up to you (or the user).

## Additional Tips

Here are a few quick tips:

- You can disable and re-enable the physics system at will through `Physics
**.**autoSimulation`. Doing this will save even more power. - Use `OnDemandRendering
**.**willCurrentFrameRender` to check if the current frame will render. Use this to visualize and debug how often your app renders. - Monobehaviours still execute `Update` when the current frame doesn’t render. That means that heavy operations can still consume a lot of power in the background. If possible, you can avoid this by disabling those components when in low power mode.

## Wrap Up

So we’ve seen that it’s relatively easy to toggle the low-power mode on and off. Now the question is, how do we use it? The answer is going to change on a case-by-case basis. Any time your game is paused or static, you can aggressively limit the power consumption. Even in non-static menus, you can moderately restrict the frame rate and benefit from reduced power usage.

**See the code and example project ****on GitHub****. Please ****join my mailing list**** to support my work. If you do, I’ll notify you whenever I write a new post.**

## Grzegorz Kiernozek

nice article, thank you 🙂

## bronson

you’re welcome!