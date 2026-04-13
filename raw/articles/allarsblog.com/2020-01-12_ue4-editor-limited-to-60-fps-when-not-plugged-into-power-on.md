---
title: UE4 Editor limited to 60 FPS when not plugged into power (on battery)
url: https://allarsblog.com/2020/01/12/ue4-framerate-limited-60fps-when-on-battery/
author: Michael Allar
published: '2020-01-12'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

As of Unreal Engine 4.24.1, the time this post was written, UE4's Editor will force itself to run at 60 FPS to prevent battery drain on any device that thinks it is currently running on some sort of battery.

This appears to be *Editor Only*. There **does not appear** to be any non-editor tick rate limit based on whether you are running on battery or not for standalone game run-times.

Unless you are in fringe territory, this generally only applies to laptops, but technically it is based off of a OS platform specific call that could be wrong for a variety of reasons.

The most common reason a machine may falsely identify as being ran on a battery appears to be the case of a desktop using an Uninterruptible Power Supply (UPS) that is being wrongly reported as an internal battery. A desktop machine running on a UPS should realize there is no internal battery and report to UE4 that this power source is not a system battery, but not all UPS manufacturers are compliant in this regard it seems.

A machine may throttle itself in a variety of ways when it determines that it is not plugged into power, but UE4's Editor itself also does a hard-coded throttle to 60FPS on it's own.

In order to override this behavior, you can set console variable r.DontLimitOnBattery to a non-zero value. The simplest way of doing this is running the console command:

```
r.DontLimitOnBattery 1
```


This will disable the max tick rate limit of 60.0 when running on battery.

If you want to limit to another tick/framerate limit while on battery, say 30.0 if you are trying to be even more conservative with your power, there is currently no way to change the built in battery limit rate without editing source code. You can however use another limiter instead, such as:

```
t.maxFPS 30
```


If you would like to change the hardcoded engine limit, you can do so in:

```
Engine\Source\Editor\UnrealEd\Private\EditorEngine.cpp Line 2001
// Laptops should throttle to 60 hz in editor to reduce battery drain
static const auto CVarDontLimitOnBattery = IConsoleManager::Get().FindTConsoleVariableDataInt(TEXT("r.DontLimitOnBattery"));
const bool bLimitOnBattery = (FPlatformMisc::IsRunningOnBattery() && CVarDontLimitOnBattery->GetValueOnGameThread() == 0);
if( bLimitOnBattery )
{
MaxTickRate = 60.0f; // Here is where you would change the battery limit
}
```