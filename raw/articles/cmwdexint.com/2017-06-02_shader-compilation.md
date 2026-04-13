---
title: Shader Compilation
url: https://cmwdexint.com/2017/06/02/shader-compilation/
author: Ming Wai Chan
published: '2017-06-02'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

**Import time** – when you create a .shader file

- compile the shader variants only when needed, etc. platform, variants

**Build time** – when you build a player

- [level 1] ShaderLab -> glsl or hlsl or …etc
- if platform supports, from [level 2] hlsl -> IL or MetalSL to AIR…etc

- Cache identical shaders under Library/ShaderCache
- compile only not-yet-ever-compiled shaders (variants for this platform only)

**Run time** – when you open the app

- [level 3] glsl or hlsl or IL or AIR…etc -> driver (GPU bytecode)
- because target device is unknown for PC/mobile at buildtime

- Depends on driver, when to compile these codes e.g. only when it’s used
- use shader pre-warm to “use” shaders to trigger compilation