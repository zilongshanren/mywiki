---
title: How I Fixed My App Taking 5 Minutes to Start
url: https://asawicki.info/news_1796_how_i_fixed_my_app_taking_5_minutes_to_start
published: '2025-12-22'
source_blog: Adam Sawicki Home Page - programming, graphics, games, media, C++, Windows,
  I...
source_site: https://asawicki.info/
category: graphics
fetched: '2026-04-19'
---

Mon

22

Dec 2025

I recently got a new Windows PC, which I use for development. I work on a game based on Unreal Engine, and I build both the game and the engine from C++ source code using Visual Studio. From the very beginning, I had an annoying problem with this machine: **every first launch of the game took almost five minutes.** I don’t mean loading textures, other assets, or getting into gameplay. I mean the time from launching the app to seeing *anything* on the screen indicating that it had even started loading. I had to wait that long every time I started or restarted the system. Subsequent launches were almost instantaneous, since I use a fast M.2 SSD. Something was clearly slowing down the first launch.

**Solution: open Windows Settings and disable Smart App Control.** This is a security feature that Microsoft enables by default on fresh Windows installations, and it can severely slow down application launches. If you installed your system a long time ago, you may not have it enabled. Once you turn it off, it cannot be turned back on - but that’s fine for me.

**Full story:** I observed my game taking almost five minutes to launch for the first time after every system restart. Before I found the solution, I tried many things to debug the problem. When running the app under the Visual Studio debugger, I noticed messages like the following slowly appearing in the Output panel:

'UnrealEditor-Win64-DebugGame.exe' (Win32): Loaded (...)Engine\Binaries\Win64\UnrealEditor-(...).dll. Symbols loaded.

That’s how I realized that loading each .dll was what took so long. In total, launching the Unreal Engine editor on my system requires loading 914 unique .exe and .dll files.

At first, I blamed the loading of debug symbols from .pdb files, but I quickly ruled that out, because launching the game without the debugger attached (Ctrl+F5 in Visual Studio) was just as slow - only without any indication of what the process was doing during those five minutes before anything appeared on the screen.

Next, I started profiling this slow launch to see what was happening on the call stack. I used the [Very Sleepy profiler](https://github.com/VerySleepy/verysleepy), as well as [Concurrency Visualizer extension](https://learn.microsoft.com/en-us/visualstudio/profiling/concurrency-visualizer?view=visualstudio) for Visual Studio. However, I didn’t find anything unusual beyond standard `LoadLibrary`

calls and other generic system functions. That led me to suspect that something was happening in kernel space or in another process, while my process was simply blocked, waiting on each
DLL load.

Naturally, my next assumption was that some security feature was scanning every .dll file for viruses. I opened Windows Settings → Protection & security → Virus & threat protection and added the folder containing my project’s source code and binaries to the exclusions list. That didn’t help. I then completely disabled real-time protection and the other toggles on that page. That didn’t help either. For completeness, I should add that I don’t have any third-party antivirus software installed on this machine.

I was desperate to find a solution, so I thought: what if I wrote a separate program that calls `LoadLibrary`

on each .dll file required by the project, in parallel, using multiple threads? Would that “pre-warm” whatever scanning was happening, so that launching the game afterward would be instantaneous?

I saved the debugger log containing all the “Loaded … .dll” messages to a text file and wrote a small C++ program to process it, calling `LoadLibrary`

on each entry. It turned out that doing this on multiple threads didn’t help at all - it still took 4–5 minutes. Apparently, there must be some internal mutex preventing any real parallelism within a single process.

Next, I modified the tool to spawn multiple separate processes, each responsible for loading every N-th .dll file. That actually helped. Processing all files this way took less than a minute, and afterward I could launch my game quickly. Still, this was clearly just a workaround, not a real solution.

I lived with this workaround for weeks, until I stumbled upon an article about the Smart App Control feature in Windows while reading random IT news. I immediately tried disabling it - and it solved the problem completely.

Apparently, Microsoft is trying to improve security by scanning and potentially blocking every executable and .dll library before it loads, likely involving sending it to their servers, which takes a very long time. I understand the motivation: these days, most users launch only a web browser and maybe one or two additional apps like Spotify, so every newly seen executable could indeed be malware trying to steal their banking credentials. However, for developers compiling and running large software projects with hundreds of binaries, this results in an egregious slowdown.