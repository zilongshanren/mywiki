---
title: 'UE4 4.5 UMG Workaround: UI loses focus when clicking on no widget'
url: https://allarsblog.com/2014/10/19/umgmenulosefocus/
author: Michael Allar
published: '2014-10-19'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

In 4.5 UMG if you set a player controller's input mode to UI Only when trying to show a modal widget, clicking in the empty/dead space of the viewport causes focus to shift back to the player controller. If you don't want this behavior, the easiest workaround is to set the root CanvasPanel's visibility in your modal widget to Visible instead of Self Hit Test Invisible. This will cause the CanvasPanel to absorb all click events, including the click event that would normally send your focus back to the player controller.

![Canvas Panel Visibility](../../assets/bb88a1d21e86108d.png)