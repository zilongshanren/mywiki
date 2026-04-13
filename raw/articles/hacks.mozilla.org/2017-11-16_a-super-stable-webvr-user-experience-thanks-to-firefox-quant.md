---
title: A super-stable WebVR user experience thanks to Firefox Quantum – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2017/11/a-super-stable-webvr-user-experience-thanks-to-firefox-quantum/
author: Salva
published: '2017-11-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

On Tuesday, Mozilla released Firefox Quantum, the 57th release of the Firefox browser since we started counting. This landmark release replaces some core browser components with newer, faster and more modern implementations. In addition, the Quantum release incorporates major optimizations from Quantum Flow, an holistic effort to modernize and improve the foundations of the Firefox web engine by identifying and removing the main sources of jank without rewriting everything from scratch, an effort my colleague Lin Clark describes as “[a browser performance strike force](https://hacks.mozilla.org/2017/11/entering-the-quantum-era-how-firefox-got-fast-again-and-where-its-going-to-get-faster/).”

Quantum Flow has had an important and noticeable effect on WebVR stability as you can see in the following video:

This video shows the execution profiles of the [Snowglobe](https://2017.ronikdesign.com/?camera=fps) demo while running [Speedometer](http://browserbench.org/Speedometer/) in the background to simulate the effect of multiple tabs open in a regular scenario.

![](../../assets/aca220beeb43eeac.jpg)


![](../../assets/aca220beeb43eeac.jpg)

The intermittent flashes in Firefox 55 correspond to the wide gaps in which the VR system tries to bring the user to the safe space. Notice that in Quantum the effect does not happen, and the experience is smoother and more comfortable.

The difference is due to the fact that Quantum Flow has removed the bottlenecks interfering with the browser’s ability to send fresh images to the VR system on time.

To understand how comprehensive optimizations affect virtual reality presentation, it is necessary to know the strict requirements of VR systems and to understand the communication infrastructure of Firefox.

## The VR frame

In the browser, regular 3D content is displayed at 60 Hz. This implies that the web content has around 16.6 ms to simulate the world, render the scene, and send the new image to the browser compositor thread. If the web page meets the 16.6 ms deadline, the frame rate will be a constant 60 fps (frames per second) and the animations will run smoothly and jank-free.

![](../../assets/340acd0691249668.png)


![](../../assets/340acd0691249668.png)

VR content is displayed at 90 Hz so the rendering time for VR is reduced to 11.1 ms. In WebVR, the web content sends the rendered frames to a dedicated WebVR thread.

More important, in VR, we should take into account a fact previously ignored: The delay between when a web page starts rendering the VR scene and when a new image is displayed in the headset has a direct impact on the user’s perception.

This happens because the scene starts to render after placing the camera at the beginning of the frame based on the user’s head position, but the scene is displayed a little bit after, with just enough time for the user to change their orientation. This delay is known as [motion-to-photon](https://xinreality.com/wiki/Motion-to-photon_latency) latency and can cause dizziness and nausea.

![](../../assets/07662983ff48208d.gif)


![](../../assets/07662983ff48208d.gif)

Fortunately, VR systems can partially fix this effect without increasing latency, by warping the rendered scene before displaying it in the headset, in a process known as [reprojection](https://xinreality.com/wiki/Timewarp).

However, the lower the latency, the more accurate the simulation. So, to reduce latency length, the browser does not start rendering immediately after showing the last frame.

![](../../assets/82d65f5af3b1d37b.png)


![](../../assets/82d65f5af3b1d37b.png)

Instead, it asks the VR system for a waiting period to delay rendering the scene.

![](../../assets/534d77d5dd99e1ea.png)


![](../../assets/534d77d5dd99e1ea.png)

As discussed below, web content and the WebVR thread run in different processes but they need to coordinate to render the scene. Before Quantum Flow, communication between processes came with the potential risk of becoming a bottleneck. In the VR frame, there are two critical communication points: one after waiting, when WebVR yields the execution to the web page for rendering the scene; and another, after rendering, when the web content sends the frame to the WebVR thread.

An unexpected delay in either would cause the motion-to-photon latency to peak and the headset would reject the frame.

## Inter-process communication messages in Firefox

Firefox organizes its execution into multiple processes: the *parent process*, which contains the browser UI and can access the system resources; the *GPU process*, specifically intended to communicate with the graphics card and containing the Firefox compositor and WebVR threads; and several *content processes*, which run the web content but can not communicate with other parts of the system. This [separation of processes](https://hacks.mozilla.org/2017/06/firefox-54-e10s-webextension-apis-css-clip-path/) enable future increases in browser security and prevents a buggy web page from crashing the entire browser.

![](../../assets/cc33f8c77ddee363.png)


![](../../assets/cc33f8c77ddee363.png)

Quite often, processes need to communicate with each other. To do so, they use Inter-Process Communication (IPC) messages. An IPC message consists of three parts: 1) sending the request, 2) performing a task in the recipient, and 3) returning a result to the initiator. These messages can be synchronous or asynchronous.

We speak of synchronous IPC when any other attempt at messaging via IPC must wait until the current communication finishes. This includes waiting to send the message, completing the task, and returning the result.

![](../../assets/e2af097044962c25.gif)


![](../../assets/e2af097044962c25.gif)

The problem with synchronous IPC is that an active tab attempting to communicate with the parent process may block delivery. This forces a wait until the result of a different communication reaches the initiator, even when the latter is a background tab (and therefore, not urgent) or the ongoing task has nothing to do with the attempted communication.

In contrast, we speak of asynchronous IPC when sending the request, performing the task, and returning the result are independent operations. New communications don’t have to wait to be sent. Execution and result delivery can happen out-of-order and the tasks can be reprioritized dynamically.

![](../../assets/743b49e43bf8578e.gif)


![](../../assets/743b49e43bf8578e.gif)

One of the goals of Quantum Flow, over the course of Firefox 55, 56 and 57 releases, has been to [identify synchronous IPCs and transform them into asynchronous IPCs](https://bugzilla.mozilla.org/show_bug.cgi?id=SyncIPC#module-tracking-title). [Ehsan Akhgari](https://twitter.com/ehsanakhgari), in his series “[Quantum Flow Engineering Newsletter](https://ehsanakhgari.org/blog/2017-03-09/quantum-flow-engineering-newsletter-1)”, perfectly reviews the progress of the Quantum Flow initiative this year.

Now that we’ve explored the performance risks that come with synchronous IPC, let’s revisit the two critical communications inside the VR frame: the one for yielding execution to the web page to start rendering, and the one that sends the frame to the headset; both requiring an IPC from *GPU-to-content* and *content-to-GPU* respectively.

![](../../assets/3636bdd8ec70551b.png)


![](../../assets/3636bdd8ec70551b.png)

Due to the VR frame rate, these critical moments of risk happen 180 times per second. During the early stages of Quantum Flow in Firefox 55, the high frame rates, in addition to the background activity of other open tabs, increased the probability of being delayed by an ongoing synchronous IPC request. Wait times were not uncommon. In this situation, the browser was constantly missing the deadlines imposed by the VR gear.

After advancing Quantum Flow efforts in Firefox 56 and 57, the ongoing removal of synchronous IPC reduces the chance of being interrupted by an unexpected communication, and now the browser does not miss a deadline.

Although Quantum Flow was not aimed specifically at improving WebVR, by removing communication bottlenecks new components can contribute effectively to the global performance gain. Without Quantum Flow, it does not matter how fast, new or modern the browser is, if new features and capabilities are blocked waiting for unrelated operations to finish.

And thus, Firefox Quantum is not only the fastest version of Firefox for 2D content rendering, it is also the browser that will bring you the most stable and comfortable viewing experience in WebVR so far. And [the best is yet to come](https://research.mozilla.org/mixed-reality/).

## About
[
Salva ](https://salvadelapuente.com)

Front-end developer at Mozilla. Open-web and WebVR advocate, I love programming languages, cinema, music, video-games and beer.

## 2 comments

Pete MarkiewiczNovember 17th, 2017 at 11:07Koprowski.itNovember 18th, 2017 at 07:47