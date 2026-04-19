---
title: Play 3D Blu-Ray in SBS Directly From the Disc for Playback on 3D Monitors,
  XR Glasses, and VR Headsets, Using Free and Open Source Tools
url: https://cybereality.com/play-3d-blu-ray-in-sbs-directly-from-the-disc-for-playback-on-3d-monitors-xr-glasses-and-vr-headsets-using-free-and-open-source-tools/
author: Cybereality
published: '2025-04-28'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/4b001614f5ce7a52.jpg)

One thing that’s been driving me crazy since the last “wave” of 3D died, is that lots of the associated content kinda got lost with it. This is what sorta happened with Blu-Ray 3D. While films continue to come to theaters in 3D, and get a disc release, it’s incredibly difficult to play the discs on modern stereoscopic hardware, like popular XR glasses, or the new “glasses free” 3D monitors that are just now coming out. Searching online led to me various social media posts, most of them only partially working, or outdated. After a few days of research, though, I think I’ve discovered the correct free tools and settings needed to playback 3D films directly from the disc, and view them in SBS 3D on modern hardware.

In order to complete this guide, you’ll need a Windows PC (with a newer GPU), a USB (or internal) Blu-Ray disc drive, and a stereo 3D display device that can accept a standard SBS (side-by-side) signal. Now simply follow these steps below to install the required software, installed in this order.

- Download the
[K-Lite Codec Pack (Standard)](https://codecguide.com/download_k-lite_codec_pack_standard.htm). - If it asks you to uninstall old LAV Filters, click Yes.
- Default options are fine, just keep clicking Okay.
- Install the
[Intel Media SDK DLLs](https://codecguide.com/download_other.htm#libmfxsw). - Download and run the latest
[LAV Filters installer](https://github.com/nevcairiel/lavfilters/releases). **IMPORTANT:**Select “H.264 MVC 3D Decoder”.- Download
[madVR](https://forum.doom9.org/showthread.php?t=146228)from Doom9. - Extract the folder to a permanent location.
- Then right-click “install.bat” and “Run as Admin”.
- Download and install
[Media Player Classic (MPC-HC x64)](https://github.com/mpc-hc/mpc-hc/releases/tag/1.7.13) - Open MPC-HC (not the newer Media Player Classic).
- In the top menu, click View > Options.
- Under Playback > Output, select madVR for DirectShow Video.
- Select External Filters, add the following to the list (in this order).
- LAV Audio Decoder
- LAV Splitter
- LAV Splitter Source
- LAV Video Decoder
- madVR

- On each of them, select Prefer, then click Apply and OK.
- From the madVR folder, run “madHcCtrl.exe”.
- In the system tray, right click the icon and choose Edit Settings.
- Under devices, expand your display and select properties.
- Set 3D format to side-by-side.
- Under rendering > general settings, uncheck everything.
- On stereo 3d, select “enable stereo 3d playback” and “when playing 3d content”.
- For full-width SBS, open MPC-HC, go to View > PnS Frame Adjust > Edit.
- Add a new entry “Full Width SBS” with the Zoom settings at “2.0 -> 1.0”.
- Both MPC-HC and Media Player Classic should now playback 3D Blu-Ray.

![](../../assets/7a72a497d6ecb15b.jpg)

**WARNING:** This configuration only allows MVC encoded 3D video to display as SBS. Commercial 3D Blu-Ray discs are most likely protected, and will not playback on a PC without special hardware or software. It may also be a gray area, legally, depending on what country you reside in, so please do your own research.