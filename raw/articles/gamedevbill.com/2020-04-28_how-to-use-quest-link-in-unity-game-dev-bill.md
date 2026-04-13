---
title: How to use Quest Link in Unity - Game Dev Bill
url: https://gamedevbill.com/how-to-use-quest-link-in-unity/
author: Bill
published: '2020-04-28'
source_blog: Game Dev Bill
source_site: https://gamedevbill.com/
category: game programming
fetched: '2026-04-13'
---

![Quest Link in Unity how-to](../../assets/5db5b20c9b024608.png)

A while ago I got an Oculus Quest and began developing in Unity for the headset. Only recently, however, did I get a computer that supported Link. Using Quest Link in Unity’s Play Mode has been a complete game changer.

With this new mode, I can now use the in-editor Play Mode to interact in VR. No player build required! Each change in code or content used to take minutes to build and deploy, now can be done in a couple seconds at most.

For a video version of these steps, see below.

I was expecting setup to be fairly straightforward, but it was not. I found a few forum posts that had most of the instructions that I needed, but couldn’t find a single source with current and complete info. So I decided to gather those notes, modify them to what worked for me, and post it here. Please ping me on [Twitter](https://twitter.com/gamedevbill) or [comment on the forum](https://forum.unity.com/threads/gamedevbill-tutorial-comment-thread.945515/) if anything isn’t working for you.

And if it is working, [a follow on Twitter](https://twitter.com/gamedevbill), a download of [my free shader graph node](https://assetstore.unity.com/packages/vfx/shaders/cartesian-coordinate-shader-graph-node-158568?aid=1011l3QFn), or a purchase of a [recommended ](https://assetstore.unity.com/packages/3d/vegetation/the-illustrated-nature-153939?aid=1011l3QFn)[asset ](https://assetstore.unity.com/packages/vfx/shaders/nodes-for-shader-graph-124611?aid=1011l3QFn)is always appreciated.

These should be valid for Unity 2019.3+

###### T*his article may contain affiliate links, mistakes, or bad puns. Please read the *[disclaimer](https://gamedevbill.com/disclaimer/) for more information.

[disclaimer](https://gamedevbill.com/disclaimer/)for more information.

## How to Setup Quest Link in Unity

I’ll go into details below, but at a high level, here are the steps needed to setup Quest Link in Unity:

- Ensure you have a
[powerful enough computer](https://support.oculus.com/444256562873335/)and[the right (10ft) cable](https://www.amazon.com/gp/product/B01E9W8KYC/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01E9W8KYC&linkCode=as2&tag=gamedevbill0e-20&linkId=fd75df3c2e54879b74f49ebee2604a98) - Install
[Oculus Desktop](https://www.oculus.com/setup/#quest-setup) - Open the Rift home screen in your headset.
- Open or create VR/XR Unity project
- Install Oculus XR form package manager.
- Switch to Android or Standalone platform.
- In Player Settings, add Oculus Loader to the XR Plugin Management.
- Press the Play button in Unity. Put the headset on.

## Step 1: Get the Right Hardware

Oculus Link is in beta, but you can see the [latest hardware requirements on the Oculus website](https://support.oculus.com/444256562873335/). In addition to the right computer, you need the right cable. The one that shipped with your Quest will not do.

The official Oculus cable for Link is expensive, and generally sold out. So in its place, I [recommend this alternative](https://www.amazon.com/gp/product/B01E9W8KYC/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01E9W8KYC&linkCode=as2&tag=gamedevbill0e-20&linkId=fd75df3c2e54879b74f49ebee2604a98). Note that it comes in different sizes, but you almost certainly want the 10ft.

*October 2020 Update – I’ve had the alternative for about 7 months now, and it has started to have more disconnects. I’m not totally sure if it’s the cable or my computer. I have upgraded to the official cable, and things seem to be running more smoothly. It is still hard to find in stock, but if you are willing to pay the extra money, you could try here. Generally my recommendation is to get the cheaper one if you are just using it lightly, and the official one if it is a much more regular thing.*

## Step 2: Install Oculus Desktop

The Oculus Desktop software is built around the Rift. Originally you could only download it by going through the RiftS setup, but [now they have a dedicated download for the Link setup](https://www.oculus.com/setup/#quest-setup).

During setup, you’ll need to plug the headset in using that fancy USB cable mentioned above. As you go through the setup, Oculus Desktop will verify that the linkage is working and your system meets the requirements.

![Oculus desktop showing connected Quest](https://i1.wp.com/gamedevbill.com/wp-content/uploads/2020/04/devices.png?fit=760%2C453&ssl=1)

## Step 3: Open Rift Home Screen

There isn’t much to be done on this step other than make sure that it works. With the headset plugged into the computer, put it on, and hit the “Enable Link” button. This button should show up automatically when you plug in, but if it doesn’t, it’s available on main Quest toolbar near the battery power indicator (left side of toolbar).

Assuming you can see a very different home screen than the normal Quest home, you should be good to go. Just **make sure it is open in this mode before hitting play** in Unity.

## Step 4: Open or Create VR/XR Unity Project

I’m going to assume you’ve successfully set up your VR project. If that part throws you off as well, let me know in the comments or on Twitter and I can work on a how-to for that.

The main point i want to make here is to point out some aspects of your app that Link doesn’t care about, because I’ve seen some misleading info online. For one, you don’t actually need the Android settings in place. If you want to deploy a built player to the Quest you will need those settings, but not to use Link in play mode. You also don’t need to stick with the built in renderer. You should be able to use it or URP. I believe HDRP doesn’t yet support VR, but URP does.

![Unity HUB options for VR](../../assets/1158abe7e820793a.png)

## Step 5: Install Oculus XR Package

To get Unity to interact with the Oculus Desktop software, you need the Oculus XR package installed. This is available in *Window->Package Manger*. Note, many places online reference the Oculus Desktop package, but that info is out of date. The Oculus Desktop package is obsolete, and Oculus XR is what you now need.

![package manager showing XR Plugin](../../assets/eb57dfebb0ae33e5.png)

## Step 6: Switch to Standalone or Android

When you are using Link in play mode, it should work for any platform. Windows Standalone and Android are the main two I could think you’d care about, but it actually shouldn’t matter. The reason I have this step here at all, is not so much to make sure you take the step, but to make sure you know it’s not super important.

When running Oculus Link, your Quest is essentially emulating a Rift. Rift devices run on Windows, not on Android. And when you are in the editor, your editor is running on Windows. So at the end of the day, as long as play mode works, it should work in Link. For me, Standalone Windows works more reliably than Android, but that’s anecdotal, so take it for what it’s worth.

Many other setups I’ve seen mention being in Android mode. This is what mode you need to be in to build the player, and actually run it on-device. But this is not required to do Link in Play Mode.

![Unity build settings window](../../assets/a9a154508a38b9df.png)

## Step 7: Add Oculus Loader in Settings

To get play mode to connect to the actual device, it needs the proper settings configured.

- From the Build Settings window open Player Settings.
- Select XR Plugin Management
- Add Oculus Loader for whatever platforms you want to use. I recommend adding it to both standalone and Android to be safe.

![Unity Project Settings](../../assets/2ba623512e6c06b3.png)

## Step 8: Press Play. Wear Headset.

Lastly, hit play, and enjoy using your VR headset without leaving the comfort of your editor. Quest Link in Unity takes it from there.

![](../../assets/e0bc79269d5e2cfe.png)

## Wrapping up Oculus Link

Hope this helps. Using Quest Link in Unity is a huge time saver for anyone doing Quest development. If there are any issues, again, feel free to reach out on [Twitter. Or just reach out to say hi.](https://twitter.com/gamedevbill)

If you are doing some Quest development, be sure to check out my [shader tutorials](https://gamedevbill.com/shader-series/), especially the Shader Graph specific ones.

*Do something. Make progress. Have fun.*

## 1 comment on How to use Quest Link in Unity

## Comments are closed.