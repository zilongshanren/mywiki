---
title: Threading in Unity
url: https://cmwdexint.com/2018/06/06/threading-in-unity/
author: Ming Wai Chan
published: '2018-06-06'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

**Single ****thread**** / direct **** ****-force-gfx-direct**

- Main thread
- device


**Multi**

**–**

**thread**

**/ client+worker pair**

**-force-gfx-mt**

default, and if GraphicsJobs checkbox is off

- Main thread
- device
- client

- Render thread
- device
- worker


**Graphics Jobs / legacy **** ****-force-gfx-jobs legacy**

Cpu command – run in linear

Render command – run in parallel

- Main thread
- Render thread
- Job thread
- client on each job thread

**Graphics Jobs / native**


**-force-gfx-jobs native**

if GraphicsJobs checkbox is on.

if platform / API doesn’t support native then will fallback to legacy

only in player +

**Vulkan / DX12 / Metal**

Cpu command – run in parallel

Render command – run in parallel

- Main thread
- device
- client


- Render thread
- device
- worker


- Task execute
- Job thread
- N render thread