---
title: Simonschreibt.
url: https://simonschreibt.de/wft/terminate-software-like-a-pro/
author: Simon
published: '2022-11-14'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

We all know it: Photoshop, 3DsMax or any [#gamedev](https://twitter.com/hashtag/gamedev?src=hashtag_click) Engine stops, freezes, turns white and doesn’t even let us press the X to close the software. Waiting for the “Close program”-dialog is annoying. **>:|**

Here is my workflow how I kill every software. **WITHOUT. WAITING!**

In my Taskbar, I have shortcuts like this. If I click them, the program is IMMEDIATELY closed. No matter if it’s hanging, freezing… These shortcuts link to a Scriptfile which use a “taskkill” command – DON’T WORRY if you don’t know what a Script is! It’s easy (and worth it)!

I promise: After you setup this, you’ll WISH for a software being frozen because it feels SO GOOD to click the Kill-Shortcut and see it close within a split-second!

First: Create a folder for the Scriptfiles. I usually put it into my Dropbox/GDrive/NextCloud-Folder so they are save (and shareable between Computers). Create a textfile in this folder. Rename this textfile to e.g. kill3DsMax.bat – You SHOULD see a dialog like this. Click “Yes”.

If it does not ask, it’s because you’re not seeing a file-extension (.txt). You need them by UNCHECKING in windows explorer: View > Options > View (Tab) > “Hide Extensions for known file types”

Now, rename the .txt into a .bat and open it in a text editor (e.g. notepad) and paste this command: `taskkill /f /t /im 3dsmax.exe.`


**/f**Forces the application to close**/t**Terminates also all child processes**/im**Makes it possible to names like 3dsmax.exe

Copy this file several times, rename it to e.g. `killPhotoshop.bat`

, `killUnity.bat`

, … – Open the files in notepad and change the .exe file you want to terminate by executing this specific script. If you double click the file(s), it will already work and close the software!

Now: Adding Shortcuts to the taskbar: Right-Click an EMPTY space in the taskbar and make sure it is NOT locked (NO checkmark in front of this menu).

Right-Click the taskbar AGAIN, create a new toolbar. Choose/Create a folder where the shortcuts will be placed (I sometimes put a new folder on the desktop when I have one of my crazy days [#clutteredDesktop](https://twitter.com/hashtag/clutteredDesktop?src=hashtag_click)).

Drag&Drop this line upward/left/right depending how your taskbar is oriented. I like mine vertical. (The line is NOT visible if the taskbar is locked!).

Drag&Drop your Bat-File(s) in there. Technically we’re done now BUT here come some Pro-Design-Tips!

Right-Click the Shortcut in the taskbar > Properties > Change Icon. Choose a nice happy icon.

Right-Click the double-line (which you just moved to see more) of your toolbar > and uncheck “Show title” and check “Small Icons”

Right-Click the Shortcut and rename it from e.g. “killMax.bat – Shortcut” to something like “kill 3DsMax :,)”

Also: you can assign this shortcut a shortcut (Right-Click the Shortcut > Properties)! [#killWithKeystrokeInsteadOfMouseclick](https://twitter.com/hashtag/killWithKeystrokeInsteadOfMouseclick?src=hashtag_click)

Done! Repeat all this with as many Bat-Files / Shortcuts you want and then eagerly wait for one of the programs to dare freezing in your face. I hope this helps – Let me know how it feels for you to press these buttons! 🔥