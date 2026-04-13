---
title: Simonschreibt.
url: https://simonschreibt.de/wft/watchdog-structure/
author: Simon
published: '2015-10-04'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Before you start creating the script you have to choose a scripting/programming language. I started with BAT-Files but later ported everything to C# because it runs faster and you have more functionality.

![](../../assets/a337b961fbdd9ba2.png)


The BAT-Syntax is sometimes a bit cryptic. For example this **%%~ni** (BAT) and this **Path.GetFileNameWithoutExtension(i)** (C#) does the same, where I think the latter is better read-able. **But** it was possible to do everything within a BAT-File, so if you have no idea about other languages, give it a try!

I write two programs: one compares the screenshots and sends out warning mails (**wd.exe**, abbriviation for “Watchdog”) while the other one creates HTML galleries and sends out performance warning mails (**wdg.exe**, abbriviation for “Watchdog Gallery”)

Both programs require some parameters and that’s why we created a **BAT**-File for each containing only one line and which look like that:

![](../../assets/7f4e5a887eb8bc5b.png)


wd.exe “C:\xrebirth\XRebirth.exe” “C:\Users\X Rebirth\Documents” “report@server.com” “-disablecockpit -disableui” “effecttest materials” “ep1open allzones_compass”

**Parameters**:

- Path to game EXE
- Path to documents directory
- Mail address/es where the error reports are send to
- Parameters for the game
- Parameters for the game to start different test-modules

wdg.exe “C:\Documents\X Rebirth\screenshots” “galleryReport@server.com” 50 “perfReport@server.com”

**Parameters**:

- Path to the directory where the screenshots are put into
- Mail address/es where the gallery creation report is sent to
- FPS threshold which defines how much tolerance you give until a performance warning is sent out
- Mail address/es where the performance reports are sent to

Both BAT-Files are executed every night by our build server. This should enough dry theory, let’s have a look how it actually works.