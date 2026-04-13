---
title: VR development from the comfort of your regular environment – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2017/05/vr-development-from-the-comfort-of-your-regular-environment/
author: Salva
published: '2017-05-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

If, like me, you’re new at developing VR content, maybe you’ve recently switched to a Windows PC. Coming from Mac and Linux systems, I find switching to and from Windows can be an annoying experience. If this is your situation too, I’ve researched some setups that minimize and sometimes avoid disruptive context switches. Here’s a walkthrough of my setup for virtual reality development, that maintains the comfort of a familiar context.

## Run on Windows; use on Mac/Linux

[Remote Desktop Protocol](https://en.wikipedia.org/wiki/Remote_Desktop_Protocol) or RDP enables local computers to connect and control a desktop session on a remote Windows machine. RDP has very light overhead and is perfect for programming. However, VR development usually involves working with 3D modelling solutions, the kind of software that does not interact well with RDP.

In this brief video tutorial, I walk you through every step of the process for setting up RDP to enable your familiar dev environment. I’ll show you how to configure the MacOS RDP client, establish a remote session to a Windows PC, and overcome some graphic issues when launching modelling tools like [Magica Voxel](https://voxel.codeplex.com/) or [Blender](https://www.blender.org/). This may require some trade-off between comfort and responsiveness.

Check the [downloads section](https://hacks.mozilla.org#downloads) at the end of the article to find all the software you may need and pay special attention if your Windows version is Home Edition.

## Sharing your keyboard and mouse

I was working with this setup but **while trying to record some videos** I started to notice the effect of the RDP overhead, which caused unacceptable frame drops. To avoid this overhead, as you continue working with your regular mouse and keyboard, you can use a **virtual KVM** (kernel-based virtual machine) like [Share Mouse](http://www.keyboard-and-mouse-sharing.com/) to allow your Mac peripherals to control the Windows PC. However, if you want to use this, you will need to physically connect your Windows PC to your monitor.

If your regular development environment is Linux, you can use [Synergy](https://symless.com/synergy) instead, although notice ~~there is no free version~~.

**Edit**: thanks to [Avi Kac](https://hacks.mozilla.org#comment-21243) for reminding that synergy software is open source. So you [can clone the repository](https://github.com/symless/synergy), compile and install by your own.

## What’s next?

Much has changed since the last time I developed in Windows. I strongly recommend you read [Windows Development Environment](https://github.com/felixrieseberg/windows-development-environment/blob/master/README.md) before you begin. The guide includes installing a package provider for Windows, terminal setup, as well as other useful tools, tips and tricks, and offers a complete tutorial for getting started with modern Windows development.

Is it a perfect setup? Probably not for everyone, but it works for me. I would be interested in hearing what works for you. Please, join the conversation and tell us about your favorite setup in the comments or join the [WebVR Slack](https://webvr-slack.herokuapp.com/) to share with other practitioners.

## Downloads

If coming from Mac: [RDP client](https://itunes.apple.com/us/app/microsoft-remote-desktop/id715768417?mt=12), [TeamViewer](https://www.teamviewer.com/en/download/mac/) and [Share Mouse](http://www.keyboard-and-mouse-sharing.com/) for mouse and keyboard sharing.

If coming from Linux (not tested): [several RDP clients](http://www.techradar.com/news/5-of-the-best-linux-remote-desktop-clients) available, [TeamViewer](https://www.teamviewer.com/en/download/linux/) and [Synergy](https://symless.com/synergy) for mouse and keyboard sharing.

For the RDP solution to work in Windows Home Edition, you’ll need to install [RDP Wrapper](https://github.com/stascorp/rdpwrap/releases). Notice [it is not yet compatible](https://github.com/stascorp/rdpwrap/issues/194) with the latest Windows Creators Update.

## About
[
Salva ](https://salvadelapuente.com)

Front-end developer at Mozilla. Open-web and WebVR advocate, I love programming languages, cinema, music, video-games and beer.

## 10 comments

Tim SchaeferMay 31st, 2017 at 09:12Avi KavMay 31st, 2017 at 21:13Dr. PavelJune 1st, 2017 at 12:32UtopiahJune 3rd, 2017 at 02:59Avi KavMay 31st, 2017 at 20:57EduardoJune 1st, 2017 at 14:25SalvaJune 1st, 2017 at 23:04EduardoJune 1st, 2017 at 14:29Camilo MartinJune 16th, 2017 at 18:19SalvaJune 16th, 2017 at 22:55