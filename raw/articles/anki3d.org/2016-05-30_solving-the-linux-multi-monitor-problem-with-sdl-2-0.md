---
title: Solving the Linux multi-monitor problem with SDL 2.0
url: https://anki3d.org/solving-the-linux-multi-monitor-problem-with-sdl-2-0/
author: Panagiotis Christopoulos Charitos
published: '2016-05-30'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

A few days back I decided to upgrade my Ubuntu 14.04 LTS to Ubuntu 16.04 LTS and the first thing I did, after the upgrade, was to re-build and test AnKi. Everything seemed to work fine except the fullscreen mode. In my dual-monitor setup and with 14.04 SDL was creating a fullscreen SDL_Window in my primary monitor and the second monitor was left alone. In 16.04 though the fulscreen window covered both the monitors and it was placed in a very odd position. This is the code I’m using to create the SDL_Window:

U32 flags = SDL_WINDOW_OPENGL; if(init.m_fullscreenDesktopRez) { flags |= SDL_WINDOW_FULLSCREEN_DESKTOP; } m_impl->m_window = SDL_CreateWindow(&init.m_title[0], SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, init.m_width, init.m_height, flags);

I spend quite a few hours trying to understand the issue and after some digging I found out that SDL was reporting only one display (SDL_GetNumVideoDisplays) with the resolution of my entire desktop. Obviously that was wrong. After trying different stuff I found out the culprit. Apparently SDL 2.0 is using libxinerama.so to query some information related to multi-monitor setups. Since my Ubuntu installation was brand new I didn’t have that library installed. That didn’t stop SDL from building but querying multiple monitors was not working properly.

Hopefully this sort post will help people that have similar problems. If you have multiple monitors and you are using SDL 2.0 install libxinerama-dev.

You should also install libxrandr-dev (xrandr is used for similar purposes, but AFAIK is more flexible/powerful and widely supported nowadays).