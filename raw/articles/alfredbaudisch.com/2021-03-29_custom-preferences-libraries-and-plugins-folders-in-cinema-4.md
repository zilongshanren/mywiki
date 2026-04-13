---
title: Custom Preferences, Libraries, and Plugins Folders in Cinema 4D
url: https://alfredbaudisch.com/blog/custom-preferences-libraries-and-plugins-folders-in-cinema-4d/
author: Alfred Reinold Baudisch
published: '2021-03-29'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

All folders used by Cinema 4D can be pointed to a custom path, even the Preferences and Default libraries/browser directories, this is possible by adding some Environment Variables and adding a single parameter to the Cinema 4D shortcut (this is how you can move away from the C:/ hard drive and away from the AppData directory).

## Browser, Plugins and Scripts Paths

In Windows, right-click "This PC" (or "My PC"), go to *Properties* and choose *Advanced system settings*, then click *Environment Variables*.

In "System variables", click "New…" and in "Variable name" put one of the 3 values below. For the "Variable value" click "Browse Directory…" and go to the directory related to the variable name. Repeat this step three types, one for each of variable names below.

All the variables that you have to add:

```
C4D_BROWSERLIBS
C4D_PLUGINS_DIR
C4D_SCRIPTS_DIR
```


Source: [https://www.youtube.com/watch?v=pyrEevPPtRM](https://www.youtube.com/watch?v=pyrEevPPtRM)

## Custom Preferences Folder (Windows)

You have to add a custom parameter to your Cinema 4D shortcut. Before doing so, first copy your current Preferences folder to the new desired location (for example, another Hard Drive).

### Copy Current Folder

In Cinema 4D, go to Edit, Preferences. Then click "Open Preferences Folder…" at the bottom.

When the folder opens in Windows Explorer, copy all the contents and paste into your desired new folder. Close Cinema 4D.

### Make Cinema 4D use the new custom Preferences Folder Path

- Right-click a Cinema 4D shortcut and go to Properties.
- In "Target", inside double-quotes, you will have the path to the Cinema 4D executable.
- After the quotes, add a space and then
, example:`-g_prefspath`

=[custom preferences folder]

```
"C:\Program Files\Cinema 4D\Cinema 4D.exe" -g_prefspath=F:\Cinema4D\preferences
```


You can now delete the previous preferences folder. But, remember to always open the software from this shortcut.

## Coffee, Coins and Thumbs Up

If you like my content or if you learned something from it, [buy me a coffee](https://ko-fi.com/alfredbaudisch) ☕, [be my Patreon](https://www.patreon.com/alfredbaudisch) or simply check [all of my links](https://linktr.ee/alfredbaudisch) 🔗 and follow me/subscribe/star my repositories/whatever you prefer. If you want to learn Godot, be sure to check [my courses](https://alfredbaudisch.com/projects/education/dynamic-inventory-system-and-user-interfaces-with-godot-course/) 📚!

**Or you can simply add my game to your Steam Wishlist – that helps GREATLY and it's easy and free 🙂**